"""Validate Decision 024 criterion 11 against the accepted cell population.

Requires two pilot CSVs, then 16 full batch CSVs (cell and annual views).
Never interprets raw pasture-age code 1 or 100 as canonical origin.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


VERSION = "pasture-age-source-audit-v1"
PANEL_HASH = "ef3589be99e3a2cdc1c2245a15cedd090c8255775b34f14d4f2f27d3f9f8faa7"
SPATIAL_HASH = "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc"
N_CELLS = 24889
EXPECTED_TRANSBIOME = 582
YEARS = tuple(range(1985, 2026))
UNITS = ("pixel_equiv", "ha")
ANNUAL = ("raw_code1", "reuse100")
CELL_FIELDS = (
    "domain", "ever_pas", "audit_cohort", "raw_code1_any", "reuse100_any",
    "code1_outside_ever_pas", "raw_code1_years", "reuse100_years",
    "code1_pas_years", "code1_nonpas_years", "code1_uncertain_years",
    "code100_unresolved_years", "code100_nonpas_years", "new_entry_events",
    "reentry_events", "reentry_any", "reentry_two_plus",
    "max_reentry_duration_years", "reentry_duration_ge2",
    "reentry_duration_ge5", "joint_none", "joint_code1_only",
    "joint_reuse100_only", "joint_both",
)
JOINT = ("joint_none", "joint_code1_only", "joint_reuse100_only", "joint_both")
CELL_NUMERIC = tuple(f"{f}_{u}" for f in CELL_FIELDS for u in UNITS)
ANNUAL_NUMERIC = tuple(
    f"{name}_{year}_{unit}" for year in YEARS for name in ANNUAL for unit in UNITS
)
META = ("cell_id", "GRID_ID", "source_batch_id", "output_version")
TOL_HA = 1e-3
TOL_PIXEL = 1e-3


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_export(path, fields):
    require(path.is_file(), f"Missing GEE export: {path}")
    frame = pd.read_csv(path, dtype={"cell_id": "string", "GRID_ID": "string",
                                     "output_version": "string"}, low_memory=False)
    require(set(META + fields) == set(frame.columns),
            f"{path.name}: fields differ; missing={set(META + fields)-set(frame.columns)}; "
            f"unexpected={set(frame.columns)-set(META + fields)}")
    for col in ("cell_id", "GRID_ID"):
        require(frame[col].notna().all(), f"{path.name}: missing {col}")
        frame[col] = frame[col].astype(str).str.strip()
        require(frame[col].ne("").all(), f"{path.name}: empty {col}")
    require(frame.cell_id.is_unique, f"{path.name}: duplicated cell_id")
    require(frame.output_version.eq(VERSION).all(), f"{path.name}: wrong version")
    for col in fields + ("source_batch_id",):
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
        vals = frame[col].to_numpy(float)
        require(np.isfinite(vals).all() and np.min(vals) >= -1e-7,
                f"{path.name}: invalid {col}")
    require(frame.source_batch_id.between(0, 7).all() and
            np.max(abs(frame.source_batch_id - np.rint(frame.source_batch_id))) < 1e-7,
            f"{path.name}: invalid source batch")
    return frame


def aligned(cell, annual, label):
    require(len(cell) == len(annual) and set(cell.cell_id) == set(annual.cell_id),
            f"{label}: annual and cell populations differ")
    a = cell.set_index("cell_id").sort_index()
    b = annual.set_index("cell_id").reindex(a.index)
    require(a.GRID_ID.eq(b.GRID_ID).all() and
            a.source_batch_id.eq(b.source_batch_id).all(),
            f"{label}: annual/cell metadata differ")
    return a, b


def near(left, right, label, tolerance):
    delta = np.max(np.abs(np.asarray(left, float) - np.asarray(right, float)))
    require(delta <= tolerance, f"{label}: max residual={delta:.8g}")
    return float(delta)


def validate_pair(cell, annual, label):
    a, b = aligned(cell, annual, label)
    residual = 0.0
    for unit in UNITS:
        tol = TOL_HA if unit == "ha" else TOL_PIXEL
        col = lambda name: a[f"{name}_{unit}"].to_numpy(float)
        require((col("domain") > 0).all(), f"{label}: empty domain")
        residual = max(residual, near(
            col("audit_cohort"), sum(col(x) for x in JOINT),
            f"{label}: joint longitudinal partition ({unit})", tol))
        residual = max(residual, near(
            col("raw_code1_any"), col("joint_code1_only") + col("joint_both"),
            f"{label}: code1 union ({unit})", tol))
        residual = max(residual, near(
            col("reuse100_any"), col("joint_reuse100_only") + col("joint_both"),
            f"{label}: reused-100 union ({unit})", tol))
        residual = max(residual, near(
            col("raw_code1_years"), sum(
                col(x) for x in ("code1_pas_years", "code1_nonpas_years",
                                 "code1_uncertain_years")),
            f"{label}: coverage condition of code1 ({unit})", tol))
        for annual_name, cumulative in (("raw_code1", "raw_code1_years"),
                                         ("reuse100", "reuse100_years")):
            stacked = b[[f"{annual_name}_{y}_{unit}" for y in YEARS]].sum(axis=1)
            residual = max(residual, near(col(cumulative), stacked,
                f"{label}: 41-year {annual_name} ({unit})", tol))
        for subset, whole in (
            ("audit_cohort", "domain"), ("ever_pas", "audit_cohort"),
            ("raw_code1_any", "audit_cohort"), ("reuse100_any", "ever_pas"),
            ("code1_outside_ever_pas", "raw_code1_any"),
            ("reentry_any", "ever_pas"),
            ("reentry_two_plus", "reentry_any"),
            ("reentry_duration_ge5", "reentry_duration_ge2"),
            ("reentry_duration_ge2", "reentry_any"),
        ):
            require(np.max(col(subset) - col(whole)) <= tol,
                    f"{label}: {subset} exceeds {whole} ({unit})")
        require(np.max(col("reentry_events") - col("new_entry_events")) <= tol,
                f"{label}: reentry events exceed new entries ({unit})")
        for name in ANNUAL:
            for y in YEARS:
                require((b[f"{name}_{y}_{unit}"] <= col("domain") + tol).all(),
                        f"{label}: {name} {y} exceeds domain")
        if unit == "pixel_equiv":
            require((col("max_reentry_duration_years") <=
                     40 * col("reentry_any") + tol).all(),
                    f"{label}: invalid episode durations")
    return residual


def self_test():
    c = {"cell_id": "synthetic", "GRID_ID": "test", "source_batch_id": 0,
         "output_version": VERSION}
    for f in CELL_FIELDS:
        for u in UNITS:
            c[f"{f}_{u}"] = 0.0
    for u in UNITS:
        for name, v in {"domain": 10, "ever_pas": 7, "audit_cohort": 7,
                        "raw_code1_any": 2, "reuse100_any": 1,
                        "raw_code1_years": 3, "reuse100_years": 1,
                        "code1_pas_years": 3, "new_entry_events": 2,
                        "reentry_events": 1, "reentry_any": 1,
                        "max_reentry_duration_years": 2,
                        "reentry_duration_ge2": 1,
                        "joint_none": 5, "joint_code1_only": 1,
                        "joint_both": 1}.items():
            c[f"{name}_{u}"] = float(v)
    a = {k:c[k] for k in META}
    for col in ANNUAL_NUMERIC:
        a[col] = 0.0
    for u in UNITS:
        a[f"raw_code1_1986_{u}"] = 2.0
        a[f"raw_code1_1987_{u}"] = 1.0
        a[f"reuse100_1990_{u}"] = 1.0
    cell, annual = pd.DataFrame([c]), pd.DataFrame([a])
    validate_pair(cell, annual, "synthetic")
    broken = annual.copy()
    broken.loc[0, "raw_code1_1986_ha"] += 0.1
    try:
        validate_pair(cell, broken, "synthetic mismatch")
    except ValueError:
        pass
    else:
        raise AssertionError("Broken annual-to-cell closure passed")
    print("SOURCE AUDIT VALIDATOR SELF-TEST PASS")


def write_fixed(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    value = payload.encode("utf-8") if isinstance(payload, str) else payload
    if path.exists():
        require(path.read_bytes() == value,
                f"Existing versioned record differs: {path}")
    else:
        tmp = path.with_name(path.name + ".partial")
        try:
            tmp.write_bytes(value)
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=("pilot", "full"), default="pilot")
    ap.add_argument("--project-dir", type=Path, default=Path(
        "/content/drive/MyDrive/Trabalho/Contabilidade"))
    ap.add_argument("--raw-dir", type=Path, default=Path(
        "/content/drive/MyDrive/pasture_age_source_audit_raw_v1"))
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()
    self_test()
    try:
        from google.colab import drive
        drive.mount("/content/drive")
    except ImportError:
        pass
    project = args.project_dir
    out = args.output_dir or project / "spatial/phase9/pasture_age_source_audit_v1"
    panel_path = project / "panel/canonical_stock_flow_panel_1985_2025_v2.parquet"
    spatial_path = project / "spatial/phase1/canonical_spatial_support_v1.parquet"
    require(panel_path.is_file() and sha256(panel_path) == PANEL_HASH,
            "Corrected canonical panel is missing or differs")
    require(spatial_path.is_file() and sha256(spatial_path) == SPATIAL_HASH,
            "Accepted spatial support is missing or differs")
    ref = pd.read_parquet(panel_path, columns=["cell_id", "GRID_ID",
        "source_batch_id", "t0", "t1"])
    ref = ref.loc[(ref.t0 == 2020) & (ref.t1 == 2025),
                  ["cell_id", "GRID_ID", "source_batch_id"]].copy()
    # Phase 1 stores the two area fractions, not a transbiome_flag column.
    # Reproduce Phase 7's definition on the authenticated spatial support.
    spatial = pd.read_parquet(spatial_path, columns=["cell_id",
        "primary_biome", "amazon_fraction_cell", "cerrado_fraction_cell"])
    require(spatial[["amazon_fraction_cell", "cerrado_fraction_cell"]]
            .notna().all().all(), "Missing biome fractions")
    spatial["transbiome_flag"] = (
        spatial.amazon_fraction_cell.gt(0) &
        spatial.cerrado_fraction_cell.gt(0)
    ).astype("int8")
    require(int(spatial.transbiome_flag.sum()) == EXPECTED_TRANSBIOME,
            "Phase 7 transbiome population differs from the accepted count")
    spatial = spatial[["cell_id", "primary_biome", "transbiome_flag"]]
    for f in (ref, spatial):
        f.cell_id = f.cell_id.astype(str).str.strip()
    ref.GRID_ID = ref.GRID_ID.astype(str).str.strip()
    require(len(ref) == len(spatial) == N_CELLS and
            ref.cell_id.is_unique and spatial.cell_id.is_unique and
            set(ref.cell_id) == set(spatial.cell_id),
            "Accepted canonical populations differ")
    suffixes = ["pilot"] if args.mode == "pilot" else [f"b{b:02d}" for b in range(8)]
    if args.mode == "full":
        pilot_validation_path = out / "pilot_pasture_age_source_audit_validation_v1.json"
        require(pilot_validation_path.is_file(), "Pilot validation is required")
        pilot = json.loads(pilot_validation_path.read_text(encoding="utf-8"))
        require(pilot.get("status") == "PASS" and
                pilot.get("validator_revision") == "source-audit-validator-v2" and
                pilot.get("panel_sha256") == PANEL_HASH and
                pilot.get("spatial_sha256") == SPATIAL_HASH,
                "Pilot validation is invalid")
        for kind in ("cell", "annual"):
            path = args.raw_dir / f"canonical_pasture_age_source_audit_{kind}_pilot_v1.csv"
            require(pilot[f"pilot_{kind}_sha256"] == sha256(path),
                    "Pilot raw CSV changed since validation")
    cells, annuals, raw_hashes, max_residual = [], [], [], 0.0
    for suffix in suffixes:
        pair = {}
        for kind, fields in (("cell", CELL_NUMERIC), ("annual", ANNUAL_NUMERIC)):
            path = args.raw_dir / f"canonical_pasture_age_source_audit_{kind}_{suffix}_v1.csv"
            pair[kind] = read_export(path, fields)
            raw_hashes.append({"file":path.name, "sha256":sha256(path),
                               "rows":len(pair[kind])})
        cell, annual = pair["cell"], pair["annual"]
        if args.mode == "pilot":
            require(1 <= len(cell) <= 12, "Pilot population unexpectedly large")
        else:
            batch = int(suffix[-2:])
            require(cell.source_batch_id.eq(batch).all() and
                    annual.source_batch_id.eq(batch).all(),
                    f"{suffix}: incorrect source batch")
        max_residual = max(max_residual, validate_pair(cell, annual, suffix))
        cells.append(cell)
        annuals.append(annual)
        print(f"VALIDATED | {suffix} | cells={len(cell):,} | years=41")
    cell = pd.concat(cells, ignore_index=True)
    annual = pd.concat(annuals, ignore_index=True)
    a, b = aligned(cell, annual, "combined")
    require(a.index.is_unique and b.index.is_unique,
            "Duplicated cell across batches")
    require(len(a) == N_CELLS if args.mode == "full" else len(a) <= 12,
            "Incorrect population")
    check = cell[list(META[:3])].merge(ref,on="cell_id",how="left",
        validate="one_to_one",suffixes=("_export", "_panel"),indicator=True)
    require(check._merge.eq("both").all() and
            check.GRID_ID_export.eq(check.GRID_ID_panel).all() and
            check.source_batch_id_export.eq(check.source_batch_id_panel).all(),
            "Export metadata differ from accepted panel")
    if args.mode == "full":
        require(set(cell.cell_id) == set(ref.cell_id),
                "Incomplete canonical cell population")
        for kind, data in (("cell", a), ("annual", b)):
            path = args.raw_dir / f"canonical_pasture_age_source_audit_{kind}_pilot_v1.csv"
            probe = read_export(path, CELL_NUMERIC if kind == "cell" else ANNUAL_NUMERIC)
            x = data.reindex(probe.cell_id).reset_index(drop=True)
            fields = CELL_NUMERIC if kind == "cell" else ANNUAL_NUMERIC
            require(len(x) == len(probe) and np.max(np.abs(
                x[list(fields)].to_numpy(float) -
                probe[list(fields)].to_numpy(float))) <= TOL_HA,
                f"Full run differs from {kind} pilot")
    else:
        require(a.raw_code1_any_ha.sum() > 0 and a.reuse100_any_ha.sum() > 0,
                "Pilot did not capture both known anomalies; adjust pilot points")

    annual_rows = []
    for year in YEARS:
        item = {"year":year,"diagnostic_extension":int(year > 2020),
                "cells":len(a)}
        for name in ANNUAL:
            vals = b[f"{name}_{year}_pixel_equiv"]
            item[f"{name}_affected_cells"] = int(vals.gt(1e-9).sum())
            for u in UNITS:
                item[f"{name}_{u}"] = float(b[f"{name}_{year}_{u}"].sum())
        annual_rows.append(item)
    annual_summary = pd.DataFrame(annual_rows)
    joint_rows = []
    for group in JOINT:
        joint_rows.append({"category":group, "scope":args.mode,
            "affected_cells":int(a[f"{group}_pixel_equiv"].gt(1e-9).sum()),
            **{f"{u}":float(a[f"{group}_{u}"].sum()) for u in UNITS}})
    joint = pd.DataFrame(joint_rows)
    require(joint.category.eq("joint_both").sum() == 1,
            "Missing longitudinal overlap category")

    first_last = pd.DataFrame({"cell_id":a.index.to_numpy()})
    for name in ANNUAL:
        yearly = b[[f"{name}_{y}_pixel_equiv" for y in YEARS]].to_numpy(float)
        positive = yearly > 1e-9
        first = np.where(positive.any(axis=1),
                         np.asarray(YEARS)[positive.argmax(axis=1)], -1)
        last = np.where(positive.any(axis=1),
                        np.asarray(YEARS)[len(YEARS)-1-positive[:, ::-1].argmax(axis=1)], -1)
        first_last["first_"+name+"_year"] = pd.Series(first).replace(-1, pd.NA).astype("Int64")
        first_last["last_"+name+"_year"] = pd.Series(last).replace(-1, pd.NA).astype("Int64")
    enriched = cell.merge(spatial,on="cell_id",validate="one_to_one").merge(
        first_last,on="cell_id",validate="one_to_one")
    biome_rows = []
    for (biome,boundary), group in enriched.groupby(
            ["primary_biome","transbiome_flag"],dropna=False):
        row={"primary_biome":biome,"transbiome_flag":boundary,
             "cells":len(group)}
        for name in ("raw_code1_any", "reuse100_any", "joint_both",
                     "reentry_any", "reentry_two_plus", "reentry_duration_ge2",
                     "reentry_duration_ge5", "code100_unresolved_years"):
            row[name+"_ha"] = float(group[name+"_ha"].sum())
            row[name+"_affected_cells"] = int(group[name+"_pixel_equiv"].gt(1e-9).sum())
        biome_rows.append(row)
    biome_summary = pd.DataFrame(biome_rows)

    prefix = "pilot" if args.mode == "pilot" else "canonical"
    annual_path = out / f"{prefix}_pasture_age_source_audit_annual_v1.csv"
    joint_path = out / f"{prefix}_pasture_age_source_audit_joint_v1.csv"
    biome_path = out / f"{prefix}_pasture_age_source_audit_biome_v1.csv"
    val_path = out / f"{prefix}_pasture_age_source_audit_validation_v1.json"
    outputs = [(annual_path, annual_summary), (joint_path,joint),
               (biome_path,biome_summary)]
    if args.mode == "full":
        wide_path = out / "canonical_pasture_age_source_audit_cell_v1.parquet"
        sorted_enriched = enriched.sort_values("cell_id").reset_index(drop=True)
        if wide_path.exists():
            existing = pd.read_parquet(wide_path)
            require(existing.equals(sorted_enriched),
                    f"Existing versioned Parquet differs: {wide_path}")
        else:
            out.mkdir(parents=True, exist_ok=True)
            temp = wide_path.with_name(wide_path.name+".partial")
            try:
                sorted_enriched.to_parquet(temp,index=False)
                temp.replace(wide_path)
            finally:
                temp.unlink(missing_ok=True)
    for path, data in outputs:
        write_fixed(path, data.to_csv(index=False,float_format="%.12g"))
    local_gee = Path(__file__).resolve().parent.parent / "gee/17u_export_pasture_age_source_audit_v1.js"
    result = {"status":"PASS", "mode":args.mode,
        "validator_revision":"source-audit-validator-v2",
        "criterion_11":"PASS" if args.mode == "full" else "PILOT_ONLY",
        "decision_024_fully_implemented":False,
        "population_cells":len(a),"years":list(YEARS),
        "panel_sha256":PANEL_HASH,"spatial_sha256":SPATIAL_HASH,
        "raw_exports":raw_hashes,
        "pilot_cell_sha256":next((x["sha256"] for x in raw_hashes
            if x["file"].endswith("cell_pilot_v1.csv")),None),
        "pilot_annual_sha256":next((x["sha256"] for x in raw_hashes
            if x["file"].endswith("annual_pilot_v1.csv")),None),
        "max_internal_residual":max_residual,
        "gee_script_local_sha256":sha256(local_gee) if local_gee.is_file() else None,
        "gee_code_editor_limitation":"Local JS hash cannot prove which text was executed in the Code Editor",
        "source_age_asset":"projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_age_v1",
        "raw_code1_definition":"Raw age value 1, regardless of coverage state",
        "reuse100_definition":"Raw age 100 when independently reconstructed coverage-derived state is observed post-1985 NEW PAS",
        "joint_universe":"pixels that ever had observed PAS or raw age code 1 in 1985-2025",
        "joint_overlap":"same pixel in at least one code-1 year and at least one reuse-100 year; not same year",
        "cell_biome_scope":"whole-cell area assigned to canonical primary_biome; not exact within-biome pixel area",
        "transbiome_rule":"Phase 7: amazon_fraction_cell > 0 and cerrado_fraction_cell > 0; 582 canonical cells",
        "pixel_interpretation":"weighted pixel equivalents under polygon-boundary reduction, not unweighted integer pixels",
        "source100_unresolved_ha_years":float(a.code100_unresolved_years_ha.sum()),
        "reentry_events_area_weighted_ha_events":float(a.reentry_events_ha.sum()),
        "annual_summary_sha256":sha256(annual_path),
        "joint_summary_sha256":sha256(joint_path),
        "biome_summary_sha256":sha256(biome_path),
        "cell_parquet_sha256":sha256(wide_path) if args.mode == "full" else None,
        "first_raw_code1_year":next((int(x.year) for x in annual_summary.itertuples()
            if x.raw_code1_ha > 0),None),
        "last_raw_code1_year":next((int(x.year) for x in annual_summary.iloc[::-1].itertuples()
            if x.raw_code1_ha > 0),None),
        "first_reuse100_year":next((int(x.year) for x in annual_summary.itertuples()
            if x.reuse100_ha > 0),None),
        "last_reuse100_year":next((int(x.year) for x in annual_summary.iloc[::-1].itertuples()
            if x.reuse100_ha > 0),None)}
    write_fixed(val_path,json.dumps(result,indent=2,ensure_ascii=False,
                                    allow_nan=False)+"\n")
    print(f"PASTURE-AGE SOURCE AUDIT {args.mode.upper()} — VALIDATION PASS")
    print("Cells:",len(a),"Years:",len(YEARS))
    print("Joint both (ha):",float(joint.loc[joint.category.eq("joint_both"),"ha"].iloc[0]))
    print("Validation:",val_path)
    print("Annual:",annual_path)
    print("Joint:",joint_path)
    print("Biome:",biome_path)


if __name__ == "__main__":
    main()

"""Revalidate RQ1's fixed-1985 pasture cohort after Decision 024.

This reads the accepted original GEE export; it does not reconstruct current
pasture-spell origin or rewrite the accepted Phase 9 RQ1 products.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT = Path("/content/drive/MyDrive/Trabalho/Contabilidade")
COHORT = Path(
    "/content/drive/MyDrive/pasture_crop_dynamic_canonical/"
    "canonical_fixed_1985_pasture_cohort_states_full_v1.csv"
)
YEARS = (1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025)
STATES = ("nat", "pas", "tmp", "oag", "out", "water", "nodata", "unexpected", "masked")
N_CELLS = 24_889
TOL = 1e-3  # hectares per cell or summary row; much smaller than one native pixel

HASH = {
    "cohort": "2c6dd05d69f5851477dee856c23530d2d0f1979dcc40c6bb5d83964c4d9f755f",
    "baseline": "3007f29b4b0ae872b2f730ba72fd170f13231fed3c9b760031ddb92bd65c75d7",
    "panel_v2": "ef3589be99e3a2cdc1c2245a15cedd090c8255775b34f14d4f2f27d3f9f8faa7",
    "spatial": "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc",
    "phase9_validation": "16443cc274772e43cc575d3687888d56a09fc420dd18d68fc4266525bc244951",
    "phase9_summary": "f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85",
}


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def authenticate(label, path, expected):
    require(path.is_file(), f"Missing {label}: {path}")
    observed = sha256(path)
    require(observed == expected,
            f"{label} hash differs: observed {observed}; expected {expected}")
    print(f"AUTHENTICATED | {label} | {observed[:12]}")
    return observed


def write_once(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = payload.encode("utf-8")
    if path.exists():
        require(path.read_bytes() == data,
                f"Existing versioned output differs: {path}")
        return
    temp = path.with_name(path.name + ".partial")
    try:
        temp.write_bytes(data)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def numeric(frame, names, label):
    for name in names:
        require(name in frame, f"{label}: missing column {name}")
        frame[name] = pd.to_numeric(frame[name], errors="coerce")
        require(np.isfinite(frame[name].to_numpy(float)).all(),
                f"{label}: missing/nonfinite {name}")


def unique_ids(frame, label):
    require("cell_id" in frame and len(frame) == N_CELLS,
            f"{label}: expected {N_CELLS} cells")
    frame["cell_id"] = frame.cell_id.astype("string").str.strip()
    require(frame.cell_id.notna().all() and frame.cell_id.ne("").all()
            and frame.cell_id.is_unique, f"{label}: invalid cell_id")
    return frame.set_index("cell_id", drop=False).sort_index()


def max_abs(left, right, label, tolerance=TOL):
    a, b = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    require(a.shape == b.shape and np.isfinite(a).all() and np.isfinite(b).all(),
            f"{label}: invalid comparison population")
    value = float(np.max(np.abs(a - b))) if a.size else 0.0
    require(value <= tolerance, f"{label}: max difference {value:.9g} > {tolerance}")
    return value


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-dir", type=Path, default=PROJECT)
    p.add_argument("--cohort", type=Path, default=COHORT)
    p.add_argument("--baseline", type=Path)
    p.add_argument("--panel-v2", type=Path)
    p.add_argument("--spatial", type=Path)
    p.add_argument("--phase9-validation", type=Path)
    p.add_argument("--phase9-summary", type=Path)
    p.add_argument("--source-audit-validation", type=Path)
    p.add_argument("--source-audit-annual", type=Path)
    p.add_argument("--output-dir", type=Path)
    return p.parse_args()


def main():
    args = parse_args()
    try:
        from google.colab import drive
        drive.mount("/content/drive")
    except ImportError:
        pass
    project = args.project_dir
    paths = {
        "cohort": args.cohort,
        "baseline": args.baseline or project / "csv/canonical_stock_flow_1985_1990_full_v1.csv",
        "panel_v2": args.panel_v2 or project / "panel/canonical_stock_flow_panel_1985_2025_v2.parquet",
        "spatial": args.spatial or project / "spatial/phase1/canonical_spatial_support_v1.parquet",
        "phase9_validation": args.phase9_validation or project / "spatial/phase9/gap_resolution_v1/canonical_phase9_gap_resolution_validation_v1.json",
        "phase9_summary": args.phase9_summary or project / "spatial/phase9/gap_resolution_v1/canonical_fixed_1985_pasture_cohort_summary_v1.csv",
        "source_audit_validation": args.source_audit_validation or project / "spatial/phase9/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_validation_v1.json",
        "source_audit_annual": args.source_audit_annual or project / "spatial/phase9/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_annual_v1.csv",
    }
    out = args.output_dir or project / "spatial/phase9/fixed_1985_cohort_revalidation_v1"
    print("RQ1 FIXED 1985 PASTURE COHORT — INDEPENDENT REVALIDATION V1")
    input_hashes = {name: authenticate(name, paths[name], HASH[name]) for name in HASH}

    accepted = json.loads(paths["phase9_validation"].read_text(encoding="utf-8"))
    require(accepted.get("validation_status") == "PASS" and accepted.get("mode") == "full",
            "Accepted Phase 9 validation is not a full PASS")
    require(accepted["inputs"]["fixed_cohort_export"]["raw_sha256"] == HASH["cohort"]
            and accepted["inputs"]["fixed_cohort_export"]["rows"] == N_CELLS,
            "Phase 9 validation references a different cohort export")
    require(accepted["outputs"][paths["phase9_summary"].name]["sha256"] == HASH["phase9_summary"],
            "Phase 9 validation references a different cohort summary")

    audit = json.loads(paths["source_audit_validation"].read_text(encoding="utf-8"))
    require(audit.get("status") == "PASS" and audit.get("criterion_11") == "PASS"
            and audit.get("population_cells") == N_CELLS,
            "Source-age audit must be a full-domain PASS")
    audit_hash = sha256(paths["source_audit_validation"])
    annual_hash = authenticate("source_audit_annual", paths["source_audit_annual"],
                               audit["annual_summary_sha256"])
    audit_annual = pd.read_csv(paths["source_audit_annual"])
    first = audit_annual.loc[audit_annual.year.eq(1985)]
    require(len(audit_annual) == 41 and len(first) == 1
            and first["raw_code1_ha"].iloc[0] == 0
            and first["reuse100_ha"].iloc[0] == 0,
            "Source audit's 1985 anomaly baseline differs")

    cohort = pd.read_csv(paths["cohort"], dtype={"cell_id": "string", "GRID_ID": "string"},
                         float_precision="round_trip", low_memory=False)
    expected_cols = {"cell_id", "GRID_ID", "source_batch_id", "cohort_extraction_version",
                     "cohort_definition", "run_mode", "cohort_total_ha"}
    for year in YEARS:
        expected_cols |= {f"cohort_{year}_{state}_ha" for state in STATES}
        expected_cols |= {f"cohort_{year}_state_total_ha",
                          f"cohort_{year}_closure_residual_ha"}
    require(set(cohort) == expected_cols and len(expected_cols) == 106,
            "Cohort export schema differs")
    cohort = unique_ids(cohort, "cohort export")
    require(cohort.cohort_extraction_version.eq(
        "phase9-fixed-1985-pasture-cohort-export-v1").all()
        and cohort.cohort_definition.eq(
            "coverage_1985_is_pas_and_pasture_age_1985_equals_100").all()
        and cohort.run_mode.eq("full").all(), "Cohort provenance metadata differs")
    numeric(cohort, ["source_batch_id", "cohort_total_ha"]
            + [f"cohort_{y}_{s}_ha" for y in YEARS for s in STATES]
            + [f"cohort_{y}_{suffix}_ha" for y in YEARS
               for suffix in ("state_total", "closure_residual")], "cohort export")
    require(cohort.source_batch_id.between(0, 7).all()
            and (cohort.source_batch_id == cohort.source_batch_id.astype(int)).all(),
            "Cohort batch IDs differ")
    require((cohort.cohort_total_ha >= -1e-9).all(), "Negative cohort area")
    cohort_area = float(cohort.cohort_total_ha.sum())
    require(abs(cohort_area - 49_035_870.56718212) <= TOL,
            "Original fixed-cohort area changed")
    cells_with_cohort = int(cohort.cohort_total_ha.gt(1e-9).sum())
    require(cells_with_cohort == 16_421, "Original cohort population changed")

    baseline = pd.read_csv(paths["baseline"], dtype={"cell_id": "string", "GRID_ID": "string"},
                           usecols=["cell_id", "GRID_ID", "source_batch_id",
                                    "t0", "t1", "stock0_pas"], float_precision="round_trip")
    baseline = unique_ids(baseline, "accepted 1985–1990 flow")
    require(cohort.index.equals(baseline.index), "Cohort and baseline cell sets differ")
    numeric(baseline, ["source_batch_id", "t0", "t1", "stock0_pas"], "baseline")
    require(baseline.t0.eq(1985).all() and baseline.t1.eq(1990).all(),
            "Unexpected baseline interval")
    require(cohort.GRID_ID.equals(baseline.GRID_ID)
            and cohort.source_batch_id.equals(baseline.source_batch_id),
            "Cohort/baseline grid metadata differ")
    delta_baseline = max_abs(cohort.cohort_total_ha, baseline.stock0_pas,
                             "Cohort area versus coverage-only PAS stock (1985)")

    panel = pd.read_parquet(paths["panel_v2"], columns=["cell_id", "t0", "t1", "stock0_pas"])
    require(len(panel) == 199_112 and panel.cell_id.astype(str).nunique() == N_CELLS,
            "Corrected panel v2 population differs")
    panel["cell_id"] = panel.cell_id.astype("string").str.strip()
    require(not panel.duplicated(["cell_id", "t0", "t1"]).any(),
            "Corrected panel v2 duplicates keys")
    selection = panel.loc[panel.t0.eq(1985) & panel.t1.eq(1990)].copy()
    selection = unique_ids(selection, "corrected panel baseline")
    require(cohort.index.equals(selection.index),
            "Cohort/corrected panel cell sets differ")
    numeric(selection, ["stock0_pas"], "corrected panel")
    delta_panel = max_abs(cohort.cohort_total_ha, selection.stock0_pas,
                          "Cohort area versus corrected panel v2 PAS stock (1985)")
    delta_panel_baseline = max_abs(baseline.stock0_pas, selection.stock0_pas,
                                   "Original versus corrected 1985 PAS stock")

    spatial = pd.read_parquet(paths["spatial"], columns=["cell_id", "primary_biome",
                             "amazon_fraction_cell", "cerrado_fraction_cell"])
    spatial = unique_ids(spatial, "canonical spatial support")
    require(cohort.index.equals(spatial.index), "Spatial/cohort cell sets differ")
    require(spatial.primary_biome.value_counts().to_dict()
            == {"Amazon": 14_213, "Cerrado": 10_676}, "Biome populations differ")
    spatial["transbiome_flag"] = (spatial.amazon_fraction_cell.gt(0)
                                  & spatial.cerrado_fraction_cell.gt(0))
    require(int(spatial.transbiome_flag.sum()) == 582,
            "Amazon–Cerrado overlap population differs")

    accepted_summary = pd.read_csv(paths["phase9_summary"], float_precision="round_trip")
    require(len(accepted_summary) == 45 and not accepted_summary.duplicated(
        ["boundary_scope", "primary_biome", "year"]).any(),
        "Accepted RQ1 summary population differs")
    accepted_summary = accepted_summary.set_index(
        ["boundary_scope", "primary_biome", "year"]).sort_index()
    groups = [("combined_domain", "All", np.ones(N_CELLS, dtype=bool))]
    for biome in ("Amazon", "Cerrado"):
        primary = spatial.primary_biome.eq(biome).to_numpy()
        groups.extend([
            ("primary_assignment", biome, primary),
            ("nontransbiome_sensitivity", biome,
             primary & ~spatial.transbiome_flag.to_numpy()),
        ])
    comparison = []
    row_closure = 0.0
    row_constancy = 0.0
    for year in YEARS:
        state_cols = [f"cohort_{year}_{s}_ha" for s in STATES]
        state_total = cohort[state_cols].sum(axis=1).to_numpy(float)
        total = cohort.cohort_total_ha.to_numpy(float)
        row_closure = max(row_closure, max_abs(state_total, total,
            f"Per-cell fixed-area state closure {year}"))
        row_constancy = max(row_constancy, max_abs(
            cohort[f"cohort_{year}_state_total_ha"], total,
            f"Per-cell state total {year}"))
        max_abs(cohort[f"cohort_{year}_closure_residual_ha"], total-state_total,
                f"Per-cell residual field {year}")
        if year == 1985:
            non_pas = cohort[[f"cohort_1985_{s}_ha" for s in STATES if s != "pas"]]
            require(non_pas.to_numpy(float).min() >= -TOL,
                    "Baseline contains negative non-PAS components")
            max_abs(cohort["cohort_1985_pas_ha"], total,
                    "All fixed-cohort area is PAS at baseline")
            require(float(non_pas.to_numpy(float).sum()) <= TOL,
                    "Non-PAS area in 1985 fixed cohort")
        for scope, biome, mask in groups:
            key = (scope, biome, year)
            require(key in accepted_summary.index, f"Missing accepted summary row {key}")
            previous = accepted_summary.loc[key]
            sub = cohort.loc[mask]
            new_total = float(sub.cohort_total_ha.sum())
            new_areas = {s:float(sub[f"cohort_{year}_{s}_ha"].sum()) for s in STATES}
            max_delta = max(abs(new_areas[s]-float(previous[f"{s}_ha"])) for s in STATES)
            max_share_delta = max(abs(new_areas[s]/new_total
                                  - float(previous[f"{s}_share"])) for s in STATES)
            max_abs([new_total], [previous.cohort_total_ha],
                    f"Accepted fixed cohort total {key}")
            require(max_delta <= TOL and max_share_delta <= 1e-9,
                    f"Accepted endpoint composition differs at {key}")
            require(int(previous.cells) == int(mask.sum())
                    and int(previous.cells_with_cohort)
                    == int(sub.cohort_total_ha.gt(1e-9).sum())
                    and int(previous.diagnostic_endpoint) == int(year == 2025),
                    f"Accepted endpoint population or diagnostic flag differs: {key}")
            require(abs(float(previous.partition_residual_ha)) <= TOL,
                    f"Accepted summary partition fails: {key}")
            comparison.append({"boundary_scope":scope, "primary_biome":biome,
                "year":year,"diagnostic_endpoint":int(year == 2025),
                "cells":int(mask.sum()),"cohort_total_ha":new_total,
                "cohort_total_delta_ha":new_total-float(previous.cohort_total_ha),
                "max_abs_state_delta_ha":max_delta,
                "max_abs_state_share_delta":max_share_delta})
    require(len(comparison) == 45, "Wrong comparison population")

    comp = pd.DataFrame(comparison)
    comp_path = out / "canonical_fixed_1985_cohort_revalidation_comparison_v1.csv"
    json_path = out / "canonical_fixed_1985_cohort_revalidation_validation_v1.json"
    write_once(comp_path, comp.to_csv(index=False,float_format="%.15g",lineterminator="\n"))
    result = {
        "status":"PASS", "scope":"Decision 024 RQ1 fixed-baseline cohort revalidation",
        "script_version":"17w-fixed-1985-cohort-revalidation-v1",
        "decision_024_fully_implemented":False,
        "rq1_fixed_cohort_baseline_revalidated":True,
        "no_new_gee_processing":True,
        "pixel_level_independent_resampling":False,
        "cohort_definition":"coverage 1985 PAS AND public pasture-age 1985 == 100",
        "cells":N_CELLS,"cells_with_cohort":cells_with_cohort,"cohort_area_ha":cohort_area,
        "reference_years":list(YEARS),"comparison_rows":len(comp),
        "1985_raw_code1_area_ha":float(first.raw_code1_ha.iloc[0]),
        "max_cell_cohort_vs_baseline_ha":delta_baseline,
        "max_cell_cohort_vs_panel_v2_ha":delta_panel,
        "max_cell_original_vs_panel_v2_ha":delta_panel_baseline,
        "max_cell_state_closure_ha":row_closure,
        "max_cell_state_total_difference_ha":row_constancy,
        "max_summary_state_delta_ha":float(comp.max_abs_state_delta_ha.max()),
        "max_summary_share_delta":float(comp.max_abs_state_share_delta.max()),
        "input_sha256":{**input_hashes,
            "source_audit_validation":audit_hash,"source_audit_annual":annual_hash},
        "comparison_sha256":sha256(comp_path),
        "limits":["The accepted 15b export is authenticated, not reobserved at native pixels.",
                  "Matching per-cell area to coverage PAS establishes area equivalence under the 15b subset mask; it does not create a new fixed cohort.",
                  "Endpoint composition remains a nine-date composition of fixed pixels, not a survival curve or within-interval path analysis."],
        "evidence_status":"P9A035-P9A037 remain suspended pending Decision 024 criterion 12",
    }
    write_once(json_path, json.dumps(result,indent=2,allow_nan=False)+"\n")
    print("RQ1 FIXED 1985 COHORT REVALIDATION — PASS")
    print(f"Cells: {N_CELLS:,} | cohort cells: {cells_with_cohort:,} | area: {cohort_area:,.6f} ha")
    print("Max per-cell cohort/baseline difference:",delta_baseline)
    print("Max per-cell cohort/panel-v2 difference:",delta_panel)
    print("Comparison:",comp_path)
    print("Validation:",json_path)


if __name__ == "__main__":
    main()

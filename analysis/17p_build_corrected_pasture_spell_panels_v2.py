"""Build versioned stock-flow, derived, and integrated panels after Decision 024.

The accepted v1 non-origin columns are preserved exactly. Source pasture-age
components and their dependent residual/shares are removed. Corrected origin
and origin-by-destination areas come from authenticated full_v3 CSVs. The
accepted NAT->TMP trajectory columns are preserved in the integrated panel.
No v1 file is modified. Output files are installed only after validation.
"""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd


INTERVALS = [(y, y + 5) for y in range(1985, 2025, 5)]
KEY = ["cell_id", "t0", "t1"]
ORIGINS = ("initial", "new", "unresolved")
DESTS = ("pas", "tmp", "nat", "oag", "out", "water", "nodata", "unexpected", "masked")
OLD_AREAS = ["pas_tmp_censored", "pas_tmp_new", "pas_tmp_unresolved_age",
             "pas_tmp_unattributed_age"]
OLD_SHARES = ["pas_tmp_censored_share", "pas_tmp_new_share",
              "pas_tmp_unresolved_age_share", "pas_tmp_unattributed_age_share"]
OLD_RESIDUAL = "residual_pas_tmp_partition"
DROP_PANEL = OLD_AREAS + [OLD_RESIDUAL]
DROP_DERIVED = DROP_PANEL + OLD_SHARES
NEW_ORIGIN_AREAS = [f"origin_{o}" for o in ORIGINS]
NEW_PARTITIONS = [f"pas_{o}_to_{d}" for d in DESTS for o in ORIGINS]
NEW_AREAS = NEW_ORIGIN_AREAS + NEW_PARTITIONS
NEW_TOTALS = ["pas_observed_outflow_ha", "pas_observation_loss_ha"]
NEW_SHARES = [f"pas_tmp_origin_{o}_share" for o in ORIGINS]
TOL = 0.01  # ha per cell, consistent with validated 17m outputs
EXPECTED = 24_889 * 8
HASHES = {
    "panel": "2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64",
    "derived": "671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302",
    "integrated": "7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28",
    "trajectory": "c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9",
}
VERSION_PANEL = "canonical-stock-flow-panel-pasture-spell-v2"
VERSION_DERIVED = "canonical-derived-stock-flow-pasture-spell-v2"
VERSION_INTEGRATED = "canonical-integrated-stock-flow-trajectory-v2"


def require(ok, message):
    if not bool(ok):
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def key_frame(frame):
    return pd.DataFrame({"cell_id": frame.cell_id.astype(str).str.strip(),
                         "t0": frame.t0.astype(int), "t1": frame.t1.astype(int)})


def require_keys(frame, label):
    keys = key_frame(frame)
    require(len(keys) == EXPECTED and not keys.duplicated().any(),
            f"{label}: incorrect or duplicate key population")
    require(keys.cell_id.nunique() == 24_889 and keys.groupby("cell_id").size().eq(8).all(),
            f"{label}: incomplete eight-interval cell population")
    return keys


def align_to(reference, other, label):
    a, b = key_frame(reference), key_frame(other)
    require(not b.duplicated().any() and len(a) == len(b), f"{label}: duplicate/row count")
    idx = pd.MultiIndex.from_frame(a)
    out = other.copy()
    out.index = pd.MultiIndex.from_frame(b)
    require(out.index.is_unique and out.index.difference(idx).empty and idx.difference(out.index).empty,
            f"{label}: key membership differs")
    return out.reindex(idx).reset_index(drop=True)


def max_delta(a, b, label, tolerance=TOL):
    x = pd.to_numeric(a).to_numpy(dtype="float64")
    y = pd.to_numeric(b).to_numpy(dtype="float64")
    require(np.isfinite(x).all() and np.isfinite(y).all(), f"{label}: missing/nonfinite")
    d = float(np.max(np.abs(x - y))) if len(x) else 0.0
    require(d <= tolerance, f"{label}: maximum discrepancy {d:.9g} ha")
    return d


def same_columns(old, new, excluded, label):
    kept = [x for x in old.columns if x not in excluded]
    require(new[kept].equals(old[kept]), f"{label}: non-origin value or dtype changed")
    return len(kept)


def safe_share(num, den):
    x = pd.Series(np.nan, index=den.index, dtype="float64")
    active = den > 1e-9
    x.loc[active] = num.loc[active] / den.loc[active]
    return x


def self_test():
    a = pd.DataFrame({"cell_id": ["2", "1"], "t0": [1985, 1985],
                      "t1": [1990, 1990], "value": [2.0, 1.0]})
    b = a.iloc[::-1].copy()
    require(align_to(a, b, "synthetic").value.tolist() == [2., 1.],
            "Reordered-key test failed")
    b.loc[b.cell_id == "1", "value"] = 1.1
    try:
        max_delta(a.value, align_to(a, b, "synthetic").value,
                  "synthetic change", .01)
    except ValueError:
        pass
    else:
        raise AssertionError("A changed area passed the negative test")
    print("CORRECTED PANEL ENGINE SELF-TEST PASS")


def write_parquet_checked(frame, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".partial")
    try:
        frame.to_parquet(temp, index=False, compression="snappy", engine="pyarrow")
        reread = pd.read_parquet(temp)
        require(reread.equals(frame.reset_index(drop=True)),
                f"Parquet round-trip changed {path.name}")
        if path.exists():
            require(pd.read_parquet(path).equals(frame.reset_index(drop=True)),
                    f"Existing versioned output differs; use a new version: {path}")
            temp.unlink()
        else:
            temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()
    return sha(path)


def run(args):
    project = args.project_dir
    inputs = {
        "panel": project / "panel/canonical_stock_flow_panel_1985_2025_v1.parquet",
        "derived": project / "analysis/canonical_stock_flow_derived_metrics_1985_2025_v1.parquet",
        "integrated": project / "analysis/canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet",
        "trajectory": project / "panel/canonical_nat_tmp_trajectory_panel_1985_2025_v1.parquet",
    }
    for name, path in inputs.items():
        require(path.is_file() and sha(path) == HASHES[name],
                f"Accepted {name} panel missing or hash differs: {path}")
        print(f"AUTHENTICATED | {name} | {HASHES[name][:12]}")
    gate_path = project / "spatial/phase9/pasture_spell_invariance_v1/canonical_pasture_spell_nonorigin_invariance_validation_v1.json"
    require(gate_path.is_file(), "The accepted 17o gate record is missing")
    gate = json.loads(gate_path.read_text(encoding="utf-8"))
    require(gate.get("status") == "PASS" and len(gate.get("intervals", [])) == 8 and
            gate.get("accepted_panel_hashes", {}).get("panel") == HASHES["panel"],
            "The 17o gate record is not a matching full-series PASS")

    v1 = pd.read_parquet(inputs["panel"]).reset_index(drop=True)
    derived_v1 = align_to(v1, pd.read_parquet(inputs["derived"]), "derived v1")
    integrated_v1 = align_to(v1, pd.read_parquet(inputs["integrated"]), "integrated v1")
    trajectory_v1 = pd.read_parquet(inputs["trajectory"])
    require(len(v1) == len(derived_v1) == len(integrated_v1) == len(trajectory_v1) == EXPECTED,
            "Accepted panel sizes differ")
    require_keys(v1, "stock-flow v1")
    require(set(DROP_PANEL).issubset(v1.columns) and
            set(DROP_DERIVED).issubset(derived_v1.columns) and
            set(DROP_DERIVED).issubset(integrated_v1.columns),
            "Legacy origin schema differs")
    require(derived_v1[v1.columns.tolist()].equals(v1),
            "Derived v1 does not preserve accepted stock-flow fields")
    require(integrated_v1[derived_v1.columns.tolist()].equals(derived_v1),
            "Integrated v1 does not preserve accepted derived fields")
    require(align_to(v1, trajectory_v1, "trajectory v1").shape[0] == EXPECTED,
            "Accepted NAT->TMP trajectory population differs")

    closure_dir = args.closure_dir or project / "spatial/phase9/pasture_spell_closure_full_v1"
    parts, input_records = [], []
    for t0, t1 in INTERVALS:
        tag = f"{t0}_{t1}"
        data_path = closure_dir / f"canonical_pas_origin_destination_{tag}_full_v3.csv"
        record_path = closure_dir / f"canonical_pas_origin_destination_{tag}_validation_v3.json"
        require(data_path.is_file() and record_path.is_file(), f"{tag}: corrected input missing")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        require(record.get("status") == "PASS" and record.get("interval") == tag and
                record.get("cells") == 24_889 and sha(data_path) == record.get("output_sha256"),
                f"{tag}: corrected input is not authenticated")
        part = pd.read_csv(data_path, dtype={"cell_id": "string", "GRID_ID": "string"},
                           low_memory=False)
        require(len(part) == 24_889 and not key_frame(part).duplicated().any() and
                set(part.diagnostic_interval) == {int(t0 == 2020)},
                f"{tag}: corrected population/flag differs")
        parts.append(part)
        input_records.append({"interval": tag, "csv_sha256": record["output_sha256"],
                              "validation_sha256": sha(record_path)})
    corrected = align_to(v1, pd.concat(parts, ignore_index=True), "full corrected closure")
    require((v1.GRID_ID.astype(str) == corrected.GRID_ID.astype(str)).all() and
            (v1.source_batch_id.to_numpy() == corrected.source_batch_id.to_numpy()).all(),
            "Cell/batch metadata differs")

    max_pas_change = 0.0
    for name in ["stock0_pas"] + [f"flow_pas_{d}" for d in DESTS]:
        max_pas_change = max(max_pas_change, max_delta(v1[name], corrected[name], name))
    require(set(NEW_AREAS).issubset(corrected.columns), "Corrected origin schema incomplete")
    require(np.isfinite(corrected[NEW_AREAS].to_numpy(dtype=float)).all() and
            (corrected[NEW_AREAS].to_numpy(dtype=float) >= -1e-7).all(),
            "Invalid corrected origin areas")
    max_origin_residual = max_delta(corrected.stock0_pas,
                                    sum(corrected[f"origin_{o}"] for o in ORIGINS),
                                    "Origin to initial PAS stock")
    for d in DESTS:
        max_origin_residual = max(max_origin_residual,
            max_delta(corrected[f"flow_pas_{d}"],
                      sum(corrected[f"pas_{o}_to_{d}"] for o in ORIGINS),
                      f"PAS->{d} origin closure"))
    for o in ORIGINS:
        max_origin_residual = max(max_origin_residual,
            max_delta(corrected[f"origin_{o}"],
                      sum(corrected[f"pas_{o}_to_{d}"] for d in DESTS),
                      f"Origin {o} destination closure"))

    # Retain only valid v1 source fields. Source-based age columns and their
    # validation residual are excluded from the corrected analytical product.
    panel_v2 = v1.drop(columns=DROP_PANEL).copy()
    for name in NEW_AREAS:
        require(name not in panel_v2.columns, f"New field collides: {name}")
        panel_v2[name] = corrected[name].to_numpy()
    panel_v2["pas_observed_outflow_ha"] = sum(panel_v2[f"flow_pas_{d}"]
                                                for d in ("tmp", "nat", "oag", "out", "water"))
    panel_v2["pas_observation_loss_ha"] = sum(panel_v2[f"flow_pas_{d}"]
                                                for d in ("nodata", "unexpected", "masked"))
    for name in NEW_TOTALS:
        max_delta(panel_v2[name], corrected[name], name)
    max_delta(panel_v2.stock0_pas,
              panel_v2.flow_pas_pas + panel_v2.pas_observed_outflow_ha +
              panel_v2.pas_observation_loss_ha, "PAS stock closure")
    panel_v2["pasture_spell_accounting_version"] = "pas-origin-destination-full-v3"
    panel_v2["stock_flow_panel_version"] = VERSION_PANEL
    same_columns(v1, panel_v2, DROP_PANEL, "Stock-flow panel v2")

    derived_v2 = derived_v1.drop(columns=DROP_DERIVED).copy()
    added_panel = [c for c in panel_v2 if c not in v1.columns]
    for name in added_panel:
        require(name not in derived_v2.columns, f"Derived field collides: {name}")
        derived_v2[name] = panel_v2[name].to_numpy()
    active = derived_v2.flow_pas_tmp > 1e-9
    for o in ORIGINS:
        derived_v2[f"pas_tmp_origin_{o}_share"] = safe_share(
            derived_v2[f"pas_{o}_to_tmp"], derived_v2.flow_pas_tmp)
    share_sum = derived_v2[NEW_SHARES].sum(axis=1)
    require((share_sum.loc[active] - 1).abs().max() < 1e-6 and
            derived_v2.loc[~active, NEW_SHARES].isna().all().all(),
            "Corrected RQ2 share closure or undefined denominator failed")
    derived_v2["derived_output_version"] = VERSION_DERIVED
    same_columns(derived_v1, derived_v2, DROP_DERIVED, "Derived panel v2")
    require(derived_v2[panel_v2.columns.tolist()].equals(panel_v2),
            "Derived panel changed corrected stock-flow fields")

    integrated_v2 = integrated_v1.drop(columns=DROP_DERIVED).copy()
    for name in added_panel + NEW_SHARES + ["derived_output_version"]:
        require(name not in integrated_v2.columns, f"Integrated field collides: {name}")
        integrated_v2[name] = derived_v2[name].to_numpy()
    require(set(integrated_v2.integrated_output_version) ==
            {"canonical-integrated-stock-flow-trajectory-v1"},
            "Unexpected v1 integrated version")
    integrated_v2["integrated_output_version"] = VERSION_INTEGRATED
    same_columns(integrated_v1, integrated_v2,
                 DROP_DERIVED + ["integrated_output_version"], "Integrated panel v2")
    require(integrated_v2[derived_v2.columns.tolist()].equals(derived_v2),
            "Integrated panel changed corrected derived fields")
    for name, frame in (("panel v2", panel_v2), ("derived v2", derived_v2),
                        ("integrated v2", integrated_v2)):
        require_keys(frame, name)
        require(not (set(DROP_DERIVED) & set(frame.columns)),
                f"{name}: legacy source-age column leaked")
    print("VERSIONED PANELS VERIFIED IN MEMORY | rows=199,112 | intervals=8")

    output_files = {
        "panel": project / "panel/canonical_stock_flow_panel_1985_2025_v2.parquet",
        "derived": project / "analysis/canonical_stock_flow_derived_metrics_1985_2025_v2.parquet",
        "integrated": project / "analysis/canonical_integrated_stock_flow_trajectory_1985_2025_v2.parquet",
    }
    output_hashes = {}
    for name, frame in (("panel", panel_v2), ("derived", derived_v2),
                        ("integrated", integrated_v2)):
        output_hashes[name] = write_parquet_checked(frame, output_files[name])
        print(f"WRITTEN | {name} | {frame.shape} | {output_hashes[name][:12]}")

    rows = []
    for t0, t1 in INTERVALS:
        frame = derived_v2.loc[derived_v2.t0.eq(t0) & derived_v2.t1.eq(t1)]
        totals = [float(frame[f"pas_{o}_to_tmp"].sum()) for o in ORIGINS]
        den = float(frame.flow_pas_tmp.sum())
        require(abs(sum(totals) - den) <= TOL * 24_889,
                "Interval RQ2 total differs")
        rows.append({"interval": f"{t0}_{t1}", "diagnostic_interval": int(t0 == 2020),
                     "flow_pas_tmp_ha": den, "initial_ha": totals[0],
                     "new_ha": totals[1], "unresolved_ha": totals[2],
                     "initial_pct": 100 * totals[0] / den if den else None,
                     "new_pct": 100 * totals[1] / den if den else None,
                     "unresolved_pct": 100 * totals[2] / den if den else None})
    pooled = []
    accepted_pooled = [
        ("primary_1985_2020", rows[:7], 20_119_468.09856614,
         46.9098986949934, 53.08979031861919),
        ("full_observed_1985_2025", rows, 22_205_794.84859696,
         44.392464342562924, 55.60721315233414),
    ]
    for name, selected, expected_area, expected_initial, expected_new in accepted_pooled:
        den = sum(r["flow_pas_tmp_ha"] for r in selected)
        ini = sum(r["initial_ha"] for r in selected)
        new = sum(r["new_ha"] for r in selected)
        unr = sum(r["unresolved_ha"] for r in selected)
        initial_pct, new_pct = 100 * ini / den, 100 * new / den
        require(abs(den - expected_area) < 0.1 and
                abs(initial_pct - expected_initial) < 0.001 and
                abs(new_pct - expected_new) < 0.001 and
                abs(ini + new + unr - den) < TOL * EXPECTED,
                f"{name}: pooled RQ2 no longer reproduces accepted reassessment")
        pooled.append({"window": name, "intervals": len(selected),
                       "includes_diagnostic_interval": int(len(selected) == 8),
                       "flow_pas_tmp_ha": den, "initial_ha": ini,
                       "new_ha": new, "unresolved_ha": unr,
                       "initial_pct": initial_pct, "new_pct": new_pct,
                       "unresolved_pct": 100 * unr / den})

    outdir = project / "spatial/phase9/pasture_spell_panel_v2"
    outdir.mkdir(parents=True, exist_ok=True)
    summary = outdir / "canonical_pas_tmp_origin_interval_summary_v2.csv"
    pooled_path = outdir / "canonical_pas_tmp_origin_pooled_summary_v2.csv"
    for path, data in ((summary, rows), (pooled_path, pooled)):
        buf = io.StringIO(newline="")
        writer = csv.DictWriter(buf, fieldnames=list(data[0]))
        writer.writeheader()
        writer.writerows(data)
        payload = buf.getvalue()
        if path.exists():
            require(path.read_text(encoding="utf-8") == payload,
                    f"Existing summary differs; use a new version: {path}")
        else:
            path.write_text(payload, encoding="utf-8")

    validation = {
        "status": "PASS", "scope": "versioned_corrected_stock_flow_derived_integrated_panels",
        "rows": EXPECTED, "cells": 24_889, "intervals": 8,
        "source_hashes": HASHES, "gate_17o_sha256": sha(gate_path),
        "corrected_inputs": input_records,
        "removed_source_age_fields": DROP_DERIVED,
        "corrected_area_fields": NEW_AREAS + NEW_TOTALS,
        "corrected_share_fields": NEW_SHARES,
        "nonorigin_fields_preserved_exactly": True,
        "maximum_pas_total_difference_ha_per_cell": max_pas_change,
        "maximum_origin_identity_residual_ha_per_cell": max_origin_residual,
        "independent_reexport_of_other_raster_flows": False,
        "decision_024_criterion_9_versioned_panel_comparison": "PASS",
        "decision_024_fully_implemented": False,
        "outputs": {name: {"path": str(output_files[name]), "sha256": output_hashes[name]}
                    for name in output_files},
        "interval_summary": {"path": str(summary), "sha256": sha(summary)},
        "pooled_summary": {"path": str(pooled_path), "sha256": sha(pooled_path)},
    }
    target = outdir / "canonical_pasture_spell_panel_v2_validation.json"
    payload = json.dumps(validation, indent=2, allow_nan=False) + "\n"
    if target.exists():
        require(target.read_text(encoding="utf-8") == payload,
                "Existing validation record differs; use a new version")
    else:
        target.write_text(payload, encoding="utf-8")
    print("CORRECTED PASTURE-SPELL PANELS V2 — VALIDATION PASS")
    print("Validation:", target)
    print("Interval summary:", summary)
    print("Pooled summary:", pooled_path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-dir", type=Path,
                   default=Path("/content/drive/MyDrive/Trabalho/Contabilidade"))
    p.add_argument("--closure-dir", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    self_test()
    if not args.self_test:
        if str(args.project_dir).startswith("/content/drive"):
            try:
                from google.colab import drive
            except ImportError:
                pass
            else:
                drive.mount("/content/drive")
        run(args)


if __name__ == "__main__":
    main()

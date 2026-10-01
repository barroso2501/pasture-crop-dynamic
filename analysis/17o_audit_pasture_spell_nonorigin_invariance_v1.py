"""Audit the non-origin impact of Decision 024 on accepted stock-flow products.

Read-only with respect to accepted inputs. The corrected closure tables contain
PAS-origin partitions and PAS endpoint totals; they do not re-export all other
land-cover flows. Therefore this gate compares every newly exported PAS total
against the authenticated v1 baseline, authenticates the accepted panel chain,
and checks the quantitative inputs used by Phase 2. It records this precise
scope and does not claim an independent raster re-extraction of all 90 fields.

Colab: %run /content/17o_audit_pasture_spell_nonorigin_invariance_v1.py
Local: python 17o_audit_pasture_spell_nonorigin_invariance_v1.py --project-dir PATH
"""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


INTERVALS = [(year, year + 5) for year in range(1985, 2025, 5)]
KEY = ["cell_id", "t0", "t1"]
DEST = ("pas", "tmp", "nat", "oag", "out", "water", "nodata", "unexpected", "masked")
ORIGIN = ("initial", "new", "unresolved")
AREA_TOL = 0.01  # ha per cell: the accepted 17m closure tolerance
ROWS = 24_889
HASHES = {
    "panel": "2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64",
    "derived": "671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302",
    "integrated": "7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28",
    "spatial": "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c",
}
SPATIAL_INPUTS = [
    "cell_id", "t0", "t1", "GRID_ID", "source_batch_id", "interval",
    "diagnostic_interval", "primary_inference_interval",
    "stock0_pas", "stock0_nat", "flow_pas_tmp", "flow_nat_pas", "flow_nat_tmp",
    "consolidation_ha", "replenishment_ha", "gross_cr_activity_ha",
    "net_cr_balance_ha", "nat_tmp_endpoint_ha", "nat_tmp_pas_any_ha",
    "nat_tmp_pas_2plus_ha", "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_without_intermediate_pasture_ha", "nat_tmp_mid_incomplete_ha",
    "consolidation_rate_initial_pasture", "replenishment_rate_initial_native",
    "cr_balance_index", "has_consolidation", "has_replenishment",
    "has_cr_activity", "cr_activity_class", "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_2plus_share_endpoint", "nat_tmp_pas_consecutive2_share_endpoint",
    "nat_tmp_pas_consecutive2_share_any", "nat_tmp_mid_incomplete_share_endpoint",
]
LEGACY_ORIGIN = {
    "pas_tmp_censored", "pas_tmp_new", "pas_tmp_unresolved_age",
    "pas_tmp_unattributed_age", "pas_tmp_censored_share", "pas_tmp_new_share",
    "pas_tmp_unresolved_age_share", "pas_tmp_unattributed_age_share",
}


def require(ok, message):
    if not bool(ok):
        raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonicalize(frame):
    frame = frame.copy()
    frame["cell_id"] = frame["cell_id"].astype(str).str.strip()
    frame["t0"] = frame["t0"].astype(int)
    frame["t1"] = frame["t1"].astype(int)
    require(not frame.duplicated(KEY).any(), "Duplicate cell/interval key")
    return frame.sort_values(KEY, kind="stable").reset_index(drop=True)


def maximum_difference(left, right, label, tolerance=0.0):
    """Require equal keys; preserve undefined numeric values as matched NaNs."""
    left = canonicalize(left)
    right = canonicalize(right)
    require(left[KEY].equals(right[KEY]), f"{label}: key population differs")
    names = [x for x in left.columns if x not in KEY]
    require(set(names).issubset(right.columns), f"{label}: columns missing")
    maxima = {}
    for col in names:
        a, b = left[col], right[col]
        if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
            av = pd.to_numeric(a).to_numpy(dtype="float64")
            bv = pd.to_numeric(b).to_numpy(dtype="float64")
            require(np.array_equal(np.isnan(av), np.isnan(bv)),
                    f"{label}: undefined status differs in {col}")
            require(np.isfinite(av[~np.isnan(av)]).all() and
                    np.isfinite(bv[~np.isnan(bv)]).all(),
                    f"{label}: nonfinite {col}")
            delta = np.abs(av - bv)
            diff = float(np.nanmax(delta)) if len(delta) and np.isfinite(delta).any() else 0.0
            require(diff <= tolerance, f"{label}: {col} differs by {diff:.9g}")
            maxima[col] = diff
        else:
            require(a.astype("string").fillna("<NULL>").equals(
                    b.astype("string").fillna("<NULL>")),
                    f"{label}: {col} differs")
    return maxima


def self_test():
    a = pd.DataFrame({"cell_id": ["01", "02"], "t0": [1985, 1985],
                      "t1": [1990, 1990], "x": [0.0, np.nan], "label": ["a", "b"]})
    b = a.iloc[::-1].copy()
    require(maximum_difference(a, b, "synthetic") == {"x": 0.0},
            "Self-test: reordered keys")
    b.loc[b.cell_id == "01", "x"] = .02
    try:
        maximum_difference(a, b, "synthetic", .01)
    except ValueError:
        pass
    else:
        raise AssertionError("Self-test: change exceeding tolerance was accepted")
    print("INVARIANCE ENGINE SELF-TEST PASS")


def read_csv(path):
    require(path.is_file(), f"Missing input: {path}")
    return pd.read_csv(path, dtype={"cell_id": "string", "GRID_ID": "string"},
                       low_memory=False)


def run(args):
    project = args.project_dir
    baseline_dir = args.baseline_dir or project / "csv"
    closure_dir = args.closure_dir or project / "spatial/phase9/pasture_spell_closure_full_v1"
    output_dir = args.output_dir or project / "spatial/phase9/pasture_spell_invariance_v1"
    paths = {
        "panel": project / "panel/canonical_stock_flow_panel_1985_2025_v1.parquet",
        "derived": project / "analysis/canonical_stock_flow_derived_metrics_1985_2025_v1.parquet",
        "integrated": project / "analysis/canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet",
        "spatial": project / "spatial/phase2/canonical_spatial_metrics_panel_v1.parquet",
    }
    checked_hashes = {}
    for name, path in paths.items():
        require(path.is_file(), f"Missing accepted {name} panel: {path}")
        digest = sha256(path)
        require(digest == HASHES[name], f"Accepted {name} hash differs: {digest}")
        checked_hashes[name] = digest
        print(f"AUTHENTICATED | {name} | {digest[:12]}")

    # Source-level comparison. Do not compare legacy age-origin partitions;
    # those are the variables that the remediation intentionally changes.
    panel = canonicalize(pd.read_parquet(paths["panel"]))
    require(len(panel) == ROWS * 8 and panel.cell_id.nunique() == ROWS,
            "Canonical panel population differs")
    require(len(panel.columns) == 90, "Unexpected original panel schema")
    require(LEGACY_ORIGIN.intersection(panel.columns) == {
        "pas_tmp_censored", "pas_tmp_new", "pas_tmp_unresolved_age",
        "pas_tmp_unattributed_age"}, "Original age-origin schema differs")

    interval_records = []
    for t0, t1 in INTERVALS:
        tag = f"{t0}_{t1}"
        base_path = baseline_dir / f"canonical_stock_flow_{tag}_full_v1.csv"
        corrected_path = closure_dir / f"canonical_pas_origin_destination_{tag}_full_v3.csv"
        record_path = closure_dir / f"canonical_pas_origin_destination_{tag}_validation_v3.json"
        require(record_path.is_file(), f"Missing closure validation: {record_path}")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        require(record.get("status") == "PASS" and record.get("interval") == tag
                and record.get("cells") == ROWS, f"{tag}: invalid validation scope")
        require(record.get("decision_024_fully_implemented") is False,
                f"{tag}: unexpected decision status")
        require(base_path.is_file() and corrected_path.is_file(),
                f"{tag}: missing baseline or corrected CSV")
        require(sha256(base_path) == record["baseline_sha256"],
                f"{tag}: baseline authentication failed")
        require(sha256(corrected_path) == record["output_sha256"],
                f"{tag}: corrected CSV authentication failed")
        base, corr = read_csv(base_path), read_csv(corrected_path)
        require(len(base) == len(corr) == ROWS, f"{tag}: row population differs")
        old = panel[(panel.t0 == t0) & (panel.t1 == t1)]
        require(len(old) == ROWS, f"{tag}: canonical panel population differs")
        # Check the complete source-panel schema against its authenticated CSV.
        source_diff = maximum_difference(old, base[old.columns.tolist()],
                                         f"{tag}: baseline to panel", 2e-6)
        totals = ["stock0_pas"] + [f"flow_pas_{d}" for d in DEST]
        selected = KEY + ["GRID_ID", "source_batch_id", "diagnostic_interval"] + totals
        require(set(selected).issubset(corr.columns), f"{tag}: closure schema differs")
        closure_diff = maximum_difference(base[selected], corr[selected],
                                          f"{tag}: source versus corrected", AREA_TOL)
        cc = canonicalize(corr)
        require(cc.cell_id.nunique() == ROWS and set(cc.diagnostic_interval) ==
                {int(t0 == 2020)}, f"{tag}: corrected population/flag differs")
        numeric = cc[["stock0_pas"] + [f"origin_{o}" for o in ORIGIN] +
                     [f"flow_pas_{d}" for d in DEST] +
                     [f"pas_{o}_to_{d}" for o in ORIGIN for d in DEST]]
        require(np.isfinite(numeric.to_numpy(dtype=float)).all() and
                (numeric.to_numpy(dtype=float) >= -1e-7).all(),
                f"{tag}: invalid closure area")
        # Origin components are new. They are checked here so the gate cannot
        # pass against a table with unchanged totals but a broken partition.
        partition_max = 0.0
        for d in DEST:
            diff = (cc[f"flow_pas_{d}"] - sum(cc[f"pas_{o}_to_{d}"]
                                                for o in ORIGIN)).abs().max()
            partition_max = max(partition_max, float(diff))
        require(partition_max <= AREA_TOL, f"{tag}: origin partition differs")
        interval_records.append({
            "interval": tag, "cells": ROWS,
            "max_source_panel_delta_ha": max(source_diff.values(), default=0.0),
            "max_corrected_nonorigin_delta_ha": max(closure_diff.values(), default=0.0),
            "max_origin_partition_residual_ha": partition_max,
            "baseline_sha256": record["baseline_sha256"],
            "corrected_sha256": record["output_sha256"],
        })
        print(f"PASS | {t0}–{t1} | cells={ROWS:,} | "
              f"max non-origin delta={max(closure_diff.values(),default=0):.3g} ha")

    # Authenticate the accepted dependency chain. Select the source fields
    # Phase 2 actually uses; none is a source-age/origin partition field.
    require(not LEGACY_ORIGIN.intersection(SPATIAL_INPUTS),
            "A source-age field is listed as a Phase 2 dependency")
    import pyarrow.parquet as pq
    derived_schema = set(pq.read_schema(paths["derived"]).names)
    derived_columns = list(dict.fromkeys(
        KEY + [c for c in panel.columns if c not in LEGACY_ORIGIN] +
        [c for c in SPATIAL_INPUTS if c in derived_schema]))
    require(set(derived_columns).issubset(derived_schema),
            "Accepted derived schema lacks a canonical non-origin field")
    derived = pd.read_parquet(paths["derived"], columns=derived_columns)
    integrated = pd.read_parquet(paths["integrated"], columns=SPATIAL_INPUTS)
    spatial = pd.read_parquet(paths["spatial"], columns=SPATIAL_INPUTS)
    require(all(len(f) == ROWS * 8 for f in (derived, integrated, spatial)),
            "Accepted downstream populations differ")
    common = [c for c in panel.columns if c not in LEGACY_ORIGIN]
    panel_to_derived = maximum_difference(panel[common], derived[common],
                                          "canonical panel to derived", 0.0)
    common_spatial = [c for c in SPATIAL_INPUTS if c in derived.columns]
    derived_to_integrated = maximum_difference(derived[common_spatial],
                                                integrated[common_spatial],
                                                "derived to integrated", 0.0)
    integrated_to_spatial = maximum_difference(integrated[SPATIAL_INPUTS],
                                                spatial[SPATIAL_INPUTS],
                                                "integrated to spatial", 0.0)

    result = {
        "status": "PASS",
        "scope": "nonorigin_pas_closure_and_accepted_phase2_dependency_chain",
        "script_version": "phase9-pasture-spell-nonorigin-invariance-v1",
        "decision_024_criterion_9_fully_implemented": False,
        "independent_reexport_of_all_nonorigin_raster_fields": False,
        "interpretation": (
            "The correction changes episode-origin attribution. All newly "
            "exported PAS stock and nine endpoint totals reproduce the accepted "
            "v1 source per cell, and accepted non-origin Phase 2 inputs are "
            "identical along the authenticated panel chain. No Phase 2–8 "
            "recomputation is indicated by this gate; full criterion 9 also "
            "requires a versioned corrected panel and explicit comparison "
            "of all non-origin fields."
        ),
        "accepted_panel_hashes": checked_hashes,
        "intervals": interval_records,
        "nonorigin_original_panel_columns_checked": common,
        "phase2_input_columns_checked": SPATIAL_INPUTS,
        "legacy_origin_columns_excluded_from_invariance": sorted(LEGACY_ORIGIN),
        "max_stage_delta": {
            "panel_to_derived": max(panel_to_derived.values(), default=0.0),
            "derived_to_integrated": max(derived_to_integrated.values(), default=0.0),
            "integrated_to_spatial": max(integrated_to_spatial.values(), default=0.0),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    validation = output_dir / "canonical_pasture_spell_nonorigin_invariance_validation_v1.json"
    inventory = output_dir / "canonical_pasture_spell_nonorigin_invariance_intervals_v1.csv"
    tmp = validation.with_suffix(".json.partial")
    tmp.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    tmp.replace(validation)
    with inventory.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=interval_records[0].keys())
        writer.writeheader()
        writer.writerows(interval_records)
    print("NON-ORIGIN PAS CLOSURE AND PHASE 2 DEPENDENCY GATE — PASS")
    print("Decision 024 criterion 9 fully complete: False")
    print("Validation:", validation)
    print("Interval record:", inventory)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-dir", type=Path,
                   default=Path("/content/drive/MyDrive/Trabalho/Contabilidade"))
    p.add_argument("--baseline-dir", type=Path)
    p.add_argument("--closure-dir", type=Path)
    p.add_argument("--output-dir", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    self_test()
    if args.self_test:
        return
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

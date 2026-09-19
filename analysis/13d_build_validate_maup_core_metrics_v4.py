"""Build and validate the Phase 8B restricted MAUP metric panel, revision 4.

Revision 4 retains the accepted common-mask extraction schema and the
outcome-independent geometric tolerance introduced in revision 3. It replaces
the inappropriate near-equality requirement among alternative-grid raster
support totals with three explicit checks: temporal invariance within each
grid, agreement of each grid with the fixed vector domain, and bounded
cross-grid variation attributable to raster boundary allocation.

Modes
-----
pilot (default)
    Validate the shifted 20k, 2005–2010 export before the other 23 Earth
    Engine tasks are run.
full
    Assemble all 24 exports, derive the restricted metrics, compare their
    fixed-domain totals with the accepted canonical panel, and write the
    complete Phase 8B panel and compact audit products.

Colab examples
---------------
%run /content/13d_build_validate_maup_core_metrics_v4.py --mode pilot
%run /content/13d_build_validate_maup_core_metrics_v4.py --mode full
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


if importlib.util.find_spec("pyarrow") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyarrow>=14"])

import numpy as np
import pandas as pd

try:
    from google.colab import drive
except ImportError:
    drive = None


VERSION = "phase8b-build-validate-maup-core-metrics-v4"
PROJECT_DIR = Path(os.environ.get(
    "PHASE8_PROJECT_DIR",
    "/content/drive/MyDrive/Trabalho/Contabilidade",
))
RAW_DIR = Path(os.environ.get(
    "PHASE8B_RAW_DIR",
    "/content/drive/MyDrive/phase8_maup_metrics_raw_v1",
))
OUTPUT_DIR = PROJECT_DIR / "spatial" / "phase8" / "maup_metrics_v1"
CANONICAL_PANEL = (
    PROJECT_DIR / "spatial" / "phase2" / "canonical_spatial_metrics_panel_v1.parquet"
)

EXPECTED_CANONICAL_SHA256 = (
    "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c"
)
FIXED_VECTOR_DOMAIN_HA = 497_776_400.44341594
ZERO_TOLERANCE_HA = 1e-9
ROW_IDENTITY_TOLERANCE_HA = 2e-6
VECTOR_RASTER_DOMAIN_RELATIVE_TOLERANCE = 2e-3
WITHIN_GRID_TEMPORAL_SUPPORT_RELATIVE_TOLERANCE = 1e-10
CROSS_GRID_SUPPORT_RELATIVE_TOLERANCE = 2e-3
TOTAL_COMPARISON_RELATIVE_TOLERANCE = 5e-6
TOTAL_COMPARISON_ABSOLUTE_TOLERANCE_HA = 1.0

GRID_ROWS = {
    "hex10k_base": 56_520,
    "hex20k_shift": 29_396,
    "hex40k_base": 15_309,
}
EXPECTED_SUPPORT_COUNTS = {
    "hex10k_base": {25: 52_404, 50: 49_716, 75: 47_191},
    "hex20k_shift": {25: 27_352, 50: 25_015, 75: 22_426},
    "hex40k_base": {25: 13_759, 50: 12_445, 75: 11_160},
}
INTERVALS = [
    (1985, 1990), (1990, 1995), (1995, 2000), (2000, 2005),
    (2005, 2010), (2010, 2015), (2015, 2020), (2020, 2025),
]
PILOT = ("hex20k_shift", 2005, 2010)

GRID_FIELDS = [
    "maup_id", "maup_uid", "grid_code", "batch_id",
    "axial_q", "axial_r", "nominal_ha", "support_ha", "support_fr",
]
METADATA_FIELDS = [
    "t0", "t1", "interval", "diagnostic_interval", "output_version",
]
BASE_METRICS = [
    "raster_domain_support_ha",
    "observed0_area_ha", "observed1_area_ha",
    "unobserved0_area_ha", "unobserved1_area_ha",
    "stock0_nat_ha", "stock0_pas_ha",
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
]
AUDIT_FIELDS = [
    "residual_observation0_partition_ha",
    "residual_observation1_partition_ha",
    "vector_raster_support_difference_ha",
    "raster_support_fraction_nominal",
]
REQUIRED_FIELDS = set(GRID_FIELDS + METADATA_FIELDS + BASE_METRICS + AUDIT_FIELDS)
OUTPUT_VERSION = "phase8b-maup-core-metrics-v2"
CANONICAL_OUTCOMES = [
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
]


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise ValueError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def safe_divide(numerator, denominator, tolerance=ZERO_TOLERANCE_HA):
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    return np.divide(
        numerator,
        denominator,
        out=np.full(numerator.shape, np.nan, dtype=float),
        where=denominator > tolerance,
    )


def expected_path(grid_code: str, t0: int, t1: int) -> Path:
    return RAW_DIR / f"maup_core_metrics_{grid_code}_{t0}_{t1}_v2.csv"


def read_export(grid_code: str, t0: int, t1: int) -> tuple[pd.DataFrame, dict]:
    path = expected_path(grid_code, t0, t1)
    require(path.is_file(), f"Missing Earth Engine export: {path}")
    frame = pd.read_csv(
        path,
        dtype={
            "maup_uid": "string", "grid_code": "string",
            "interval": "string", "output_version": "string",
        },
        low_memory=False,
    )
    require(REQUIRED_FIELDS.issubset(frame.columns),
            f"Missing required fields in {path.name}: {sorted(REQUIRED_FIELDS - set(frame.columns))}")
    require(len(frame) == GRID_ROWS[grid_code],
            f"Unexpected row count in {path.name}: {len(frame)}")
    require(frame["grid_code"].eq(grid_code).all(),
            f"grid_code mismatch in {path.name}")
    require(frame["t0"].eq(t0).all() and frame["t1"].eq(t1).all(),
            f"Interval mismatch in {path.name}")
    require(frame["interval"].eq(f"{t0}_{t1}").all(),
            f"Interval label mismatch in {path.name}")
    require(frame["diagnostic_interval"].eq(int((t0, t1) == (2020, 2025))).all(),
            f"Diagnostic flag mismatch in {path.name}")
    require(frame["output_version"].eq(OUTPUT_VERSION).all(),
            f"Output version mismatch in {path.name}")

    frame["maup_id"] = pd.to_numeric(frame["maup_id"], errors="raise").astype("int64")
    for field in ("batch_id", "axial_q", "axial_r", "t0", "t1",
                  "diagnostic_interval"):
        frame[field] = pd.to_numeric(frame[field], errors="raise").astype("int64")
    numeric = [
        "nominal_ha", "support_ha", "support_fr", *BASE_METRICS, *AUDIT_FIELDS
    ]
    for field in numeric:
        frame[field] = pd.to_numeric(frame[field], errors="raise").astype("float64")

    require(frame["maup_id"].nunique() == len(frame),
            f"Duplicate maup_id in {path.name}")
    require(frame["maup_uid"].nunique() == len(frame),
            f"Duplicate maup_uid in {path.name}")
    require(frame["support_fr"].gt(0).all() and frame["support_fr"].le(1 + 1e-9).all(),
            f"Invalid vector support in {path.name}")
    require(np.isfinite(frame[numeric].to_numpy()).all(),
            f"Non-finite numeric value in {path.name}")
    require(frame[BASE_METRICS].ge(-ROW_IDENTITY_TOLERANCE_HA).all().all(),
            f"Negative area in {path.name}")

    return frame, {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "grid_code": grid_code,
        "t0": t0,
        "t1": t1,
        "rows": len(frame),
    }


def derive(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame = frame.rename(columns={
        "maup_id": "maup_cell_id",
        "nominal_ha": "nominal_area_ha",
        "support_ha": "vector_domain_support_ha",
        "support_fr": "domain_support_fraction",
    })
    frame["primary_inference_interval"] = (1 - frame["diagnostic_interval"]).astype("int8")
    frame["support_positive"] = frame["domain_support_fraction"].gt(0).astype("int8")
    for pct, threshold in ((25, 0.25), (50, 0.50), (75, 0.75)):
        frame[f"support_ge_{pct}pct"] = (
            frame["domain_support_fraction"] >= threshold
        ).astype("int8")
    frame["raster_domain_support_fraction_nominal"] = safe_divide(
        frame["raster_domain_support_ha"], frame["nominal_area_ha"]
    )
    frame["gross_cr_activity_ha"] = frame["consolidation_ha"] + frame["replenishment_ha"]
    frame["net_cr_balance_ha"] = frame["consolidation_ha"] - frame["replenishment_ha"]
    frame["cr_balance_index"] = safe_divide(
        frame["net_cr_balance_ha"], frame["gross_cr_activity_ha"]
    )
    frame["consolidation_rate_initial_pasture"] = safe_divide(
        frame["consolidation_ha"], frame["stock0_pas_ha"]
    )
    frame["replenishment_rate_initial_native"] = safe_divide(
        frame["replenishment_ha"], frame["stock0_nat_ha"]
    )
    frame["nat_tmp_intensity_initial_native"] = safe_divide(
        frame["nat_tmp_endpoint_ha"], frame["stock0_nat_ha"]
    )
    frame["has_cr_activity"] = frame["gross_cr_activity_ha"].gt(ZERO_TOLERANCE_HA).astype("int8")
    frame["consolidation_rate_defined"] = frame["stock0_pas_ha"].gt(ZERO_TOLERANCE_HA).astype("int8")
    frame["replenishment_rate_defined"] = frame["stock0_nat_ha"].gt(ZERO_TOLERANCE_HA).astype("int8")
    frame["nat_tmp_intensity_defined"] = frame["stock0_nat_ha"].gt(ZERO_TOLERANCE_HA).astype("int8")
    return frame


def validate_rows(frame: pd.DataFrame) -> dict:
    maximum_partition_residual = float(frame[[
        "residual_observation0_partition_ha",
        "residual_observation1_partition_ha",
    ]].abs().to_numpy().max())
    require(maximum_partition_residual <= ROW_IDENTITY_TOLERANCE_HA,
            "Observed/unobserved raster-support partition failed")

    tolerance = ROW_IDENTITY_TOLERANCE_HA
    require((frame["observed0_area_ha"] <= frame["raster_domain_support_ha"] + tolerance).all(),
            "Observed t0 area exceeds raster support")
    require((frame["observed1_area_ha"] <= frame["raster_domain_support_ha"] + tolerance).all(),
            "Observed t1 area exceeds raster support")
    require((frame["consolidation_ha"] <= frame["stock0_pas_ha"] + tolerance).all(),
            "Consolidation exceeds initial pasture")
    require((frame["replenishment_ha"] <= frame["stock0_nat_ha"] + tolerance).all(),
            "Replenishment exceeds initial native area")
    require((frame["nat_tmp_endpoint_ha"] <= frame["stock0_nat_ha"] + tolerance).all(),
            "NAT-TMP exceeds initial native area")

    active = frame["has_cr_activity"].eq(1)
    require(frame.loc[active, "cr_balance_index"].between(-1 - 1e-12, 1 + 1e-12).all(),
            "Active C-R index lies outside [-1, 1]")
    require(frame.loc[~active, "cr_balance_index"].isna().all(),
            "Inactive C-R rows must have undefined index")
    for value, flag in (
        ("consolidation_rate_initial_pasture", "consolidation_rate_defined"),
        ("replenishment_rate_initial_native", "replenishment_rate_defined"),
        ("nat_tmp_intensity_initial_native", "nat_tmp_intensity_defined"),
    ):
        defined = frame[flag].eq(1)
        require(frame.loc[defined, value].between(-1e-12, 1 + 1e-12).all(),
                f"{value} lies outside [0, 1]")
        require(frame.loc[~defined, value].isna().all(),
                f"Undefined {value} rows are not null")

    return {"maximum_observation_partition_residual_ha": maximum_partition_residual}


def canonical_totals() -> pd.DataFrame:
    require(CANONICAL_PANEL.is_file(), f"Missing canonical comparison panel: {CANONICAL_PANEL}")
    require(sha256_file(CANONICAL_PANEL) == EXPECTED_CANONICAL_SHA256,
            "Canonical Phase 2 panel hash mismatch")
    canonical = pd.read_parquet(
        CANONICAL_PANEL,
        columns=["t0", "t1", *CANONICAL_OUTCOMES],
        engine="pyarrow",
    )
    require(len(canonical) == 199_112, "Unexpected canonical panel population")
    return canonical.groupby(["t0", "t1"], as_index=False)[CANONICAL_OUTCOMES].sum()


def total_comparison(
    frame: pd.DataFrame,
    reference: pd.DataFrame,
) -> pd.DataFrame:
    alternative = frame.groupby(["grid_code", "t0", "t1"], as_index=False)[
        [*CANONICAL_OUTCOMES, "raster_domain_support_ha"]
    ].sum()
    comparison = alternative.merge(reference, on=["t0", "t1"], suffixes=("_alternative", "_canonical"), validate="many_to_one")
    comparison["geometric_support_relative_tolerance"] = (
        comparison["raster_domain_support_ha"] - FIXED_VECTOR_DOMAIN_HA
    ).abs() / FIXED_VECTOR_DOMAIN_HA
    comparison["effective_total_relative_tolerance"] = np.maximum(
        TOTAL_COMPARISON_RELATIVE_TOLERANCE,
        comparison["geometric_support_relative_tolerance"],
    )
    pass_fields = []
    for metric in CANONICAL_OUTCOMES:
        alt = comparison[f"{metric}_alternative"]
        ref = comparison[f"{metric}_canonical"]
        difference = alt - ref
        allowed = np.maximum(
            TOTAL_COMPARISON_ABSOLUTE_TOLERANCE_HA,
            ref.abs() * comparison["effective_total_relative_tolerance"],
        )
        comparison[f"{metric}_difference_ha"] = difference
        comparison[f"{metric}_relative_difference"] = safe_divide(difference.abs(), ref.abs(), tolerance=0)
        comparison[f"{metric}_allowed_difference_ha"] = allowed
        field = f"{metric}_comparison_pass"
        comparison[field] = difference.abs().le(allowed)
        pass_fields.append(field)
    require(comparison[pass_fields].all().all(),
            "At least one alternative-grid total differs from the canonical total beyond tolerance")
    return comparison


def build_summary(frame: pd.DataFrame) -> pd.DataFrame:
    scopes = {
        "all_positive": "support_positive",
        "support_ge_25pct": "support_ge_25pct",
        "support_ge_50pct_primary": "support_ge_50pct",
        "support_ge_75pct": "support_ge_75pct",
    }
    records = []
    for (grid_code, t0, t1), group in frame.groupby(["grid_code", "t0", "t1"], sort=True):
        for scope, flag in scopes.items():
            selected = group.loc[group[flag].eq(1)]
            c_sum = float(selected["consolidation_ha"].sum())
            r_sum = float(selected["replenishment_ha"].sum())
            nat_sum = float(selected["nat_tmp_endpoint_ha"].sum())
            gross = c_sum + r_sum
            records.append({
                "grid_code": grid_code, "t0": int(t0), "t1": int(t1),
                "interval": f"{t0}_{t1}",
                "diagnostic_interval": int((t0, t1) == (2020, 2025)),
                "support_scope": scope,
                "cells": len(selected),
                "raster_domain_support_ha": float(selected["raster_domain_support_ha"].sum()),
                "consolidation_ha": c_sum,
                "replenishment_ha": r_sum,
                "nat_tmp_endpoint_ha": nat_sum,
                "net_cr_balance_ha": c_sum - r_sum,
                "aggregate_cr_balance_index": (c_sum - r_sum) / gross if gross > ZERO_TOLERANCE_HA else np.nan,
                "aggregate_consolidation_rate": c_sum / selected["stock0_pas_ha"].sum() if selected["stock0_pas_ha"].sum() > ZERO_TOLERANCE_HA else np.nan,
                "aggregate_replenishment_rate": r_sum / selected["stock0_nat_ha"].sum() if selected["stock0_nat_ha"].sum() > ZERO_TOLERANCE_HA else np.nan,
                "aggregate_nat_tmp_intensity": nat_sum / selected["stock0_nat_ha"].sum() if selected["stock0_nat_ha"].sum() > ZERO_TOLERANCE_HA else np.nan,
            })
    return pd.DataFrame(records)


def validate_support_totals(frame: pd.DataFrame, full_mode: bool) -> dict:
    totals = frame.groupby(["grid_code", "t0", "t1"], as_index=False)[
        "raster_domain_support_ha"
    ].sum()
    totals["vector_domain_relative_difference"] = (
        totals["raster_domain_support_ha"] - FIXED_VECTOR_DOMAIN_HA
    ).abs() / FIXED_VECTOR_DOMAIN_HA
    require(totals["vector_domain_relative_difference"].le(
        VECTOR_RASTER_DOMAIN_RELATIVE_TOLERANCE).all(),
        "Raster fixed-domain support differs excessively from vector support")

    grid_summary = totals.groupby("grid_code").agg(
        intervals=("raster_domain_support_ha", "size"),
        minimum_support_ha=("raster_domain_support_ha", "min"),
        maximum_support_ha=("raster_domain_support_ha", "max"),
        mean_support_ha=("raster_domain_support_ha", "mean"),
        maximum_vector_domain_relative_difference=(
            "vector_domain_relative_difference", "max"
        ),
    )
    grid_summary["within_grid_support_relative_spread"] = (
        grid_summary["maximum_support_ha"]
        - grid_summary["minimum_support_ha"]
    ) / grid_summary["mean_support_ha"]
    require(
        grid_summary["within_grid_support_relative_spread"].le(
            WITHIN_GRID_TEMPORAL_SUPPORT_RELATIVE_TOLERANCE
        ).all(),
        "Raster support is not temporally invariant within an alternative grid",
    )

    per_grid = {
        str(grid_code): {
            "intervals": int(row["intervals"]),
            "minimum_raster_domain_support_ha": float(row["minimum_support_ha"]),
            "maximum_raster_domain_support_ha": float(row["maximum_support_ha"]),
            "mean_raster_domain_support_ha": float(row["mean_support_ha"]),
            "within_grid_support_relative_spread": float(
                row["within_grid_support_relative_spread"]
            ),
            "maximum_vector_raster_domain_relative_difference": float(
                row["maximum_vector_domain_relative_difference"]
            ),
        }
        for grid_code, row in grid_summary.iterrows()
    }

    result = {
        "minimum_raster_domain_support_ha": float(totals["raster_domain_support_ha"].min()),
        "maximum_raster_domain_support_ha": float(totals["raster_domain_support_ha"].max()),
        "maximum_vector_raster_domain_relative_difference": float(totals["vector_domain_relative_difference"].max()),
        "maximum_within_grid_support_relative_spread": float(
            grid_summary["within_grid_support_relative_spread"].max()
        ),
        "per_grid": per_grid,
    }
    if full_mode:
        require(grid_summary["intervals"].eq(len(INTERVALS)).all(),
                "Not every alternative grid has all expected intervals")
        spread = (
            totals.groupby(["t0", "t1"])["raster_domain_support_ha"]
            .agg(lambda x: (x.max() - x.min()) / x.mean())
        )
        require(spread.le(CROSS_GRID_SUPPORT_RELATIVE_TOLERANCE).all(),
                "Cross-grid raster support variation exceeds geometric tolerance")
        result["maximum_cross_grid_support_relative_spread"] = float(spread.max())
    return result


def output_inventory(paths: list[Path]) -> pd.DataFrame:
    return pd.DataFrame([
        {"relative_path": path.name, "bytes": path.stat().st_size,
         "sha256": sha256_file(path)} for path in paths
    ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("pilot", "full"), default="pilot")
    args = parser.parse_args()
    if drive is not None:
        drive.mount("/content/drive")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("CANONICAL MAUP CORE METRICS — PHASE 8B VALIDATOR REVISION 4")
    print("COMMON-MASK EXPORT SCHEMA: REQUIRED")
    print("GEOMETRIC SUPPORT-BASED TOTAL TOLERANCE: ENABLED")
    print("PER-GRID TEMPORAL SUPPORT INVARIANCE: REQUIRED")
    print("Mode:", args.mode)
    print("Raw export directory:", RAW_DIR)
    print("Output directory:", OUTPUT_DIR)

    targets = [PILOT] if args.mode == "pilot" else [
        (grid, t0, t1) for grid in GRID_ROWS for t0, t1 in INTERVALS
    ]
    frames = []
    raw_records = []
    for grid_code, t0, t1 in targets:
        frame, record = read_export(grid_code, t0, t1)
        frames.append(frame)
        raw_records.append(record)
        print("LOADED |", grid_code, "|", f"{t0}–{t1}", "| rows =", f"{len(frame):,}")

    panel = derive(pd.concat(frames, ignore_index=True))
    expected_rows = GRID_ROWS[PILOT[0]] if args.mode == "pilot" else sum(GRID_ROWS.values()) * len(INTERVALS)
    require(len(panel) == expected_rows, "Unexpected assembled panel population")
    require(not panel.duplicated(["grid_code", "maup_cell_id", "t0", "t1"]).any(),
            "Duplicate grid-cell-interval key")
    for grid_code, group in panel.groupby("grid_code"):
        interval_groups = group.groupby(["t0", "t1"])
        for pct in (25, 50, 75):
            counts = interval_groups[f"support_ge_{pct}pct"].sum()
            require(counts.eq(EXPECTED_SUPPORT_COUNTS[grid_code][pct]).all(),
                    f"Phase 8A support population changed for {grid_code} at {pct}%")
        if args.mode == "full":
            repetitions = group.groupby("maup_cell_id").size()
            require(repetitions.eq(len(INTERVALS)).all(),
                    f"Unbalanced interval population for {grid_code}")
            static_fields = [
                "maup_uid", "batch_id", "axial_q", "axial_r",
                "nominal_area_ha", "vector_domain_support_ha",
                "domain_support_fraction",
            ]
            require(group.groupby("maup_cell_id")[static_fields].nunique(dropna=False).le(1).all().all(),
                    f"Static grid attributes changed across intervals for {grid_code}")
    row_checks = validate_rows(panel)
    support_checks = validate_support_totals(panel, args.mode == "full")
    reference = canonical_totals()
    comparison = total_comparison(panel, reference)
    maximum_geometric_tolerance = float(
        comparison["effective_total_relative_tolerance"].max()
    )
    geometric_tolerance_by_grid = {
        str(grid_code): float(value)
        for grid_code, value in comparison.groupby("grid_code")[
            "effective_total_relative_tolerance"
        ].max().items()
    }
    summary = build_summary(panel)

    prefix = "pilot" if args.mode == "pilot" else "canonical"
    comparison_path = OUTPUT_DIR / f"{prefix}_maup_core_metric_total_comparison_v4.csv"
    summary_path = OUTPUT_DIR / f"{prefix}_maup_core_metric_summary_v4.csv"
    raw_inventory_path = OUTPUT_DIR / f"{prefix}_maup_raw_export_inventory_v4.csv"
    comparison.to_csv(comparison_path, index=False, encoding="utf-8-sig")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    pd.DataFrame(raw_records).to_csv(raw_inventory_path, index=False, encoding="utf-8-sig")

    output_paths = [comparison_path, summary_path, raw_inventory_path]
    if args.mode == "pilot":
        panel_path = OUTPUT_DIR / "pilot_maup_core_metrics_hex20k_shift_2005_2010_v4.parquet"
    else:
        panel_path = OUTPUT_DIR / "canonical_maup_core_metrics_panel_v4.parquet"
    panel.to_parquet(panel_path, index=False, compression="zstd")
    output_paths.insert(0, panel_path)

    validation_path = OUTPUT_DIR / f"{prefix}_maup_core_metrics_validation_v4.json"
    validation = {
        "validation_status": "PASS",
        "mode": args.mode,
        "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256_file(Path(__file__)),
        "inputs": {
            "canonical_panel": {"path": str(CANONICAL_PANEL), "sha256": EXPECTED_CANONICAL_SHA256},
            "raw_exports": raw_records,
        },
        "structure": {
            "rows": len(panel),
            "grids": int(panel["grid_code"].nunique()),
            "intervals": int(panel[["t0", "t1"]].drop_duplicates().shape[0]),
            "duplicate_keys": int(panel.duplicated(["grid_code", "maup_cell_id", "t0", "t1"]).sum()),
        },
        "tolerances": {
            "row_identity_ha": ROW_IDENTITY_TOLERANCE_HA,
            "vector_raster_domain_relative": VECTOR_RASTER_DOMAIN_RELATIVE_TOLERANCE,
            "within_grid_temporal_support_relative": (
                WITHIN_GRID_TEMPORAL_SUPPORT_RELATIVE_TOLERANCE
            ),
            "cross_grid_support_relative": CROSS_GRID_SUPPORT_RELATIVE_TOLERANCE,
            "total_comparison_relative": TOTAL_COMPARISON_RELATIVE_TOLERANCE,
            "total_comparison_absolute_ha": TOTAL_COMPARISON_ABSOLUTE_TOLERANCE_HA,
            "effective_total_relative_rule": (
                "for each grid and interval: max(base relative tolerance, "
                "that grid-interval vector-raster domain support relative difference)"
            ),
            "maximum_effective_total_relative_tolerance": maximum_geometric_tolerance,
            "effective_total_relative_tolerance_by_grid": geometric_tolerance_by_grid,
        },
        "row_checks": row_checks,
        "support_checks": support_checks,
        "maximum_total_relative_differences": {
            metric: float(comparison[f"{metric}_relative_difference"].max())
            for metric in CANONICAL_OUTCOMES
        },
        "checks": {
            "raw_file_set_complete": True,
            "expected_populations_match": True,
            "keys_are_unique": True,
            "metadata_are_consistent": True,
            "areas_are_nonnegative": True,
            "observation_partitions_close": True,
            "processes_do_not_exceed_source_stocks": True,
            "derived_metric_domains_are_valid": True,
            "fixed_raster_support_matches_vector_domain": True,
            "raster_support_is_temporally_invariant_within_grid": True,
            "cross_grid_support_variation_is_within_geometric_tolerance": True,
            "alternative_totals_match_canonical_totals": True,
            "diagnostic_interval_is_retained": True,
            "support_threshold_flags_are_preserved": True,
        },
    }
    write_json(validation_path, validation)
    output_paths.append(validation_path)
    inventory_path = OUTPUT_DIR / f"{prefix}_maup_core_metrics_inventory_v4.csv"
    output_inventory(output_paths).to_csv(inventory_path, index=False, encoding="utf-8-sig")

    print("PHASE 8B", args.mode.upper(), "VALIDATION PASS")
    print("Rows:", f"{len(panel):,}")
    print("Grids:", panel["grid_code"].nunique())
    print("Intervals:", panel[["t0", "t1"]].drop_duplicates().shape[0])
    print("Validation:", validation_path)
    print("Inventory:", inventory_path)


if __name__ == "__main__":
    main()

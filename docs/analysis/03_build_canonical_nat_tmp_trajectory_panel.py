"""
03_build_canonical_nat_tmp_trajectory_panel.py

Build and validate the canonical 1985-2025 NAT-to-TMP within-interval
trajectory panel from the eight complete-domain CSV exports in Google Drive.

Designed for Google Colab. Run the complete script in one cell or upload it
and execute with %run. Source CSV and stock-flow panel files are read only and
never modified.
"""

from google.colab import drive
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import numpy as np
import pandas as pd


# Parquet support is normally preinstalled in Colab. Install it only when the
# current runtime does not provide it.
try:
    import pyarrow  # noqa: F401
except ImportError:
    print("Installing the missing pyarrow dependency ...")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--quiet",
        "pyarrow",
    ])


# ---------------------------------------------------------------------------
# Google Drive and paths
# ---------------------------------------------------------------------------

drive.mount("/content/drive")

PROJECT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade")
INPUT_DIR = PROJECT_DIR / "csv"
OUTPUT_DIR = PROJECT_DIR / "panel"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STOCK_FLOW_PANEL_PATH = (
    OUTPUT_DIR / "canonical_stock_flow_panel_1985_2025_v1.parquet"
)

PANEL_PATH = (
    OUTPUT_DIR
    / "canonical_nat_tmp_trajectory_panel_1985_2025_v1.parquet"
)
MANIFEST_PATH = (
    OUTPUT_DIR
    / "canonical_nat_tmp_trajectory_panel_manifest_v1.csv"
)
VALIDATION_PATH = (
    OUTPUT_DIR
    / "canonical_nat_tmp_trajectory_panel_validation_v1.json"
)
SUMMARY_PATH = (
    OUTPUT_DIR
    / "canonical_nat_tmp_trajectory_summary_v1.csv"
)

INTERVALS = [
    (1985, 1990),
    (1990, 1995),
    (1995, 2000),
    (2000, 2005),
    (2005, 2010),
    (2010, 2015),
    (2015, 2020),
    (2020, 2025),
]

EXPECTED_ROWS_PER_INTERVAL = 24_889
EXPECTED_COLUMNS = 28
EXPECTED_PANEL_ROWS = EXPECTED_ROWS_PER_INTERVAL * len(INTERVALS)
OUTPUT_VERSION = "canonical-nat-tmp-trajectory-v1"

AREA_TOLERANCE_HA = 1e-9
RECONCILIATION_TOLERANCE_HA = 2e-6

# Validated by analysis/01_build_canonical_stock_flow_panel.py and used by
# analysis/02_derive_stock_flow_metrics.py. This protects the external closure
# control from accidental substitution.
EXPECTED_STOCK_FLOW_PANEL_SHA256 = (
    "2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64"
)

AREA_COLUMNS = [
    "geometry_area_ha",
    "nat_tmp_endpoint_ha",
    "nat_tmp_mid_all_observed_ha",
    "nat_tmp_mid_incomplete_ha",
    "nat_tmp_pas_years_0_ha",
    "nat_tmp_pas_years_1_ha",
    "nat_tmp_pas_years_2_ha",
    "nat_tmp_pas_years_3_ha",
    "nat_tmp_pas_years_4_ha",
    "nat_tmp_pas_any_ha",
    "nat_tmp_pas_2plus_ha",
    "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_pas_any_nonconsecutive2_ha",
    "raster_area_ha",
]

RESIDUAL_COLUMNS = [
    "residual_endpoint_observation_partition",
    "residual_pas_count_partition",
    "residual_pas_any_partition",
    "residual_pas_2plus_partition",
    "residual_pas_consecutive_partition",
]

SUMMARY_AREA_COLUMNS = [
    "nat_tmp_endpoint_ha",
    "nat_tmp_mid_all_observed_ha",
    "nat_tmp_mid_incomplete_ha",
    "nat_tmp_pas_years_0_ha",
    "nat_tmp_pas_years_1_ha",
    "nat_tmp_pas_years_2_ha",
    "nat_tmp_pas_years_3_ha",
    "nat_tmp_pas_years_4_ha",
    "nat_tmp_pas_any_ha",
    "nat_tmp_pas_2plus_ha",
    "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_pas_any_nonconsecutive2_ha",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def expected_filename(t0, t1):
    return f"canonical_nat_tmp_trajectory_{t0}_{t1}_full_v1.csv"


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def safe_ratio(numerator, denominator):
    if abs(denominator) <= AREA_TOLERANCE_HA:
        return np.nan
    return numerator / denominator


# ---------------------------------------------------------------------------
# Inventory and per-interval validation
# ---------------------------------------------------------------------------

print("CANONICAL NAT-TMP TRAJECTORY PANEL BUILD - VERSION 1")
print("Input directory:", INPUT_DIR)
print("Output directory:", OUTPUT_DIR)

require(INPUT_DIR.exists(), f"Input directory not found: {INPUT_DIR}")

expected_paths = {
    (t0, t1): INPUT_DIR / expected_filename(t0, t1)
    for t0, t1 in INTERVALS
}

missing_files = [
    str(path) for path in expected_paths.values() if not path.exists()
]
require(
    not missing_files,
    "Missing expected files:\n" + "\n".join(missing_files),
)

frames = {}
manifest_rows = []
interval_checks = []
summary_rows = []
reference_columns = None
reference_cell_ids = None
reference_grid_ids = None

for t0, t1 in INTERVALS:
    interval = f"{t0}_{t1}"
    path = expected_paths[(t0, t1)]
    expected_mid_years = ",".join(str(year) for year in range(t0 + 1, t1))
    expected_diagnostic = 1 if (t0, t1) == (2020, 2025) else 0

    print(f"Reading {path.name} ...")
    frame = pd.read_csv(path, low_memory=False)

    if reference_columns is None:
        reference_columns = frame.columns.tolist()
        reference_cell_ids = set(frame["cell_id"].astype(str))
        reference_grid_ids = set(frame["GRID_ID"].astype(str))

    require(
        frame.shape == (EXPECTED_ROWS_PER_INTERVAL, EXPECTED_COLUMNS),
        f"{interval}: unexpected shape {frame.shape}",
    )
    require(
        frame.columns.tolist() == reference_columns,
        f"{interval}: column names or order differ from the reference",
    )
    require(
        frame["cell_id"].nunique() == EXPECTED_ROWS_PER_INTERVAL,
        f"{interval}: cell_id is not unique",
    )
    require(
        frame["GRID_ID"].nunique() == EXPECTED_ROWS_PER_INTERVAL,
        f"{interval}: GRID_ID is not unique",
    )
    require(
        set(frame["cell_id"].astype(str)) == reference_cell_ids,
        f"{interval}: cell_id membership differs from the fixed domain",
    )
    require(
        set(frame["GRID_ID"].astype(str)) == reference_grid_ids,
        f"{interval}: GRID_ID membership differs from the fixed domain",
    )
    require(
        int(frame.isna().sum().sum()) == 0,
        f"{interval}: missing values found",
    )

    require(set(frame["t0"].unique()) == {t0},
            f"{interval}: invalid t0 metadata")
    require(set(frame["t1"].unique()) == {t1},
            f"{interval}: invalid t1 metadata")
    require(set(frame["interval"].astype(str).unique()) == {interval},
            f"{interval}: invalid interval label")
    require(set(frame["output_version"].unique()) == {OUTPUT_VERSION},
            f"{interval}: invalid output_version")
    require(
        set(frame["diagnostic_interval"].unique()) == {expected_diagnostic},
        f"{interval}: invalid diagnostic_interval flag",
    )
    require(
        set(frame["intermediate_years"].astype(str).unique())
        == {expected_mid_years},
        f"{interval}: invalid intermediate_years metadata",
    )

    negative_area_values = int(
        (frame[AREA_COLUMNS] < -AREA_TOLERANCE_HA).sum().sum()
    )
    require(
        negative_area_values == 0,
        f"{interval}: negative area values found",
    )

    residual_maximum = float(frame[RESIDUAL_COLUMNS].abs().max().max())
    residual_rows_over_tolerance = int(
        (frame[RESIDUAL_COLUMNS].abs() > AREA_TOLERANCE_HA)
        .any(axis=1)
        .sum()
    )
    require(
        residual_rows_over_tolerance == 0,
        f"{interval}: an accounting residual exceeds tolerance",
    )

    subset_violations = {
        "consecutive2_gt_2plus": int((
            frame["nat_tmp_pas_consecutive2_ha"]
            > frame["nat_tmp_pas_2plus_ha"] + AREA_TOLERANCE_HA
        ).sum()),
        "2plus_gt_any": int((
            frame["nat_tmp_pas_2plus_ha"]
            > frame["nat_tmp_pas_any_ha"] + AREA_TOLERANCE_HA
        ).sum()),
        "any_gt_all_observed": int((
            frame["nat_tmp_pas_any_ha"]
            > frame["nat_tmp_mid_all_observed_ha"] + AREA_TOLERANCE_HA
        ).sum()),
        "all_observed_gt_endpoint": int((
            frame["nat_tmp_mid_all_observed_ha"]
            > frame["nat_tmp_endpoint_ha"] + AREA_TOLERANCE_HA
        ).sum()),
    }
    require(
        sum(subset_violations.values()) == 0,
        f"{interval}: trajectory subset relationship failed",
    )

    totals = {
        column: float(frame[column].sum())
        for column in SUMMARY_AREA_COLUMNS
    }
    endpoint = totals["nat_tmp_endpoint_ha"]
    pasture_any = totals["nat_tmp_pas_any_ha"]
    pasture_2plus = totals["nat_tmp_pas_2plus_ha"]
    pasture_consecutive2 = totals["nat_tmp_pas_consecutive2_ha"]

    summary_rows.append({
        "interval": interval,
        "t0": t0,
        "t1": t1,
        "diagnostic_interval": expected_diagnostic,
        **totals,
        "nat_tmp_pas_any_share_endpoint": safe_ratio(
            pasture_any, endpoint
        ),
        "nat_tmp_pas_2plus_share_endpoint": safe_ratio(
            pasture_2plus, endpoint
        ),
        "nat_tmp_pas_consecutive2_share_endpoint": safe_ratio(
            pasture_consecutive2, endpoint
        ),
        "nat_tmp_pas_consecutive2_share_any": safe_ratio(
            pasture_consecutive2, pasture_any
        ),
        "nat_tmp_mid_incomplete_share_endpoint": safe_ratio(
            totals["nat_tmp_mid_incomplete_ha"], endpoint
        ),
        "positive_endpoint_cells": int(
            (frame["nat_tmp_endpoint_ha"] > AREA_TOLERANCE_HA).sum()
        ),
        "positive_pas_any_cells": int(
            (frame["nat_tmp_pas_any_ha"] > AREA_TOLERANCE_HA).sum()
        ),
        "positive_pas_2plus_cells": int(
            (frame["nat_tmp_pas_2plus_ha"] > AREA_TOLERANCE_HA).sum()
        ),
        "positive_pas_consecutive2_cells": int(
            (frame["nat_tmp_pas_consecutive2_ha"] > AREA_TOLERANCE_HA).sum()
        ),
        "positive_incomplete_support_cells": int(
            (frame["nat_tmp_mid_incomplete_ha"] > AREA_TOLERANCE_HA).sum()
        ),
    })

    manifest_rows.append({
        "interval": interval,
        "t0": t0,
        "t1": t1,
        "filename": path.name,
        "file_size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "diagnostic_interval": expected_diagnostic,
    })

    interval_checks.append({
        "interval": interval,
        "rows": int(frame.shape[0]),
        "columns": int(frame.shape[1]),
        "unique_cell_id": int(frame["cell_id"].nunique()),
        "unique_GRID_ID": int(frame["GRID_ID"].nunique()),
        "missing_values": int(frame.isna().sum().sum()),
        "negative_area_values": negative_area_values,
        "maximum_absolute_residual_ha": residual_maximum,
        "residual_rows_over_1e_9_ha": residual_rows_over_tolerance,
        "subset_violations": subset_violations,
        "incomplete_support_area_ha": totals[
            "nat_tmp_mid_incomplete_ha"
        ],
        "incomplete_support_positive_cells": int(
            (frame["nat_tmp_mid_incomplete_ha"] > AREA_TOLERANCE_HA).sum()
        ),
    })

    frames[(t0, t1)] = frame


# ---------------------------------------------------------------------------
# Panel assembly
# ---------------------------------------------------------------------------

panel = pd.concat(
    [frames[interval] for interval in INTERVALS],
    axis=0,
    ignore_index=True,
    copy=False,
)

panel = panel.sort_values(
    ["cell_id", "t0", "t1"], kind="stable"
).reset_index(drop=True)

require(
    panel.shape == (EXPECTED_PANEL_ROWS, EXPECTED_COLUMNS),
    f"Final panel has unexpected shape: {panel.shape}",
)
require(
    panel.duplicated(subset=["cell_id", "t0", "t1"]).sum() == 0,
    "Final panel contains duplicate cell-interval rows",
)
require(
    panel.groupby("cell_id")["interval"].nunique().eq(8).all(),
    "At least one cell does not contain all eight intervals",
)
require(
    int(panel["diagnostic_interval"].sum()) == EXPECTED_ROWS_PER_INTERVAL,
    "Diagnostic flag count is not 24,889",
)


# ---------------------------------------------------------------------------
# External reconciliation with the validated stock-flow panel
# ---------------------------------------------------------------------------

require(
    STOCK_FLOW_PANEL_PATH.exists(),
    f"Validated stock-flow panel not found: {STOCK_FLOW_PANEL_PATH}",
)

stock_flow_panel_sha256 = sha256_file(STOCK_FLOW_PANEL_PATH)
require(
    stock_flow_panel_sha256 == EXPECTED_STOCK_FLOW_PANEL_SHA256,
    "The stock-flow panel checksum differs from the validated version.\n"
    f"Expected: {EXPECTED_STOCK_FLOW_PANEL_SHA256}\n"
    f"Found:    {stock_flow_panel_sha256}",
)

stock_flow = pd.read_parquet(
    STOCK_FLOW_PANEL_PATH,
    columns=["cell_id", "t0", "t1", "flow_nat_tmp"],
    engine="pyarrow",
)

require(
    stock_flow.shape[0] == EXPECTED_PANEL_ROWS,
    f"Unexpected stock-flow panel row count: {stock_flow.shape[0]}",
)
require(
    stock_flow.duplicated(subset=["cell_id", "t0", "t1"]).sum() == 0,
    "Stock-flow closure control contains duplicate cell-interval rows",
)

trajectory_closure = panel[[
    "cell_id", "t0", "t1", "nat_tmp_endpoint_ha"
]].copy()
stock_flow_closure = stock_flow.copy()

# String keys make the comparison robust to harmless integer/string import
# differences while leaving the canonical panel fields unchanged.
trajectory_closure["_cell_key"] = trajectory_closure["cell_id"].astype(str)
stock_flow_closure["_cell_key"] = stock_flow_closure["cell_id"].astype(str)

closure = trajectory_closure.merge(
    stock_flow_closure,
    on=["_cell_key", "t0", "t1"],
    how="outer",
    indicator=True,
    suffixes=("_trajectory", "_stock_flow"),
)

unmatched_closure_rows = int((closure["_merge"] != "both").sum())
require(
    unmatched_closure_rows == 0,
    "Trajectory and stock-flow panels have unmatched cell-interval rows",
)

closure["absolute_difference_ha"] = (
    closure["nat_tmp_endpoint_ha"] - closure["flow_nat_tmp"]
).abs()

maximum_reconciliation_difference = float(
    closure["absolute_difference_ha"].max()
)
reconciliation_rows_over_tolerance = int((
    closure["absolute_difference_ha"] > RECONCILIATION_TOLERANCE_HA
).sum())

require(
    reconciliation_rows_over_tolerance == 0,
    "Trajectory endpoint does not reconcile with canonical flow_nat_tmp",
)

reconciliation_checks = []
for t0, t1 in INTERVALS:
    interval_mask = (closure["t0"] == t0) & (closure["t1"] == t1)
    interval_closure = closure.loc[interval_mask]
    reconciliation_checks.append({
        "interval": f"{t0}_{t1}",
        "matched_rows": int(len(interval_closure)),
        "maximum_absolute_difference_ha": float(
            interval_closure["absolute_difference_ha"].max()
        ),
        "rows_over_2e_6_ha": int((
            interval_closure["absolute_difference_ha"]
            > RECONCILIATION_TOLERANCE_HA
        ).sum()),
        "trajectory_endpoint_total_ha": float(
            interval_closure["nat_tmp_endpoint_ha"].sum()
        ),
        "stock_flow_endpoint_total_ha": float(
            interval_closure["flow_nat_tmp"].sum()
        ),
    })


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

manifest = pd.DataFrame(manifest_rows)
manifest.to_csv(MANIFEST_PATH, index=False)

summary = pd.DataFrame(summary_rows)
summary.to_csv(SUMMARY_PATH, index=False)

panel.to_parquet(
    PANEL_PATH,
    index=False,
    engine="pyarrow",
    compression="snappy",
)

panel_sha256 = sha256_file(PANEL_PATH)

pooled_endpoint = float(panel["nat_tmp_endpoint_ha"].sum())
pooled_any = float(panel["nat_tmp_pas_any_ha"].sum())
pooled_2plus = float(panel["nat_tmp_pas_2plus_ha"].sum())
pooled_consecutive2 = float(
    panel["nat_tmp_pas_consecutive2_ha"].sum()
)
pooled_incomplete = float(
    panel["nat_tmp_mid_incomplete_ha"].sum()
)

validation = {
    "validation_status": "PASS",
    "validation_version": "canonical-nat-tmp-trajectory-panel-validation-v1",
    "source_directory": str(INPUT_DIR),
    "output_panel": str(PANEL_PATH),
    "output_panel_sha256": panel_sha256,
    "stock_flow_panel": str(STOCK_FLOW_PANEL_PATH),
    "stock_flow_panel_sha256": stock_flow_panel_sha256,
    "expected_intervals": [f"{t0}_{t1}" for t0, t1 in INTERVALS],
    "interval_count": len(INTERVALS),
    "rows_per_interval": EXPECTED_ROWS_PER_INTERVAL,
    "panel_rows": int(panel.shape[0]),
    "panel_columns": int(panel.shape[1]),
    "unique_cell_id": int(panel["cell_id"].nunique()),
    "duplicate_cell_interval_rows": int(
        panel.duplicated(subset=["cell_id", "t0", "t1"]).sum()
    ),
    "diagnostic_interval_rows": int(panel["diagnostic_interval"].sum()),
    "area_tolerance_ha": AREA_TOLERANCE_HA,
    "reconciliation_tolerance_ha": RECONCILIATION_TOLERANCE_HA,
    "maximum_absolute_residual_ha": float(
        max(item["maximum_absolute_residual_ha"] for item in interval_checks)
    ),
    "maximum_stock_flow_reconciliation_difference_ha": (
        maximum_reconciliation_difference
    ),
    "stock_flow_reconciliation_rows_over_tolerance": (
        reconciliation_rows_over_tolerance
    ),
    "incomplete_intermediate_support_area_ha": pooled_incomplete,
    "incomplete_intermediate_support_share_endpoint": safe_ratio(
        pooled_incomplete, pooled_endpoint
    ),
    "pooled_totals": {
        "nat_tmp_endpoint_ha": pooled_endpoint,
        "nat_tmp_pas_any_ha": pooled_any,
        "nat_tmp_pas_2plus_ha": pooled_2plus,
        "nat_tmp_pas_consecutive2_ha": pooled_consecutive2,
        "nat_tmp_pas_any_share_endpoint": safe_ratio(
            pooled_any, pooled_endpoint
        ),
        "nat_tmp_pas_2plus_share_endpoint": safe_ratio(
            pooled_2plus, pooled_endpoint
        ),
        "nat_tmp_pas_consecutive2_share_endpoint": safe_ratio(
            pooled_consecutive2, pooled_endpoint
        ),
        "nat_tmp_pas_consecutive2_share_any": safe_ratio(
            pooled_consecutive2, pooled_any
        ),
    },
    "interval_checks": interval_checks,
    "stock_flow_reconciliation_checks": reconciliation_checks,
}

with VALIDATION_PATH.open("w", encoding="utf-8") as output:
    json.dump(
        validation,
        output,
        indent=2,
        ensure_ascii=False,
        default=python_scalar,
    )


# ---------------------------------------------------------------------------
# Completion report
# ---------------------------------------------------------------------------

print("\nVALIDATION STATUS: PASS")
print("Intervals:", len(INTERVALS))
print("Rows:", f"{panel.shape[0]:,}")
print("Columns:", panel.shape[1])
print("Unique cell_id:", f"{panel['cell_id'].nunique():,}")
print(
    "Maximum accounting residual (ha):",
    f"{validation['maximum_absolute_residual_ha']:.12g}",
)
print(
    "Maximum stock-flow reconciliation difference (ha):",
    f"{maximum_reconciliation_difference:.12g}",
)
print(
    "Incomplete intermediate support (ha):",
    f"{pooled_incomplete:.6f}",
)
print("\nFiles created:")
print(PANEL_PATH)
print(MANIFEST_PATH)
print(VALIDATION_PATH)
print(SUMMARY_PATH)

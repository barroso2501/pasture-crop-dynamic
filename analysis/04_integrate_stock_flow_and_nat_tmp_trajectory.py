"""
04_integrate_stock_flow_and_nat_tmp_trajectory.py

Join the validated canonical stock-flow derived table to the validated
NAT-to-TMP within-interval trajectory panel.

Designed for Google Colab. Run the complete script in one cell or upload it
and execute with %run. Both canonical input Parquet files are read only and
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
# Google Drive and canonical paths
# ---------------------------------------------------------------------------

drive.mount("/content/drive")

PROJECT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade")
ANALYSIS_DIR = PROJECT_DIR / "analysis"
PANEL_DIR = PROJECT_DIR / "panel"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

STOCK_FLOW_DERIVED_PATH = (
    ANALYSIS_DIR
    / "canonical_stock_flow_derived_metrics_1985_2025_v1.parquet"
)
TRAJECTORY_PANEL_PATH = (
    PANEL_DIR
    / "canonical_nat_tmp_trajectory_panel_1985_2025_v1.parquet"
)

INTEGRATED_PANEL_PATH = (
    ANALYSIS_DIR
    / "canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet"
)
SUMMARY_PATH = (
    ANALYSIS_DIR
    / "canonical_integrated_stock_flow_trajectory_summary_v1.csv"
)
VALIDATION_PATH = (
    ANALYSIS_DIR
    / "canonical_integrated_stock_flow_trajectory_validation_v1.json"
)

EXPECTED_STOCK_FLOW_DERIVED_SHA256 = (
    "671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302"
)
EXPECTED_TRAJECTORY_PANEL_SHA256 = (
    "c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9"
)

EXPECTED_ROWS = 199_112
EXPECTED_CELLS = 24_889
EXPECTED_INTERVALS = 8
EXPECTED_STOCK_FLOW_COLUMNS = 122
EXPECTED_TRAJECTORY_COLUMNS = 28

KEY_COLUMNS = ["cell_id", "t0", "t1"]
ZERO_TOLERANCE_HA = 1e-9
IDENTITY_TOLERANCE_HA = 2e-6
INTEGRATED_VERSION = "canonical-integrated-stock-flow-trajectory-v1"

TRAJECTORY_METRIC_COLUMNS = [
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

TRAJECTORY_RESIDUAL_COLUMNS = [
    "residual_endpoint_observation_partition",
    "residual_pas_count_partition",
    "residual_pas_any_partition",
    "residual_pas_2plus_partition",
    "residual_pas_consecutive_partition",
]

TRAJECTORY_COLUMNS_TO_ADD = [
    "trajectory_output_version",
    "intermediate_years",
    *TRAJECTORY_METRIC_COLUMNS,
    *TRAJECTORY_RESIDUAL_COLUMNS,
]

DERIVED_TRAJECTORY_COLUMNS = [
    "nat_tmp_without_intermediate_pasture_ha",
    "nat_tmp_pas_one_year_only_ha",
    "nat_tmp_pas_2plus_nonconsecutive_ha",
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_2plus_share_endpoint",
    "nat_tmp_pas_consecutive2_share_endpoint",
    "nat_tmp_pas_consecutive2_share_any",
    "nat_tmp_mid_incomplete_share_endpoint",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def safe_divide(numerator, denominator, tolerance=ZERO_TOLERANCE_HA):
    result = pd.Series(np.nan, index=numerator.index, dtype="float64")
    valid = denominator > tolerance
    result.loc[valid] = numerator.loc[valid] / denominator.loc[valid]
    return result


def aggregate_ratio(numerator, denominator):
    if denominator <= ZERO_TOLERANCE_HA:
        return np.nan
    return numerator / denominator


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


# ---------------------------------------------------------------------------
# Load and protect canonical inputs
# ---------------------------------------------------------------------------

print("CANONICAL STOCK-FLOW AND NAT-TMP TRAJECTORY INTEGRATION - VERSION 1")
print("Stock-flow derived input:", STOCK_FLOW_DERIVED_PATH)
print("Trajectory input:", TRAJECTORY_PANEL_PATH)
print("Output directory:", ANALYSIS_DIR)

require(
    STOCK_FLOW_DERIVED_PATH.exists(),
    f"Stock-flow derived table not found: {STOCK_FLOW_DERIVED_PATH}",
)
require(
    TRAJECTORY_PANEL_PATH.exists(),
    f"Trajectory panel not found: {TRAJECTORY_PANEL_PATH}",
)

stock_flow_sha256 = sha256_file(STOCK_FLOW_DERIVED_PATH)
trajectory_sha256 = sha256_file(TRAJECTORY_PANEL_PATH)

require(
    stock_flow_sha256 == EXPECTED_STOCK_FLOW_DERIVED_SHA256,
    "The stock-flow derived input checksum differs from the validated version.\n"
    f"Expected: {EXPECTED_STOCK_FLOW_DERIVED_SHA256}\n"
    f"Found:    {stock_flow_sha256}",
)
require(
    trajectory_sha256 == EXPECTED_TRAJECTORY_PANEL_SHA256,
    "The trajectory input checksum differs from the validated version.\n"
    f"Expected: {EXPECTED_TRAJECTORY_PANEL_SHA256}\n"
    f"Found:    {trajectory_sha256}",
)

stock_flow = pd.read_parquet(STOCK_FLOW_DERIVED_PATH, engine="pyarrow")
trajectory = pd.read_parquet(TRAJECTORY_PANEL_PATH, engine="pyarrow")

require(
    stock_flow.shape == (EXPECTED_ROWS, EXPECTED_STOCK_FLOW_COLUMNS),
    f"Unexpected stock-flow derived shape: {stock_flow.shape}",
)
require(
    trajectory.shape == (EXPECTED_ROWS, EXPECTED_TRAJECTORY_COLUMNS),
    f"Unexpected trajectory panel shape: {trajectory.shape}",
)

for name, frame in [
    ("stock-flow derived", stock_flow),
    ("trajectory", trajectory),
]:
    require(
        frame["cell_id"].nunique() == EXPECTED_CELLS,
        f"Unexpected cell count in {name} input",
    )
    require(
        frame["interval"].nunique() == EXPECTED_INTERVALS,
        f"Unexpected interval count in {name} input",
    )
    require(
        frame.duplicated(subset=KEY_COLUMNS).sum() == 0,
        f"Duplicate join keys found in {name} input",
    )

# Canonical sorting makes row-wise preservation and shared-field comparison
# explicit and reproducible.
stock_flow = stock_flow.sort_values(KEY_COLUMNS, kind="stable").reset_index(drop=True)
trajectory = trajectory.sort_values(KEY_COLUMNS, kind="stable").reset_index(drop=True)

require(
    stock_flow[KEY_COLUMNS].equals(trajectory[KEY_COLUMNS]),
    "The two canonical panels do not have identical ordered join keys",
)

stock_flow_original_columns = stock_flow.columns.tolist()
trajectory_original_columns = trajectory.columns.tolist()


# ---------------------------------------------------------------------------
# Validate shared metadata and spatial support before joining
# ---------------------------------------------------------------------------

EXACT_SHARED_COLUMNS = [
    "GRID_ID",
    "source_batch_id",
    "interval",
    "diagnostic_interval",
]

exact_shared_mismatches = {}
for column in EXACT_SHARED_COLUMNS:
    mismatches = int((stock_flow[column] != trajectory[column]).sum())
    exact_shared_mismatches[column] = mismatches
    require(mismatches == 0, f"Shared field differs: {column}")

NUMERIC_SHARED_COLUMNS = ["geometry_area_ha", "raster_area_ha"]
numeric_shared_maximum_differences = {}
for column in NUMERIC_SHARED_COLUMNS:
    maximum_difference = float(
        (stock_flow[column] - trajectory[column]).abs().max()
    )
    numeric_shared_maximum_differences[column] = maximum_difference
    require(
        maximum_difference <= IDENTITY_TOLERANCE_HA,
        f"Shared numeric field differs beyond tolerance: {column}",
    )

endpoint_difference_flow = (
    trajectory["nat_tmp_endpoint_ha"] - stock_flow["flow_nat_tmp"]
).abs()
endpoint_difference_derived = (
    trajectory["nat_tmp_endpoint_ha"]
    - stock_flow["nat_to_tmp_endpoint_flow_ha"]
).abs()

maximum_endpoint_difference_flow = float(endpoint_difference_flow.max())
maximum_endpoint_difference_derived = float(endpoint_difference_derived.max())

require(
    maximum_endpoint_difference_flow <= IDENTITY_TOLERANCE_HA,
    "Trajectory endpoint does not reconcile with flow_nat_tmp",
)
require(
    maximum_endpoint_difference_derived <= IDENTITY_TOLERANCE_HA,
    "Trajectory endpoint does not reconcile with the derived endpoint field",
)


# ---------------------------------------------------------------------------
# One-to-one integration
# ---------------------------------------------------------------------------

trajectory_for_join = trajectory[
    KEY_COLUMNS
    + ["output_version", "intermediate_years"]
    + TRAJECTORY_METRIC_COLUMNS
    + TRAJECTORY_RESIDUAL_COLUMNS
].rename(columns={"output_version": "trajectory_output_version"})

integrated = stock_flow.merge(
    trajectory_for_join,
    on=KEY_COLUMNS,
    how="left",
    validate="one_to_one",
    sort=False,
)

require(
    integrated.shape[0] == EXPECTED_ROWS,
    "Integration changed the number of rows",
)
require(
    integrated.duplicated(subset=KEY_COLUMNS).sum() == 0,
    "Integrated table contains duplicate cell-interval rows",
)
require(
    int(integrated[TRAJECTORY_COLUMNS_TO_ADD].isna().sum().sum()) == 0,
    "At least one stock-flow row lacks a matched trajectory record",
)
require(
    integrated[stock_flow_original_columns].equals(stock_flow),
    "At least one stock-flow input column changed during integration",
)

trajectory_joined_check = integrated[
    KEY_COLUMNS + TRAJECTORY_COLUMNS_TO_ADD
]
require(
    trajectory_joined_check.equals(trajectory_for_join),
    "At least one trajectory input field changed during integration",
)


# ---------------------------------------------------------------------------
# Complementary cell-level trajectory metrics
# ---------------------------------------------------------------------------

integrated["nat_tmp_without_intermediate_pasture_ha"] = integrated[
    "nat_tmp_pas_years_0_ha"
]
integrated["nat_tmp_pas_one_year_only_ha"] = integrated[
    "nat_tmp_pas_years_1_ha"
]
integrated["nat_tmp_pas_2plus_nonconsecutive_ha"] = (
    integrated["nat_tmp_pas_2plus_ha"]
    - integrated["nat_tmp_pas_consecutive2_ha"]
)

integrated["nat_tmp_pas_any_share_endpoint"] = safe_divide(
    integrated["nat_tmp_pas_any_ha"],
    integrated["nat_tmp_endpoint_ha"],
)
integrated["nat_tmp_pas_2plus_share_endpoint"] = safe_divide(
    integrated["nat_tmp_pas_2plus_ha"],
    integrated["nat_tmp_endpoint_ha"],
)
integrated["nat_tmp_pas_consecutive2_share_endpoint"] = safe_divide(
    integrated["nat_tmp_pas_consecutive2_ha"],
    integrated["nat_tmp_endpoint_ha"],
)
integrated["nat_tmp_pas_consecutive2_share_any"] = safe_divide(
    integrated["nat_tmp_pas_consecutive2_ha"],
    integrated["nat_tmp_pas_any_ha"],
)
integrated["nat_tmp_mid_incomplete_share_endpoint"] = safe_divide(
    integrated["nat_tmp_mid_incomplete_ha"],
    integrated["nat_tmp_endpoint_ha"],
)

integrated["integrated_output_version"] = INTEGRATED_VERSION


# ---------------------------------------------------------------------------
# Validate derived trajectory metrics
# ---------------------------------------------------------------------------

require(
    float((
        integrated["nat_tmp_without_intermediate_pasture_ha"]
        - integrated["nat_tmp_pas_years_0_ha"]
    ).abs().max()) <= ZERO_TOLERANCE_HA,
    "No-pasture area alias failed",
)
require(
    float((
        integrated["nat_tmp_pas_one_year_only_ha"]
        - integrated["nat_tmp_pas_years_1_ha"]
    ).abs().max()) <= ZERO_TOLERANCE_HA,
    "One-year pasture area alias failed",
)

nonconsecutive_minimum = float(
    integrated["nat_tmp_pas_2plus_nonconsecutive_ha"].min()
)
require(
    nonconsecutive_minimum >= -ZERO_TOLERANCE_HA,
    "Derived multi-year nonconsecutive area is negative",
)

numeric_derived = integrated[DERIVED_TRAJECTORY_COLUMNS].to_numpy(
    dtype="float64"
)
infinite_derived_values = int(np.isinf(numeric_derived).sum())
require(infinite_derived_values == 0, "Infinite derived values found")

SHARE_COLUMNS = [
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_2plus_share_endpoint",
    "nat_tmp_pas_consecutive2_share_endpoint",
    "nat_tmp_pas_consecutive2_share_any",
    "nat_tmp_mid_incomplete_share_endpoint",
]

share_array = integrated[SHARE_COLUMNS].to_numpy(dtype="float64")
share_values = share_array[~np.isnan(share_array)]
share_values_outside_zero_one = int((
    (share_values < -1e-12) | (share_values > 1 + 1e-12)
).sum())
require(
    share_values_outside_zero_one == 0,
    "At least one derived trajectory share is outside [0, 1]",
)

zero_endpoint = integrated["nat_tmp_endpoint_ha"] <= ZERO_TOLERANCE_HA
endpoint_share_columns = [
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_2plus_share_endpoint",
    "nat_tmp_pas_consecutive2_share_endpoint",
    "nat_tmp_mid_incomplete_share_endpoint",
]
require(
    integrated.loc[zero_endpoint, endpoint_share_columns].isna().all().all(),
    "Endpoint shares must be undefined when NAT->TMP endpoint area is zero",
)
require(
    integrated.loc[~zero_endpoint, endpoint_share_columns]
    .notna()
    .all()
    .all(),
    "Positive NAT->TMP endpoint rows must have defined endpoint shares",
)

zero_any = integrated["nat_tmp_pas_any_ha"] <= ZERO_TOLERANCE_HA
require(
    integrated.loc[
        zero_any, "nat_tmp_pas_consecutive2_share_any"
    ].isna().all(),
    "Persistence share must be undefined when inclusive pasture area is zero",
)
require(
    integrated.loc[
        ~zero_any, "nat_tmp_pas_consecutive2_share_any"
    ].notna().all(),
    "Positive inclusive pasture rows must have a persistence share",
)


# ---------------------------------------------------------------------------
# Integrated interval summary
# ---------------------------------------------------------------------------

summary_rows = []

for (t0, t1), group in integrated.groupby(["t0", "t1"], sort=True):
    endpoint = float(group["nat_tmp_endpoint_ha"].sum())
    pasture_any = float(group["nat_tmp_pas_any_ha"].sum())
    pasture_2plus = float(group["nat_tmp_pas_2plus_ha"].sum())
    pasture_consecutive2 = float(
        group["nat_tmp_pas_consecutive2_ha"].sum()
    )
    incomplete = float(group["nat_tmp_mid_incomplete_ha"].sum())
    consolidation = float(group["consolidation_ha"].sum())
    replenishment = float(group["replenishment_ha"].sum())
    gross_cr = consolidation + replenishment

    summary_rows.append({
        "interval": f"{int(t0)}_{int(t1)}",
        "t0": int(t0),
        "t1": int(t1),
        "diagnostic_interval": int(group["diagnostic_interval"].iloc[0]),
        "cells": int(len(group)),
        "consolidation_ha": consolidation,
        "replenishment_ha": replenishment,
        "gross_cr_activity_ha": gross_cr,
        "net_cr_balance_ha": consolidation - replenishment,
        "aggregate_cr_balance_index": aggregate_ratio(
            consolidation - replenishment, gross_cr
        ),
        "nat_tmp_endpoint_ha": endpoint,
        "nat_tmp_without_intermediate_pasture_ha": float(
            group["nat_tmp_without_intermediate_pasture_ha"].sum()
        ),
        "nat_tmp_pas_one_year_only_ha": float(
            group["nat_tmp_pas_one_year_only_ha"].sum()
        ),
        "nat_tmp_pas_any_ha": pasture_any,
        "nat_tmp_pas_2plus_ha": pasture_2plus,
        "nat_tmp_pas_consecutive2_ha": pasture_consecutive2,
        "nat_tmp_pas_2plus_nonconsecutive_ha": float(
            group["nat_tmp_pas_2plus_nonconsecutive_ha"].sum()
        ),
        "nat_tmp_mid_incomplete_ha": incomplete,
        "nat_tmp_pas_any_share_endpoint": aggregate_ratio(
            pasture_any, endpoint
        ),
        "nat_tmp_pas_2plus_share_endpoint": aggregate_ratio(
            pasture_2plus, endpoint
        ),
        "nat_tmp_pas_consecutive2_share_endpoint": aggregate_ratio(
            pasture_consecutive2, endpoint
        ),
        "nat_tmp_pas_consecutive2_share_any": aggregate_ratio(
            pasture_consecutive2, pasture_any
        ),
        "nat_tmp_mid_incomplete_share_endpoint": aggregate_ratio(
            incomplete, endpoint
        ),
        "cells_with_nat_tmp_endpoint": int((
            group["nat_tmp_endpoint_ha"] > ZERO_TOLERANCE_HA
        ).sum()),
        "cells_with_nat_tmp_pas_any": int((
            group["nat_tmp_pas_any_ha"] > ZERO_TOLERANCE_HA
        ).sum()),
        "cells_with_nat_tmp_pas_consecutive2": int((
            group["nat_tmp_pas_consecutive2_ha"] > ZERO_TOLERANCE_HA
        ).sum()),
    })

summary = pd.DataFrame(summary_rows)
require(
    len(summary) == EXPECTED_INTERVALS,
    "Integrated summary does not contain eight intervals",
)


# ---------------------------------------------------------------------------
# Save outputs and validation record
# ---------------------------------------------------------------------------

integrated.to_parquet(
    INTEGRATED_PANEL_PATH,
    index=False,
    engine="pyarrow",
    compression="snappy",
)
summary.to_csv(SUMMARY_PATH, index=False)

integrated_sha256 = sha256_file(INTEGRATED_PANEL_PATH)
summary_sha256 = sha256_file(SUMMARY_PATH)

expected_output_columns = (
    EXPECTED_STOCK_FLOW_COLUMNS
    + len(TRAJECTORY_COLUMNS_TO_ADD)
    + len(DERIVED_TRAJECTORY_COLUMNS)
    + 1  # integrated_output_version
)
require(
    integrated.shape == (EXPECTED_ROWS, expected_output_columns),
    f"Unexpected integrated output shape: {integrated.shape}",
)

nullable_integrated_counts = {
    column: int(integrated[column].isna().sum())
    for column in DERIVED_TRAJECTORY_COLUMNS
    if int(integrated[column].isna().sum()) > 0
}

validation = {
    "validation_status": "PASS",
    "validation_version": (
        "canonical-integrated-stock-flow-trajectory-validation-v1"
    ),
    "stock_flow_derived_input": str(STOCK_FLOW_DERIVED_PATH),
    "stock_flow_derived_input_sha256": stock_flow_sha256,
    "trajectory_input": str(TRAJECTORY_PANEL_PATH),
    "trajectory_input_sha256": trajectory_sha256,
    "integrated_panel": str(INTEGRATED_PANEL_PATH),
    "integrated_panel_sha256": integrated_sha256,
    "summary_file": str(SUMMARY_PATH),
    "summary_file_sha256": summary_sha256,
    "integrated_output_version": INTEGRATED_VERSION,
    "rows": int(integrated.shape[0]),
    "columns": int(integrated.shape[1]),
    "unique_cell_id": int(integrated["cell_id"].nunique()),
    "interval_count": int(integrated["interval"].nunique()),
    "duplicate_cell_interval_rows": int(
        integrated.duplicated(subset=KEY_COLUMNS).sum()
    ),
    "stock_flow_columns_preserved": bool(
        integrated[stock_flow_original_columns].equals(stock_flow)
    ),
    "trajectory_columns_preserved": bool(
        trajectory_joined_check.equals(trajectory_for_join)
    ),
    "stock_flow_input_columns": len(stock_flow_original_columns),
    "trajectory_input_columns": len(trajectory_original_columns),
    "trajectory_columns_added": len(TRAJECTORY_COLUMNS_TO_ADD),
    "derived_trajectory_columns_added": len(DERIVED_TRAJECTORY_COLUMNS),
    "derived_trajectory_column_names": DERIVED_TRAJECTORY_COLUMNS,
    "exact_shared_field_mismatches": exact_shared_mismatches,
    "numeric_shared_maximum_differences_ha": (
        numeric_shared_maximum_differences
    ),
    "maximum_endpoint_flow_nat_tmp_difference_ha": (
        maximum_endpoint_difference_flow
    ),
    "maximum_endpoint_derived_field_difference_ha": (
        maximum_endpoint_difference_derived
    ),
    "endpoint_reconciliation_rows_over_2e_6_ha": int((
        endpoint_difference_flow > IDENTITY_TOLERANCE_HA
    ).sum()),
    "infinite_derived_values": infinite_derived_values,
    "share_values_outside_zero_one": share_values_outside_zero_one,
    "minimum_2plus_nonconsecutive_area_ha": nonconsecutive_minimum,
    "nullable_derived_value_counts": nullable_integrated_counts,
    "zero_tolerance_ha": ZERO_TOLERANCE_HA,
    "identity_tolerance_ha": IDENTITY_TOLERANCE_HA,
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
print("Rows:", f"{integrated.shape[0]:,}")
print("Columns:", integrated.shape[1])
print("Unique cell_id:", f"{integrated['cell_id'].nunique():,}")
print("Intervals:", integrated["interval"].nunique())
print("Stock-flow columns preserved:", len(stock_flow_original_columns))
print("Trajectory columns added:", len(TRAJECTORY_COLUMNS_TO_ADD))
print("Derived trajectory columns added:", len(DERIVED_TRAJECTORY_COLUMNS))
print(
    "Maximum NAT-TMP endpoint reconciliation difference (ha):",
    f"{maximum_endpoint_difference_flow:.12g}",
)
print("Infinite derived values:", infinite_derived_values)
print("Share values outside [0, 1]:", share_values_outside_zero_one)
print("\nFiles created:")
print(INTEGRATED_PANEL_PATH)
print(SUMMARY_PATH)
print(VALIDATION_PATH)

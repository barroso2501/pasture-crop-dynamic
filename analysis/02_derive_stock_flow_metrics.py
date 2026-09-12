"""
02_derive_stock_flow_metrics.py

Create and validate the derived analytical table for the canonical five-year
stock-and-flow panel.

Designed for Google Colab. Run the complete script in one cell or upload it
and execute with %run. The canonical Parquet input is read only and is never
modified.
"""

from google.colab import drive
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import numpy as np
import pandas as pd


# Parquet support is normally available in Colab. Install it only when the
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
INPUT_PATH = (
    PROJECT_DIR
    / "panel"
    / "canonical_stock_flow_panel_1985_2025_v1.parquet"
)
OUTPUT_DIR = PROJECT_DIR / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DERIVED_PATH = (
    OUTPUT_DIR
    / "canonical_stock_flow_derived_metrics_1985_2025_v1.parquet"
)
SUMMARY_PATH = (
    OUTPUT_DIR
    / "canonical_stock_flow_derived_metrics_summary_v1.csv"
)
VALIDATION_PATH = (
    OUTPUT_DIR
    / "canonical_stock_flow_derived_metrics_validation_v1.json"
)

EXPECTED_INPUT_SHA256 = (
    "2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64"
)
EXPECTED_ROWS = 199_112
EXPECTED_INPUT_COLUMNS = 90
EXPECTED_CELL_COUNT = 24_889
EXPECTED_INTERVAL_COUNT = 8

ZERO_TOLERANCE_HA = 1e-9
IDENTITY_TOLERANCE_HA = 2e-6
LOW_SUPPORT_THRESHOLD = 0.99

AGE_COMPONENTS = {
    "censored": "pas_tmp_censored",
    "new": "pas_tmp_new",
    "unresolved_age": "pas_tmp_unresolved_age",
    "unattributed_age": "pas_tmp_unattributed_age",
}


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
    """Divide only where the denominator is meaningfully positive."""
    result = pd.Series(np.nan, index=numerator.index, dtype="float64")
    valid = denominator > tolerance
    result.loc[valid] = numerator.loc[valid] / denominator.loc[valid]
    return result


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


# ---------------------------------------------------------------------------
# Load and protect the canonical input
# ---------------------------------------------------------------------------

print("CANONICAL DERIVED STOCK-FLOW METRICS - VERSION 1")
print("Input:", INPUT_PATH)
print("Output directory:", OUTPUT_DIR)

require(INPUT_PATH.exists(), f"Canonical panel not found: {INPUT_PATH}")

input_sha256 = sha256_file(INPUT_PATH)
require(
    input_sha256 == EXPECTED_INPUT_SHA256,
    "The input Parquet checksum differs from the validated canonical panel.\n"
    f"Expected: {EXPECTED_INPUT_SHA256}\n"
    f"Found:    {input_sha256}",
)

panel = pd.read_parquet(INPUT_PATH, engine="pyarrow")
original_columns = panel.columns.tolist()

require(panel.shape == (EXPECTED_ROWS, EXPECTED_INPUT_COLUMNS),
        f"Unexpected canonical panel shape: {panel.shape}")
require(panel["cell_id"].nunique() == EXPECTED_CELL_COUNT,
        "Unexpected number of distinct cell_id values")
require(panel["interval"].nunique() == EXPECTED_INTERVAL_COUNT,
        "Unexpected number of intervals")
require(panel.duplicated(subset=["cell_id", "t0", "t1"]).sum() == 0,
        "Duplicate cell-interval rows found")
require(panel.groupby("cell_id")["interval"].nunique().eq(8).all(),
        "At least one cell does not contain all eight intervals")

expected_diagnostic = (
    (panel["t0"] == 2020) & (panel["t1"] == 2025)
).astype("int8")
require(
    np.array_equal(
        panel["diagnostic_interval"].astype("int8").to_numpy(),
        expected_diagnostic.to_numpy(),
    ),
    "diagnostic_interval is inconsistent with the 2020-2025 interval",
)


# ---------------------------------------------------------------------------
# Derived metrics
# ---------------------------------------------------------------------------

derived = panel.copy()

# Analysis-period flag. The diagnostic interval remains in the table.
derived["primary_inference_interval"] = (
    1 - derived["diagnostic_interval"].astype("int8")
).astype("int8")

# Spatial support. These fields are descriptive and do not filter cells.
derived["raster_fraction_geometry"] = safe_divide(
    derived["raster_area_ha"], derived["geometry_area_ha"]
)
derived["valid0_fraction_geometry"] = safe_divide(
    derived["valid0_area_ha"], derived["geometry_area_ha"]
)
derived["valid1_fraction_geometry"] = safe_divide(
    derived["valid1_area_ha"], derived["geometry_area_ha"]
)
derived["minimum_valid_fraction_geometry"] = derived[
    ["valid0_fraction_geometry", "valid1_fraction_geometry"]
].min(axis=1)
derived["valid_support_below_99pct"] = (
    derived["minimum_valid_fraction_geometry"] < LOW_SUPPORT_THRESHOLD
).astype("int8")

# Focal stocks as fractions of valid endpoint area.
for endpoint in (0, 1):
    valid_area = derived[f"valid{endpoint}_area_ha"]
    for state in ("nat", "pas", "tmp"):
        derived[f"stock{endpoint}_{state}_fraction_valid"] = safe_divide(
            derived[f"stock{endpoint}_{state}"], valid_area
        )

# Net stock changes. These remain distinct from gross directed flows.
for state in ("nat", "pas", "tmp"):
    derived[f"delta_stock_{state}_ha"] = (
        derived[f"stock1_{state}"] - derived[f"stock0_{state}"]
    )

# Core consolidation-replenishment accounting.
derived["consolidation_ha"] = derived["flow_pas_tmp"]
derived["replenishment_ha"] = derived["flow_nat_pas"]
derived["nat_to_tmp_endpoint_flow_ha"] = derived["flow_nat_tmp"]
derived["gross_cr_activity_ha"] = (
    derived["consolidation_ha"] + derived["replenishment_ha"]
)
derived["net_cr_balance_ha"] = (
    derived["consolidation_ha"] - derived["replenishment_ha"]
)
derived["cr_balance_index"] = safe_divide(
    derived["net_cr_balance_ha"], derived["gross_cr_activity_ha"]
)

# Source-stock conversion rates.
derived["consolidation_rate_initial_pasture"] = safe_divide(
    derived["consolidation_ha"], derived["stock0_pas"]
)
derived["replenishment_rate_initial_native"] = safe_divide(
    derived["replenishment_ha"], derived["stock0_nat"]
)

# PAS->TMP origin shares. They are undefined, not zero, when PAS->TMP is zero.
for short_name, source_column in AGE_COMPONENTS.items():
    derived[f"pas_tmp_{short_name}_share"] = safe_divide(
        derived[source_column], derived["consolidation_ha"]
    )

# Explicit analytical-population flags.
derived["has_consolidation"] = (
    derived["consolidation_ha"] > ZERO_TOLERANCE_HA
).astype("int8")
derived["has_replenishment"] = (
    derived["replenishment_ha"] > ZERO_TOLERANCE_HA
).astype("int8")
derived["has_cr_activity"] = (
    (derived["has_consolidation"] == 1)
    | (derived["has_replenishment"] == 1)
).astype("int8")
derived["has_both_cr_processes"] = (
    (derived["has_consolidation"] == 1)
    & (derived["has_replenishment"] == 1)
).astype("int8")

conditions = [
    (derived["has_consolidation"] == 0)
    & (derived["has_replenishment"] == 0),
    (derived["has_consolidation"] == 1)
    & (derived["has_replenishment"] == 0),
    (derived["has_consolidation"] == 0)
    & (derived["has_replenishment"] == 1),
    (derived["has_consolidation"] == 1)
    & (derived["has_replenishment"] == 1),
]

derived["cr_activity_class"] = np.select(
    conditions,
    ["none", "consolidation_only", "replenishment_only", "both"],
    default="invalid",
)

derived_columns = [
    column for column in derived.columns if column not in original_columns
]


# ---------------------------------------------------------------------------
# Validation of derived fields
# ---------------------------------------------------------------------------

require(derived.shape[0] == EXPECTED_ROWS,
        "Derived table changed the number of rows")
require(derived[original_columns].equals(panel[original_columns]),
        "At least one canonical input column was changed")
require(derived.duplicated(subset=["cell_id", "t0", "t1"]).sum() == 0,
        "Derived table contains duplicate cell-interval rows")
require(not derived["cr_activity_class"].eq("invalid").any(),
        "Invalid consolidation-replenishment activity class")

numeric_derived_columns = derived[derived_columns].select_dtypes(
    include=[np.number]
).columns
infinite_values = int(
    np.isinf(derived[numeric_derived_columns].to_numpy(dtype="float64")).sum()
)
require(infinite_values == 0, "Infinite values found in derived metrics")

active = derived["has_cr_activity"] == 1
inactive = ~active
balance_outside_range = int(
    (
        (derived.loc[active, "cr_balance_index"] < -1 - 1e-12)
        | (derived.loc[active, "cr_balance_index"] > 1 + 1e-12)
    ).sum()
)
require(balance_outside_range == 0,
        "cr_balance_index contains values outside [-1, 1]")
require(derived.loc[inactive, "cr_balance_index"].isna().all(),
        "Inactive rows must have undefined cr_balance_index")
require(derived.loc[active, "cr_balance_index"].notna().all(),
        "Active rows must have a defined cr_balance_index")

positive_consolidation = derived["has_consolidation"] == 1
zero_consolidation = ~positive_consolidation
share_columns = [f"pas_tmp_{name}_share" for name in AGE_COMPONENTS]
share_sum = derived[share_columns].sum(axis=1, min_count=1)
share_closure_max_difference = float(
    (share_sum.loc[positive_consolidation] - 1).abs().max()
)
share_closure_violations = int(
    (
        (share_sum.loc[positive_consolidation] - 1).abs()
        > IDENTITY_TOLERANCE_HA
    ).sum()
)
require(share_closure_violations == 0,
        "PAS->TMP derived origin shares do not sum to one")
require(derived.loc[zero_consolidation, share_columns].isna().all().all(),
        "PAS->TMP shares must be undefined when consolidation is zero")

balance_identity_difference = (
    derived["net_cr_balance_ha"]
    - (derived["consolidation_ha"] - derived["replenishment_ha"])
).abs()
require(float(balance_identity_difference.max()) <= ZERO_TOLERANCE_HA,
        "Net consolidation-replenishment balance identity failed")

for state in ("nat", "pas", "tmp"):
    difference = (
        derived[f"delta_stock_{state}_ha"]
        - (derived[f"stock1_{state}"] - derived[f"stock0_{state}"])
    ).abs()
    require(float(difference.max()) <= ZERO_TOLERANCE_HA,
            f"Net stock identity failed for {state}")


# ---------------------------------------------------------------------------
# Interval summary
# ---------------------------------------------------------------------------

summary_rows = []

for (t0, t1), group in derived.groupby(["t0", "t1"], sort=True):
    consolidation_total = float(group["consolidation_ha"].sum())
    replenishment_total = float(group["replenishment_ha"].sum())
    gross_total = consolidation_total + replenishment_total
    aggregate_balance = (
        (consolidation_total - replenishment_total) / gross_total
        if gross_total > ZERO_TOLERANCE_HA
        else np.nan
    )

    row = {
        "interval": f"{int(t0)}_{int(t1)}",
        "t0": int(t0),
        "t1": int(t1),
        "diagnostic_interval": int(group["diagnostic_interval"].iloc[0]),
        "cells": int(len(group)),
        "cells_with_consolidation": int(group["has_consolidation"].sum()),
        "cells_with_replenishment": int(group["has_replenishment"].sum()),
        "cells_with_cr_activity": int(group["has_cr_activity"].sum()),
        "cells_with_both_processes": int(group["has_both_cr_processes"].sum()),
        "cells_below_99pct_valid_support": int(
            group["valid_support_below_99pct"].sum()
        ),
        "consolidation_ha": consolidation_total,
        "replenishment_ha": replenishment_total,
        "nat_to_tmp_endpoint_flow_ha": float(
            group["nat_to_tmp_endpoint_flow_ha"].sum()
        ),
        "gross_cr_activity_ha": gross_total,
        "net_cr_balance_ha": consolidation_total - replenishment_total,
        "aggregate_cr_balance_index": aggregate_balance,
        "median_active_cell_cr_balance_index": float(
            group.loc[group["has_cr_activity"] == 1, "cr_balance_index"].median()
        ),
        "aggregate_consolidation_rate_initial_pasture": (
            consolidation_total / float(group["stock0_pas"].sum())
            if float(group["stock0_pas"].sum()) > ZERO_TOLERANCE_HA
            else np.nan
        ),
        "aggregate_replenishment_rate_initial_native": (
            replenishment_total / float(group["stock0_nat"].sum())
            if float(group["stock0_nat"].sum()) > ZERO_TOLERANCE_HA
            else np.nan
        ),
    }

    for short_name, source_column in AGE_COMPONENTS.items():
        component_total = float(group[source_column].sum())
        row[f"pas_tmp_{short_name}_ha"] = component_total
        row[f"pas_tmp_{short_name}_share"] = (
            component_total / consolidation_total
            if consolidation_total > ZERO_TOLERANCE_HA
            else np.nan
        )

    summary_rows.append(row)

summary = pd.DataFrame(summary_rows)
require(len(summary) == EXPECTED_INTERVAL_COUNT,
        "Interval summary does not contain eight rows")


# ---------------------------------------------------------------------------
# Save outputs and validation record
# ---------------------------------------------------------------------------

derived.to_parquet(
    DERIVED_PATH,
    index=False,
    engine="pyarrow",
    compression="snappy",
)
summary.to_csv(SUMMARY_PATH, index=False)

derived_sha256 = sha256_file(DERIVED_PATH)
summary_sha256 = sha256_file(SUMMARY_PATH)

nullable_derived_counts = {
    column: int(derived[column].isna().sum())
    for column in derived_columns
    if int(derived[column].isna().sum()) > 0
}

validation = {
    "validation_status": "PASS",
    "validation_version": "canonical-derived-stock-flow-validation-v1",
    "input_panel": str(INPUT_PATH),
    "input_panel_sha256": input_sha256,
    "derived_panel": str(DERIVED_PATH),
    "derived_panel_sha256": derived_sha256,
    "summary_file": str(SUMMARY_PATH),
    "summary_file_sha256": summary_sha256,
    "rows": int(derived.shape[0]),
    "input_columns": len(original_columns),
    "derived_columns_added": len(derived_columns),
    "output_columns": int(derived.shape[1]),
    "unique_cell_id": int(derived["cell_id"].nunique()),
    "interval_count": int(derived["interval"].nunique()),
    "duplicate_cell_interval_rows": int(
        derived.duplicated(subset=["cell_id", "t0", "t1"]).sum()
    ),
    "canonical_columns_unchanged": bool(
        derived[original_columns].equals(panel[original_columns])
    ),
    "infinite_derived_values": infinite_values,
    "balance_values_outside_minus1_plus1": balance_outside_range,
    "share_closure_violations": share_closure_violations,
    "maximum_share_closure_difference": share_closure_max_difference,
    "zero_tolerance_ha": ZERO_TOLERANCE_HA,
    "identity_tolerance_ha": IDENTITY_TOLERANCE_HA,
    "low_support_threshold": LOW_SUPPORT_THRESHOLD,
    "derived_column_names": derived_columns,
    "nullable_derived_value_counts": nullable_derived_counts,
    "activity_class_counts": {
        str(key): int(value)
        for key, value in derived["cr_activity_class"].value_counts().items()
    },
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
print("Rows:", f"{derived.shape[0]:,}")
print("Original columns preserved:", len(original_columns))
print("Derived columns added:", len(derived_columns))
print("Output columns:", derived.shape[1])
print("Unique cell_id:", f"{derived['cell_id'].nunique():,}")
print("Intervals:", derived["interval"].nunique())
print("Infinite derived values:", infinite_values)
print("Share closure violations:", share_closure_violations)
print("Balance values outside [-1, 1]:", balance_outside_range)
print("\nFiles created:")
print(DERIVED_PATH)
print(SUMMARY_PATH)
print(VALIDATION_PATH)


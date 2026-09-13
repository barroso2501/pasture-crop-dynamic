"""
Phase 0 validation of Earth Engine runtime configuration and the explicit
native-transform 2005-2010 b00 stock-flow replication.

Designed for Google Colab. Place the three input CSV files in
MyDrive/Trabalho/Contabilidade/csv before running this script.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from google.colab import drive
except ImportError:  # Allows the same validation to be tested outside Colab.
    drive = None


# -----------------------------------------------------------------------------
# 1. Canonical configuration
# -----------------------------------------------------------------------------

if drive is not None:
    drive.mount("/content/drive")

PROJECT_DIR = Path(
    os.environ.get(
        "CANONICAL_PHASE0_PROJECT_DIR",
        "/content/drive/MyDrive/Trabalho/Contabilidade",
    )
)
INPUT_DIR = PROJECT_DIR / "csv"
OUTPUT_DIR = PROJECT_DIR / "analysis" / "provenance"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AUDIT_PATH = INPUT_DIR / "canonical_runtime_configuration_audit_v1.csv"
REFERENCE_PATH = INPUT_DIR / "canonical_stock_flow_2005_2010_b00_v1.csv"
VERIFICATION_PATH = (
    INPUT_DIR
    / "canonical_stock_flow_2005_2010_b00_native_transform_verification_v1.csv"
)

COLUMN_COMPARISON_PATH = (
    OUTPUT_DIR / "canonical_phase0_b00_column_comparison_v1.csv"
)
CELL_COMPARISON_PATH = (
    OUTPUT_DIR / "canonical_phase0_b00_cell_comparison_v1.csv"
)
VALIDATION_PATH = (
    OUTPUT_DIR / "canonical_phase0_provenance_validation_v1.json"
)

OUTPUT_VERSION = "canonical-phase0-provenance-validation-v1"
EXPECTED_REFERENCE_SHA256 = (
    "bad0505b70a8ed1c408edc8290d5e9c5dfca22913edd8d0447db1c12112b1636"
)
EXPECTED_ROWS = 3_168
EXPECTED_COLUMNS = 90
AREA_TOLERANCE_HA = 2e-6

KEY_COLUMN = "cell_id"
EXACT_METADATA_COLUMNS = [
    "GRID_ID",
    "source_batch_id",
    "t0",
    "t1",
    "interval",
    "output_version",
    "diagnostic_interval",
]

AUDIT_PASS_COLUMNS = [
    "coverage_asset_match",
    "pasture_age_asset_match",
    "analytical_grid_match",
    "expected_cell_count_match",
    "grid_count_pass",
    "distinct_cell_id_pass",
    "runtime_crs_match",
    "coverage_native_crs_match",
    "pasture_age_native_crs_match",
    "repository_runtime_transform_match",
    "runtime_coverage_native_transform_match",
    "coverage_age_pixel_scale_match",
    "coverage_age_integer_x_offset",
    "coverage_age_integer_y_offset",
    "coverage_age_same_lattice",
    "output_version_match",
    "coverage_band_count_pass",
    "pasture_age_band_count_pass",
    "static_configuration_pass",
    "complete_runtime_configuration_pass",
]


# -----------------------------------------------------------------------------
# 2. Helpers
# -----------------------------------------------------------------------------

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def truthy(value) -> bool:
    if pd.isna(value):
        return False
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value) == 1.0
    return str(value).strip().lower() in {"1", "true", "yes"}


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


# -----------------------------------------------------------------------------
# 3. Input inventory and runtime-configuration audit
# -----------------------------------------------------------------------------

print("PHASE 0 PROVENANCE VALIDATION - VERSION 1")
print("Input directory:", INPUT_DIR)
print("Output directory:", OUTPUT_DIR)

for path in [AUDIT_PATH, REFERENCE_PATH, VERIFICATION_PATH]:
    require(path.exists(), f"Required input file not found: {path}")

input_hashes = {
    "runtime_configuration_audit": sha256_file(AUDIT_PATH),
    "accepted_b00_reference": sha256_file(REFERENCE_PATH),
    "explicit_native_transform_b00": sha256_file(VERIFICATION_PATH),
}

require(
    input_hashes["accepted_b00_reference"] == EXPECTED_REFERENCE_SHA256,
    "The accepted b00 reference CSV does not match its pinned SHA-256. "
    f"Expected {EXPECTED_REFERENCE_SHA256}, found "
    f"{input_hashes['accepted_b00_reference']}.",
)

audit = pd.read_csv(AUDIT_PATH, low_memory=False)
require(len(audit) == 1, f"Runtime audit must contain one row; found {len(audit)}")

missing_audit_columns = sorted(set(AUDIT_PASS_COLUMNS).difference(audit.columns))
require(
    not missing_audit_columns,
    f"Runtime audit is missing pass fields: {missing_audit_columns}",
)

audit_row = audit.iloc[0]
failed_audit_checks = [
    column for column in AUDIT_PASS_COLUMNS if not truthy(audit_row[column])
]

require(
    not failed_audit_checks,
    "Runtime configuration audit failed: " + ", ".join(failed_audit_checks),
)
require(
    int(audit_row["observed_grid_count"]) == 24_889,
    "Runtime audit observed an unexpected canonical-grid count.",
)
require(
    int(audit_row["observed_distinct_cell_ids"]) == 24_889,
    "Runtime audit observed an unexpected distinct cell_id count.",
)
require(
    abs(float(audit_row["coverage_age_x_offset_pixels"]) - 76.0) <= 1e-8,
    "Unexpected coverage-age X pixel offset.",
)
require(
    abs(float(audit_row["coverage_age_y_offset_pixels"]) - 2205.0) <= 1e-8,
    "Unexpected coverage-age Y pixel offset.",
)


# -----------------------------------------------------------------------------
# 4. Load and structurally validate both b00 exports
# -----------------------------------------------------------------------------

reference = pd.read_csv(REFERENCE_PATH, low_memory=False)
verification = pd.read_csv(VERIFICATION_PATH, low_memory=False)

for label, frame in [("reference", reference), ("verification", verification)]:
    require(
        frame.shape == (EXPECTED_ROWS, EXPECTED_COLUMNS),
        f"{label}: expected shape ({EXPECTED_ROWS}, {EXPECTED_COLUMNS}), "
        f"found {frame.shape}",
    )
    require(KEY_COLUMN in frame.columns, f"{label}: missing {KEY_COLUMN}")
    require(
        frame[KEY_COLUMN].nunique() == EXPECTED_ROWS,
        f"{label}: {KEY_COLUMN} is not unique",
    )
    require(
        int(frame.isna().sum().sum()) == 0,
        f"{label}: missing values found",
    )

require(
    reference.columns.tolist() == verification.columns.tolist(),
    "Reference and verification column names or order differ.",
)

reference[KEY_COLUMN] = reference[KEY_COLUMN].astype(str)
verification[KEY_COLUMN] = verification[KEY_COLUMN].astype(str)

require(
    set(reference[KEY_COLUMN]) == set(verification[KEY_COLUMN]),
    "Reference and verification cell_id populations differ.",
)

reference = reference.sort_values(KEY_COLUMN).reset_index(drop=True)
verification = verification.sort_values(KEY_COLUMN).reset_index(drop=True)

require(
    reference[KEY_COLUMN].equals(verification[KEY_COLUMN]),
    "Sorted cell_id order does not reconcile.",
)


# -----------------------------------------------------------------------------
# 5. Exact metadata and cell-by-cell numerical comparison
# -----------------------------------------------------------------------------

metadata_mismatch_counts = {}
for column in EXACT_METADATA_COLUMNS:
    require(column in reference.columns, f"Missing metadata column: {column}")
    mismatch_count = int(
        (reference[column].astype(str) != verification[column].astype(str)).sum()
    )
    metadata_mismatch_counts[column] = mismatch_count

require(
    sum(metadata_mismatch_counts.values()) == 0,
    f"Metadata mismatches found: {metadata_mismatch_counts}",
)

numeric_columns = [
    column
    for column in reference.columns
    if column not in {KEY_COLUMN, *EXACT_METADATA_COLUMNS}
]

reference_numeric = reference[numeric_columns].apply(pd.to_numeric, errors="raise")
verification_numeric = verification[numeric_columns].apply(
    pd.to_numeric, errors="raise"
)

absolute_difference = (verification_numeric - reference_numeric).abs()

column_rows = []
for column in numeric_columns:
    values = absolute_difference[column].to_numpy(dtype=float)
    column_rows.append(
        {
            "column": column,
            "maximum_absolute_difference": float(values.max()),
            "mean_absolute_difference": float(values.mean()),
            "root_mean_square_difference": float(np.sqrt(np.mean(values ** 2))),
            "cells_above_tolerance": int((values > AREA_TOLERANCE_HA).sum()),
            "tolerance": AREA_TOLERANCE_HA,
            "output_version": OUTPUT_VERSION,
        }
    )

column_comparison = pd.DataFrame(column_rows)
column_comparison = column_comparison.sort_values(
    ["maximum_absolute_difference", "column"],
    ascending=[False, True],
).reset_index(drop=True)

cell_maximum = absolute_difference.max(axis=1)
cell_columns_above = (absolute_difference > AREA_TOLERANCE_HA).sum(axis=1)
cell_comparison = pd.DataFrame(
    {
        "cell_id": reference[KEY_COLUMN],
        "GRID_ID": reference["GRID_ID"],
        "maximum_absolute_difference": cell_maximum,
        "columns_above_tolerance": cell_columns_above,
        "tolerance": AREA_TOLERANCE_HA,
        "output_version": OUTPUT_VERSION,
    }
).sort_values(["maximum_absolute_difference", "cell_id"], ascending=[False, True])

maximum_absolute_difference = float(absolute_difference.to_numpy().max())
cells_above_tolerance = int((cell_maximum > AREA_TOLERANCE_HA).sum())
columns_above_tolerance = int(
    (column_comparison["cells_above_tolerance"] > 0).sum()
)

require(
    maximum_absolute_difference <= AREA_TOLERANCE_HA,
    "Explicit-transform replication differs from the accepted pilot above "
    f"the {AREA_TOLERANCE_HA} ha tolerance. Maximum difference: "
    f"{maximum_absolute_difference} ha.",
)
require(cells_above_tolerance == 0, "Cells above tolerance were found.")
require(columns_above_tolerance == 0, "Columns above tolerance were found.")


# -----------------------------------------------------------------------------
# 6. Outputs and validation record
# -----------------------------------------------------------------------------

column_comparison.to_csv(
    COLUMN_COMPARISON_PATH,
    index=False,
    float_format="%.12g",
)
cell_comparison.to_csv(
    CELL_COMPARISON_PATH,
    index=False,
    float_format="%.12g",
)

validation = {
    "validation_status": "PASS",
    "output_version": OUTPUT_VERSION,
    "input_files": {
        "runtime_configuration_audit": {
            "path": str(AUDIT_PATH),
            "sha256": input_hashes["runtime_configuration_audit"],
            "rows": int(len(audit)),
        },
        "accepted_b00_reference": {
            "path": str(REFERENCE_PATH),
            "sha256": input_hashes["accepted_b00_reference"],
            "rows": int(len(reference)),
            "columns": int(len(reference.columns)),
        },
        "explicit_native_transform_b00": {
            "path": str(VERIFICATION_PATH),
            "sha256": input_hashes["explicit_native_transform_b00"],
            "rows": int(len(verification)),
            "columns": int(len(verification.columns)),
        },
    },
    "runtime_configuration": {
        "audit_version": str(audit_row["audit_version"]),
        "module_path": str(audit_row["module_path"]),
        "runtime_coverage_asset": str(audit_row["runtime_coverage_asset"]),
        "runtime_pasture_age_asset": str(
            audit_row["runtime_pasture_age_asset"]
        ),
        "runtime_analytical_grid": str(audit_row["runtime_analytical_grid"]),
        "runtime_crs": str(audit_row["runtime_crs"]),
        "runtime_transform": str(audit_row["runtime_transform"]),
        "coverage_native_transform": str(
            audit_row["coverage_native_transform"]
        ),
        "observed_grid_count": int(audit_row["observed_grid_count"]),
        "observed_distinct_cell_ids": int(
            audit_row["observed_distinct_cell_ids"]
        ),
        "coverage_age_x_offset_pixels": float(
            audit_row["coverage_age_x_offset_pixels"]
        ),
        "coverage_age_y_offset_pixels": float(
            audit_row["coverage_age_y_offset_pixels"]
        ),
        "failed_checks": failed_audit_checks,
    },
    "b00_comparison": {
        "key": KEY_COLUMN,
        "rows_compared": int(len(reference)),
        "numeric_columns_compared": int(len(numeric_columns)),
        "exact_metadata_columns": EXACT_METADATA_COLUMNS,
        "metadata_mismatch_counts": metadata_mismatch_counts,
        "tolerance_ha": AREA_TOLERANCE_HA,
        "maximum_absolute_difference_ha": maximum_absolute_difference,
        "cells_above_tolerance": cells_above_tolerance,
        "columns_above_tolerance": columns_above_tolerance,
    },
    "outputs": {
        "column_comparison": {
            "path": str(COLUMN_COMPARISON_PATH),
            "sha256": sha256_file(COLUMN_COMPARISON_PATH),
            "rows": int(len(column_comparison)),
        },
        "cell_comparison": {
            "path": str(CELL_COMPARISON_PATH),
            "sha256": sha256_file(CELL_COMPARISON_PATH),
            "rows": int(len(cell_comparison)),
        },
    },
    "checks": {
        "runtime_configuration_all_pass": True,
        "reference_hash_matches_pinned_value": True,
        "expected_b00_shapes": True,
        "identical_column_names_and_order": True,
        "unique_and_identical_cell_population": True,
        "exact_metadata_match": True,
        "all_numeric_fields_compared_by_cell": True,
        "maximum_difference_within_tolerance": True,
        "no_cells_above_tolerance": True,
        "no_columns_above_tolerance": True,
    },
}

with VALIDATION_PATH.open("w", encoding="utf-8") as destination:
    json.dump(
        validation,
        destination,
        ensure_ascii=False,
        indent=2,
        default=python_scalar,
    )

print("\nPHASE 0 PROVENANCE VALIDATION COMPLETE")
print("Validation status: PASS")
print("Runtime configuration checks:", len(AUDIT_PASS_COLUMNS), "passed")
print("Rows compared:", f"{len(reference):,}")
print("Numeric columns compared:", len(numeric_columns))
print("Maximum absolute difference (ha):", maximum_absolute_difference)
print("Cells above tolerance:", cells_above_tolerance)
print("Columns above tolerance:", columns_above_tolerance)
print("Column comparison:", COLUMN_COMPARISON_PATH)
print("Cell comparison:", CELL_COMPARISON_PATH)
print("Validation record:", VALIDATION_PATH)

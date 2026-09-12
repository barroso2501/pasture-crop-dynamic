"""
01_build_canonical_stock_flow_panel.py

Build and validate the canonical 1985-2025 five-year stock-and-flow panel
from the eight complete-domain CSV exports stored in Google Drive.

Designed for Google Colab. Run the complete script in one cell or upload it
and execute with %run. Source CSV files are read only and never modified.
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

INPUT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade/csv")
OUTPUT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade/panel")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PANEL_PATH = OUTPUT_DIR / "canonical_stock_flow_panel_1985_2025_v1.parquet"
MANIFEST_PATH = OUTPUT_DIR / "canonical_stock_flow_panel_manifest_v1.csv"
VALIDATION_PATH = OUTPUT_DIR / "canonical_stock_flow_panel_validation_v1.json"

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
EXPECTED_COLUMNS = 90
EXPECTED_PANEL_ROWS = EXPECTED_ROWS_PER_INTERVAL * len(INTERVALS)
OUTPUT_VERSION = "canonical-stock-flow-v1"
AREA_TOLERANCE_HA = 1e-9
CONTINUITY_TOLERANCE_HA = 2e-6

STATE_NAMES = [
    "nat",
    "pas",
    "tmp",
    "oag",
    "out",
    "water",
    "nodata",
    "unexpected",
    "masked",
]

FOCAL_NAMES = ["nat", "pas", "tmp"]

AUXILIARY_NAMES = [
    "oag",
    "out",
    "water",
    "nodata",
    "unexpected",
    "masked",
]

RESIDUAL_COLUMNS = [
    "residual_stock0_area",
    "residual_stock1_area",
    "residual_origin_nat",
    "residual_origin_pas",
    "residual_origin_tmp",
    "residual_destination_nat",
    "residual_destination_pas",
    "residual_destination_tmp",
    "residual_pas_tmp_partition",
]

AGE_PARTITION_COLUMNS = [
    "pas_tmp_censored",
    "pas_tmp_new",
    "pas_tmp_unresolved_age",
    "pas_tmp_unattributed_age",
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
    return f"canonical_stock_flow_{t0}_{t1}_full_v1.csv"


def python_scalar(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


# ---------------------------------------------------------------------------
# Inventory and per-interval validation
# ---------------------------------------------------------------------------

print("CANONICAL STOCK-FLOW PANEL BUILD - VERSION 1")
print("Input directory:", INPUT_DIR)
print("Output directory:", OUTPUT_DIR)

require(INPUT_DIR.exists(), f"Input directory not found: {INPUT_DIR}")

expected_paths = {
    (t0, t1): INPUT_DIR / expected_filename(t0, t1)
    for t0, t1 in INTERVALS
}

missing_files = [str(path) for path in expected_paths.values() if not path.exists()]
require(not missing_files, "Missing expected files:\n" + "\n".join(missing_files))

frames = {}
manifest_rows = []
interval_checks = []
reference_columns = None
reference_cell_ids = None
reference_grid_ids = None

for t0, t1 in INTERVALS:
    interval = f"{t0}_{t1}"
    path = expected_paths[(t0, t1)]

    print(f"Reading {path.name} ...")
    frame = pd.read_csv(path, low_memory=False)

    if reference_columns is None:
        reference_columns = frame.columns.tolist()
    if reference_cell_ids is None:
        reference_cell_ids = set(frame["cell_id"].astype(str))
    if reference_grid_ids is None:
        reference_grid_ids = set(frame["GRID_ID"].astype(str))

    require(frame.shape[0] == EXPECTED_ROWS_PER_INTERVAL,
            f"{interval}: expected {EXPECTED_ROWS_PER_INTERVAL} rows, "
            f"found {frame.shape[0]}")
    require(frame.shape[1] == EXPECTED_COLUMNS,
            f"{interval}: expected {EXPECTED_COLUMNS} columns, "
            f"found {frame.shape[1]}")
    require(frame.columns.tolist() == reference_columns,
            f"{interval}: column names or order differ from the reference")
    require(frame["cell_id"].nunique() == EXPECTED_ROWS_PER_INTERVAL,
            f"{interval}: cell_id is not unique")
    require(frame["GRID_ID"].nunique() == EXPECTED_ROWS_PER_INTERVAL,
            f"{interval}: GRID_ID is not unique")
    require(set(frame["cell_id"].astype(str)) == reference_cell_ids,
            f"{interval}: cell_id membership differs from the fixed domain")
    require(set(frame["GRID_ID"].astype(str)) == reference_grid_ids,
            f"{interval}: GRID_ID membership differs from the fixed domain")
    require(int(frame.isna().sum().sum()) == 0,
            f"{interval}: missing values found")

    require(set(frame["t0"].unique()) == {t0},
            f"{interval}: invalid t0 metadata")
    require(set(frame["t1"].unique()) == {t1},
            f"{interval}: invalid t1 metadata")
    require(set(frame["interval"].unique()) == {interval},
            f"{interval}: invalid interval label")
    require(set(frame["output_version"].unique()) == {OUTPUT_VERSION},
            f"{interval}: invalid output_version")

    expected_diagnostic = 1 if (t0, t1) == (2020, 2025) else 0
    require(set(frame["diagnostic_interval"].unique()) == {expected_diagnostic},
            f"{interval}: invalid diagnostic_interval flag")

    area_columns = [
        column for column in frame.columns
        if (
            column.startswith("stock")
            or column.startswith("flow")
            or column.startswith("pas_tmp_")
            or column in {
                "geometry_area_ha",
                "valid0_area_ha",
                "valid1_area_ha",
                "raster_area_ha",
            }
        )
        and not column.startswith("residual_")
    ]

    negative_values = int((frame[area_columns] < -AREA_TOLERANCE_HA).sum().sum())
    require(negative_values == 0, f"{interval}: negative area values found")

    residual_max = float(frame[RESIDUAL_COLUMNS].abs().max().max())
    residual_rows_over_tolerance = int(
        (frame[RESIDUAL_COLUMNS].abs() > AREA_TOLERANCE_HA).any(axis=1).sum()
    )
    require(residual_rows_over_tolerance == 0,
            f"{interval}: accounting residual exceeds tolerance")

    partition = frame[AGE_PARTITION_COLUMNS].sum(axis=1)
    partition_max_difference = float((frame["flow_pas_tmp"] - partition).abs().max())
    require(partition_max_difference <= AREA_TOLERANCE_HA,
            f"{interval}: PAS->TMP partition does not close")

    flow_bound_violations = 0

    for origin in FOCAL_NAMES:
        for destination in STATE_NAMES:
            flow = f"flow_{origin}_{destination}"
            origin_stock = f"stock0_{origin}"
            flow_bound_violations += int(
                ((frame[flow] - frame[origin_stock]) > CONTINUITY_TOLERANCE_HA).sum()
            )

    for origin in AUXILIARY_NAMES:
        for destination in FOCAL_NAMES:
            flow = f"flow_{origin}_{destination}"
            destination_stock = f"stock1_{destination}"
            flow_bound_violations += int(
                ((frame[flow] - frame[destination_stock])
                 > CONTINUITY_TOLERANCE_HA).sum()
            )

    require(flow_bound_violations == 0,
            f"{interval}: flow exceeds an origin or destination stock")

    nodata_area = float(frame["stock0_nodata"].sum() + frame["stock1_nodata"].sum())
    unexpected_area = float(
        frame["stock0_unexpected"].sum() + frame["stock1_unexpected"].sum()
    )
    require(abs(nodata_area) <= AREA_TOLERANCE_HA,
            f"{interval}: class-27 area found")
    require(abs(unexpected_area) <= AREA_TOLERANCE_HA,
            f"{interval}: unexpected coverage area found")

    file_hash = sha256_file(path)
    manifest_rows.append({
        "interval": interval,
        "t0": t0,
        "t1": t1,
        "filename": path.name,
        "file_size_bytes": path.stat().st_size,
        "sha256": file_hash,
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
        "negative_area_values": negative_values,
        "maximum_absolute_residual_ha": residual_max,
        "residual_rows_over_1e_9_ha": residual_rows_over_tolerance,
        "flow_bound_violations": flow_bound_violations,
        "maximum_partition_difference_ha": partition_max_difference,
        "nodata_area_ha": nodata_area,
        "unexpected_area_ha": unexpected_area,
    })

    frames[(t0, t1)] = frame


# ---------------------------------------------------------------------------
# Longitudinal continuity
# ---------------------------------------------------------------------------

continuity_checks = []

for previous_interval, next_interval in zip(INTERVALS[:-1], INTERVALS[1:]):
    previous = frames[previous_interval].sort_values("cell_id").reset_index(drop=True)
    following = frames[next_interval].sort_values("cell_id").reset_index(drop=True)
    shared_year = previous_interval[1]

    require(previous["cell_id"].equals(following["cell_id"]),
            f"{shared_year}: cell_id sequence differs between intervals")

    differences = np.column_stack([
        previous[f"stock1_{state}"].to_numpy()
        - following[f"stock0_{state}"].to_numpy()
        for state in STATE_NAMES
    ])

    maximum_difference = float(np.abs(differences).max())
    values_over_tolerance = int(
        (np.abs(differences) > CONTINUITY_TOLERANCE_HA).sum()
    )
    rows_over_tolerance = int(
        (np.abs(differences) > CONTINUITY_TOLERANCE_HA).any(axis=1).sum()
    )

    require(values_over_tolerance == 0,
            f"{shared_year}: endpoint stocks fail longitudinal continuity")

    continuity_checks.append({
        "shared_year": shared_year,
        "maximum_absolute_difference_ha": maximum_difference,
        "values_over_2e_6_ha": values_over_tolerance,
        "rows_over_2e_6_ha": rows_over_tolerance,
    })


# ---------------------------------------------------------------------------
# Panel assembly and final checks
# ---------------------------------------------------------------------------

panel = pd.concat(
    [frames[interval] for interval in INTERVALS],
    axis=0,
    ignore_index=True,
    copy=False,
)

panel = panel.sort_values(["cell_id", "t0", "t1"], kind="stable").reset_index(drop=True)

require(panel.shape == (EXPECTED_PANEL_ROWS, EXPECTED_COLUMNS),
        f"Final panel has unexpected shape: {panel.shape}")
require(panel.duplicated(subset=["cell_id", "t0", "t1"]).sum() == 0,
        "Final panel contains duplicate cell-interval rows")
require(panel.groupby("cell_id")["interval"].nunique().eq(8).all(),
        "At least one cell does not contain all eight intervals")
require(panel["diagnostic_interval"].sum() == EXPECTED_ROWS_PER_INTERVAL,
        "Diagnostic flag count is not 24,889")


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

manifest = pd.DataFrame(manifest_rows)
manifest.to_csv(MANIFEST_PATH, index=False)

panel.to_parquet(
    PANEL_PATH,
    index=False,
    engine="pyarrow",
    compression="snappy",
)

panel_hash = sha256_file(PANEL_PATH)

validation = {
    "validation_status": "PASS",
    "validation_version": "canonical-stock-flow-panel-validation-v1",
    "source_directory": str(INPUT_DIR),
    "output_panel": str(PANEL_PATH),
    "output_panel_sha256": panel_hash,
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
    "continuity_tolerance_ha": CONTINUITY_TOLERANCE_HA,
    "maximum_absolute_residual_ha": float(
        max(item["maximum_absolute_residual_ha"] for item in interval_checks)
    ),
    "maximum_longitudinal_difference_ha": float(
        max(item["maximum_absolute_difference_ha"] for item in continuity_checks)
    ),
    "interval_checks": interval_checks,
    "continuity_checks": continuity_checks,
}

with VALIDATION_PATH.open("w", encoding="utf-8") as output:
    json.dump(validation, output, indent=2, ensure_ascii=False, default=python_scalar)


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
    "Maximum longitudinal difference (ha):",
    f"{validation['maximum_longitudinal_difference_ha']:.12g}",
)
print("\nFiles created:")
print(PANEL_PATH)
print(MANIFEST_PATH)
print(VALIDATION_PATH)

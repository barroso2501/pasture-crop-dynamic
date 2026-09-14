"""
Export Phase 3B cell-level metrics and frozen map classes for GIS joins.

Designed for Google Colab. The script creates one CSV per five-year interval,
with exactly one row per canonical cell_id. Each table combines selected
continuous Phase 2 metrics, spatial/support attributes, and the corresponding
Phase 3B class labels and codes. A schema.ini file preserves field types when
the CSVs are opened in ArcGIS Pro.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile


# -----------------------------------------------------------------------------
# 0. Colab dependency
# -----------------------------------------------------------------------------

if importlib.util.find_spec("pyarrow") is None:
    print("Installing missing dependency: pyarrow>=14")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "pyarrow>=14"]
    )

import numpy as np
import pandas as pd

try:
    from google.colab import drive
except ImportError:
    drive = None


# -----------------------------------------------------------------------------
# 1. Paths and canonical identities
# -----------------------------------------------------------------------------

if drive is not None:
    drive.mount("/content/drive")

PROJECT_DIR = Path(
    os.environ.get(
        "CANONICAL_SPATIAL_PROJECT_DIR",
        "/content/drive/MyDrive/Trabalho/Contabilidade",
    )
)

PHASE2_DIR = PROJECT_DIR / "spatial" / "phase2"
PHASE3_DIR = PROJECT_DIR / "spatial" / "phase3"
OUTPUT_DIR = PHASE3_DIR / "gis_tables_v1"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

METRICS_INPUT = PHASE2_DIR / "canonical_spatial_metrics_panel_v1.parquet"
PHASE2_VALIDATION_INPUT = PHASE2_DIR / "canonical_spatial_metrics_validation_v1.json"
CLASSES_INPUT = PHASE3_DIR / "canonical_spatial_map_classes_v1.parquet"
PHASE3B_VALIDATION_INPUT = PHASE3_DIR / "canonical_comparable_maps_validation_v1.json"

MANIFEST_OUTPUT = OUTPUT_DIR / "canonical_gis_interval_tables_manifest_v1.csv"
DICTIONARY_OUTPUT = OUTPUT_DIR / "canonical_gis_interval_fields_v1.csv"
SCHEMA_OUTPUT = OUTPUT_DIR / "schema.ini"
ZIP_OUTPUT = OUTPUT_DIR / "canonical_gis_interval_tables_v1.zip"
VALIDATION_OUTPUT = OUTPUT_DIR / "canonical_gis_interval_tables_validation_v1.json"

EXPECTED_METRICS_SHA256 = (
    "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c"
)
EXPECTED_PHASE2_VALIDATION_SHA256 = (
    "9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8"
)

EXPECTED_ROWS = 199_112
EXPECTED_CELLS = 24_889
EXPECTED_INTERVALS = 8
EXPECTED_METRIC_COLUMNS = 211
EXPECTED_CLASS_METRICS = 12
EXPECTED_CLASS_COLUMNS = EXPECTED_CLASS_METRICS * 2

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
DIAGNOSTIC_INTERVAL = (2020, 2025)
KEY_COLUMNS = ["cell_id", "t0", "t1"]
OUTPUT_VERSION = "canonical-gis-interval-tables-v1"
MAP_CLASS_VERSION = "canonical-comparable-map-classes-v2"
MAP_PRODUCT_VERSION = "canonical-comparable-interval-maps-v1"


# -----------------------------------------------------------------------------
# 2. GIS field selection
# -----------------------------------------------------------------------------

IDENTIFIER_COLUMNS = [
    "cell_id",
    "GRID_ID",
    "t0",
    "t1",
    "interval",
    "diagnostic_interval",
    "primary_inference_interval",
]

SPATIAL_CONTEXT_COLUMNS = [
    "geometry_area_geodesic_ha",
    "geometry_area_aea_ha",
    "centroid_lon_aea",
    "centroid_lat_aea",
    "amazon_overlap_ha",
    "cerrado_overlap_ha",
    "amazon_fraction_cell",
    "cerrado_fraction_cell",
    "target_biome_fraction_cell",
    "outside_target_biomes_fraction",
    "primary_biome",
    "primary_biome_code",
    "primary_biome_fraction_cell",
    "primary_biome_fraction_target_overlap",
    "crosses_amazon_cerrado_boundary",
    "extends_outside_target_biomes",
    "neighbor_count",
    "is_island",
    "component_id",
    "component_size",
]

DENOMINATOR_COLUMNS = [
    "stock0_pas",
    "stock0_nat",
    "gross_cr_activity_ha",
]

METRIC_COLUMNS = [
    "consolidation_ha",
    "consolidation_rate_initial_pasture",
    "replenishment_ha",
    "replenishment_rate_initial_native",
    "nat_tmp_endpoint_ha",
    "nat_tmp_intensity_initial_native",
    "nat_tmp_pas_any_ha",
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_pas_consecutive2_share_endpoint",
    "net_cr_balance_ha",
    "cr_balance_index",
]

SUPPORT_COLUMNS = [
    "consolidation_rate_defined",
    "replenishment_rate_defined",
    "nat_tmp_intensity_defined",
    "cr_balance_defined",
    "nat_tmp_endpoint_share_defined",
    "nat_tmp_pas_any_share_defined",
]

OCCURRENCE_COLUMNS = [
    "has_consolidation",
    "has_replenishment",
    "has_cr_activity",
]

VERSION_COLUMNS = [
    "spatial_support_version",
    "graph_version",
    "spatial_metrics_version",
]

BASE_COLUMNS = (
    IDENTIFIER_COLUMNS
    + SPATIAL_CONTEXT_COLUMNS
    + DENOMINATOR_COLUMNS
    + METRIC_COLUMNS
    + SUPPORT_COLUMNS
    + OCCURRENCE_COLUMNS
    + VERSION_COLUMNS
)

UNITS = {
    "geometry_area_geodesic_ha": "ha",
    "geometry_area_aea_ha": "ha",
    "centroid_lon_aea": "decimal_degree",
    "centroid_lat_aea": "decimal_degree",
    "amazon_overlap_ha": "ha",
    "cerrado_overlap_ha": "ha",
    "stock0_pas": "ha",
    "stock0_nat": "ha",
    "gross_cr_activity_ha": "ha",
    "consolidation_ha": "ha",
    "replenishment_ha": "ha",
    "nat_tmp_endpoint_ha": "ha",
    "nat_tmp_pas_any_ha": "ha",
    "nat_tmp_pas_consecutive2_ha": "ha",
    "net_cr_balance_ha": "ha",
    "consolidation_rate_initial_pasture": "proportion",
    "replenishment_rate_initial_native": "proportion",
    "nat_tmp_intensity_initial_native": "proportion",
    "nat_tmp_pas_any_share_endpoint": "proportion",
    "nat_tmp_pas_consecutive2_share_endpoint": "proportion",
    "cr_balance_index": "bounded_index_-1_to_1",
}

DESCRIPTIONS = {
    "cell_id": "Canonical unique cell identifier and recommended GIS join key.",
    "GRID_ID": "Parent-grid identifier retained for provenance.",
    "t0": "Initial year of the five-year accounting interval.",
    "t1": "Final year of the five-year accounting interval.",
    "interval": "Interval label in YYYY_YYYY format.",
    "diagnostic_interval": "1 for the diagnostic 2020-2025 interval; otherwise 0.",
    "primary_inference_interval": "1 for the seven primary intervals; otherwise 0.",
    "geometry_area_geodesic_ha": "Complete-cell geodesic area recorded by Earth Engine.",
    "geometry_area_aea_ha": "Complete-cell area in the project Albers equal-area CRS.",
    "centroid_lon_aea": "Longitude of the centroid derived in the AEA CRS.",
    "centroid_lat_aea": "Latitude of the centroid derived in the AEA CRS.",
    "amazon_overlap_ha": "Cell area overlapping the Amazon biome.",
    "cerrado_overlap_ha": "Cell area overlapping the Cerrado biome.",
    "amazon_fraction_cell": "Fraction of complete cell overlapping the Amazon biome.",
    "cerrado_fraction_cell": "Fraction of complete cell overlapping the Cerrado biome.",
    "target_biome_fraction_cell": "Fraction overlapping either target biome.",
    "outside_target_biomes_fraction": "Fraction outside Amazon and Cerrado polygons.",
    "primary_biome": "Deterministic dominant-overlap biome label.",
    "primary_biome_code": "IBGE code of the primary biome.",
    "primary_biome_fraction_cell": "Complete-cell fraction in the primary biome.",
    "primary_biome_fraction_target_overlap": "Primary-biome share of target-biome overlap.",
    "crosses_amazon_cerrado_boundary": "1 when the cell overlaps both target biomes.",
    "extends_outside_target_biomes": "1 when part of the complete cell lies outside both biomes.",
    "neighbor_count": "Number of shared-edge neighbors in the fixed canonical graph.",
    "is_island": "1 when the cell has no shared-edge neighbor in the reduced domain.",
    "component_id": "Connected-component identifier in the fixed graph.",
    "component_size": "Number of cells in the connected component.",
    "stock0_pas": "Pasture stock at the beginning of the interval.",
    "stock0_nat": "Native-vegetation stock at the beginning of the interval.",
    "gross_cr_activity_ha": "Consolidation plus replenishment area.",
    "consolidation_ha": "Pasture-to-temporary-crop flow (PAS to TMP).",
    "consolidation_rate_initial_pasture": "Consolidation divided by initial pasture stock.",
    "replenishment_ha": "Native-vegetation-to-pasture flow (NAT to PAS).",
    "replenishment_rate_initial_native": "Replenishment divided by initial native stock.",
    "nat_tmp_endpoint_ha": "Native-to-temporary-crop endpoint flow (NAT to TMP).",
    "nat_tmp_intensity_initial_native": "NAT-TMP endpoint flow divided by initial native stock.",
    "nat_tmp_pas_any_ha": "NAT-TMP endpoint area with pasture in any intermediate year.",
    "nat_tmp_pas_any_share_endpoint": "Share of NAT-TMP endpoint area with any intermediate pasture.",
    "nat_tmp_pas_consecutive2_ha": "NAT-TMP area with pasture in at least two consecutive intermediate years.",
    "nat_tmp_pas_consecutive2_share_endpoint": "Share of NAT-TMP endpoint area with at least two consecutive pasture years.",
    "net_cr_balance_ha": "Consolidation minus replenishment area.",
    "cr_balance_index": "Net C-R balance divided by gross C-R activity; undefined when inactive.",
    "consolidation_rate_defined": "1 when initial pasture supports the consolidation rate.",
    "replenishment_rate_defined": "1 when initial native area supports the replenishment rate.",
    "nat_tmp_intensity_defined": "1 when initial native area supports NAT-TMP intensity.",
    "cr_balance_defined": "1 when gross C-R activity is positive.",
    "nat_tmp_endpoint_share_defined": "1 when NAT-TMP endpoint area is positive.",
    "nat_tmp_pas_any_share_defined": "1 when any-pasture trajectory area is positive.",
    "has_consolidation": "Primary-tolerance occurrence flag for consolidation.",
    "has_replenishment": "Primary-tolerance occurrence flag for replenishment.",
    "has_cr_activity": "Primary-tolerance occurrence flag for any C-R activity.",
    "spatial_support_version": "Version of the canonical spatial support.",
    "graph_version": "Version of the fixed shared-edge graph.",
    "spatial_metrics_version": "Version of the Phase 2 spatial metrics.",
}


# -----------------------------------------------------------------------------
# 3. Helpers
# -----------------------------------------------------------------------------

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(chunk_size), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_identifier(value) -> str:
    if pd.isna(value):
        raise ValueError("Missing identifier encountered")
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    return str(value).strip()


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "not-recorded"


def python_scalar(value):
    if isinstance(value, np.generic):
        return value.item()
    return value


def interval_label(t0: int, t1: int) -> str:
    return f"{int(t0)}_{int(t1)}"


def schema_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series.dtype):
        return "Long"
    if pd.api.types.is_float_dtype(series.dtype):
        return "Double"
    if pd.api.types.is_bool_dtype(series.dtype):
        return "Long"
    maximum_length = series.astype("string").str.len().max(skipna=True)
    if pd.isna(maximum_length):
        maximum_length = 32
    width = max(32, min(255, int(maximum_length)))
    return f"Text Width {width}"


def field_role(field: str) -> str:
    if field in IDENTIFIER_COLUMNS:
        return "identifier_or_interval"
    if field in SPATIAL_CONTEXT_COLUMNS:
        return "spatial_context"
    if field in DENOMINATOR_COLUMNS:
        return "denominator_or_activity"
    if field in METRIC_COLUMNS:
        return "continuous_metric"
    if field in SUPPORT_COLUMNS:
        return "support_flag"
    if field in OCCURRENCE_COLUMNS:
        return "occurrence_flag"
    if field in VERSION_COLUMNS:
        return "provenance"
    if field.endswith("__class"):
        return "frozen_map_class_label"
    if field.endswith("__code"):
        return "frozen_map_class_code"
    return "other"


def field_description(field: str) -> str:
    if field in DESCRIPTIONS:
        return DESCRIPTIONS[field]
    if field.endswith("__class"):
        metric = field.removesuffix("__class")
        return f"Frozen Phase 3A v2 map-class label for {metric}."
    if field.endswith("__code"):
        metric = field.removesuffix("__code")
        return f"Ordered integer code for the frozen map class of {metric}."
    return "Field retained from the validated canonical workflow."


def missing_meaning(field: str) -> str:
    if field in {
        "consolidation_rate_initial_pasture",
        "replenishment_rate_initial_native",
        "nat_tmp_intensity_initial_native",
        "cr_balance_index",
        "nat_tmp_pas_any_share_endpoint",
        "nat_tmp_pas_consecutive2_share_endpoint",
    }:
        return "Undefined process-specific denominator; see support flag and class."
    return "No missing values expected."


# -----------------------------------------------------------------------------
# 4. Authenticate inputs
# -----------------------------------------------------------------------------

print("CANONICAL GIS INTERVAL TABLE EXPORT - VERSION 1")
print("Project directory:", PROJECT_DIR)
print("Output directory:", OUTPUT_DIR)

for path in [
    METRICS_INPUT,
    PHASE2_VALIDATION_INPUT,
    CLASSES_INPUT,
    PHASE3B_VALIDATION_INPUT,
]:
    require(path.exists(), f"Missing required input: {path}")

metrics_hash = sha256_file(METRICS_INPUT)
phase2_validation_hash = sha256_file(PHASE2_VALIDATION_INPUT)
classes_hash = sha256_file(CLASSES_INPUT)
phase3b_validation_hash = sha256_file(PHASE3B_VALIDATION_INPUT)

require(metrics_hash == EXPECTED_METRICS_SHA256,
        "Phase 2 metrics-panel SHA-256 mismatch")
require(phase2_validation_hash == EXPECTED_PHASE2_VALIDATION_SHA256,
        "Phase 2 validation SHA-256 mismatch")

with PHASE2_VALIDATION_INPUT.open("r", encoding="utf-8") as source:
    phase2_validation = json.load(source)
with PHASE3B_VALIDATION_INPUT.open("r", encoding="utf-8") as source:
    phase3b_validation = json.load(source)

require(phase2_validation.get("validation_status") == "PASS",
        "Phase 2 validation did not pass")
require(all(phase2_validation.get("checks", {}).values()),
        "At least one Phase 2 validation check is false")
require(phase3b_validation.get("validation_status") == "PASS",
        "Phase 3B validation did not pass")
require(all(phase3b_validation.get("checks", {}).values()),
        "At least one Phase 3B validation check is false")
require(phase3b_validation.get("map_class_version") == MAP_CLASS_VERSION,
        "Unexpected map-class version")
require(phase3b_validation.get("map_product_version") == MAP_PRODUCT_VERSION,
        "Unexpected map-product version")

recorded_classes = phase3b_validation.get("outputs", {}).get(
    CLASSES_INPUT.name, {}
).get("sha256")
require(recorded_classes == classes_hash,
        "Classified panel does not match the Phase 3B validation record")


# -----------------------------------------------------------------------------
# 5. Read, join, and validate the cell-level table
# -----------------------------------------------------------------------------

metrics = pd.read_parquet(METRICS_INPUT)
classes = pd.read_parquet(CLASSES_INPUT)

metrics["cell_id"] = metrics["cell_id"].map(normalize_identifier)
metrics["GRID_ID"] = metrics["GRID_ID"].map(normalize_identifier)
classes["cell_id"] = classes["cell_id"].map(normalize_identifier)

require(metrics.shape == (EXPECTED_ROWS, EXPECTED_METRIC_COLUMNS),
        f"Unexpected Phase 2 panel shape: {metrics.shape}")
require(len(classes) == EXPECTED_ROWS,
        f"Unexpected classified-panel rows: {len(classes)}")
require(metrics.duplicated(KEY_COLUMNS).sum() == 0,
        "Duplicate Phase 2 cell-interval keys")
require(classes.duplicated(KEY_COLUMNS).sum() == 0,
        "Duplicate Phase 3B cell-interval keys")
require(metrics["cell_id"].nunique() == EXPECTED_CELLS,
        "Unexpected Phase 2 cell population")
require(classes["cell_id"].nunique() == EXPECTED_CELLS,
        "Unexpected Phase 3B cell population")

missing_base_columns = sorted(set(BASE_COLUMNS) - set(metrics.columns))
require(not missing_base_columns,
        f"Missing required Phase 2 fields: {missing_base_columns}")

class_label_columns = sorted(
    column for column in classes.columns if column.endswith("__class")
)
class_code_columns = sorted(
    column for column in classes.columns if column.endswith("__code")
)
require(len(class_label_columns) == EXPECTED_CLASS_METRICS,
        "Unexpected number of map-class label fields")
require(len(class_code_columns) == EXPECTED_CLASS_METRICS,
        "Unexpected number of map-class code fields")
require(
    {column.removesuffix("__class") for column in class_label_columns}
    == {column.removesuffix("__code") for column in class_code_columns},
    "Class-label and class-code metrics differ",
)

class_columns = []
for metric in METRIC_COLUMNS:
    class_field = f"{metric}__class"
    code_field = f"{metric}__code"
    require(class_field in classes.columns and code_field in classes.columns,
            f"Missing classified fields for {metric}")
    class_columns.extend([class_field, code_field])

left_keys = metrics[KEY_COLUMNS].sort_values(KEY_COLUMNS).reset_index(drop=True)
right_keys = classes[KEY_COLUMNS].sort_values(KEY_COLUMNS).reset_index(drop=True)
require(left_keys.equals(right_keys),
        "Phase 2 and Phase 3B cell-interval keys differ")

joined = metrics[BASE_COLUMNS].merge(
    classes[KEY_COLUMNS + class_columns],
    on=KEY_COLUMNS,
    how="left",
    validate="one_to_one",
)
joined = joined.sort_values(["t0", "t1", "cell_id"]).reset_index(drop=True)
require(len(joined) == EXPECTED_ROWS, "GIS join changed the panel row count")
require(not joined[class_columns].isna().any().any(),
        "Missing map class after GIS-table join")
require(joined.groupby(["t0", "t1"]).size().eq(EXPECTED_CELLS).all(),
        "At least one GIS interval is incomplete")

observed_intervals = sorted(
    (int(row.t0), int(row.t1))
    for row in joined[["t0", "t1"]].drop_duplicates().itertuples()
)
require(observed_intervals == INTERVALS, "Unexpected GIS interval sequence")


# -----------------------------------------------------------------------------
# 6. Export one one-to-one table per interval
# -----------------------------------------------------------------------------

csv_paths = []
manifest_rows = []
schema_sections = []

for t0, t1 in INTERVALS:
    interval = interval_label(t0, t1)
    interval_table = joined.loc[
        joined["t0"].eq(t0) & joined["t1"].eq(t1)
    ].copy()
    interval_table = interval_table.sort_values("cell_id").reset_index(drop=True)
    require(len(interval_table) == EXPECTED_CELLS,
            f"Unexpected rows for {interval}")
    require(interval_table["cell_id"].is_unique,
            f"cell_id is not unique for {interval}")
    require(interval_table["cell_id"].notna().all(),
            f"Missing cell_id for {interval}")

    output_path = OUTPUT_DIR / f"canonical_gis_metrics_classes_{interval}_v1.csv"
    interval_table.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
        float_format="%.15g",
        quoting=csv.QUOTE_NONNUMERIC,
    )
    require(output_path.exists() and output_path.stat().st_size > 0,
            f"CSV not created: {output_path}")

    reread = pd.read_csv(output_path, dtype={"cell_id": "string", "GRID_ID": "string"})
    require(len(reread) == EXPECTED_CELLS,
            f"CSV reread row mismatch for {interval}")
    require(reread["cell_id"].nunique() == EXPECTED_CELLS,
            f"CSV reread cell_id mismatch for {interval}")
    require(set(reread["cell_id"]) == set(interval_table["cell_id"]),
            f"CSV reread changed cell identifiers for {interval}")

    csv_paths.append(output_path)
    manifest_rows.append(
        {
            "t0": t0,
            "t1": t1,
            "interval": interval,
            "diagnostic_interval": int((t0, t1) == DIAGNOSTIC_INTERVAL),
            "file_name": output_path.name,
            "row_count": len(interval_table),
            "distinct_cell_id": interval_table["cell_id"].nunique(),
            "column_count": len(interval_table.columns),
            "join_field": "cell_id",
            "join_cardinality": "one_to_one",
            "sha256": sha256_file(output_path),
            "output_version": OUTPUT_VERSION,
        }
    )

    schema_lines = [
        f"[{output_path.name}]",
        "Format=CSVDelimited",
        "ColNameHeader=True",
        "CharacterSet=65001",
        "MaxScanRows=0",
    ]
    for position, column in enumerate(interval_table.columns, start=1):
        schema_lines.append(
            f"Col{position}={column} {schema_type(interval_table[column])}"
        )
    schema_sections.append("\n".join(schema_lines))

manifest = pd.DataFrame(manifest_rows)
manifest.to_csv(MANIFEST_OUTPUT, index=False)

dictionary_rows = []
for order, column in enumerate(joined.columns, start=1):
    dictionary_rows.append(
        {
            "field_order": order,
            "field_name": column,
            "field_role": field_role(column),
            "pandas_dtype": str(joined[column].dtype),
            "schema_ini_type": schema_type(joined[column]),
            "units": UNITS.get(column, "not_applicable"),
            "missing_value_meaning": missing_meaning(column),
            "description": field_description(column),
            "output_version": OUTPUT_VERSION,
        }
    )
dictionary = pd.DataFrame(dictionary_rows)
dictionary.to_csv(DICTIONARY_OUTPUT, index=False)

SCHEMA_OUTPUT.write_text("\n\n".join(schema_sections) + "\n", encoding="utf-8")


# -----------------------------------------------------------------------------
# 7. Create portable ZIP and validation record
# -----------------------------------------------------------------------------

with zipfile.ZipFile(ZIP_OUTPUT, "w", compression=zipfile.ZIP_DEFLATED,
                     compresslevel=9) as archive:
    for path in [*csv_paths, MANIFEST_OUTPUT, DICTIONARY_OUTPUT, SCHEMA_OUTPUT]:
        archive.write(path, arcname=path.name)

with zipfile.ZipFile(ZIP_OUTPUT, "r") as archive:
    require(archive.testzip() is None, "ZIP integrity test failed")
    expected_zip_members = {
        path.name
        for path in [*csv_paths, MANIFEST_OUTPUT, DICTIONARY_OUTPUT, SCHEMA_OUTPUT]
    }
    require(set(archive.namelist()) == expected_zip_members,
            "Unexpected GIS ZIP members")

output_paths = [
    *csv_paths,
    MANIFEST_OUTPUT,
    DICTIONARY_OUTPUT,
    SCHEMA_OUTPUT,
    ZIP_OUTPUT,
]
output_hashes = {
    path.name: {"path": str(path), "sha256": sha256_file(path)}
    for path in output_paths
}

validation = {
    "validation_status": "PASS",
    "output_version": OUTPUT_VERSION,
    "purpose": "one-to-one ArcGIS join tables by five-year interval",
    "inputs": {
        METRICS_INPUT.name: {"path": str(METRICS_INPUT), "sha256": metrics_hash},
        PHASE2_VALIDATION_INPUT.name: {
            "path": str(PHASE2_VALIDATION_INPUT),
            "sha256": phase2_validation_hash,
        },
        CLASSES_INPUT.name: {"path": str(CLASSES_INPUT), "sha256": classes_hash},
        PHASE3B_VALIDATION_INPUT.name: {
            "path": str(PHASE3B_VALIDATION_INPUT),
            "sha256": phase3b_validation_hash,
        },
    },
    "structure": {
        "source_rows": len(joined),
        "cells": joined["cell_id"].nunique(),
        "intervals": len(INTERVALS),
        "csv_files": len(csv_paths),
        "rows_per_csv": EXPECTED_CELLS,
        "columns_per_csv": len(joined.columns),
        "continuous_map_metrics": len(METRIC_COLUMNS),
        "class_label_fields": len(class_label_columns),
        "class_code_fields": len(class_code_columns),
        "join_field": "cell_id",
        "join_cardinality_within_each_csv": "one_to_one",
        "diagnostic_interval": "2020_2025",
    },
    "arcgis": {
        "recommended_join": "shapefile cell_id to CSV cell_id",
        "cell_id_type": "text",
        "schema_ini_required_location": "same directory as the eight CSV files",
        "csv_encoding": "UTF-8 with BOM",
        "warning": (
            "If joined features are exported, prefer a file geodatabase or "
            "GeoPackage. Shapefile output truncates field names."
        ),
    },
    "outputs": output_hashes,
    "software": {
        "python": sys.version,
        "pandas": package_version("pandas"),
        "numpy": package_version("numpy"),
        "pyarrow": package_version("pyarrow"),
    },
    "checks": {
        "phase2_input_hashes_match": True,
        "phase2_validation_passed": True,
        "phase3b_validation_passed": True,
        "classified_panel_matches_phase3b_record": True,
        "phase2_and_phase3b_keys_match": True,
        "one_to_one_join_preserves_all_rows": True,
        "all_class_fields_complete": True,
        "eight_expected_intervals_present": True,
        "each_csv_has_24889_rows": True,
        "cell_id_unique_within_each_csv": True,
        "cell_id_survives_csv_roundtrip": True,
        "schema_ini_created": True,
        "manifest_and_dictionary_created": True,
        "portable_zip_integrity_passed": True,
    },
}

with VALIDATION_OUTPUT.open("w", encoding="utf-8") as destination:
    json.dump(validation, destination, indent=2, ensure_ascii=False,
              default=python_scalar)

print()
print("GIS INTERVAL TABLE EXPORT COMPLETE")
print("Validation status: PASS")
print("CSV files:", len(csv_paths))
print("Rows per CSV:", f"{EXPECTED_CELLS:,}")
print("Columns per CSV:", len(joined.columns))
print("Join field: cell_id")
print("Join cardinality within each interval: one-to-one")
print("Keep schema.ini in the same directory as the CSV files.")
print("Manifest:", MANIFEST_OUTPUT)
print("Field dictionary:", DICTIONARY_OUTPUT)
print("Validation record:", VALIDATION_OUTPUT)
print("Portable ZIP:", ZIP_OUTPUT)

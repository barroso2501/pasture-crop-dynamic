"""
Build and validate the Phase 3B comparable interval maps (script revision 3).

Designed for Google Colab. This script authenticates the accepted Phase 1
spatial support, Phase 2 metric panel, and final Phase 3A v2 class records. It
then reproduces the frozen classifications, verifies them against the accepted
Phase 3A counts, and creates one eight-panel map series for each of 12 metrics.

No class limit is estimated in this script. The seven primary intervals and
the diagnostic 2020-2025 interval use exactly the same frozen v2 limits.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


# -----------------------------------------------------------------------------
# 0. Colab dependencies
# -----------------------------------------------------------------------------

REQUIRED_PACKAGES = {
    "geopandas": "geopandas>=0.14,<2",
    "shapely": "shapely>=2,<3",
    "pyproj": "pyproj>=3.6,<4",
    "pyarrow": "pyarrow>=14",
    "matplotlib": "matplotlib>=3.7,<4",
    "PIL": "pillow>=10,<13",
}


def version_tuple(package: str) -> tuple[int, ...]:
    try:
        version = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return ()
    return tuple(int(part) for part in re.findall(r"\d+", version)[:3])


missing_packages = []
for module, requirement in REQUIRED_PACKAGES.items():
    installed = importlib.util.find_spec(module) is not None
    too_old = (
        (module == "geopandas" and version_tuple("geopandas") < (0, 14))
        or (module == "shapely" and version_tuple("shapely") < (2, 0))
        or (module == "matplotlib" and version_tuple("matplotlib") < (3, 7))
    )
    if not installed or too_old:
        missing_packages.append(requirement)

if missing_packages:
    print("Installing missing mapping dependencies:", missing_packages)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *missing_packages]
    )

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from PIL import Image

try:
    from google.colab import drive
except ImportError:
    drive = None


# -----------------------------------------------------------------------------
# 1. Paths, identities, and fixed scope
# -----------------------------------------------------------------------------

if drive is not None:
    drive.mount("/content/drive")

PROJECT_DIR = Path(
    os.environ.get(
        "CANONICAL_SPATIAL_PROJECT_DIR",
        "/content/drive/MyDrive/Trabalho/Contabilidade",
    )
)

INPUT_DIR = PROJECT_DIR / "spatial" / "inputs"
PHASE1_DIR = PROJECT_DIR / "spatial" / "phase1"
PHASE2_DIR = PROJECT_DIR / "spatial" / "phase2"
PHASE3_DIR = PROJECT_DIR / "spatial" / "phase3"
MAP_DIR = PHASE3_DIR / "maps_v1"
PNG_DIR = MAP_DIR / "png"
SVG_DIR = MAP_DIR / "svg"
for directory in [PHASE3_DIR, MAP_DIR, PNG_DIR, SVG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

BIOME_INPUT = INPUT_DIR / "canonical_biomes_input_ibge2025_v1.geojson"
SPATIAL_SUPPORT_INPUT = PHASE1_DIR / "canonical_spatial_support_v1.parquet"
SPATIAL_METRICS_INPUT = PHASE2_DIR / "canonical_spatial_metrics_panel_v1.parquet"
PHASE2_VALIDATION_INPUT = PHASE2_DIR / "canonical_spatial_metrics_validation_v1.json"
CLASS_LIMITS_INPUT = PHASE3_DIR / "canonical_comparable_map_class_limits_v2.csv"
CLASS_COUNTS_INPUT = PHASE3_DIR / "canonical_comparable_map_class_counts_v2.csv"
PHASE3A_VALIDATION_INPUT = PHASE3_DIR / "canonical_map_classes_validation_v2.json"

CLASSIFIED_PANEL_OUTPUT = PHASE3_DIR / "canonical_spatial_map_classes_v1.parquet"
LEGEND_OUTPUT = PHASE3_DIR / "canonical_comparable_map_legend_v1.csv"
RENDER_COUNTS_OUTPUT = PHASE3_DIR / "canonical_comparable_map_render_counts_v1.csv"
MAP_INVENTORY_OUTPUT = PHASE3_DIR / "canonical_comparable_map_inventory_v1.csv"
VALIDATION_OUTPUT = PHASE3_DIR / "canonical_comparable_maps_validation_v1.json"

EXPECTED_HASHES = {
    BIOME_INPUT.name: "1f3dfccef176e4de5b64405cc5dacf2c098805e99e2ac4449352b9fb307a38a6",
    SPATIAL_SUPPORT_INPUT.name: "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc",
    SPATIAL_METRICS_INPUT.name: "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c",
    PHASE2_VALIDATION_INPUT.name: "9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8",
    CLASS_LIMITS_INPUT.name: "b8861926a1ceb02ad8c065cbc4ea46ca6b4af2fed61561e4eb615c7aa5fc981d",
    CLASS_COUNTS_INPUT.name: "1740b1fa90d47a2031202426efb0973a02ea93a8e94f20a00323e382fe54a908",
    PHASE3A_VALIDATION_INPUT.name: "cb909c77372c34947d670342db233a51e07f31996a4bb8085947f973937f7343",
}

EXPECTED_ROWS = 199_112
EXPECTED_CELLS = 24_889
EXPECTED_INTERVALS = 8
EXPECTED_METRICS = 12
EXPECTED_CLASS_COUNT_ROWS = 504
EXPECTED_PHASE2_COLUMNS = 211

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
MAP_CLASS_VERSION = "canonical-comparable-map-classes-v2"
OUTPUT_VERSION = "canonical-comparable-interval-maps-v1"
SCRIPT_VERSION = "phase3b-comparable-interval-maps-script-v3"
SHARE_MINIMUM_CELL_FRACTION = 0.001
AREA_RECONCILIATION_TOLERANCE = 0.005
PNG_DPI = 250
WGS84_CRS = "EPSG:4326"
AEA_CRS = (
    "+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 "
    "+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"
)


# -----------------------------------------------------------------------------
# 2. Metric order and cartographic design
# -----------------------------------------------------------------------------

METRIC_ORDER = [
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

METRIC_LABELS = {
    "consolidation_ha": "Pasture-to-crop consolidation (ha)",
    "consolidation_rate_initial_pasture": "Consolidation / initial pasture",
    "replenishment_ha": "Native-to-pasture replenishment (ha)",
    "replenishment_rate_initial_native": "Replenishment / initial native vegetation",
    "nat_tmp_endpoint_ha": "Native-to-temporary-crop endpoint flow (ha)",
    "nat_tmp_intensity_initial_native": "NAT-TMP / initial native vegetation",
    "nat_tmp_pas_any_ha": "NAT-TMP with any intermediate pasture (ha)",
    "nat_tmp_pas_any_share_endpoint": "Share of NAT-TMP with any pasture",
    "nat_tmp_pas_consecutive2_ha": (
        "NAT-TMP with at least 2 consecutive pasture years (ha)"
    ),
    "nat_tmp_pas_consecutive2_share_endpoint": (
        "Share of NAT-TMP with at least 2 consecutive pasture years"
    ),
    "net_cr_balance_ha": "Net consolidation-replenishment balance (ha)",
    "cr_balance_index": "Consolidation-replenishment balance index",
}

POSITIVE_PALETTES = {
    "consolidation": {
        "undefined": "#bdbdbd", "zero": "#f7f7f7",
        "positive_low": "#dadaeb", "positive_moderate": "#9e9ac8",
        "positive_high": "#54278f",
    },
    "replenishment": {
        "undefined": "#bdbdbd", "zero": "#f7f7f7",
        "positive_low": "#c7e9c0", "positive_moderate": "#74c476",
        "positive_high": "#238b45",
    },
    "nat_tmp": {
        "undefined": "#bdbdbd", "zero": "#f7f7f7",
        "positive_low": "#fee8c8", "positive_moderate": "#fdbb84",
        "positive_high": "#e34a33",
    },
    "trajectory": {
        "undefined": "#bdbdbd", "not_applicable": "#d9d9d9",
        "low_support": "#969696", "zero": "#f7f7f7",
        "positive_low": "#c6dbef", "positive_moderate": "#6baed6",
        "positive_high": "#2171b5",
    },
}

SIGNED_PALETTE = {
    "replenishment_high": "#006d2c",
    "replenishment_moderate": "#31a354",
    "replenishment_low": "#a1d99b",
    "zero": "#f7f7f7",
    "consolidation_low": "#dadaeb",
    "consolidation_moderate": "#9e9ac8",
    "consolidation_high": "#54278f",
}

BALANCE_PALETTE = {
    "inactive": "#d9d9d9",
    "replenishment_dominant": "#238b45",
    "mixed": "#fddc6c",
    "consolidation_dominant": "#6a51a3",
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


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "not-recorded"


def normalize_identifier(value) -> str:
    if pd.isna(value):
        raise ValueError("Missing identifier encountered")
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    return str(value).strip()


def python_scalar(value):
    if isinstance(value, np.generic):
        return value.item()
    return value


def interval_label(t0: int, t1: int) -> str:
    return f"{int(t0)}_{int(t1)}"


def metric_palette(metric: str) -> dict[str, str]:
    if metric == "net_cr_balance_ha":
        return SIGNED_PALETTE
    if metric == "cr_balance_index":
        return BALANCE_PALETTE
    if "pas_any" in metric or "pas_consecutive2" in metric:
        return POSITIVE_PALETTES["trajectory"]
    if metric.startswith("consolidation"):
        return POSITIVE_PALETTES["consolidation"]
    if metric.startswith("replenishment"):
        return POSITIVE_PALETTES["replenishment"]
    return POSITIVE_PALETTES["nat_tmp"]


def measure_is_ratio(measure_type: str) -> bool:
    return measure_type in {"relative_intensity", "trajectory_share"}


def format_value(value: float, measure_type: str) -> str:
    if measure_is_ratio(measure_type):
        return f"{100.0 * value:.1f}%"
    if measure_type in {"absolute_area_ha", "trajectory_area_ha", "signed_area_ha"}:
        return f"{value:,.1f} ha"
    return f"{value:.3f}"


def legend_label(
    class_label: str,
    measure_type: str,
    break_1: float,
    break_2: float,
) -> str:
    if class_label == "undefined":
        return "Undefined denominator"
    if class_label == "not_applicable":
        return "No NAT-TMP endpoint"
    if class_label == "low_support":
        return "Low endpoint support (<=0.1% cell)"
    if class_label == "inactive":
        return "Inactive"
    if class_label == "zero":
        return "Zero"
    if class_label == "positive_low":
        return f">0 to {format_value(break_1, measure_type)}"
    if class_label == "positive_moderate":
        return (
            f">{format_value(break_1, measure_type)} to "
            f"{format_value(break_2, measure_type)}"
        )
    if class_label == "positive_high":
        return f">{format_value(break_2, measure_type)}"
    if class_label == "replenishment_high":
        return f"Replenishment >{format_value(break_2, measure_type)}"
    if class_label == "replenishment_moderate":
        return (
            f"Replenishment {format_value(break_1, measure_type)}-"
            f"{format_value(break_2, measure_type)}"
        )
    if class_label == "replenishment_low":
        return f"Replenishment >0-{format_value(break_1, measure_type)}"
    if class_label == "consolidation_low":
        return f"Consolidation >0-{format_value(break_1, measure_type)}"
    if class_label == "consolidation_moderate":
        return (
            f"Consolidation {format_value(break_1, measure_type)}-"
            f"{format_value(break_2, measure_type)}"
        )
    if class_label == "consolidation_high":
        return f"Consolidation >{format_value(break_2, measure_type)}"
    if class_label == "replenishment_dominant":
        return "Replenishment-dominant (<-1/3)"
    if class_label == "mixed":
        return "Mixed (-1/3 to 1/3)"
    if class_label == "consolidation_dominant":
        return "Consolidation-dominant (>1/3)"
    return class_label.replace("_", " ").title()


def classify_metric(frame: pd.DataFrame, limit: pd.Series) -> pd.Series:
    metric = str(limit["metric"])
    measure_type = str(limit["measure_type"])
    labels = json.loads(str(limit["class_labels"]))
    break_1 = float(limit["break_1"])
    break_2 = float(limit["break_2"])
    tolerance = float(limit["zero_tolerance"])
    values = pd.to_numeric(frame[metric], errors="coerce")

    if measure_type == "trajectory_share":
        mathematically_defined = frame["nat_tmp_endpoint_share_defined"].eq(1)
        minimum_support = (
            pd.to_numeric(frame["geometry_area_aea_ha"], errors="raise")
            * SHARE_MINIMUM_CELL_FRACTION
        )
        eligible = (
            mathematically_defined
            & pd.to_numeric(frame["nat_tmp_endpoint_ha"], errors="raise")
            .gt(minimum_support)
        )
        low_support = mathematically_defined & ~eligible
        classes = pd.Series("not_applicable", index=frame.index, dtype="object")
        classes.loc[low_support] = "low_support"
        classes.loc[eligible & values.le(tolerance)] = "zero"
        classes.loc[eligible & values.gt(tolerance) & values.le(break_1)] = (
            "positive_low"
        )
        classes.loc[eligible & values.gt(break_1) & values.le(break_2)] = (
            "positive_moderate"
        )
        classes.loc[eligible & values.gt(break_2)] = "positive_high"
    elif measure_type == "signed_area_ha":
        classes = pd.Series("zero", index=frame.index, dtype="object")
        classes.loc[values.lt(-break_2)] = "replenishment_high"
        classes.loc[values.ge(-break_2) & values.lt(-break_1)] = (
            "replenishment_moderate"
        )
        classes.loc[values.ge(-break_1) & values.lt(-tolerance)] = (
            "replenishment_low"
        )
        classes.loc[values.gt(tolerance) & values.le(break_1)] = (
            "consolidation_low"
        )
        classes.loc[values.gt(break_1) & values.le(break_2)] = (
            "consolidation_moderate"
        )
        classes.loc[values.gt(break_2)] = "consolidation_high"
    elif measure_type == "bounded_balance_index":
        classes = frame["cr_balance_state"].astype(str).copy()
    else:
        support_field = str(limit["support_field"])
        supported = (
            frame[metric].notna()
            if support_field == "all_rows"
            else frame[support_field].eq(1)
        )
        classes = pd.Series("undefined", index=frame.index, dtype="object")
        classes.loc[supported & values.le(tolerance)] = "zero"
        classes.loc[supported & values.gt(tolerance) & values.le(break_1)] = (
            "positive_low"
        )
        classes.loc[supported & values.gt(break_1) & values.le(break_2)] = (
            "positive_moderate"
        )
        classes.loc[supported & values.gt(break_2)] = "positive_high"

    require(set(classes.unique()).issubset(set(labels)),
            f"Unexpected class generated for {metric}")
    return classes


def draw_north_arrow(ax, bounds: tuple[float, float, float, float]) -> None:
    minx, miny, maxx, maxy = bounds
    width = maxx - minx
    height = maxy - miny
    x = minx + 0.055 * width
    y0 = miny + 0.80 * height
    y1 = miny + 0.91 * height
    ax.annotate(
        "N", xy=(x, y1), xytext=(x, y0), ha="center", va="bottom",
        fontsize=8, fontweight="bold",
        arrowprops={"arrowstyle": "-|>", "color": "#333333", "lw": 1.0},
    )


def draw_scale_bar(ax, bounds: tuple[float, float, float, float]) -> None:
    minx, miny, maxx, maxy = bounds
    width = maxx - minx
    height = maxy - miny
    length_m = 1_000_000.0
    x0 = minx + 0.055 * width
    y = miny + 0.055 * height
    ax.plot([x0, x0 + length_m], [y, y], color="#333333", lw=2.0)
    ax.plot([x0, x0], [y - 0.008 * height, y + 0.008 * height],
            color="#333333", lw=1.0)
    ax.plot([x0 + length_m, x0 + length_m],
            [y - 0.008 * height, y + 0.008 * height],
            color="#333333", lw=1.0)
    ax.text(x0 + length_m / 2, y + 0.018 * height, "1,000 km",
            ha="center", va="bottom", fontsize=7, color="#333333")


# -----------------------------------------------------------------------------
# 4. Authenticate and read inputs
# -----------------------------------------------------------------------------

print("CANONICAL COMPARABLE INTERVAL MAPS - PHASE 3B SCRIPT REVISION 3")
print("WGS84-TO-AEA REPROJECTION FIX: ENABLED")
print("FULL-PRECISION PHASE 3A LIMITS: ENABLED")
print("Script version:", SCRIPT_VERSION)
print("Project directory:", PROJECT_DIR)
print("Map output directory:", MAP_DIR)

required_inputs = [
    BIOME_INPUT,
    SPATIAL_SUPPORT_INPUT,
    SPATIAL_METRICS_INPUT,
    PHASE2_VALIDATION_INPUT,
    CLASS_LIMITS_INPUT,
    CLASS_COUNTS_INPUT,
    PHASE3A_VALIDATION_INPUT,
]
for path in required_inputs:
    require(path.exists(), f"Missing required input: {path}")

input_hashes = {path.name: sha256_file(path) for path in required_inputs}
for name, expected in EXPECTED_HASHES.items():
    require(
        input_hashes[name] == expected,
        f"Input SHA-256 mismatch for {name}: expected {expected}, "
        f"found {input_hashes[name]}",
    )

with PHASE2_VALIDATION_INPUT.open("r", encoding="utf-8") as source:
    phase2_validation = json.load(source)
with PHASE3A_VALIDATION_INPUT.open("r", encoding="utf-8") as source:
    phase3a_validation = json.load(source)

require(phase2_validation.get("validation_status") == "PASS",
        "Phase 2 validation status is not PASS")
require(all(phase2_validation.get("checks", {}).values()),
        "At least one Phase 2 check is false")
require(phase3a_validation.get("validation_status") == "PASS",
        "Phase 3A validation status is not PASS")
require(all(phase3a_validation.get("checks", {}).values()),
        "At least one Phase 3A check is false")
require(phase3a_validation.get("map_class_version") == MAP_CLASS_VERSION,
        "Unexpected Phase 3A map-class version")
require(phase3a_validation["scope"]["diagnostic_used_to_fit_limits"] is False,
        "Diagnostic interval contributed to class-limit fitting")
require(phase3a_validation["scope"]["maps_created"] is False,
        "Phase 3A unexpectedly records map creation")

panel = pd.read_parquet(SPATIAL_METRICS_INPUT)
spatial = gpd.read_parquet(SPATIAL_SUPPORT_INPUT)
biomes = gpd.read_file(BIOME_INPUT)
limits_csv = pd.read_csv(CLASS_LIMITS_INPUT, low_memory=False)
# Phase 3A stores the exact in-memory limits in its authenticated JSON. The
# CSV uses %.12g serialization and is therefore a human-readable rounded view.
# Exact boundary reproduction must use the JSON values because pooled medians
# and p90 values can coincide with observed cell values.
limits = pd.DataFrame(phase3a_validation["limits"])
accepted_counts = pd.read_csv(CLASS_COUNTS_INPUT, low_memory=False)

panel["cell_id"] = panel["cell_id"].map(normalize_identifier)
spatial["cell_id"] = spatial["cell_id"].map(normalize_identifier)
panel = panel.sort_values(KEY_COLUMNS).reset_index(drop=True)
spatial = spatial.sort_values("cell_id").reset_index(drop=True)


# -----------------------------------------------------------------------------
# 5. Structural, spatial, and class-input validation
# -----------------------------------------------------------------------------

require(panel.shape == (EXPECTED_ROWS, EXPECTED_PHASE2_COLUMNS),
        f"Unexpected Phase 2 panel shape: {panel.shape}")
require(panel.duplicated(KEY_COLUMNS).sum() == 0, "Duplicate panel keys")
require(panel["cell_id"].nunique() == EXPECTED_CELLS,
        "Unexpected distinct panel cells")
require(panel.groupby(["t0", "t1"]).size().eq(EXPECTED_CELLS).all(),
        "At least one interval is incomplete")
observed_intervals = sorted(
    (int(row.t0), int(row.t1))
    for row in panel[["t0", "t1"]].drop_duplicates().itertuples()
)
require(observed_intervals == INTERVALS, "Unexpected interval sequence")

require(len(spatial) == EXPECTED_CELLS, "Unexpected spatial-support rows")
require(spatial["cell_id"].nunique() == EXPECTED_CELLS,
        "Duplicate spatial-support cell_id")
require(set(spatial["cell_id"]) == set(panel["cell_id"]),
        "Panel and spatial-support cell populations differ")
require(spatial.crs is not None, "Spatial-support CRS is missing")
print("Stored spatial-support CRS:", spatial.crs)
require(spatial.crs.to_epsg() == 4326,
        f"Unexpected stored spatial-support CRS: {spatial.crs}")
require(spatial.geometry.notna().all(), "Missing map geometry")
require(spatial.geometry.is_valid.all(), "Invalid map geometry")
require(spatial.geom_type.isin(["Polygon", "MultiPolygon"]).all(),
        "Unexpected map geometry type")

# Phase 1 deliberately stores the canonical geometry in EPSG:4326. Reproject
# here to exactly the same custom Albers equal-area CRS used to derive its AEA
# area fields. Raster processing CRS and cartographic CRS remain distinct.
source_geometry_crs = spatial.crs.to_string()
spatial = spatial.to_crs(AEA_CRS)
print("Internal cartographic CRS is projected:", spatial.crs.is_projected)
require(spatial.crs.is_projected,
        "Internal cartographic geometry was not projected")
require(spatial.geometry.is_valid.all(),
        "Invalid geometry after AEA reprojection")

calculated_area_ha = spatial.geometry.area / 10_000.0
stored_area_ha = pd.to_numeric(spatial["geometry_area_aea_ha"], errors="raise")
maximum_internal_area_difference_ha = float(
    (calculated_area_ha - stored_area_ha).abs().max()
)
maximum_aea_vs_geodesic_relative_difference = float(
    pd.to_numeric(
        spatial["area_aea_vs_gee_relative_difference"], errors="raise"
    ).abs().max()
)
require(maximum_internal_area_difference_ha <= 1e-6,
        "Mapped geometry area differs from stored AEA area")
require(maximum_aea_vs_geodesic_relative_difference <= AREA_RECONCILIATION_TOLERANCE,
        "AEA-versus-geodesic area difference exceeds tolerance")

require(len(limits) == EXPECTED_METRICS, "Unexpected class-limit rows")
require(len(limits_csv) == EXPECTED_METRICS,
        "Unexpected class-limit CSV rows")
require(limits["metric"].is_unique, "Duplicate class-limit metric")
require(limits_csv["metric"].is_unique,
        "Duplicate class-limit metric in CSV")
require(limits["metric"].tolist() == METRIC_ORDER,
        "Class-limit metric order differs from the canonical order")
require(limits_csv["metric"].tolist() == METRIC_ORDER,
        "Class-limit CSV metric order differs from the canonical order")
require(set(limits["map_class_version"].astype(str)) == {MAP_CLASS_VERSION},
        "Unexpected map-class version in class limits")
require(set(limits_csv["map_class_version"].astype(str)) == {MAP_CLASS_VERSION},
        "Unexpected map-class version in class-limit CSV")
require(limits["diagnostic_used_to_fit_limits"].eq(0).all(),
        "At least one limit used the diagnostic interval")

exact_identity_fields = [
    "metric", "metric_label", "measure_type", "denominator",
    "classification_method", "threshold_source", "break_1_definition",
    "break_2_definition", "quantile_method", "class_labels",
    "map_class_version",
]
for field in exact_identity_fields:
    require(
        limits[field].astype(str).eq(limits_csv[field].astype(str)).all(),
        f"Class-limit CSV and validation JSON differ in {field}",
    )

exact_count_fields = [
    "diagnostic_used_to_fit_limits", "source_defined_count",
    "source_undefined_count", "source_low_support_count",
    "source_classification_eligible_count", "source_zero_count",
    "source_nonzero_count",
]
for field in exact_count_fields:
    require(
        pd.to_numeric(limits[field], errors="raise").eq(
            pd.to_numeric(limits_csv[field], errors="raise")
        ).all(),
        f"Class-limit CSV and validation JSON differ in {field}",
    )

for field in ["break_1", "break_2", "zero_tolerance"]:
    require(
        np.allclose(
            pd.to_numeric(limits[field], errors="raise"),
            pd.to_numeric(limits_csv[field], errors="raise"),
            rtol=1e-10,
            atol=1e-12,
        ),
        f"Class-limit CSV differs materially from validation JSON in {field}",
    )
require(len(accepted_counts) == EXPECTED_CLASS_COUNT_ROWS,
        "Unexpected accepted class-count rows")
require(set(accepted_counts["metric"]) == set(METRIC_ORDER),
        "Accepted class-count metrics differ")

required_metric_fields = set(METRIC_ORDER) | {
    "cell_id", "t0", "t1", "interval", "diagnostic_interval",
    "geometry_area_aea_ha", "nat_tmp_endpoint_ha",
    "nat_tmp_endpoint_share_defined", "cr_balance_state",
    "consolidation_rate_defined", "replenishment_rate_defined",
    "nat_tmp_intensity_defined",
}
require(required_metric_fields.issubset(panel.columns),
        f"Missing map fields: {sorted(required_metric_fields - set(panel.columns))}")

biomes_aea = biomes.to_crs(spatial.crs)
require(len(biomes_aea) == 2, "Expected two target-biome geometries")


# -----------------------------------------------------------------------------
# 6. Reproduce all frozen classes and verify Phase 3A counts
# -----------------------------------------------------------------------------

classified = panel[["cell_id", "t0", "t1", "interval",
                    "diagnostic_interval"]].copy()
render_count_rows = []
legend_rows = []

for metric in METRIC_ORDER:
    limit = limits.loc[limits["metric"].eq(metric)].iloc[0]
    classes = classify_metric(panel, limit)
    labels = json.loads(str(limit["class_labels"]))
    code_lookup = {label: order for order, label in enumerate(labels)}
    classified[f"{metric}__class"] = classes
    classified[f"{metric}__code"] = classes.map(code_lookup).astype("int8")

    for (t0, t1), group_index in panel.groupby(["t0", "t1"], sort=True).groups.items():
        interval_classes = classes.loc[group_index]
        counts = interval_classes.value_counts().to_dict()
        for order, label in enumerate(labels):
            render_count_rows.append(
                {
                    "metric": metric,
                    "t0": int(t0),
                    "t1": int(t1),
                    "interval": interval_label(t0, t1),
                    "diagnostic_interval": int((int(t0), int(t1)) == DIAGNOSTIC_INTERVAL),
                    "class_order": order,
                    "class_label": label,
                    "cell_count": int(counts.get(label, 0)),
                    "map_class_version": MAP_CLASS_VERSION,
                    "map_product_version": OUTPUT_VERSION,
                }
            )

    palette = metric_palette(metric)
    for order, label in enumerate(labels):
        require(label in palette, f"Missing color for {metric}: {label}")
        legend_rows.append(
            {
                "metric": metric,
                "metric_label": METRIC_LABELS[metric],
                "measure_type": str(limit["measure_type"]),
                "class_order": order,
                "class_label": label,
                "legend_label": legend_label(
                    label,
                    str(limit["measure_type"]),
                    float(limit["break_1"]),
                    float(limit["break_2"]),
                ),
                "color_hex": palette[label],
                "break_1": float(limit["break_1"]),
                "break_2": float(limit["break_2"]),
                "map_class_version": MAP_CLASS_VERSION,
                "map_product_version": OUTPUT_VERSION,
            }
        )

render_counts = pd.DataFrame(render_count_rows).sort_values(
    ["metric", "t0", "t1", "class_order"]
).reset_index(drop=True)
legend = pd.DataFrame(legend_rows).sort_values(
    ["metric", "class_order"]
).reset_index(drop=True)

require(render_counts.groupby(["metric", "t0", "t1"])["cell_count"]
        .sum().eq(EXPECTED_CELLS).all(),
        "At least one rendered class population does not close")

comparison_columns = [
    "metric", "t0", "t1", "class_order", "class_label", "cell_count"
]
left = render_counts[comparison_columns].sort_values(comparison_columns[:-1])
right = accepted_counts[comparison_columns].sort_values(comparison_columns[:-1])
comparison = left.merge(
    right,
    on=comparison_columns[:-1],
    how="outer",
    suffixes=("_rendered", "_accepted"),
    indicator=True,
)
require(comparison["_merge"].eq("both").all(),
        "Rendered and accepted class rows differ")
require(comparison["cell_count_rendered"].eq(
            comparison["cell_count_accepted"]).all(),
        "Rendered class counts differ from final Phase 3A counts")

classified["map_class_version"] = MAP_CLASS_VERSION
classified["map_product_version"] = OUTPUT_VERSION


# -----------------------------------------------------------------------------
# 7. Write classified data and legends before rendering
# -----------------------------------------------------------------------------

classified.to_parquet(CLASSIFIED_PANEL_OUTPUT, index=False, compression="zstd")
legend.to_csv(LEGEND_OUTPUT, index=False, float_format="%.12g")
render_counts.to_csv(RENDER_COUNTS_OUTPUT, index=False)


# -----------------------------------------------------------------------------
# 8. Render 12 comparable eight-panel map series
# -----------------------------------------------------------------------------

bounds = tuple(float(value) for value in spatial.total_bounds)
minx, miny, maxx, maxy = bounds
padding_x = 0.015 * (maxx - minx)
padding_y = 0.015 * (maxy - miny)
plot_bounds = (
    minx - padding_x, miny - padding_y,
    maxx + padding_x, maxy + padding_y,
)

inventory_rows = []
spatial_index = spatial.set_index("cell_id", drop=False)

for sequence, metric in enumerate(METRIC_ORDER, start=1):
    print(f"Rendering map {sequence:02d}/{EXPECTED_METRICS}: {metric}")
    limit = limits.loc[limits["metric"].eq(metric)].iloc[0]
    labels = json.loads(str(limit["class_labels"]))
    palette = metric_palette(metric)
    metric_legend = legend.loc[legend["metric"].eq(metric)].copy()

    fig, axes = plt.subplots(2, 4, figsize=(18, 10), facecolor="white")
    for ax, (t0, t1) in zip(axes.flat, INTERVALS):
        interval_rows = classified.loc[
            classified["t0"].eq(t0) & classified["t1"].eq(t1),
            ["cell_id", f"{metric}__class"],
        ].set_index("cell_id")
        require(len(interval_rows) == EXPECTED_CELLS,
                f"Incomplete map interval for {metric}, {t0}-{t1}")
        ordered_classes = interval_rows.loc[spatial_index.index,
                                            f"{metric}__class"]
        colors = ordered_classes.map(palette)
        require(colors.notna().all(), f"Unmapped color in {metric}, {t0}-{t1}")

        spatial_index.plot(
            ax=ax,
            color=colors.to_numpy(),
            edgecolor="none",
            linewidth=0,
            rasterized=True,
        )
        biomes_aea.boundary.plot(ax=ax, color="#262626", linewidth=0.35,
                                 alpha=0.85, zorder=3)
        ax.set_xlim(plot_bounds[0], plot_bounds[2])
        ax.set_ylim(plot_bounds[1], plot_bounds[3])
        ax.set_aspect("equal")
        ax.set_axis_off()
        is_diagnostic = (t0, t1) == DIAGNOSTIC_INTERVAL
        title = f"{t0}-{t1}" + (" (diagnostic)" if is_diagnostic else "")
        ax.set_title(
            title,
            fontsize=10,
            fontweight="bold" if is_diagnostic else "normal",
            color="#b2182b" if is_diagnostic else "#222222",
            pad=4,
        )
        if (t0, t1) == INTERVALS[0]:
            draw_north_arrow(ax, plot_bounds)
            draw_scale_bar(ax, plot_bounds)

    handles = [
        Patch(
            facecolor=row.color_hex,
            edgecolor="#777777",
            linewidth=0.3,
            label=row.legend_label,
        )
        for row in metric_legend.itertuples(index=False)
    ]
    fig.suptitle(METRIC_LABELS[metric], fontsize=16, fontweight="bold", y=0.975)
    fig.text(
        0.5,
        0.945,
        "Fixed classes fitted from pooled primary intervals, 1985-2020",
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.018),
        ncol=min(len(handles), 7),
        frameon=False,
        fontsize=8,
        handlelength=1.6,
        columnspacing=1.2,
    )
    fig.text(
        0.99, 0.008,
        "MapBiomas Brazil Collection 11 | canonical ~20,000 ha hexagonal grid",
        ha="right", va="bottom", fontsize=7, color="#666666",
    )
    fig.tight_layout(rect=(0.01, 0.075, 0.99, 0.925), w_pad=0.2, h_pad=0.8)

    stem = f"map{sequence:02d}_{metric}_comparable_intervals_v1"
    png_path = PNG_DIR / f"{stem}.png"
    svg_path = SVG_DIR / f"{stem}.svg"
    fig.savefig(png_path, dpi=PNG_DPI, bbox_inches="tight", facecolor="white")
    fig.savefig(svg_path, dpi=PNG_DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    require(png_path.exists() and png_path.stat().st_size > 0,
            f"PNG was not created: {png_path}")
    require(svg_path.exists() and svg_path.stat().st_size > 0,
            f"SVG was not created: {svg_path}")
    with Image.open(png_path) as image:
        png_width, png_height = image.size
        require(png_width >= 3000 and png_height >= 1500,
                f"Unexpectedly small PNG dimensions: {image.size}")
    ET.parse(svg_path)

    inventory_rows.append(
        {
            "map_order": sequence,
            "metric": metric,
            "metric_label": METRIC_LABELS[metric],
            "measure_type": str(limit["measure_type"]),
            "primary_interval_count": 7,
            "diagnostic_interval_count": 1,
            "diagnostic_interval": "2020_2025",
            "class_limit_numeric_source": PHASE3A_VALIDATION_INPUT.name,
            "class_limit_tabular_record": CLASS_LIMITS_INPUT.name,
            "map_class_version": MAP_CLASS_VERSION,
            "map_product_version": OUTPUT_VERSION,
            "png_relative_path": str(png_path.relative_to(PHASE3_DIR)),
            "png_sha256": sha256_file(png_path),
            "png_width_pixels": png_width,
            "png_height_pixels": png_height,
            "svg_relative_path": str(svg_path.relative_to(PHASE3_DIR)),
            "svg_sha256": sha256_file(svg_path),
        }
    )

inventory = pd.DataFrame(inventory_rows).sort_values("map_order").reset_index(drop=True)
inventory.to_csv(MAP_INVENTORY_OUTPUT, index=False)


# -----------------------------------------------------------------------------
# 9. Final output authentication and validation record
# -----------------------------------------------------------------------------

tabular_outputs = [
    CLASSIFIED_PANEL_OUTPUT,
    LEGEND_OUTPUT,
    RENDER_COUNTS_OUTPUT,
    MAP_INVENTORY_OUTPUT,
]
output_hashes = {
    path.name: {"path": str(path), "sha256": sha256_file(path)}
    for path in tabular_outputs
}

map_hashes = {}
for row in inventory.itertuples(index=False):
    map_hashes[row.metric] = {
        "png": {
            "path": str(PHASE3_DIR / row.png_relative_path),
            "sha256": row.png_sha256,
        },
        "svg": {
            "path": str(PHASE3_DIR / row.svg_relative_path),
            "sha256": row.svg_sha256,
        },
    }

validation = {
    "validation_status": "PASS",
    "map_product_version": OUTPUT_VERSION,
    "script_version": SCRIPT_VERSION,
    "map_class_version": MAP_CLASS_VERSION,
    "scope": {
        "metrics_mapped": EXPECTED_METRICS,
        "intervals_per_metric": EXPECTED_INTERVALS,
        "primary_intervals": [interval_label(*item) for item in INTERVALS[:-1]],
        "diagnostic_interval": interval_label(*DIAGNOSTIC_INTERVAL),
        "diagnostic_used_to_fit_limits": False,
        "class_limits_recalculated": False,
        "class_limit_numeric_source": PHASE3A_VALIDATION_INPUT.name,
        "class_limit_csv_role": "authenticated_rounded_tabular_record",
        "gee_processing_required": False,
    },
    "inputs": {
        path.name: {"path": str(path), "sha256": input_hashes[path.name]}
        for path in required_inputs
    },
    "structure": {
        "panel_rows": len(panel),
        "cells": panel["cell_id"].nunique(),
        "intervals": panel["interval"].nunique(),
        "metrics": len(METRIC_ORDER),
        "class_limit_rows": len(limits),
        "accepted_class_count_rows": len(accepted_counts),
        "reproduced_class_count_rows": len(render_counts),
        "classified_panel_columns": len(classified.columns),
        "legend_rows": len(legend),
        "png_maps": len(inventory),
        "svg_maps": len(inventory),
    },
    "cartography": {
        "stored_geometry_crs": source_geometry_crs,
        "crs_wkt": spatial.crs.to_wkt(),
        "crs_proj_string": spatial.crs.to_string(),
        "polygon_layers_rasterized_in_svg": True,
        "png_dpi": PNG_DPI,
        "maximum_geometry_vs_stored_aea_area_difference_ha": (
            maximum_internal_area_difference_ha
        ),
        "maximum_aea_vs_geodesic_relative_area_difference": (
            maximum_aea_vs_geodesic_relative_difference
        ),
        "area_reconciliation_tolerance": AREA_RECONCILIATION_TOLERANCE,
    },
    "outputs": output_hashes,
    "maps": map_hashes,
    "software": {
        "python": sys.version,
        "pandas": package_version("pandas"),
        "numpy": package_version("numpy"),
        "geopandas": package_version("geopandas"),
        "shapely": package_version("shapely"),
        "pyproj": package_version("pyproj"),
        "matplotlib": package_version("matplotlib"),
        "pyarrow": package_version("pyarrow"),
        "pillow": package_version("pillow"),
    },
    "checks": {
        "all_input_hashes_match": True,
        "phase2_validation_passed": True,
        "phase3a_validation_passed": True,
        "phase3a_v2_limits_authenticated": True,
        "csv_limits_match_exact_json_within_serialization_precision": True,
        "balanced_unique_panel": True,
        "spatial_and_panel_cell_populations_match": True,
        "projected_aea_geometry_valid": True,
        "aea_area_reconciliation_passes": True,
        "one_frozen_limit_record_per_metric": True,
        "diagnostic_interval_excluded_from_limit_fitting": True,
        "no_class_limits_recalculated": True,
        "all_frozen_classes_reproduced": True,
        "all_metric_interval_populations_close": True,
        "rendered_counts_match_phase3a_exactly": True,
        "all_class_labels_have_fixed_colors": True,
        "all_png_maps_created_and_readable": True,
        "all_svg_maps_created_and_parseable": True,
        "map_inventory_complete": True,
    },
}

with VALIDATION_OUTPUT.open("w", encoding="utf-8") as destination:
    json.dump(validation, destination, indent=2, ensure_ascii=False,
              default=python_scalar)

print()
print("PHASE 3B COMPARABLE MAP BUILD COMPLETE")
print("Validation status: PASS")
print("Rows classified:", f"{len(classified):,}")
print("Cells:", f"{panel['cell_id'].nunique():,}")
print("Intervals:", panel["interval"].nunique())
print("Metrics mapped:", len(inventory))
print("PNG maps:", len(inventory))
print("SVG maps:", len(inventory))
print("Class-count agreement with Phase 3A: EXACT")
print("Class limits recalculated: NO")
print("Exact class-limit source:", PHASE3A_VALIDATION_INPUT.name)
print("Diagnostic interval used to fit limits: NO")
print(
    "Maximum AEA-versus-geodesic relative area difference:",
    maximum_aea_vs_geodesic_relative_difference,
)
print("Classified panel:", CLASSIFIED_PANEL_OUTPUT)
print("Legend:", LEGEND_OUTPUT)
print("Map inventory:", MAP_INVENTORY_OUTPUT)
print("Validation record:", VALIDATION_OUTPUT)
print("Map directory:", MAP_DIR)

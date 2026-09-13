"""
Build and validate the Phase 1 canonical spatial-support table and fixed
edge-contiguity graph.

Designed for Google Colab. Place the two Phase 1A GeoJSON files in:
MyDrive/Trabalho/Contabilidade/spatial/inputs

The canonical integrated analytical panel must remain in the existing
MyDrive/Trabalho/Contabilidade/analysis directory. Source files are read only.
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


# -----------------------------------------------------------------------------
# 0. Colab dependencies
# -----------------------------------------------------------------------------

REQUIRED_PACKAGES = {
    "geopandas": "geopandas>=0.14,<2",
    "shapely": "shapely>=2,<3",
    "pyproj": "pyproj>=3.6,<4",
    "pyarrow": "pyarrow>=14",
    "networkx": "networkx>=3,<4",
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
        or (module == "networkx" and version_tuple("networkx") < (3, 0))
    )
    if not installed or too_old:
        missing_packages.append(requirement)

if missing_packages:
    print("Installing missing spatial dependencies:", missing_packages)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *missing_packages]
    )

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import pyproj
import shapely
from pyproj import Geod
from shapely.ops import unary_union

try:
    from google.colab import drive
except ImportError:
    drive = None


# -----------------------------------------------------------------------------
# 1. Canonical configuration
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
OUTPUT_DIR = PROJECT_DIR / "spatial" / "phase1"
ANALYSIS_DIR = PROJECT_DIR / "analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRID_INPUT = INPUT_DIR / "canonical_spatial_grid_input_v1.geojson"
BIOME_INPUT = INPUT_DIR / "canonical_biomes_input_ibge2025_v1.geojson"
PANEL_INPUT = (
    ANALYSIS_DIR
    / "canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet"
)

SPATIAL_SUPPORT_OUTPUT = OUTPUT_DIR / "canonical_spatial_support_v1.parquet"
SPATIAL_ATTRIBUTES_OUTPUT = (
    OUTPUT_DIR / "canonical_spatial_support_attributes_v1.csv"
)
WEIGHTS_OUTPUT = OUTPUT_DIR / "canonical_contiguity_weights_v1.parquet"
BIOME_SUMMARY_OUTPUT = OUTPUT_DIR / "canonical_biome_assignment_summary_v1.csv"
NEIGHBOR_SUMMARY_OUTPUT = (
    OUTPUT_DIR / "canonical_neighbor_count_distribution_v1.csv"
)
COMPONENT_SUMMARY_OUTPUT = (
    OUTPUT_DIR / "canonical_connected_components_v1.csv"
)
SUMMARY_OUTPUT = OUTPUT_DIR / "canonical_spatial_support_summary_v1.csv"
VALIDATION_OUTPUT = OUTPUT_DIR / "canonical_spatial_support_validation_v1.json"

EXPECTED_GRID_SHA256 = (
    "c3ce310bc474a05f168a2e7ce5b7644026630038c68457ff5948304d0ce1950f"
)
EXPECTED_BIOME_SHA256 = (
    "1f3dfccef176e4de5b64405cc5dacf2c098805e99e2ac4449352b9fb307a38a6"
)
EXPECTED_PANEL_SHA256 = (
    "7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28"
)

EXPECTED_CELLS = 24_889
EXPECTED_BIOME_CODES = {"1", "3"}
EXPECTED_SOURCE_VERSION = "canonical-spatial-input-export-v1"
OUTPUT_VERSION = "canonical-spatial-support-v1"
GRAPH_VERSION = "canonical-edge-contiguity-v1"

WGS84_CRS = "EPSG:4326"
AEA_CRS = (
    "+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 "
    "+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"
)

AREA_RELATIVE_TOLERANCE = 0.005
BIOME_AREA_TOLERANCE_HA = 0.01
POSITIVE_OVERLAP_TOLERANCE_HA = 1e-6
SHARED_EDGE_TOLERANCE_M = 1.0
GRID_OVERLAP_TOLERANCE_M2 = 1.0
ROW_WEIGHT_TOLERANCE = 1e-12


# -----------------------------------------------------------------------------
# 2. Helpers
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


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "not-recorded"


def candidate_pairs(gdf: gpd.GeoDataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Return unique geometry-index pairs whose geometries intersect."""
    left = gpd.GeoDataFrame(
        {
            "left_index": np.arange(len(gdf), dtype=np.int64),
        },
        geometry=gdf.geometry,
        crs=gdf.crs,
    )
    right = gpd.GeoDataFrame(
        {
            "right_index": np.arange(len(gdf), dtype=np.int64),
        },
        geometry=gdf.geometry,
        crs=gdf.crs,
    )
    joined = gpd.sjoin(left, right, how="inner", predicate="intersects")
    i = joined["left_index"].to_numpy(dtype=np.int64)
    j = joined["right_index"].to_numpy(dtype=np.int64)
    keep = i < j
    pairs = np.column_stack([i[keep], j[keep]])
    if len(pairs) == 0:
        return np.array([], dtype=np.int64), np.array([], dtype=np.int64)
    pairs = np.unique(pairs, axis=0)
    return pairs[:, 0], pairs[:, 1]


def dataframe_hashes(paths: list[Path]) -> dict:
    return {path.name: sha256_file(path) for path in paths}


# -----------------------------------------------------------------------------
# 3. Input identity and structural validation
# -----------------------------------------------------------------------------

print("CANONICAL SPATIAL SUPPORT AND CONTIGUITY - PHASE 1 VERSION 1")
print("Input directory:", INPUT_DIR)
print("Output directory:", OUTPUT_DIR)

for path in [GRID_INPUT, BIOME_INPUT, PANEL_INPUT]:
    require(path.exists(), f"Required input not found: {path}")

input_hashes = {
    "grid_geojson": sha256_file(GRID_INPUT),
    "biome_geojson": sha256_file(BIOME_INPUT),
    "integrated_panel": sha256_file(PANEL_INPUT),
}

require(
    input_hashes["grid_geojson"] == EXPECTED_GRID_SHA256,
    "Grid GeoJSON SHA-256 does not match the accepted Phase 1A export.",
)
require(
    input_hashes["biome_geojson"] == EXPECTED_BIOME_SHA256,
    "Biome GeoJSON SHA-256 does not match the accepted Phase 1A export.",
)
require(
    input_hashes["integrated_panel"] == EXPECTED_PANEL_SHA256,
    "Integrated-panel SHA-256 does not match the canonical panel.",
)

grid = gpd.read_file(GRID_INPUT)
biomes = gpd.read_file(BIOME_INPUT)

require(len(grid) == EXPECTED_CELLS, f"Unexpected grid count: {len(grid)}")
require(grid.crs is not None, "Grid CRS is missing")
require(biomes.crs is not None, "Biome CRS is missing")
require(grid.crs.to_epsg() == 4326, f"Unexpected grid CRS: {grid.crs}")
require(biomes.crs.to_epsg() == 4326, f"Unexpected biome CRS: {biomes.crs}")

required_grid_columns = {
    "cell_id",
    "GRID_ID",
    "source_batch_id",
    "canonical_member",
    "domain_version",
    "geometry_type_gee",
    "geometry_area_geodesic_ha",
    "centroid_lon_gee",
    "centroid_lat_gee",
    "spatial_input_version",
    "geometry",
}
required_biome_columns = {"biome_code", "biome_name", "geometry"}

require(
    required_grid_columns.issubset(grid.columns),
    f"Grid fields missing: {sorted(required_grid_columns - set(grid.columns))}",
)
require(
    required_biome_columns.issubset(biomes.columns),
    f"Biome fields missing: {sorted(required_biome_columns - set(biomes.columns))}",
)

grid["cell_id"] = grid["cell_id"].map(normalize_identifier)
grid["GRID_ID"] = grid["GRID_ID"].map(normalize_identifier)
biomes["biome_code"] = biomes["biome_code"].map(normalize_identifier)

require(grid["cell_id"].nunique() == EXPECTED_CELLS, "cell_id is not unique")
require(grid["GRID_ID"].nunique() == EXPECTED_CELLS, "GRID_ID is not unique")
require(set(biomes["biome_code"]) == EXPECTED_BIOME_CODES, "Unexpected biomes")
require(len(biomes) == 2, f"Expected two biome features; found {len(biomes)}")
require(grid.geometry.notna().all(), "Missing grid geometries found")
require((~grid.geometry.is_empty).all(), "Empty grid geometries found")
require(grid.geometry.is_valid.all(), "Invalid grid geometries found")
require(biomes.geometry.notna().all(), "Missing biome geometries found")
require((~biomes.geometry.is_empty).all(), "Empty biome geometries found")
require(biomes.geometry.is_valid.all(), "Invalid biome geometries found")
require(set(grid.geom_type) == {"Polygon"}, "Grid must contain polygons only")
require(
    set(grid["spatial_input_version"].astype(str)) == {EXPECTED_SOURCE_VERSION},
    "Unexpected spatial input version",
)
require((pd.to_numeric(grid["canonical_member"]) == 1).all(), "Nonmember cell found")

panel_ids = pd.read_parquet(PANEL_INPUT, columns=["cell_id"])["cell_id"]
panel_ids = panel_ids.map(normalize_identifier)
panel_unique_ids = set(panel_ids.unique())
grid_id_set = set(grid["cell_id"])
require(len(panel_unique_ids) == EXPECTED_CELLS, "Unexpected panel cell population")
require(grid_id_set == panel_unique_ids, "Grid and panel cell populations differ")


# -----------------------------------------------------------------------------
# 4. Equal-area geometry, centroids, and biome overlap
# -----------------------------------------------------------------------------

grid = grid.sort_values("cell_id").reset_index(drop=True)
grid_aea = grid.to_crs(AEA_CRS)
biomes_aea = biomes.to_crs(AEA_CRS)

grid["geometry_area_aea_ha"] = grid_aea.geometry.area.to_numpy() / 10000.0
grid["geometry_area_geodesic_ha"] = pd.to_numeric(
    grid["geometry_area_geodesic_ha"], errors="raise"
)
grid["area_aea_vs_gee_relative_difference"] = (
    grid["geometry_area_aea_ha"] - grid["geometry_area_geodesic_ha"]
).abs() / grid["geometry_area_geodesic_ha"]

maximum_area_relative_difference = float(
    grid["area_aea_vs_gee_relative_difference"].max()
)
require(
    maximum_area_relative_difference <= AREA_RELATIVE_TOLERANCE,
    "Equal-area and GEE geodesic cell areas differ above tolerance: "
    f"{maximum_area_relative_difference}",
)

centroids_aea = grid_aea.geometry.centroid
centroids_wgs84 = gpd.GeoSeries(centroids_aea, crs=AEA_CRS).to_crs(WGS84_CRS)
grid["centroid_lon_aea"] = centroids_wgs84.x.to_numpy()
grid["centroid_lat_aea"] = centroids_wgs84.y.to_numpy()

geod = Geod(ellps="GRS80")
_, _, centroid_distance_m = geod.inv(
    pd.to_numeric(grid["centroid_lon_gee"]).to_numpy(),
    pd.to_numeric(grid["centroid_lat_gee"]).to_numpy(),
    grid["centroid_lon_aea"].to_numpy(),
    grid["centroid_lat_aea"].to_numpy(),
)
grid["centroid_method_distance_m"] = np.asarray(centroid_distance_m)
grid["aea_centroid_within_cell"] = grid_aea.geometry.covers(centroids_aea).to_numpy()
require(grid["aea_centroid_within_cell"].all(), "A centroid falls outside its cell")

biome_intersections = gpd.overlay(
    grid_aea[["cell_id", "geometry"]],
    biomes_aea[["biome_code", "geometry"]],
    how="intersection",
    keep_geom_type=False,
    make_valid=False,
)
biome_intersections["overlap_ha"] = biome_intersections.geometry.area / 10000.0

overlap_table = (
    biome_intersections.groupby(["cell_id", "biome_code"], as_index=False)[
        "overlap_ha"
    ]
    .sum()
    .pivot(index="cell_id", columns="biome_code", values="overlap_ha")
    .fillna(0.0)
)
overlap_table = overlap_table.reindex(grid["cell_id"], fill_value=0.0)
overlap_table = overlap_table.reindex(columns=["1", "3"], fill_value=0.0)

grid["amazon_overlap_ha"] = overlap_table["1"].to_numpy()
grid["cerrado_overlap_ha"] = overlap_table["3"].to_numpy()
grid["target_biome_overlap_ha"] = (
    grid["amazon_overlap_ha"] + grid["cerrado_overlap_ha"]
)
grid["biome_overlap_excess_ha"] = np.maximum(
    grid["target_biome_overlap_ha"] - grid["geometry_area_aea_ha"], 0.0
)

maximum_biome_excess_ha = float(grid["biome_overlap_excess_ha"].max())
require(
    maximum_biome_excess_ha <= BIOME_AREA_TOLERANCE_HA,
    "Amazon and Cerrado overlap areas exceed cell area above tolerance: "
    f"{maximum_biome_excess_ha} ha",
)
require(
    (grid["target_biome_overlap_ha"] > POSITIVE_OVERLAP_TOLERANCE_HA).all(),
    "A canonical cell has no positive target-biome overlap",
)

grid["amazon_fraction_cell"] = (
    grid["amazon_overlap_ha"] / grid["geometry_area_aea_ha"]
)
grid["cerrado_fraction_cell"] = (
    grid["cerrado_overlap_ha"] / grid["geometry_area_aea_ha"]
)
grid["target_biome_fraction_cell"] = (
    grid["target_biome_overlap_ha"] / grid["geometry_area_aea_ha"]
)
grid["outside_target_biomes_ha"] = np.maximum(
    grid["geometry_area_aea_ha"] - grid["target_biome_overlap_ha"], 0.0
)
grid["outside_target_biomes_fraction"] = (
    grid["outside_target_biomes_ha"] / grid["geometry_area_aea_ha"]
)

amazon_larger = grid["amazon_overlap_ha"] > grid["cerrado_overlap_ha"]
cerrado_larger = grid["cerrado_overlap_ha"] > grid["amazon_overlap_ha"]
grid["primary_biome"] = np.select(
    [amazon_larger, cerrado_larger], ["Amazon", "Cerrado"], default="Tie"
)
grid["primary_biome_code"] = np.select(
    [amazon_larger, cerrado_larger], ["1", "3"], default="tie"
)
grid["primary_biome_overlap_ha"] = np.maximum(
    grid["amazon_overlap_ha"], grid["cerrado_overlap_ha"]
)
grid["primary_biome_fraction_cell"] = (
    grid["primary_biome_overlap_ha"] / grid["geometry_area_aea_ha"]
)
grid["primary_biome_fraction_target_overlap"] = (
    grid["primary_biome_overlap_ha"] / grid["target_biome_overlap_ha"]
)
grid["crosses_amazon_cerrado_boundary"] = (
    (grid["amazon_overlap_ha"] > POSITIVE_OVERLAP_TOLERANCE_HA)
    & (grid["cerrado_overlap_ha"] > POSITIVE_OVERLAP_TOLERANCE_HA)
)
grid["extends_outside_target_biomes"] = (
    grid["outside_target_biomes_ha"] > BIOME_AREA_TOLERANCE_HA
)


# -----------------------------------------------------------------------------
# 5. Fixed shared-edge contiguity graph
# -----------------------------------------------------------------------------

i, j = candidate_pairs(grid_aea)
geometry_array = np.asarray(grid_aea.geometry.array, dtype=object)
left_geometry = geometry_array[i]
right_geometry = geometry_array[j]

pair_intersections = shapely.intersection(left_geometry, right_geometry)
pair_overlap_m2 = np.asarray(shapely.area(pair_intersections), dtype=float)
maximum_grid_overlap_m2 = float(pair_overlap_m2.max(initial=0.0))
require(
    maximum_grid_overlap_m2 <= GRID_OVERLAP_TOLERANCE_M2,
    f"Grid-cell overlap exceeds tolerance: {maximum_grid_overlap_m2} m2",
)

shared_boundary_m = np.asarray(
    shapely.length(
        shapely.intersection(
            shapely.boundary(left_geometry),
            shapely.boundary(right_geometry),
        )
    ),
    dtype=float,
)

edge_keep = shared_boundary_m > SHARED_EDGE_TOLERANCE_M
edge_i = i[edge_keep]
edge_j = j[edge_keep]
edge_length = shared_boundary_m[edge_keep]

cell_ids = grid["cell_id"].to_numpy(dtype=str)
undirected_edges = pd.DataFrame(
    {
        "cell_id_a": cell_ids[edge_i],
        "cell_id_b": cell_ids[edge_j],
        "shared_boundary_m": edge_length,
    }
).sort_values(["cell_id_a", "cell_id_b"]).reset_index(drop=True)

require(
    not (undirected_edges["cell_id_a"] == undirected_edges["cell_id_b"]).any(),
    "Self-loop found in contiguity graph",
)
require(
    not undirected_edges.duplicated(["cell_id_a", "cell_id_b"]).any(),
    "Duplicate undirected edges found",
)

graph = nx.Graph()
graph.add_nodes_from(cell_ids)
graph.add_edges_from(
    undirected_edges[["cell_id_a", "cell_id_b"]].itertuples(index=False, name=None)
)

degree = dict(graph.degree())
grid["neighbor_count"] = grid["cell_id"].map(degree).astype(int)
grid["is_island"] = grid["neighbor_count"].eq(0)

components = list(nx.connected_components(graph))
components = sorted(components, key=lambda values: (-len(values), min(values)))
component_lookup = {}
component_size_lookup = {}
component_rows = []

for sequence, members in enumerate(components, start=1):
    component_id = f"component_{sequence:04d}"
    ordered_members = sorted(members)
    component_rows.append(
        {
            "component_id": component_id,
            "cell_count": len(ordered_members),
            "representative_cell_id": ordered_members[0],
            "is_island_component": int(len(ordered_members) == 1),
            "graph_version": GRAPH_VERSION,
        }
    )
    for cell_id in ordered_members:
        component_lookup[cell_id] = component_id
        component_size_lookup[cell_id] = len(ordered_members)

grid["component_id"] = grid["cell_id"].map(component_lookup)
grid["component_size"] = grid["cell_id"].map(component_size_lookup).astype(int)

forward = undirected_edges.rename(
    columns={"cell_id_a": "focal_cell_id", "cell_id_b": "neighbor_cell_id"}
)
reverse = undirected_edges.rename(
    columns={"cell_id_b": "focal_cell_id", "cell_id_a": "neighbor_cell_id"}
)
directed_weights = pd.concat([forward, reverse], ignore_index=True)
directed_weights["binary_weight"] = 1.0
directed_weights["row_standardized_weight"] = directed_weights[
    "focal_cell_id"
].map(lambda value: 1.0 / degree[value])
directed_weights["graph_version"] = GRAPH_VERSION
directed_weights = directed_weights.sort_values(
    ["focal_cell_id", "neighbor_cell_id"]
).reset_index(drop=True)

reverse_pairs = set(
    zip(directed_weights["neighbor_cell_id"], directed_weights["focal_cell_id"])
)
forward_pairs = set(
    zip(directed_weights["focal_cell_id"], directed_weights["neighbor_cell_id"])
)
require(forward_pairs == reverse_pairs, "Directed weights are not symmetric")

row_sums = directed_weights.groupby("focal_cell_id")[
    "row_standardized_weight"
].sum()
maximum_row_sum_difference = float((row_sums - 1.0).abs().max())
require(
    maximum_row_sum_difference <= ROW_WEIGHT_TOLERANCE,
    "Row-standardized weights do not sum to one",
)
require(
    len(directed_weights) == 2 * len(undirected_edges),
    "Directed and undirected edge counts do not reconcile",
)
require(sum(degree.values()) == len(directed_weights), "Degree sum does not close")


# -----------------------------------------------------------------------------
# 6. Outputs
# -----------------------------------------------------------------------------

grid["geometry_valid"] = grid.geometry.is_valid
grid["geometry_type"] = grid.geom_type
grid["spatial_support_version"] = OUTPUT_VERSION
grid["graph_version"] = GRAPH_VERSION

output_columns = [
    "cell_id",
    "GRID_ID",
    "source_batch_id",
    "canonical_member",
    "domain_version",
    "geometry_type",
    "geometry_valid",
    "geometry_area_geodesic_ha",
    "geometry_area_aea_ha",
    "area_aea_vs_gee_relative_difference",
    "centroid_lon_gee",
    "centroid_lat_gee",
    "centroid_lon_aea",
    "centroid_lat_aea",
    "centroid_method_distance_m",
    "aea_centroid_within_cell",
    "amazon_overlap_ha",
    "cerrado_overlap_ha",
    "target_biome_overlap_ha",
    "amazon_fraction_cell",
    "cerrado_fraction_cell",
    "target_biome_fraction_cell",
    "outside_target_biomes_ha",
    "outside_target_biomes_fraction",
    "primary_biome",
    "primary_biome_code",
    "primary_biome_overlap_ha",
    "primary_biome_fraction_cell",
    "primary_biome_fraction_target_overlap",
    "crosses_amazon_cerrado_boundary",
    "extends_outside_target_biomes",
    "neighbor_count",
    "is_island",
    "component_id",
    "component_size",
    "spatial_support_version",
    "graph_version",
    "geometry",
]

spatial_support = gpd.GeoDataFrame(
    grid[output_columns].copy(), geometry="geometry", crs=WGS84_CRS
)
spatial_support.to_parquet(
    SPATIAL_SUPPORT_OUTPUT, index=False, compression="zstd"
)
spatial_support.drop(columns="geometry").to_csv(
    SPATIAL_ATTRIBUTES_OUTPUT, index=False, float_format="%.12g"
)
directed_weights.to_parquet(WEIGHTS_OUTPUT, index=False, compression="zstd")

biome_summary = (
    spatial_support.groupby("primary_biome", dropna=False)
    .agg(
        cell_count=("cell_id", "size"),
        cell_area_ha=("geometry_area_aea_ha", "sum"),
        amazon_overlap_ha=("amazon_overlap_ha", "sum"),
        cerrado_overlap_ha=("cerrado_overlap_ha", "sum"),
        target_biome_overlap_ha=("target_biome_overlap_ha", "sum"),
        boundary_cell_count=("crosses_amazon_cerrado_boundary", "sum"),
        outside_target_cell_count=("extends_outside_target_biomes", "sum"),
    )
    .reset_index()
)
biome_summary["spatial_support_version"] = OUTPUT_VERSION
biome_summary.to_csv(BIOME_SUMMARY_OUTPUT, index=False, float_format="%.12g")

neighbor_summary = (
    spatial_support.groupby("neighbor_count", dropna=False)
    .size()
    .rename("cell_count")
    .reset_index()
    .sort_values("neighbor_count")
)
neighbor_summary["cell_fraction"] = neighbor_summary["cell_count"] / EXPECTED_CELLS
neighbor_summary["graph_version"] = GRAPH_VERSION
neighbor_summary.to_csv(
    NEIGHBOR_SUMMARY_OUTPUT, index=False, float_format="%.12g"
)

component_summary = pd.DataFrame(component_rows)
component_summary.to_csv(COMPONENT_SUMMARY_OUTPUT, index=False)

summary = pd.DataFrame(
    [
        {
            "spatial_support_version": OUTPUT_VERSION,
            "graph_version": GRAPH_VERSION,
            "cell_count": len(spatial_support),
            "distinct_cell_id_count": spatial_support["cell_id"].nunique(),
            "grid_panel_unmatched_count": len(grid_id_set ^ panel_unique_ids),
            "invalid_geometry_count": int((~spatial_support.geometry.is_valid).sum()),
            "empty_geometry_count": int(spatial_support.geometry.is_empty.sum()),
            "maximum_area_relative_difference": maximum_area_relative_difference,
            "maximum_biome_overlap_excess_ha": maximum_biome_excess_ha,
            "cells_without_target_biome_overlap": int(
                (spatial_support["target_biome_overlap_ha"] <= 0).sum()
            ),
            "amazon_primary_cells": int(
                (spatial_support["primary_biome"] == "Amazon").sum()
            ),
            "cerrado_primary_cells": int(
                (spatial_support["primary_biome"] == "Cerrado").sum()
            ),
            "tied_primary_biome_cells": int(
                (spatial_support["primary_biome"] == "Tie").sum()
            ),
            "amazon_cerrado_boundary_cells": int(
                spatial_support["crosses_amazon_cerrado_boundary"].sum()
            ),
            "cells_extending_outside_target_biomes": int(
                spatial_support["extends_outside_target_biomes"].sum()
            ),
            "candidate_intersection_pairs": len(i),
            "undirected_edge_count": len(undirected_edges),
            "directed_weight_count": len(directed_weights),
            "connected_component_count": len(components),
            "island_count": int(spatial_support["is_island"].sum()),
            "minimum_neighbor_count": int(spatial_support["neighbor_count"].min()),
            "mean_neighbor_count": float(spatial_support["neighbor_count"].mean()),
            "maximum_neighbor_count": int(spatial_support["neighbor_count"].max()),
            "maximum_grid_overlap_m2": maximum_grid_overlap_m2,
            "maximum_row_weight_sum_difference": maximum_row_sum_difference,
            "shared_edge_tolerance_m": SHARED_EDGE_TOLERANCE_M,
            "row_standardization": "binary weights standardized to sum to 1 by focal cell",
            "island_treatment": "retained with zero neighbors; no artificial links added",
            "cartographic_crs": AEA_CRS,
        }
    ]
)
summary.to_csv(SUMMARY_OUTPUT, index=False, float_format="%.12g")

output_paths = [
    SPATIAL_SUPPORT_OUTPUT,
    SPATIAL_ATTRIBUTES_OUTPUT,
    WEIGHTS_OUTPUT,
    BIOME_SUMMARY_OUTPUT,
    NEIGHBOR_SUMMARY_OUTPUT,
    COMPONENT_SUMMARY_OUTPUT,
    SUMMARY_OUTPUT,
]
output_hashes = dataframe_hashes(output_paths)

validation = {
    "validation_status": "PASS",
    "spatial_support_version": OUTPUT_VERSION,
    "graph_version": GRAPH_VERSION,
    "inputs": {
        "grid_geojson": {"path": str(GRID_INPUT), "sha256": input_hashes["grid_geojson"]},
        "biome_geojson": {"path": str(BIOME_INPUT), "sha256": input_hashes["biome_geojson"]},
        "integrated_panel": {"path": str(PANEL_INPUT), "sha256": input_hashes["integrated_panel"]},
    },
    "configuration": {
        "wgs84_crs": WGS84_CRS,
        "cartographic_equal_area_crs": AEA_CRS,
        "area_relative_tolerance": AREA_RELATIVE_TOLERANCE,
        "biome_area_tolerance_ha": BIOME_AREA_TOLERANCE_HA,
        "positive_overlap_tolerance_ha": POSITIVE_OVERLAP_TOLERANCE_HA,
        "shared_edge_tolerance_m": SHARED_EDGE_TOLERANCE_M,
        "grid_overlap_tolerance_m2": GRID_OVERLAP_TOLERANCE_M2,
        "row_weight_tolerance": ROW_WEIGHT_TOLERANCE,
        "weight_standardization": "binary row-standardized",
        "island_treatment": "retain islands with zero neighbors; do not add links",
        "primary_biome_rule": "largest Amazon or Cerrado overlap area in AEA CRS",
    },
    "spatial_support": {
        "cell_count": len(spatial_support),
        "distinct_cell_id_count": spatial_support["cell_id"].nunique(),
        "invalid_geometry_count": int((~spatial_support.geometry.is_valid).sum()),
        "empty_geometry_count": int(spatial_support.geometry.is_empty.sum()),
        "grid_panel_unmatched_count": len(grid_id_set ^ panel_unique_ids),
        "maximum_area_relative_difference": maximum_area_relative_difference,
        "maximum_biome_overlap_excess_ha": maximum_biome_excess_ha,
        "cells_without_target_biome_overlap": int(
            (spatial_support["target_biome_overlap_ha"] <= 0).sum()
        ),
        "primary_biome_counts": spatial_support["primary_biome"].value_counts().to_dict(),
        "boundary_cell_count": int(
            spatial_support["crosses_amazon_cerrado_boundary"].sum()
        ),
    },
    "contiguity_graph": {
        "candidate_intersection_pairs": len(i),
        "undirected_edge_count": len(undirected_edges),
        "directed_weight_count": len(directed_weights),
        "connected_component_count": len(components),
        "island_count": int(spatial_support["is_island"].sum()),
        "minimum_neighbor_count": int(spatial_support["neighbor_count"].min()),
        "mean_neighbor_count": float(spatial_support["neighbor_count"].mean()),
        "maximum_neighbor_count": int(spatial_support["neighbor_count"].max()),
        "maximum_grid_overlap_m2": maximum_grid_overlap_m2,
        "maximum_row_weight_sum_difference": maximum_row_sum_difference,
        "symmetric_directed_weights": True,
    },
    "software": {
        "python": sys.version,
        "geopandas": package_version("geopandas"),
        "shapely": package_version("shapely"),
        "pyproj": package_version("pyproj"),
        "pyarrow": package_version("pyarrow"),
        "networkx": package_version("networkx"),
        "pandas": package_version("pandas"),
        "numpy": package_version("numpy"),
    },
    "outputs": {
        path.name: {"path": str(path), "sha256": output_hashes[path.name]}
        for path in output_paths
    },
    "checks": {
        "input_hashes_match": True,
        "expected_grid_and_biome_counts": True,
        "unique_grid_identifiers": True,
        "valid_nonempty_geometries": True,
        "grid_population_matches_integrated_panel": True,
        "equal_area_reconciliation_within_tolerance": True,
        "positive_target_biome_overlap_for_every_cell": True,
        "biome_overlap_reconciles_with_cell_area": True,
        "no_material_grid_overlap": True,
        "no_self_or_duplicate_edges": True,
        "symmetric_directed_weights": True,
        "row_standardized_weights_close": True,
        "all_cells_assigned_to_components": True,
    },
}

with VALIDATION_OUTPUT.open("w", encoding="utf-8") as destination:
    json.dump(
        validation,
        destination,
        ensure_ascii=False,
        indent=2,
        default=python_scalar,
    )

print("\nPHASE 1 SPATIAL SUPPORT BUILD COMPLETE")
print("Validation status: PASS")
print("Cells:", f"{len(spatial_support):,}")
print("Primary-biome counts:", spatial_support["primary_biome"].value_counts().to_dict())
print("Boundary cells:", int(spatial_support["crosses_amazon_cerrado_boundary"].sum()))
print("Undirected shared-edge links:", f"{len(undirected_edges):,}")
print("Directed weight rows:", f"{len(directed_weights):,}")
print("Connected components:", len(components))
print("Islands:", int(spatial_support["is_island"].sum()))
print("Neighbor-count range:", int(spatial_support["neighbor_count"].min()), "to", int(spatial_support["neighbor_count"].max()))
print("Maximum AEA-versus-GEE area difference:", maximum_area_relative_difference)
print("Maximum grid overlap (m2):", maximum_grid_overlap_m2)
print("Maximum row-weight sum difference:", maximum_row_sum_difference)
print("Validation record:", VALIDATION_OUTPUT)

"""
Build and validate the Phase 2 canonical spatial-metrics panel.

Designed for Google Colab. The script joins the validated integrated
cell-interval panel to the validated Phase 1 spatial support, preserves the
fixed complete-domain graph, derives prespecified spatial-analysis fields,
and records the inherited active-cell subgraph for each interval.

This stage does not calculate Moran's I, LISA, map classes, or temporal
clusters.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys


# -----------------------------------------------------------------------------
# 0. Colab dependencies
# -----------------------------------------------------------------------------

REQUIRED_PACKAGES = {
    "geopandas": "geopandas>=0.14,<2",
    "pyarrow": "pyarrow>=14",
    "networkx": "networkx>=3,<4",
}

missing_packages = [
    requirement
    for module, requirement in REQUIRED_PACKAGES.items()
    if importlib.util.find_spec(module) is None
]

if missing_packages:
    print("Installing missing dependencies:", missing_packages)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *missing_packages]
    )

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

try:
    from google.colab import drive
except ImportError:
    drive = None


# -----------------------------------------------------------------------------
# 1. Canonical paths and identities
# -----------------------------------------------------------------------------

if drive is not None:
    drive.mount("/content/drive")

PROJECT_DIR = Path(
    os.environ.get(
        "CANONICAL_SPATIAL_PROJECT_DIR",
        "/content/drive/MyDrive/Trabalho/Contabilidade",
    )
)

ANALYSIS_DIR = PROJECT_DIR / "analysis"
PHASE1_DIR = PROJECT_DIR / "spatial" / "phase1"
OUTPUT_DIR = PROJECT_DIR / "spatial" / "phase2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

INTEGRATED_PANEL_INPUT = (
    ANALYSIS_DIR
    / "canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet"
)
INTEGRATED_SUMMARY_INPUT = (
    ANALYSIS_DIR / "canonical_integrated_stock_flow_trajectory_summary_v1.csv"
)
SPATIAL_SUPPORT_INPUT = PHASE1_DIR / "canonical_spatial_support_v1.parquet"
CONTIGUITY_WEIGHTS_INPUT = (
    PHASE1_DIR / "canonical_contiguity_weights_v1.parquet"
)

SPATIAL_METRICS_OUTPUT = OUTPUT_DIR / "canonical_spatial_metrics_panel_v1.parquet"
SPATIAL_METRICS_SUMMARY_OUTPUT = (
    OUTPUT_DIR / "canonical_spatial_metrics_summary_v1.csv"
)
CONDITIONAL_NODES_OUTPUT = (
    OUTPUT_DIR / "canonical_cr_balance_active_subgraph_nodes_v1.parquet"
)
CONDITIONAL_SUMMARY_OUTPUT = (
    OUTPUT_DIR / "canonical_cr_balance_active_subgraph_summary_v1.csv"
)
VALIDATION_OUTPUT = OUTPUT_DIR / "canonical_spatial_metrics_validation_v1.json"

EXPECTED_INTEGRATED_PANEL_SHA256 = (
    "7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28"
)
EXPECTED_INTEGRATED_SUMMARY_SHA256 = (
    "962803ebccc49f6c2aca14f3cbe7a24143ae2324ed4cbb17a18a2ce62970cab8"
)
EXPECTED_SPATIAL_SUPPORT_SHA256 = (
    "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc"
)
EXPECTED_CONTIGUITY_WEIGHTS_SHA256 = (
    "85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f"
)

EXPECTED_ROWS = 199_112
EXPECTED_CELLS = 24_889
EXPECTED_INTERVALS = 8
EXPECTED_INTEGRATED_COLUMNS = 150
EXPECTED_WEIGHT_ROWS = 134_906

SPATIAL_SUPPORT_VERSION = "canonical-spatial-support-v1"
GRAPH_VERSION = "canonical-edge-contiguity-v1"
OUTPUT_VERSION = "canonical-spatial-metrics-v1"
CONDITIONAL_GRAPH_VERSION = "canonical-cr-balance-active-subgraph-v1"

ZERO_TOLERANCE_HA = 1e-9
IDENTITY_TOLERANCE_HA = 2e-6
ROW_WEIGHT_TOLERANCE = 1e-12
SHARED_EDGE_TOLERANCE_M = 1.0
SENSITIVITY_THRESHOLDS_HA = {
    "primary": ZERO_TOLERANCE_HA,
    "0p1ha": 0.1,
    "1ha": 1.0,
}

KEY_COLUMNS = ["cell_id", "t0", "t1"]


# -----------------------------------------------------------------------------
# 2. Required source fields
# -----------------------------------------------------------------------------

CORE_AREA_COLUMNS = [
    "consolidation_ha",
    "replenishment_ha",
    "gross_cr_activity_ha",
    "net_cr_balance_ha",
    "nat_tmp_endpoint_ha",
    "nat_tmp_pas_any_ha",
    "nat_tmp_pas_2plus_ha",
    "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_without_intermediate_pasture_ha",
    "nat_tmp_mid_incomplete_ha",
]

TRAJECTORY_SHARE_COLUMNS = [
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_2plus_share_endpoint",
    "nat_tmp_pas_consecutive2_share_endpoint",
    "nat_tmp_pas_consecutive2_share_any",
    "nat_tmp_mid_incomplete_share_endpoint",
]

REQUIRED_PANEL_COLUMNS = {
    "cell_id",
    "GRID_ID",
    "source_batch_id",
    "t0",
    "t1",
    "interval",
    "diagnostic_interval",
    "primary_inference_interval",
    "stock0_pas",
    "stock0_nat",
    "flow_pas_tmp",
    "flow_nat_pas",
    "flow_nat_tmp",
    "consolidation_rate_initial_pasture",
    "replenishment_rate_initial_native",
    "cr_balance_index",
    "has_consolidation",
    "has_replenishment",
    "has_cr_activity",
    "cr_activity_class",
    *CORE_AREA_COLUMNS,
    *TRAJECTORY_SHARE_COLUMNS,
}

REQUIRED_SPATIAL_COLUMNS = {
    "cell_id",
    "GRID_ID",
    "source_batch_id",
    "canonical_member",
    "domain_version",
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
    "spatial_support_version",
    "graph_version",
    "geometry",
}

REQUIRED_WEIGHT_COLUMNS = {
    "focal_cell_id",
    "neighbor_cell_id",
    "shared_boundary_m",
    "binary_weight",
    "row_standardized_weight",
    "graph_version",
}

OCCURRENCE_AREA_FIELDS = {
    "consolidation": "consolidation_ha",
    "replenishment": "replenishment_ha",
    "cr_activity": "gross_cr_activity_ha",
    "nat_tmp": "nat_tmp_endpoint_ha",
    "nat_tmp_pas_any": "nat_tmp_pas_any_ha",
    "nat_tmp_pas_consecutive2": "nat_tmp_pas_consecutive2_ha",
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


def safe_divide(numerator, denominator, tolerance=ZERO_TOLERANCE_HA):
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    return np.divide(
        numerator,
        denominator,
        out=np.full(numerator.shape, np.nan, dtype=float),
        where=denominator > tolerance,
    )


def maximum_absolute_difference(left, right) -> float:
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.size == 0:
        return 0.0
    return float(np.nanmax(np.abs(left - right)))


def package_version(package: str) -> str:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return "not-recorded"


def python_scalar(value):
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


# -----------------------------------------------------------------------------
# 4. Input identity and structure
# -----------------------------------------------------------------------------

print("CANONICAL SPATIAL METRICS - PHASE 2 VERSION 1")
print("Output directory:", OUTPUT_DIR)

input_paths = [
    INTEGRATED_PANEL_INPUT,
    INTEGRATED_SUMMARY_INPUT,
    SPATIAL_SUPPORT_INPUT,
    CONTIGUITY_WEIGHTS_INPUT,
]
for path in input_paths:
    require(path.exists(), f"Required input not found: {path}")

input_hashes = {path.name: sha256_file(path) for path in input_paths}
expected_hashes = {
    INTEGRATED_PANEL_INPUT.name: EXPECTED_INTEGRATED_PANEL_SHA256,
    INTEGRATED_SUMMARY_INPUT.name: EXPECTED_INTEGRATED_SUMMARY_SHA256,
    SPATIAL_SUPPORT_INPUT.name: EXPECTED_SPATIAL_SUPPORT_SHA256,
    CONTIGUITY_WEIGHTS_INPUT.name: EXPECTED_CONTIGUITY_WEIGHTS_SHA256,
}
for name, expected_hash in expected_hashes.items():
    require(
        input_hashes[name] == expected_hash,
        f"Input SHA-256 mismatch for {name}: expected {expected_hash}, "
        f"found {input_hashes[name]}",
    )

panel = pd.read_parquet(INTEGRATED_PANEL_INPUT)
accepted_summary = pd.read_csv(INTEGRATED_SUMMARY_INPUT, low_memory=False)
spatial = gpd.read_parquet(SPATIAL_SUPPORT_INPUT)
weights = pd.read_parquet(CONTIGUITY_WEIGHTS_INPUT)

require(
    panel.shape == (EXPECTED_ROWS, EXPECTED_INTEGRATED_COLUMNS),
    f"Unexpected integrated panel shape: {panel.shape}",
)
require(len(spatial) == EXPECTED_CELLS, "Unexpected spatial-support row count")
require(len(weights) == EXPECTED_WEIGHT_ROWS, "Unexpected weight row count")
require(len(accepted_summary) == EXPECTED_INTERVALS, "Unexpected summary rows")
require(
    REQUIRED_PANEL_COLUMNS.issubset(panel.columns),
    f"Missing panel fields: {sorted(REQUIRED_PANEL_COLUMNS - set(panel.columns))}",
)
require(
    REQUIRED_SPATIAL_COLUMNS.issubset(spatial.columns),
    f"Missing spatial fields: {sorted(REQUIRED_SPATIAL_COLUMNS - set(spatial.columns))}",
)
require(
    REQUIRED_WEIGHT_COLUMNS.issubset(weights.columns),
    f"Missing weight fields: {sorted(REQUIRED_WEIGHT_COLUMNS - set(weights.columns))}",
)

panel["cell_id"] = panel["cell_id"].map(normalize_identifier)
panel["GRID_ID"] = panel["GRID_ID"].map(normalize_identifier)
spatial["cell_id"] = spatial["cell_id"].map(normalize_identifier)
spatial["GRID_ID"] = spatial["GRID_ID"].map(normalize_identifier)
weights["focal_cell_id"] = weights["focal_cell_id"].map(normalize_identifier)
weights["neighbor_cell_id"] = weights["neighbor_cell_id"].map(normalize_identifier)

panel_original_columns = panel.columns.tolist()
panel = panel.sort_values(KEY_COLUMNS).reset_index(drop=True)
spatial = spatial.sort_values("cell_id").reset_index(drop=True)

require(panel.duplicated(KEY_COLUMNS).sum() == 0, "Duplicate panel keys")
require(panel["cell_id"].nunique() == EXPECTED_CELLS, "Unexpected panel cells")
require(spatial["cell_id"].nunique() == EXPECTED_CELLS, "Duplicate spatial cells")
require(panel["interval"].nunique() == EXPECTED_INTERVALS, "Unexpected intervals")
require(
    panel.groupby("cell_id")["interval"].nunique().eq(EXPECTED_INTERVALS).all(),
    "At least one cell lacks an interval",
)
require(
    set(panel["cell_id"]) == set(spatial["cell_id"]),
    "Panel and spatial-support cell populations differ",
)
require(
    set(spatial["spatial_support_version"].astype(str))
    == {SPATIAL_SUPPORT_VERSION},
    "Unexpected spatial-support version",
)
require(
    set(spatial["graph_version"].astype(str)) == {GRAPH_VERSION},
    "Unexpected graph version in spatial support",
)
require(
    set(weights["graph_version"].astype(str)) == {GRAPH_VERSION},
    "Unexpected graph version in weights",
)


# -----------------------------------------------------------------------------
# 5. Fixed graph validation
# -----------------------------------------------------------------------------

require(
    not (weights["focal_cell_id"] == weights["neighbor_cell_id"]).any(),
    "Self-link found in weights",
)
require(
    not weights.duplicated(["focal_cell_id", "neighbor_cell_id"]).any(),
    "Duplicate directed weights found",
)
require(
    np.allclose(weights["binary_weight"], 1.0),
    "Binary weight differs from one",
)

directed_pairs = set(
    zip(weights["focal_cell_id"], weights["neighbor_cell_id"])
)
reverse_pairs = set(
    zip(weights["neighbor_cell_id"], weights["focal_cell_id"])
)
require(directed_pairs == reverse_pairs, "Weight matrix is not symmetric")

row_sums = weights.groupby("focal_cell_id")["row_standardized_weight"].sum()
maximum_row_sum_difference = float((row_sums - 1.0).abs().max())
require(
    maximum_row_sum_difference <= ROW_WEIGHT_TOLERANCE,
    "Full-graph row-standardized weights do not close",
)

observed_degree = weights.groupby("focal_cell_id").size()
expected_row_weight = weights["focal_cell_id"].map(
    lambda value: 1.0 / observed_degree[value]
)
maximum_individual_weight_difference = maximum_absolute_difference(
    weights["row_standardized_weight"], expected_row_weight
)
require(
    maximum_individual_weight_difference <= ROW_WEIGHT_TOLERANCE,
    "At least one row-standardized weight differs from 1 / degree",
)
require(
    (
        pd.to_numeric(weights["shared_boundary_m"], errors="raise")
        > SHARED_EDGE_TOLERANCE_M
    ).all(),
    "A retained graph link does not meet the shared-edge tolerance",
)

expected_degree = spatial.set_index("cell_id")["neighbor_count"].astype(int)
degree_from_weights = expected_degree.index.to_series().map(observed_degree).fillna(0).astype(int)
degree_mismatch_count = int((degree_from_weights.to_numpy() != expected_degree.to_numpy()).sum())
require(degree_mismatch_count == 0, "Spatial neighbor counts do not match weights")

full_graph = nx.Graph()
full_graph.add_nodes_from(spatial["cell_id"])
full_graph.add_edges_from(directed_pairs)
require(full_graph.number_of_nodes() == EXPECTED_CELLS, "Graph node loss")
require(
    full_graph.number_of_edges() * 2 == EXPECTED_WEIGHT_ROWS,
    "Graph edge count does not reconcile",
)

computed_components = list(nx.connected_components(full_graph))
computed_components = sorted(
    computed_components, key=lambda values: (-len(values), min(values))
)
computed_component_id = {}
computed_component_size = {}
for sequence, members in enumerate(computed_components, start=1):
    component_id = f"component_{sequence:04d}"
    for cell_id in members:
        computed_component_id[cell_id] = component_id
        computed_component_size[cell_id] = len(members)

component_id_mismatch_count = int(
    (
        spatial["cell_id"].map(computed_component_id).astype(str)
        != spatial["component_id"].astype(str)
    ).sum()
)
component_size_mismatch_count = int(
    (
        spatial["cell_id"].map(computed_component_size).astype(int)
        != spatial["component_size"].astype(int)
    ).sum()
)
island_flag_mismatch_count = int(
    (
        spatial["is_island"].astype(bool)
        != spatial["neighbor_count"].astype(int).eq(0)
    ).sum()
)
require(component_id_mismatch_count == 0, "Component ID mismatch")
require(component_size_mismatch_count == 0, "Component size mismatch")
require(island_flag_mismatch_count == 0, "Island flag mismatch")


# -----------------------------------------------------------------------------
# 6. Validate shared identifiers and join spatial attributes
# -----------------------------------------------------------------------------

panel_cell_metadata = (
    panel[["cell_id", "GRID_ID", "source_batch_id"]]
    .drop_duplicates()
    .sort_values("cell_id")
    .reset_index(drop=True)
)
require(
    len(panel_cell_metadata) == EXPECTED_CELLS,
    "Panel metadata varies within cell",
)

spatial_metadata = spatial[["cell_id", "GRID_ID", "source_batch_id"]].copy()
spatial_metadata["source_batch_id"] = pd.to_numeric(
    spatial_metadata["source_batch_id"], errors="raise"
)
panel_cell_metadata["source_batch_id"] = pd.to_numeric(
    panel_cell_metadata["source_batch_id"], errors="raise"
)

metadata_check = panel_cell_metadata.merge(
    spatial_metadata,
    on="cell_id",
    how="outer",
    validate="one_to_one",
    suffixes=("_panel", "_spatial"),
    indicator=True,
)
require((metadata_check["_merge"] == "both").all(), "Spatial metadata join loss")
require(
    (metadata_check["GRID_ID_panel"] == metadata_check["GRID_ID_spatial"]).all(),
    "GRID_ID mismatch between panel and spatial support",
)
require(
    (
        metadata_check["source_batch_id_panel"]
        == metadata_check["source_batch_id_spatial"]
    ).all(),
    "source_batch_id mismatch between panel and spatial support",
)

spatial_attributes = spatial.drop(columns="geometry").copy()
overlapping_spatial_fields = [
    column
    for column in spatial_attributes.columns
    if column in panel.columns and column != "cell_id"
]
spatial_fields_to_add = [
    column
    for column in spatial_attributes.columns
    if column not in panel.columns and column != "cell_id"
]

metrics = panel.merge(
    spatial_attributes[["cell_id", *spatial_fields_to_add]],
    on="cell_id",
    how="left",
    validate="many_to_one",
    sort=False,
)
metrics = metrics.sort_values(KEY_COLUMNS).reset_index(drop=True)

require(len(metrics) == EXPECTED_ROWS, "Spatial join changed row count")
require(
    metrics[spatial_fields_to_add].notna().all().all(),
    "Missing spatial attributes after join",
)
require(
    metrics[panel_original_columns].equals(panel[panel_original_columns]),
    "At least one integrated-panel value changed during the spatial join",
)


# -----------------------------------------------------------------------------
# 7. Prespecified spatial-analysis metrics and support flags
# -----------------------------------------------------------------------------

metrics["nat_tmp_intensity_initial_native"] = safe_divide(
    metrics["nat_tmp_endpoint_ha"], metrics["stock0_nat"]
)

metrics["consolidation_rate_defined"] = (
    metrics["stock0_pas"] > ZERO_TOLERANCE_HA
).astype("int8")
metrics["replenishment_rate_defined"] = (
    metrics["stock0_nat"] > ZERO_TOLERANCE_HA
).astype("int8")
metrics["nat_tmp_intensity_defined"] = (
    metrics["stock0_nat"] > ZERO_TOLERANCE_HA
).astype("int8")
metrics["cr_balance_defined"] = (
    metrics["gross_cr_activity_ha"] > ZERO_TOLERANCE_HA
).astype("int8")
metrics["nat_tmp_endpoint_share_defined"] = (
    metrics["nat_tmp_endpoint_ha"] > ZERO_TOLERANCE_HA
).astype("int8")
metrics["nat_tmp_pas_any_share_defined"] = (
    metrics["nat_tmp_pas_any_ha"] > ZERO_TOLERANCE_HA
).astype("int8")

for process_name, area_column in OCCURRENCE_AREA_FIELDS.items():
    for threshold_name, threshold_ha in SENSITIVITY_THRESHOLDS_HA.items():
        metrics[f"{process_name}_occurs_gt_{threshold_name}"] = (
            metrics[area_column] > threshold_ha
        ).astype("int8")

inactive = metrics["cr_balance_defined"].eq(0)
replenishment_dominant = metrics["cr_balance_index"] < (-1.0 / 3.0)
mixed = metrics["cr_balance_index"].between(
    -1.0 / 3.0, 1.0 / 3.0, inclusive="both"
)
consolidation_dominant = metrics["cr_balance_index"] > (1.0 / 3.0)

metrics["cr_balance_state"] = np.select(
    [inactive, replenishment_dominant, mixed, consolidation_dominant],
    [
        "inactive",
        "replenishment_dominant",
        "mixed",
        "consolidation_dominant",
    ],
    default="invalid",
)
metrics["spatial_metrics_version"] = OUTPUT_VERSION


# -----------------------------------------------------------------------------
# 8. Metric validation
# -----------------------------------------------------------------------------

formula_differences = {
    "consolidation_identity": maximum_absolute_difference(
        metrics["consolidation_ha"], metrics["flow_pas_tmp"]
    ),
    "replenishment_identity": maximum_absolute_difference(
        metrics["replenishment_ha"], metrics["flow_nat_pas"]
    ),
    "nat_tmp_endpoint_identity": maximum_absolute_difference(
        metrics["nat_tmp_endpoint_ha"], metrics["flow_nat_tmp"]
    ),
    "gross_cr_identity": maximum_absolute_difference(
        metrics["gross_cr_activity_ha"],
        metrics["consolidation_ha"] + metrics["replenishment_ha"],
    ),
    "net_cr_identity": maximum_absolute_difference(
        metrics["net_cr_balance_ha"],
        metrics["consolidation_ha"] - metrics["replenishment_ha"],
    ),
    "balance_index_identity": maximum_absolute_difference(
        metrics.loc[~inactive, "cr_balance_index"],
        safe_divide(
            metrics.loc[~inactive, "net_cr_balance_ha"],
            metrics.loc[~inactive, "gross_cr_activity_ha"],
        ),
    ),
    "consolidation_rate_identity": maximum_absolute_difference(
        metrics.loc[metrics["consolidation_rate_defined"].eq(1),
                    "consolidation_rate_initial_pasture"],
        safe_divide(
            metrics.loc[metrics["consolidation_rate_defined"].eq(1),
                        "consolidation_ha"],
            metrics.loc[metrics["consolidation_rate_defined"].eq(1),
                        "stock0_pas"],
        ),
    ),
    "replenishment_rate_identity": maximum_absolute_difference(
        metrics.loc[metrics["replenishment_rate_defined"].eq(1),
                    "replenishment_rate_initial_native"],
        safe_divide(
            metrics.loc[metrics["replenishment_rate_defined"].eq(1),
                        "replenishment_ha"],
            metrics.loc[metrics["replenishment_rate_defined"].eq(1),
                        "stock0_nat"],
        ),
    ),
}

require(
    max(formula_differences.values()) <= IDENTITY_TOLERANCE_HA,
    f"Metric identity failed: {formula_differences}",
)
require(not metrics["cr_balance_state"].eq("invalid").any(), "Invalid balance state")
require(
    metrics["has_consolidation"].astype("int8").eq(
        metrics["consolidation_occurs_gt_primary"]
    ).all(),
    "Primary consolidation occurrence differs from accepted flag",
)
require(
    metrics["has_replenishment"].astype("int8").eq(
        metrics["replenishment_occurs_gt_primary"]
    ).all(),
    "Primary replenishment occurrence differs from accepted flag",
)
require(
    metrics["has_cr_activity"].astype("int8").eq(
        metrics["cr_activity_occurs_gt_primary"]
    ).all(),
    "Primary C-R occurrence differs from accepted flag",
)
require(
    metrics.loc[inactive, "cr_balance_index"].isna().all(),
    "Inactive balance rows must be undefined",
)
require(
    metrics.loc[~inactive, "cr_balance_index"].notna().all(),
    "Active balance rows must be defined",
)

rate_field_checks = [
    ("consolidation_rate_initial_pasture", "consolidation_rate_defined"),
    ("replenishment_rate_initial_native", "replenishment_rate_defined"),
    ("nat_tmp_intensity_initial_native", "nat_tmp_intensity_defined"),
]
for value_column, flag_column in rate_field_checks:
    defined = metrics[flag_column].eq(1)
    require(
        metrics.loc[defined, value_column].notna().all(),
        f"Defined {value_column} contains missing values",
    )
    require(
        metrics.loc[~defined, value_column].isna().all(),
        f"Undefined {value_column} must be missing",
    )
    values = metrics.loc[defined, value_column]
    require(
        ((values >= -1e-12) & (values <= 1 + 1e-12)).all(),
        f"{value_column} outside [0, 1]",
    )

require(
    metrics["nat_tmp_endpoint_share_defined"].eq(
        metrics["nat_tmp_pas_any_share_endpoint"].notna().astype("int8")
    ).all(),
    "NAT-TMP endpoint-share support flag mismatch",
)
require(
    metrics["nat_tmp_pas_any_share_defined"].eq(
        metrics["nat_tmp_pas_consecutive2_share_any"].notna().astype("int8")
    ).all(),
    "Pasture-any share support flag mismatch",
)

for process_name in OCCURRENCE_AREA_FIELDS:
    primary_flag = metrics[f"{process_name}_occurs_gt_primary"]
    flag_0p1 = metrics[f"{process_name}_occurs_gt_0p1ha"]
    flag_1 = metrics[f"{process_name}_occurs_gt_1ha"]
    require((primary_flag >= flag_0p1).all(), f"{process_name}: 0.1-ha nesting failed")
    require((flag_0p1 >= flag_1).all(), f"{process_name}: 1-ha nesting failed")


# -----------------------------------------------------------------------------
# 9. Inherited active-cell subgraphs by interval
# -----------------------------------------------------------------------------

conditional_node_rows = []
conditional_summary_rows = []

for (t0, t1), group in metrics.groupby(["t0", "t1"], sort=True):
    active_ids = set(group.loc[group["cr_balance_defined"].eq(1), "cell_id"])
    active_graph = full_graph.subgraph(active_ids).copy()

    components = list(nx.connected_components(active_graph))
    components = sorted(components, key=lambda values: (-len(values), min(values)))
    component_lookup = {}
    component_size_lookup = {}

    for sequence, members in enumerate(components, start=1):
        component_id = f"{int(t0)}_{int(t1)}_component_{sequence:04d}"
        for cell_id in members:
            component_lookup[cell_id] = component_id
            component_size_lookup[cell_id] = len(members)

    active_degree = dict(active_graph.degree())
    for cell_id in sorted(active_ids):
        conditional_node_rows.append(
            {
                "cell_id": cell_id,
                "t0": int(t0),
                "t1": int(t1),
                "interval": f"{int(t0)}_{int(t1)}",
                "active_neighbor_count": int(active_degree[cell_id]),
                "active_island": int(active_degree[cell_id] == 0),
                "active_component_id": component_lookup[cell_id],
                "active_component_size": int(component_size_lookup[cell_id]),
                "conditional_graph_version": CONDITIONAL_GRAPH_VERSION,
            }
        )

    degree_values = np.array(list(active_degree.values()), dtype=int)
    inactive_count = EXPECTED_CELLS - len(active_ids)
    conditional_summary_rows.append(
        {
            "t0": int(t0),
            "t1": int(t1),
            "interval": f"{int(t0)}_{int(t1)}",
            "diagnostic_interval": int((int(t0), int(t1)) == (2020, 2025)),
            "active_cell_count": len(active_ids),
            "inactive_cell_count": inactive_count,
            "active_cell_fraction": len(active_ids) / EXPECTED_CELLS,
            "active_undirected_edge_count": active_graph.number_of_edges(),
            "active_component_count": len(components),
            "active_island_count": int((degree_values == 0).sum()),
            "minimum_active_neighbor_count": int(degree_values.min()),
            "mean_active_neighbor_count": float(degree_values.mean()),
            "maximum_active_neighbor_count": int(degree_values.max()),
            "largest_active_component_size": int(max(map(len, components))),
            "conditional_graph_version": CONDITIONAL_GRAPH_VERSION,
        }
    )

conditional_nodes = pd.DataFrame(conditional_node_rows).sort_values(
    ["t0", "t1", "cell_id"]
).reset_index(drop=True)
conditional_summary = pd.DataFrame(conditional_summary_rows).sort_values(
    ["t0", "t1"]
).reset_index(drop=True)

require(
    len(conditional_nodes) == int(metrics["cr_balance_defined"].sum()),
    "Conditional-node population does not match active balance rows",
)
require(
    (conditional_summary["active_cell_count"]
     + conditional_summary["inactive_cell_count"]).eq(EXPECTED_CELLS).all(),
    "Conditional active and inactive counts do not close",
)


# -----------------------------------------------------------------------------
# 10. Interval summary and reconciliation with accepted totals
# -----------------------------------------------------------------------------

summary_rows = []
for (t0, t1), group in metrics.groupby(["t0", "t1"], sort=True):
    consolidation = float(group["consolidation_ha"].sum())
    replenishment = float(group["replenishment_ha"].sum())
    gross = consolidation + replenishment
    row = {
        "t0": int(t0),
        "t1": int(t1),
        "interval": f"{int(t0)}_{int(t1)}",
        "diagnostic_interval": int((int(t0), int(t1)) == (2020, 2025)),
        "cell_count": len(group),
        "consolidation_ha": consolidation,
        "replenishment_ha": replenishment,
        "gross_cr_activity_ha": gross,
        "net_cr_balance_ha": consolidation - replenishment,
        "aggregate_cr_balance_index": (
            (consolidation - replenishment) / gross if gross > ZERO_TOLERANCE_HA else np.nan
        ),
        "nat_tmp_endpoint_ha": float(group["nat_tmp_endpoint_ha"].sum()),
        "aggregate_consolidation_rate_initial_pasture": (
            consolidation / float(group["stock0_pas"].sum())
            if float(group["stock0_pas"].sum()) > ZERO_TOLERANCE_HA
            else np.nan
        ),
        "aggregate_replenishment_rate_initial_native": (
            replenishment / float(group["stock0_nat"].sum())
            if float(group["stock0_nat"].sum()) > ZERO_TOLERANCE_HA
            else np.nan
        ),
        "aggregate_nat_tmp_intensity_initial_native": (
            float(group["nat_tmp_endpoint_ha"].sum()) / float(group["stock0_nat"].sum())
            if float(group["stock0_nat"].sum()) > ZERO_TOLERANCE_HA
            else np.nan
        ),
        "defined_consolidation_rate_cells": int(group["consolidation_rate_defined"].sum()),
        "defined_replenishment_rate_cells": int(group["replenishment_rate_defined"].sum()),
        "defined_nat_tmp_intensity_cells": int(group["nat_tmp_intensity_defined"].sum()),
        "defined_cr_balance_cells": int(group["cr_balance_defined"].sum()),
        "defined_nat_tmp_endpoint_share_cells": int(
            group["nat_tmp_endpoint_share_defined"].sum()
        ),
        "spatial_metrics_version": OUTPUT_VERSION,
    }
    for process_name in OCCURRENCE_AREA_FIELDS:
        for threshold_name in SENSITIVITY_THRESHOLDS_HA:
            row[f"{process_name}_cells_gt_{threshold_name}"] = int(
                group[f"{process_name}_occurs_gt_{threshold_name}"].sum()
            )
    summary_rows.append(row)

spatial_summary = pd.DataFrame(summary_rows).sort_values(["t0", "t1"]).reset_index(drop=True)

accepted_for_join = accepted_summary.copy()
accepted_for_join["interval"] = accepted_for_join["interval"].astype(str)
summary_check = spatial_summary.merge(
    accepted_for_join,
    on=["t0", "t1", "interval"],
    how="outer",
    validate="one_to_one",
    suffixes=("_phase2", "_accepted"),
    indicator=True,
)
require((summary_check["_merge"] == "both").all(), "Interval-summary join failed")

summary_reconciliation_fields = [
    "consolidation_ha",
    "replenishment_ha",
    "gross_cr_activity_ha",
    "net_cr_balance_ha",
    "aggregate_cr_balance_index",
    "nat_tmp_endpoint_ha",
]
summary_maximum_differences = {}
for column in summary_reconciliation_fields:
    difference = maximum_absolute_difference(
        summary_check[f"{column}_phase2"],
        summary_check[f"{column}_accepted"],
    )
    summary_maximum_differences[column] = difference
    require(
        difference <= IDENTITY_TOLERANCE_HA,
        f"Accepted interval summary mismatch for {column}: {difference}",
    )


# -----------------------------------------------------------------------------
# 11. Write outputs and validation record
# -----------------------------------------------------------------------------

metrics.to_parquet(SPATIAL_METRICS_OUTPUT, index=False, compression="zstd")
spatial_summary.to_csv(
    SPATIAL_METRICS_SUMMARY_OUTPUT, index=False, float_format="%.12g"
)
conditional_nodes.to_parquet(
    CONDITIONAL_NODES_OUTPUT, index=False, compression="zstd"
)
conditional_summary.to_csv(
    CONDITIONAL_SUMMARY_OUTPUT, index=False, float_format="%.12g"
)

output_paths = [
    SPATIAL_METRICS_OUTPUT,
    SPATIAL_METRICS_SUMMARY_OUTPUT,
    CONDITIONAL_NODES_OUTPUT,
    CONDITIONAL_SUMMARY_OUTPUT,
]
output_hashes = {path.name: sha256_file(path) for path in output_paths}

validation = {
    "validation_status": "PASS",
    "spatial_metrics_version": OUTPUT_VERSION,
    "conditional_graph_version": CONDITIONAL_GRAPH_VERSION,
    "inputs": {
        path.name: {"path": str(path), "sha256": input_hashes[path.name]}
        for path in input_paths
    },
    "configuration": {
        "zero_tolerance_ha": ZERO_TOLERANCE_HA,
        "identity_tolerance_ha": IDENTITY_TOLERANCE_HA,
        "sensitivity_thresholds_ha": SENSITIVITY_THRESHOLDS_HA,
        "balance_states": {
            "inactive": "gross_cr_activity_ha <= 1e-9",
            "replenishment_dominant": "cr_balance_index < -1/3",
            "mixed": "-1/3 <= cr_balance_index <= 1/3",
            "consolidation_dominant": "cr_balance_index > 1/3",
        },
        "conditional_graph_rule": (
            "induced subgraph of complete shared-edge graph among cells with "
            "gross_cr_activity_ha > 1e-9; no artificial links"
        ),
    },
    "structure": {
        "output_rows": len(metrics),
        "output_columns": len(metrics.columns),
        "distinct_cells": metrics["cell_id"].nunique(),
        "intervals": metrics["interval"].nunique(),
        "duplicate_keys": int(metrics.duplicated(KEY_COLUMNS).sum()),
        "spatial_fields_added": len(spatial_fields_to_add),
        "overlapping_spatial_fields_validated": overlapping_spatial_fields,
    },
    "full_graph": {
        "nodes": full_graph.number_of_nodes(),
        "undirected_edges": full_graph.number_of_edges(),
        "directed_weight_rows": len(weights),
        "degree_mismatch_count": degree_mismatch_count,
        "maximum_row_weight_sum_difference": maximum_row_sum_difference,
        "maximum_individual_weight_difference": maximum_individual_weight_difference,
        "connected_component_count": len(computed_components),
        "component_id_mismatch_count": component_id_mismatch_count,
        "component_size_mismatch_count": component_size_mismatch_count,
        "island_flag_mismatch_count": island_flag_mismatch_count,
    },
    "metric_validation": {
        "formula_maximum_absolute_differences": formula_differences,
        "accepted_summary_maximum_absolute_differences": summary_maximum_differences,
        "undefined_cr_balance_rows": int(metrics["cr_balance_index"].isna().sum()),
        "defined_cr_balance_rows": int(metrics["cr_balance_defined"].sum()),
        "balance_state_counts": metrics["cr_balance_state"].value_counts().to_dict(),
    },
    "conditional_subgraphs": conditional_summary.to_dict(orient="records"),
    "software": {
        "python": sys.version,
        "geopandas": package_version("geopandas"),
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
        "source_structures_match": True,
        "unique_balanced_panel": True,
        "panel_spatial_population_match": True,
        "fixed_graph_reconciles": True,
        "spatial_join_is_many_to_one_without_loss": True,
        "integrated_panel_fields_preserved": True,
        "core_metric_identities_pass": True,
        "undefined_value_rules_pass": True,
        "occurrence_thresholds_are_nested": True,
        "balance_states_are_complete": True,
        "accepted_interval_totals_reproduced": True,
        "conditional_subgraph_populations_reconcile": True,
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

print("\nPHASE 2 SPATIAL METRICS BUILD COMPLETE")
print("Validation status: PASS")
print("Rows:", f"{len(metrics):,}")
print("Columns:", len(metrics.columns))
print("Cells:", f"{metrics['cell_id'].nunique():,}")
print("Intervals:", metrics["interval"].nunique())
print("Spatial fields added:", len(spatial_fields_to_add))
print("Defined CR-balance rows:", f"{int(metrics['cr_balance_defined'].sum()):,}")
print("Conditional graph summaries:")
print(conditional_summary.to_string(index=False))
print("No Moran, LISA, map classes, or temporal clusters were calculated.")
print("Validation record:", VALIDATION_OUTPUT)

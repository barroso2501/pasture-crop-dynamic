"""Phase 8D: compare Global Moran across canonical and alternative MAUP grids.

Colab:
    %run /content/14b_compute_maup_global_moran_v1.py

Dependencies: numpy, pandas, scipy, matplotlib, pyarrow.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import itertools
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


VERSION = "phase8d-maup-global-moran-script-revision-2"
ANALYTICAL_VERSION = "phase8d-maup-global-moran-v1"
MASTER_SEED = 20260920
PERMUTATIONS = 9_999
PRIMARY_SUPPORT_THRESHOLD = 0.50
MORAN_ABSOLUTE_DIFFERENCE_THRESHOLD = 0.10
TEMPORAL_SPEARMAN_THRESHOLD = 0.90
EXTREMUM_INTERVAL_DISTANCE_THRESHOLD = 1
ALPHA = 0.05

PROJECT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade")
CANONICAL_PANEL = PROJECT_DIR / "spatial/phase2/canonical_spatial_metrics_panel_v1.parquet"
CANONICAL_WEIGHTS = PROJECT_DIR / "spatial/phase1/canonical_contiguity_weights_v1.parquet"
CANONICAL_PHASE5_RESULTS = PROJECT_DIR / "spatial/phase5/global_moran_v1/canonical_global_moran_results_v1.csv"
ALTERNATIVE_PANEL = PROJECT_DIR / "spatial/phase8/maup_metrics_v1/canonical_maup_core_metrics_panel_v4.parquet"
GRID_DIR = PROJECT_DIR / "spatial/phase8/maup_grids_v1"
OUTPUT_DIR = PROJECT_DIR / "spatial/phase8/maup_global_moran_v1"

EXPECTED_HASHES = {
    "canonical_panel": "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c",
    "canonical_weights": "85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f",
    "canonical_phase5_results": "30ababa6003dc03909819563d7b8389ca11c794f9fb9ed58681f4919864966e5",
    "alternative_panel": "cdd5d4db2abb7648f8801694de93e6976d8073e271c12bd71b8c972b2a366313",
    "hex10k_base": "306eaa5d72fa57373187d42d9c4f98c3216a8b31ecc30bf4fd5e95fe7112db02",
    "hex20k_shift": "838ed063d5976b895155905821803d873b2ba0aae1cd6796b228e0302e978965",
    "hex40k_base": "57e1fde8fd61cd183acbab78f02585bd57b7e72287a70d8549ead0c33cf83e43",
}

GRID_ROWS = {"hex10k_base": 56_520, "hex20k_shift": 29_396, "hex40k_base": 15_309}
PRIMARY_ROWS = {"hex10k_base": 49_716, "hex20k_shift": 25_015, "hex40k_base": 12_445}
NEIGHBOR_DISTANCE_M = {
    "hex10k_base": 10_745.5804336879,
    "hex20k_shift": 15_196.54558489239,
    "hex40k_base": 21_491.1608673758,
}
ALTERNATIVE_GRIDS = ["hex10k_base", "hex20k_shift", "hex40k_base"]
GRID_ORDER = ["hex20k_canonical", *ALTERNATIVE_GRIDS]
EFFECT_LABEL = {
    "hex10k_base": "finer_scale_10k",
    "hex20k_shift": "zoning_shift_20k",
    "hex40k_base": "coarser_scale_40k",
}
INTERVALS = [(year, year + 5) for year in range(1985, 2025, 5)]

METRICS = {
    "consolidation_density_per_10kha": ("consolidation_ha", "complete"),
    "replenishment_density_per_10kha": ("replenishment_ha", "complete"),
    "nat_tmp_density_per_10kha": ("nat_tmp_endpoint_ha", "complete"),
    "net_cr_balance_density_per_10kha": ("net_cr_balance_ha", "complete"),
    "cr_balance_index": ("cr_balance_index", "conditional"),
}
RAW_PHASE5_METRIC = {
    "consolidation_density_per_10kha": "consolidation_ha",
    "replenishment_density_per_10kha": "replenishment_ha",
    "nat_tmp_density_per_10kha": "nat_tmp_endpoint_ha",
    "net_cr_balance_density_per_10kha": "net_cr_balance_ha",
    "cr_balance_index": "cr_balance_index",
}

CANONICAL_COLUMNS = [
    "cell_id", "t0", "t1", "diagnostic_interval", "geometry_area_aea_ha",
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
    "net_cr_balance_ha", "cr_balance_index", "cr_balance_defined",
]
ALTERNATIVE_COLUMNS = [
    "maup_cell_id", "grid_code", "t0", "t1", "diagnostic_interval",
    "raster_domain_support_ha", "domain_support_fraction", "support_ge_50pct",
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
    "net_cr_balance_ha", "cr_balance_index", "has_cr_activity",
]
GRID_COLUMNS = [
    "maup_cell_id", "maup_uid", "grid_code", "axial_q", "axial_r",
    "domain_support_fraction", "centroid_x_aea", "centroid_y_aea",
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
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    write_json(temporary, value)
    temporary.replace(path)


def standardize(binary: csr_matrix) -> tuple[csr_matrix, np.ndarray]:
    weights = binary.astype(float).tocsr()
    degree = np.asarray(weights.sum(axis=1)).ravel()
    factors = np.divide(1.0, degree, out=np.zeros_like(degree), where=degree > 0)
    weights.data *= np.repeat(factors, np.diff(weights.indptr))
    return weights, degree


def observed_moran(values: np.ndarray, weights: csr_matrix) -> float:
    values = np.asarray(values, dtype=float)
    centered = values - values.mean()
    denominator = float(centered @ centered)
    s0 = float(weights.sum())
    if len(values) < 3 or denominator == 0 or s0 == 0:
        return np.nan
    return float(len(values) / s0 * (centered @ (weights @ centered)) / denominator)


def simulate_moran(values: np.ndarray, weights: csr_matrix, permutations: int, seed: int) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    centered = values - values.mean()
    denominator = float(centered @ centered)
    s0 = float(weights.sum())
    require(len(values) >= 3 and denominator > 0 and s0 > 0, "Untestable Moran simulation")
    rng = np.random.default_rng(seed)
    simulations = np.empty(permutations, dtype=float)
    for start in range(0, permutations, 64):
        count = min(64, permutations - start)
        permuted = np.stack([rng.permutation(centered) for _ in range(count)])
        lag = (weights @ permuted.T).T
        simulations[start:start + count] = (
            len(values) / s0 / denominator * np.einsum("ij,ij->i", permuted, lag)
        )
    return simulations


def permutation_pvalue(value: float, simulations: np.ndarray, expected: float) -> float:
    tolerance = 1e-12 * max(1.0, abs(value - expected))
    extreme = np.count_nonzero(
        np.abs(simulations - expected) >= abs(value - expected) - tolerance
    )
    return float((1 + extreme) / (len(simulations) + 1))


def by_adjust(values) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    order = np.argsort(values)
    count = len(values)
    harmonic = sum(1.0 / number for number in range(1, count + 1))
    adjusted_ordered = values[order] * count * harmonic / np.arange(1, count + 1)
    adjusted_ordered = np.minimum.accumulate(adjusted_ordered[::-1])[::-1]
    adjusted = np.empty(count, dtype=float)
    adjusted[order] = np.minimum(adjusted_ordered, 1.0)
    return adjusted


def rank_correlation(first, second) -> float:
    first = pd.Series(np.asarray(first, dtype=float))
    second = pd.Series(np.asarray(second, dtype=float))
    valid = first.notna() & second.notna()
    require(valid.sum() >= 2, "Too few temporal observations")
    first = first[valid]
    second = second[valid]
    if first.nunique() == 1 and second.nunique() == 1:
        return 1.0 if np.isclose(first.iloc[0], second.iloc[0]) else 0.0
    if first.nunique() == 1 or second.nunique() == 1:
        return 0.0
    return float(first.rank(method="average").corr(second.rank(method="average")))


def sign_code(value: float) -> str:
    if not np.isfinite(value):
        return "undefined"
    if value > 1e-12:
        return "positive"
    if value < -1e-12:
        return "negative"
    return "zero"


def seed_for(grid_code: str, metric: str, t0: int) -> int:
    # Keep the accepted revision-1 seed identity so existing checkpoints and
    # any not-yet-computed test belong to one identical analytical design.
    text = f"{MASTER_SEED}|{ANALYTICAL_VERSION}|{grid_code}|{metric}|{t0}"
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:4], "little")


def graph_diagnostics(binary: csr_matrix, degree: np.ndarray) -> dict:
    components, labels = connected_components(binary, directed=False)
    largest = int(np.bincount(labels).max()) if len(labels) else 0
    unique, counts = np.unique(degree.astype(int), return_counts=True)
    return {
        "cells": int(binary.shape[0]),
        "undirected_edges": int(binary.nnz // 2),
        "components": int(components),
        "islands": int((degree == 0).sum()),
        "largest_component": largest,
        "mean_degree": float(degree.mean()) if len(degree) else np.nan,
        "degree_distribution_json": json.dumps(
            {int(key): int(value) for key, value in zip(unique, counts)}, sort_keys=True
        ),
    }


def build_canonical_graph(weights_frame: pd.DataFrame, cell_ids: list[str]):
    lookup = {cell_id: position for position, cell_id in enumerate(cell_ids)}
    frame = weights_frame.copy()
    frame["focal_cell_id"] = frame["focal_cell_id"].astype(str)
    frame["neighbor_cell_id"] = frame["neighbor_cell_id"].astype(str)
    require(len(frame) == 134_906, "Unexpected canonical directed-edge population")
    require(not frame.duplicated(["focal_cell_id", "neighbor_cell_id"]).any(), "Duplicate canonical edge")
    require(frame["focal_cell_id"].isin(cell_ids).all(), "Unknown canonical focal cell")
    require(frame["neighbor_cell_id"].isin(cell_ids).all(), "Unknown canonical neighbor cell")
    row = frame["focal_cell_id"].map(lookup).to_numpy()
    column = frame["neighbor_cell_id"].map(lookup).to_numpy()
    require((row != column).all(), "Canonical graph contains self-link")
    binary = csr_matrix((np.ones(len(frame)), (row, column)), shape=(len(cell_ids), len(cell_ids)))
    require((binary != binary.T).nnz == 0, "Canonical adjacency is not symmetric")
    standardized, degree = standardize(binary)
    diagnostics = graph_diagnostics(binary, degree)
    require(diagnostics["undirected_edges"] == 67_453, "Canonical edge count differs")
    require(diagnostics["components"] == 264, "Canonical component count differs")
    require(diagnostics["islands"] == 163, "Canonical island count differs")
    require(diagnostics["largest_component"] == 24_014, "Canonical largest component differs")
    require(
        np.allclose(standardized[row, column].A1, frame["row_standardized_weight"], atol=1e-12, rtol=0),
        "Canonical stored weights differ from row standardization",
    )
    return binary, standardized, degree, diagnostics


def build_axial_graph(grid: pd.DataFrame, grid_code: str):
    selected = grid.loc[grid["domain_support_fraction"].ge(PRIMARY_SUPPORT_THRESHOLD)].copy()
    selected.sort_values("maup_cell_id", inplace=True, ignore_index=True)
    require(len(selected) == PRIMARY_ROWS[grid_code], f"Unexpected primary population: {grid_code}")
    require(not selected.duplicated(["axial_q", "axial_r"]).any(), f"Duplicate axial coordinate: {grid_code}")
    coordinates = list(zip(selected["axial_q"].astype(int), selected["axial_r"].astype(int)))
    lookup = {coordinate: position for position, coordinate in enumerate(coordinates)}
    rows = []
    columns = []
    for position, (q_value, r_value) in enumerate(coordinates):
        for dq, dr in ((1, 0), (0, 1), (1, -1)):
            neighbor = lookup.get((q_value + dq, r_value + dr))
            if neighbor is not None:
                rows.extend((position, neighbor))
                columns.extend((neighbor, position))
    binary = csr_matrix((np.ones(len(rows)), (rows, columns)), shape=(len(selected), len(selected)))
    require((binary != binary.T).nnz == 0, f"Asymmetric alternative adjacency: {grid_code}")
    require(binary.diagonal().sum() == 0, f"Alternative graph self-link: {grid_code}")
    standardized, degree = standardize(binary)
    require(degree.max(initial=0) <= 6, f"Hexagonal degree greater than six: {grid_code}")
    edge_row, edge_column = binary.nonzero()
    forward = edge_row < edge_column
    x = selected["centroid_x_aea"].to_numpy(float)
    y = selected["centroid_y_aea"].to_numpy(float)
    distance = np.hypot(x[edge_row[forward]] - x[edge_column[forward]], y[edge_row[forward]] - y[edge_column[forward]])
    relative_error = np.abs(distance - NEIGHBOR_DISTANCE_M[grid_code]) / NEIGHBOR_DISTANCE_M[grid_code]
    require(relative_error.max(initial=0) <= 1e-6, f"Axial and geometric neighbors disagree: {grid_code}")
    diagnostics = graph_diagnostics(binary, degree)
    diagnostics["maximum_neighbor_distance_relative_error"] = float(relative_error.max(initial=0))
    return selected, binary, standardized, degree, diagnostics


def metric_values(frame: pd.DataFrame, metric: str, support_column: str) -> tuple[np.ndarray, np.ndarray]:
    source, component = METRICS[metric]
    if component == "conditional":
        flag = "cr_balance_defined" if "cr_balance_defined" in frame.columns else "has_cr_activity"
        mask = frame[flag].eq(1).to_numpy()
        values = frame[source].to_numpy(float)
    else:
        mask = np.ones(len(frame), dtype=bool)
        support = frame[support_column].to_numpy(float)
        require(np.isfinite(support).all() and (support > 0).all(), "Invalid analytical support")
        values = frame[source].to_numpy(float) / support * 10_000.0
    require(np.isfinite(values[mask]).all(), f"Non-finite supported values: {metric}")
    return values, mask


def evaluate(values: np.ndarray, mask: np.ndarray, binary: csr_matrix) -> tuple[float, csr_matrix, np.ndarray, dict]:
    selected_binary = binary[mask][:, mask]
    weights, degree = standardize(selected_binary)
    statistic = observed_moran(values[mask], weights)
    diagnostics = graph_diagnostics(selected_binary, degree)
    return statistic, weights, degree, diagnostics


def verify_engine() -> dict:
    binary = csr_matrix(np.array([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]], float))
    weights, _ = standardize(binary)
    values = np.array([1.0, 2.0, 7.0, 4.0])
    dense = weights.toarray()
    centered = values - values.mean()
    direct = 4 / dense.sum() * sum(
        dense[i, j] * centered[i] * centered[j] for i in range(4) for j in range(4)
    ) / sum(centered * centered)
    require(np.isclose(observed_moran(values, weights), direct), "Sparse/dense Moran disagreement")
    require(np.isclose(observed_moran(values, weights), observed_moran(values * 3 + 9, weights)), "Affine invariance failure")
    exact = np.array([observed_moran(np.array(permutation), weights) for permutation in itertools.permutations(values)])
    require(np.isclose(exact.mean(), -1 / 3), "Exact permutation expectation with island differs")
    require(np.isnan(observed_moran(np.ones(4), weights)), "Constant variable must be undefined")
    require(np.array_equal(simulate_moran(values, weights, 99, 19), simulate_moran(values, weights, 99, 19)), "Seed reproducibility failure")
    require(np.allclose(by_adjust([0.01, 0.02, 1.0]), [0.055, 0.055, 1.0]), "BY reference failure")
    synthetic = pd.DataFrame({
        "maup_cell_id": [1, 2, 3, 4], "maup_uid": ["a", "b", "c", "d"],
        "grid_code": ["synthetic"] * 4, "axial_q": [0, 1, 0, 2], "axial_r": [0, 0, 1, 0],
        "domain_support_fraction": [1.0] * 4, "centroid_x_aea": [0.0, 1.0, 0.5, 2.0],
        "centroid_y_aea": [0.0, 0.0, np.sqrt(3) / 2, 0.0],
    })
    coordinates = set(zip(synthetic.axial_q, synthetic.axial_r))
    expected_edges = {((0, 0), (1, 0)), ((0, 0), (0, 1)), ((0, 1), (1, 0)), ((1, 0), (2, 0))}
    recovered = set()
    for q_value, r_value in coordinates:
        for dq, dr in ((1, 0), (0, 1), (1, -1)):
            neighbor = (q_value + dq, r_value + dr)
            if neighbor in coordinates:
                recovered.add(((q_value, r_value), neighbor))
    require(recovered == expected_edges, "Axial-neighbor reference failure")
    return {
        "sparse_dense_agreement": True,
        "affine_invariance": True,
        "exhaustive_permutation_expectation_with_island": True,
        "constant_undefined": True,
        "seed_reproducible": True,
        "by_reference": True,
        "axial_neighbor_reference": True,
    }


def authenticate(path: Path, expected_hash: str, label: str) -> dict:
    require(path.is_file(), f"Missing input: {path}")
    actual = sha256_file(path)
    require(actual == expected_hash, f"Input hash mismatch: {label}")
    return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}


def read_inputs(project_dir: Path):
    canonical_panel_path = project_dir / "spatial/phase2/canonical_spatial_metrics_panel_v1.parquet"
    canonical_weights_path = project_dir / "spatial/phase1/canonical_contiguity_weights_v1.parquet"
    phase5_path = project_dir / "spatial/phase5/global_moran_v1/canonical_global_moran_results_v1.csv"
    alternative_panel_path = project_dir / "spatial/phase8/maup_metrics_v1/canonical_maup_core_metrics_panel_v4.parquet"
    grid_dir = project_dir / "spatial/phase8/maup_grids_v1"
    inputs = {
        "canonical_panel": authenticate(canonical_panel_path, EXPECTED_HASHES["canonical_panel"], "canonical panel"),
        "canonical_weights": authenticate(canonical_weights_path, EXPECTED_HASHES["canonical_weights"], "canonical weights"),
        "canonical_phase5_results": authenticate(phase5_path, EXPECTED_HASHES["canonical_phase5_results"], "Phase 5 results"),
        "alternative_panel": authenticate(alternative_panel_path, EXPECTED_HASHES["alternative_panel"], "alternative panel"),
    }
    canonical = pd.read_parquet(canonical_panel_path, columns=CANONICAL_COLUMNS)
    weights = pd.read_parquet(canonical_weights_path)
    phase5 = pd.read_csv(phase5_path)
    alternative = pd.read_parquet(alternative_panel_path, columns=ALTERNATIVE_COLUMNS)
    grids = {}
    for grid_code in ALTERNATIVE_GRIDS:
        path = grid_dir / f"maup_grid_{grid_code}_v1.parquet"
        inputs[grid_code] = authenticate(path, EXPECTED_HASHES[grid_code], grid_code)
        grids[grid_code] = pd.read_parquet(path, columns=GRID_COLUMNS)
    return canonical, weights, phase5, alternative, grids, inputs


def validate_panels(canonical: pd.DataFrame, alternative: pd.DataFrame, grids: dict) -> None:
    canonical["cell_id"] = canonical["cell_id"].astype(str)
    require(len(canonical) == 199_112, "Unexpected canonical panel rows")
    require(canonical["cell_id"].nunique() == 24_889, "Unexpected canonical cell population")
    require(not canonical.duplicated(["cell_id", "t0", "t1"]).any(), "Duplicate canonical key")
    require(set(zip(canonical.t0, canonical.t1)) == set(INTERVALS), "Unexpected canonical intervals")
    require(canonical.groupby("cell_id").size().eq(8).all(), "Unbalanced canonical panel")
    require(len(alternative) == 809_800, "Unexpected alternative panel rows")
    require(not alternative.duplicated(["grid_code", "maup_cell_id", "t0", "t1"]).any(), "Duplicate alternative key")
    require(set(alternative["grid_code"].astype(str)) == set(ALTERNATIVE_GRIDS), "Unexpected alternative grid")
    for grid_code in ALTERNATIVE_GRIDS:
        panel = alternative.loc[alternative["grid_code"].eq(grid_code)]
        grid = grids[grid_code]
        require(len(grid) == GRID_ROWS[grid_code], f"Unexpected geometry population: {grid_code}")
        require(grid["maup_cell_id"].is_unique, f"Duplicate grid ID: {grid_code}")
        require(grid["grid_code"].eq(grid_code).all(), f"Geometry grid code mismatch: {grid_code}")
        require(len(panel) == GRID_ROWS[grid_code] * 8, f"Unexpected panel population: {grid_code}")
        require(panel["maup_cell_id"].nunique() == GRID_ROWS[grid_code], f"Unexpected panel cells: {grid_code}")
        require(panel.groupby("maup_cell_id").size().eq(8).all(), f"Unbalanced alternative panel: {grid_code}")
        require(set(panel["maup_cell_id"]) == set(grid["maup_cell_id"]), f"Geometry/panel IDs differ: {grid_code}")
        support = panel.groupby("maup_cell_id", sort=False)["domain_support_fraction"].agg(["min", "max"])
        require(np.allclose(support["min"], support["max"], atol=1e-12, rtol=0), f"Temporal support changed: {grid_code}")
        require(int(panel.loc[panel.t0.eq(1985), "support_ge_50pct"].sum()) == PRIMARY_ROWS[grid_code], f"Primary population differs: {grid_code}")


def canonical_reference(canonical, weights_frame, phase5):
    cell_ids = sorted(canonical["cell_id"].unique())
    binary, weights, degree, diagnostics = build_canonical_graph(weights_frame, cell_ids)
    phase5_raw = phase5.loc[
        phase5["transformation"].eq("raw")
        & phase5["metric"].isin(RAW_PHASE5_METRIC.values())
    ].copy()
    require(len(phase5_raw) == 40, "Accepted Phase 5 reference rows differ")
    require(phase5_raw["significant_by_005"].all(), "Accepted Phase 5 focal result is not significant")
    rows = []
    maximum_raw_residual = 0.0
    for t0, t1 in INTERVALS:
        interval = canonical.loc[canonical.t0.eq(t0)].set_index("cell_id").loc[cell_ids]
        require(len(interval) == 24_889, "Canonical interval population differs")
        for metric, (source, component) in METRICS.items():
            raw_values = interval[source].to_numpy(float)
            raw_mask = interval["cr_balance_defined"].eq(1).to_numpy() if component == "conditional" else np.ones(len(interval), dtype=bool)
            raw_statistic, _, _, _ = evaluate(raw_values, raw_mask, binary)
            reference = phase5_raw.loc[
                phase5_raw.metric.eq(RAW_PHASE5_METRIC[metric]) & phase5_raw.t0.eq(t0)
            ]
            require(len(reference) == 1, f"Missing Phase 5 reference: {metric}, {t0}")
            residual = abs(raw_statistic - float(reference.iloc[0].moran_i))
            maximum_raw_residual = max(maximum_raw_residual, residual)
            values, mask = metric_values(interval, metric, "geometry_area_aea_ha")
            statistic, selected_weights, selected_degree, selected_diag = evaluate(values, mask, binary)
            require(np.isfinite(statistic), f"Undefined canonical Moran: {metric}, {t0}")
            rows.append({
                "grid_code": "hex20k_canonical", "comparison_effect": "canonical_reference",
                "metric": metric, "component": component, "t0": t0, "t1": t1,
                "interval": f"{t0}_{t1}", "diagnostic_interval": int(t0 == 2020),
                "support_rule": "complete_canonical_cells",
                "supported_cells": int(mask.sum()), "excluded_cells": int((~mask).sum()),
                **selected_diag, "s0": float(selected_weights.sum()),
                "moran_i": statistic, "expected_i": float(-1 / (mask.sum() - 1)),
                "seed": np.nan, "permutations": 9_999,
                "p_two_sided": float(reference.iloc[0].p_two_sided),
                "q_by": float(reference.iloc[0].q_by),
                "significant_by_005": bool(reference.iloc[0].significant_by_005),
                "status": "accepted_phase5_reference_reexpressed_as_density",
            })
    require(maximum_raw_residual <= 1e-12, "Canonical engine does not reproduce accepted Phase 5 Moran")
    return pd.DataFrame(rows), binary, diagnostics, maximum_raw_residual


def checkpoint_test(checkpoint_dir: Path, meta: dict, grid_code: str, metric: str, t0: int,
                    values: np.ndarray, mask: np.ndarray, binary: csr_matrix, permutations: int):
    code = f"{grid_code}__{metric}__{t0}"
    row_path = checkpoint_dir / f"{code}.json"
    simulation_path = checkpoint_dir / f"{code}.npy"
    if row_path.is_file() and simulation_path.is_file():
        row = json.loads(row_path.read_text(encoding="utf-8"))
        simulations = np.load(simulation_path)
        require(row["checkpoint_design_sha256"] == meta["checkpoint_design_sha256"], f"Checkpoint design differs: {code}")
        require(len(simulations) == permutations and np.isfinite(simulations).all(), f"Invalid checkpoint simulations: {code}")
        return row, simulations, "RESUMED"
    statistic, selected_weights, selected_degree, diagnostics = evaluate(values, mask, binary)
    require(np.isfinite(statistic), f"Undefined alternative Moran: {code}")
    seed = seed_for(grid_code, metric, t0)
    simulations = simulate_moran(values[mask], selected_weights, permutations, seed)
    expected = float(-1 / (mask.sum() - 1))
    row = {
        "checkpoint_design_sha256": meta["checkpoint_design_sha256"],
        "grid_code": grid_code, "metric": metric, "t0": t0,
        "supported_cells": int(mask.sum()), "excluded_cells": int((~mask).sum()),
        **diagnostics, "s0": float(selected_weights.sum()), "moran_i": statistic,
        "expected_i": expected, "seed": seed, "permutations": permutations,
        "p_two_sided": permutation_pvalue(statistic, simulations, expected),
        "permutation_mean": float(simulations.mean()),
        "permutation_sd": float(simulations.std(ddof=1)),
        "permutation_q025": float(np.quantile(simulations, 0.025)),
        "permutation_q975": float(np.quantile(simulations, 0.975)),
    }
    temporary = simulation_path.with_suffix(".npy.tmp")
    with temporary.open("wb") as stream:
        np.save(stream, simulations)
    temporary.replace(simulation_path)
    atomic_json(row_path, row)
    return row, simulations, "COMPUTED"


def alternative_results(alternative, grids, graphs, checkpoint_dir, checkpoint_meta, permutations):
    rows = []
    simulations = {}
    for grid_code in ALTERNATIVE_GRIDS:
        selected_grid, binary, _, _, _ = graphs[grid_code]
        selected_ids = selected_grid["maup_cell_id"].astype(int).tolist()
        grid_panel = alternative.loc[alternative["grid_code"].eq(grid_code)].copy()
        for t0, t1 in INTERVALS:
            interval = grid_panel.loc[grid_panel.t0.eq(t0)].set_index("maup_cell_id").loc[selected_ids]
            require(interval["support_ge_50pct"].eq(1).all(), f"Selected low-support cell: {grid_code}")
            for metric, (_, component) in METRICS.items():
                values, mask = metric_values(interval, metric, "raster_domain_support_ha")
                checkpoint, simulation, state = checkpoint_test(
                    checkpoint_dir, checkpoint_meta, grid_code, metric, t0,
                    values, mask, binary, permutations,
                )
                row = dict(checkpoint)
                row.pop("checkpoint_design_sha256", None)
                row.update({
                    "comparison_effect": EFFECT_LABEL[grid_code], "component": component,
                    "t1": t1, "interval": f"{t0}_{t1}",
                    "diagnostic_interval": int(t0 == 2020),
                    "support_rule": "domain_support_fraction_ge_0p50",
                    "q_by": np.nan, "significant_by_005": False, "status": "tested",
                })
                rows.append(row)
                simulations[f"{grid_code}__{metric}__{t0}"] = simulation
                print(f"{state} | {grid_code} | {metric} | {t0}–{t1} | I={row['moran_i']:.6f}", flush=True)
    result = pd.DataFrame(rows)
    result["family"] = result["component"] + "_" + np.where(result.diagnostic_interval.eq(1), "diagnostic", "primary")
    expected_sizes = {"complete_primary": 84, "conditional_primary": 21, "complete_diagnostic": 12, "conditional_diagnostic": 3}
    require(result.groupby("family").size().to_dict() == expected_sizes, "Alternative BY families differ")
    for family, index in result.groupby("family").groups.items():
        result.loc[index, "q_by"] = by_adjust(result.loc[index, "p_two_sided"].to_numpy())
    result["significant_by_005"] = result["q_by"].le(ALPHA)
    return result, simulations


def compare_results(canonical: pd.DataFrame, alternative: pd.DataFrame) -> pd.DataFrame:
    reference = canonical[["metric", "t0", "moran_i", "significant_by_005"]].rename(columns={
        "moran_i": "canonical_moran_i", "significant_by_005": "canonical_significant_by_005"
    })
    result = alternative.merge(reference, on=["metric", "t0"], how="left", validate="many_to_one")
    require(result["canonical_moran_i"].notna().all(), "Missing canonical Moran reference")
    result.rename(columns={"moran_i": "alternative_moran_i", "significant_by_005": "alternative_significant_by_005"}, inplace=True)
    result["signed_difference"] = result["alternative_moran_i"] - result["canonical_moran_i"]
    result["absolute_difference"] = result["signed_difference"].abs()
    result["absolute_difference_threshold"] = MORAN_ABSOLUTE_DIFFERENCE_THRESHOLD
    result["magnitude_pass"] = result["absolute_difference"].le(MORAN_ABSOLUTE_DIFFERENCE_THRESHOLD)
    result["canonical_sign"] = result["canonical_moran_i"].map(sign_code)
    result["alternative_sign"] = result["alternative_moran_i"].map(sign_code)
    result["sign_preserved"] = result["canonical_sign"].eq(result["alternative_sign"])
    result["significance_preserved"] = result["canonical_significant_by_005"] & result["alternative_significant_by_005"]
    result["interval_criterion_pass"] = result["magnitude_pass"] & result["sign_preserved"] & result["significance_preserved"]
    columns = [
        "grid_code", "comparison_effect", "metric", "component", "t0", "t1", "interval",
        "diagnostic_interval", "supported_cells", "excluded_cells", "components", "islands",
        "undirected_edges", "mean_degree", "canonical_moran_i", "alternative_moran_i",
        "signed_difference", "absolute_difference", "absolute_difference_threshold",
        "magnitude_pass", "canonical_sign", "alternative_sign", "sign_preserved",
        "canonical_significant_by_005", "alternative_significant_by_005",
        "significance_preserved", "interval_criterion_pass", "p_two_sided", "q_by",
    ]
    return result[columns].copy()


def temporal_comparison(comparison: pd.DataFrame) -> pd.DataFrame:
    rows = []
    windows = {"primary_1985_2020": list(range(1985, 2020, 5)), "full_observed_1985_2025": list(range(1985, 2025, 5))}
    for grid_code in ALTERNATIVE_GRIDS:
        for metric in METRICS:
            group = comparison.loc[(comparison.grid_code.eq(grid_code)) & (comparison.metric.eq(metric))].sort_values("t0")
            for window, years in windows.items():
                selected = group.loc[group.t0.isin(years)]
                require(len(selected) == len(years), f"Temporal population differs: {grid_code}, {metric}, {window}")
                canonical_values = selected["canonical_moran_i"].to_numpy(float)
                alternative_values = selected["alternative_moran_i"].to_numpy(float)
                peak_distance = abs(int(np.argmax(canonical_values)) - int(np.argmax(alternative_values)))
                trough_distance = abs(int(np.argmin(canonical_values)) - int(np.argmin(alternative_values)))
                correlation = rank_correlation(canonical_values, alternative_values)
                temporal_pass = (
                    correlation >= TEMPORAL_SPEARMAN_THRESHOLD
                    and peak_distance <= EXTREMUM_INTERVAL_DISTANCE_THRESHOLD
                    and trough_distance <= EXTREMUM_INTERVAL_DISTANCE_THRESHOLD
                )
                rows.append({
                    "grid_code": grid_code, "comparison_effect": EFFECT_LABEL[grid_code],
                    "metric": metric, "window": window, "interval_count": len(selected),
                    "spearman_rank_correlation": correlation,
                    "spearman_threshold": TEMPORAL_SPEARMAN_THRESHOLD,
                    "spearman_pass": correlation >= TEMPORAL_SPEARMAN_THRESHOLD,
                    "canonical_peak_interval": selected.iloc[int(np.argmax(canonical_values))].interval,
                    "alternative_peak_interval": selected.iloc[int(np.argmax(alternative_values))].interval,
                    "peak_interval_distance": peak_distance,
                    "canonical_trough_interval": selected.iloc[int(np.argmin(canonical_values))].interval,
                    "alternative_trough_interval": selected.iloc[int(np.argmin(alternative_values))].interval,
                    "trough_interval_distance": trough_distance,
                    "extrema_distance_threshold": EXTREMUM_INTERVAL_DISTANCE_THRESHOLD,
                    "temporal_criterion_pass": temporal_pass,
                })
    return pd.DataFrame(rows)


def assessments(comparison: pd.DataFrame, temporal: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for grid_code in ALTERNATIVE_GRIDS:
        for window, include_diagnostic in (("primary_1985_2020", False), ("full_observed_1985_2025", True)):
            interval_rows = comparison.loc[comparison.grid_code.eq(grid_code)]
            if not include_diagnostic:
                interval_rows = interval_rows.loc[interval_rows.diagnostic_interval.eq(0)]
            temporal_rows = temporal.loc[(temporal.grid_code.eq(grid_code)) & (temporal.window.eq(window))]
            interval_failed = int((~interval_rows.interval_criterion_pass).sum())
            temporal_failed = int((~temporal_rows.temporal_criterion_pass).sum())
            passed = interval_failed == 0 and temporal_failed == 0
            rows.append({
                "grid_code": grid_code, "comparison_effect": EFFECT_LABEL[grid_code], "window": window,
                "interval_checks": len(interval_rows), "interval_failed": interval_failed,
                "magnitude_failed": int((~interval_rows.magnitude_pass).sum()),
                "sign_failed": int((~interval_rows.sign_preserved).sum()),
                "significance_failed": int((~interval_rows.significance_preserved).sum()),
                "temporal_checks": len(temporal_rows), "temporal_failed": temporal_failed,
                "overall_prespecified_robustness_pass": passed,
                "assessment": "stable_under_prespecified_criteria" if passed else "sensitive_for_at_least_one_criterion",
            })
    return pd.DataFrame(rows)


def create_figures(results: pd.DataFrame, comparison: pd.DataFrame, output: Path) -> list[Path]:
    colors = {"hex20k_canonical": "#222222", "hex10k_base": "#2b8cbe", "hex20k_shift": "#7b3294", "hex40k_base": "#e34a33"}
    figure1, axes = plt.subplots(3, 2, figsize=(15, 15), sharex=True)
    for axis, metric in zip(axes.ravel(), METRICS):
        for grid_code in GRID_ORDER:
            group = results.loc[(results.grid_code.eq(grid_code)) & (results.metric.eq(metric))].sort_values("t0")
            axis.plot(group.t0, group.moran_i, marker="o", label=grid_code, color=colors[grid_code])
        axis.axhline(0, color="gray", linewidth=0.7)
        axis.axvspan(2017.5, 2022.5, color="gray", alpha=0.10)
        axis.set_title(metric)
        axis.set_ylabel("Global Moran's I")
        axis.grid(alpha=0.2)
    axes[2, 1].axis("off")
    axes[0, 0].legend(fontsize=8)
    for axis in axes[2, :1]:
        axis.set_xlabel("Initial year of five-year interval")
    figure1.suptitle("Global spatial autocorrelation across MAUP grids")
    figure1.tight_layout()
    path1 = output / "fig01_maup_global_moran_trajectories_v1.png"
    figure1.savefig(path1, dpi=180, bbox_inches="tight")
    plt.close(figure1)

    row_labels = [f"{grid} | {metric}" for grid in ALTERNATIVE_GRIDS for metric in METRICS]
    matrix = np.full((len(row_labels), len(INTERVALS)), np.nan)
    for row_index, label in enumerate(row_labels):
        grid_code, metric = label.split(" | ", 1)
        group = comparison.loc[(comparison.grid_code.eq(grid_code)) & (comparison.metric.eq(metric))].sort_values("t0")
        matrix[row_index, :] = group.signed_difference.to_numpy(float)
    limit = max(0.10, float(np.nanmax(np.abs(matrix))))
    figure2, axis = plt.subplots(figsize=(13, 9))
    image = axis.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-limit, vmax=limit)
    axis.set_yticks(np.arange(len(row_labels)), row_labels, fontsize=8)
    axis.set_xticks(np.arange(len(INTERVALS)), [f"{a}_{b}" for a, b in INTERVALS], rotation=45, ha="right")
    axis.set_title("Alternative minus canonical Global Moran's I")
    colorbar = figure2.colorbar(image, ax=axis)
    colorbar.set_label("Signed difference in Moran's I")
    figure2.tight_layout()
    path2 = output / "fig02_maup_global_moran_difference_heatmap_v1.png"
    figure2.savefig(path2, dpi=180, bbox_inches="tight")
    plt.close(figure2)
    return [path1, path2]


def run(args) -> None:
    print("CANONICAL MAUP GLOBAL MORAN — PHASE 8D VERSION 1", flush=True)
    print("SCRIPT REVISION 2 — FINAL JSON NON-FINITE VALUE FIX", flush=True)
    print("GLOBAL BEFORE LOCAL; 9,999 PERMUTATIONS; CHECKPOINT RESUME ENABLED", flush=True)
    print("PRIMARY ALTERNATIVE SUPPORT: DOMAIN FRACTION >= 0.50", flush=True)
    print("Script version:", VERSION, flush=True)
    engine_checks = verify_engine()
    print("Statistical and axial-graph engine verification: PASS", flush=True)
    project_dir = args.project_dir
    if not project_dir.exists() and str(project_dir).startswith("/content/drive/"):
        from google.colab import drive
        drive.mount("/content/drive")
    output = args.output_dir or project_dir / "spatial/phase8/maup_global_moran_v1"
    output.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = output / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    canonical, weights_frame, phase5, alternative, grids, inputs = read_inputs(project_dir)
    validate_panels(canonical, alternative, grids)
    canonical_results, _, canonical_graph_diagnostics, maximum_raw_residual = canonical_reference(canonical, weights_frame, phase5)
    print("Canonical Phase 5 reproduction: PASS", flush=True)
    graph_objects = {}
    graph_rows = [{
        "grid_code": "hex20k_canonical",
        "support_rule": "complete_canonical_cells",
        "maximum_neighbor_distance_relative_error": 0.0,
        **canonical_graph_diagnostics,
    }]
    for grid_code in ALTERNATIVE_GRIDS:
        graph = build_axial_graph(grids[grid_code], grid_code)
        graph_objects[grid_code] = graph
        graph_rows.append({"grid_code": grid_code, "support_rule": "domain_support_fraction_ge_0p50", **graph[4]})
        print("GRAPH", grid_code, "| cells =", f"{graph[4]['cells']:,}", "| edges =", f"{graph[4]['undirected_edges']:,}", flush=True)
    graph_summary = pd.DataFrame(graph_rows)
    checkpoint_design = {
        # This key intentionally retains the revision-1 analytical identity.
        # It makes the serialization-only revision compatible with completed
        # revision-1 checkpoints.
        "script_version": ANALYTICAL_VERSION, "permutations": args.permutations,
        "master_seed": MASTER_SEED, "support_threshold": PRIMARY_SUPPORT_THRESHOLD,
        "metrics": list(METRICS), "input_hashes": {key: value["sha256"] for key, value in inputs.items()},
    }
    checkpoint_design_text = json.dumps(checkpoint_design, sort_keys=True, separators=(",", ":"))
    checkpoint_design["checkpoint_design_sha256"] = hashlib.sha256(checkpoint_design_text.encode()).hexdigest()
    meta_path = checkpoint_dir / "checkpoint_design_v1.json"
    if meta_path.is_file():
        existing = json.loads(meta_path.read_text(encoding="utf-8"))
        require(existing == checkpoint_design, "Existing checkpoints belong to a different design")
    else:
        atomic_json(meta_path, checkpoint_design)
    alternative_result, simulations = alternative_results(
        alternative, grids, graph_objects, checkpoint_dir, checkpoint_design, args.permutations
    )
    combined_results = pd.concat([canonical_results, alternative_result], ignore_index=True, sort=False)
    require(len(combined_results) == 160, "Unexpected Moran result population")
    comparison = compare_results(canonical_results, alternative_result)
    require(len(comparison) == 120, "Unexpected interval comparison population")
    temporal = temporal_comparison(comparison)
    require(len(temporal) == 30, "Unexpected temporal comparison population")
    assessment = assessments(comparison, temporal)
    require(len(assessment) == 6, "Unexpected assessment population")

    result_path = output / "canonical_maup_global_moran_results_v1.csv"
    comparison_path = output / "canonical_maup_global_moran_comparison_v1.csv"
    temporal_path = output / "canonical_maup_global_moran_temporal_comparison_v1.csv"
    assessment_path = output / "canonical_maup_global_moran_assessment_v1.csv"
    graph_path = output / "canonical_maup_global_moran_graph_summary_v1.csv"
    permutation_path = output / "canonical_maup_global_moran_permutations_v1.npz"
    combined_results.to_csv(result_path, index=False, float_format="%.17g")
    comparison.to_csv(comparison_path, index=False, float_format="%.17g")
    temporal.to_csv(temporal_path, index=False, float_format="%.17g")
    assessment.to_csv(assessment_path, index=False)
    graph_summary.to_csv(graph_path, index=False, float_format="%.17g")
    np.savez_compressed(permutation_path, **simulations)
    figure_paths = create_figures(combined_results, comparison, output)

    output_paths = [result_path, comparison_path, temporal_path, assessment_path, graph_path, permutation_path, *figure_paths]
    validation_path = output / "canonical_maup_global_moran_validation_v1.json"
    validation = {
        "validation_status": "PASS", "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": sha256_file(Path(__file__)),
        "inputs": inputs, "engine_checks": engine_checks,
        "design": {
            "analytical_version": ANALYTICAL_VERSION,
            "permutations": args.permutations, "master_seed": MASTER_SEED,
            "alternative_support_threshold": PRIMARY_SUPPORT_THRESHOLD,
            "metrics": list(METRICS), "moran_absolute_difference_threshold": MORAN_ABSOLUTE_DIFFERENCE_THRESHOLD,
            "temporal_spearman_threshold": TEMPORAL_SPEARMAN_THRESHOLD,
            "extremum_interval_distance_threshold": EXTREMUM_INTERVAL_DISTANCE_THRESHOLD,
            "multiple_testing": "Benjamini-Yekutieli across all three alternative grids; complete/conditional and primary/diagnostic separate",
        },
        "structure": {
            "result_rows": len(combined_results), "comparison_rows": len(comparison),
            "temporal_rows": len(temporal), "assessment_rows": len(assessment),
            "alternative_permutation_distributions": len(simulations),
            "simulated_statistics": int(sum(len(value) for value in simulations.values())),
        },
        "canonical_reproduction": {"maximum_absolute_raw_moran_residual": maximum_raw_residual},
        "graphs": graph_summary.to_dict("records"),
        "result_counts": {
            "alternative_significant_by": int(alternative_result.significant_by_005.sum()),
            "interval_failed": int((~comparison.interval_criterion_pass).sum()),
            "temporal_failed": int((~temporal.temporal_criterion_pass).sum()),
            "assessments_passing": int(assessment.overall_prespecified_robustness_pass.sum()),
        },
        "checks": {
            "input_hashes_match": True, "panel_populations_match": True,
            "canonical_graph_matches_phase1": True, "alternative_axial_graphs_match_geometry": True,
            "support_threshold_populations_match_phase8a": True,
            "canonical_engine_reproduces_phase5": True,
            "density_normalization_applied_to_area_metrics": True,
            "conditional_balance_support_preserved": True,
            "primary_and_diagnostic_families_are_separate": True,
            "checkpoint_design_authenticated": True,
            "sensitivity_is_reported_as_result_not_validation_error": True,
        },
        "outputs": {path.name: {"bytes": path.stat().st_size, "sha256": sha256_file(path)} for path in output_paths},
    }
    write_json(validation_path, validation)
    inventory_rows = []
    for path in [*output_paths, validation_path]:
        inventory_rows.append({"relative_path": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    inventory_path = output / "canonical_maup_global_moran_inventory_v1.csv"
    pd.DataFrame(inventory_rows).to_csv(inventory_path, index=False)
    print("PHASE 8D GLOBAL MORAN COMPLETE — VALIDATION PASS", flush=True)
    print("Results:", f"{len(combined_results):,}", flush=True)
    print("Comparisons:", f"{len(comparison):,}", flush=True)
    print("Temporal comparisons:", f"{len(temporal):,}", flush=True)
    for row in assessment.itertuples(index=False):
        print("ASSESSMENT |", row.grid_code, "|", row.window, "|", row.assessment, flush=True)
    print("Validation:", validation_path, flush=True)
    print("Inventory:", inventory_path, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        print(json.dumps(verify_engine(), indent=2))
    else:
        require(arguments.permutations == PERMUTATIONS, "Production requires prespecified 9,999 permutations")
        run(arguments)

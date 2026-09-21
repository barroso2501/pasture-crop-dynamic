"""Phase 8E: broad HH-cluster location and persistence across MAUP grids.

Colab
------
%pip install -q esda==2.7.1 libpysal==4.13.0 pyarrow geopandas shapely
%run /content/14c_compare_maup_hh_clusters_v1.py --mode pilot
%run /content/14c_compare_maup_hh_clusters_v1.py --mode full

The pilot computes one production test and its spatial crosswalk. The full run
reuses that checkpoint and completes 120 alternative-grid Local Moran maps.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.stats import rankdata

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


VERSION = "phase8e-maup-hh-cluster-robustness-v1"
MASTER_SEED = 20260921
PERMUTATIONS = 9_999
ALPHA = 0.05
PRIMARY_SUPPORT_THRESHOLD = 0.50
JACCARD_THRESHOLD = 0.40
OVERLAP_COEFFICIENT_THRESHOLD = 0.60
FREQUENCY_SPEARMAN_THRESHOLD = 0.70
PRIMARY_INTERVAL_PASSES_REQUIRED = 5
FULL_INTERVAL_PASSES_REQUIRED = 6
AEA = "+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"

PROJECT_DIR = Path("/content/drive/MyDrive/Trabalho/Contabilidade")
OUTPUT_RELATIVE = Path("spatial/phase8/maup_cluster_robustness_v1")

EXPECTED_HASHES = {
    "canonical_local": "ec5906cb86e4044082db91d4cf11440b0d5401f6f8b6484217c7e246449ca2b4",
    "canonical_spatial": "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc",
    "alternative_panel": "cdd5d4db2abb7648f8801694de93e6976d8073e271c12bd71b8c972b2a366313",
    "hex10k_base": "306eaa5d72fa57373187d42d9c4f98c3216a8b31ecc30bf4fd5e95fe7112db02",
    "hex20k_shift": "838ed063d5976b895155905821803d873b2ba0aae1cd6796b228e0302e978965",
    "hex40k_base": "57e1fde8fd61cd183acbab78f02585bd57b7e72287a70d8549ead0c33cf83e43",
}

GRIDS = ["hex10k_base", "hex20k_shift", "hex40k_base"]
GRID_ROWS = {"hex10k_base": 56_520, "hex20k_shift": 29_396, "hex40k_base": 15_309}
PRIMARY_ROWS = {"hex10k_base": 49_716, "hex20k_shift": 25_015, "hex40k_base": 12_445}
INTERVALS = [(year, year + 5) for year in range(1985, 2025, 5)]
PRIMARY_T0 = list(range(1985, 2020, 5))
FULL_T0 = list(range(1985, 2025, 5))
QUADRANTS = {1: "HH", 2: "LH", 3: "LL", 4: "HL"}

METRICS = {
    "consolidation_density_per_10kha": ("consolidation_ha", "consolidation_ha", "complete"),
    "replenishment_density_per_10kha": ("replenishment_ha", "replenishment_ha", "complete"),
    "nat_tmp_density_per_10kha": ("nat_tmp_endpoint_ha", "nat_tmp_endpoint_ha", "complete"),
    "net_cr_balance_density_per_10kha": ("net_cr_balance_ha", "net_cr_balance_ha", "complete"),
    "cr_balance_index": ("cr_balance_index", "cr_balance_index", "conditional"),
}

PILOT_GRID = "hex20k_shift"
PILOT_METRIC = "nat_tmp_density_per_10kha"
PILOT_T0 = 2005


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


def authenticate(path: Path, expected: str, label: str) -> dict:
    require(path.is_file(), f"Missing input: {path}")
    actual = sha256_file(path)
    require(actual == expected, f"Input hash mismatch: {label}")
    return {"path": str(path), "sha256": actual, "bytes": path.stat().st_size}


def fdr_adjust(values, method: str) -> np.ndarray:
    p = np.asarray(values, dtype=float)
    require(p.ndim == 1 and len(p) > 0 and np.isfinite(p).all(), "Invalid p-values")
    require(((p >= 0) & (p <= 1)).all(), "p-values outside [0,1]")
    order = np.argsort(p, kind="mergesort")
    ranks = np.arange(1, len(p) + 1, dtype=float)
    factor = 1.0 if method == "bh" else float(np.sum(1.0 / ranks))
    adjusted = p[order] * len(p) * factor / ranks
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    result = np.empty(len(p), dtype=float)
    result[order] = np.minimum(adjusted, 1.0)
    return result


def stable_seed(grid_code: str, metric: str, t0: int) -> int:
    token = f"{MASTER_SEED}|{VERSION}|{grid_code}|{metric}|{t0}".encode()
    return int.from_bytes(hashlib.sha256(token).digest()[:4], "little")


def max_run(sequence, target="HH") -> int:
    best = current = 0
    for value in sequence:
        current = current + 1 if value == target else 0
        best = max(best, current)
    return best


def weighted_correlation(first, second, weights) -> float:
    first = np.asarray(first, dtype=float)
    second = np.asarray(second, dtype=float)
    weights = np.asarray(weights, dtype=float)
    valid = np.isfinite(first) & np.isfinite(second) & np.isfinite(weights) & (weights > 0)
    require(valid.sum() >= 3, "Too few values for weighted correlation")
    first, second, weights = first[valid], second[valid], weights[valid]
    if np.ptp(first) == 0 and np.ptp(second) == 0:
        return 1.0 if np.isclose(first[0], second[0]) else 0.0
    if np.ptp(first) == 0 or np.ptp(second) == 0:
        return 0.0
    weights = weights / weights.sum()
    first_centered = first - np.sum(weights * first)
    second_centered = second - np.sum(weights * second)
    denominator = np.sqrt(np.sum(weights * first_centered**2) * np.sum(weights * second_centered**2))
    return float(np.sum(weights * first_centered * second_centered) / denominator)


def weighted_spearman(first, second, weights) -> float:
    return weighted_correlation(rankdata(first, method="average"), rankdata(second, method="average"), weights)


def verify_engine() -> dict:
    require(np.allclose(fdr_adjust([0.01, 0.02, 1.0], "bh"), [0.03, 0.03, 1.0]), "BH reference failure")
    require(np.allclose(fdr_adjust([0.01, 0.02, 1.0], "by"), [0.055, 0.055, 1.0]), "BY reference failure")
    require(max_run(["HH", "HH", "LL", "HH"]) == 2, "Run reference failure")
    require(np.isclose(weighted_spearman([1, 2, 3], [1, 2, 3], [1, 2, 1]), 1.0), "Weighted rank failure")
    try:
        from esda import Moran_Local
        from libpysal.weights import W
    except ImportError as exc:
        raise RuntimeError("Install esda==2.7.1 and libpysal==4.13.0") from exc
    weights = W({"a": ["b"], "b": ["a", "c"], "c": ["b"], "d": []},
                id_order=["a", "b", "c", "d"], silence_warnings=True)
    model = Moran_Local(np.array([1.0, 2.0, 7.0, 4.0]), weights, transformation="r",
                        permutations=99, geoda_quads=False, n_jobs=1,
                        keep_simulations=False, seed=19, island_weight=0)
    require(model.q.tolist() == [3, 2, 4, 4], "PySAL quadrant convention changed")
    return {
        "bh_reference": True, "by_reference": True, "run_reference": True,
        "weighted_spearman_reference": True,
        "pysal_quadrants": {str(key): value for key, value in QUADRANTS.items()},
    }


def read_inputs(project_dir: Path):
    import geopandas as gpd
    local_path = project_dir / "spatial/phase6/local_moran_v1/canonical_local_moran_cell_results_v1.parquet"
    spatial_path = project_dir / "spatial/phase1/canonical_spatial_support_v1.parquet"
    panel_path = project_dir / "spatial/phase8/maup_metrics_v1/canonical_maup_core_metrics_panel_v4.parquet"
    grid_dir = project_dir / "spatial/phase8/maup_grids_v1"
    inputs = {
        "canonical_local": authenticate(local_path, EXPECTED_HASHES["canonical_local"], "canonical Local Moran"),
        "canonical_spatial": authenticate(spatial_path, EXPECTED_HASHES["canonical_spatial"], "canonical spatial support"),
        "alternative_panel": authenticate(panel_path, EXPECTED_HASHES["alternative_panel"], "alternative metric panel"),
    }
    canonical_local = pd.read_parquet(local_path, columns=[
        "cell_id", "metric", "t0", "t1", "diagnostic_interval", "quadrant_code",
        "significant_bh_005", "significant_by_005", "lisa_class", "analysis_status",
    ])
    canonical_spatial = gpd.read_parquet(spatial_path, columns=["cell_id", "geometry_area_aea_ha", "geometry"])
    alternative = pd.read_parquet(panel_path, columns=[
        "maup_cell_id", "grid_code", "t0", "t1", "diagnostic_interval",
        "raster_domain_support_ha", "domain_support_fraction", "support_ge_50pct",
        "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
        "net_cr_balance_ha", "cr_balance_index", "has_cr_activity",
    ])
    grids = {}
    for grid_code in GRIDS:
        path = grid_dir / f"maup_grid_{grid_code}_v1.parquet"
        inputs[grid_code] = authenticate(path, EXPECTED_HASHES[grid_code], grid_code)
        grids[grid_code] = gpd.read_parquet(path, columns=[
            "maup_cell_id", "maup_uid", "grid_code", "axial_q", "axial_r",
            "domain_support_fraction", "vector_domain_support_ha", "geometry",
        ])
    return canonical_local, canonical_spatial, alternative, grids, inputs


def validate_inputs(canonical_local, canonical_spatial, alternative, grids) -> None:
    canonical_local["cell_id"] = canonical_local["cell_id"].astype(str)
    canonical_spatial["cell_id"] = canonical_spatial["cell_id"].astype(str)
    require(len(canonical_local) == 995_560, "Unexpected canonical Local Moran rows")
    require(canonical_local["cell_id"].nunique() == 24_889, "Unexpected canonical cell population")
    require(not canonical_local.duplicated(["cell_id", "metric", "t0"]).any(), "Duplicate canonical Local Moran key")
    require(len(canonical_spatial) == 24_889 and canonical_spatial["cell_id"].is_unique, "Invalid canonical geometry")
    require(set(canonical_local["cell_id"]) == set(canonical_spatial["cell_id"]), "Canonical populations differ")
    require(len(alternative) == 809_800, "Unexpected alternative panel rows")
    require(not alternative.duplicated(["grid_code", "maup_cell_id", "t0"]).any(), "Duplicate alternative panel key")
    for grid_code in GRIDS:
        grid = grids[grid_code]
        panel = alternative.loc[alternative.grid_code.eq(grid_code)]
        require(len(grid) == GRID_ROWS[grid_code] and grid.maup_cell_id.is_unique, f"Invalid grid: {grid_code}")
        require(len(panel) == GRID_ROWS[grid_code] * 8, f"Invalid panel rows: {grid_code}")
        require(panel.maup_cell_id.nunique() == GRID_ROWS[grid_code], f"Invalid panel cells: {grid_code}")
        require(set(panel.maup_cell_id) == set(grid.maup_cell_id), f"Grid/panel cells differ: {grid_code}")
        require(int(grid.domain_support_fraction.ge(PRIMARY_SUPPORT_THRESHOLD).sum()) == PRIMARY_ROWS[grid_code],
                f"Primary support population differs: {grid_code}")


def build_graph(grid, grid_code: str):
    selected = grid.loc[grid.domain_support_fraction.ge(PRIMARY_SUPPORT_THRESHOLD)].copy()
    selected.sort_values("maup_cell_id", inplace=True, ignore_index=True)
    coordinates = list(zip(selected.axial_q.astype(int), selected.axial_r.astype(int)))
    require(len(set(coordinates)) == len(coordinates), f"Duplicate axial coordinate: {grid_code}")
    lookup = {coordinate: position for position, coordinate in enumerate(coordinates)}
    rows, columns = [], []
    for position, (q_value, r_value) in enumerate(coordinates):
        for dq, dr in ((1, 0), (0, 1), (1, -1)):
            neighbor = lookup.get((q_value + dq, r_value + dr))
            if neighbor is not None:
                rows.extend((position, neighbor)); columns.extend((neighbor, position))
    binary = csr_matrix((np.ones(len(rows), dtype=np.int8), (rows, columns)),
                        shape=(len(selected), len(selected)))
    require((binary != binary.T).nnz == 0 and binary.diagonal().sum() == 0, f"Invalid graph: {grid_code}")
    degree = np.asarray(binary.sum(axis=1)).ravel().astype(int)
    require(degree.max(initial=0) <= 6, f"Degree above six: {grid_code}")
    return selected, binary, degree


def make_weights(ids, binary):
    from libpysal.weights import W
    ids = list(ids)
    neighbors = {}
    for position, identifier in enumerate(ids):
        start, end = binary.indptr[position], binary.indptr[position + 1]
        neighbors[identifier] = [ids[index] for index in binary.indices[start:end]]
    return W(neighbors, id_order=ids, silence_warnings=True)


def metric_values(interval, metric: str):
    _, alternative_field, component = METRICS[metric]
    if component == "conditional":
        supported = interval.has_cr_activity.eq(1).to_numpy()
        values = interval[alternative_field].to_numpy(float)
    else:
        supported = np.ones(len(interval), dtype=bool)
        denominator = interval.raster_domain_support_ha.to_numpy(float)
        require(np.isfinite(denominator).all() and (denominator > 0).all(), "Invalid raster support")
        values = interval[alternative_field].to_numpy(float) / denominator * 10_000.0
    require(np.isfinite(values[supported]).all(), f"Non-finite supported values: {metric}")
    return values, supported


def checkpoint_config(inputs, grid_code, metric, t0):
    return {
        "analytical_version": VERSION, "input_hashes": {key: value["sha256"] for key, value in inputs.items()},
        "grid_code": grid_code, "metric": metric, "t0": int(t0), "t1": int(t0 + 5),
        "support_threshold": PRIMARY_SUPPORT_THRESHOLD, "permutations": PERMUTATIONS,
        "seed": stable_seed(grid_code, metric, t0), "transformation": "row-standardized",
        "permutation_null": "PySAL conditional randomization at each location",
        "fdr_primary": "BH within grid x metric x interval", "fdr_sensitivity": "BY within same map",
        "alpha": ALPHA, "island_weight": 0, "geoda_quads": False,
    }


def read_checkpoint(data_path, meta_path, expected, expected_rows):
    if not data_path.exists() and not meta_path.exists():
        return None
    require(data_path.exists() and meta_path.exists(), f"Incomplete checkpoint: {data_path.stem}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    require(meta.get("config") == expected, f"Checkpoint configuration differs: {data_path.stem}")
    require(meta.get("parquet_sha256") == sha256_file(data_path), f"Checkpoint hash differs: {data_path.stem}")
    frame = pd.read_parquet(data_path)
    require(len(frame) == expected_rows and frame.maup_cell_id.is_unique, f"Checkpoint population differs: {data_path.stem}")
    return frame


def compute_local_map(grid_code, metric, t0, selected, binary, degree_full, panel):
    from esda import Moran_Local
    ids = selected.maup_cell_id.astype(int).to_numpy()
    interval = panel.loc[(panel.grid_code.eq(grid_code)) & panel.t0.eq(t0)].set_index("maup_cell_id").loc[ids]
    require(interval.support_ge_50pct.eq(1).all(), f"Low-support selected cell: {grid_code}")
    values, supported = metric_values(interval, metric)
    selected_ids = ids[supported].tolist()
    selected_binary = binary[supported][:, supported].tocsr()
    weights = make_weights(selected_ids, selected_binary)
    local_degree = np.asarray(selected_binary.sum(axis=1)).ravel().astype(int)
    model = Moran_Local(values[supported], weights, transformation="r", permutations=PERMUTATIONS,
                        geoda_quads=False, n_jobs=1, keep_simulations=False,
                        seed=stable_seed(grid_code, metric, t0), island_weight=0)
    tested = local_degree > 0
    p_sim = np.asarray(model.p_sim, dtype=float)
    require(np.isfinite(p_sim[tested]).all(), "Non-finite tested pseudo p-values")
    q_bh = np.full(len(selected_ids), np.nan); q_by = np.full(len(selected_ids), np.nan)
    q_bh[tested] = fdr_adjust(p_sim[tested], "bh")
    q_by[tested] = fdr_adjust(p_sim[tested], "by")
    quadrant = np.asarray(model.q, dtype=int)
    class_bh = np.array([QUADRANTS.get(int(value), "not_significant") for value in quadrant], dtype=object)
    class_by = class_bh.copy()
    class_bh[~(tested & (q_bh <= ALPHA))] = "not_significant"
    class_by[~(tested & (q_by <= ALPHA))] = "not_significant"
    spatial_lag = np.asarray(weights.sparse @ model.z).ravel()
    output = pd.DataFrame({
        "maup_cell_id": ids, "grid_code": grid_code, "metric": metric, "t0": t0, "t1": t0 + 5,
        "diagnostic_interval": int(t0 == 2020), "metric_value": values,
        "supported_flag": supported.astype(np.int8), "full_graph_degree": degree_full,
        "local_graph_degree": np.nan, "island_flag": 0, "z_score": np.nan,
        "spatial_lag_z": np.nan, "local_moran_i": np.nan, "quadrant_code": 0,
        "p_sim": np.nan, "q_bh": np.nan, "q_by": np.nan,
        "significant_bh_005": 0, "significant_by_005": 0,
        "lisa_class_bh": "not_applicable", "lisa_class_by": "not_applicable",
        "analysis_status": "unsupported", "seed": stable_seed(grid_code, metric, t0),
        "permutations": PERMUTATIONS,
    })
    location = np.flatnonzero(supported)
    output.loc[location, "local_graph_degree"] = local_degree
    output.loc[location, "island_flag"] = (local_degree == 0).astype(np.int8)
    output.loc[location, "z_score"] = model.z
    output.loc[location, "spatial_lag_z"] = spatial_lag
    output.loc[location, "local_moran_i"] = model.Is
    output.loc[location, "quadrant_code"] = quadrant
    output.loc[location, "p_sim"] = np.where(tested, p_sim, np.nan)
    output.loc[location, "q_bh"] = q_bh; output.loc[location, "q_by"] = q_by
    output.loc[location, "significant_bh_005"] = (tested & (q_bh <= ALPHA)).astype(np.int8)
    output.loc[location, "significant_by_005"] = (tested & (q_by <= ALPHA)).astype(np.int8)
    output.loc[location, "lisa_class_bh"] = class_bh; output.loc[location, "lisa_class_by"] = class_by
    output.loc[location, "analysis_status"] = np.where(tested, "tested", "island")
    require(output.loc[output.island_flag.eq(1), "significant_bh_005"].eq(0).all(), "Island significant under BH")
    return output


def build_or_read_crosswalk(grid_code, selected, canonical_spatial, cache_dir):
    import geopandas as gpd
    path = cache_dir / f"crosswalk_canonical__{grid_code}_v1.parquet"
    meta_path = cache_dir / f"crosswalk_canonical__{grid_code}_v1.json"
    expected = {
        "version": VERSION, "grid_code": grid_code,
        "canonical_spatial_sha256": EXPECTED_HASHES["canonical_spatial"],
        "alternative_grid_sha256": EXPECTED_HASHES[grid_code],
        "support_threshold": PRIMARY_SUPPORT_THRESHOLD, "crs": AEA,
    }
    if path.is_file() and meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        require(meta.get("config") == expected, f"Crosswalk configuration differs: {grid_code}")
        require(meta.get("parquet_sha256") == sha256_file(path), f"Crosswalk hash differs: {grid_code}")
        return pd.read_parquet(path), meta, "REUSED"
    canonical = canonical_spatial[["cell_id", "geometry"]].copy()
    alternative = selected[["maup_cell_id", "geometry"]].copy()
    if canonical.crs is None or alternative.crs is None:
        raise ValueError("Missing geometry CRS")
    canonical = canonical.to_crs(AEA); alternative = alternative.to_crs(AEA)
    pieces = gpd.overlay(canonical, alternative, how="intersection", keep_geom_type=False)
    pieces["overlap_ha"] = pieces.geometry.area / 10_000.0
    pieces = pieces.loc[pieces.overlap_ha.gt(1e-8), ["cell_id", "maup_cell_id", "overlap_ha"]].copy()
    pieces["cell_id"] = pieces.cell_id.astype(str); pieces["maup_cell_id"] = pieces.maup_cell_id.astype(int)
    require(not pieces.duplicated(["cell_id", "maup_cell_id"]).any(), f"Duplicate crosswalk pair: {grid_code}")
    expected_area = float(selected.vector_domain_support_ha.sum())
    observed_area = float(pieces.overlap_ha.sum())
    relative_error = abs(observed_area - expected_area) / expected_area
    require(relative_error <= 2e-6, f"Crosswalk area closure failed: {grid_code}")
    pieces.to_parquet(path, index=False, compression="zstd")
    meta = {
        "config": expected, "rows": len(pieces), "shared_support_ha": observed_area,
        "expected_selected_domain_intersection_ha": expected_area,
        "relative_area_closure_error": relative_error,
        "parquet_sha256": sha256_file(path), "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    atomic_json(meta_path, meta)
    return pieces, meta, "COMPUTED"


def canonical_classes(canonical_local):
    frame = canonical_local.loc[canonical_local.metric.isin([value[0] for value in METRICS.values()])].copy()
    reverse = {value[0]: key for key, value in METRICS.items()}
    frame["metric_comparison"] = frame.metric.map(reverse)
    frame["lisa_class_bh"] = frame.lisa_class
    raw = frame.quadrant_code.map(QUADRANTS).fillna("not_significant")
    frame["lisa_class_by"] = np.where(frame.significant_by_005.eq(1), raw, "not_significant")
    frame.loc[frame.analysis_status.eq("unsupported"), "lisa_class_by"] = "not_applicable"
    require(len(frame) == 24_889 * 5 * 8, "Canonical focal result population differs")
    return frame


def footprint_metrics(crosswalk, canonical_ids, alternative_ids):
    canonical_hit = crosswalk.cell_id.isin(set(canonical_ids)).to_numpy()
    alternative_hit = crosswalk.maup_cell_id.isin(set(alternative_ids)).to_numpy()
    area = crosswalk.overlap_ha.to_numpy(float)
    canonical_area = float(area[canonical_hit].sum())
    alternative_area = float(area[alternative_hit].sum())
    intersection = float(area[canonical_hit & alternative_hit].sum())
    union = float(area[canonical_hit | alternative_hit].sum())
    if union == 0:
        jaccard = 1.0
    else:
        jaccard = intersection / union
    if canonical_area == 0 and alternative_area == 0:
        overlap = 1.0
    elif min(canonical_area, alternative_area) == 0:
        overlap = 0.0
    else:
        overlap = intersection / min(canonical_area, alternative_area)
    recall = intersection / canonical_area if canonical_area > 0 else (1.0 if alternative_area == 0 else 0.0)
    precision = intersection / alternative_area if alternative_area > 0 else (1.0 if canonical_area == 0 else 0.0)
    passed = jaccard >= JACCARD_THRESHOLD and overlap >= OVERLAP_COEFFICIENT_THRESHOLD
    return {
        "canonical_hh_area_ha": canonical_area, "alternative_hh_area_ha": alternative_area,
        "intersection_ha": intersection, "union_ha": union, "jaccard": jaccard,
        "overlap_coefficient": overlap, "canonical_capture": recall,
        "alternative_precision": precision, "footprint_ratio_alternative_to_canonical":
            alternative_area / canonical_area if canonical_area > 0 else None,
        "jaccard_threshold": JACCARD_THRESHOLD,
        "overlap_coefficient_threshold": OVERLAP_COEFFICIENT_THRESHOLD,
        "location_criterion_pass": bool(passed),
    }


def interval_comparisons(canonical, alternatives, crosswalks):
    rows = []
    for grid_code in GRIDS:
        alternative = alternatives[grid_code]
        crosswalk = crosswalks[grid_code]
        for metric in METRICS:
            for t0, t1 in INTERVALS:
                can = canonical.loc[(canonical.metric_comparison.eq(metric)) & canonical.t0.eq(t0)]
                alt = alternative.loc[(alternative.metric.eq(metric)) & alternative.t0.eq(t0)]
                for inference, can_col, alt_col in [
                    ("BH", "lisa_class_bh", "lisa_class_bh"),
                    ("BY", "lisa_class_by", "lisa_class_by"),
                ]:
                    metrics = footprint_metrics(
                        crosswalk, can.loc[can[can_col].eq("HH"), "cell_id"],
                        alt.loc[alt[alt_col].eq("HH"), "maup_cell_id"],
                    )
                    rows.append({
                        "grid_code": grid_code, "metric": metric, "t0": t0, "t1": t1,
                        "interval": f"{t0}_{t1}", "diagnostic_interval": int(t0 == 2020),
                        "inference": inference, "primary_inference": int(inference == "BH"),
                        "shared_support_ha": float(crosswalk.overlap_ha.sum()), **metrics,
                    })
    result = pd.DataFrame(rows)
    require(len(result) == 3 * 5 * 8 * 2, "Interval comparison population differs")
    return result


def trajectory_metrics(frame, id_column, metric_column, class_column, years):
    subset = frame.loc[frame.t0.isin(years), [id_column, metric_column, "t0", class_column]].copy()
    output = []
    for metric, group in subset.groupby(metric_column, sort=False):
        pivot = group.pivot(index=id_column, columns="t0", values=class_column).reindex(columns=years)
        require(not pivot.isna().any().any(), f"Incomplete trajectory: {metric}")
        matrix = pivot.to_numpy(object)
        hh = matrix == "HH"
        frequency = hh.sum(axis=1).astype(int)
        runs = np.array([max_run(row.tolist(), "HH") for row in matrix], dtype=int)
        part = pd.DataFrame({id_column: pivot.index, "metric": metric,
                             "hh_frequency": frequency, "max_hh_run": runs,
                             "persistent_hh_2plus": (runs >= 2).astype(np.int8)})
        output.append(part)
    return pd.concat(output, ignore_index=True)


def temporal_comparisons(canonical, alternatives, crosswalks):
    rows = []
    for inference, canonical_class, alternative_class in [
        ("BH", "lisa_class_bh", "lisa_class_bh"), ("BY", "lisa_class_by", "lisa_class_by")
    ]:
        for window, years in [("primary_1985_2020", PRIMARY_T0), ("full_observed_1985_2025", FULL_T0)]:
            can_traj = trajectory_metrics(canonical, "cell_id", "metric_comparison", canonical_class, years)
            for grid_code in GRIDS:
                alt_traj = trajectory_metrics(alternatives[grid_code], "maup_cell_id", "metric", alternative_class, years)
                crosswalk = crosswalks[grid_code]
                for metric in METRICS:
                    can = can_traj.loc[can_traj.metric.eq(metric)].set_index("cell_id")
                    alt = alt_traj.loc[alt_traj.metric.eq(metric)].set_index("maup_cell_id")
                    footprint = footprint_metrics(
                        crosswalk, can.index[can.persistent_hh_2plus.eq(1)],
                        alt.index[alt.persistent_hh_2plus.eq(1)],
                    )
                    projection = crosswalk.copy()
                    projection["alternative_frequency"] = projection.maup_cell_id.map(alt.hh_frequency)
                    projection["weighted_frequency"] = (
                        projection.alternative_frequency * projection.overlap_ha
                    )
                    grouped = projection.groupby("cell_id", as_index=False).agg(
                        covered_area_ha=("overlap_ha", "sum"),
                        weighted_frequency=("weighted_frequency", "sum"),
                    )
                    grouped["alternative_frequency_projected"] = (
                        grouped.weighted_frequency / grouped.covered_area_ha
                    )
                    grouped["canonical_frequency"] = grouped.cell_id.map(can.hh_frequency)
                    rho = weighted_spearman(grouped.canonical_frequency,
                                            grouped.alternative_frequency_projected,
                                            grouped.covered_area_ha)
                    rows.append({
                        "grid_code": grid_code, "metric": metric, "window": window,
                        "interval_count": len(years), "inference": inference,
                        "primary_inference": int(inference == "BH"),
                        "hh_frequency_weighted_spearman": rho,
                        "frequency_spearman_threshold": FREQUENCY_SPEARMAN_THRESHOLD,
                        "frequency_criterion_pass": bool(rho >= FREQUENCY_SPEARMAN_THRESHOLD),
                        "persistent_hh_jaccard": footprint["jaccard"],
                        "persistent_hh_overlap_coefficient": footprint["overlap_coefficient"],
                        "persistent_hh_canonical_capture": footprint["canonical_capture"],
                        "persistent_hh_alternative_precision": footprint["alternative_precision"],
                        "persistent_hh_criterion_pass": footprint["location_criterion_pass"],
                        "temporal_criterion_pass": bool(
                            rho >= FREQUENCY_SPEARMAN_THRESHOLD and footprint["location_criterion_pass"]
                        ),
                    })
    result = pd.DataFrame(rows)
    require(len(result) == 3 * 5 * 2 * 2, "Temporal comparison population differs")
    return result


def assessments(interval, temporal):
    rows = []
    primary_interval = interval.loc[interval.inference.eq("BH")]
    primary_temporal = temporal.loc[temporal.inference.eq("BH")]
    for grid_code in GRIDS:
        for metric in METRICS:
            for window, years, required in [
                ("primary_1985_2020", PRIMARY_T0, PRIMARY_INTERVAL_PASSES_REQUIRED),
                ("full_observed_1985_2025", FULL_T0, FULL_INTERVAL_PASSES_REQUIRED),
            ]:
                maps = primary_interval.loc[
                    primary_interval.grid_code.eq(grid_code) & primary_interval.metric.eq(metric)
                    & primary_interval.t0.isin(years)
                ]
                temporal_row = primary_temporal.loc[
                    primary_temporal.grid_code.eq(grid_code) & primary_temporal.metric.eq(metric)
                    & primary_temporal.window.eq(window)
                ].iloc[0]
                passed = int(maps.location_criterion_pass.sum())
                interval_pass = passed >= required
                overall = bool(interval_pass and temporal_row.temporal_criterion_pass)
                rows.append({
                    "grid_code": grid_code, "metric": metric, "window": window,
                    "interval_maps": len(maps), "interval_maps_passed": passed,
                    "interval_passes_required": required,
                    "interval_location_criterion_pass": interval_pass,
                    "frequency_criterion_pass": bool(temporal_row.frequency_criterion_pass),
                    "persistent_hh_criterion_pass": bool(temporal_row.persistent_hh_criterion_pass),
                    "overall_prespecified_robustness_pass": overall,
                    "assessment": "stable_under_prespecified_criteria" if overall else "sensitive_for_at_least_one_criterion",
                })
    result = pd.DataFrame(rows)
    require(len(result) == 3 * 5 * 2, "Assessment population differs")
    return result


def create_figures(interval, temporal, output):
    figures = output / "figures"; figures.mkdir(exist_ok=True)
    primary = interval.loc[interval.inference.eq("BH")].copy()
    row_labels = [f"{grid} | {metric}" for grid in GRIDS for metric in METRICS]
    matrix = np.array([
        primary.loc[(primary.grid_code.eq(grid)) & primary.metric.eq(metric)].sort_values("t0").jaccard.to_numpy()
        for grid in GRIDS for metric in METRICS
    ])
    fig, ax = plt.subplots(figsize=(12, 8))
    image = ax.imshow(matrix, vmin=0, vmax=1, cmap="viridis", aspect="auto")
    ax.set_yticks(range(len(row_labels)), row_labels, fontsize=8)
    ax.set_xticks(range(8), [f"{year}–{year+5}" for year in range(1985, 2025, 5)], rotation=45, ha="right")
    ax.set_title("HH footprint Jaccard: alternative versus canonical (BH 5%)")
    fig.colorbar(image, ax=ax, label="area-weighted Jaccard")
    fig.tight_layout(); fig.savefig(figures / "fig01_hh_interval_jaccard_heatmap_v1.png", dpi=180); plt.close(fig)

    temporal_bh = temporal.loc[temporal.inference.eq("BH") & temporal.window.eq("primary_1985_2020")]
    labels = [f"{grid}\n{metric}" for grid in GRIDS for metric in METRICS]
    ordered = pd.concat([
        temporal_bh.loc[(temporal_bh.grid_code.eq(grid)) & temporal_bh.metric.eq(metric)]
        for grid in GRIDS for metric in METRICS
    ])
    x = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x, ordered.hh_frequency_weighted_spearman, color="#4c78a8")
    ax.axhline(FREQUENCY_SPEARMAN_THRESHOLD, color="#b2182b", linestyle="--", label="criterion")
    ax.set_ylim(0, 1); ax.set_ylabel("weighted Spearman correlation"); ax.set_xticks(x, labels, rotation=75, ha="right", fontsize=7)
    ax.set_title("Primary-period HH frequency agreement"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(figures / "fig02_hh_frequency_correlation_v1.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x, ordered.persistent_hh_jaccard, color="#59a14f")
    ax.axhline(JACCARD_THRESHOLD, color="#b2182b", linestyle="--", label="Jaccard criterion")
    ax.set_ylim(0, 1); ax.set_ylabel("area-weighted Jaccard"); ax.set_xticks(x, labels, rotation=75, ha="right", fontsize=7)
    ax.set_title("Primary-period persistent-HH footprint agreement"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(figures / "fig03_hh_persistent_overlap_v1.png", dpi=180); plt.close(fig)


def inventory_files(output):
    paths = sorted(path for path in output.rglob("*") if path.is_file()
                   and "checkpoints" not in path.parts and "crosswalks" not in path.parts
                   and path.name != "canonical_maup_hh_cluster_inventory_v1.csv")
    return pd.DataFrame([{
        "relative_path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    } for path in paths])


def run(arguments):
    print("CANONICAL MAUP HH CLUSTER ROBUSTNESS — PHASE 8E VERSION 1", flush=True)
    print("BH PRIMARY; BY SENSITIVITY; 9,999 CONDITIONAL PERMUTATIONS", flush=True)
    print("Mode:", arguments.mode, flush=True)
    engine = verify_engine(); print("Statistical and overlap engine verification: PASS", flush=True)
    project_dir = arguments.project_dir
    if not project_dir.exists() and str(project_dir).startswith("/content/drive/"):
        from google.colab import drive
        drive.mount("/content/drive")
    output = arguments.output_dir or project_dir / OUTPUT_RELATIVE
    output.mkdir(parents=True, exist_ok=True)
    checkpoints = output / "checkpoints"; checkpoints.mkdir(exist_ok=True)
    crosswalk_dir = output / "crosswalks"; crosswalk_dir.mkdir(exist_ok=True)

    canonical_local, canonical_spatial, panel, grids, inputs = read_inputs(project_dir)
    validate_inputs(canonical_local, canonical_spatial, panel, grids)
    canonical = canonical_classes(canonical_local)
    target_grids = [PILOT_GRID] if arguments.mode == "pilot" else GRIDS
    target_metrics = [PILOT_METRIC] if arguments.mode == "pilot" else list(METRICS)
    target_intervals = [(PILOT_T0, PILOT_T0 + 5)] if arguments.mode == "pilot" else INTERVALS
    results_by_grid = {}
    crosswalks = {}
    crosswalk_meta = {}

    for grid_code in target_grids:
        selected, binary, degree = build_graph(grids[grid_code], grid_code)
        crosswalk, metadata, crosswalk_state = build_or_read_crosswalk(
            grid_code, selected, canonical_spatial, crosswalk_dir
        )
        crosswalks[grid_code] = crosswalk; crosswalk_meta[grid_code] = metadata
        print(f"{crosswalk_state} CROSSWALK | {grid_code} | rows={len(crosswalk):,}", flush=True)
        frames = []
        for metric in target_metrics:
            for t0, t1 in target_intervals:
                stem = f"checkpoint_{grid_code}_{metric}_{t0}_{t1}_v1"
                data_path = checkpoints / f"{stem}.parquet"; meta_path = checkpoints / f"{stem}.json"
                config = checkpoint_config(inputs, grid_code, metric, t0)
                frame = read_checkpoint(data_path, meta_path, config, len(selected))
                if frame is None:
                    frame = compute_local_map(grid_code, metric, t0, selected, binary, degree, panel)
                    frame.to_parquet(data_path, index=False, compression="zstd")
                    atomic_json(meta_path, {"config": config, "rows": len(frame),
                                            "parquet_sha256": sha256_file(data_path),
                                            "created_utc": datetime.now(timezone.utc).isoformat()})
                    state = "COMPUTED"
                else:
                    state = "RESUMED"
                frames.append(frame)
                print(f"{state} | {grid_code} | {metric} | {t0}–{t1} | BH HH={int(frame.lisa_class_bh.eq('HH').sum()):,}", flush=True)
        results_by_grid[grid_code] = pd.concat(frames, ignore_index=True)

    if arguments.mode == "pilot":
        alternative = results_by_grid[PILOT_GRID]
        can = canonical.loc[(canonical.metric_comparison.eq(PILOT_METRIC)) & canonical.t0.eq(PILOT_T0)]
        footprint = footprint_metrics(
            crosswalks[PILOT_GRID], can.loc[can.lisa_class_bh.eq("HH"), "cell_id"],
            alternative.loc[alternative.lisa_class_bh.eq("HH"), "maup_cell_id"],
        )
        validation = {
            "validation_status": "PASS", "mode": "pilot", "script_version": VERSION,
            "execution_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": sha256_file(Path(__file__)),
            "engine_checks": engine, "inputs": inputs, "test": {
                "grid_code": PILOT_GRID, "metric": PILOT_METRIC, "t0": PILOT_T0,
                "rows": len(alternative), "permutations": PERMUTATIONS,
                "bh_hh_cells": int(alternative.lisa_class_bh.eq("HH").sum()), **footprint,
            }, "crosswalk": crosswalk_meta[PILOT_GRID],
        }
        write_json(output / "pilot_maup_hh_cluster_validation_v1.json", validation)
        print("PHASE 8E PILOT VALIDATION PASS", flush=True)
        print("Output:", output, flush=True)
        return

    for grid_code, frame in results_by_grid.items():
        require(len(frame) == PRIMARY_ROWS[grid_code] * 5 * 8, f"Full result population differs: {grid_code}")
        require(not frame.duplicated(["maup_cell_id", "metric", "t0"]).any(), f"Duplicate result key: {grid_code}")
        frame.to_parquet(output / f"alternative_local_moran_{grid_code}_v1.parquet", index=False, compression="zstd")

    interval = interval_comparisons(canonical, results_by_grid, crosswalks)
    temporal = temporal_comparisons(canonical, results_by_grid, crosswalks)
    assessment = assessments(interval, temporal)
    interval.to_csv(output / "canonical_maup_hh_interval_overlap_v1.csv", index=False, float_format="%.17g")
    temporal.to_csv(output / "canonical_maup_hh_temporal_persistence_v1.csv", index=False, float_format="%.17g")
    assessment.to_csv(output / "canonical_maup_hh_robustness_assessment_v1.csv", index=False)
    class_summary = pd.concat(results_by_grid.values()).groupby(
        ["grid_code", "metric", "t0", "t1", "diagnostic_interval", "lisa_class_bh"], as_index=False
    ).agg(cells=("maup_cell_id", "size"))
    class_summary.to_csv(output / "canonical_maup_local_moran_class_counts_v1.csv", index=False)
    create_figures(interval, temporal, output)

    validation_path = output / "canonical_maup_hh_cluster_validation_v1.json"
    validation = {
        "validation_status": "PASS", "mode": "full", "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": sha256_file(Path(__file__)),
        "engine_checks": engine, "inputs": inputs,
        "design": {
            "primary_cluster": "HH significant after BH within grid x metric x interval",
            "sensitivity": "BY within the same map", "permutations": PERMUTATIONS,
            "support_threshold": PRIMARY_SUPPORT_THRESHOLD,
            "jaccard_threshold": JACCARD_THRESHOLD,
            "overlap_coefficient_threshold": OVERLAP_COEFFICIENT_THRESHOLD,
            "frequency_spearman_threshold": FREQUENCY_SPEARMAN_THRESHOLD,
            "primary_interval_passes_required": PRIMARY_INTERVAL_PASSES_REQUIRED,
            "full_interval_passes_required": FULL_INTERVAL_PASSES_REQUIRED,
        },
        "structure": {
            "alternative_maps": 120, "alternative_cell_map_rows": int(sum(len(value) for value in results_by_grid.values())),
            "interval_comparisons": len(interval), "temporal_comparisons": len(temporal),
            "assessments": len(assessment),
        },
        "results": {
            "primary_interval_location_passes": int(interval.loc[interval.inference.eq("BH"), "location_criterion_pass"].sum()),
            "primary_temporal_passes": int(temporal.loc[temporal.inference.eq("BH"), "temporal_criterion_pass"].sum()),
            "assessments_passing": int(assessment.overall_prespecified_robustness_pass.sum()),
        },
        "crosswalks": crosswalk_meta,
        "checks": {
            "all_maps_present": all(len(results_by_grid[grid]) == PRIMARY_ROWS[grid] * 40 for grid in GRIDS),
            "all_interval_comparisons_present": len(interval) == 240,
            "all_temporal_comparisons_present": len(temporal) == 60,
            "all_assessments_present": len(assessment) == 30,
            "interval_metrics_bounded": bool(interval[["jaccard", "overlap_coefficient", "canonical_capture", "alternative_precision"]].apply(lambda column: column.between(0, 1).all()).all()),
            "temporal_correlations_bounded": bool(temporal.hh_frequency_weighted_spearman.between(-1, 1).all()),
            "diagnostic_interval_included": bool(set(interval.loc[interval.diagnostic_interval.eq(1), "t0"]) == {2020}),
        },
    }
    require(all(validation["checks"].values()), "Final validation check failed")
    write_json(validation_path, validation)
    inventory = inventory_files(output)
    inventory.to_csv(output / "canonical_maup_hh_cluster_inventory_v1.csv", index=False)
    print("PHASE 8E FULL COMPARISON COMPLETE — VALIDATION PASS", flush=True)
    print("Alternative maps:", 120, flush=True)
    print("Cell-map rows:", f"{validation['structure']['alternative_cell_map_rows']:,}", flush=True)
    print("Validation:", validation_path, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--mode", choices=["pilot", "full"], default="pilot")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        print(json.dumps(verify_engine(), indent=2))
    else:
        run(arguments)

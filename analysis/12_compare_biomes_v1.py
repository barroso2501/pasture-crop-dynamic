"""Phase 7: canonical Cerrado-Amazon comparison.

Colab
------
%pip install -q pyarrow scipy matplotlib
%run /content/12_compare_biomes_v1.py

The script reuses accepted Phase 2, 3, 5 and 6 products. It does not refit map
classes and does not recompute Local Moran/LISA. Biome-specific Global Moran's
I is computed on induced canonical graphs with resumable checkpoints.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


VERSION = "phase7-biome-comparison-v1"
N_CELLS = 24_889
N_INTERVALS = 8
PERMUTATIONS = 9_999
MASTER_SEED = 20260917
BIOMES = ["Amazon", "Cerrado"]
SCOPES = ["primary_assignment", "single_biome_sensitivity"]
INTERVALS = [(year, year + 5) for year in range(1985, 2025, 5)]
KEYS = ["cell_id", "t0", "t1"]
ZERO_HA = 1e-9

HASHES = {
    "metrics": "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c",
    "classes": "f0860bd2aff2c5bf6f6020bcd5022c86180311229191f58a1ed9600809d12bc3",
    "spatial": "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc",
    "graph": "85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f",
    "global": "30ababa6003dc03909819563d7b8389ca11c794f9fb9ed58681f4919864966e5",
    "local": "ec5906cb86e4044082db91d4cf11440b0d5401f6f8b6484217c7e246449ca2b4",
}

METRICS = {
    "consolidation_ha": (None, "absolute_area", True),
    "consolidation_rate_initial_pasture": ("consolidation_rate_defined", "relative_intensity", False),
    "replenishment_ha": (None, "absolute_area", True),
    "replenishment_rate_initial_native": ("replenishment_rate_defined", "relative_intensity", False),
    "nat_tmp_endpoint_ha": (None, "absolute_area", True),
    "nat_tmp_intensity_initial_native": ("nat_tmp_intensity_defined", "relative_intensity", False),
    "nat_tmp_pas_any_ha": (None, "trajectory_area", True),
    "nat_tmp_pas_any_share_endpoint": ("nat_tmp_endpoint_share_defined", "trajectory_share", False),
    "nat_tmp_pas_consecutive2_ha": (None, "trajectory_area", True),
    "nat_tmp_pas_consecutive2_share_endpoint": ("nat_tmp_endpoint_share_defined", "trajectory_share", False),
    "net_cr_balance_ha": (None, "signed_area", True),
    "cr_balance_index": ("cr_balance_defined", "bounded_index", False),
}
GLOBAL_METRICS = {
    "consolidation_ha": None,
    "replenishment_ha": None,
    "nat_tmp_endpoint_ha": None,
    "net_cr_balance_ha": None,
    "cr_balance_index": "cr_balance_defined",
}
CORE_AXES = ["nat_tmp_endpoint_ha", "cr_balance_index"]
LISA_CLASSES = ["HH", "LL", "HL", "LH", "not_significant", "island", "not_applicable"]
COLORS = {"Amazon": "#2a9d55", "Cerrado": "#d59a2f", "Combined domain": "#4c566a"}


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def by_adjust(values):
    p = np.asarray(values, dtype=float)
    require(p.ndim == 1 and len(p) and np.isfinite(p).all(), "Invalid BY input")
    order = np.argsort(p, kind="mergesort")
    ranks = np.arange(1, len(p) + 1, dtype=float)
    harmonic = np.sum(1.0 / ranks)
    adjusted = p[order] * len(p) * harmonic / ranks
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    out = np.empty(len(p), dtype=float)
    out[order] = np.minimum(adjusted, 1.0)
    return out


def row_standardize(binary):
    weights = binary.astype(float).tocsr()
    degree = np.asarray(weights.sum(axis=1)).ravel()
    inverse = np.divide(1.0, degree, out=np.zeros_like(degree), where=degree > 0)
    weights.data *= np.repeat(inverse, np.diff(weights.indptr))
    return weights, degree


def moran_i(values, weights):
    values = np.asarray(values, dtype=float)
    z = values - values.mean()
    denominator = float(z @ z)
    s0 = float(weights.sum())
    if len(values) < 3 or denominator == 0 or s0 == 0:
        return np.nan
    return float(len(values) / s0 * (z @ (weights @ z)) / denominator)


def simulate_moran(values, weights, permutations, seed):
    values = np.asarray(values, dtype=float)
    z = values - values.mean()
    denominator = float(z @ z)
    s0 = float(weights.sum())
    factor = len(values) / s0 / denominator
    rng = np.random.default_rng(seed)
    simulations = np.empty(permutations, dtype=float)
    for start in range(0, permutations, 64):
        count = min(64, permutations - start)
        permuted = np.stack([rng.permutation(z) for _ in range(count)])
        lag = (weights @ permuted.T).T
        simulations[start:start + count] = factor * np.einsum("ij,ij->i", permuted, lag)
    return simulations


def permutation_pvalue(observed, simulations, expected):
    tolerance = 1e-12 * max(1.0, abs(observed - expected))
    extreme = np.abs(simulations - expected) >= abs(observed - expected) - tolerance
    return float((1 + np.count_nonzero(extreme)) / (len(simulations) + 1))


def stable_seed(scope, biome, metric, t0):
    token = f"{MASTER_SEED}|{VERSION}|{scope}|{biome}|{metric}|{t0}".encode()
    return int.from_bytes(hashlib.sha256(token).digest()[:4], "little")


def max_run(sequence, target=None):
    best = current = 0
    previous = object()
    for value in sequence:
        if target is not None:
            current = current + 1 if value == target else 0
            best = max(best, current)
        else:
            current = current + 1 if value == previous else 1
            best = max(best, current)
        previous = value
    return best


def verify_engine():
    adjacency = csr_matrix(np.array([
        [0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]
    ], dtype=float))
    weights, _ = row_standardize(adjacency)
    values = np.array([1.0, 2.0, 7.0, 4.0])
    exact = np.array([moran_i(np.array(p), weights) for p in itertools.permutations(values)])
    require(np.isclose(exact.mean(), -1 / 3), "Moran permutation expectation failed")
    require(np.isclose(moran_i(values, weights), moran_i(values * 3 + 9, weights)), "Affine invariance failed")
    require(np.array_equal(simulate_moran(values, weights, 99, 19),
                           simulate_moran(values, weights, 99, 19)), "Seed reproducibility failed")
    require(np.allclose(by_adjust([0.01, 0.02, 1.0]), [0.055, 0.055, 1.0]), "BY reference failed")
    require(max_run(["A", "A", "B", "B", "B"]) == 3, "Episode run test failed")
    require(max_run(["HH", "HH", "LL"], "HH") == 2, "Target run test failed")
    return {
        "permutation_expectation": True, "affine_invariance": True,
        "seed_reproducibility": True, "by_reference": True, "run_lengths": True,
    }


def load_inputs(root):
    paths = {
        "metrics": root / "spatial/phase2/canonical_spatial_metrics_panel_v1.parquet",
        "classes": root / "spatial/phase3/canonical_spatial_map_classes_v1.parquet",
        "spatial": root / "spatial/phase1/canonical_spatial_support_v1.parquet",
        "graph": root / "spatial/phase1/canonical_contiguity_weights_v1.parquet",
        "global": root / "spatial/phase5/global_moran_v1/canonical_global_moran_results_v1.csv",
        "local": root / "spatial/phase6/local_moran_v1/canonical_local_moran_cell_results_v1.parquet",
    }
    records = {}
    for key, path in paths.items():
        require(path.is_file(), "Missing accepted input: " + str(path))
        digest = sha256(path)
        require(digest == HASHES[key], f"Input hash mismatch: {key}")
        records[key] = {"path": str(path), "sha256": digest}
    panel = pd.read_parquet(paths["metrics"])
    classes = pd.read_parquet(paths["classes"])
    spatial = pd.read_parquet(paths["spatial"])
    graph = pd.read_parquet(paths["graph"])
    global_reference = pd.read_csv(paths["global"])
    local = pd.read_parquet(paths["local"])
    for frame, fields in [(panel, ["cell_id"]), (classes, ["cell_id"]), (spatial, ["cell_id"]),
                          (local, ["cell_id"]), (graph, ["focal_cell_id", "neighbor_cell_id"])]:
        for field in fields:
            frame[field] = frame[field].astype(str)
    require(len(panel) == N_CELLS * N_INTERVALS and not panel.duplicated(KEYS).any(), "Invalid metric panel")
    require(len(classes) == len(panel) and not classes.duplicated(KEYS).any(), "Invalid class panel")
    require(len(spatial) == N_CELLS and spatial.cell_id.is_unique, "Invalid spatial support")
    require(len(graph) == 134_906 and not graph.duplicated(["focal_cell_id", "neighbor_cell_id"]).any(), "Invalid graph")
    require(len(local) == N_CELLS * 5 * N_INTERVALS and
            not local.duplicated(["cell_id", "metric", "t0"]).any(), "Invalid local Moran panel")
    ids = set(spatial.cell_id)
    require(set(panel.cell_id) == ids == set(classes.cell_id) == set(local.cell_id), "Input cell populations differ")
    require(set(spatial.primary_biome) == set(BIOMES), "Unexpected primary-biome labels")
    for metric, (support, _, _) in METRICS.items():
        require(metric in panel and f"{metric}__class" in classes, "Missing metric or class: " + metric)
        require(support is None or support in panel, "Missing support field: " + str(support))
    return panel, classes, spatial, graph, global_reference, local, records


def add_attributes(spatial):
    attrs = spatial[["cell_id", "primary_biome", "amazon_fraction_cell", "cerrado_fraction_cell",
                     "geometry_area_aea_ha"]].copy()
    attrs["transbiome_flag"] = (
        attrs.amazon_fraction_cell.gt(0) & attrs.cerrado_fraction_cell.gt(0)
    ).astype("int8")
    require(attrs.groupby("primary_biome").size().sum() == N_CELLS, "Biome population does not close")
    return attrs


def scope_cells(attrs, scope, biome):
    mask = attrs.primary_biome.eq(biome)
    if scope == "single_biome_sensitivity":
        mask &= attrs.transbiome_flag.eq(0)
    return set(attrs.loc[mask, "cell_id"])


def process_summary(panel, attrs):
    enriched = panel.drop(columns=["primary_biome", "transbiome_flag"], errors="ignore").merge(
        attrs[["cell_id", "primary_biome", "transbiome_flag"]], on="cell_id", validate="many_to_one"
    )
    domain_totals = {metric: panel.groupby("t0")[metric].sum(min_count=1) for metric, (_, _, additive) in METRICS.items() if additive}
    rows = []
    for scope in SCOPES:
        scoped = enriched if scope == "primary_assignment" else enriched[enriched.transbiome_flag.eq(0)]
        for (biome, t0), group in scoped.groupby(["primary_biome", "t0"], sort=True):
            for metric, (support, measure_type, additive) in METRICS.items():
                supported = group[metric].notna() if support is None else group[support].eq(1)
                values = group.loc[supported, metric].astype(float)
                require(np.isfinite(values).all(), "Nonfinite supported values: " + metric)
                total = float(values.sum()) if len(values) else np.nan
                rows.append({
                    "boundary_scope": scope, "primary_biome": biome, "metric": metric,
                    "measure_type": measure_type, "t0": int(t0), "t1": int(t0 + 5),
                    "diagnostic_interval": int(t0 == 2020), "cells": len(group),
                    "supported_cells": len(values), "undefined_cells": int(len(group) - len(values)),
                    "nonzero_cells": int(np.count_nonzero(np.abs(values) > ZERO_HA)),
                    "value_sum": total, "value_mean": float(values.mean()) if len(values) else np.nan,
                    "value_median": float(values.median()) if len(values) else np.nan,
                    "value_q90": float(values.quantile(.9)) if len(values) else np.nan,
                    "contribution_to_combined_domain_sum": (
                        total / float(domain_totals[metric].loc[t0])
                        if additive and abs(float(domain_totals[metric].loc[t0])) > ZERO_HA else np.nan
                    ),
                })
    result = pd.DataFrame(rows)
    require(len(result) == len(SCOPES) * len(BIOMES) * N_INTERVALS * len(METRICS), "Process summary dimensions differ")
    return result


def state_and_transition_summaries(classes, attrs):
    fields = KEYS + [f"{metric}__class" for metric in METRICS]
    enriched = classes[fields].merge(attrs[["cell_id", "primary_biome", "transbiome_flag"]], on="cell_id", validate="many_to_one")
    states, transitions, trajectories = [], [], []
    for scope in SCOPES:
        scoped = enriched if scope == "primary_assignment" else enriched[enriched.transbiome_flag.eq(0)]
        for biome in BIOMES:
            biome_frame = scoped[scoped.primary_biome.eq(biome)].sort_values(["cell_id", "t0"])
            n = biome_frame.cell_id.nunique()
            require(len(biome_frame) == n * N_INTERVALS, "Unbalanced biome class panel")
            for metric in METRICS:
                field = f"{metric}__class"
                grouped = biome_frame.groupby(["t0", field], observed=True).size().rename("cells").reset_index()
                for row in grouped.itertuples(index=False):
                    states.append({"boundary_scope": scope, "primary_biome": biome, "metric": metric,
                                   "t0": int(row.t0), "t1": int(row.t0 + 5),
                                   "diagnostic_interval": int(row.t0 == 2020), "stage": getattr(row, field),
                                   "cells": int(row.cells), "biome_cells": n, "cell_fraction": row.cells / n})
            for metric in CORE_AXES:
                field = f"{metric}__class"
                wide = biome_frame.pivot(index="cell_id", columns="t0", values=field).loc[:, [x[0] for x in INTERVALS]]
                for window, length in [("primary", 7), ("full_observed", 8)]:
                    array = wide.iloc[:, :length].to_numpy(object)
                    change_counts, distinct_counts, longest = [], [], []
                    constant = 0
                    for sequence in array:
                        changes = sum(a != b for a, b in zip(sequence, sequence[1:]))
                        change_counts.append(changes); distinct_counts.append(len(set(sequence)))
                        longest.append(max_run(sequence)); constant += int(changes == 0)
                    trajectories.append({
                        "boundary_scope": scope, "primary_biome": biome, "metric": metric,
                        "analysis_window": window, "cells": n, "mean_state_changes": float(np.mean(change_counts)),
                        "mean_distinct_states": float(np.mean(distinct_counts)), "constant_cells": constant,
                        "constant_cell_fraction": constant / n, "mean_maximum_episode_intervals": float(np.mean(longest)),
                    })
                    for step in range(length - 1):
                        pairs = pd.DataFrame({"from_stage": array[:, step], "to_stage": array[:, step + 1]})
                        counts = pairs.groupby(["from_stage", "to_stage"], observed=True).size().rename("cells").reset_index()
                        source = pairs.groupby("from_stage", observed=True).size()
                        for row in counts.itertuples(index=False):
                            transitions.append({
                                "boundary_scope": scope, "primary_biome": biome, "metric": metric,
                                "analysis_window": window, "from_t0": INTERVALS[step][0], "from_t1": INTERVALS[step][1],
                                "to_t0": INTERVALS[step + 1][0], "to_t1": INTERVALS[step + 1][1],
                                "contains_diagnostic_interval": int(step + 1 == 7),
                                "from_stage": row.from_stage, "to_stage": row.to_stage, "cells": int(row.cells),
                                "source_cells": int(source.loc[row.from_stage]),
                                "source_transition_fraction": row.cells / source.loc[row.from_stage],
                            })
                    expected = n * (length - 1)
                    actual = sum(x["cells"] for x in transitions if x["boundary_scope"] == scope and
                                 x["primary_biome"] == biome and x["metric"] == metric and
                                 x["analysis_window"] == window)
                    require(actual == expected, "Transition population does not close")
    state = pd.DataFrame(states)
    transition = pd.DataFrame(transitions)
    trajectory = pd.DataFrame(trajectories)
    require(len(trajectory) == len(SCOPES) * len(BIOMES) * len(CORE_AXES) * 2, "Trajectory summary dimensions differ")
    return state, transition, trajectory


def reference_moran_lookup(reference):
    selected = []
    for metric in GLOBAL_METRICS:
        component = "conditional" if metric == "cr_balance_index" else "complete"
        part = reference[(reference.metric == metric) & (reference.component == component) &
                         (reference.transformation == "raw")]
        require(len(part) == N_INTERVALS, "Missing combined-domain Moran reference: " + metric)
        selected.append(part[["metric", "t0", "moran_i"]])
    result = pd.concat(selected, ignore_index=True)
    return result.set_index(["metric", "t0"]).moran_i


def biome_global_moran(panel, attrs, graph, reference, output, permutations):
    ids = sorted(attrs.cell_id)
    lookup = {cell_id: i for i, cell_id in enumerate(ids)}
    row = graph.focal_cell_id.map(lookup).to_numpy()
    col = graph.neighbor_cell_id.map(lookup).to_numpy()
    adjacency = csr_matrix((np.ones(len(graph)), (row, col)), shape=(N_CELLS, N_CELLS))
    require((adjacency != adjacency.T).nnz == 0, "Canonical graph is not symmetric")
    ordered = panel.set_index(["t0", "cell_id"]).sort_index()
    reference_lookup = reference_moran_lookup(reference)
    checkpoints = output / "checkpoints_global_moran"
    checkpoints.mkdir(exist_ok=True)
    rows = []
    for scope in SCOPES:
        for biome in BIOMES:
            biome_ids = scope_cells(attrs, scope, biome)
            biome_mask = np.array([cell_id in biome_ids for cell_id in ids])
            for metric, support_field in GLOBAL_METRICS.items():
                for t0, t1 in INTERVALS:
                    checkpoint = checkpoints / f"{scope}__{biome}__{metric}__{t0}_{t1}.json"
                    seed = stable_seed(scope, biome, metric, t0)
                    config = {"version": VERSION, "scope": scope, "biome": biome, "metric": metric,
                              "t0": t0, "permutations": permutations, "seed": seed}
                    saved = None
                    if checkpoint.is_file():
                        candidate = json.loads(checkpoint.read_text(encoding="utf-8"))
                        if candidate.get("config") == config:
                            saved = candidate.get("result")
                    if saved is None:
                        frame = ordered.loc[t0].reindex(ids)
                        support = np.ones(N_CELLS, dtype=bool) if support_field is None else frame[support_field].eq(1).to_numpy()
                        mask = biome_mask & support
                        values = frame.loc[mask, metric].to_numpy(float)
                        require(np.isfinite(values).all(), "Nonfinite Moran values")
                        selected = adjacency[mask][:, mask]
                        weights, degree = row_standardize(selected)
                        observed = moran_i(values, weights)
                        expected = -1 / (len(values) - 1) if len(values) > 1 else np.nan
                        components = connected_components(selected, directed=False, return_labels=False) if len(values) else 0
                        result = {
                            "boundary_scope": scope, "primary_biome": biome, "metric": metric,
                            "t0": t0, "t1": t1, "diagnostic_interval": int(t0 == 2020),
                            "supported_cells": int(len(values)), "excluded_biome_cells": int(biome_mask.sum() - len(values)),
                            "components": int(components), "islands": int((degree == 0).sum()),
                            "undirected_edges": int(selected.nnz // 2), "s0": float(weights.sum()),
                            "mean_neighbor_count": float(degree.mean()), "moran_i": float(observed),
                            "expected_i": float(expected), "seed": seed, "permutations": permutations,
                            "status": "tested" if np.isfinite(observed) else "undefined_constant_or_no_edges",
                        }
                        if np.isfinite(observed):
                            simulations = simulate_moran(values, weights, permutations, seed)
                            result.update({
                                "p_two_sided": permutation_pvalue(observed, simulations, expected),
                                "permutation_mean": float(simulations.mean()),
                                "permutation_sd": float(simulations.std(ddof=1)),
                                "permutation_q025": float(np.quantile(simulations, .025)),
                                "permutation_q975": float(np.quantile(simulations, .975)),
                            })
                        else:
                            result.update({key: None for key in ["p_two_sided", "permutation_mean", "permutation_sd",
                                                                 "permutation_q025", "permutation_q975"]})
                        write_json(checkpoint, {"config": config, "result": result})
                        saved = result
                        status = "COMPUTED"
                    else:
                        status = "REUSED"
                    rows.append(saved)
                    print(f"{status} | {scope} | {biome} | {metric} | {t0}–{t1}", flush=True)
    result = pd.DataFrame(rows)
    require(len(result) == len(SCOPES) * len(BIOMES) * len(GLOBAL_METRICS) * N_INTERVALS, "Biome Moran dimensions differ")
    result["family"] = (result.boundary_scope + "__" + result.primary_biome + "__" +
                        np.where(result.diagnostic_interval.eq(1), "diagnostic", "primary"))
    result["q_by"] = np.nan
    for _, index in result.groupby("family").groups.items():
        result.loc[index, "q_by"] = by_adjust(result.loc[index, "p_two_sided"].fillna(1).to_numpy())
    result["significant_by_005"] = result.status.eq("tested") & result.q_by.le(.05)
    result["combined_domain_moran_i"] = [reference_lookup.loc[(m, t)] for m, t in zip(result.metric, result.t0)]
    result["biome_minus_combined_moran_i"] = result.moran_i - result.combined_domain_moran_i
    return result


def local_cluster_summaries(local, attrs):
    enriched = local.merge(attrs, on="cell_id", validate="many_to_one")
    summaries, persistence = [], []
    for scope in SCOPES:
        scoped = enriched if scope == "primary_assignment" else enriched[enriched.transbiome_flag.eq(0)]
        for biome in BIOMES:
            biome_frame = scoped[scoped.primary_biome.eq(biome)]
            for (metric, t0), group in biome_frame.groupby(["metric", "t0"], sort=True):
                supported = int(group.supported_flag.sum())
                for lisa_class in LISA_CLASSES:
                    part = group[group.lisa_class.eq(lisa_class)]
                    summaries.append({
                        "boundary_scope": scope, "primary_biome": biome, "metric": metric,
                        "t0": int(t0), "t1": int(t0 + 5), "diagnostic_interval": int(t0 == 2020),
                        "lisa_class": lisa_class, "cells": len(part), "biome_cells": len(group),
                        "supported_cells": supported,
                        "class_share_of_biome_cells": len(part) / len(group),
                        "class_share_of_supported_cells": (
                            len(part) / supported if supported and lisa_class != "not_applicable" else np.nan
                        ),
                        "metric_value_sum": float(part.metric_value.sum()) if len(part) else 0.0,
                    })
            primary = biome_frame[biome_frame.t0.lt(2020)].sort_values(["metric", "cell_id", "t0"])
            diagnostic = biome_frame[biome_frame.t0.eq(2020)].set_index(["metric", "cell_id"]).lisa_class
            for metric, metric_frame in primary.groupby("metric", sort=True):
                cell_rows = []
                for cell_id, cell in metric_frame.groupby("cell_id", sort=False):
                    sequence = cell.lisa_class.tolist()
                    cell_rows.append({
                        "cell_id": cell_id, "hh_intervals": sequence.count("HH"), "ll_intervals": sequence.count("LL"),
                        "hh_max_run": max_run(sequence, "HH"), "ll_max_run": max_run(sequence, "LL"),
                        "diagnostic_hh_continues": int(sequence[-1] == "HH" and diagnostic.get((metric, cell_id)) == "HH"),
                        "diagnostic_ll_continues": int(sequence[-1] == "LL" and diagnostic.get((metric, cell_id)) == "LL"),
                    })
                cell_table = pd.DataFrame(cell_rows)
                persistence.append({
                    "boundary_scope": scope, "primary_biome": biome, "metric": metric, "cells": len(cell_table),
                    "any_hh_primary_cells": int(cell_table.hh_intervals.gt(0).sum()),
                    "hh_persistent_2plus_primary_cells": int(cell_table.hh_max_run.ge(2).sum()),
                    "mean_hh_primary_intervals": float(cell_table.hh_intervals.mean()),
                    "mean_hh_maximum_run": float(cell_table.hh_max_run.mean()),
                    "any_ll_primary_cells": int(cell_table.ll_intervals.gt(0).sum()),
                    "ll_persistent_2plus_primary_cells": int(cell_table.ll_max_run.ge(2).sum()),
                    "mean_ll_primary_intervals": float(cell_table.ll_intervals.mean()),
                    "mean_ll_maximum_run": float(cell_table.ll_max_run.mean()),
                    "diagnostic_continues_hh_cells": int(cell_table.diagnostic_hh_continues.sum()),
                    "diagnostic_continues_ll_cells": int(cell_table.diagnostic_ll_continues.sum()),
                })
    summary = pd.DataFrame(summaries)
    persistent = pd.DataFrame(persistence)
    require(len(persistent) == len(SCOPES) * len(BIOMES) * len(GLOBAL_METRICS), "LISA persistence dimensions differ")
    return summary, persistent


def make_figures(process, global_moran, local_summary, figures):
    figures.mkdir(exist_ok=True)
    base = process[(process.boundary_scope == "primary_assignment") &
                   process.metric.isin(["consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha"])]
    fig, axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)
    for ax, metric in zip(axes, ["consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha"]):
        for biome in BIOMES:
            part = base[(base.metric == metric) & (base.primary_biome == biome)].sort_values("t0")
            ax.plot(part.t0, part.value_sum / 1e6, marker="o", color=COLORS[biome], label=biome)
        ax.axvspan(2017.5, 2022.5, color="gray", alpha=.12)
        ax.set_ylabel("million ha"); ax.set_title(metric); ax.grid(alpha=.2)
    axes[-1].set_xticks(range(1985, 2025, 5), [f"{y}–{y+5}" for y in range(1985, 2025, 5)], rotation=35)
    axes[0].legend(); fig.suptitle("Absolute process totals by primary biome (* diagnostic interval)")
    fig.tight_layout(); fig.savefig(figures / "phase7_biome_absolute_processes_v1.png", dpi=180); plt.close(fig)

    primary = global_moran[global_moran.boundary_scope.eq("primary_assignment")]
    fig, axes = plt.subplots(3, 2, figsize=(14, 12), sharex=True)
    for ax, metric in zip(axes.ravel(), GLOBAL_METRICS):
        metric_frame = primary[primary.metric.eq(metric)]
        for biome in BIOMES:
            part = metric_frame[metric_frame.primary_biome.eq(biome)].sort_values("t0")
            ax.plot(part.t0, part.moran_i, marker="o", color=COLORS[biome], label=biome)
        ref = metric_frame.sort_values("t0").drop_duplicates("t0")
        ax.plot(ref.t0, ref.combined_domain_moran_i, marker=".", ls="--", color=COLORS["Combined domain"], label="Combined domain")
        ax.axvspan(2017.5, 2022.5, color="gray", alpha=.12); ax.set_title(metric); ax.grid(alpha=.2)
    axes.ravel()[-1].axis("off")
    axes[0, 0].legend(fontsize=8); fig.suptitle("Global Moran's I: induced biome graphs and combined-domain reference")
    fig.tight_layout(); fig.savefig(figures / "phase7_biome_global_moran_v1.png", dpi=180); plt.close(fig)

    focal = local_summary[(local_summary.boundary_scope == "primary_assignment") &
                          local_summary.lisa_class.isin(["HH", "LL"])].copy()
    fig, axes = plt.subplots(3, 2, figsize=(14, 12), sharex=True)
    for ax, metric in zip(axes.ravel(), GLOBAL_METRICS):
        metric_frame = focal[focal.metric.eq(metric)]
        for biome in BIOMES:
            for lisa_class, style in [("HH", "-"), ("LL", "--")]:
                part = metric_frame[(metric_frame.primary_biome == biome) &
                                    (metric_frame.lisa_class == lisa_class)].sort_values("t0")
                ax.plot(part.t0, 100 * part.class_share_of_supported_cells, marker="o", ls=style,
                        color=COLORS[biome], label=f"{biome} {lisa_class}")
        ax.axvspan(2017.5, 2022.5, color="gray", alpha=.12); ax.set_title(metric); ax.set_ylabel("% supported cells"); ax.grid(alpha=.2)
    axes.ravel()[-1].axis("off")
    axes[0, 0].legend(fontsize=7, ncol=2); fig.suptitle("Contribution of primary biomes to combined-domain LISA classes")
    fig.tight_layout(); fig.savefig(figures / "phase7_biome_lisa_hh_ll_v1.png", dpi=180); plt.close(fig)


def run(args):
    print("CANONICAL BIOME COMPARISON — PHASE 7 VERSION 1", flush=True)
    print("PRIMARY ASSIGNMENT + SINGLE-BIOME SENSITIVITY; 2020–2025 INCLUDED", flush=True)
    engine = verify_engine()
    print("Statistical-engine verification: PASS", flush=True)
    root = args.project_dir
    if not root.exists() and str(root).startswith("/content/drive/"):
        from google.colab import drive
        drive.mount("/content/drive")
    panel, classes, spatial, graph, global_reference, local, inputs = load_inputs(root)
    attrs = add_attributes(spatial)
    output = args.output_dir or root / "spatial/phase7/biome_comparison_v1"
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "canonical_phase7_biome_design_v1.json", {
        "script_version": VERSION, "biomes": BIOMES, "intervals": INTERVALS,
        "diagnostic_interval": [2020, 2025], "diagnostic_included": True,
        "primary_boundary_rule": "deterministic primary_biome from Phase 1",
        "boundary_sensitivity": "exclude cells with positive overlap in both target biomes; do not reassign",
        "global_moran": "recomputed on the induced graph for each biome and boundary scope",
        "local_moran": "accepted combined-domain Phase 6 classes summarized by primary biome; not recomputed",
        "multiple_testing": "BY within boundary_scope x biome x primary/diagnostic family",
        "permutations": args.permutations, "master_seed": MASTER_SEED,
        "map_classes_refitted": False,
    })
    process = process_summary(panel, attrs)
    state, transition, trajectory = state_and_transition_summaries(classes, attrs)
    global_moran = biome_global_moran(panel, attrs, graph, global_reference, output, args.permutations)
    local_summary, local_persistence = local_cluster_summaries(local, attrs)
    tables = {
        "canonical_phase7_biome_process_summary_v1.csv": process,
        "canonical_phase7_biome_state_composition_v1.csv": state,
        "canonical_phase7_biome_transition_summary_v1.csv": transition,
        "canonical_phase7_biome_trajectory_summary_v1.csv": trajectory,
        "canonical_phase7_biome_global_moran_v1.csv": global_moran,
        "canonical_phase7_biome_local_cluster_summary_v1.csv": local_summary,
        "canonical_phase7_biome_local_persistence_v1.csv": local_persistence,
    }
    for name, frame in tables.items():
        frame.to_csv(output / name, index=False, encoding="utf-8-sig", float_format="%.17g")
    make_figures(process, global_moran, local_summary, output / "figures")
    public_files = [p for p in output.rglob("*") if p.is_file() and
                    "checkpoints_global_moran" not in p.parts and p.name != "canonical_phase7_biome_validation_v1.json"]
    inventory = pd.DataFrame([{
        "relative_path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size,
        "sha256": sha256(p), "rows": len(tables[p.name]) if p.name in tables else None,
    } for p in sorted(public_files)])
    inventory.to_csv(output / "canonical_phase7_biome_inventory_v1.csv", index=False)
    checks = {
        "authenticated_accepted_inputs": True, "canonical_cell_population": len(attrs) == N_CELLS,
        "balanced_eight_interval_panels": True, "primary_and_strict_boundary_scopes": True,
        "twelve_metrics_summarized_without_refitting": len(process.metric.unique()) == 12,
        "core_state_transitions_close": True, "diagnostic_interval_included": True,
        "biome_global_moran_recomputed_on_induced_graphs": len(global_moran) == 160,
        "combined_domain_global_moran_used_only_as_reference": True,
        "local_moran_classes_not_recomputed": True,
        "local_hh_ll_persistence_partitioned_by_biome": len(local_persistence) == 20,
    }
    require(all(checks.values()), "One or more Phase 7 checks failed")
    validation = {
        "validation_status": "PASS", "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": sha256(__file__),
        "inputs": inputs, "engine_checks": engine,
        "population": {"cells": N_CELLS, "primary_biome_counts": attrs.groupby("primary_biome").size().to_dict(),
                       "transbiome_cells": int(attrs.transbiome_flag.sum()), "intervals": N_INTERVALS,
                       "metrics": len(METRICS), "global_moran_tests": len(global_moran)},
        "checks": checks,
        "outputs": {p.relative_to(output).as_posix(): {"sha256": sha256(p), "bytes": p.stat().st_size}
                    for p in public_files + [output / "canonical_phase7_biome_inventory_v1.csv"]},
    }
    write_json(output / "canonical_phase7_biome_validation_v1.json", validation)
    archive = output / "canonical_phase7_biome_results_v1"
    if archive.with_suffix(".zip").exists():
        archive.with_suffix(".zip").unlink()
    portable = output / "portable"
    if portable.exists():
        shutil.rmtree(portable)
    portable.mkdir()
    for path in public_files + [output / "canonical_phase7_biome_inventory_v1.csv",
                                output / "canonical_phase7_biome_validation_v1.json"]:
        target = portable / path.relative_to(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    shutil.make_archive(str(archive), "zip", portable)
    shutil.rmtree(portable)
    print("PHASE 7 BIOME COMPARISON COMPLETE — VALIDATION PASS", flush=True)
    print("Output:", output, flush=True)
    print("Global Moran tests:", len(global_moran), flush=True)
    print("Transbiome cells:", f"{int(attrs.transbiome_flag.sum()):,}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path,
                        default=Path("/content/drive/MyDrive/Trabalho/Contabilidade"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        print(json.dumps(verify_engine(), indent=2))
    else:
        require(arguments.permutations == PERMUTATIONS,
                "Production requires the prespecified 9,999 permutations")
        run(arguments)

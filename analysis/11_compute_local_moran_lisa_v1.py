"""Canonical local Moran/LISA analysis for Phase 6.

Colab
------
%pip install -q esda==2.7.1 libpysal==4.13.0 pyarrow geopandas
%run /content/11_compute_local_moran_lisa_v1.py

The production run uses 9,999 conditional permutations, deterministic seeds,
one checkpoint per metric x interval, and the accepted canonical graph.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

VERSION = "phase6-local-moran-lisa-v1"
MASTER_SEED = 20260916
N_CELLS = 24889
PERMUTATIONS = 9999
ALPHA = 0.05
PANEL_HASH = "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c"
GRAPH_HASH = "85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f"
SPATIAL_HASH = "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc"
AEA = "+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"
METRICS = {
    "consolidation_ha": None,
    "replenishment_ha": None,
    "nat_tmp_endpoint_ha": None,
    "net_cr_balance_ha": None,
    "cr_balance_index": "cr_balance_defined",
}
QUADRANTS = {1: "HH", 2: "LH", 3: "LL", 4: "HL"}
COLORS = {
    "HH": "#b2182b", "LL": "#2166ac", "HL": "#ef8a62", "LH": "#67a9cf",
    "not_significant": "#d9d9d9", "island": "#636363", "not_applicable": "#ffffff",
}


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def fdr_adjust(values, method="bh"):
    p = np.asarray(values, dtype=float)
    require(p.ndim == 1 and len(p) > 0 and np.isfinite(p).all(), "Invalid p-values for FDR")
    require(((p >= 0) & (p <= 1)).all(), "p-values outside [0,1]")
    order = np.argsort(p, kind="mergesort")
    ranks = np.arange(1, len(p) + 1, dtype=float)
    factor = 1.0 if method == "bh" else sum(1.0 / ranks)
    adjusted = p[order] * len(p) * factor / ranks
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    out = np.empty(len(p), dtype=float)
    out[order] = np.minimum(adjusted, 1.0)
    return out


def stable_seed(metric, t0):
    token = f"{MASTER_SEED}|{metric}|{t0}|{VERSION}".encode()
    return int.from_bytes(hashlib.sha256(token).digest()[:4], "little")


def max_run(sequence, target):
    best = current = 0
    for value in sequence:
        current = current + 1 if value == target else 0
        best = max(best, current)
    return best


def verify_engine():
    require(np.allclose(fdr_adjust([.01, .02, 1], "bh"), [.03, .03, 1]), "BH reference failure")
    require(np.allclose(fdr_adjust([.01, .02, 1], "by"), [.055, .055, 1]), "BY reference failure")
    require(max_run(["HH", "HH", "LL", "HH"], "HH") == 2, "Run-length test failure")
    require(stable_seed("x", 1985) == stable_seed("x", 1985), "Seed reproducibility failure")
    try:
        from esda import Moran_Local
        from libpysal.weights import W
    except ImportError as exc:
        raise RuntimeError("Install production dependencies: pip install esda==2.7.1 libpysal==4.13.0") from exc
    w = W({"a": ["b"], "b": ["a", "c"], "c": ["b"], "d": []}, id_order=["a", "b", "c", "d"], silence_warnings=True)
    model = Moran_Local(np.array([1., 2., 7., 4.]), w, transformation="r", permutations=99,
                        geoda_quads=False, n_jobs=1, keep_simulations=False, seed=19, island_weight=0)
    require(model.q.tolist() == [3, 2, 4, 4], "PySAL quadrant convention changed")
    require(np.isfinite(model.Is).all() and np.isfinite(model.p_sim).all(), "Local Moran smoke test failed")
    return {
        "bh_reference": True, "by_reference": True, "run_length": True,
        "seed_reproducible": True, "pysal_quadrants": {"1": "HH", "2": "LH", "3": "LL", "4": "HL"},
    }


def make_weights(ids, graph):
    from libpysal.weights import W
    chosen = set(ids)
    neighbors = {cid: [] for cid in ids}
    for focal, neighbor in graph[["focal_cell_id", "neighbor_cell_id"]].itertuples(index=False, name=None):
        if focal in chosen and neighbor in chosen:
            neighbors[focal].append(neighbor)
    return W(neighbors, id_order=list(ids), silence_warnings=True)


def checkpoint_config(metric, t0, seed, permutations):
    return {
        "script_version": VERSION, "panel_sha256": PANEL_HASH, "graph_sha256": GRAPH_HASH,
        "metric": metric, "t0": int(t0), "t1": int(t0 + 5), "permutations": int(permutations),
        "seed": int(seed), "transformation": "row-standardized", "geoda_quads": False,
        "island_weight": 0, "fdr_primary": "BH within metric x interval", "alpha": ALPHA,
    }


def read_checkpoint(data_path, meta_path, expected):
    if not data_path.exists() and not meta_path.exists():
        return None
    require(data_path.exists() and meta_path.exists(), f"Incomplete checkpoint pair: {data_path.name}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    require(meta.get("config") == expected, f"Checkpoint configuration differs: {data_path.name}")
    require(meta.get("parquet_sha256") == sha256(data_path), f"Checkpoint hash mismatch: {data_path.name}")
    frame = pd.read_parquet(data_path)
    require(len(frame) == N_CELLS and frame.cell_id.nunique() == N_CELLS, f"Invalid checkpoint population: {data_path.name}")
    return frame


def compute_map(metric, support_flag, t0, interval, ids, graph, degree_full, permutations):
    from esda import Moran_Local
    values = interval.set_index("cell_id").loc[ids, metric].to_numpy(float)
    supported = np.ones(N_CELLS, dtype=bool) if support_flag is None else interval.set_index("cell_id").loc[ids, support_flag].eq(1).to_numpy()
    require(np.isfinite(values[supported]).all(), f"Nonfinite supported values: {metric} {t0}")
    require(pd.isna(values[~supported]).all() if support_flag else True, f"Unsupported values must remain null: {metric} {t0}")
    selected_ids = np.asarray(ids)[supported].tolist()
    weights = make_weights(selected_ids, graph)
    local_degree = np.array([len(weights.neighbors[cid]) for cid in selected_ids], dtype=int)
    cardinalities = np.array([weights.cardinalities[cid] for cid in selected_ids], dtype=int)
    require(np.array_equal(local_degree, cardinalities), "Island diagnostics differ")
    model = Moran_Local(values[supported], weights, transformation="r", permutations=permutations,
                        geoda_quads=False, n_jobs=1, keep_simulations=False,
                        seed=stable_seed(metric, t0), island_weight=0)
    spatial_lag = np.asarray(weights.sparse @ model.z).ravel()
    tested = local_degree > 0
    p_sim = np.asarray(model.p_sim, float)
    require(np.isfinite(p_sim[tested]).all(), "Nonfinite tested pseudo p-values")
    q_bh = np.full(len(selected_ids), np.nan)
    q_by = np.full(len(selected_ids), np.nan)
    q_bh[tested] = fdr_adjust(p_sim[tested], "bh")
    q_by[tested] = fdr_adjust(p_sim[tested], "by")
    quadrant = np.asarray(model.q, int)
    lisa = np.array([QUADRANTS.get(int(q), "not_significant") for q in quadrant], dtype=object)
    lisa[~(tested & (q_bh <= ALPHA))] = "not_significant"

    out = pd.DataFrame({
        "cell_id": ids, "metric": metric, "t0": t0, "t1": t0 + 5,
        "diagnostic_interval": int(t0 == 2020), "metric_value": values,
        "supported_flag": supported.astype(np.int8), "full_graph_degree": degree_full,
        "local_graph_degree": np.nan, "island_flag": 0, "z_score": np.nan,
        "spatial_lag_z": np.nan, "local_moran_i": np.nan, "quadrant_code": 0,
        "p_sim": np.nan, "q_bh": np.nan, "q_by": np.nan,
        "significant_bh_005": 0, "significant_by_005": 0,
        "lisa_class": "not_applicable", "analysis_status": "unsupported",
        "seed": stable_seed(metric, t0), "permutations": permutations,
    })
    loc = np.flatnonzero(supported)
    out.loc[loc, "local_graph_degree"] = local_degree
    out.loc[loc, "island_flag"] = (local_degree == 0).astype(np.int8)
    out.loc[loc, "z_score"] = model.z
    out.loc[loc, "spatial_lag_z"] = spatial_lag
    out.loc[loc, "local_moran_i"] = model.Is
    out.loc[loc, "quadrant_code"] = quadrant
    out.loc[loc, "p_sim"] = np.where(tested, p_sim, np.nan)
    out.loc[loc, "q_bh"] = q_bh
    out.loc[loc, "q_by"] = q_by
    out.loc[loc, "significant_bh_005"] = (tested & (q_bh <= ALPHA)).astype(np.int8)
    out.loc[loc, "significant_by_005"] = (tested & (q_by <= ALPHA)).astype(np.int8)
    out.loc[loc, "lisa_class"] = lisa
    out.loc[loc, "analysis_status"] = np.where(tested, "tested", "island")
    require(out.cell_id.is_unique and len(out) == N_CELLS, "Map output population failure")
    require(out.loc[out.island_flag.eq(1), "significant_bh_005"].eq(0).all(), "Island classified significant")
    return out


def create_schema(csv_frames):
    text = []
    for name, frame in csv_frames:
        text.extend([f"[{name}]", "Format=CSVDelimited", "ColNameHeader=True", "MaxScanRows=0"])
        for index, column in enumerate(frame.columns, 1):
            if column in {"cell_id", "metric", "lisa_class", "analysis_status", "primary_biome"}:
                kind = "Text Width 64"
            elif pd.api.types.is_integer_dtype(frame[column]):
                kind = "Long"
            else:
                kind = "Double"
            text.append(f"Col{index}={column} {kind}")
        text.append("")
    return "\n".join(text)


def create_summaries(results, attributes, output):
    enriched = results.merge(attributes, on="cell_id", how="left", validate="many_to_one")
    require(enriched.geometry_area_aea_ha.notna().all(), "Missing cell areas after join")
    class_summary = enriched.groupby(
        ["metric", "t0", "t1", "diagnostic_interval", "lisa_class"], dropna=False
    ).agg(cells=("cell_id", "size"), cell_footprint_ha=("geometry_area_aea_ha", "sum"),
          metric_value_sum=("metric_value", lambda x: x.sum(min_count=1)), metric_value_mean=("metric_value", "mean"),
          metric_value_median=("metric_value", "median")).reset_index()
    class_summary.to_csv(output / "canonical_local_moran_class_summary_v1.csv", index=False, float_format="%.17g")
    biome = enriched.groupby(
        ["metric", "t0", "t1", "diagnostic_interval", "primary_biome", "lisa_class"], dropna=False
    ).agg(cells=("cell_id", "size"), cell_footprint_ha=("geometry_area_aea_ha", "sum"),
          metric_value_sum=("metric_value", lambda x: x.sum(min_count=1))).reset_index()
    biome.to_csv(output / "canonical_local_moran_biome_summary_v1.csv", index=False, float_format="%.17g")

    trajectory_rows = []
    for (metric, cell_id), group in results.sort_values("t0").groupby(["metric", "cell_id"], sort=False):
        sequence = group.lisa_class.tolist()
        primary = sequence[:7]
        trajectory_rows.append({
            "metric": metric, "cell_id": cell_id,
            "lisa_sequence_full": "|".join(sequence), "lisa_sequence_primary": "|".join(primary),
            "hh_intervals_primary": primary.count("HH"), "ll_intervals_primary": primary.count("LL"),
            "hh_intervals_full": sequence.count("HH"), "ll_intervals_full": sequence.count("LL"),
            "max_hh_run_primary": max_run(primary, "HH"), "max_ll_run_primary": max_run(primary, "LL"),
            "max_hh_run_full": max_run(sequence, "HH"), "max_ll_run_full": max_run(sequence, "LL"),
            "hh_persistent_2plus_primary": int(max_run(primary, "HH") >= 2),
            "ll_persistent_2plus_primary": int(max_run(primary, "LL") >= 2),
            "diagnostic_continues_hh": int(len(sequence) == 8 and sequence[-2:] == ["HH", "HH"]),
            "diagnostic_continues_ll": int(len(sequence) == 8 and sequence[-2:] == ["LL", "LL"]),
        })
    trajectories = pd.DataFrame(trajectory_rows)
    require(len(trajectories) == N_CELLS * len(METRICS), "Trajectory population failure")
    trajectories.to_parquet(output / "canonical_local_moran_persistence_v1.parquet", index=False)
    persistence_summary = trajectories.groupby("metric").agg(
        cells=("cell_id", "size"), hh_persistent_2plus_primary=("hh_persistent_2plus_primary", "sum"),
        ll_persistent_2plus_primary=("ll_persistent_2plus_primary", "sum"),
        diagnostic_continues_hh=("diagnostic_continues_hh", "sum"),
        diagnostic_continues_ll=("diagnostic_continues_ll", "sum"),
    ).reset_index()
    persistence_summary.to_csv(output / "canonical_local_moran_persistence_summary_v1.csv", index=False)

    jaccard_rows = []
    for metric, group in results.groupby("metric"):
        sets = {(int(t0), cls): set(part.loc[part.lisa_class.eq(cls), "cell_id"])
                for t0, part in group.groupby("t0") for cls in ["HH", "LL"]}
        for t0 in range(1985, 2020, 5):
            for cls in ["HH", "LL"]:
                left, right = sets[(t0, cls)], sets[(t0 + 5, cls)]
                union = left | right
                jaccard_rows.append({
                    "metric": metric, "lisa_class": cls, "t0_from": t0, "t0_to": t0 + 5,
                    "destination_diagnostic_interval": int(t0 + 5 == 2020),
                    "cells_from": len(left), "cells_to": len(right), "intersection_cells": len(left & right),
                    "union_cells": len(union), "jaccard": len(left & right) / len(union) if union else np.nan,
                })
    pd.DataFrame(jaccard_rows).to_csv(output / "canonical_local_moran_adjacent_jaccard_v1.csv", index=False, float_format="%.17g")
    return class_summary, trajectories


def create_maps(results, spatial, output):
    import geopandas as gpd
    maps = output / "maps"
    maps.mkdir(exist_ok=True)
    geo = spatial[["cell_id", "geometry"]].copy()
    if geo.crs is None:
        raise ValueError("Spatial support CRS is missing")
    if not geo.crs.is_projected:
        geo = geo.to_crs(AEA)
    bounds = geo.total_bounds
    legend = [Patch(facecolor=COLORS[k], edgecolor="#555555", label=k) for k in
              ["HH", "LL", "HL", "LH", "not_significant", "island", "not_applicable"]]
    for metric in METRICS:
        fig, axes = plt.subplots(2, 4, figsize=(16, 9))
        for ax, t0 in zip(axes.ravel(), range(1985, 2025, 5)):
            frame = geo.merge(results[(results.metric.eq(metric)) & (results.t0.eq(t0))], on="cell_id", validate="one_to_one")
            draw_class = frame.lisa_class.copy()
            draw_class.loc[frame.island_flag.eq(1)] = "island"
            frame.plot(ax=ax, color=draw_class.map(COLORS), edgecolor="none", linewidth=0, rasterized=True)
            ax.set_xlim(bounds[0], bounds[2]); ax.set_ylim(bounds[1], bounds[3]); ax.set_axis_off()
            ax.set_title(f"{t0}–{t0+5}" + (" (diagnóstico)" if t0 == 2020 else ""), fontsize=10)
        fig.legend(handles=legend, loc="lower center", ncol=7, frameon=False, fontsize=9)
        fig.suptitle(f"Moran local (LISA, BH 5%) — {metric}", fontsize=14)
        fig.tight_layout(rect=[0, .055, 1, .96])
        fig.savefig(maps / f"local_moran_{metric}_v1.png", dpi=180, bbox_inches="tight")
        fig.savefig(maps / f"local_moran_{metric}_v1.svg", bbox_inches="tight")
        plt.close(fig)


def run(args):
    print("CANONICAL LOCAL MORAN / LISA — PHASE 6 VERSION 1", flush=True)
    print("9,999 PERMUTATIONS; CHECKPOINTS; BH PRIMARY; BY SENSITIVITY", flush=True)
    engine = verify_engine()
    print("Statistical-engine verification: PASS", flush=True)
    root = args.project_dir
    if not root.exists() and str(root).startswith("/content/drive/"):
        from google.colab import drive
        drive.mount("/content/drive")
    paths = {
        "metrics": root / "spatial/phase2/canonical_spatial_metrics_panel_v1.parquet",
        "weights": root / "spatial/phase1/canonical_contiguity_weights_v1.parquet",
        "spatial": root / "spatial/phase1/canonical_spatial_support_v1.parquet",
    }
    inputs = {}
    for key, expected in [("metrics", PANEL_HASH), ("weights", GRAPH_HASH), ("spatial", SPATIAL_HASH)]:
        require(paths[key].is_file(), "Missing input: " + str(paths[key]))
        digest = sha256(paths[key]); require(digest == expected, "Input hash mismatch: " + key)
        inputs[key] = {"path": str(paths[key]), "sha256": digest}
    import geopandas as gpd
    panel = pd.read_parquet(paths["metrics"]); panel.cell_id = panel.cell_id.astype(str)
    graph = pd.read_parquet(paths["weights"]); graph.focal_cell_id = graph.focal_cell_id.astype(str); graph.neighbor_cell_id = graph.neighbor_cell_id.astype(str)
    spatial = gpd.read_parquet(paths["spatial"]); spatial.cell_id = spatial.cell_id.astype(str)
    require(len(panel) == 199112 and not panel.duplicated(["cell_id", "t0", "t1"]).any(), "Invalid panel keys")
    require(len(spatial) == N_CELLS and spatial.cell_id.is_unique, "Invalid spatial population")
    ids = sorted(spatial.cell_id.tolist())
    require(set(panel.cell_id) == set(ids), "Panel/spatial populations differ")
    require(len(graph) == 134906 and not graph.duplicated(["focal_cell_id", "neighbor_cell_id"]).any(), "Invalid graph rows")
    require(set(graph.focal_cell_id).issubset(ids) and set(graph.neighbor_cell_id).issubset(ids), "Unknown graph cell")
    require(graph.focal_cell_id.ne(graph.neighbor_cell_id).all(), "Graph contains self-links")
    directed_edges = set(zip(graph.focal_cell_id, graph.neighbor_cell_id))
    require(all((neighbor, focal) in directed_edges for focal, neighbor in directed_edges), "Graph is not symmetric")
    degree_map = graph.groupby("focal_cell_id").size().reindex(ids, fill_value=0).to_numpy(int)
    require(int((degree_map == 0).sum()) == 163 and int(degree_map.sum()) == 134906, "Canonical degree diagnostics differ")
    for metric, flag in METRICS.items():
        require(metric in panel and (flag is None or flag in panel), "Missing metric/support field: " + metric)
    output = args.output_dir or root / "spatial/phase6/local_moran_v1"
    output.mkdir(parents=True, exist_ok=True)
    checkpoints = output / "checkpoints"; checkpoints.mkdir(exist_ok=True)
    write_json(output / "canonical_local_moran_design_v1.json", {
        "script_version": VERSION, "metrics": METRICS, "intervals": [[y, y + 5] for y in range(1985, 2025, 5)],
        "diagnostic_interval": [2020, 2025], "permutations": args.permutations, "master_seed": MASTER_SEED,
        "weights": "accepted binary contiguity graph, row-standardized within the eligible support",
        "permutation_null": "PySAL conditional randomization at each location",
        "pvalue": "esda.Moran_Local p_sim; one-sided extremeness relative to conditional simulations",
        "multiple_testing_primary": "Benjamini-Hochberg within each metric x interval map, alpha=0.05",
        "multiple_testing_sensitivity": "Benjamini-Yekutieli within the same family",
        "islands": "retained; zero spatial lag; never significant; no artificial links",
        "quadrants": QUADRANTS,
    })
    frames = []
    for metric, support_flag in METRICS.items():
        for t0 in range(1985, 2025, 5):
            stem = f"checkpoint_{metric}_{t0}_{t0+5}_v1"
            data_path, meta_path = checkpoints / f"{stem}.parquet", checkpoints / f"{stem}.json"
            config = checkpoint_config(metric, t0, stable_seed(metric, t0), args.permutations)
            frame = read_checkpoint(data_path, meta_path, config)
            if frame is None:
                interval = panel.loc[panel.t0.eq(t0)].copy()
                require(len(interval) == N_CELLS and interval.cell_id.is_unique, f"Interval population differs: {t0}")
                frame = compute_map(metric, support_flag, t0, interval, ids, graph, degree_map, args.permutations)
                frame.to_parquet(data_path, index=False)
                write_json(meta_path, {"config": config, "rows": len(frame), "parquet_sha256": sha256(data_path),
                                      "created_utc": datetime.now(timezone.utc).isoformat()})
                status = "COMPUTED"
            else:
                status = "REUSED"
            frames.append(frame)
            print(f"{status} | {metric} | {t0}–{t0+5} | BH significant={int(frame.significant_bh_005.sum()):,}", flush=True)
    results = pd.concat(frames, ignore_index=True)
    require(len(results) == N_CELLS * 40 and not results.duplicated(["cell_id", "metric", "t0"]).any(), "Consolidated result keys differ")
    results.to_parquet(output / "canonical_local_moran_cell_results_v1.parquet", index=False)
    attrs = spatial[["cell_id", "geometry_area_aea_ha", "primary_biome", "amazon_fraction_cell", "cerrado_fraction_cell"]].copy()
    attrs["transbiome_flag"] = (attrs.amazon_fraction_cell.gt(0) & attrs.cerrado_fraction_cell.gt(0)).astype(np.int8)
    class_summary, trajectories = create_summaries(results, attrs, output)

    gis = output / "gis"; gis.mkdir(exist_ok=True)
    csv_frames, manifest = [], []
    gis_columns = ["cell_id", "metric", "t0", "t1", "diagnostic_interval", "metric_value", "supported_flag",
                   "full_graph_degree", "local_graph_degree", "island_flag", "z_score", "spatial_lag_z", "local_moran_i",
                   "quadrant_code", "p_sim", "q_bh", "q_by", "significant_bh_005", "significant_by_005", "lisa_class", "analysis_status"]
    for (metric, t0), part in results.groupby(["metric", "t0"], sort=True):
        name = f"lisa_{metric}_{t0}_{t0+5}_v1.csv"
        export = part[gis_columns].copy()
        export.to_csv(gis / name, index=False, encoding="utf-8-sig", float_format="%.17g")
        csv_frames.append((name, export)); manifest.append({"file": name, "metric": metric, "t0": t0, "t1": t0+5,
                                                             "rows": len(export), "sha256": sha256(gis / name)})
    (gis / "schema.ini").write_text(create_schema(csv_frames), encoding="ascii")
    pd.DataFrame(manifest).to_csv(gis / "canonical_local_moran_gis_manifest_v1.csv", index=False)
    create_maps(results, spatial, output)
    zip_base = output / "canonical_local_moran_gis_tables_v1"
    if zip_base.with_suffix(".zip").exists():
        zip_base.with_suffix(".zip").unlink()
    shutil.make_archive(str(zip_base), "zip", gis)

    public_files = [p for p in output.iterdir() if p.is_file() and p.name != "canonical_local_moran_validation_v1.json"]
    public_files += sorted((output / "maps").glob("*"))
    validation = {
        "validation_status": "PASS", "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": sha256(__file__),
        "inputs": inputs, "engine_checks": engine,
        "population": {"cells": N_CELLS, "metrics": 5, "intervals": 8, "maps": 40, "cell_results": len(results)},
        "graph": {"directed_edges": 134906, "undirected_edges": 67453, "complete_graph_islands": 163},
        "results": {"bh_significant_cells": int(results.significant_bh_005.sum()),
                    "by_significant_cells": int(results.significant_by_005.sum()),
                    "unsupported_rows": int(results.supported_flag.eq(0).sum()),
                    "island_rows": int(results.island_flag.eq(1).sum()),
                    "class_count_rows": len(class_summary), "trajectory_rows": len(trajectories)},
        "outputs": {p.relative_to(output).as_posix(): {"sha256": sha256(p), "bytes": p.stat().st_size} for p in public_files},
    }
    write_json(output / "canonical_local_moran_validation_v1.json", validation)
    print("LOCAL MORAN / LISA COMPLETE — VALIDATION PASS", flush=True)
    print("Output:", output, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=Path("/content/drive/MyDrive/Trabalho/Contabilidade"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(verify_engine(), indent=2))
    else:
        require(args.permutations == PERMUTATIONS, "Production requires the prespecified 9,999 permutations")
        run(args)

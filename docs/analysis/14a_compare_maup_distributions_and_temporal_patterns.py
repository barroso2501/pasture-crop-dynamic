"""Compare canonical and alternative-grid metrics for Phase 8C.

This script performs the descriptive and temporal MAUP comparison that follows
the accepted Phase 8B alternative-grid production. It does not construct
spatial weights or calculate Moran/LISA statistics.

Colab
------
%run /content/14a_compare_maup_distributions_and_temporal_patterns.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


if importlib.util.find_spec("pyarrow") is None:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "pyarrow>=14"]
    )

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from google.colab import drive
except ImportError:
    drive = None


VERSION = "phase8c-maup-distribution-temporal-comparison-v1"
PROJECT_DIR = Path(os.environ.get(
    "PHASE8_PROJECT_DIR",
    "/content/drive/MyDrive/Trabalho/Contabilidade",
))
CANONICAL_PANEL = (
    PROJECT_DIR / "spatial" / "phase2" / "canonical_spatial_metrics_panel_v1.parquet"
)
ALTERNATIVE_PANEL = (
    PROJECT_DIR / "spatial" / "phase8" / "maup_metrics_v1"
    / "canonical_maup_core_metrics_panel_v4.parquet"
)
OUTPUT_DIR = (
    PROJECT_DIR / "spatial" / "phase8" / "maup_comparison_v1"
)
FIGURE_DIR = OUTPUT_DIR / "figures"

EXPECTED_CANONICAL_SHA256 = (
    "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c"
)
EXPECTED_ALTERNATIVE_SHA256 = (
    "cdd5d4db2abb7648f8801694de93e6976d8073e271c12bd71b8c972b2a366313"
)
EXPECTED_CANONICAL_ROWS = 199_112
EXPECTED_CANONICAL_CELLS = 24_889
EXPECTED_ALTERNATIVE_ROWS = 809_800
GRID_ROWS = {
    "hex10k_base": 56_520,
    "hex20k_shift": 29_396,
    "hex40k_base": 15_309,
}
EXPECTED_SUPPORT_COUNTS = {
    "hex10k_base": {25: 52_404, 50: 49_716, 75: 47_191},
    "hex20k_shift": {25: 27_352, 50: 25_015, 75: 22_426},
    "hex40k_base": {25: 13_759, 50: 12_445, 75: 11_160},
}
INTERVALS = [
    (1985, 1990), (1990, 1995), (1995, 2000), (2000, 2005),
    (2005, 2010), (2010, 2015), (2015, 2020), (2020, 2025),
]
GRID_ORDER = [
    "hex20k_canonical", "hex10k_base", "hex20k_shift", "hex40k_base"
]
ALTERNATIVE_GRIDS = GRID_ORDER[1:]
EFFECT_LABELS = {
    "hex10k_base": "finer_scale_10k",
    "hex20k_shift": "zoning_shift_20k",
    "hex40k_base": "coarser_scale_40k",
}
SUPPORT_SCOPES = {
    "primary_ge_50pct": "support_ge_50pct",
    "sensitivity_ge_25pct": "support_ge_25pct",
    "sensitivity_ge_75pct": "support_ge_75pct",
}

ZERO_TOLERANCE_HA = 1e-9
TOTAL_RELATIVE_THRESHOLD = 0.002
AGGREGATE_ABSOLUTE_THRESHOLD = 0.02
NET_GROSS_NORMALIZED_THRESHOLD = 0.02
WEIGHTED_KS_THRESHOLD = 0.10
DEFINED_SUPPORT_FRACTION_THRESHOLD = 0.05
TEMPORAL_SPEARMAN_THRESHOLD = 0.90
EXTREMUM_INTERVAL_DISTANCE_THRESHOLD = 1

AREA_METRICS = {
    "consolidation_density_per_10kha": "consolidation_ha",
    "replenishment_density_per_10kha": "replenishment_ha",
    "nat_tmp_density_per_10kha": "nat_tmp_endpoint_ha",
    "net_cr_balance_density_per_10kha": "net_cr_balance_ha",
}
CONDITIONAL_METRICS = [
    "cr_balance_index",
    "consolidation_rate_initial_pasture",
    "replenishment_rate_initial_native",
    "nat_tmp_intensity_initial_native",
]
DISTRIBUTION_METRICS = [*AREA_METRICS, *CONDITIONAL_METRICS]
AGGREGATE_METRICS = [
    "consolidation_ha",
    "replenishment_ha",
    "nat_tmp_endpoint_ha",
    "net_cr_balance_ha",
    "aggregate_cr_balance_index",
    "aggregate_consolidation_rate",
    "aggregate_replenishment_rate",
    "aggregate_nat_tmp_intensity",
]
FOCAL_TOTALS = {
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha"
}
RATE_INDEX_METRICS = {
    "aggregate_cr_balance_index",
    "aggregate_consolidation_rate",
    "aggregate_replenishment_rate",
    "aggregate_nat_tmp_intensity",
}
QUANTILES = [0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99, 1.0]

CANONICAL_COLUMNS = [
    "cell_id", "t0", "t1", "interval", "diagnostic_interval",
    "geometry_area_aea_ha", "stock0_pas", "stock0_nat",
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
    "net_cr_balance_ha", "cr_balance_index",
    "consolidation_rate_initial_pasture",
    "replenishment_rate_initial_native",
    "nat_tmp_intensity_initial_native",
    "consolidation_rate_defined", "replenishment_rate_defined",
    "nat_tmp_intensity_defined", "cr_balance_defined",
]
ALTERNATIVE_COLUMNS = [
    "maup_cell_id", "grid_code", "t0", "t1", "interval",
    "diagnostic_interval", "raster_domain_support_ha",
    "domain_support_fraction", "support_ge_25pct", "support_ge_50pct",
    "support_ge_75pct", "stock0_pas_ha", "stock0_nat_ha",
    "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
    "net_cr_balance_ha", "cr_balance_index",
    "consolidation_rate_initial_pasture",
    "replenishment_rate_initial_native",
    "nat_tmp_intensity_initial_native",
    "consolidation_rate_defined", "replenishment_rate_defined",
    "nat_tmp_intensity_defined", "has_cr_activity",
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


def safe_ratio(numerator: float, denominator: float) -> float:
    if not np.isfinite(denominator) or abs(denominator) <= ZERO_TOLERANCE_HA:
        return np.nan
    return float(numerator / denominator)


def sign_code(value: float, tolerance: float = ZERO_TOLERANCE_HA) -> str:
    if not np.isfinite(value):
        return "undefined"
    if value > tolerance:
        return "positive"
    if value < -tolerance:
        return "negative"
    return "zero"


def balance_class(value: float) -> str:
    if not np.isfinite(value):
        return "inactive"
    if value < -1.0 / 3.0:
        return "replenishment_dominant"
    if value <= 1.0 / 3.0:
        return "mixed"
    return "consolidation_dominant"


def weighted_quantiles(values, weights, quantiles=QUANTILES) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    require(valid.any(), "Weighted quantile received no valid observations")
    values = values[valid]
    weights = weights[valid]
    order = np.argsort(values, kind="mergesort")
    values = values[order]
    weights = weights[order]
    cumulative = np.cumsum(weights)
    targets = np.asarray(quantiles, dtype=float) * cumulative[-1]
    positions = np.searchsorted(cumulative, targets, side="left")
    positions = np.clip(positions, 0, len(values) - 1)
    return values[positions]


def weighted_moments(values, weights) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    require(valid.any(), "Weighted moments received no valid observations")
    values = values[valid]
    weights = weights[valid]
    total = weights.sum()
    mean = float(np.sum(values * weights) / total)
    variance = float(np.sum(weights * (values - mean) ** 2) / total)
    return mean, float(np.sqrt(max(variance, 0.0)))


def weighted_ks(values_a, weights_a, values_b, weights_b) -> float:
    def prepared(values, weights):
        values = np.asarray(values, dtype=float)
        weights = np.asarray(weights, dtype=float)
        valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
        require(valid.any(), "Weighted KS received an empty valid sample")
        values = values[valid]
        weights = weights[valid]
        order = np.argsort(values, kind="mergesort")
        values = values[order]
        cumulative = np.cumsum(weights[order])
        cumulative = cumulative / cumulative[-1]
        return values, cumulative

    a_values, a_cumulative = prepared(values_a, weights_a)
    b_values, b_cumulative = prepared(values_b, weights_b)
    points = np.union1d(a_values, b_values)

    def cdf_at(values, cumulative):
        positions = np.searchsorted(values, points, side="right") - 1
        result = np.zeros(len(points), dtype=float)
        valid = positions >= 0
        result[valid] = cumulative[positions[valid]]
        return result

    return float(np.max(np.abs(
        cdf_at(a_values, a_cumulative) - cdf_at(b_values, b_cumulative)
    )))


def rank_correlation(values_a, values_b) -> float:
    a = pd.Series(np.asarray(values_a, dtype=float))
    b = pd.Series(np.asarray(values_b, dtype=float))
    valid = a.notna() & b.notna()
    require(valid.sum() >= 2, "Too few paired values for temporal correlation")
    a = a[valid]
    b = b[valid]
    if a.nunique() == 1 and b.nunique() == 1:
        return 1.0 if np.isclose(a.iloc[0], b.iloc[0]) else 0.0
    if a.nunique() == 1 or b.nunique() == 1:
        return 0.0
    return float(a.rank(method="average").corr(b.rank(method="average")))


def verify_engine() -> None:
    q = weighted_quantiles([0, 1, 2, 3], [1, 1, 1, 1], [0.0, 0.5, 1.0])
    require(np.array_equal(q, np.array([0.0, 1.0, 3.0])),
            "Weighted-quantile engine verification failed")
    require(abs(weighted_ks([0, 1], [1, 1], [0, 1], [1, 1])) < 1e-15,
            "Weighted-KS identity verification failed")
    require(np.isclose(weighted_ks([0, 0], [1, 1], [1, 1], [1, 1]), 1.0),
            "Weighted-KS separation verification failed")
    require(np.isclose(rank_correlation([1, 2, 3], [10, 20, 30]), 1.0),
            "Temporal-rank engine verification failed")


def read_inputs() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    require(CANONICAL_PANEL.is_file(), f"Missing canonical panel: {CANONICAL_PANEL}")
    require(ALTERNATIVE_PANEL.is_file(), f"Missing alternative panel: {ALTERNATIVE_PANEL}")
    canonical_hash = sha256_file(CANONICAL_PANEL)
    alternative_hash = sha256_file(ALTERNATIVE_PANEL)
    require(canonical_hash == EXPECTED_CANONICAL_SHA256,
            "Canonical Phase 2 panel hash mismatch")
    require(alternative_hash == EXPECTED_ALTERNATIVE_SHA256,
            "Alternative Phase 8B panel hash mismatch")

    canonical = pd.read_parquet(CANONICAL_PANEL, columns=CANONICAL_COLUMNS)
    alternative = pd.read_parquet(ALTERNATIVE_PANEL, columns=ALTERNATIVE_COLUMNS)
    require(len(canonical) == EXPECTED_CANONICAL_ROWS,
            "Unexpected canonical panel population")
    require(len(alternative) == EXPECTED_ALTERNATIVE_ROWS,
            "Unexpected alternative panel population")
    return canonical, alternative, {
        "canonical_panel": {
            "path": str(CANONICAL_PANEL), "sha256": canonical_hash,
            "rows": len(canonical),
        },
        "alternative_panel": {
            "path": str(ALTERNATIVE_PANEL), "sha256": alternative_hash,
            "rows": len(alternative),
        },
    }


def harmonize(canonical: pd.DataFrame, alternative: pd.DataFrame) -> pd.DataFrame:
    require(not canonical.duplicated(["cell_id", "t0", "t1"]).any(),
            "Duplicate canonical cell-interval key")
    require(canonical["cell_id"].nunique() == EXPECTED_CANONICAL_CELLS,
            "Unexpected canonical cell count")
    require(canonical.groupby("cell_id").size().eq(len(INTERVALS)).all(),
            "Unbalanced canonical panel")

    can = canonical.rename(columns={
        "cell_id": "analysis_cell_id",
        "geometry_area_aea_ha": "analysis_support_ha",
        "stock0_pas": "stock0_pas_ha",
        "stock0_nat": "stock0_nat_ha",
        "cr_balance_defined": "has_cr_activity",
    }).copy()
    can["grid_code"] = "hex20k_canonical"
    can["domain_support_fraction"] = 1.0
    for pct in (25, 50, 75):
        can[f"support_ge_{pct}pct"] = 1

    alt = alternative.rename(columns={
        "maup_cell_id": "analysis_cell_id",
        "raster_domain_support_ha": "analysis_support_ha",
    }).copy()
    require(not alt.duplicated(["grid_code", "analysis_cell_id", "t0", "t1"]).any(),
            "Duplicate alternative grid-cell-interval key")
    require(set(alt["grid_code"].astype(str)) == set(ALTERNATIVE_GRIDS),
            "Unexpected alternative grid code")
    for grid_code, expected in GRID_ROWS.items():
        group = alt.loc[alt["grid_code"].eq(grid_code)]
        require(len(group) == expected * len(INTERVALS),
                f"Unexpected population for {grid_code}")
        require(group["analysis_cell_id"].nunique() == expected,
                f"Unexpected unique cells for {grid_code}")
        require(group.groupby("analysis_cell_id").size().eq(len(INTERVALS)).all(),
                f"Unbalanced intervals for {grid_code}")
        for pct in (25, 50, 75):
            counts = group.groupby(["t0", "t1"])[f"support_ge_{pct}pct"].sum()
            require(counts.eq(EXPECTED_SUPPORT_COUNTS[grid_code][pct]).all(),
                    f"Support population changed for {grid_code} at {pct}%")

    common_columns = [
        "analysis_cell_id", "grid_code", "t0", "t1", "interval",
        "diagnostic_interval", "analysis_support_ha", "domain_support_fraction",
        "support_ge_25pct", "support_ge_50pct", "support_ge_75pct",
        "stock0_pas_ha", "stock0_nat_ha", "consolidation_ha",
        "replenishment_ha", "nat_tmp_endpoint_ha", "net_cr_balance_ha",
        "cr_balance_index", "consolidation_rate_initial_pasture",
        "replenishment_rate_initial_native", "nat_tmp_intensity_initial_native",
        "consolidation_rate_defined", "replenishment_rate_defined",
        "nat_tmp_intensity_defined", "has_cr_activity",
    ]
    combined = pd.concat([can[common_columns], alt[common_columns]], ignore_index=True)
    combined["grid_code"] = pd.Categorical(
        combined["grid_code"], categories=GRID_ORDER, ordered=True
    )
    numeric_nonnegative = [
        "analysis_support_ha", "stock0_pas_ha", "stock0_nat_ha",
        "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha",
    ]
    require(np.isfinite(combined[numeric_nonnegative].to_numpy()).all(),
            "Non-finite required area in harmonized panel")
    require(combined[numeric_nonnegative].ge(-1e-8).all().all(),
            "Negative required area in harmonized panel")
    require(combined["analysis_support_ha"].gt(0).all(),
            "Non-positive analysis support")
    require(combined["diagnostic_interval"].eq(
        ((combined["t0"].eq(2020)) & (combined["t1"].eq(2025))).astype(int)
    ).all(), "Diagnostic interval flag mismatch")

    for output, source in AREA_METRICS.items():
        combined[output] = (
            combined[source] / combined["analysis_support_ha"] * 10_000.0
        )
    return combined


def build_aggregate_summary(combined: pd.DataFrame) -> pd.DataFrame:
    records = []
    for (grid_code, t0, t1), group in combined.groupby(
        ["grid_code", "t0", "t1"], observed=True, sort=True
    ):
        consolidation = float(group["consolidation_ha"].sum())
        replenishment = float(group["replenishment_ha"].sum())
        nat_tmp = float(group["nat_tmp_endpoint_ha"].sum())
        pasture = float(group["stock0_pas_ha"].sum())
        native = float(group["stock0_nat_ha"].sum())
        gross = consolidation + replenishment
        records.append({
            "grid_code": str(grid_code), "t0": int(t0), "t1": int(t1),
            "interval": f"{int(t0)}_{int(t1)}",
            "diagnostic_interval": int((int(t0), int(t1)) == (2020, 2025)),
            "cells": len(group),
            "analysis_support_ha": float(group["analysis_support_ha"].sum()),
            "consolidation_ha": consolidation,
            "replenishment_ha": replenishment,
            "nat_tmp_endpoint_ha": nat_tmp,
            "gross_cr_activity_ha": gross,
            "net_cr_balance_ha": consolidation - replenishment,
            "aggregate_cr_balance_index": safe_ratio(
                consolidation - replenishment, gross
            ),
            "aggregate_consolidation_rate": safe_ratio(consolidation, pasture),
            "aggregate_replenishment_rate": safe_ratio(replenishment, native),
            "aggregate_nat_tmp_intensity": safe_ratio(nat_tmp, native),
        })
    result = pd.DataFrame(records)
    require(len(result) == len(GRID_ORDER) * len(INTERVALS),
            "Unexpected aggregate-summary population")
    return result


def build_aggregate_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    canonical = summary.loc[
        summary["grid_code"].eq("hex20k_canonical")
    ].set_index(["t0", "t1"])
    records = []
    for grid_code in ALTERNATIVE_GRIDS:
        alternative = summary.loc[summary["grid_code"].eq(grid_code)].set_index(["t0", "t1"])
        for t0, t1 in INTERVALS:
            can = canonical.loc[(t0, t1)]
            alt = alternative.loc[(t0, t1)]
            for metric in AGGREGATE_METRICS:
                can_value = float(can[metric])
                alt_value = float(alt[metric])
                difference = alt_value - can_value
                relative = safe_ratio(abs(difference), abs(can_value))
                if metric in FOCAL_TOTALS:
                    criterion = "relative_difference_le_0p002"
                    statistic = relative
                    threshold = TOTAL_RELATIVE_THRESHOLD
                elif metric in RATE_INDEX_METRICS:
                    criterion = "absolute_difference_le_0p02"
                    statistic = abs(difference)
                    threshold = AGGREGATE_ABSOLUTE_THRESHOLD
                else:
                    criterion = "difference_over_canonical_gross_le_0p02"
                    statistic = safe_ratio(abs(difference), float(can["gross_cr_activity_ha"]))
                    threshold = NET_GROSS_NORMALIZED_THRESHOLD
                records.append({
                    "comparison_grid": grid_code,
                    "comparison_effect": EFFECT_LABELS[grid_code],
                    "t0": t0, "t1": t1, "interval": f"{t0}_{t1}",
                    "diagnostic_interval": int((t0, t1) == (2020, 2025)),
                    "metric": metric,
                    "canonical_value": can_value,
                    "alternative_value": alt_value,
                    "signed_difference": difference,
                    "absolute_difference": abs(difference),
                    "relative_difference": relative,
                    "criterion": criterion,
                    "criterion_statistic": statistic,
                    "criterion_threshold": threshold,
                    "criterion_pass": bool(np.isfinite(statistic) and statistic <= threshold),
                    "canonical_sign": sign_code(can_value),
                    "alternative_sign": sign_code(alt_value),
                    "sign_preserved": sign_code(can_value) == sign_code(alt_value),
                    "canonical_balance_class": (
                        balance_class(can_value)
                        if metric == "aggregate_cr_balance_index" else "not_applicable"
                    ),
                    "alternative_balance_class": (
                        balance_class(alt_value)
                        if metric == "aggregate_cr_balance_index" else "not_applicable"
                    ),
                })
    result = pd.DataFrame(records)
    result["balance_class_preserved"] = np.where(
        result["metric"].eq("aggregate_cr_balance_index"),
        result["canonical_balance_class"].eq(result["alternative_balance_class"]),
        True,
    )
    require(len(result) == len(ALTERNATIVE_GRIDS) * len(INTERVALS) * len(AGGREGATE_METRICS),
            "Unexpected aggregate-comparison population")
    return result


def selected_group(
    combined: pd.DataFrame, grid_code: str, t0: int, t1: int, flag: str
) -> pd.DataFrame:
    group = combined.loc[
        combined["grid_code"].astype(str).eq(grid_code)
        & combined["t0"].eq(t0)
        & combined["t1"].eq(t1)
    ]
    if grid_code != "hex20k_canonical":
        group = group.loc[group[flag].eq(1)]
    return group


def build_distribution_summary(combined: pd.DataFrame) -> pd.DataFrame:
    records = []
    for grid_code in GRID_ORDER:
        for t0, t1 in INTERVALS:
            for scope, flag in SUPPORT_SCOPES.items():
                group = selected_group(combined, grid_code, t0, t1, flag)
                total_weight = float(group["analysis_support_ha"].sum())
                require(total_weight > 0, "Selected support has zero weight")
                for metric in DISTRIBUTION_METRICS:
                    values = group[metric].to_numpy(dtype=float)
                    weights = group["analysis_support_ha"].to_numpy(dtype=float)
                    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
                    require(valid.any(), f"No defined values for {grid_code}, {metric}")
                    quantiles = weighted_quantiles(values[valid], weights[valid])
                    mean, std = weighted_moments(values[valid], weights[valid])
                    row = {
                        "grid_code": grid_code, "support_scope": scope,
                        "t0": t0, "t1": t1, "interval": f"{t0}_{t1}",
                        "diagnostic_interval": int((t0, t1) == (2020, 2025)),
                        "metric": metric, "selected_cells": len(group),
                        "defined_cells": int(valid.sum()),
                        "selected_support_ha": total_weight,
                        "defined_support_ha": float(weights[valid].sum()),
                        "defined_support_fraction": float(weights[valid].sum() / total_weight),
                        "weighted_mean": mean, "weighted_std": std,
                    }
                    for q, value in zip(QUANTILES, quantiles):
                        label = f"q{int(round(q * 100)):02d}"
                        row[label] = float(value)
                    records.append(row)
    result = pd.DataFrame(records)
    expected = len(GRID_ORDER) * len(INTERVALS) * len(SUPPORT_SCOPES) * len(DISTRIBUTION_METRICS)
    require(len(result) == expected, "Unexpected distribution-summary population")
    return result


def build_distribution_comparison(combined: pd.DataFrame) -> pd.DataFrame:
    records = []
    for grid_code in ALTERNATIVE_GRIDS:
        for t0, t1 in INTERVALS:
            for scope, flag in SUPPORT_SCOPES.items():
                canonical = selected_group(
                    combined, "hex20k_canonical", t0, t1, flag
                )
                alternative = selected_group(combined, grid_code, t0, t1, flag)
                for metric in DISTRIBUTION_METRICS:
                    can_values = canonical[metric].to_numpy(dtype=float)
                    can_weights = canonical["analysis_support_ha"].to_numpy(dtype=float)
                    alt_values = alternative[metric].to_numpy(dtype=float)
                    alt_weights = alternative["analysis_support_ha"].to_numpy(dtype=float)
                    can_valid = np.isfinite(can_values) & (can_weights > 0)
                    alt_valid = np.isfinite(alt_values) & (alt_weights > 0)
                    can_defined_fraction = float(
                        can_weights[can_valid].sum() / can_weights.sum()
                    )
                    alt_defined_fraction = float(
                        alt_weights[alt_valid].sum() / alt_weights.sum()
                    )
                    ks = weighted_ks(
                        can_values[can_valid], can_weights[can_valid],
                        alt_values[alt_valid], alt_weights[alt_valid],
                    )
                    coverage_difference = abs(
                        alt_defined_fraction - can_defined_fraction
                    )
                    records.append({
                        "comparison_grid": grid_code,
                        "comparison_effect": EFFECT_LABELS[grid_code],
                        "support_scope": scope,
                        "t0": t0, "t1": t1, "interval": f"{t0}_{t1}",
                        "diagnostic_interval": int((t0, t1) == (2020, 2025)),
                        "metric": metric,
                        "weighted_ks_distance": ks,
                        "weighted_ks_threshold": WEIGHTED_KS_THRESHOLD,
                        "weighted_ks_pass": ks <= WEIGHTED_KS_THRESHOLD,
                        "canonical_defined_support_fraction": can_defined_fraction,
                        "alternative_defined_support_fraction": alt_defined_fraction,
                        "defined_support_fraction_absolute_difference": coverage_difference,
                        "defined_support_fraction_threshold": DEFINED_SUPPORT_FRACTION_THRESHOLD,
                        "defined_support_fraction_pass": (
                            coverage_difference <= DEFINED_SUPPORT_FRACTION_THRESHOLD
                        ),
                    })
    result = pd.DataFrame(records)
    result["distribution_criterion_pass"] = (
        result["weighted_ks_pass"] & result["defined_support_fraction_pass"]
    )
    expected = len(ALTERNATIVE_GRIDS) * len(INTERVALS) * len(SUPPORT_SCOPES) * len(DISTRIBUTION_METRICS)
    require(len(result) == expected, "Unexpected distribution-comparison population")
    return result


def build_temporal_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    windows = {
        "primary_1985_2020": [(a, b) for a, b in INTERVALS if b <= 2020],
        "full_observed_1985_2025": INTERVALS,
    }
    canonical = summary.loc[
        summary["grid_code"].eq("hex20k_canonical")
    ].set_index(["t0", "t1"])
    records = []
    for grid_code in ALTERNATIVE_GRIDS:
        alternative = summary.loc[
            summary["grid_code"].eq(grid_code)
        ].set_index(["t0", "t1"])
        for window, intervals in windows.items():
            for metric in AGGREGATE_METRICS:
                can = np.array([canonical.loc[key, metric] for key in intervals], dtype=float)
                alt = np.array([alternative.loc[key, metric] for key in intervals], dtype=float)
                rho = rank_correlation(can, alt)
                can_peak = int(np.nanargmax(can))
                alt_peak = int(np.nanargmax(alt))
                can_trough = int(np.nanargmin(can))
                alt_trough = int(np.nanargmin(alt))
                peak_distance = abs(alt_peak - can_peak)
                trough_distance = abs(alt_trough - can_trough)
                sign_preserved = all(
                    sign_code(x) == sign_code(y) for x, y in zip(can, alt)
                )
                if metric == "aggregate_cr_balance_index":
                    class_preserved = all(
                        balance_class(x) == balance_class(y)
                        for x, y in zip(can, alt)
                    )
                else:
                    class_preserved = True
                stable = (
                    rho >= TEMPORAL_SPEARMAN_THRESHOLD
                    and peak_distance <= EXTREMUM_INTERVAL_DISTANCE_THRESHOLD
                    and trough_distance <= EXTREMUM_INTERVAL_DISTANCE_THRESHOLD
                    and sign_preserved
                    and class_preserved
                )
                records.append({
                    "comparison_grid": grid_code,
                    "comparison_effect": EFFECT_LABELS[grid_code],
                    "window": window, "metric": metric,
                    "interval_count": len(intervals),
                    "spearman_rank_correlation": rho,
                    "spearman_threshold": TEMPORAL_SPEARMAN_THRESHOLD,
                    "spearman_pass": rho >= TEMPORAL_SPEARMAN_THRESHOLD,
                    "canonical_peak_interval": f"{intervals[can_peak][0]}_{intervals[can_peak][1]}",
                    "alternative_peak_interval": f"{intervals[alt_peak][0]}_{intervals[alt_peak][1]}",
                    "peak_interval_distance": peak_distance,
                    "canonical_trough_interval": f"{intervals[can_trough][0]}_{intervals[can_trough][1]}",
                    "alternative_trough_interval": f"{intervals[alt_trough][0]}_{intervals[alt_trough][1]}",
                    "trough_interval_distance": trough_distance,
                    "extrema_distance_threshold": EXTREMUM_INTERVAL_DISTANCE_THRESHOLD,
                    "sign_sequence_preserved": sign_preserved,
                    "balance_class_sequence_preserved": class_preserved,
                    "temporal_criterion_pass": stable,
                })
    result = pd.DataFrame(records)
    expected = len(ALTERNATIVE_GRIDS) * 2 * len(AGGREGATE_METRICS)
    require(len(result) == expected, "Unexpected temporal-comparison population")
    return result


def build_assessment(
    aggregate_comparison: pd.DataFrame,
    distribution_comparison: pd.DataFrame,
    temporal_comparison: pd.DataFrame,
) -> pd.DataFrame:
    records = []
    for grid_code in ALTERNATIVE_GRIDS:
        for window in ("primary_1985_2020", "full_observed_1985_2025"):
            is_primary = window == "primary_1985_2020"
            agg = aggregate_comparison.loc[
                aggregate_comparison["comparison_grid"].eq(grid_code)
                & (aggregate_comparison["t1"].le(2020) if is_primary else True)
            ]
            dist = distribution_comparison.loc[
                distribution_comparison["comparison_grid"].eq(grid_code)
                & distribution_comparison["support_scope"].eq("primary_ge_50pct")
                & (distribution_comparison["t1"].le(2020) if is_primary else True)
            ]
            temporal = temporal_comparison.loc[
                temporal_comparison["comparison_grid"].eq(grid_code)
                & temporal_comparison["window"].eq(window)
            ]
            require(len(agg) > 0 and len(dist) > 0 and len(temporal) > 0,
                    "Empty robustness assessment component")
            aggregate_pass = bool(
                agg["criterion_pass"].all()
                and agg["sign_preserved"].all()
                and agg["balance_class_preserved"].all()
            )
            distribution_pass = bool(dist["distribution_criterion_pass"].all())
            temporal_pass = bool(temporal["temporal_criterion_pass"].all())
            overall = aggregate_pass and distribution_pass and temporal_pass
            records.append({
                "comparison_grid": grid_code,
                "comparison_effect": EFFECT_LABELS[grid_code],
                "window": window,
                "aggregate_checks": len(agg),
                "aggregate_failed": int((~agg["criterion_pass"]).sum()),
                "aggregate_direction_or_class_failed": int((~(
                    agg["sign_preserved"] & agg["balance_class_preserved"]
                )).sum()),
                "aggregate_component_pass": aggregate_pass,
                "distribution_checks": len(dist),
                "distribution_failed": int((~dist["distribution_criterion_pass"]).sum()),
                "distribution_component_pass": distribution_pass,
                "temporal_checks": len(temporal),
                "temporal_failed": int((~temporal["temporal_criterion_pass"]).sum()),
                "temporal_component_pass": temporal_pass,
                "overall_prespecified_robustness_pass": overall,
                "assessment": (
                    "stable_under_prespecified_criteria"
                    if overall else "sensitive_for_at_least_one_criterion"
                ),
            })
    result = pd.DataFrame(records)
    require(len(result) == len(ALTERNATIVE_GRIDS) * 2,
            "Unexpected robustness-assessment population")
    return result


def create_figures(
    aggregate_comparison: pd.DataFrame,
    distribution_summary: pd.DataFrame,
    distribution_comparison: pd.DataFrame,
    aggregate_summary: pd.DataFrame,
) -> list[Path]:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    colors = {
        "hex20k_canonical": "#222222", "hex10k_base": "#2B8CBE",
        "hex20k_shift": "#7B3294", "hex40k_base": "#E34A33",
    }
    paths = []

    focal = aggregate_comparison.loc[
        aggregate_comparison["metric"].isin(FOCAL_TOTALS)
    ].copy()
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for axis, metric in zip(axes, [
        "consolidation_ha", "replenishment_ha", "nat_tmp_endpoint_ha"
    ]):
        metric_data = focal.loc[focal["metric"].eq(metric)]
        for grid_code in ALTERNATIVE_GRIDS:
            group = metric_data.loc[metric_data["comparison_grid"].eq(grid_code)]
            axis.plot(group["interval"], group["relative_difference"] * 100,
                      marker="o", label=grid_code, color=colors[grid_code])
        axis.axhline(TOTAL_RELATIVE_THRESHOLD * 100, color="#777777",
                     linestyle="--", linewidth=1)
        axis.set_ylabel("Absolute difference (%)")
        axis.set_title(metric)
        axis.grid(axis="y", alpha=0.2)
    axes[-1].tick_params(axis="x", rotation=45)
    axes[0].legend(ncol=3, frameon=False)
    fig.suptitle("Alternative-grid aggregate differences from the canonical grid")
    fig.tight_layout()
    path = FIGURE_DIR / "fig01_maup_aggregate_relative_differences_v1.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    paths.append(path)

    density_metrics = [
        "consolidation_density_per_10kha",
        "replenishment_density_per_10kha",
        "nat_tmp_density_per_10kha",
    ]
    data = distribution_summary.loc[
        distribution_summary["support_scope"].eq("primary_ge_50pct")
        & distribution_summary["metric"].isin(density_metrics)
    ]
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    for axis, metric in zip(axes, density_metrics):
        for grid_code in GRID_ORDER:
            group = data.loc[
                data["metric"].eq(metric) & data["grid_code"].eq(grid_code)
            ]
            axis.plot(group["interval"], group["q50"], marker="o",
                      color=colors[grid_code], label=grid_code)
        axis.set_ylabel("Weighted median\n(ha per 10,000 ha)")
        axis.set_title(metric)
        axis.grid(axis="y", alpha=0.2)
    axes[-1].tick_params(axis="x", rotation=45)
    axes[0].legend(ncol=2, frameon=False)
    fig.suptitle("Support-weighted median process densities")
    fig.tight_layout()
    path = FIGURE_DIR / "fig02_maup_weighted_median_densities_v1.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    paths.append(path)

    primary = distribution_comparison.loc[
        distribution_comparison["support_scope"].eq("primary_ge_50pct")
    ].copy()
    heat = primary.pivot_table(
        index=["comparison_grid", "metric"], columns="interval",
        values="weighted_ks_distance", aggfunc="first"
    )
    fig, axis = plt.subplots(figsize=(11, 9))
    image = axis.imshow(heat.to_numpy(), aspect="auto", vmin=0, vmax=max(
        WEIGHTED_KS_THRESHOLD, float(heat.max().max())
    ), cmap="viridis")
    axis.set_yticks(np.arange(len(heat)))
    axis.set_yticklabels([f"{a} | {b}" for a, b in heat.index], fontsize=8)
    axis.set_xticks(np.arange(len(heat.columns)))
    axis.set_xticklabels(heat.columns, rotation=45, ha="right")
    axis.set_title("Weighted distribution distance from canonical grid (primary support)")
    fig.colorbar(image, ax=axis, label="Weighted KS distance")
    fig.tight_layout()
    path = FIGURE_DIR / "fig03_maup_weighted_ks_heatmap_v1.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    paths.append(path)

    metrics = [
        "aggregate_cr_balance_index", "aggregate_consolidation_rate",
        "aggregate_replenishment_rate", "aggregate_nat_tmp_intensity",
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    for axis, metric in zip(axes.ravel(), metrics):
        for grid_code in GRID_ORDER:
            group = aggregate_summary.loc[
                aggregate_summary["grid_code"].eq(grid_code)
            ]
            axis.plot(group["interval"], group[metric], marker="o",
                      color=colors[grid_code], label=grid_code)
        axis.set_title(metric)
        axis.grid(axis="y", alpha=0.2)
        axis.tick_params(axis="x", rotation=45)
    axes[0, 0].legend(ncol=2, frameon=False)
    fig.suptitle("Aggregate balance and stock-specific rates by grid")
    fig.tight_layout()
    path = FIGURE_DIR / "fig04_maup_aggregate_balance_and_rates_v1.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    paths.append(path)
    return paths


def output_inventory(paths: list[Path]) -> pd.DataFrame:
    return pd.DataFrame([
        {"relative_path": str(path.relative_to(OUTPUT_DIR)),
         "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        for path in paths
    ])


def main() -> None:
    if drive is not None:
        drive.mount("/content/drive")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    print("CANONICAL MAUP DISTRIBUTION AND TEMPORAL COMPARISON — PHASE 8C VERSION 1")
    print("CANONICAL GRID REMAINS PRIMARY; ALTERNATIVE GRIDS ARE SENSITIVITY TESTS")
    print("DIAGNOSTIC 2020–2025: INCLUDED AND FLAGGED")
    print("Script version:", VERSION)
    print("Output directory:", OUTPUT_DIR)
    verify_engine()
    print("Comparison-engine verification: PASS")

    canonical, alternative, inputs = read_inputs()
    combined = harmonize(canonical, alternative)
    print("Inputs authenticated and harmonized:", f"{len(combined):,}", "rows")

    aggregate_summary = build_aggregate_summary(combined)
    aggregate_comparison = build_aggregate_comparison(aggregate_summary)
    distribution_summary = build_distribution_summary(combined)
    distribution_comparison = build_distribution_comparison(combined)
    temporal_comparison = build_temporal_comparison(aggregate_summary)
    assessment = build_assessment(
        aggregate_comparison, distribution_comparison, temporal_comparison
    )

    tables = {
        "canonical_maup_aggregate_summary_v1.csv": aggregate_summary,
        "canonical_maup_aggregate_comparison_v1.csv": aggregate_comparison,
        "canonical_maup_weighted_distribution_summary_v1.csv": distribution_summary,
        "canonical_maup_distribution_comparison_v1.csv": distribution_comparison,
        "canonical_maup_temporal_comparison_v1.csv": temporal_comparison,
        "canonical_maup_robustness_assessment_v1.csv": assessment,
    }
    output_paths = []
    for name, table in tables.items():
        path = OUTPUT_DIR / name
        table.to_csv(path, index=False, encoding="utf-8-sig")
        output_paths.append(path)

    figure_paths = create_figures(
        aggregate_comparison, distribution_summary,
        distribution_comparison, aggregate_summary,
    )
    output_paths.extend(figure_paths)

    validation_path = OUTPUT_DIR / "canonical_maup_comparison_validation_v1.json"
    validation = {
        "validation_status": "PASS",
        "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256_file(Path(__file__)),
        "inputs": inputs,
        "structure": {
            "harmonized_rows": len(combined),
            "canonical_rows": len(canonical),
            "alternative_rows": len(alternative),
            "grids": int(combined["grid_code"].nunique()),
            "intervals": int(combined[["t0", "t1"]].drop_duplicates().shape[0]),
            "aggregate_summary_rows": len(aggregate_summary),
            "aggregate_comparison_rows": len(aggregate_comparison),
            "distribution_summary_rows": len(distribution_summary),
            "distribution_comparison_rows": len(distribution_comparison),
            "temporal_comparison_rows": len(temporal_comparison),
            "assessment_rows": len(assessment),
        },
        "prespecified_thresholds": {
            "focal_total_relative_difference": TOTAL_RELATIVE_THRESHOLD,
            "aggregate_rate_or_index_absolute_difference": AGGREGATE_ABSOLUTE_THRESHOLD,
            "net_balance_difference_over_canonical_gross": NET_GROSS_NORMALIZED_THRESHOLD,
            "weighted_ks_distance": WEIGHTED_KS_THRESHOLD,
            "defined_support_fraction_absolute_difference": DEFINED_SUPPORT_FRACTION_THRESHOLD,
            "temporal_spearman": TEMPORAL_SPEARMAN_THRESHOLD,
            "extremum_interval_distance": EXTREMUM_INTERVAL_DISTANCE_THRESHOLD,
        },
        "result_counts": {
            "aggregate_failed": int((~aggregate_comparison["criterion_pass"]).sum()),
            "distribution_failed": int((~distribution_comparison["distribution_criterion_pass"]).sum()),
            "temporal_failed": int((~temporal_comparison["temporal_criterion_pass"]).sum()),
            "overall_assessments_passing": int(assessment["overall_prespecified_robustness_pass"].sum()),
        },
        "checks": {
            "input_hashes_match": True,
            "expected_populations_match": True,
            "keys_are_unique": True,
            "interval_panels_are_balanced": True,
            "support_threshold_populations_match_phase8a": True,
            "diagnostic_interval_is_retained": True,
            "absolute_cell_areas_are_compared_only_after_support_normalization": True,
            "aggregate_totals_use_complete_positive_support": True,
            "distribution_weights_are_positive": True,
            "conditional_metric_support_is_explicit": True,
            "primary_and_full_windows_are_separate": True,
            "robustness_failures_are_reported_as_results_not_runtime_errors": True,
        },
    }
    validation_path.write_text(
        json.dumps(validation, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    output_paths.append(validation_path)

    inventory_path = OUTPUT_DIR / "canonical_maup_comparison_inventory_v1.csv"
    output_inventory(output_paths).to_csv(
        inventory_path, index=False, encoding="utf-8-sig"
    )

    print("PHASE 8C COMPARISON COMPLETE — VALIDATION PASS")
    print("Aggregate comparisons:", f"{len(aggregate_comparison):,}")
    print("Distribution comparisons:", f"{len(distribution_comparison):,}")
    print("Temporal comparisons:", f"{len(temporal_comparison):,}")
    print("Robustness assessments:", f"{len(assessment):,}")
    for row in assessment.itertuples(index=False):
        print("ASSESSMENT |", row.comparison_grid, "|", row.window, "|", row.assessment)
    print("Validation:", validation_path)
    print("Inventory:", inventory_path)


if __name__ == "__main__":
    main()


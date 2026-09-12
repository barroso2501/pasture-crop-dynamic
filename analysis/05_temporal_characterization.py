"""
Temporal characterization of the canonical integrated stock-flow/trajectory panel.

Designed for Google Colab. It reads the canonical integrated Parquet panel,
creates auditable interval-level tables, and exports publication-ready figures
as PNG (300 dpi) and SVG.

This script is descriptive. It does not define data-driven historical phases
and does not perform trend or change-point inference.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter

try:
    from google.colab import drive
except ImportError:  # Allows reproducibility tests outside Colab.
    drive = None


# -----------------------------------------------------------------------------
# 1. Canonical configuration
# -----------------------------------------------------------------------------

PROJECT_DIR = Path(
    os.environ.get(
        "CANONICAL_TEMPORAL_PROJECT_DIR",
        "/content/drive/MyDrive/Trabalho/Contabilidade",
    )
)
ANALYSIS_DIR = PROJECT_DIR / "analysis"
INPUT_FILE = ANALYSIS_DIR / "canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet"

OUTPUT_DIR = ANALYSIS_DIR / "temporal"
FIGURE_DIR = PROJECT_DIR / "figures" / "temporal"

OUTPUT_VERSION = "canonical_integrated_temporal_characterization_v1"
EXPECTED_INPUT_SHA256 = os.environ.get(
    "CANONICAL_TEMPORAL_EXPECTED_SHA256",
    "7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28",
)
EXPECTED_ROWS = 199_112
EXPECTED_COLUMNS = 150
EXPECTED_CELLS = 24_889

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

PRIMARY_INTERVALS = INTERVALS[:-1]
DIAGNOSTIC_INTERVAL = INTERVALS[-1]

SUMMARY_FILE = OUTPUT_DIR / "canonical_integrated_temporal_summary_v1.csv"
ACTIVITY_FILE = OUTPUT_DIR / "canonical_integrated_temporal_activity_classes_v1.csv"
BALANCE_FILE = OUTPUT_DIR / "canonical_integrated_temporal_balance_distribution_v1.csv"
VALIDATION_FILE = OUTPUT_DIR / "canonical_integrated_temporal_validation_v1.json"

FIGURE_STEMS = [
    "fig01_core_flows_by_interval_v1",
    "fig02_nat_tmp_pathway_composition_v1",
    "fig03_nat_tmp_rule_sensitivity_v1",
    "fig04_cr_activity_classes_v1",
    "fig05_balance_distribution_both_processes_v1",
]

AREA_COLUMNS = [
    "consolidation_ha",
    "replenishment_ha",
    "gross_cr_activity_ha",
    "net_cr_balance_ha",
    "nat_tmp_endpoint_ha",
    "nat_tmp_mid_all_observed_ha",
    "nat_tmp_mid_incomplete_ha",
    "nat_tmp_pas_years_0_ha",
    "nat_tmp_pas_years_1_ha",
    "nat_tmp_pas_years_2_ha",
    "nat_tmp_pas_years_3_ha",
    "nat_tmp_pas_years_4_ha",
    "nat_tmp_pas_any_ha",
    "nat_tmp_pas_2plus_ha",
    "nat_tmp_pas_consecutive2_ha",
    "nat_tmp_pas_any_nonconsecutive2_ha",
]

NONNEGATIVE_AREA_COLUMNS = [column for column in AREA_COLUMNS if column != "net_cr_balance_ha"]

REQUIRED_COLUMNS = {
    "cell_id",
    "t0",
    "t1",
    "interval",
    "diagnostic_interval",
    "primary_inference_interval",
    "cr_balance_index",
    "has_both_cr_processes",
    "cr_activity_class",
    *AREA_COLUMNS,
}

ACTIVITY_CLASS_ORDER = [
    "none",
    "consolidation_only",
    "replenishment_only",
    "both",
]

ACTIVITY_CLASS_LABELS = {
    "none": "No C-R activity",
    "consolidation_only": "Consolidation only",
    "replenishment_only": "Replenishment only",
    "both": "Both processes",
}

COLORS = {
    "consolidation": "#D55E00",
    "replenishment": "#0072B2",
    "nat_tmp": "#009E73",
    "none": "#D9D9D9",
    "consolidation_only": "#E69F00",
    "replenishment_only": "#56B4E9",
    "both": "#6A3D9A",
}


# -----------------------------------------------------------------------------
# 2. Helpers
# -----------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def interval_label(t0: int, t1: int) -> str:
    return f"{int(t0)}\u2013{int(t1)}"


def safe_divide(numerator, denominator):
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    return np.divide(
        numerator,
        denominator,
        out=np.full_like(numerator, np.nan, dtype=float),
        where=denominator != 0,
    )


def assert_close(value: float, expected: float, tolerance: float, message: str) -> None:
    if not np.isfinite(value) or abs(value - expected) > tolerance:
        raise AssertionError(
            f"{message}: value={value:.12g}, expected={expected:.12g}, "
            f"tolerance={tolerance:.3g}"
        )


def add_diagnostic_background(ax) -> None:
    ax.axvspan(6.5, 7.5, color="#ECEFF1", zorder=0)
    ax.axvline(6.5, color="#6B7280", linewidth=0.8, linestyle="--", zorder=1)


def style_axis(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#D1D5DB", linewidth=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def save_figure(fig, stem: str) -> list[Path]:
    png = FIGURE_DIR / f"{stem}.png"
    svg = FIGURE_DIR / f"{stem}.svg"
    fig.savefig(png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return [png, svg]


# -----------------------------------------------------------------------------
# 3. Load and validate the canonical panel
# -----------------------------------------------------------------------------

if drive is not None:
    drive.mount("/content/drive")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(f"Canonical integrated panel not found: {INPUT_FILE}")

input_sha256 = sha256_file(INPUT_FILE)
if input_sha256 != EXPECTED_INPUT_SHA256:
    raise AssertionError(
        "Input SHA-256 does not match the canonical integrated panel. "
        f"Expected {EXPECTED_INPUT_SHA256}, found {input_sha256}."
    )

panel = pd.read_parquet(INPUT_FILE)
source_shape = panel.shape

if panel.shape != (EXPECTED_ROWS, EXPECTED_COLUMNS):
    raise AssertionError(
        f"Unexpected panel shape: {panel.shape}; "
        f"expected ({EXPECTED_ROWS}, {EXPECTED_COLUMNS})."
    )

missing_columns = sorted(REQUIRED_COLUMNS.difference(panel.columns))
if missing_columns:
    raise AssertionError(f"Required columns are missing: {missing_columns}")

if panel[["cell_id", "t0", "t1"]].duplicated().any():
    raise AssertionError("Duplicate cell_id-t0-t1 keys found in the integrated panel.")

if panel["cell_id"].nunique() != EXPECTED_CELLS:
    raise AssertionError(
        f"Unexpected distinct cell count: {panel['cell_id'].nunique()}; "
        f"expected {EXPECTED_CELLS}."
    )

observed_intervals = list(
    panel[["t0", "t1"]]
    .drop_duplicates()
    .sort_values(["t0", "t1"])
    .itertuples(index=False, name=None)
)
if observed_intervals != INTERVALS:
    raise AssertionError(f"Unexpected interval sequence: {observed_intervals}")

interval_counts = panel.groupby(["t0", "t1"], observed=True).size()
if not (interval_counts == EXPECTED_CELLS).all():
    raise AssertionError(f"Incomplete interval-cell panel detected:\n{interval_counts}")

expected_primary = panel["t1"].lt(2025).astype(int)
expected_diagnostic = panel["t1"].eq(2025).astype(int)
if not np.array_equal(panel["primary_inference_interval"].astype(int), expected_primary):
    raise AssertionError("primary_inference_interval is inconsistent with the canonical rule.")
if not np.array_equal(panel["diagnostic_interval"].astype(int), expected_diagnostic):
    raise AssertionError("diagnostic_interval is inconsistent with the canonical rule.")

if panel[AREA_COLUMNS].isna().any().any():
    raise AssertionError("Missing values found in required area columns.")
if (panel[NONNEGATIVE_AREA_COLUMNS] < -1e-9).any().any():
    raise AssertionError("Negative values found in non-negative area columns.")

panel = panel.copy()
panel["interval_order"] = panel["t0"].map({t0: i + 1 for i, (t0, _) in enumerate(INTERVALS)})
panel["interval_label"] = [interval_label(t0, t1) for t0, t1 in zip(panel["t0"], panel["t1"])]
panel["temporal_scope"] = np.where(
    panel["diagnostic_interval"].astype(int).eq(1),
    "diagnostic_extension",
    "primary_inference",
)


# -----------------------------------------------------------------------------
# 4. Interval-level temporal summary
# -----------------------------------------------------------------------------

group_keys = ["interval_order", "t0", "t1", "interval_label", "temporal_scope"]
summary = (
    panel.groupby(group_keys, as_index=False, sort=True, observed=True)[AREA_COLUMNS]
    .sum()
    .sort_values("interval_order")
    .reset_index(drop=True)
)

summary["cell_count"] = EXPECTED_CELLS
summary["consolidation_mha"] = summary["consolidation_ha"] / 1_000_000
summary["replenishment_mha"] = summary["replenishment_ha"] / 1_000_000
summary["gross_cr_activity_mha"] = summary["gross_cr_activity_ha"] / 1_000_000
summary["net_cr_balance_mha"] = summary["net_cr_balance_ha"] / 1_000_000
summary["nat_tmp_endpoint_mha"] = summary["nat_tmp_endpoint_ha"] / 1_000_000

summary["aggregate_cr_balance_index"] = safe_divide(
    summary["net_cr_balance_ha"], summary["gross_cr_activity_ha"]
)
summary["nat_tmp_pas_any_share_endpoint"] = safe_divide(
    summary["nat_tmp_pas_any_ha"], summary["nat_tmp_endpoint_ha"]
)
summary["nat_tmp_pas_2plus_share_endpoint"] = safe_divide(
    summary["nat_tmp_pas_2plus_ha"], summary["nat_tmp_endpoint_ha"]
)
summary["nat_tmp_pas_consecutive2_share_endpoint"] = safe_divide(
    summary["nat_tmp_pas_consecutive2_ha"], summary["nat_tmp_endpoint_ha"]
)
summary["nat_tmp_mid_incomplete_share_endpoint"] = safe_divide(
    summary["nat_tmp_mid_incomplete_ha"], summary["nat_tmp_endpoint_ha"]
)

complete_support = summary["nat_tmp_mid_all_observed_ha"]
for pasture_years in range(5):
    summary[f"nat_tmp_pas_years_{pasture_years}_share_complete"] = safe_divide(
        summary[f"nat_tmp_pas_years_{pasture_years}_ha"], complete_support
    )

summary["output_version"] = OUTPUT_VERSION


# -----------------------------------------------------------------------------
# 5. Activity-class composition and balance-index distribution
# -----------------------------------------------------------------------------

unexpected_classes = sorted(
    set(panel["cr_activity_class"].dropna().astype(str)).difference(ACTIVITY_CLASS_ORDER)
)
if unexpected_classes:
    raise AssertionError(f"Unexpected cr_activity_class values: {unexpected_classes}")

activity = (
    panel.groupby(["interval_order", "cr_activity_class"], observed=True)
    .size()
    .rename("cell_count")
    .reset_index()
)

complete_activity_index = pd.MultiIndex.from_product(
    [
        summary["interval_order"].tolist(),
        ACTIVITY_CLASS_ORDER,
    ],
    names=["interval_order", "cr_activity_class"],
)

activity = (
    activity.set_index(["interval_order", "cr_activity_class"])
    .reindex(complete_activity_index, fill_value=0)
    .reset_index()
)
activity = activity.merge(
    summary[["interval_order", "t0", "t1", "interval_label", "temporal_scope"]],
    on="interval_order",
    how="left",
    validate="many_to_one",
)
activity["cell_share"] = activity["cell_count"] / EXPECTED_CELLS
activity["class_label"] = activity["cr_activity_class"].map(ACTIVITY_CLASS_LABELS)
activity["output_version"] = OUTPUT_VERSION
activity = activity[
    [
        "interval_order",
        "t0",
        "t1",
        "interval_label",
        "temporal_scope",
        "cr_activity_class",
        "class_label",
        "cell_count",
        "cell_share",
        "output_version",
    ]
].sort_values(
    ["interval_order", "cr_activity_class"],
    key=lambda series: series.map({c: i for i, c in enumerate(ACTIVITY_CLASS_ORDER)})
    if series.name == "cr_activity_class"
    else series,
)

both = panel.loc[
    panel["has_both_cr_processes"].astype(int).eq(1),
    ["interval_order", "t0", "t1", "interval_label", "temporal_scope", "cr_balance_index"],
].copy()

if both["cr_balance_index"].isna().any():
    raise AssertionError("Missing cr_balance_index among cells with both C-R processes.")
if not both["cr_balance_index"].between(-1 - 1e-12, 1 + 1e-12).all():
    raise AssertionError("cr_balance_index outside [-1, 1].")

balance = (
    both.groupby(
        ["interval_order", "t0", "t1", "interval_label", "temporal_scope"],
        observed=True,
    )["cr_balance_index"]
    .agg(
        cell_count="count",
        mean="mean",
        standard_deviation="std",
        minimum="min",
        maximum="max",
        q05=lambda x: x.quantile(0.05),
        q25=lambda x: x.quantile(0.25),
        median="median",
        q75=lambda x: x.quantile(0.75),
        q95=lambda x: x.quantile(0.95),
    )
    .reset_index()
    .sort_values("interval_order")
)
balance["output_version"] = OUTPUT_VERSION


# -----------------------------------------------------------------------------
# 6. Numerical validation and table export
# -----------------------------------------------------------------------------

for row in summary.itertuples(index=False):
    assert_close(
        row.gross_cr_activity_ha,
        row.consolidation_ha + row.replenishment_ha,
        1e-5,
        f"Gross C-R identity failed for {row.interval_label}",
    )
    assert_close(
        row.net_cr_balance_ha,
        row.consolidation_ha - row.replenishment_ha,
        1e-5,
        f"Net C-R identity failed for {row.interval_label}",
    )
    pasture_partition = sum(
        getattr(row, f"nat_tmp_pas_years_{pasture_years}_ha")
        for pasture_years in range(5)
    )
    assert_close(
        pasture_partition,
        row.nat_tmp_mid_all_observed_ha,
        1e-5,
        f"NAT-TMP pasture-year partition failed for {row.interval_label}",
    )
    assert_close(
        row.nat_tmp_mid_all_observed_ha + row.nat_tmp_mid_incomplete_ha,
        row.nat_tmp_endpoint_ha,
        1e-5,
        f"NAT-TMP observation-support partition failed for {row.interval_label}",
    )

activity_totals = activity.groupby("interval_order", observed=True)["cell_count"].sum()
if not (activity_totals == EXPECTED_CELLS).all():
    raise AssertionError(f"Activity classes do not exhaust the cell population:\n{activity_totals}")

composition_columns = [
    f"nat_tmp_pas_years_{pasture_years}_share_complete" for pasture_years in range(5)
]
if not np.allclose(summary[composition_columns].sum(axis=1), 1.0, atol=1e-10):
    raise AssertionError("Complete-support NAT-TMP composition shares do not sum to 1.")

summary.to_csv(SUMMARY_FILE, index=False, float_format="%.12g")
activity.to_csv(ACTIVITY_FILE, index=False, float_format="%.12g")
balance.to_csv(BALANCE_FILE, index=False, float_format="%.12g")


# -----------------------------------------------------------------------------
# 7. Reproducible figures
# -----------------------------------------------------------------------------

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "figure.dpi": 120,
    }
)

x = np.arange(len(summary))
labels = summary["interval_label"].tolist()

# Figure 1: core directed flows
fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
add_diagnostic_background(ax)
ax.plot(
    x,
    summary["consolidation_mha"],
    color=COLORS["consolidation"],
    marker="o",
    linewidth=2,
    label="Consolidation (pasture to temporary crops)",
)
ax.plot(
    x,
    summary["replenishment_mha"],
    color=COLORS["replenishment"],
    marker="s",
    linewidth=2,
    label="Replenishment (native vegetation to pasture)",
)
ax.plot(
    x,
    summary["nat_tmp_endpoint_mha"],
    color=COLORS["nat_tmp"],
    marker="^",
    linewidth=2,
    label="Native vegetation to temporary crops",
)
ax.set_xticks(x, labels, rotation=35, ha="right")
ax.set_ylabel("Area per five-year interval (Mha)")
ax.set_xlabel("Five-year interval")
ax.set_title("Core land-use flows across the canonical domain")
ax.legend(frameon=False, loc="upper right")
style_axis(ax)
save_figure(fig, FIGURE_STEMS[0])

# Figure 2: fully observed NAT-TMP pathway composition
fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
add_diagnostic_background(ax)
bottom = np.zeros(len(summary))
pathway_colors = ["#4D4D4D", "#E69F00", "#56B4E9", "#0072B2", "#6A3D9A"]
for pasture_years, color in zip(range(5), pathway_colors):
    values = summary[f"nat_tmp_pas_years_{pasture_years}_share_complete"].to_numpy()
    ax.bar(
        x,
        values,
        bottom=bottom,
        color=color,
        width=0.72,
        label=f"{pasture_years} intermediate pasture year" + ("" if pasture_years == 1 else "s"),
    )
    bottom += values
ax.set_xticks(x, labels, rotation=35, ha="right")
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_ylabel("Share of fully observed NAT-TMP endpoint area")
ax.set_xlabel("Five-year interval")
ax.set_title("Intermediate-pasture duration within native-to-crop trajectories")
ax.legend(frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left")
style_axis(ax)
save_figure(fig, FIGURE_STEMS[1])

# Figure 3: trajectory-rule sensitivity
fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
add_diagnostic_background(ax)
sensitivity_series = [
    ("nat_tmp_pas_any_share_endpoint", "Any pasture year", "#E69F00", "o", "-"),
    ("nat_tmp_pas_2plus_share_endpoint", "At least two pasture years", "#0072B2", "s", "--"),
    (
        "nat_tmp_pas_consecutive2_share_endpoint",
        "At least two consecutive pasture years",
        "#6A3D9A",
        "^",
        ":",
    ),
]
for column, label, color, marker, linestyle in sensitivity_series:
    ax.plot(
        x,
        summary[column],
        color=color,
        marker=marker,
        linestyle=linestyle,
        linewidth=2,
        label=label,
    )
ax.set_xticks(x, labels, rotation=35, ha="right")
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_ylabel("Share of NAT-TMP endpoint area")
ax.set_xlabel("Five-year interval")
ax.set_title("Sensitivity of the intermediate-pasture trajectory rule")
ax.legend(frameon=False, loc="upper right")
style_axis(ax)
save_figure(fig, FIGURE_STEMS[2])

# Figure 4: C-R activity-class composition
activity_wide = (
    activity.pivot(index="interval_order", columns="cr_activity_class", values="cell_share")
    .reindex(index=range(1, 9), columns=ACTIVITY_CLASS_ORDER)
    .fillna(0)
)
fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
add_diagnostic_background(ax)
bottom = np.zeros(len(activity_wide))
for class_name in ACTIVITY_CLASS_ORDER:
    values = activity_wide[class_name].to_numpy()
    ax.bar(
        x,
        values,
        bottom=bottom,
        width=0.72,
        color=COLORS[class_name],
        label=ACTIVITY_CLASS_LABELS[class_name],
    )
    bottom += values
ax.set_xticks(x, labels, rotation=35, ha="right")
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_ylabel("Share of canonical cells")
ax.set_xlabel("Five-year interval")
ax.set_title("Cell-level consolidation-replenishment activity classes")
ax.legend(frameon=False, bbox_to_anchor=(1.02, 1), loc="upper left")
style_axis(ax)
save_figure(fig, FIGURE_STEMS[3])

# Figure 5: cell-level balance distribution where both processes occur
box_values = [
    both.loc[both["interval_order"].eq(order), "cr_balance_index"].to_numpy()
    for order in range(1, 9)
]
fig, ax = plt.subplots(figsize=(9.2, 4.8), constrained_layout=True)
add_diagnostic_background(ax)
box = ax.boxplot(
    box_values,
    positions=x,
    widths=0.58,
    patch_artist=True,
    showfliers=False,
    medianprops={"color": "#111827", "linewidth": 1.4},
    whiskerprops={"color": "#4B5563"},
    capprops={"color": "#4B5563"},
)
for patch in box["boxes"]:
    patch.set_facecolor("#B8D8EB")
    patch.set_edgecolor("#0072B2")
ax.axhline(0, color="#111827", linewidth=0.8)
ax.set_xticks(x, labels, rotation=35, ha="right")
ax.set_ylim(-1.03, 1.03)
ax.set_ylabel("Cell-level C-R balance index")
ax.set_xlabel("Five-year interval")
ax.set_title("Balance distribution among cells with both C-R processes")
style_axis(ax)
save_figure(fig, FIGURE_STEMS[4])


# -----------------------------------------------------------------------------
# 8. Validation record
# -----------------------------------------------------------------------------

figure_paths = [
    FIGURE_DIR / f"{stem}.{extension}"
    for stem in FIGURE_STEMS
    for extension in ("png", "svg")
]
for figure_path in figure_paths:
    if not figure_path.exists() or figure_path.stat().st_size == 0:
        raise AssertionError(f"Figure was not created correctly: {figure_path}")

validation = {
    "validation_status": "PASS",
    "output_version": OUTPUT_VERSION,
    "analysis_type": "descriptive_temporal_characterization",
    "analysis_scope": "combined_cerrado_amazon_canonical_domain",
    "biome_stratification_included": False,
    "formal_temporal_inference_included": False,
    "data_driven_phase_definition_included": False,
    "temporal_categories": {
        "primary_inference": [interval_label(*interval) for interval in PRIMARY_INTERVALS],
        "diagnostic_extension": interval_label(*DIAGNOSTIC_INTERVAL),
    },
    "input": {
        "path": str(INPUT_FILE),
        "sha256": input_sha256,
        "rows": int(panel.shape[0]),
        "columns": int(source_shape[1]),
        "distinct_cells": int(panel["cell_id"].nunique()),
        "intervals": int(len(observed_intervals)),
    },
    "outputs": {
        "temporal_summary": {
            "path": str(SUMMARY_FILE),
            "sha256": sha256_file(SUMMARY_FILE),
            "rows": int(len(summary)),
        },
        "activity_classes": {
            "path": str(ACTIVITY_FILE),
            "sha256": sha256_file(ACTIVITY_FILE),
            "rows": int(len(activity)),
        },
        "balance_distribution": {
            "path": str(BALANCE_FILE),
            "sha256": sha256_file(BALANCE_FILE),
            "rows": int(len(balance)),
        },
        "figures": [
            {
                "path": str(path),
                "sha256": sha256_file(path),
                "bytes": int(path.stat().st_size),
            }
            for path in figure_paths
        ],
    },
    "checks": {
        "canonical_input_hash": True,
        "expected_panel_shape": True,
        "unique_cell_interval_key": True,
        "complete_cell_interval_panel": True,
        "primary_diagnostic_assignment": True,
        "nonnegative_area_metrics": True,
        "gross_cr_identity": True,
        "net_cr_identity": True,
        "nat_tmp_pasture_year_partition": True,
        "nat_tmp_observation_support_partition": True,
        "activity_classes_exhaust_cell_population": True,
        "complete_support_composition_sums_to_one": True,
        "balance_index_valid_for_both_processes": True,
        "all_figure_files_created": True,
    },
    "interpretive_guardrails": [
        "The 2020-2025 interval is a diagnostic extension and is not part of primary inference.",
        "Lines connect ordered interval summaries for visualization; they are not fitted temporal trends.",
        "No historical phases or change points are inferred in this script.",
        "Results represent the combined Cerrado-Amazon canonical domain; biome-specific estimates require a separate spatial biome assignment.",
        "The cell-level C-R balance distribution includes only cells where both consolidation and replenishment are positive.",
        "NAT-TMP composition is calculated among trajectories with all four intermediate years observed; incomplete support is reported separately in the summary table.",
    ],
}

with VALIDATION_FILE.open("w", encoding="utf-8") as stream:
    json.dump(validation, stream, ensure_ascii=False, indent=2)


# -----------------------------------------------------------------------------
# 9. Concise execution report
# -----------------------------------------------------------------------------

print("TEMPORAL CHARACTERIZATION COMPLETE")
print(f"Input: {INPUT_FILE}")
print(f"Input SHA-256: {input_sha256}")
print(f"Panel: {source_shape[0]:,} rows x {source_shape[1]:,} source columns")
print(f"Canonical cells: {panel['cell_id'].nunique():,}")
print(f"Intervals: {len(observed_intervals)} (7 primary + 1 diagnostic)")
print(f"Temporal summary: {SUMMARY_FILE}")
print(f"Activity classes: {ACTIVITY_FILE}")
print(f"Balance distribution: {BALANCE_FILE}")
print(f"Validation: {VALIDATION_FILE}")
print(f"Figures: {FIGURE_DIR} (5 PNG + 5 SVG)")
print("Validation status: PASS")
print("\nInterval summary:")
print(
    summary[
        [
            "interval_label",
            "temporal_scope",
            "consolidation_mha",
            "replenishment_mha",
            "nat_tmp_endpoint_mha",
            "aggregate_cr_balance_index",
            "nat_tmp_pas_any_share_endpoint",
            "nat_tmp_pas_consecutive2_share_endpoint",
        ]
    ].to_string(index=False)
)

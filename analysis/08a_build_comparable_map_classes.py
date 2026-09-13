"""
Build and validate the Phase 3A fixed comparable-map class limits.

Designed for Google Colab. The script reads the accepted Phase 2 spatial-
metrics panel, calculates pooled class limits from the seven primary
intervals (1985-2020), applies those same limits to all eight intervals for
diagnostic class-count validation, and exports compact records.

This stage does not create maps. The limits must be reviewed and accepted
before a separate Phase 3B mapping script is run. The 2020-2025 diagnostic
interval is classified with the frozen limits but never contributes to their
calculation.
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

PHASE2_DIR = PROJECT_DIR / "spatial" / "phase2"
OUTPUT_DIR = PROJECT_DIR / "spatial" / "phase3"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPATIAL_METRICS_INPUT = PHASE2_DIR / "canonical_spatial_metrics_panel_v1.parquet"
PHASE2_VALIDATION_INPUT = (
    PHASE2_DIR / "canonical_spatial_metrics_validation_v1.json"
)

CLASS_LIMITS_OUTPUT = OUTPUT_DIR / "canonical_comparable_map_class_limits_v1.csv"
DISTRIBUTIONS_OUTPUT = (
    OUTPUT_DIR / "canonical_comparable_map_distributions_v1.csv"
)
CLASS_COUNTS_OUTPUT = OUTPUT_DIR / "canonical_comparable_map_class_counts_v1.csv"
SHARE_DENOMINATOR_SENSITIVITY_OUTPUT = (
    OUTPUT_DIR / "canonical_share_denominator_sensitivity_v1.csv"
)
SHARE_DENOMINATOR_SENSITIVITY_POOLED_OUTPUT = (
    OUTPUT_DIR / "canonical_share_denominator_sensitivity_pooled_v1.csv"
)
VALIDATION_OUTPUT = OUTPUT_DIR / "canonical_map_classes_validation_v1.json"

EXPECTED_SPATIAL_METRICS_SHA256 = (
    "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c"
)
EXPECTED_PHASE2_VALIDATION_SHA256 = (
    "9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8"
)

EXPECTED_ROWS = 199_112
EXPECTED_COLUMNS = 211
EXPECTED_CELLS = 24_889
EXPECTED_INTERVALS = 8
EXPECTED_PRIMARY_INTERVALS = 7
EXPECTED_PRIMARY_ROWS = EXPECTED_CELLS * EXPECTED_PRIMARY_INTERVALS

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

KEY_COLUMNS = ["cell_id", "t0", "t1"]
OUTPUT_VERSION = "canonical-comparable-map-classes-v1"
QUANTILE_METHOD = "linear"
AREA_ZERO_TOLERANCE_HA = 1e-9
RATIO_ZERO_TOLERANCE = 1e-12
NUMERIC_TOLERANCE = 1e-12
SHARE_DENOMINATOR_THRESHOLDS_HA = {
    "primary": AREA_ZERO_TOLERANCE_HA,
    "0p1ha": 0.1,
    "1ha": 1.0,
    "5ha": 5.0,
    "10ha": 10.0,
    "20ha": 20.0,
    "50ha": 50.0,
}


# -----------------------------------------------------------------------------
# 2. Prespecified mapping metrics
# -----------------------------------------------------------------------------

# Positive metrics use the pooled positive median and pooled positive 90th
# percentile from the seven primary intervals. Undefined and zero observations
# remain separate classes.
POSITIVE_METRICS = [
    {
        "metric": "consolidation_ha",
        "metric_label": "Pasture-to-crop consolidation",
        "measure_type": "absolute_area_ha",
        "denominator": "none",
        "support_field": None,
        "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
    },
    {
        "metric": "consolidation_rate_initial_pasture",
        "metric_label": "Consolidation relative to initial pasture",
        "measure_type": "relative_intensity",
        "denominator": "stock0_pas",
        "support_field": "consolidation_rate_defined",
        "zero_tolerance": RATIO_ZERO_TOLERANCE,
    },
    {
        "metric": "replenishment_ha",
        "metric_label": "Native-to-pasture replenishment",
        "measure_type": "absolute_area_ha",
        "denominator": "none",
        "support_field": None,
        "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
    },
    {
        "metric": "replenishment_rate_initial_native",
        "metric_label": "Replenishment relative to initial native vegetation",
        "measure_type": "relative_intensity",
        "denominator": "stock0_nat",
        "support_field": "replenishment_rate_defined",
        "zero_tolerance": RATIO_ZERO_TOLERANCE,
    },
    {
        "metric": "nat_tmp_endpoint_ha",
        "metric_label": "Native-to-temporary-crop endpoint flow",
        "measure_type": "absolute_area_ha",
        "denominator": "none",
        "support_field": None,
        "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
    },
    {
        "metric": "nat_tmp_intensity_initial_native",
        "metric_label": "NAT-TMP relative to initial native vegetation",
        "measure_type": "relative_intensity",
        "denominator": "stock0_nat",
        "support_field": "nat_tmp_intensity_defined",
        "zero_tolerance": RATIO_ZERO_TOLERANCE,
    },
    {
        "metric": "nat_tmp_pas_any_ha",
        "metric_label": "NAT-TMP with any intermediate pasture",
        "measure_type": "trajectory_area_ha",
        "denominator": "none",
        "support_field": None,
        "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
    },
    {
        "metric": "nat_tmp_pas_any_share_endpoint",
        "metric_label": "Share of NAT-TMP with any intermediate pasture",
        "measure_type": "trajectory_share",
        "denominator": "nat_tmp_endpoint_ha",
        "support_field": "nat_tmp_endpoint_share_defined",
        "zero_tolerance": RATIO_ZERO_TOLERANCE,
    },
    {
        "metric": "nat_tmp_pas_consecutive2_ha",
        "metric_label": "NAT-TMP with consecutive-two-year pasture",
        "measure_type": "trajectory_area_ha",
        "denominator": "none",
        "support_field": None,
        "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
    },
    {
        "metric": "nat_tmp_pas_consecutive2_share_endpoint",
        "metric_label": "Share of NAT-TMP with consecutive-two-year pasture",
        "measure_type": "trajectory_share",
        "denominator": "nat_tmp_endpoint_ha",
        "support_field": "nat_tmp_endpoint_share_defined",
        "zero_tolerance": RATIO_ZERO_TOLERANCE,
    },
]

# Net C-R balance is signed. Its class magnitudes use symmetric breaks derived
# from the pooled absolute nonzero balance in the seven primary intervals.
SIGNED_METRIC = {
    "metric": "net_cr_balance_ha",
    "metric_label": "Net consolidation-replenishment balance",
    "measure_type": "signed_area_ha",
    "denominator": "none",
    "support_field": None,
    "zero_tolerance": AREA_ZERO_TOLERANCE_HA,
}

# The bounded balance index retains the Phase 2 substantive states and does not
# use data-derived quantiles.
BALANCE_METRIC = {
    "metric": "cr_balance_index",
    "metric_label": "Consolidation-replenishment balance index",
    "measure_type": "bounded_balance_index",
    "denominator": "gross_cr_activity_ha",
    "support_field": "cr_balance_defined",
    "zero_tolerance": RATIO_ZERO_TOLERANCE,
}

ALL_METRIC_NAMES = [item["metric"] for item in POSITIVE_METRICS] + [
    SIGNED_METRIC["metric"],
    BALANCE_METRIC["metric"],
]


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


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not-installed"


def python_scalar(value):
    if isinstance(value, np.generic):
        return value.item()
    return value


def normalize_identifier(value) -> str:
    if pd.isna(value):
        raise ValueError("Missing identifier encountered")
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return str(int(value))
    return str(value)


def support_mask(frame: pd.DataFrame, specification: dict) -> pd.Series:
    metric = specification["metric"]
    support_field = specification["support_field"]
    if support_field is None:
        return frame[metric].notna()
    return frame[support_field].eq(1)


def interval_label(t0: int, t1: int) -> str:
    return f"{int(t0)}_{int(t1)}"


def summarize_distribution(
    frame: pd.DataFrame,
    specification: dict,
    t0: int,
    t1: int,
) -> dict:
    metric = specification["metric"]
    tolerance = specification["zero_tolerance"]
    supported = support_mask(frame, specification)
    values = pd.to_numeric(frame.loc[supported, metric], errors="raise")
    nonzero = values.loc[values.abs() > tolerance]
    positive = values.loc[values > tolerance]
    negative = values.loc[values < -tolerance]

    quantiles = values.quantile(
        [0.10, 0.25, 0.50, 0.75, 0.90], interpolation=QUANTILE_METHOD
    ) if len(values) else pd.Series(index=[0.10, 0.25, 0.50, 0.75, 0.90], dtype=float)

    return {
        "metric": metric,
        "metric_label": specification["metric_label"],
        "measure_type": specification["measure_type"],
        "t0": int(t0),
        "t1": int(t1),
        "interval": interval_label(t0, t1),
        "diagnostic_interval": int((int(t0), int(t1)) == DIAGNOSTIC_INTERVAL),
        "cell_count": len(frame),
        "defined_count": int(supported.sum()),
        "undefined_count": int((~supported).sum()),
        "zero_count": int((values.abs() <= tolerance).sum()),
        "nonzero_count": len(nonzero),
        "positive_count": len(positive),
        "negative_count": len(negative),
        "minimum": float(values.min()) if len(values) else np.nan,
        "p10": float(quantiles.loc[0.10]) if len(values) else np.nan,
        "p25": float(quantiles.loc[0.25]) if len(values) else np.nan,
        "median": float(quantiles.loc[0.50]) if len(values) else np.nan,
        "p75": float(quantiles.loc[0.75]) if len(values) else np.nan,
        "p90": float(quantiles.loc[0.90]) if len(values) else np.nan,
        "maximum": float(values.max()) if len(values) else np.nan,
        "zero_tolerance": tolerance,
        "map_class_version": OUTPUT_VERSION,
    }


def classify_positive(
    values: pd.Series,
    supported: pd.Series,
    tolerance: float,
    median_positive: float,
    p90_positive: float,
) -> pd.Series:
    classes = pd.Series("undefined", index=values.index, dtype="object")
    classes.loc[supported & values.le(tolerance)] = "zero"
    classes.loc[
        supported & values.gt(tolerance) & values.le(median_positive)
    ] = "positive_low"
    classes.loc[
        supported & values.gt(median_positive) & values.le(p90_positive)
    ] = "positive_moderate"
    classes.loc[supported & values.gt(p90_positive)] = "positive_high"
    return classes


def classify_signed(
    values: pd.Series,
    tolerance: float,
    median_absolute_nonzero: float,
    p90_absolute_nonzero: float,
) -> pd.Series:
    classes = pd.Series("zero", index=values.index, dtype="object")
    classes.loc[values.lt(-p90_absolute_nonzero)] = "replenishment_high"
    classes.loc[
        values.ge(-p90_absolute_nonzero) & values.lt(-median_absolute_nonzero)
    ] = "replenishment_moderate"
    classes.loc[
        values.ge(-median_absolute_nonzero) & values.lt(-tolerance)
    ] = "replenishment_low"
    classes.loc[
        values.gt(tolerance) & values.le(median_absolute_nonzero)
    ] = "consolidation_low"
    classes.loc[
        values.gt(median_absolute_nonzero) & values.le(p90_absolute_nonzero)
    ] = "consolidation_moderate"
    classes.loc[values.gt(p90_absolute_nonzero)] = "consolidation_high"
    return classes


def count_classes(
    frame: pd.DataFrame,
    metric: str,
    classes: pd.Series,
    ordered_labels: list[str],
) -> list[dict]:
    counts = classes.value_counts(dropna=False).to_dict()
    t0 = int(frame["t0"].iloc[0])
    t1 = int(frame["t1"].iloc[0])
    rows = []
    for order, label in enumerate(ordered_labels):
        count = int(counts.get(label, 0))
        rows.append(
            {
                "metric": metric,
                "t0": t0,
                "t1": t1,
                "interval": interval_label(t0, t1),
                "diagnostic_interval": int((t0, t1) == DIAGNOSTIC_INTERVAL),
                "class_order": order,
                "class_label": label,
                "cell_count": count,
                "cell_fraction": count / EXPECTED_CELLS,
                "map_class_version": OUTPUT_VERSION,
            }
        )
    require(sum(row["cell_count"] for row in rows) == EXPECTED_CELLS,
            f"Class counts do not close for {metric}, {t0}-{t1}")
    return rows


# -----------------------------------------------------------------------------
# 4. Read and authenticate Phase 2
# -----------------------------------------------------------------------------

print("CANONICAL COMPARABLE MAP CLASSES - PHASE 3A VERSION 1")
print("Input directory:", PHASE2_DIR)
print("Output directory:", OUTPUT_DIR)

for path in [SPATIAL_METRICS_INPUT, PHASE2_VALIDATION_INPUT]:
    require(path.exists(), f"Missing required input: {path}")

input_hashes = {
    SPATIAL_METRICS_INPUT.name: sha256_file(SPATIAL_METRICS_INPUT),
    PHASE2_VALIDATION_INPUT.name: sha256_file(PHASE2_VALIDATION_INPUT),
}
require(
    input_hashes[SPATIAL_METRICS_INPUT.name] == EXPECTED_SPATIAL_METRICS_SHA256,
    "Phase 2 spatial-metrics panel hash mismatch",
)
require(
    input_hashes[PHASE2_VALIDATION_INPUT.name]
    == EXPECTED_PHASE2_VALIDATION_SHA256,
    "Phase 2 validation-record hash mismatch",
)

with PHASE2_VALIDATION_INPUT.open("r", encoding="utf-8") as source:
    phase2_validation = json.load(source)

require(phase2_validation.get("validation_status") == "PASS",
        "Phase 2 validation status is not PASS")
require(all(phase2_validation.get("checks", {}).values()),
        "At least one Phase 2 validation check is false")
require(
    phase2_validation["outputs"][SPATIAL_METRICS_INPUT.name]["sha256"]
    == EXPECTED_SPATIAL_METRICS_SHA256,
    "Phase 2 record does not identify the supplied spatial-metrics panel",
)

panel = pd.read_parquet(SPATIAL_METRICS_INPUT)
panel["cell_id"] = panel["cell_id"].map(normalize_identifier)


# -----------------------------------------------------------------------------
# 5. Structural and support validation
# -----------------------------------------------------------------------------

required_columns = {
    *KEY_COLUMNS,
    "interval",
    "diagnostic_interval",
    "primary_inference_interval",
    "cr_balance_state",
    *ALL_METRIC_NAMES,
    *{
        item["support_field"]
        for item in [*POSITIVE_METRICS, BALANCE_METRIC]
        if item["support_field"] is not None
    },
}
missing_columns = sorted(required_columns - set(panel.columns))
require(not missing_columns, f"Missing required columns: {missing_columns}")
require(len(panel) == EXPECTED_ROWS, "Unexpected panel row count")
require(len(panel.columns) == EXPECTED_COLUMNS, "Unexpected panel column count")
require(panel["cell_id"].nunique() == EXPECTED_CELLS,
        "Unexpected distinct cell count")
require(panel.duplicated(KEY_COLUMNS).sum() == 0, "Duplicate panel keys")
require(panel["interval"].nunique() == EXPECTED_INTERVALS,
        "Unexpected interval count")

observed_intervals = sorted(
    {(int(row.t0), int(row.t1)) for row in panel[["t0", "t1"]].drop_duplicates().itertuples()}
)
require(observed_intervals == INTERVALS, "Unexpected interval sequence")
require(panel.groupby(["t0", "t1"]).size().eq(EXPECTED_CELLS).all(),
        "At least one interval is not complete")

expected_diagnostic = (
    panel["t0"].eq(DIAGNOSTIC_INTERVAL[0])
    & panel["t1"].eq(DIAGNOSTIC_INTERVAL[1])
).astype("int8")
require(
    pd.to_numeric(panel["diagnostic_interval"], errors="raise")
    .astype("int8").eq(expected_diagnostic).all(),
    "Diagnostic interval flag mismatch",
)
require(
    pd.to_numeric(panel["primary_inference_interval"], errors="raise")
    .astype("int8").eq(1 - expected_diagnostic).all(),
    "Primary interval flag mismatch",
)

for specification in POSITIVE_METRICS:
    metric = specification["metric"]
    supported = support_mask(panel, specification)
    require(panel.loc[supported, metric].notna().all(),
            f"Defined {metric} contains missing values")
    require(panel.loc[~supported, metric].isna().all(),
            f"Undefined {metric} must be missing")
    values = pd.to_numeric(panel.loc[supported, metric], errors="raise")
    require((values >= -NUMERIC_TOLERANCE).all(), f"Negative values in {metric}")
    if specification["measure_type"] in {"relative_intensity", "trajectory_share"}:
        require((values <= 1 + NUMERIC_TOLERANCE).all(),
                f"Values above one in {metric}")

net_values = pd.to_numeric(panel[SIGNED_METRIC["metric"]], errors="raise")
require(net_values.notna().all(), "Net C-R balance must be defined for all rows")

balance_supported = support_mask(panel, BALANCE_METRIC)
balance_values = pd.to_numeric(
    panel.loc[balance_supported, BALANCE_METRIC["metric"]], errors="raise"
)
require(panel.loc[balance_supported, BALANCE_METRIC["metric"]].notna().all(),
        "Defined C-R balance contains missing values")
require(panel.loc[~balance_supported, BALANCE_METRIC["metric"]].isna().all(),
        "Inactive C-R balance must be missing")
require(balance_values.between(-1 - NUMERIC_TOLERANCE,
                               1 + NUMERIC_TOLERANCE).all(),
        "C-R balance index outside [-1, 1]")

primary = panel.loc[panel["primary_inference_interval"].eq(1)].copy()
diagnostic = panel.loc[panel["diagnostic_interval"].eq(1)].copy()
require(len(primary) == EXPECTED_PRIMARY_ROWS, "Unexpected primary-period rows")
require(len(diagnostic) == EXPECTED_CELLS, "Unexpected diagnostic-period rows")


# -----------------------------------------------------------------------------
# 6. Pooled limits from seven primary intervals only
# -----------------------------------------------------------------------------

limit_rows = []
limit_lookup = {}

for specification in POSITIVE_METRICS:
    metric = specification["metric"]
    tolerance = specification["zero_tolerance"]
    supported = support_mask(primary, specification)
    source_values = pd.to_numeric(primary.loc[supported, metric], errors="raise")
    positive_values = source_values.loc[source_values > tolerance]
    require(len(positive_values) > 0, f"No positive primary values for {metric}")

    median_positive = float(
        positive_values.quantile(0.50, interpolation=QUANTILE_METHOD)
    )
    p90_positive = float(
        positive_values.quantile(0.90, interpolation=QUANTILE_METHOD)
    )
    require(median_positive > tolerance, f"Invalid positive median for {metric}")
    require(p90_positive >= median_positive, f"Invalid p90 for {metric}")

    labels = ["undefined", "zero", "positive_low", "positive_moderate", "positive_high"]
    limit_lookup[metric] = {
        "break_1": median_positive,
        "break_2": p90_positive,
        "zero_tolerance": tolerance,
        "labels": labels,
    }
    limit_rows.append(
        {
            "metric": metric,
            "metric_label": specification["metric_label"],
            "measure_type": specification["measure_type"],
            "denominator": specification["denominator"],
            "support_field": specification["support_field"] or "all_rows",
            "classification_method": "pooled_positive_median_and_p90",
            "threshold_source": "seven_primary_intervals_1985_2020",
            "diagnostic_used_to_fit_limits": 0,
            "source_defined_count": len(source_values),
            "source_undefined_count": len(primary) - len(source_values),
            "source_zero_count": int((source_values <= tolerance).sum()),
            "source_nonzero_count": len(positive_values),
            "break_1": median_positive,
            "break_1_definition": "pooled_positive_median",
            "break_2": p90_positive,
            "break_2_definition": "pooled_positive_p90",
            "zero_tolerance": tolerance,
            "quantile_method": QUANTILE_METHOD,
            "class_labels": json.dumps(labels),
            "map_class_version": OUTPUT_VERSION,
        }
    )

signed_metric = SIGNED_METRIC["metric"]
signed_tolerance = SIGNED_METRIC["zero_tolerance"]
signed_source = pd.to_numeric(primary[signed_metric], errors="raise")
absolute_nonzero = signed_source.abs().loc[signed_source.abs() > signed_tolerance]
require(len(absolute_nonzero) > 0, "No nonzero primary net C-R balances")
signed_median = float(
    absolute_nonzero.quantile(0.50, interpolation=QUANTILE_METHOD)
)
signed_p90 = float(
    absolute_nonzero.quantile(0.90, interpolation=QUANTILE_METHOD)
)
require(signed_median > signed_tolerance, "Invalid signed-balance median")
require(signed_p90 >= signed_median, "Invalid signed-balance p90")
signed_labels = [
    "replenishment_high",
    "replenishment_moderate",
    "replenishment_low",
    "zero",
    "consolidation_low",
    "consolidation_moderate",
    "consolidation_high",
]
limit_lookup[signed_metric] = {
    "break_1": signed_median,
    "break_2": signed_p90,
    "zero_tolerance": signed_tolerance,
    "labels": signed_labels,
}
limit_rows.append(
    {
        "metric": signed_metric,
        "metric_label": SIGNED_METRIC["metric_label"],
        "measure_type": SIGNED_METRIC["measure_type"],
        "denominator": SIGNED_METRIC["denominator"],
        "support_field": "all_rows",
        "classification_method": "symmetric_pooled_absolute_nonzero_median_and_p90",
        "threshold_source": "seven_primary_intervals_1985_2020",
        "diagnostic_used_to_fit_limits": 0,
        "source_defined_count": len(signed_source),
        "source_undefined_count": 0,
        "source_zero_count": int((signed_source.abs() <= signed_tolerance).sum()),
        "source_nonzero_count": len(absolute_nonzero),
        "break_1": signed_median,
        "break_1_definition": "pooled_absolute_nonzero_median",
        "break_2": signed_p90,
        "break_2_definition": "pooled_absolute_nonzero_p90",
        "zero_tolerance": signed_tolerance,
        "quantile_method": QUANTILE_METHOD,
        "class_labels": json.dumps(signed_labels),
        "map_class_version": OUTPUT_VERSION,
    }
)

balance_labels = [
    "inactive",
    "replenishment_dominant",
    "mixed",
    "consolidation_dominant",
]
balance_primary_supported = balance_supported.loc[primary.index]
balance_primary_values = pd.to_numeric(
    primary.loc[balance_primary_supported, BALANCE_METRIC["metric"]],
    errors="raise",
)
balance_primary_zero_count = int(
    (balance_primary_values.abs() <= BALANCE_METRIC["zero_tolerance"]).sum()
)
limit_lookup[BALANCE_METRIC["metric"]] = {
    "break_1": -1.0 / 3.0,
    "break_2": 1.0 / 3.0,
    "zero_tolerance": BALANCE_METRIC["zero_tolerance"],
    "labels": balance_labels,
}
limit_rows.append(
    {
        "metric": BALANCE_METRIC["metric"],
        "metric_label": BALANCE_METRIC["metric_label"],
        "measure_type": BALANCE_METRIC["measure_type"],
        "denominator": BALANCE_METRIC["denominator"],
        "support_field": BALANCE_METRIC["support_field"],
        "classification_method": "fixed_substantive_balance_states",
        "threshold_source": "phase2_prespecified_fixed_thresholds",
        "diagnostic_used_to_fit_limits": 0,
        "source_defined_count": int(balance_primary_supported.sum()),
        "source_undefined_count": int((~balance_primary_supported).sum()),
        "source_zero_count": balance_primary_zero_count,
        "source_nonzero_count": len(balance_primary_values) - balance_primary_zero_count,
        "break_1": -1.0 / 3.0,
        "break_1_definition": "replenishment_to_mixed_boundary",
        "break_2": 1.0 / 3.0,
        "break_2_definition": "mixed_to_consolidation_boundary",
        "zero_tolerance": BALANCE_METRIC["zero_tolerance"],
        "quantile_method": "not_applicable_fixed",
        "class_labels": json.dumps(balance_labels),
        "map_class_version": OUTPUT_VERSION,
    }
)

class_limits = pd.DataFrame(limit_rows)
require(len(class_limits) == len(ALL_METRIC_NAMES),
        "Unexpected class-limit row count")
require(class_limits["metric"].is_unique, "Duplicate metric in class limits")
require(class_limits["diagnostic_used_to_fit_limits"].eq(0).all(),
        "Diagnostic interval entered threshold fitting")
require(
    (class_limits["source_defined_count"]
     + class_limits["source_undefined_count"]).eq(EXPECTED_PRIMARY_ROWS).all(),
    "Defined and undefined source counts do not close",
)
require(
    (class_limits["source_zero_count"]
     + class_limits["source_nonzero_count"])
    .eq(class_limits["source_defined_count"]).all(),
    "Zero and nonzero source counts do not close",
)


# -----------------------------------------------------------------------------
# 7. Interval distributions and frozen-limit class counts
# -----------------------------------------------------------------------------

distribution_rows = []
class_count_rows = []
specifications = [*POSITIVE_METRICS, SIGNED_METRIC, BALANCE_METRIC]

for (t0, t1), interval_frame in panel.groupby(["t0", "t1"], sort=True):
    interval_frame = interval_frame.copy()
    for specification in specifications:
        metric = specification["metric"]
        distribution_rows.append(
            summarize_distribution(interval_frame, specification, int(t0), int(t1))
        )

        values = pd.to_numeric(interval_frame[metric], errors="coerce")
        limits = limit_lookup[metric]
        if metric in {item["metric"] for item in POSITIVE_METRICS}:
            supported = support_mask(interval_frame, specification)
            classes = classify_positive(
                values,
                supported,
                limits["zero_tolerance"],
                limits["break_1"],
                limits["break_2"],
            )
        elif metric == SIGNED_METRIC["metric"]:
            classes = classify_signed(
                values,
                limits["zero_tolerance"],
                limits["break_1"],
                limits["break_2"],
            )
        else:
            classes = interval_frame["cr_balance_state"].astype(str)
            require(set(classes.unique()).issubset(set(balance_labels)),
                    "Unexpected C-R balance state")

        class_count_rows.extend(
            count_classes(interval_frame, metric, classes, limits["labels"])
        )

distributions = pd.DataFrame(distribution_rows).sort_values(
    ["metric", "t0", "t1"]
).reset_index(drop=True)
class_counts = pd.DataFrame(class_count_rows).sort_values(
    ["metric", "t0", "t1", "class_order"]
).reset_index(drop=True)

require(len(distributions) == len(ALL_METRIC_NAMES) * EXPECTED_INTERVALS,
        "Unexpected distribution-summary row count")
require(
    class_counts.groupby(["metric", "t0", "t1"])["cell_count"]
    .sum().eq(EXPECTED_CELLS).all(),
    "At least one map-class population does not close",
)
require(
    class_counts.loc[class_counts["diagnostic_interval"].eq(1), "interval"]
    .eq(interval_label(*DIAGNOSTIC_INTERVAL)).all(),
    "Diagnostic class-count labeling mismatch",
)


# -----------------------------------------------------------------------------
# 8. Trajectory-share denominator sensitivity
# -----------------------------------------------------------------------------

# Shares can become numerically extreme when their NAT-TMP endpoint denominator
# is very small. This table does not refit or replace the frozen limits. It
# reports how the same limits behave after requiring endpoint areas above the
# prespecified Phase 2 sensitivity thresholds.
share_sensitivity_rows = []
share_metric_names = {
    "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_consecutive2_share_endpoint",
}
share_numerator_fields = {
    "nat_tmp_pas_any_share_endpoint": "nat_tmp_pas_any_ha",
    "nat_tmp_pas_consecutive2_share_endpoint": "nat_tmp_pas_consecutive2_ha",
}

for (t0, t1), interval_frame in panel.groupby(["t0", "t1"], sort=True):
    for specification in POSITIVE_METRICS:
        metric = specification["metric"]
        if metric not in share_metric_names:
            continue

        limits = limit_lookup[metric]
        numerator_field = share_numerator_fields[metric]
        base_supported = support_mask(interval_frame, specification)
        base_count = int(base_supported.sum())
        base_endpoint_area = float(
            interval_frame.loc[base_supported, "nat_tmp_endpoint_ha"].sum()
        )
        base_trajectory_area = float(
            interval_frame.loc[base_supported, numerator_field].sum()
        )

        for threshold_label, threshold_ha in SHARE_DENOMINATOR_THRESHOLDS_HA.items():
            eligible = base_supported & interval_frame["nat_tmp_endpoint_ha"].gt(
                threshold_ha
            )
            values = pd.to_numeric(interval_frame.loc[eligible, metric], errors="raise")
            classes = classify_positive(
                pd.to_numeric(interval_frame[metric], errors="coerce"),
                eligible,
                limits["zero_tolerance"],
                limits["break_1"],
                limits["break_2"],
            )
            eligible_classes = classes.loc[eligible]
            class_counts_for_threshold = eligible_classes.value_counts().to_dict()
            positive_values = values.loc[values > limits["zero_tolerance"]]
            eligible_endpoint_area = float(
                interval_frame.loc[eligible, "nat_tmp_endpoint_ha"].sum()
            )
            eligible_trajectory_area = float(
                interval_frame.loc[eligible, numerator_field].sum()
            )
            excluded_endpoint_area = base_endpoint_area - eligible_endpoint_area
            excluded_trajectory_area = (
                base_trajectory_area - eligible_trajectory_area
            )

            share_sensitivity_rows.append(
                {
                    "metric": metric,
                    "t0": int(t0),
                    "t1": int(t1),
                    "interval": interval_label(t0, t1),
                    "diagnostic_interval": int(
                        (int(t0), int(t1)) == DIAGNOSTIC_INTERVAL
                    ),
                    "endpoint_threshold_label": threshold_label,
                    "endpoint_threshold_ha": threshold_ha,
                    "base_defined_count": base_count,
                    "eligible_count": int(eligible.sum()),
                    "excluded_small_denominator_count": base_count - int(eligible.sum()),
                    "base_endpoint_area_ha": base_endpoint_area,
                    "eligible_endpoint_area_ha": eligible_endpoint_area,
                    "excluded_endpoint_area_ha": excluded_endpoint_area,
                    "excluded_endpoint_area_fraction": (
                        excluded_endpoint_area / base_endpoint_area
                        if base_endpoint_area > AREA_ZERO_TOLERANCE_HA
                        else np.nan
                    ),
                    "base_trajectory_area_ha": base_trajectory_area,
                    "eligible_trajectory_area_ha": eligible_trajectory_area,
                    "excluded_trajectory_area_ha": excluded_trajectory_area,
                    "aggregate_share_eligible": (
                        eligible_trajectory_area / eligible_endpoint_area
                        if eligible_endpoint_area > AREA_ZERO_TOLERANCE_HA
                        else np.nan
                    ),
                    "zero_share_count": int(
                        class_counts_for_threshold.get("zero", 0)
                    ),
                    "positive_low_count": int(
                        class_counts_for_threshold.get("positive_low", 0)
                    ),
                    "positive_moderate_count": int(
                        class_counts_for_threshold.get("positive_moderate", 0)
                    ),
                    "positive_high_count": int(
                        class_counts_for_threshold.get("positive_high", 0)
                    ),
                    "positive_share_median": (
                        float(
                            positive_values.quantile(
                                0.50, interpolation=QUANTILE_METHOD
                            )
                        )
                        if len(positive_values)
                        else np.nan
                    ),
                    "positive_share_p90": (
                        float(
                            positive_values.quantile(
                                0.90, interpolation=QUANTILE_METHOD
                            )
                        )
                        if len(positive_values)
                        else np.nan
                    ),
                    "frozen_break_1": limits["break_1"],
                    "frozen_break_2": limits["break_2"],
                    "map_class_version": OUTPUT_VERSION,
                }
            )

share_sensitivity = pd.DataFrame(share_sensitivity_rows).sort_values(
    ["metric", "t0", "t1", "endpoint_threshold_ha"]
).reset_index(drop=True)
require(
    len(share_sensitivity)
    == len(share_metric_names) * EXPECTED_INTERVALS
    * len(SHARE_DENOMINATOR_THRESHOLDS_HA),
    "Unexpected trajectory-share denominator-sensitivity row count",
)
require(
    (
        share_sensitivity["zero_share_count"]
        + share_sensitivity["positive_low_count"]
        + share_sensitivity["positive_moderate_count"]
        + share_sensitivity["positive_high_count"]
    ).eq(share_sensitivity["eligible_count"]).all(),
    "Trajectory-share sensitivity classes do not close",
)
require(
    share_sensitivity.groupby(["metric", "t0", "t1"])["eligible_count"]
    .apply(lambda values: values.is_monotonic_decreasing)
    .all(),
    "Eligible denominator populations are not nested",
)
require(
    share_sensitivity.groupby(["metric", "t0", "t1"])["eligible_endpoint_area_ha"]
    .apply(lambda values: values.is_monotonic_decreasing)
    .all(),
    "Eligible endpoint areas are not nested",
)
require(
    np.allclose(
        share_sensitivity["eligible_endpoint_area_ha"]
        + share_sensitivity["excluded_endpoint_area_ha"],
        share_sensitivity["base_endpoint_area_ha"],
        rtol=0,
        atol=2e-6,
    ),
    "Endpoint-area sensitivity accounting does not close",
)
require(
    np.allclose(
        share_sensitivity["eligible_trajectory_area_ha"]
        + share_sensitivity["excluded_trajectory_area_ha"],
        share_sensitivity["base_trajectory_area_ha"],
        rtol=0,
        atol=2e-6,
    ),
    "Trajectory-area sensitivity accounting does not close",
)


# Pooled seven-primary-interval sensitivity is calculated directly from the
# underlying observations so that medians and percentiles are not approximated
# from interval summaries.
pooled_share_sensitivity_rows = []
for specification in POSITIVE_METRICS:
    metric = specification["metric"]
    if metric not in share_metric_names:
        continue

    limits = limit_lookup[metric]
    numerator_field = share_numerator_fields[metric]
    base_supported = support_mask(primary, specification)
    base_count = int(base_supported.sum())
    base_endpoint_area = float(
        primary.loc[base_supported, "nat_tmp_endpoint_ha"].sum()
    )
    base_trajectory_area = float(
        primary.loc[base_supported, numerator_field].sum()
    )

    for threshold_label, threshold_ha in SHARE_DENOMINATOR_THRESHOLDS_HA.items():
        eligible = base_supported & primary["nat_tmp_endpoint_ha"].gt(threshold_ha)
        values = pd.to_numeric(primary.loc[eligible, metric], errors="raise")
        positive_values = values.loc[values > limits["zero_tolerance"]]
        classes = classify_positive(
            pd.to_numeric(primary[metric], errors="coerce"),
            eligible,
            limits["zero_tolerance"],
            limits["break_1"],
            limits["break_2"],
        ).loc[eligible]
        counts_for_threshold = classes.value_counts().to_dict()
        eligible_endpoint_area = float(
            primary.loc[eligible, "nat_tmp_endpoint_ha"].sum()
        )
        eligible_trajectory_area = float(
            primary.loc[eligible, numerator_field].sum()
        )
        excluded_endpoint_area = base_endpoint_area - eligible_endpoint_area
        excluded_trajectory_area = base_trajectory_area - eligible_trajectory_area

        pooled_share_sensitivity_rows.append(
            {
                "metric": metric,
                "scope": "pooled_primary_1985_2020",
                "endpoint_threshold_label": threshold_label,
                "endpoint_threshold_ha": threshold_ha,
                "base_defined_count": base_count,
                "eligible_count": int(eligible.sum()),
                "eligible_cell_fraction": int(eligible.sum()) / base_count,
                "excluded_small_denominator_count": base_count - int(eligible.sum()),
                "excluded_cell_fraction": (
                    base_count - int(eligible.sum())
                ) / base_count,
                "base_endpoint_area_ha": base_endpoint_area,
                "eligible_endpoint_area_ha": eligible_endpoint_area,
                "excluded_endpoint_area_ha": excluded_endpoint_area,
                "excluded_endpoint_area_fraction": (
                    excluded_endpoint_area / base_endpoint_area
                    if base_endpoint_area > AREA_ZERO_TOLERANCE_HA
                    else np.nan
                ),
                "base_trajectory_area_ha": base_trajectory_area,
                "eligible_trajectory_area_ha": eligible_trajectory_area,
                "excluded_trajectory_area_ha": excluded_trajectory_area,
                "excluded_trajectory_area_fraction": (
                    excluded_trajectory_area / base_trajectory_area
                    if base_trajectory_area > AREA_ZERO_TOLERANCE_HA
                    else np.nan
                ),
                "aggregate_share_eligible": (
                    eligible_trajectory_area / eligible_endpoint_area
                    if eligible_endpoint_area > AREA_ZERO_TOLERANCE_HA
                    else np.nan
                ),
                "zero_share_count": int(counts_for_threshold.get("zero", 0)),
                "positive_low_count": int(
                    counts_for_threshold.get("positive_low", 0)
                ),
                "positive_moderate_count": int(
                    counts_for_threshold.get("positive_moderate", 0)
                ),
                "positive_high_count": int(
                    counts_for_threshold.get("positive_high", 0)
                ),
                "positive_share_median": (
                    float(
                        positive_values.quantile(
                            0.50, interpolation=QUANTILE_METHOD
                        )
                    )
                    if len(positive_values)
                    else np.nan
                ),
                "positive_share_p90": (
                    float(
                        positive_values.quantile(
                            0.90, interpolation=QUANTILE_METHOD
                        )
                    )
                    if len(positive_values)
                    else np.nan
                ),
                "frozen_break_1": limits["break_1"],
                "frozen_break_2": limits["break_2"],
                "map_class_version": OUTPUT_VERSION,
            }
        )

pooled_share_sensitivity = pd.DataFrame(pooled_share_sensitivity_rows).sort_values(
    ["metric", "endpoint_threshold_ha"]
).reset_index(drop=True)
require(
    len(pooled_share_sensitivity)
    == len(share_metric_names) * len(SHARE_DENOMINATOR_THRESHOLDS_HA),
    "Unexpected pooled share-sensitivity row count",
)
require(
    (
        pooled_share_sensitivity["zero_share_count"]
        + pooled_share_sensitivity["positive_low_count"]
        + pooled_share_sensitivity["positive_moderate_count"]
        + pooled_share_sensitivity["positive_high_count"]
    ).eq(pooled_share_sensitivity["eligible_count"]).all(),
    "Pooled share-sensitivity classes do not close",
)
require(
    pooled_share_sensitivity.groupby("metric")["eligible_count"]
    .apply(lambda values: values.is_monotonic_decreasing)
    .all(),
    "Pooled eligible populations are not nested",
)
require(
    pooled_share_sensitivity.groupby("metric")["eligible_endpoint_area_ha"]
    .apply(lambda values: values.is_monotonic_decreasing)
    .all(),
    "Pooled eligible endpoint areas are not nested",
)


# -----------------------------------------------------------------------------
# 9. Export compact records and validation
# -----------------------------------------------------------------------------

class_limits.to_csv(CLASS_LIMITS_OUTPUT, index=False, float_format="%.12g")
distributions.to_csv(DISTRIBUTIONS_OUTPUT, index=False, float_format="%.12g")
class_counts.to_csv(CLASS_COUNTS_OUTPUT, index=False, float_format="%.12g")
share_sensitivity.to_csv(
    SHARE_DENOMINATOR_SENSITIVITY_OUTPUT, index=False, float_format="%.12g"
)
pooled_share_sensitivity.to_csv(
    SHARE_DENOMINATOR_SENSITIVITY_POOLED_OUTPUT,
    index=False,
    float_format="%.12g",
)

output_paths = [
    CLASS_LIMITS_OUTPUT,
    DISTRIBUTIONS_OUTPUT,
    CLASS_COUNTS_OUTPUT,
    SHARE_DENOMINATOR_SENSITIVITY_OUTPUT,
    SHARE_DENOMINATOR_SENSITIVITY_POOLED_OUTPUT,
]
output_hashes = {path.name: sha256_file(path) for path in output_paths}

validation = {
    "validation_status": "PASS",
    "map_class_version": OUTPUT_VERSION,
    "scope": {
        "class_limit_source_intervals": [interval_label(*x) for x in PRIMARY_INTERVALS],
        "diagnostic_interval": interval_label(*DIAGNOSTIC_INTERVAL),
        "diagnostic_used_to_fit_limits": False,
        "maps_created": False,
        "next_gate": "review and accept fixed limits before Phase 3B mapping",
    },
    "configuration": {
        "positive_metric_rule": (
            "undefined; zero; positive low <= pooled positive median; "
            "positive moderate <= pooled positive p90; positive high > p90"
        ),
        "signed_net_balance_rule": (
            "symmetric classes using pooled absolute nonzero median and p90"
        ),
        "balance_index_rule": (
            "inactive; replenishment-dominant < -1/3; mixed [-1/3, 1/3]; "
            "consolidation-dominant > 1/3"
        ),
        "quantile_method": QUANTILE_METHOD,
        "area_zero_tolerance_ha": AREA_ZERO_TOLERANCE_HA,
        "ratio_zero_tolerance": RATIO_ZERO_TOLERANCE,
        "share_denominator_thresholds_ha": SHARE_DENOMINATOR_THRESHOLDS_HA,
        "metric_count": len(ALL_METRIC_NAMES),
        "metrics": ALL_METRIC_NAMES,
    },
    "inputs": {
        path.name: {"path": str(path), "sha256": input_hashes[path.name]}
        for path in [SPATIAL_METRICS_INPUT, PHASE2_VALIDATION_INPUT]
    },
    "structure": {
        "input_rows": len(panel),
        "input_columns": len(panel.columns),
        "distinct_cells": panel["cell_id"].nunique(),
        "intervals": panel["interval"].nunique(),
        "primary_rows_used_to_fit_limits": len(primary),
        "diagnostic_rows_excluded_from_limit_fitting": len(diagnostic),
        "class_limit_rows": len(class_limits),
        "distribution_rows": len(distributions),
        "class_count_rows": len(class_counts),
        "share_denominator_sensitivity_rows": len(share_sensitivity),
        "pooled_share_denominator_sensitivity_rows": len(
            pooled_share_sensitivity
        ),
    },
    "limits": class_limits.to_dict(orient="records"),
    "outputs": {
        path.name: {"path": str(path), "sha256": output_hashes[path.name]}
        for path in output_paths
    },
    "software": {
        "python": sys.version,
        "pandas": package_version("pandas"),
        "numpy": package_version("numpy"),
        "pyarrow": package_version("pyarrow"),
    },
    "checks": {
        "input_hashes_match": True,
        "phase2_validation_passed": True,
        "balanced_unique_panel": True,
        "primary_and_diagnostic_intervals_identified": True,
        "diagnostic_interval_excluded_from_limit_fitting": True,
        "metric_support_rules_pass": True,
        "metric_ranges_pass": True,
        "one_fixed_limit_record_per_metric": True,
        "limit_source_counts_reconcile": True,
        "positive_breaks_are_ordered": True,
        "signed_breaks_are_symmetric_and_ordered": True,
        "balance_state_limits_are_fixed": True,
        "class_populations_close_for_every_metric_interval": True,
        "share_denominator_sensitivity_populations_are_nested": True,
        "share_denominator_sensitivity_classes_close": True,
        "share_denominator_sensitivity_area_accounting_closes": True,
        "pooled_share_denominator_sensitivity_passes": True,
        "no_maps_created_before_limit_review": True,
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

print("\nPHASE 3A COMPARABLE MAP-CLASS BUILD COMPLETE")
print("Validation status: PASS")
print("Rows read:", f"{len(panel):,}")
print("Cells:", f"{panel['cell_id'].nunique():,}")
print("Intervals:", panel["interval"].nunique())
print("Primary rows used to fit limits:", f"{len(primary):,}")
print("Diagnostic rows excluded from fitting:", f"{len(diagnostic):,}")
print("Metrics with frozen limits:", len(class_limits))
print("\nFrozen limits:")
print(
    class_limits[
        [
            "metric",
            "classification_method",
            "source_defined_count",
            "source_undefined_count",
            "source_zero_count",
            "source_nonzero_count",
            "break_1",
            "break_2",
        ]
    ].to_string(index=False)
)
print("\nNO MAPS WERE CREATED.")
print("Review the limits before running Phase 3B.")
print("Class limits:", CLASS_LIMITS_OUTPUT)
print("Distribution summary:", DISTRIBUTIONS_OUTPUT)
print("Class counts:", CLASS_COUNTS_OUTPUT)
print("Share denominator sensitivity:", SHARE_DENOMINATOR_SENSITIVITY_OUTPUT)
print("\nPooled primary share-denominator sensitivity:")
print(
    pooled_share_sensitivity[
        [
            "metric",
            "endpoint_threshold_label",
            "eligible_count",
            "excluded_cell_fraction",
            "excluded_endpoint_area_fraction",
            "positive_share_median",
            "positive_share_p90",
            "aggregate_share_eligible",
        ]
    ].to_string(index=False)
)
print(
    "Pooled share denominator sensitivity:",
    SHARE_DENOMINATOR_SENSITIVITY_POOLED_OUTPUT,
)
print("Validation record:", VALIDATION_OUTPUT)

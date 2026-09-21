#!/usr/bin/env python3
"""Resolve Phase 9 evidence gaps for RQ1 and RQ2.

RQ1 is summarized from the fixed-1985-pasture-cohort GEE export produced by
gee/15b_export_fixed_1985_pasture_cohort_v1.js. RQ2 is extracted from the
already accepted canonical derived stock-flow summary. No interval flow,
class boundary, Moran statistic, or earlier analytical result is recomputed.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from google.colab import drive
except ImportError:  # pragma: no cover
    drive = None


VERSION = "phase9-rq1-rq2-gap-resolution-v1"
COHORT_EXPORT_VERSION = "phase9-fixed-1985-pasture-cohort-export-v1"
EVIDENCE_MATRIX_VERSION = "phase9a-gap-resolved-evidence-matrix-v2"

PROJECT_DIR = Path(os.environ.get(
    "PHASE9_PROJECT_DIR",
    "/content/drive/MyDrive/Trabalho/Contabilidade",
))
RAW_DIR = Path(os.environ.get(
    "PHASE9_COHORT_RAW_DIR",
    "/content/drive/MyDrive/pasture_crop_dynamic_canonical",
))
OUTPUT_RELATIVE = Path("spatial/phase9/gap_resolution_v1")

YEARS = [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]
PRIMARY_YEARS = YEARS[:-1]
STATES = [
    "nat", "pas", "tmp", "oag", "out",
    "water", "nodata", "unexpected", "masked",
]
ORIGIN_COMPONENTS = [
    "censored", "new", "unresolved_age", "unattributed_age",
]
EXPECTED_SPATIAL_SHA256 = (
    "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc"
)
EXPECTED_ORIGIN_SUMMARY_SHA256 = (
    "f104c4f6ec8b50fc7c276284af9386e25d32e01f80ec2c51dfaad17f4493405e"
)
EXPECTED_PILOT_CELLS = 3_168
EXPECTED_FULL_CELLS = 24_889
EXPECTED_TRANSBIOME_CELLS = 582
EXPECTED_PRIMARY_BIOME_COUNTS = {"Amazon": 14_213, "Cerrado": 10_676}
TOLERANCE_HA = 2e-6
ZERO_TOLERANCE_HA = 1e-9


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise ValueError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(json_ready(value), ensure_ascii=False, indent=2,
                   allow_nan=False) + "\n",
        encoding="utf-8",
    )


def raw_filename(mode: str) -> str:
    suffix = "b00" if mode == "pilot" else "full"
    return f"canonical_fixed_1985_pasture_cohort_states_{suffix}_v1.csv"


def state_column(year: int, state: str) -> str:
    return f"cohort_{year}_{state}_ha"


def expected_raw_columns() -> list[str]:
    columns = [
        "cell_id", "GRID_ID", "source_batch_id",
        "cohort_extraction_version", "cohort_definition", "run_mode",
        "cohort_total_ha",
    ]
    for year in YEARS:
        columns.extend(state_column(year, state) for state in STATES)
        columns.extend([
            f"cohort_{year}_state_total_ha",
            f"cohort_{year}_closure_residual_ha",
        ])
    return columns


def load_and_validate_raw(path: Path, mode: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    require(path.is_file(), f"Missing GEE cohort export: {path}")
    frame = pd.read_csv(
        path,
        dtype={"cell_id": str, "GRID_ID": str},
        float_precision="round_trip",
    )
    expected_cells = EXPECTED_PILOT_CELLS if mode == "pilot" else EXPECTED_FULL_CELLS
    missing = set(expected_raw_columns()) - set(frame.columns)
    require(not missing, f"Missing cohort-export columns: {sorted(missing)}")
    require(len(frame) == expected_cells,
            f"Unexpected {mode} row count: {len(frame)}")
    require(frame["cell_id"].notna().all() and frame["cell_id"].is_unique,
            "Invalid or duplicate cell_id")
    require(frame["GRID_ID"].notna().all() and frame["GRID_ID"].is_unique,
            "Invalid or duplicate GRID_ID")
    require(frame["cohort_extraction_version"].eq(COHORT_EXPORT_VERSION).all(),
            "Wrong cohort export version")
    require(frame["run_mode"].eq(mode).all(), "Wrong run_mode in raw export")
    if mode == "pilot":
        require(frame["source_batch_id"].astype(int).eq(0).all(),
                "Pilot contains a non-b00 cell")

    area_columns = ["cohort_total_ha"] + [
        state_column(year, state) for year in YEARS for state in STATES
    ]
    values = frame[area_columns].to_numpy(dtype="float64")
    require(np.isfinite(values).all(), "Non-finite cohort areas")
    require(float(values.min()) >= -ZERO_TOLERANCE_HA,
            "Negative cohort area")

    closure_max = 0.0
    state_total_difference_max = 0.0
    for year in YEARS:
        state_sum = frame[[state_column(year, s) for s in STATES]].sum(axis=1)
        exported_total = frame[f"cohort_{year}_state_total_ha"]
        exported_residual = frame[f"cohort_{year}_closure_residual_ha"]
        state_total_difference_max = max(
            state_total_difference_max,
            float((state_sum - exported_total).abs().max()),
        )
        closure_max = max(
            closure_max,
            float((frame["cohort_total_ha"] - state_sum).abs().max()),
            float(exported_residual.abs().max()),
        )
    require(state_total_difference_max <= TOLERANCE_HA,
            "Exported state totals differ from component sums")
    require(closure_max <= TOLERANCE_HA,
            "Fixed-cohort state partition does not close")

    baseline_nonpasture = float(frame[
        [state_column(1985, s) for s in STATES if s != "pas"]
    ].to_numpy(dtype="float64").sum())
    baseline_pas_difference = abs(
        float(frame["cohort_total_ha"].sum())
        - float(frame[state_column(1985, "pas")].sum())
    )
    require(baseline_nonpasture <= TOLERANCE_HA,
            "The fixed cohort is not entirely pasture at baseline")
    require(baseline_pas_difference <= TOLERANCE_HA,
            "Baseline pasture does not equal fixed-cohort area")
    require(float(frame["cohort_total_ha"].sum()) > 0,
            "Fixed cohort has zero area")

    return frame, {
        "mode": mode,
        "rows": len(frame),
        "columns": len(frame.columns),
        "unique_cell_id": int(frame["cell_id"].nunique()),
        "raw_sha256": sha256(path),
        "fixed_cohort_area_ha": float(frame["cohort_total_ha"].sum()),
        "cells_with_cohort": int(
            frame["cohort_total_ha"].gt(ZERO_TOLERANCE_HA).sum()
        ),
        "maximum_closure_error_ha": closure_max,
        "maximum_state_total_difference_ha": state_total_difference_max,
        "baseline_nonpasture_ha": baseline_nonpasture,
        "baseline_pas_difference_ha": baseline_pas_difference,
    }


def build_cell_year(raw: pd.DataFrame, attributes: pd.DataFrame) -> pd.DataFrame:
    frames = []
    static = raw[["cell_id", "GRID_ID", "source_batch_id", "cohort_total_ha"]]
    for year in YEARS:
        part = static.copy()
        part["year"] = year
        part["diagnostic_endpoint"] = int(year == 2025)
        for state in STATES:
            part[f"{state}_ha"] = raw[state_column(year, state)].to_numpy()
        part["state_total_ha"] = part[[f"{s}_ha" for s in STATES]].sum(axis=1)
        part["closure_residual_ha"] = (
            part["cohort_total_ha"] - part["state_total_ha"]
        )
        frames.append(part)
    long = pd.concat(frames, ignore_index=True)
    long = long.merge(attributes, on="cell_id", validate="many_to_one")
    require(len(long) == EXPECTED_FULL_CELLS * len(YEARS),
            "Cell-year population changed")
    require(not long.duplicated(["cell_id", "year"]).any(),
            "Duplicate cell-year rows")
    return long


def summarize_subset(frame: pd.DataFrame, boundary_scope: str,
                     primary_biome: str, year: int) -> dict[str, Any]:
    total = float(frame["cohort_total_ha"].sum())
    row: dict[str, Any] = {
        "boundary_scope": boundary_scope,
        "primary_biome": primary_biome,
        "year": year,
        "diagnostic_endpoint": int(year == 2025),
        "cells": int(len(frame)),
        "cells_with_cohort": int(frame["cohort_total_ha"].gt(ZERO_TOLERANCE_HA).sum()),
        "cohort_total_ha": total,
    }
    for state in STATES:
        area = float(frame[f"{state}_ha"].sum())
        row[f"{state}_ha"] = area
        row[f"{state}_share"] = area / total if total > ZERO_TOLERANCE_HA else np.nan
    row["unobserved_ha"] = sum(row[f"{s}_ha"] for s in [
        "nodata", "unexpected", "masked"
    ])
    row["unobserved_share"] = (
        row["unobserved_ha"] / total if total > ZERO_TOLERANCE_HA else np.nan
    )
    row["anthropogenic_ha"] = sum(row[f"{s}_ha"] for s in [
        "pas", "tmp", "oag", "out"
    ])
    row["anthropogenic_share"] = (
        row["anthropogenic_ha"] / total if total > ZERO_TOLERANCE_HA else np.nan
    )
    row["partition_residual_ha"] = total - sum(row[f"{s}_ha"] for s in STATES)
    return row


def build_cohort_summary(cell_year: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year in YEARS:
        year_frame = cell_year[cell_year["year"].eq(year)]
        rows.append(summarize_subset(
            year_frame, "combined_domain", "All", year
        ))
        for biome in ["Amazon", "Cerrado"]:
            rows.append(summarize_subset(
                year_frame[year_frame["primary_biome"].eq(biome)],
                "primary_assignment", biome, year,
            ))
            rows.append(summarize_subset(
                year_frame[
                    year_frame["primary_biome"].eq(biome)
                    & year_frame["transbiome_flag"].eq(0)
                ],
                "nontransbiome_sensitivity", biome, year,
            ))
    summary = pd.DataFrame(rows)
    require(len(summary) == len(YEARS) * 5, "Wrong cohort-summary population")
    require(summary["partition_residual_ha"].abs().max() <= TOLERANCE_HA,
            "Aggregated cohort partition does not close")
    return summary


def load_origin_summary(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    require(path.is_file(), f"Missing accepted origin summary: {path}")
    require(sha256(path) == EXPECTED_ORIGIN_SUMMARY_SHA256,
            "Accepted origin-summary hash differs")
    frame = pd.read_csv(path, float_precision="round_trip")
    require(len(frame) == 8, "Origin summary must contain eight intervals")
    require(frame["diagnostic_interval"].sum() == 1,
            "Origin diagnostic flag is invalid")
    component_columns = [f"pas_tmp_{c}_ha" for c in ORIGIN_COMPONENTS]
    difference = frame[component_columns].sum(axis=1) - frame["consolidation_ha"]
    require(float(difference.abs().max()) <= TOLERANCE_HA,
            "PAS-to-TMP origin partition does not close")
    for component in ORIGIN_COMPONENTS:
        calculated = frame[f"pas_tmp_{component}_ha"] / frame["consolidation_ha"]
        require(float((calculated - frame[f"pas_tmp_{component}_share"]).abs().max())
                <= 1e-12, f"Origin share differs for {component}")

    interval = frame[[
        "interval", "t0", "t1", "diagnostic_interval", "consolidation_ha",
        *component_columns,
        *[f"pas_tmp_{c}_share" for c in ORIGIN_COMPONENTS],
    ]].copy()
    interval["partition_residual_ha"] = difference

    pooled_rows = []
    for window, subset in [
        ("primary_1985_2020", interval[interval["diagnostic_interval"].eq(0)]),
        ("full_observed_1985_2025", interval),
    ]:
        total = float(subset["consolidation_ha"].sum())
        row: dict[str, Any] = {
            "window": window,
            "intervals": len(subset),
            "consolidation_ha": total,
        }
        for component in ORIGIN_COMPONENTS:
            area = float(subset[f"pas_tmp_{component}_ha"].sum())
            row[f"pas_tmp_{component}_ha"] = area
            row[f"pas_tmp_{component}_share"] = area / total
        row["partition_residual_ha"] = total - sum(
            row[f"pas_tmp_{c}_ha"] for c in ORIGIN_COMPONENTS
        )
        pooled_rows.append(row)
    pooled = pd.DataFrame(pooled_rows)
    require(pooled["partition_residual_ha"].abs().max() <= TOLERANCE_HA,
            "Pooled origin partition does not close")
    return interval, pooled


def load_phase9a_matrix(evidence_dir: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    validation_path = evidence_dir / "canonical_phase9a_evidence_validation_v1.json"
    matrix_path = evidence_dir / "canonical_integrated_evidence_matrix_v1.csv"
    require(validation_path.is_file() and matrix_path.is_file(),
            "Accepted Phase 9A evidence products are missing")
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    require(validation.get("validation_status") == "PASS",
            "Phase 9A evidence validation is not PASS")
    expected = validation["outputs"][matrix_path.name]["sha256"]
    require(sha256(matrix_path) == expected, "Phase 9A matrix hash differs")
    matrix = pd.read_csv(matrix_path, encoding="utf-8-sig")
    require(len(matrix) == 30 and matrix["finding_id"].is_unique,
            "Unexpected Phase 9A matrix population")
    gaps = matrix[matrix["evidence_status"].eq("evidence_gap")]
    require(set(gaps["finding_id"]) == {"P9A001", "P9A002"},
            "The expected RQ1/RQ2 gaps are not present")
    return matrix, validation


def pct(value: float) -> str:
    return f"{100 * value:.2f}%"


def mha(value: float) -> str:
    return f"{value / 1_000_000:.3f} million ha"


def new_evidence_rows(cohort: pd.DataFrame, origin_interval: pd.DataFrame,
                      origin_pooled: pd.DataFrame,
                      cohort_sha: str, origin_interval_sha: str,
                      origin_pooled_sha: str,
                      columns: list[str]) -> pd.DataFrame:
    domain = cohort[
        cohort["boundary_scope"].eq("combined_domain")
        & cohort["primary_biome"].eq("All")
    ].set_index("year")
    primary_domain = domain.loc[PRIMARY_YEARS]
    y2020 = domain.loc[2020]
    y2025 = domain.loc[2025]
    min_year = int(primary_domain["pas_share"].idxmin())
    min_pas = float(primary_domain.loc[min_year, "pas_share"])

    biome2020 = cohort[
        cohort["boundary_scope"].eq("primary_assignment")
        & cohort["year"].eq(2020)
    ].set_index("primary_biome")
    amazon = biome2020.loc["Amazon"]
    cerrado = biome2020.loc["Cerrado"]

    first = origin_interval.loc[origin_interval["t0"].idxmin()]
    last_primary = origin_interval[
        origin_interval["diagnostic_interval"].eq(0)
    ].sort_values("t0").iloc[-1]
    diagnostic = origin_interval[
        origin_interval["diagnostic_interval"].eq(1)
    ].iloc[0]
    primary_pool = origin_pooled[
        origin_pooled["window"].eq("primary_1985_2020")
    ].iloc[0]
    full_pool = origin_pooled[
        origin_pooled["window"].eq("full_observed_1985_2025")
    ].iloc[0]

    common = {
        "spatial_scope": "combined_domain",
        "population": "fixed_1985_pasture_cohort",
        "temporal_scope": "1985_2025",
        "temporal_role": "both",
        "evidence_mode": "descriptive",
        "evidence_status": "supported",
        "robustness_status": "not_assessed",
        "source_phase": "9A.1",
        "manuscript_use": "main_result",
        "causal_claim_flag": 0,
        "source_authenticated": True,
        "evidence_matrix_version": EVIDENCE_MATRIX_VERSION,
    }

    records = [
        {
            **common,
            "finding_id": "P9A031", "research_question": "RQ1",
            "topic": "fixed_1985_pasture_cohort_endpoint_fate",
            "metric": "cohort_state_composition",
            "temporal_scope": "1985_2020", "temporal_role": "primary",
            "main_result": (
                "The fixed 1985 pasture cohort was redistributed among endpoint "
                "land-cover states by 2020."
            ),
            "numeric_evidence": (
                f"Initial cohort = {mha(float(domain.loc[1985, 'cohort_total_ha']))}; "
                f"2020 shares: pasture {pct(float(y2020.pas_share))}, "
                f"temporary agriculture {pct(float(y2020.tmp_share))}, "
                f"native vegetation {pct(float(y2020.nat_share))}, "
                f"other agriculture {pct(float(y2020.oag_share))}."
            ),
            "interpretation_boundary": (
                "Endpoint state is not continuous pixel persistence and does not "
                "identify the date or pathway of an intervening transition."
            ),
            "source_id": "phase9_rq1_cohort_summary",
            "source_relative_path": "canonical_fixed_1985_pasture_cohort_summary_v1.csv",
            "source_sha256": cohort_sha,
            "source_locator": "Combined-domain rows for 1985 and 2020",
        },
        {
            **common,
            "finding_id": "P9A032", "research_question": "RQ1",
            "topic": "fixed_cohort_pasture_endpoint_change",
            "metric": "pas_endpoint_share",
            "temporal_scope": "1985_2020", "temporal_role": "primary",
            "main_result": (
                "The share of fixed-cohort area classified as pasture changes "
                "substantially across the primary reference years."
            ),
            "numeric_evidence": (
                f"Pasture endpoint share is 100% in 1985 and reaches its primary "
                f"minimum of {pct(min_pas)} in {min_year}."
            ),
            "interpretation_boundary": (
                "The series is not a survival curve: pixels may leave and later "
                "return to pasture between reference years."
            ),
            "source_id": "phase9_rq1_cohort_summary",
            "source_relative_path": "canonical_fixed_1985_pasture_cohort_summary_v1.csv",
            "source_sha256": cohort_sha,
            "source_locator": "Combined-domain primary endpoint series",
        },
        {
            **common,
            "finding_id": "P9A033", "research_question": "RQ1",
            "topic": "fixed_cohort_biome_contrast",
            "metric": "cohort_state_composition",
            "spatial_scope": "Amazon_and_Cerrado",
            "temporal_scope": "2020", "temporal_role": "primary",
            "main_result": (
                "The 2020 endpoint composition of the fixed cohort differs between "
                "primary-biome assignments."
            ),
            "numeric_evidence": (
                f"Amazon-assigned cohort: pasture {pct(float(amazon.pas_share))}, "
                f"temporary agriculture {pct(float(amazon.tmp_share))}; "
                f"Cerrado-assigned cohort: pasture {pct(float(cerrado.pas_share))}, "
                f"temporary agriculture {pct(float(cerrado.tmp_share))}."
            ),
            "interpretation_boundary": (
                "Whole-cell primary-biome assignment is not pixel-level partitioning; "
                "the non-transbiome sensitivity is reported separately."
            ),
            "source_id": "phase9_rq1_cohort_summary",
            "source_relative_path": "canonical_fixed_1985_pasture_cohort_summary_v1.csv",
            "source_sha256": cohort_sha,
            "source_locator": "Primary-assignment biome rows for 2020",
        },
        {
            **common,
            "finding_id": "P9A034", "research_question": "RQ1",
            "topic": "fixed_cohort_diagnostic_endpoint",
            "metric": "cohort_state_composition",
            "temporal_scope": "2020_2025", "temporal_role": "diagnostic",
            "evidence_status": "qualified", "manuscript_use": "qualification",
            "main_result": (
                "The 2025 endpoint extends the fixed-cohort composition descriptively."
            ),
            "numeric_evidence": (
                f"2025 shares: pasture {pct(float(y2025.pas_share))}, temporary "
                f"agriculture {pct(float(y2025.tmp_share))}, native vegetation "
                f"{pct(float(y2025.nat_share))}."
            ),
            "interpretation_boundary": (
                "The 2025 map is diagnostic and does not replace primary-period conclusions."
            ),
            "source_id": "phase9_rq1_cohort_summary",
            "source_relative_path": "canonical_fixed_1985_pasture_cohort_summary_v1.csv",
            "source_sha256": cohort_sha,
            "source_locator": "Combined-domain row for 2025",
        },
        {
            **common,
            "finding_id": "P9A035", "research_question": "RQ2",
            "topic": "pasture_origin_shift_in_consolidation",
            "metric": "pas_tmp_origin_share",
            "population": "all_consolidation_area",
            "temporal_scope": "1985_2020", "temporal_role": "primary",
            "main_result": (
                "The origin of pasture converted to temporary agriculture shifts "
                "from the left-censored 1985 stock toward pasture established during "
                "the observed series."
            ),
            "numeric_evidence": (
                f"Censored/new shares: 1985-1990 "
                f"{pct(float(first.pas_tmp_censored_share))}/"
                f"{pct(float(first.pas_tmp_new_share))}; 2015-2020 "
                f"{pct(float(last_primary.pas_tmp_censored_share))}/"
                f"{pct(float(last_primary.pas_tmp_new_share))}."
            ),
            "interpretation_boundary": (
                "Origin is defined by pasture-age code at interval start; it is not "
                "the complete historical trajectory of the pixel."
            ),
            "source_id": "phase9_rq2_origin_summary",
            "source_relative_path": "canonical_pas_tmp_origin_interval_summary_v1.csv",
            "source_sha256": origin_interval_sha,
            "source_locator": "Primary interval series",
        },
        {
            **common,
            "finding_id": "P9A036", "research_question": "RQ2",
            "topic": "pooled_primary_pasture_origins",
            "metric": "pas_tmp_origin_share",
            "population": "all_primary_consolidation_area",
            "temporal_scope": "1985_2020", "temporal_role": "primary",
            "main_result": (
                "Across the primary period, consolidation draws from both the fixed "
                "1985 pasture stock and pasture established during the series."
            ),
            "numeric_evidence": (
                f"Primary consolidation = {mha(float(primary_pool.consolidation_ha))}; "
                f"censored {pct(float(primary_pool.pas_tmp_censored_share))}, "
                f"new {pct(float(primary_pool.pas_tmp_new_share))}, unresolved age "
                f"{pct(float(primary_pool.pas_tmp_unresolved_age_share))}, "
                f"unattributed {pct(float(primary_pool.pas_tmp_unattributed_age_share))}."
            ),
            "interpretation_boundary": (
                "Pooled areas sum interval conversions and do not deduplicate pixels "
                "converted in different intervals."
            ),
            "source_id": "phase9_rq2_origin_summary",
            "source_relative_path": "canonical_pas_tmp_origin_pooled_summary_v1.csv",
            "source_sha256": origin_pooled_sha,
            "source_locator": "Primary pooled row",
        },
        {
            **common,
            "finding_id": "P9A037", "research_question": "RQ2",
            "topic": "pasture_age_ambiguity_components",
            "metric": "pas_tmp_unresolved_and_unattributed",
            "population": "all_observed_consolidation_area",
            "temporal_scope": "1985_2025", "temporal_role": "both",
            "evidence_status": "qualified", "manuscript_use": "qualification",
            "main_result": (
                "The unresolved pasture-age component is retained explicitly and the "
                "unattributed component is zero in the accepted series."
            ),
            "numeric_evidence": (
                f"Full observed unresolved area = "
                f"{float(full_pool.pas_tmp_unresolved_age_ha):.3f} ha "
                f"({pct(float(full_pool.pas_tmp_unresolved_age_share))}); "
                f"unattributed area = {float(full_pool.pas_tmp_unattributed_age_ha):.3f} ha. "
                f"Diagnostic 2020-2025 new-pasture share = "
                f"{pct(float(diagnostic.pas_tmp_new_share))}."
            ),
            "interpretation_boundary": (
                "Pasture-age code 1 remains unresolved and is not decoded as a numerical age."
            ),
            "source_id": "phase9_rq2_origin_summary",
            "source_relative_path": "canonical_pas_tmp_origin_pooled_summary_v1.csv",
            "source_sha256": origin_pooled_sha,
            "source_locator": "Full pooled and diagnostic rows",
        },
    ]
    result = pd.DataFrame(records)
    return result.reindex(columns=columns)


def build_coverage(matrix: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for rq, frame in matrix.groupby("research_question", sort=True):
        rows.append({
            "research_question": rq,
            "evidence_rows": len(frame),
            "supported_rows": int(frame["evidence_status"].eq("supported").sum()),
            "qualified_rows": int(frame["evidence_status"].eq("qualified").sum()),
            "evidence_gap_rows": int(frame["evidence_status"].eq("evidence_gap").sum()),
            "descriptive_rows": int(frame["evidence_mode"].eq("descriptive").sum()),
            "formal_inference_rows": int(frame["evidence_mode"].isin(
                ["global_inference", "local_inference"]
            ).sum()),
            "sensitivity_rows": int(frame["evidence_mode"].eq("sensitivity").sum()),
            "primary_or_both_rows": int(frame["temporal_role"].isin(
                ["primary", "both"]
            ).sum()),
            "diagnostic_only_rows": int(frame["temporal_role"].eq("diagnostic").sum()),
        })
    return pd.DataFrame(rows)


def build_markdown(matrix: pd.DataFrame, coverage: pd.DataFrame) -> str:
    lines = [
        "# Canonical integrated evidence matrix — gap-resolved version 2",
        "",
        "RQ1 and RQ2 are resolved by authenticated Phase 9A.1 extractions.",
        "The original version 1 matrix remains unchanged for provenance.",
        "",
        "## Coverage",
        "",
        "| Research question | Rows | Supported | Qualified | Gaps |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in coverage.to_dict("records"):
        lines.append(
            f"| {row['research_question']} | {row['evidence_rows']} | "
            f"{row['supported_rows']} | {row['qualified_rows']} | "
            f"{row['evidence_gap_rows']} |"
        )
    for rq, frame in matrix.groupby("research_question", sort=True):
        lines.extend(["", f"## {rq}", ""])
        for row in frame.to_dict("records"):
            lines.extend([
                f"### {row['finding_id']} — {row['topic']}", "",
                str(row["main_result"]), "",
                f"- **Evidence:** {row['numeric_evidence']}",
                f"- **Mode/status:** {row['evidence_mode']} / {row['evidence_status']}",
                f"- **Temporal role:** {row['temporal_role']} ({row['temporal_scope']})",
                f"- **Robustness:** {row['robustness_status']}",
                f"- **Boundary:** {row['interpretation_boundary']}",
                f"- **Source:** Phase {row['source_phase']}, "
                f"`{row['source_relative_path']}` — {row['source_locator']}", "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def make_figures(cohort: pd.DataFrame, origin: pd.DataFrame,
                 figure_dir: Path) -> list[Path]:
    figure_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 9})

    domain = cohort[
        cohort["boundary_scope"].eq("combined_domain")
        & cohort["primary_biome"].eq("All")
    ].sort_values("year")
    series = {
        "Pasture": domain["pas_ha"] / 1e6,
        "Temporary agriculture": domain["tmp_ha"] / 1e6,
        "Native vegetation": domain["nat_ha"] / 1e6,
        "Other agriculture": domain["oag_ha"] / 1e6,
        "Other / water": (domain["out_ha"] + domain["water_ha"]) / 1e6,
        "Unobserved": domain["unobserved_ha"] / 1e6,
    }
    colors = ["#d9a441", "#7b4fa3", "#3f8f5f", "#d87a3c", "#7f8790", "#d9d9d9"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.stackplot(domain["year"], *series.values(), labels=series.keys(), colors=colors)
    ax.axvline(2020, color="black", linestyle="--", linewidth=1)
    ax.text(2020.4, ax.get_ylim()[1] * 0.96, "diagnostic extension", va="top")
    ax.set_ylabel("Fixed 1985 pasture cohort area (million ha)")
    ax.set_xlabel("Reference year")
    ax.set_title("Endpoint land-cover composition of the fixed 1985 pasture cohort")
    ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    fig1 = figure_dir / "fig01_fixed_1985_pasture_cohort_composition_v1.png"
    fig.savefig(fig1, dpi=220, bbox_inches="tight")
    plt.close(fig)

    origin = origin.sort_values("t0")
    labels = [f"{int(a)}–{int(b)}" for a, b in zip(origin.t0, origin.t1)]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bottom = np.zeros(len(origin))
    origin_series = [
        ("Left-censored 1985 stock", "pas_tmp_censored_share", "#355c8a"),
        ("Pasture established during series", "pas_tmp_new_share", "#d08a2e"),
        ("Unresolved age", "pas_tmp_unresolved_age_share", "#8c6bb1"),
        ("Unattributed age", "pas_tmp_unattributed_age_share", "#bdbdbd"),
    ]
    for label, column, color in origin_series:
        values = origin[column].to_numpy(dtype=float) * 100
        ax.bar(labels, values, bottom=bottom, label=label, color=color)
        bottom += values
    ax.axvline(6.5, color="black", linestyle="--", linewidth=1)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Share of PAS→TMP area (%)")
    ax.set_xlabel("Five-year interval")
    ax.set_title("Origin of pasture converted to temporary agriculture")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    fig.tight_layout()
    fig2 = figure_dir / "fig02_pas_tmp_origin_composition_v1.png"
    fig.savefig(fig2, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return [fig1, fig2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pilot", "full"], required=True)
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--raw-file", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--no-mount", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if drive is not None and not args.no_mount:
        drive.mount("/content/drive")

    output_dir = args.output_dir or args.project_dir / OUTPUT_RELATIVE
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = args.raw_file or args.raw_dir / raw_filename(args.mode)

    print("CANONICAL PHASE 9 RQ1/RQ2 GAP RESOLUTION — VERSION 1")
    print("Mode:", args.mode)
    print("Fixed-cohort export:", raw_path)
    print("Output directory:", output_dir)

    raw, raw_checks = load_and_validate_raw(raw_path, args.mode)

    if args.mode == "pilot":
        validation_path = output_dir / "pilot_phase9_gap_resolution_validation_v1.json"
        validation = {
            "validation_status": "PASS",
            "mode": "pilot",
            "version": VERSION,
            "cohort_export_version": COHORT_EXPORT_VERSION,
            "execution_utc": datetime.now(timezone.utc).isoformat(),
            "script_sha256": sha256(Path(__file__).resolve()),
            "raw_input": {"path": str(raw_path), **raw_checks},
            "checks": {
                "row_count": raw_checks["rows"] == EXPECTED_PILOT_CELLS,
                "unique_ids": raw_checks["unique_cell_id"] == EXPECTED_PILOT_CELLS,
                "partition_closure": raw_checks["maximum_closure_error_ha"] <= TOLERANCE_HA,
                "baseline_all_pasture": raw_checks["baseline_pas_difference_ha"] <= TOLERANCE_HA,
                "positive_cohort_area": raw_checks["fixed_cohort_area_ha"] > 0,
            },
        }
        require(all(validation["checks"].values()), "Pilot checks failed")
        write_json(validation_path, validation)
        inventory = pd.DataFrame([{
            "relative_path": validation_path.name,
            "bytes": validation_path.stat().st_size,
            "sha256": sha256(validation_path),
        }])
        inventory.to_csv(
            output_dir / "pilot_phase9_gap_resolution_inventory_v1.csv",
            index=False, encoding="utf-8-sig",
        )
        print("PHASE 9 GAP-RESOLUTION PILOT — VALIDATION PASS")
        print("Rows:", f"{len(raw):,}")
        print("Fixed-cohort area in pilot (ha):",
              f"{raw_checks['fixed_cohort_area_ha']:,.3f}")
        print("Validation:", validation_path)
        return

    pilot_path = output_dir / "pilot_phase9_gap_resolution_validation_v1.json"
    require(pilot_path.is_file(), "Full mode requires an accepted pilot validation")
    pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
    require(pilot.get("validation_status") == "PASS" and pilot.get("mode") == "pilot",
            "Pilot validation is not accepted")

    spatial_path = (
        args.project_dir / "spatial/phase1/canonical_spatial_support_v1.parquet"
    )
    require(spatial_path.is_file(), f"Missing spatial support: {spatial_path}")
    require(sha256(spatial_path) == EXPECTED_SPATIAL_SHA256,
            "Spatial-support hash differs")
    spatial = pd.read_parquet(spatial_path, columns=[
        "cell_id", "primary_biome", "amazon_fraction_cell", "cerrado_fraction_cell"
    ])
    spatial["cell_id"] = spatial["cell_id"].astype(str)
    require(len(spatial) == EXPECTED_FULL_CELLS and spatial["cell_id"].is_unique,
            "Spatial-support population changed")
    require(set(raw["cell_id"]) == set(spatial["cell_id"]),
            "GEE export and canonical spatial support contain different cells")
    require(spatial["primary_biome"].value_counts().to_dict()
            == EXPECTED_PRIMARY_BIOME_COUNTS, "Primary-biome counts changed")
    spatial["transbiome_flag"] = (
        spatial["amazon_fraction_cell"].gt(0)
        & spatial["cerrado_fraction_cell"].gt(0)
    ).astype("int8")
    require(int(spatial["transbiome_flag"].sum()) == EXPECTED_TRANSBIOME_CELLS,
            "Transbiome population changed")
    attributes = spatial[["cell_id", "primary_biome", "transbiome_flag"]]

    cell_year = build_cell_year(raw, attributes)
    cohort_summary = build_cohort_summary(cell_year)

    origin_path = (
        args.project_dir / "analysis/canonical_stock_flow_derived_metrics_summary_v1.csv"
    )
    origin_interval, origin_pooled = load_origin_summary(origin_path)

    evidence_dir = args.project_dir / "spatial/phase9/evidence_matrix_v1"
    matrix_v1, phase9a_validation = load_phase9a_matrix(evidence_dir)

    cell_year_path = output_dir / "canonical_fixed_1985_pasture_cohort_cell_year_v1.parquet"
    cohort_summary_path = output_dir / "canonical_fixed_1985_pasture_cohort_summary_v1.csv"
    origin_interval_path = output_dir / "canonical_pas_tmp_origin_interval_summary_v1.csv"
    origin_pooled_path = output_dir / "canonical_pas_tmp_origin_pooled_summary_v1.csv"
    resolution_path = output_dir / "canonical_phase9_evidence_gap_resolution_v1.csv"
    matrix_path = output_dir / "canonical_integrated_evidence_matrix_v2.csv"
    markdown_path = output_dir / "canonical_integrated_evidence_matrix_v2.md"
    coverage_path = output_dir / "canonical_phase9a_evidence_coverage_v2.csv"
    validation_path = output_dir / "canonical_phase9_gap_resolution_validation_v1.json"
    inventory_path = output_dir / "canonical_phase9_gap_resolution_inventory_v1.csv"
    figure_dir = output_dir / "figures"

    cell_year.to_parquet(cell_year_path, index=False)
    cohort_summary.to_csv(cohort_summary_path, index=False, encoding="utf-8-sig",
                          float_format="%.15g")
    origin_interval.to_csv(origin_interval_path, index=False, encoding="utf-8-sig",
                           float_format="%.15g")
    origin_pooled.to_csv(origin_pooled_path, index=False, encoding="utf-8-sig",
                         float_format="%.15g")

    retained = matrix_v1[~matrix_v1["finding_id"].isin(["P9A001", "P9A002"])].copy()
    added = new_evidence_rows(
        cohort_summary, origin_interval, origin_pooled,
        sha256(cohort_summary_path), sha256(origin_interval_path),
        sha256(origin_pooled_path),
        list(matrix_v1.columns),
    )
    matrix_v2 = pd.concat([retained, added], ignore_index=True)
    matrix_v2["evidence_matrix_version"] = EVIDENCE_MATRIX_VERSION
    require(len(matrix_v2) == 35 and matrix_v2["finding_id"].is_unique,
            "Gap-resolved matrix population is invalid")
    require(not matrix_v2["evidence_status"].eq("evidence_gap").any(),
            "At least one evidence gap remains")
    require(set(matrix_v2["research_question"]) == {"RQ1", "RQ2", "RQ3", "RQ4", "RQ5"},
            "Research-question coverage changed")
    require(int(matrix_v2["causal_claim_flag"].sum()) == 0,
            "A causal claim was introduced")

    coverage = build_coverage(matrix_v2)
    resolution = pd.DataFrame([
        {
            "original_gap_id": "P9A001", "research_question": "RQ1",
            "resolution_status": "resolved_with_new_fixed_cohort_extraction",
            "replacement_finding_ids": "P9A031|P9A032|P9A033|P9A034",
            "source_product": cohort_summary_path.name,
        },
        {
            "original_gap_id": "P9A002", "research_question": "RQ2",
            "resolution_status": "resolved_from_accepted_stock_flow_accounting",
            "replacement_finding_ids": "P9A035|P9A036|P9A037",
            "source_product": origin_pooled_path.name,
        },
    ])

    matrix_v2.to_csv(matrix_path, index=False, encoding="utf-8-sig")
    coverage.to_csv(coverage_path, index=False, encoding="utf-8-sig")
    resolution.to_csv(resolution_path, index=False, encoding="utf-8-sig")
    markdown_path.write_text(build_markdown(matrix_v2, coverage), encoding="utf-8")
    figure_paths = make_figures(cohort_summary, origin_interval, figure_dir)

    domain_summary = cohort_summary[
        cohort_summary["boundary_scope"].eq("combined_domain")
    ].sort_values("year")
    checks = {
        "full_cell_population": len(raw) == EXPECTED_FULL_CELLS,
        "cell_year_population": len(cell_year) == EXPECTED_FULL_CELLS * len(YEARS),
        "raw_partition_closure": raw_checks["maximum_closure_error_ha"] <= TOLERANCE_HA,
        "baseline_all_pasture": raw_checks["baseline_pas_difference_ha"] <= TOLERANCE_HA,
        "canonical_cell_identity": set(raw["cell_id"]) == set(spatial["cell_id"]),
        "cohort_total_constant_across_years":
            float(domain_summary["cohort_total_ha"].max()
                  - domain_summary["cohort_total_ha"].min()) <= TOLERANCE_HA,
        "cohort_summary_closure":
            float(cohort_summary["partition_residual_ha"].abs().max()) <= TOLERANCE_HA,
        "origin_interval_closure":
            float(origin_interval["partition_residual_ha"].abs().max()) <= TOLERANCE_HA,
        "origin_pooled_closure":
            float(origin_pooled["partition_residual_ha"].abs().max()) <= TOLERANCE_HA,
        "phase9a_v1_authenticated": phase9a_validation["validation_status"] == "PASS",
        "matrix_v2_population": len(matrix_v2) == 35,
        "rq1_rq2_gaps_resolved": not matrix_v2["evidence_status"].eq("evidence_gap").any(),
        "diagnostic_2025_included": 2025 in set(domain_summary["year"]),
        "no_causal_claims": int(matrix_v2["causal_claim_flag"].sum()) == 0,
    }
    require(all(checks.values()), "At least one full gap-resolution check failed")

    validation = {
        "validation_status": "PASS",
        "mode": "full",
        "version": VERSION,
        "cohort_export_version": COHORT_EXPORT_VERSION,
        "evidence_matrix_version": EVIDENCE_MATRIX_VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {
            "fixed_cohort_export": {"path": str(raw_path), **raw_checks},
            "spatial_support": {"path": str(spatial_path), "sha256": sha256(spatial_path)},
            "accepted_origin_summary": {"path": str(origin_path), "sha256": sha256(origin_path)},
            "phase9a_matrix_v1": {
                "path": str(evidence_dir / "canonical_integrated_evidence_matrix_v1.csv"),
                "sha256": sha256(evidence_dir / "canonical_integrated_evidence_matrix_v1.csv"),
            },
            "pilot_validation": {"path": str(pilot_path), "sha256": sha256(pilot_path)},
        },
        "populations": {
            "cells": len(raw), "reference_years": len(YEARS),
            "cell_year_rows": len(cell_year), "cohort_summary_rows": len(cohort_summary),
            "origin_interval_rows": len(origin_interval),
            "origin_pooled_rows": len(origin_pooled),
            "matrix_v1_rows": len(matrix_v1), "matrix_v2_rows": len(matrix_v2),
            "remaining_evidence_gaps": int(
                matrix_v2["evidence_status"].eq("evidence_gap").sum()
            ),
        },
        "design_boundaries": {
            "rq1_measure": "endpoint state composition of a fixed pixel cohort",
            "rq1_not_survival_curve": True,
            "rq2_origin_time": "pasture-age code at interval start",
            "primary_period": "1985-2020",
            "diagnostic_endpoint": "2025 included and flagged",
            "new_spatial_inference": False,
            "new_causal_inference": False,
        },
        "checks": checks,
    }
    output_paths = [
        cell_year_path, cohort_summary_path, origin_interval_path,
        origin_pooled_path, resolution_path, matrix_path, markdown_path,
        coverage_path, *figure_paths,
    ]
    validation["outputs"] = {
        str(path.relative_to(output_dir)): {
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        } for path in output_paths
    }
    write_json(validation_path, validation)

    inventory_rows = []
    for path in [*output_paths, validation_path]:
        inventory_rows.append({
            "relative_path": str(path.relative_to(output_dir)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    pd.DataFrame(inventory_rows).to_csv(
        inventory_path, index=False, encoding="utf-8-sig"
    )

    print("PHASE 9 RQ1/RQ2 GAP RESOLUTION COMPLETE — VALIDATION PASS")
    print("Fixed-cohort cells:", f"{len(raw):,}")
    print("Cell-year rows:", f"{len(cell_year):,}")
    print("Gap-resolved evidence statements:", f"{len(matrix_v2):,}")
    print("Remaining evidence gaps: 0")
    print("Validation:", validation_path)
    print("Inventory:", inventory_path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Harmonize the English TMP label without changing accepted analytical results."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
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


VERSION = "phase9a2-tmp-terminology-harmonization-v1"
MATRIX_VERSION = "phase9a2-terminology-harmonized-evidence-matrix-v3"
ACCEPTED_PHASE9A1_VERSION = "phase9-rq1-rq2-gap-resolution-v1"
EXPECTED_PHASE9A1_VALIDATION_SHA256 = (
    "16443cc274772e43cc575d3687888d56a09fc420dd18d68fc4266525bc244951"
)
EXPECTED_MATRIX_V2_SHA256 = (
    "b5d5518545b23f3e1ef6e2692445021461eaad0a301711acf611bdae887eaa62"
)
EXPECTED_MATRIX_ROWS = 35
EXPECTED_TARGET_OCCURRENCES = 5
EXPECTED_CHANGED_FIELDS = 4

PROJECT_DIR = Path(os.environ.get(
    "PHASE9_PROJECT_DIR", "/content/drive/MyDrive/Trabalho/Contabilidade"
))
INPUT_RELATIVE = Path("spatial/phase9/gap_resolution_v1")
OUTPUT_RELATIVE = Path("spatial/phase9/terminology_harmonization_v1")
CONFIG_NAME = "phase9a2_tmp_terminology_crosswalk_v1.csv"
TARGET_COLUMNS = [
    "main_result", "numeric_evidence", "interpretation_boundary", "source_locator"
]
PROTECTED_TECHNICAL_TOKENS = [
    "TMP", "tmp", "NAT→TMP", "PAS→TMP", "nat_tmp", "pas_tmp"
]


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def locate_config(explicit: Path | None, project_dir: Path) -> Path:
    candidates = []
    if explicit is not None:
        candidates.append(explicit)
    script = Path(__file__).resolve()
    candidates.extend([
        script.parent.parent / "config" / CONFIG_NAME,
        script.parent / CONFIG_NAME,
        Path("/content") / CONFIG_NAME,
        project_dir / "config" / CONFIG_NAME,
    ])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"Missing {CONFIG_NAME}. Run from the extracted package or pass "
        "--terminology-config."
    )


def load_crosswalk(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    expected = {
        "term_id", "context", "stable_code", "portuguese_label",
        "preferred_english", "deprecated_english", "replacement_scope",
        "implementation_note",
    }
    require(set(frame.columns) == expected, "Unexpected crosswalk schema")
    require(len(frame) == 6 and frame["term_id"].is_unique,
            "Unexpected crosswalk population")
    require(frame.loc[frame.term_id.eq("TMP_CLASS"), "preferred_english"].item()
            == "Temporary Crop", "Unexpected canonical TMP class label")
    require(frame.loc[frame.term_id.eq("TMP_PROSE"), "preferred_english"].item()
            == "temporary crops", "Unexpected preferred TMP prose label")
    require(frame.loc[frame.term_id.eq("OAG_CLASS"), "replacement_scope"].item()
            == "no_replacement", "OAG protection rule is missing")
    return frame


def authenticate_phase9a1(input_dir: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    validation_path = input_dir / "canonical_phase9_gap_resolution_validation_v1.json"
    require(validation_path.is_file(), f"Missing accepted validation: {validation_path}")
    require(sha256(validation_path) == EXPECTED_PHASE9A1_VALIDATION_SHA256,
            "Phase 9A.1 validation hash differs from the accepted record")
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    require(validation.get("validation_status") == "PASS",
            "Phase 9A.1 validation is not PASS")
    require(validation.get("version") == ACCEPTED_PHASE9A1_VERSION,
            "Unexpected Phase 9A.1 version")

    required = {
        "matrix": "canonical_integrated_evidence_matrix_v2.csv",
        "cohort": "canonical_fixed_1985_pasture_cohort_summary_v1.csv",
        "origin": "canonical_pas_tmp_origin_interval_summary_v1.csv",
        "coverage": "canonical_phase9a_evidence_coverage_v2.csv",
    }
    paths = {key: input_dir / name for key, name in required.items()}
    outputs = validation.get("outputs", {})
    for path in paths.values():
        require(path.is_file(), f"Missing accepted Phase 9A.1 input: {path}")
        expected = outputs.get(path.name, {}).get("sha256")
        require(expected is not None, f"Input absent from validation: {path.name}")
        require(sha256(path) == expected, f"Hash mismatch: {path.name}")
    require(sha256(paths["matrix"]) == EXPECTED_MATRIX_V2_SHA256,
            "Matrix v2 hash differs from the frozen accepted matrix")
    paths["validation"] = validation_path
    return validation, paths


def replace_phrase(value: str) -> tuple[str, int]:
    pattern = re.compile(r"temporary agriculture", flags=re.IGNORECASE)

    def replacement(match: re.Match[str]) -> str:
        return "Temporary Crops" if match.group(0)[0].isupper() else "temporary crops"

    return pattern.subn(replacement, str(value))


def harmonize_matrix(matrix: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    require(len(matrix) == EXPECTED_MATRIX_ROWS, "Unexpected matrix v2 population")
    require(matrix["finding_id"].is_unique, "Duplicate finding_id in matrix v2")
    require(set(TARGET_COLUMNS).issubset(matrix.columns),
            "Matrix lacks a human-readable target column")
    require("evidence_matrix_version" in matrix.columns,
            "Matrix lacks evidence_matrix_version")

    result = matrix.copy()
    audit_rows = []
    total = 0
    for row_index, row in matrix.iterrows():
        for column in TARGET_COLUMNS:
            old = str(row[column])
            new, count = replace_phrase(old)
            if count:
                audit_rows.append({
                    "finding_id": row["finding_id"],
                    "column_name": column,
                    "occurrence_count": count,
                    "original_text": old,
                    "harmonized_text": new,
                    "change_type": "human_readable_english_label_only",
                })
                result.at[row_index, column] = new
                total += count

    require(total == EXPECTED_TARGET_OCCURRENCES,
            f"Expected 5 replacements; observed {total}")
    require(len(audit_rows) == EXPECTED_CHANGED_FIELDS,
            "Expected four changed evidence fields")
    result["evidence_matrix_version"] = MATRIX_VERSION

    remaining = sum(
        int(result[column].astype(str).str.contains(
            r"temporary agriculture", case=False, regex=True
        ).sum()) for column in TARGET_COLUMNS
    )
    require(remaining == 0,
            "Deprecated TMP wording remains in a human-readable matrix field")

    allowed = set(TARGET_COLUMNS + ["evidence_matrix_version"])
    for column in matrix.columns:
        if column not in allowed:
            require(matrix[column].equals(result[column]),
                    f"Non-terminological column changed: {column}")
    require(result["finding_id"].tolist() == matrix["finding_id"].tolist(),
            "Finding order or identity changed")
    require(result["source_sha256"].equals(matrix["source_sha256"]),
            "Source hashes changed")
    require(int(result["causal_claim_flag"].sum()) == 0,
            "A causal claim was introduced")
    require(not result["evidence_status"].eq("evidence_gap").any(),
            "An evidence gap was introduced")
    return result, pd.DataFrame(audit_rows)


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
        "# Canonical integrated evidence matrix — terminology-harmonized version 3",
        "",
        "This derivative preserves all accepted Phase 9A.1 evidence while using",
        "**Temporary Crop** as the class label and **temporary crops** in prose.",
        "Stable analytical codes and the immutable version 2 matrix are unchanged.",
        "",
        "## Coverage", "",
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
    require(len(domain) == 9, "Unexpected combined-domain cohort series")
    series = {
        "Pasture": domain["pas_ha"] / 1e6,
        "Temporary Crop": domain["tmp_ha"] / 1e6,
        "Native Vegetation": domain["nat_ha"] / 1e6,
        "Other Agriculture": domain["oag_ha"] / 1e6,
        "Other / Water": (domain["out_ha"] + domain["water_ha"]) / 1e6,
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
    fig1 = figure_dir / "fig01_fixed_1985_pasture_cohort_composition_v2.png"
    fig.savefig(fig1, dpi=220, bbox_inches="tight")
    plt.close(fig)

    origin = origin.sort_values("t0")
    require(len(origin) == 8, "Unexpected PAS→TMP interval series")
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
    ax.set_title("Origin of pasture converted to temporary crops")
    ax.tick_params(axis="x", rotation=35)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    fig.tight_layout()
    fig2 = figure_dir / "fig02_pas_tmp_origin_composition_v2.png"
    fig.savefig(fig2, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return [fig1, fig2]


def build_note(audit: pd.DataFrame) -> str:
    changed_ids = ", ".join(audit["finding_id"].tolist())
    count = int(audit["occurrence_count"].sum())
    return (
        "# Phase 9A.2 — TMP terminology harmonization\n\n"
        "The English class label is **Temporary Crop**. In running prose, the "
        "preferred form is **temporary crops**. The Portuguese source label "
        "remains *agricultura temporária* and the stable analytical code remains "
        "`TMP`.\n\n"
        f"Phase 9A.2 changed {count} human-readable occurrences in evidence "
        f"records {changed_ids}. It did not change any metric, value, class code, "
        "column name, finding identity, source hash, analytical decision, or "
        "interpretation boundary.\n\n"
        "`NAT→TMP`, `PAS→TMP`, `nat_tmp_*`, `pas_tmp_*`, and `tmp_*` remain valid "
        "stable technical notation. **Other Agriculture** (`OAG`) is a separate "
        "class and was not renamed or merged.\n\n"
        "The accepted Phase 9A v1 and Phase 9A.1 matrix v2 remain immutable "
        "provenance records. The terminology-harmonized matrix v3 is the "
        "preferred source for new English-language manuscript text and figures.\n"
    )


def verify_engine() -> None:
    cases = {
        "temporary agriculture": "temporary crops",
        "Temporary agriculture": "Temporary Crops",
        "other agriculture": "other agriculture",
        "NAT→TMP": "NAT→TMP",
        "pas_tmp_origin_share": "pas_tmp_origin_share",
    }
    for source, expected in cases.items():
        observed, _ = replace_phrase(source)
        require(observed == expected,
                f"Terminology-engine test failed: {source!r} -> {observed!r}")
    print("Terminology-engine verification: PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=PROJECT_DIR)
    parser.add_argument("--input-dir", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--terminology-config", type=Path, default=None)
    parser.add_argument("--no-mount", action="store_true")
    parser.add_argument("--verify-engine-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("CANONICAL TMP TERMINOLOGY HARMONIZATION — PHASE 9A.2 VERSION 1")
    print("HUMAN-READABLE ENGLISH ONLY; ACCEPTED V1/V2 RECORDS IMMUTABLE")
    print("Script version:", VERSION)
    verify_engine()
    if args.verify_engine_only:
        return
    if drive is not None and not args.no_mount:
        drive.mount("/content/drive")

    input_dir = args.input_dir or args.project_dir / INPUT_RELATIVE
    output_dir = args.output_dir or args.project_dir / OUTPUT_RELATIVE
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"
    config_path = locate_config(args.terminology_config, args.project_dir)
    print("Input directory:", input_dir)
    print("Output directory:", output_dir)
    print("Terminology configuration:", config_path)

    crosswalk = load_crosswalk(config_path)
    accepted_validation, inputs = authenticate_phase9a1(input_dir)
    matrix_v2 = pd.read_csv(inputs["matrix"], dtype={"finding_id": str})
    cohort = pd.read_csv(inputs["cohort"], float_precision="round_trip")
    origin = pd.read_csv(inputs["origin"], float_precision="round_trip")
    matrix_v3, audit = harmonize_matrix(matrix_v2)
    coverage_v3 = build_coverage(matrix_v3)
    accepted_coverage = pd.read_csv(inputs["coverage"])
    require(coverage_v3.equals(accepted_coverage),
            "Evidence coverage changed during terminology harmonization")

    crosswalk_path = output_dir / "canonical_phase9a2_tmp_terminology_crosswalk_v1.csv"
    audit_path = output_dir / "canonical_phase9a2_occurrence_audit_v1.csv"
    matrix_path = output_dir / "canonical_integrated_evidence_matrix_v3.csv"
    markdown_path = output_dir / "canonical_integrated_evidence_matrix_v3.md"
    coverage_path = output_dir / "canonical_phase9a_evidence_coverage_v3.csv"
    note_path = output_dir / "canonical_phase9a2_terminology_note_v1.md"
    validation_path = output_dir / "canonical_phase9a2_terminology_validation_v1.json"
    inventory_path = output_dir / "canonical_phase9a2_terminology_inventory_v1.csv"

    crosswalk.to_csv(crosswalk_path, index=False, encoding="utf-8-sig")
    audit.to_csv(audit_path, index=False, encoding="utf-8-sig")
    matrix_v3.to_csv(matrix_path, index=False, encoding="utf-8-sig")
    coverage_v3.to_csv(coverage_path, index=False, encoding="utf-8-sig")
    markdown_path.write_text(build_markdown(matrix_v3, coverage_v3), encoding="utf-8")
    note_path.write_text(build_note(audit), encoding="utf-8")
    figure_paths = make_figures(cohort, origin, figure_dir)

    output_paths = [
        crosswalk_path, audit_path, matrix_path, markdown_path, coverage_path,
        note_path, *figure_paths,
    ]
    checks = {
        "accepted_phase9a1_validation_authenticated":
            sha256(inputs["validation"]) == EXPECTED_PHASE9A1_VALIDATION_SHA256,
        "accepted_matrix_v2_authenticated":
            sha256(inputs["matrix"]) == EXPECTED_MATRIX_V2_SHA256,
        "matrix_population_preserved": len(matrix_v3) == EXPECTED_MATRIX_ROWS,
        "finding_identity_and_order_preserved":
            matrix_v3["finding_id"].tolist() == matrix_v2["finding_id"].tolist(),
        "source_hashes_preserved":
            matrix_v3["source_sha256"].equals(matrix_v2["source_sha256"]),
        "expected_human_readable_replacements":
            int(audit["occurrence_count"].sum()) == EXPECTED_TARGET_OCCURRENCES,
        "deprecated_phrase_absent_from_matrix_v3": not any(
            matrix_v3[column].astype(str).str.contains(
                r"temporary agriculture", case=False, regex=True
            ).any() for column in TARGET_COLUMNS
        ),
        "technical_column_names_preserved":
            matrix_v3.columns.tolist() == matrix_v2.columns.tolist(),
        "evidence_coverage_preserved": coverage_v3.equals(accepted_coverage),
        "no_evidence_gaps": not matrix_v3["evidence_status"].eq("evidence_gap").any(),
        "no_causal_claims": int(matrix_v3["causal_claim_flag"].sum()) == 0,
        "diagnostic_records_preserved": int(
            matrix_v3["temporal_role"].eq("diagnostic").sum()
        ) == int(matrix_v2["temporal_role"].eq("diagnostic").sum()),
        "other_agriculture_label_protected": crosswalk.loc[
            crosswalk.term_id.eq("OAG_CLASS"), "replacement_scope"
        ].item() == "no_replacement",
    }
    require(all(checks.values()), "At least one Phase 9A.2 check failed")

    validation = {
        "validation_status": "PASS",
        "version": VERSION,
        "evidence_matrix_version": MATRIX_VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__).resolve()),
        "terminology_config": {
            "path": str(config_path), "sha256": sha256(config_path),
            "rows": len(crosswalk),
        },
        "accepted_inputs": {
            "phase9a1_validation": {
                "path": str(inputs["validation"]),
                "sha256": sha256(inputs["validation"]),
                "version": accepted_validation["version"],
            },
            "matrix_v2": {
                "path": str(inputs["matrix"]),
                "sha256": sha256(inputs["matrix"]), "rows": len(matrix_v2),
            },
            "cohort_summary": {
                "path": str(inputs["cohort"]), "sha256": sha256(inputs["cohort"]),
            },
            "origin_interval_summary": {
                "path": str(inputs["origin"]), "sha256": sha256(inputs["origin"]),
            },
        },
        "change_scope": {
            "preferred_class_label": "Temporary Crop",
            "preferred_running_prose": "temporary crops",
            "deprecated_phrase": "temporary agriculture",
            "human_readable_replacements": int(audit["occurrence_count"].sum()),
            "changed_findings": audit["finding_id"].tolist(),
            "stable_codes_preserved": PROTECTED_TECHNICAL_TOKENS,
            "numerical_recalculation": False,
            "accepted_v1_v2_files_modified": False,
        },
        "populations": {
            "matrix_v2_rows": len(matrix_v2), "matrix_v3_rows": len(matrix_v3),
            "crosswalk_rows": len(crosswalk), "occurrence_audit_rows": len(audit),
            "remaining_evidence_gaps": int(
                matrix_v3["evidence_status"].eq("evidence_gap").sum()
            ),
        },
        "checks": checks,
        "outputs": {
            str(path.relative_to(output_dir)): {
                "bytes": path.stat().st_size, "sha256": sha256(path)
            } for path in output_paths
        },
    }
    write_json(validation_path, validation)
    output_paths.append(validation_path)
    inventory = pd.DataFrame([
        {
            "relative_path": str(path.relative_to(output_dir)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        } for path in output_paths
    ])
    inventory.to_csv(inventory_path, index=False, encoding="utf-8-sig")

    print("PHASE 9A.2 TERMINOLOGY HARMONIZATION COMPLETE — VALIDATION PASS")
    print("Matrix rows:", f"{len(matrix_v3):,}")
    print("Human-readable replacements:", int(audit["occurrence_count"].sum()))
    print("Changed findings:", ", ".join(audit["finding_id"].tolist()))
    print("Validation:", validation_path)
    print("Inventory:", inventory_path)


if __name__ == "__main__":
    main()

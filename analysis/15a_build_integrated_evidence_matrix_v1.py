#!/usr/bin/env python3
"""Build the canonical Phase 9A integrated evidence matrix.

This stage authenticates accepted compact records and assembles a curated
claim-level evidence registry. It does not recompute scientific metrics,
perform new hypothesis tests, or infer causal relationships.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import Any

import pandas as pd

try:
    from google.colab import drive
except ImportError:  # pragma: no cover - outside Colab
    drive = None


VERSION = "phase9a-integrated-evidence-matrix-v1"
DEFAULT_PROJECT_DIR = Path(os.environ.get(
    "PHASE9_PROJECT_DIR",
    "/content/drive/MyDrive/Trabalho/Contabilidade",
))
DEFAULT_OUTPUT_RELATIVE = Path("spatial/phase9/evidence_matrix_v1")

REQUIRED_CLAIM_COLUMNS = [
    "finding_id", "research_question", "topic", "metric", "spatial_scope",
    "population", "temporal_scope", "temporal_role", "evidence_mode",
    "evidence_status", "main_result", "numeric_evidence",
    "robustness_status", "interpretation_boundary", "source_phase",
    "source_id", "source_locator", "manuscript_use", "causal_claim_flag",
]

CONTROLLED = {
    "research_question": {"RQ1", "RQ2", "RQ3", "RQ4", "RQ5"},
    "temporal_role": {"primary", "diagnostic", "both", "not_applicable"},
    "evidence_mode": {
        "descriptive", "global_inference", "local_inference", "sensitivity",
        "validation", "limitation", "gap",
    },
    "evidence_status": {"supported", "qualified", "evidence_gap"},
    "robustness_status": {
        "robust", "partially_robust", "sensitive", "not_assessed",
        "not_applicable",
    },
    "manuscript_use": {"main_result", "qualification", "limitation", "gap"},
}


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
    if hasattr(value, "item"):
        return json_ready(value.item())
    return value


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(json_ready(value), ensure_ascii=False, indent=2,
                   allow_nan=False) + "\n",
        encoding="utf-8",
    )


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def authenticate_sources(source_root: Path, manifest: pd.DataFrame) -> pd.DataFrame:
    require(not manifest.empty, "Source manifest is empty")
    require(not manifest["source_id"].duplicated().any(), "Duplicate source_id")
    require(not manifest["relative_path"].duplicated().any(),
            "Duplicate source relative_path")
    rows = []
    for record in manifest.to_dict("records"):
        path = source_root / str(record["relative_path"])
        require(path.is_file(), f"Missing accepted source: {path}")
        observed = sha256(path)
        require(observed == record["sha256"],
                f"Source hash mismatch: {record['relative_path']}")
        rows.append({
            **record,
            "bytes": path.stat().st_size,
            "observed_sha256": observed,
            "authenticated": True,
        })
    return pd.DataFrame(rows)


def validate_claims(claims: pd.DataFrame, sources: pd.DataFrame) -> dict[str, Any]:
    require(list(claims.columns) == REQUIRED_CLAIM_COLUMNS,
            "Claim schema differs from the frozen Phase 9A schema")
    require(len(claims) == 30, "Expected exactly 30 evidence statements")
    require(claims["finding_id"].is_unique, "Duplicate finding_id")
    require(claims["finding_id"].str.fullmatch(r"P9A\d{3}").all(),
            "Invalid finding_id format")
    require(claims.notna().all().all(), "Missing claim fields")
    for field, allowed in CONTROLLED.items():
        unknown = set(claims[field].astype(str)) - allowed
        require(not unknown, f"Unknown {field} values: {sorted(unknown)}")
    require(set(claims["causal_claim_flag"].astype(int)) == {0},
            "Causal claims are outside the accepted design")
    require(set(claims["source_id"]).issubset(set(sources["source_id"])),
            "A claim references an unauthenticated source")
    require(set(claims["research_question"]) == CONTROLLED["research_question"],
            "The five research questions are not all represented")
    gaps = claims[claims["evidence_status"].eq("evidence_gap")]
    require(set(gaps["research_question"]) == {"RQ1", "RQ2"},
            "Evidence gaps must explicitly retain RQ1 and RQ2")
    require(gaps["manuscript_use"].eq("gap").all(),
            "Evidence-gap rows must be manuscript gaps")
    require(claims.loc[claims["temporal_role"].eq("diagnostic"),
                       "temporal_scope"].eq("2020_2025").all(),
            "Diagnostic-only claims must use the 2020-2025 scope")
    return {
        "claim_rows": len(claims),
        "research_questions": int(claims["research_question"].nunique()),
        "supported": int(claims["evidence_status"].eq("supported").sum()),
        "qualified": int(claims["evidence_status"].eq("qualified").sum()),
        "evidence_gaps": int(claims["evidence_status"].eq("evidence_gap").sum()),
        "causal_claims": int(claims["causal_claim_flag"].astype(int).sum()),
    }


def validate_numeric_sources(source_root: Path) -> dict[str, Any]:
    phase2 = pd.read_csv(
        source_root / "phase2/canonical_spatial_metrics_summary_v1.csv"
    )
    require(len(phase2) == 8, "Phase 2 summary must contain eight intervals")
    require(phase2["cell_count"].eq(24_889).all(), "Phase 2 cell count changed")
    require(phase2["diagnostic_interval"].sum() == 1,
            "Phase 2 diagnostic flag is invalid")
    require((phase2["replenishment_ha"] > phase2["consolidation_ha"]).all(),
            "The registered aggregate C-R direction is not reproduced")
    require(phase2["aggregate_cr_balance_index"].lt(0).all(),
            "Aggregate C-R index is not negative in every interval")

    phase3 = pd.read_csv(
        source_root / "phase3/canonical_comparable_map_distributions_v2.csv"
    )
    require(len(phase3) == 96, "Phase 3 distributions must contain 96 rows")
    require(phase3.groupby("metric").size().eq(8).all(),
            "Phase 3 metrics do not all contain eight intervals")

    phase7 = json.loads((
        source_root / "phase7/canonical_phase7_biome_validation_v1.json"
    ).read_text(encoding="utf-8"))
    require(phase7.get("validation_status") == "PASS",
            "Phase 7 validation is not accepted")

    phase8c = pd.read_csv(
        source_root / "phase8c/canonical_maup_robustness_assessment_v1.csv",
        encoding="utf-8-sig",
    )
    require(len(phase8c) == 6, "Phase 8C assessment population changed")
    require(phase8c["aggregate_component_pass"].all(),
            "A Phase 8C aggregate component no longer passes")
    require(phase8c["temporal_component_pass"].all(),
            "A Phase 8C temporal component no longer passes")
    require(int(phase8c["overall_prespecified_robustness_pass"].sum()) == 2,
            "Phase 8C overall assessment count changed")

    phase8d = pd.read_csv(
        source_root / "phase8d/canonical_maup_global_moran_assessment_v1.csv"
    )
    require(len(phase8d) == 6, "Phase 8D assessment population changed")
    require(int(phase8d["sign_failed"].sum()) == 0,
            "Phase 8D sign preservation changed")
    require(int(phase8d["significance_failed"].sum()) == 0,
            "Phase 8D significance preservation changed")
    require(int(phase8d["magnitude_failed"].sum()) == 2,
            "Phase 8D window-level magnitude failure count changed")
    require(int(phase8d["temporal_failed"].sum()) == 8,
            "Phase 8D temporal failure count changed")

    phase8e = pd.read_csv(
        source_root / "phase8e/canonical_maup_hh_robustness_assessment_v1.csv"
    )
    require(len(phase8e) == 30, "Phase 8E assessment population changed")
    require(int(phase8e["overall_prespecified_robustness_pass"].sum()) == 21,
            "Phase 8E overall pass count changed")
    by_metric = phase8e.groupby("metric")[
        "overall_prespecified_robustness_pass"
    ].sum().astype(int).to_dict()
    expected = {
        "consolidation_density_per_10kha": 3,
        "replenishment_density_per_10kha": 6,
        "nat_tmp_density_per_10kha": 0,
        "net_cr_balance_density_per_10kha": 6,
        "cr_balance_index": 6,
    }
    require(by_metric == expected, "Phase 8E metric-level decisions changed")

    return {
        "phase2_intervals": len(phase2),
        "phase3_distribution_rows": len(phase3),
        "phase7_validation_status": phase7["validation_status"],
        "phase8c_overall_passes": int(
            phase8c["overall_prespecified_robustness_pass"].sum()
        ),
        "phase8d_sign_failures": int(phase8d["sign_failed"].sum()),
        "phase8d_significance_failures": int(
            phase8d["significance_failed"].sum()
        ),
        "phase8e_overall_passes": int(
            phase8e["overall_prespecified_robustness_pass"].sum()
        ),
        "phase8e_passes_by_metric": by_metric,
    }


def build_coverage(claims: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for rq, frame in claims.groupby("research_question", sort=True):
        rows.append({
            "research_question": rq,
            "evidence_rows": len(frame),
            "supported_rows": int(frame["evidence_status"].eq("supported").sum()),
            "qualified_rows": int(frame["evidence_status"].eq("qualified").sum()),
            "evidence_gap_rows": int(
                frame["evidence_status"].eq("evidence_gap").sum()
            ),
            "descriptive_rows": int(frame["evidence_mode"].eq("descriptive").sum()),
            "formal_inference_rows": int(
                frame["evidence_mode"].isin(
                    ["global_inference", "local_inference"]
                ).sum()
            ),
            "sensitivity_rows": int(frame["evidence_mode"].eq("sensitivity").sum()),
            "primary_or_both_rows": int(
                frame["temporal_role"].isin(["primary", "both"]).sum()
            ),
            "diagnostic_only_rows": int(
                frame["temporal_role"].eq("diagnostic").sum()
            ),
        })
    return pd.DataFrame(rows)


def build_markdown(claims: pd.DataFrame, coverage: pd.DataFrame) -> str:
    lines = [
        "# Canonical integrated evidence matrix — Phase 9A",
        "",
        "This document is generated from the authenticated Phase 9A claim registry.",
        "It separates accepted evidence, qualifications and explicit evidence gaps.",
        "No new scientific metric or hypothesis test is calculated in this stage.",
        "",
        "## Coverage",
        "",
        "| Research question | Evidence rows | Supported | Qualified | Gaps |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in coverage.to_dict("records"):
        lines.append(
            f"| {row['research_question']} | {row['evidence_rows']} | "
            f"{row['supported_rows']} | {row['qualified_rows']} | "
            f"{row['evidence_gap_rows']} |"
        )
    for rq, frame in claims.groupby("research_question", sort=True):
        lines.extend(["", f"## {rq}", ""])
        for row in frame.to_dict("records"):
            lines.extend([
                f"### {row['finding_id']} — {row['topic']}",
                "",
                row["main_result"],
                "",
                f"- **Evidence:** {row['numeric_evidence']}",
                f"- **Mode:** {row['evidence_mode']}; status: "
                f"{row['evidence_status']}",
                f"- **Temporal role:** {row['temporal_role']} "
                f"({row['temporal_scope']})",
                f"- **MAUP/robustness:** {row['robustness_status']}",
                f"- **Boundary:** {row['interpretation_boundary']}",
                f"- **Source:** Phase {row['source_phase']}, "
                f"`{row['source_relative_path']}` — {row['source_locator']}",
                "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    root = package_root()
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path,
                        default=root / "inputs/accepted_records")
    parser.add_argument("--claims", type=Path,
                        default=root / "config/phase9a_evidence_claims_v1.csv")
    parser.add_argument("--manifest", type=Path,
                        default=root / "config/phase9a_source_manifest_v1.csv")
    parser.add_argument("--project-dir", type=Path, default=DEFAULT_PROJECT_DIR)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--no-mount", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if drive is not None and not args.no_mount:
        drive.mount("/content/drive")

    output_dir = args.output_dir or args.project_dir / DEFAULT_OUTPUT_RELATIVE
    output_dir.mkdir(parents=True, exist_ok=True)

    print("CANONICAL INTEGRATED EVIDENCE MATRIX — PHASE 9A VERSION 1")
    print("CURATED CLAIMS; AUTHENTICATED SOURCES; NO NEW INFERENCE")
    print("Script version:", VERSION)
    print("Output directory:", output_dir)

    manifest = pd.read_csv(args.manifest, dtype=str)
    claims = pd.read_csv(args.claims, dtype=str, keep_default_na=False)
    claims["causal_claim_flag"] = claims["causal_claim_flag"].astype(int)

    sources = authenticate_sources(args.source_root, manifest)
    claim_summary = validate_claims(claims, sources)
    numeric_summary = validate_numeric_sources(args.source_root)

    source_lookup = sources.set_index("source_id")
    matrix = claims.copy()
    matrix["source_relative_path"] = matrix["source_id"].map(
        source_lookup["relative_path"]
    )
    matrix["source_sha256"] = matrix["source_id"].map(
        source_lookup["observed_sha256"]
    )
    matrix["source_authenticated"] = True
    matrix["evidence_matrix_version"] = VERSION

    coverage = build_coverage(matrix)
    gaps = matrix[matrix["evidence_status"].eq("evidence_gap")].copy()

    matrix_path = output_dir / "canonical_integrated_evidence_matrix_v1.csv"
    markdown_path = output_dir / "canonical_integrated_evidence_matrix_v1.md"
    coverage_path = output_dir / "canonical_phase9a_evidence_coverage_v1.csv"
    gaps_path = output_dir / "canonical_phase9a_open_evidence_gaps_v1.csv"
    source_path = output_dir / "canonical_phase9a_source_inventory_v1.csv"
    validation_path = output_dir / "canonical_phase9a_evidence_validation_v1.json"
    inventory_path = output_dir / "canonical_phase9a_output_inventory_v1.csv"

    matrix.to_csv(matrix_path, index=False, encoding="utf-8-sig")
    coverage.to_csv(coverage_path, index=False, encoding="utf-8-sig")
    gaps.to_csv(gaps_path, index=False, encoding="utf-8-sig")
    sources.to_csv(source_path, index=False, encoding="utf-8-sig")
    markdown_path.write_text(build_markdown(matrix, coverage), encoding="utf-8")

    checks = {
        "all_sources_authenticated": bool(sources["authenticated"].all()),
        "claim_population_exact": len(matrix) == 30,
        "claim_ids_unique": bool(matrix["finding_id"].is_unique),
        "all_research_questions_represented":
            matrix["research_question"].nunique() == 5,
        "evidence_gaps_explicit": set(gaps["research_question"]) == {"RQ1", "RQ2"},
        "no_causal_claims": int(matrix["causal_claim_flag"].sum()) == 0,
        "phase2_direction_reproduced": True,
        "phase7_validation_accepted":
            numeric_summary["phase7_validation_status"] == "PASS",
        "phase8c_counts_reproduced":
            numeric_summary["phase8c_overall_passes"] == 2,
        "phase8d_counts_reproduced":
            numeric_summary["phase8d_sign_failures"] == 0 and
            numeric_summary["phase8d_significance_failures"] == 0,
        "phase8e_counts_reproduced":
            numeric_summary["phase8e_overall_passes"] == 21,
        "diagnostic_extension_retained":
            matrix["temporal_scope"].str.contains("2020_2025").any() or
            matrix["temporal_role"].isin(["both", "diagnostic"]).any(),
    }
    require(all(checks.values()), "At least one Phase 9A validation check failed")

    validation = {
        "validation_status": "PASS",
        "version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__).resolve()),
        "claims_config": {
            "path": str(args.claims),
            "sha256": sha256(args.claims),
        },
        "source_manifest": {
            "path": str(args.manifest),
            "sha256": sha256(args.manifest),
            "sources": len(sources),
        },
        "claim_summary": claim_summary,
        "numeric_source_checks": numeric_summary,
        "design_boundaries": {
            "new_metrics_computed": False,
            "new_hypothesis_tests": False,
            "causal_inference": False,
            "primary_period": "1985-2020",
            "diagnostic_extension": "2020-2025 included and flagged",
            "canonical_grid_remains_primary": True,
        },
        "checks": checks,
        "outputs": {
            matrix_path.name: {"rows": len(matrix), "sha256": sha256(matrix_path)},
            markdown_path.name: {"sha256": sha256(markdown_path)},
            coverage_path.name: {"rows": len(coverage), "sha256": sha256(coverage_path)},
            gaps_path.name: {"rows": len(gaps), "sha256": sha256(gaps_path)},
            source_path.name: {"rows": len(sources), "sha256": sha256(source_path)},
        },
    }
    write_json(validation_path, validation)

    inventory_rows = []
    for path in [matrix_path, markdown_path, coverage_path, gaps_path,
                 source_path, validation_path]:
        inventory_rows.append({
            "relative_path": path.name,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    pd.DataFrame(inventory_rows).to_csv(
        inventory_path, index=False, encoding="utf-8-sig"
    )

    print("PHASE 9A EVIDENCE MATRIX COMPLETE — VALIDATION PASS")
    print("Evidence statements:", f"{len(matrix):,}")
    print("Authenticated sources:", f"{len(sources):,}")
    print("Explicit evidence gaps:", f"{len(gaps):,}", "(RQ1 and RQ2)")
    print("Validation:", validation_path)
    print("Inventory:", inventory_path)


if __name__ == "__main__":
    main()

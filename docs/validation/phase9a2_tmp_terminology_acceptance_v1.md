# Phase 9A.2 — TMP terminology harmonization acceptance

## Status

**PASS — Phase 9A.2 is accepted and may be registered as complete.**

The execution used `phase9a2-tmp-terminology-harmonization-v1` and produced the
terminology-harmonized evidence matrix v3. The accepted Phase 9A v1 and Phase
9A.1 v2 records were not modified.

## Authentication

The execution ZIP contains all ten expected files: nine products listed in the
inventory and the inventory itself. Every listed file exists, and every byte
count and SHA-256 digest agrees with
`canonical_phase9a2_terminology_inventory_v1.csv`.

The executed script and terminology configuration match the implementation
package:

| Item | SHA-256 |
|---|---|
| `15d_harmonize_tmp_terminology_v1.py` | `395a7328fc49c336745ed90f6db4cdd5be0d949bb77b64eb115e2c1ed1273d3f` |
| `phase9a2_tmp_terminology_crosswalk_v1.csv` | `877cfb6ea0760e7ede7ca17b36d4968f1f40dd6ee0b9b169e300528e11c123d1` |

The procedure authenticated the frozen Phase 9A.1 validation record, matrix
v2, fixed-cohort summary, and PAS→TMP origin summary before generating any
derivative file.

## Differential review of matrix v3

The v2 and v3 matrices both contain 35 findings in the same order. All 35
`finding_id` values, research-question assignments, evidence statuses,
robustness statuses, temporal roles, causal-claim flags, source paths, and
source hashes are preserved.

The differential audit found only the authorized changes:

- the `evidence_matrix_version` field changed in all 35 rows;
- four human-readable fields changed across P9A031, P9A033, P9A034, and
  P9A035;
- those four fields contain five occurrences of the deprecated phrase because
  P9A033 reports Amazon and Cerrado separately;
- every occurrence of `temporary agriculture` in the current matrix was
  replaced by `temporary crops`;
- no numerical value or analytical conclusion changed.

The matrix retains zero evidence gaps and zero causal claims. Diagnostic
records are unchanged. `TMP`, `NAT→TMP`, `PAS→TMP`, `nat_tmp_*`, `pas_tmp_*`,
and `tmp_*` remain stable technical notation. **Other Agriculture** remains a
separate protected class.

## Figures

Both figures were inspected visually. They are complete and legible. Figure 1
uses **Temporary Crop** as the class label, and Figure 2 uses **temporary
crops** in running prose. The plots retain the 2020–2025 diagnostic marker and
the accepted values from the Phase 9A.1 compact summaries.

## Accepted products

- `canonical_integrated_evidence_matrix_v3.csv`
- `canonical_integrated_evidence_matrix_v3.md`
- `canonical_phase9a_evidence_coverage_v3.csv`
- `canonical_phase9a2_tmp_terminology_crosswalk_v1.csv`
- `canonical_phase9a2_occurrence_audit_v1.csv`
- `canonical_phase9a2_terminology_note_v1.md`
- `canonical_phase9a2_terminology_validation_v1.json`
- `canonical_phase9a2_terminology_inventory_v1.csv`
- `figures/fig01_fixed_1985_pasture_cohort_composition_v2.png`
- `figures/fig02_pas_tmp_origin_composition_v2.png`

The preferred source for new English-language synthesis and manuscript text is
matrix v3. Matrices v1 and v2 remain immutable provenance records.


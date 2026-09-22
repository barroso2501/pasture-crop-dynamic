# Phase 9A — validation of the integrated evidence matrix

## Acceptance status

**Status: PASS — accepted as the immutable Phase 9A v1 synthesis record.**

The Phase 9A execution produced the complete set of seven expected outputs. The
validation record reports `PASS`; every file listed in the output inventory is
present and its SHA-256 digest and byte size agree with the inventory. The
curated claims configuration, source manifest, and execution script also match
the hashes recorded by the run.

Phase 9A v1 is a synthesis product. It does not introduce new statistical
inference. Its purpose is to connect previously accepted results to the five
research questions while preserving their original qualifications,
sensitivity findings, diagnostic-period flags, and inferential boundaries.

## Population and structural checks

The accepted matrix contains 30 unique evidence statements and 23 fields.
Every research question is represented:

| Research question | Statements |
|---|---:|
| RQ1 | 1 |
| RQ2 | 1 |
| RQ3 | 2 |
| RQ4 | 18 |
| RQ5 | 8 |
| **Total** | **30** |

Evidence status is distributed as 21 `supported`, 7 `qualified`, and 2
`evidence_gap`. The two gaps are explicit records rather than missing rows.
There are no causal claims. The diagnostic interval 2020–2025 remains included
and identified wherever applicable.

The source inventory contains 16 authenticated accepted records from Phases
2–8 and the investigation plan. No unauthenticated source contributes to a
statement. The execution reproduces the expected Phase 2 direction and the
accepted Phase 7 and Phase 8C–8E result populations.

## Substantive review of all 30 statements

Each row was checked against the cited accepted record, including the stated
evidence status, robustness status, intended manuscript use, and interpretation
boundary.

| IDs | Substantive conclusion | Review decision |
|---|---|---|
| P9A001 | RQ1 lacked a fixed-1985-pasture cohort result at the time of Phase 9A. | Accepted as an explicit historical gap. |
| P9A002 | RQ2 lacked an age-attributed decomposition of pasture-to-cropland conversion. | Accepted as an explicit historical gap. |
| P9A003–P9A004 | The detected-pasture share in high-magnitude NAT→TMP cells is valid but does not establish direct pixel pathways; absence of detected pasture is not proof of direct conversion. | Accepted with the recorded qualification and limitation. |
| P9A005–P9A011 | The national balance direction, high-magnitude cohort, temporal concentration, center displacement, regional contrasts, persistence, and reversals agree with the accepted Phase 2 and Phase 4 records. | Accepted. |
| P9A012–P9A017 | Global and local spatial autocorrelation statements, HH persistence, overlap, and BH/BY sensitivity agree with the accepted Phase 5 and Phase 6 records. | Accepted with the stated multiplicity and trend-test boundaries. |
| P9A018–P9A021 | Biome compositions, trajectories, HH contributions, and boundary sensitivity agree with the accepted Phase 7 record. | Accepted. |
| P9A022–P9A029 | MAUP distributional, temporal, global-Moran, and HH-overlap conclusions agree with the accepted Phase 8C–8E records. Statements marked `sensitive` correctly report supported evidence of sensitivity rather than failed evidence. | Accepted. |
| P9A030 | The synthesis is descriptive and associational and does not identify causal effects. | Accepted as the governing inferential boundary. |

No row requires rejection, recalculation, or reclassification. In particular,
P9A027 is intentionally `supported` while its robustness status is `sensitive`:
the supported finding is that the outcome changes under the prespecified
spatial sensitivity test.

## Treatment of the two evidence gaps

P9A001 and P9A002 were valid open gaps when Phase 9A v1 was executed. Phase
9A.1 subsequently resolved them with the fixed 1985 pasture cohort and the
age-attributed conversion decomposition. This later resolution does not justify
editing the accepted v1 matrix in place. Provenance requires retaining:

- Phase 9A v1: 30 statements and two explicit gaps;
- Phase 9A.1: the superseding gap-resolution record with the additional
  evidence and no remaining RQ1/RQ2 gaps.

## Terminology note and Phase 9A.2

Some historical records use **temporary agriculture** as the English rendering
of Portuguese *agricultura temporária*. For an English-language audience, this
can incorrectly suggest that agriculture itself is temporary. The intended
class is annual or seasonal crops.

This is an editorial nomenclature issue, not a numerical or methodological
defect in Phase 9A v1. The accepted v1 files remain immutable. Phase 9A.2 will
introduce a controlled terminology crosswalk and use **temporary crops** as the
preferred English label while preserving the stable code `TMP` and the original
Portuguese definition.

## Files accepted

Summary outputs:

- `canonical_integrated_evidence_matrix_v1.csv`
- `canonical_integrated_evidence_matrix_v1.md`
- `canonical_phase9a_evidence_coverage_v1.csv`
- `canonical_phase9a_open_evidence_gaps_v1.csv`

Validation outputs:

- `canonical_phase9a_evidence_validation_v1.json`
- `canonical_phase9a_output_inventory_v1.csv`
- `canonical_phase9a_source_inventory_v1.csv`

The execution-only snapshots under `inputs/accepted_records/` are deliberately
excluded from the GitHub update because their canonical source records already
exist in the repository.


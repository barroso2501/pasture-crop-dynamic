# Phase 8E validation — MAUP HH-cluster robustness

- **Status:** PASS
- **Execution:** 2026-09-21
- **Script:** `analysis/14c_compare_maup_hh_clusters_v1.py`
- **Script version:** `phase8e-maup-hh-cluster-robustness-v1`
- **Script SHA-256:** `2666bd3c8e2e770325dc9a8f27e24c7d4ea98a1f5787c9f0fddc065f1e3406f5`

## Scope

Phase 8E evaluates whether the broad location, recurrence and persistence of
canonical BH-significant HH clusters are preserved on three alternative
hexagonal grids. It is a sensitivity analysis. It does not replace the
canonical Phase 6 Local Moran/LISA results.

The validation status concerns computational completeness and internal
consistency. A `PASS` does not assert that every substantive robustness
criterion passed.

## Frozen design

- five focal metrics;
- three alternative grids;
- eight intervals, including diagnostic 2020–2025;
- fixed-domain support fraction `>= 0.50`;
- 9,999 conditional permutations per map;
- BH at 5% as primary inference;
- BY at 5% as sensitivity inference;
- HH as the primary cluster class;
- interval agreement: Jaccard `>= 0.40` and overlap coefficient `>= 0.60`;
- temporal agreement: weighted Spearman `>= 0.70`, persistent-HH Jaccard
  `>= 0.40` and overlap coefficient `>= 0.60`;
- interval passes required: five of seven in 1985–2020 and six of eight in
  1985–2025.

## Structural validation

| Object | Expected | Observed | Result |
|---|---:|---:|---|
| Alternative Local Moran maps | 120 | 120 | PASS |
| Cell-map rows | 3,487,040 | 3,487,040 | PASS |
| Interval comparisons | 240 | 240 | PASS |
| Temporal comparisons | 60 | 60 | PASS |
| Primary assessments | 30 | 30 | PASS |

All engine reference checks passed. All bounded statistics remained within
their declared ranges, and the diagnostic interval was present and flagged.

## Crosswalk closure

| Alternative grid | Rows | Shared support (ha) | Relative closure error |
|---|---:|---:|---:|
| `hex10k_base` | 136,201 | 483,388,508.802 | `2.466e-16` |
| `hex20k_shift` | 93,843 | 472,684,218.796 | `2.522e-16` |
| `hex40k_base` | 67,245 | 472,204,812.003 | `1.262e-16` |

The crosswalks therefore close to numerical precision on the shared support.

## Primary substantive results

- 94 of 120 BH interval comparisons passed the location criterion;
- 26 of 30 BH temporal comparisons passed;
- 21 of 30 complete grid–metric–window assessments passed.

These are scientific results rather than validation failures. The nine failed
overall assessments are retained in the published tables.

## Independent review

The compact outputs supplied for review were checked independently. The
review confirmed:

- exact row counts and map populations;
- exact sum of class counts to 3,487,040 cell-map records;
- zero discrepancies when recomputing interval pass rules;
- zero discrepancies when recomputing temporal and overall assessment rules;
- matching SHA-256 values for all supplied CSV, JSON and PNG products;
- correct presence and legibility of the three figures.

The three alternative Local Moran cell-result Parquets were not included in
the transferred review material because of their size. Their identities and
execution-side hashes remain recorded in the canonical inventory. They were
therefore authenticated by the producing workflow but not independently
rehased during this review.

| External Parquet | Bytes | Recorded SHA-256 |
|---|---:|---|
| `alternative_local_moran_hex10k_base_v1.parquet` | 49,445,535 | `87ed0fa499819d473e2c6d7672e456fc7f53b60d1cbf495682ef5486c6a9544a` |
| `alternative_local_moran_hex20k_shift_v1.parquet` | 27,374,039 | `5cedc39823d13e5ff88410d09db233a1e5bfb5d4319a64f1289e9bd0370b66a2` |
| `alternative_local_moran_hex40k_base_v1.parquet` | 15,444,497 | `566b9748fd263e80088c10b3a24369a953d10d7b142d7577afdd1dc3c867f1a8` |

## Acceptance

Phase 8E is accepted. The implementation completed the prespecified tests,
preserved all sensitivity findings and provides sufficient compact evidence
for repository review. Phase 8 can be closed, with the canonical grid retained
as the primary analytical support.

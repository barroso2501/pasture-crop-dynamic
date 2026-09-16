# Validation of canonical local Moran/LISA outputs — Phase 6

- **Production status:** PASS
- **Execution:** 2026-09-16
- **Script version:** `phase6-local-moran-lisa-v1`
- **Script SHA-256:** `56d041f8357c403b492951ccec5887932038610e81f24b4cf37a5fd96fb66de8`
- **Interpretive status:** Accepted under Decisions 011 and 012

## Scope of review

The review examined the runtime validation record, design record, class and
biome summaries, persistence summary, adjacent-interval Jaccard table, five PNG
map series and the identity of the consolidated cell-level Parquet.

The compact tables were independently reconciled. The consolidated Parquet
and all five PNG files matched the SHA-256 identities recorded by the
production validation. The Parquet content was validated during production but
was not independently reread in this compact review.

## Authenticated inputs

| Input | SHA-256 |
|---|---|
| `canonical_spatial_metrics_panel_v1.parquet` | `8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c` |
| `canonical_contiguity_weights_v1.parquet` | `85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f` |
| `canonical_spatial_support_v1.parquet` | `22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc` |

## Population and graph checks

| Check | Result |
|---|---:|
| Canonical cells | 24,889 |
| Metrics | 5 |
| Intervals | 8 |
| Metric-interval maps | 40 |
| Cell-metric-interval rows | 995,560 |
| Cell-metric persistence rows | 124,445 |
| Directed graph links | 134,906 |
| Undirected graph links | 67,453 |
| Complete-domain islands | 163 |
| Unsupported conditional rows | 38,168 |
| Island rows across all maps | 6,384 |

Every map reconciled to 24,889 cells. Unsupported rows matched the changing
support of `cr_balance_index`; no undefined ratio was counted as zero. Class
counts by primary biome reproduced the domain-level class counts. Equal-area
cell footprints reconciled within floating-point precision.

## Inference checks

The engine checks for BH, BY, deterministic seeds, run length and PySAL
quadrant codes passed. BH correction was applied separately within each
metric-by-interval map. Islands had no test result and could not be declared
significant.

| Result | Cell-map records | Share of tested non-island records |
|---|---:|---:|
| Significant by BH | 168,860 | 17.76% |
| Significant by BY | 72,221 | 7.59% |

BY retained 42.77% of the BH-significant cell-map records. This difference is
material and requires sensitivity language for emphasized local clusters, but
it does not replace the prespecified BH classification.

## BH class reconciliation

| Class | Cell-map records |
|---|---:|
| HH | 52,867 |
| LL | 113,044 |
| HL | 497 |
| LH | 2,452 |
| Not significant | 788,532 |
| Not applicable | 38,168 |

The four significant classes sum exactly to 168,860. LL prevalence is strongly
affected by spatially clustered zero and near-zero values in the absolute
metrics and cannot be read as process concentration.

## Temporal-summary checks

The Jaccard table contained exactly 70 comparisons: five metrics, two focal
classes and seven adjacent transitions. Ten rows correctly represented the
transition into the diagnostic interval. No comparison was missing or
duplicated.

The persistence summary contained exactly one row for each of the five metrics
and reconciled to 24,889 cells per metric. The primary window used seven
intervals and the full window included the 2020–2025 diagnostic extension.

## Visual review

All five map series displayed the expected BH classes, islands and conditional
support. The maps confirmed spatially coherent HH and LL structures and sparse
HL/LH outliers. `not_applicable` areas appeared only where expected for the
conditional balance index.

The period titles in the `replenishment_ha` and `net_cr_balance_ha` PNGs are
clipped or overlap the panels. This is a layout defect only. It does not affect
the underlying cell classifications, tables or acceptance of the statistical
outputs. These two figures must be rerendered before publication or final
repository use; no LISA recomputation is required.

## Acceptance

The Phase 6 statistical production is accepted. Decisions 011 and 012 govern
inference and interpretation. HH is the primary local result for absolute
process metrics; HH and LL are co-primary for signed and relative C–R balance
metrics. The only pending correction is the non-statistical layout of two map
series.

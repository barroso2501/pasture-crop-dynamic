# Canonical spatial-metrics validation: Phase 2

- **Status:** Passed
- **Validation date:** 2026-09-13
- **Method:** `docs/methods/canonical_spatial_metrics.md`
- **Analysis script:** `analysis/07_build_canonical_spatial_metrics.py`
- **Script SHA-256:** `a298880d53f436e63b5d91bdb28548f69060fd1aeda45ba4f50e4bf2b3dd2b70`
- **Validation record:** `outputs/validation/phase2_spatial_metrics/canonical_spatial_metrics_validation_v1.json`

## Scope

This validation covers input identity, the spatial many-to-one join, retention
of the integrated panel, core metric identities, denominator and missing-value
rules, occurrence-threshold nesting, C-R balance states, reproduction of
accepted interval totals, the fixed full-domain graph, and the inherited
active-cell subgraphs.

It does not validate map classes, Moran's I, LISA, temporal clusters, or
scientific interpretation of mapped patterns. Those analyses were not run in
Phase 2.

## Structural result

| Check | Result |
|---|---:|
| Output rows | 199,112 |
| Output columns | 211 |
| Distinct cells | 24,889 |
| Five-year intervals | 8 |
| Duplicate `cell_id`, `t0`, `t1` keys | 0 |
| Phase 1 spatial fields added | 34 |
| Spatial fields already present and checked | `GRID_ID`, `source_batch_id` |

The spatial join retained every integrated-panel row exactly once, added all
expected attributes, and did not change any upstream analytical value.

## Metric and accounting checks

| Identity | Maximum absolute difference |
|---|---:|
| Consolidation versus `flow_pas_tmp` | `0.0` ha |
| Replenishment versus `flow_nat_pas` | `0.0` ha |
| NAT-TMP endpoint versus `flow_nat_tmp` | `2.2352e-8` ha |
| Gross C-R activity | `0.0` ha |
| Net C-R balance | `0.0` ha |
| C-R balance index | `0.0` |
| Consolidation rate | `0.0` |
| Replenishment rate | `0.0` |

The maximum accepted-summary reconciliation difference was `5.58794e-9` ha,
well below the declared `2e-6` ha identity tolerance. The NAT-TMP difference
is the already accepted floating-point reconciliation value and does not
represent an accounting discrepancy.

## Defined and undefined balance support

| Support or state | Rows | Share of all rows |
|---|---:|---:|
| Defined C-R balance | 160,944 | 80.83% |
| Inactive; balance undefined | 38,168 | 19.17% |
| Replenishment-dominant | 131,523 | 66.05% |
| Mixed | 11,721 | 5.89% |
| Consolidation-dominant | 17,700 | 8.89% |

Among rows with defined balance, 81.72% are replenishment-dominant, 7.28% are
mixed, and 11.00% are consolidation-dominant. These pooled row counts describe
the data structure across all intervals; they are not substitutes for
interval-specific spatial analysis.

All inactive rows have a missing `cr_balance_index`, and all active rows have
a defined value. Relative metrics are missing exactly when their prescribed
denominators are unavailable.

## Activity-threshold sensitivity

The C-R active population changes as follows:

| Interval | `>1e-9` ha | `>0.1` ha | `>1.0` ha |
|---|---:|---:|---:|
| 1985-1990 | 17,626 | 17,584 | 17,388 |
| 1990-1995 | 18,713 | 18,675 | 18,469 |
| 1995-2000 | 19,453 | 19,421 | 19,217 |
| 2000-2005 | 20,394 | 20,368 | 20,174 |
| 2005-2010 | 20,642 | 20,609 | 20,415 |
| 2010-2015 | 20,860 | 20,821 | 20,595 |
| 2015-2020 | 21,206 | 21,156 | 20,925 |
| 2020-2025 diagnostic | 22,050 | 22,011 | 21,778 |

Relative to the primary rule, the `0.1` ha threshold removes at most 50 active
cells in an interval, or 0.24%; the `1.0` ha threshold removes at most 281, or
1.35%. The increase in cells with C-R activity is therefore not driven by
numerical traces or observations below 1 ha.

NAT-TMP occurrence is more sensitive to a 1 ha minimum: the maximum reduction
is 1,909 cells, or 17.96%. Nevertheless, all three thresholds show the same
broad temporal behavior, with increasing occurrence through 2015-2020 and a
lower count in the diagnostic 2020-2025 interval. This sensitivity must remain
visible in subsequent mapping and classification.

Occurrence is not area or intensity. The increasing number of active C-R cells
therefore cannot yet be interpreted as increasing total activity, geographic
movement, or clustering.

## Conditional C-R graph

| Interval | Active cells | Active share | Edges | Components | Islands | Largest component |
|---|---:|---:|---:|---:|---:|---:|
| 1985-1990 | 17,626 | 70.82% | 46,479 | 265 | 163 | 16,694 |
| 1990-1995 | 18,713 | 75.19% | 49,778 | 253 | 157 | 17,631 |
| 1995-2000 | 19,453 | 78.16% | 52,034 | 262 | 165 | 18,344 |
| 2000-2005 | 20,394 | 81.94% | 55,120 | 220 | 135 | 19,297 |
| 2005-2010 | 20,642 | 82.94% | 55,936 | 195 | 110 | 19,594 |
| 2010-2015 | 20,860 | 83.81% | 56,551 | 242 | 135 | 19,727 |
| 2015-2020 | 21,206 | 85.20% | 57,621 | 246 | 152 | 20,521 |
| 2020-2025 diagnostic | 22,050 | 88.59% | 59,914 | 257 | 151 | 21,366 |

Active and inactive populations sum to 24,889 in every interval. All edges
are inherited from the accepted complete-domain shared-edge graph, and no
artificial link was introduced. The largest component contains 94.2%-96.9% of
active cells, while isolated active cells remain explicit.

The changing conditional population means that future interval-specific
Moran's I values for `cr_balance_index` will not be strictly comparable to
complete-domain statistics or to one another without these support diagnostics.

## Fixed-graph reconciliation

| Check | Result |
|---|---:|
| Full-graph nodes | 24,889 |
| Undirected edges | 67,453 |
| Directed weight rows | 134,906 |
| Degree mismatches | 0 |
| Component-ID mismatches | 0 |
| Component-size mismatches | 0 |
| Island-flag mismatches | 0 |
| Maximum row-weight sum difference | `0.0` |
| Maximum individual-weight difference | `0.0` |

## Output identity

| Output | Dimensions | SHA-256 |
|---|---:|---|
| `canonical_spatial_metrics_panel_v1.parquet` | 199,112 × 211 | `8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c` |
| `canonical_spatial_metrics_summary_v1.csv` | 8 × 38 | `4d9a4ee8d9fefa5e281be3a765e20509756c7bb29f86046aaf6d87a1b9314bdf` |
| `canonical_cr_balance_active_subgraph_nodes_v1.parquet` | 160,944 × 9 | `ec9fda1818f43dedb53fd3a5e597d1837ad92bcf55350203c8d5d79232219c50` |
| `canonical_cr_balance_active_subgraph_summary_v1.csv` | 8 × 15 | `cf3fa7142b192538f4b71cdda3fbefd28c5927e36f536d5136ed0f747a621f0b` |
| `canonical_spatial_metrics_validation_v1.json` | validation record | `9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8` |

The two Parquet outputs remain in
`MyDrive/Trabalho/Contabilidade/spatial/phase2`. Their hashes, dimensions, and
paths are retained in the validation record; they are not committed to GitHub.

## Acceptance

All 13 predefined checks in the validation JSON are `true`. Phase 2 is
accepted without reprocessing and without a new methodological decision.

The increasing spatial occurrence of C-R activity is a validated descriptive
quantity but not yet a spatial conclusion. Phase 3 is authorized to calculate
pooled, fixed map limits from the seven primary intervals and to produce
comparable maps while keeping 2020-2025 visibly diagnostic.

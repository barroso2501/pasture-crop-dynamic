# NAT-to-TMP within-interval trajectory validation: 2005-2010

- **Status:** Passed
- **Validation date:** 2026-09-12
- **Method:** `docs/methods/within_interval_nat_tmp_trajectories.md`
- **Decision:** `docs/decisions/006_canonical_within_interval_trajectory_analysis.md`
- **Pilot script:** `gee/04a_reprocess_nat_tmp_trajectory_2005_2010_full_domain.js`

## Purpose

This validation establishes that the canonical within-interval trajectory
analysis can decompose the complete 2005-2010 `NAT->TMP` endpoint flow by
annual evidence of planted pasture during 2006-2009.

The validation concerns computational integrity, partition closure, temporal
rule consistency, and agreement with the canonical stock-and-flow panel. The
reported areas are processing diagnostics at this stage, not final manuscript
conclusions or a thematic-accuracy assessment of MapBiomas classifications.

## Canonical inputs

| Role | Source |
|---|---|
| Annual land cover | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3` |
| Canonical grid | `projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3` |
| Class definitions and spatial constants | `config/constants.js` |
| Interval | 2005-2010 |
| Intermediate years | 2006, 2007, 2008, 2009 |
| Cells | 24,889 |
| Output version | `canonical-nat-tmp-trajectory-v1` |

The pasture-age product is not used in this analysis.

## Execution record

| Field | Value |
|---|---|
| Task | `canonical_nat_tmp_trajectory_2005_2010_full_v1` |
| Task ID | `GM52H5ZMLAQ7HOQTQTFKFF6U` |
| Status | Completed, attempt 1 |
| Start | 2026-09-11 21:57:19, UTC-03:00 |
| Runtime | 7 minutes |
| Priority | 100, default |
| Batch compute usage | 461,640.1875 EECU-seconds |
| Output file | `canonical_nat_tmp_trajectory_2005_2010_full_v1.csv` |

## Structural validation

| Check | Result |
|---|---:|
| Rows | 24,889 |
| Columns | 28 |
| Distinct `cell_id` values | 24,889 |
| Duplicate `cell_id` values | 0 |
| Distinct `GRID_ID` values | 24,889 |
| Duplicate `GRID_ID` values | 0 |
| Rows containing missing values | 0 |
| Area values below `-1e-9` ha | 0 |

All rows contain the expected interval metadata: `t0 = 2005`, `t1 = 2010`,
`interval = 2005_2010`, intermediate years `2006,2007,2008,2009`, and
`diagnostic_interval = 0`.

## Partition and subset validation

| Identity or relationship | Maximum absolute residual (ha) | Rows above `1e-9` ha |
|---|---:|---:|
| Endpoint observation partition | 0 | 0 |
| Number-of-pasture-years partition | `9.094947e-13` | 0 |
| Any-pasture partition | `1.023182e-12` | 0 |
| Two-or-more-years partition | `1.136868e-13` | 0 |
| Consecutive-two-years partition | `5.684342e-14` | 0 |

No row violated the required nesting:

```text
consecutive two-year pasture
    <= two-or-more pasture years
    <= any intermediate pasture
    <= all intermediate years observed
    <= NAT->TMP endpoint
```

## Reconciliation with canonical stock-and-flow accounting

The trajectory-derived endpoint was compared cell by cell with `flow_nat_tmp`
from `canonical_stock_flow_2005_2010_full_v1.csv`.

| Check | Result |
|---|---:|
| Matched `cell_id` values | 24,889 |
| Unmatched identifiers | 0 |
| Maximum absolute difference | `1.818989e-12` ha |
| Differences above `2e-6` ha | 0 |
| Endpoint total in each result | 945,225.118068 ha |

The trajectory analysis therefore decomposes exactly the same endpoint
population as the accepted stock-and-flow accounting. It does not create,
remove, or reassign endpoint flow.

## Intermediate observation support

| Component | Area (ha) | Share of endpoint | Cells with positive area |
|---|---:|---:|---:|
| All four intermediate years observed | 945,223.024454 | 99.9997785% | 8,799 |
| Incomplete intermediate support | 2.093614 | 0.0002215% | 4 |
| **Total `NAT->TMP` endpoint** | **945,225.118068** | **100%** | **8,799** |

The incompletely observed area is retained explicitly and is not assigned to
the no-pasture category. Its magnitude is negligible for this interval but the
same diagnostic must be preserved in all subsequent exports.

## Intermediate pasture-year distribution

The mutually exclusive year-count classes apply only where all four
intermediate observations are available.

| Number of intermediate pasture years | Area (ha) | Share of endpoint |
|---:|---:|---:|
| 0 | 864,851.302278 | 91.496860% |
| 1 | 3,774.843212 | 0.399359% |
| 2 | 38,609.257502 | 4.084663% |
| 3 | 25,472.737998 | 2.694886% |
| 4 | 12,514.883464 | 1.324011% |

## Detection-rule results

| Rule | Area (ha) | Share of endpoint | Cells with positive area |
|---|---:|---:|---:|
| At least one pasture year | 80,371.722176 | 8.502919% | 6,238 |
| At least two pasture years | 76,596.878964 | 8.103559% | 5,873 |
| At least two consecutive pasture years | 76,578.168989 | 8.101580% | 5,872 |
| Any pasture without a consecutive pair | 3,793.553187 | 0.401339% | — |

The consecutive-two-year component represents approximately 95.28% of the
area detected by the inclusive rule. Requiring persistence therefore reduces
the estimated share of the complete endpoint flow from 8.50% to 8.10% in this
interval. The difference between the two-or-more and consecutive-two-year
rules is only 18.710 ha.

These pilot results demonstrate that alternative persistence rules can be
reported without changing the endpoint accounting. Selection of the primary
scientific rule remains pending until all intervals have been processed.

## Diagnostic comparison with the historical analysis

The historical `pentefino_2005_2010.csv` reported:

| Processing | `NAT->TMP` endpoint (ha) | Any intermediate pasture (ha) | Share |
|---|---:|---:|---:|
| Historical | 854,480.076838 | 117,041.858816 | 13.6974% |
| Canonical | 945,225.118068 | 80,371.722176 | 8.5029% |

The historical and canonical results are not expected to be identical because
the historical workflow used the preliminary `classification-ft` source, the
21,869-cell historical grid, a generic 30-m scale, and positive-flow filtering.

A diagnostic comparison restricted to the 8,599 positive cell identifiers
shared by both outputs produced:

| Processing on shared identifiers | Endpoint (ha) | Any pasture (ha) | Share |
|---|---:|---:|---:|
| Historical | 851,505.400488 | 116,676.545728 | 13.7024% |
| Canonical | 845,427.282345 | 70,659.244488 | 8.3578% |

Because the difference remains large among shared identifiers while endpoint
area changes comparatively little, domain reconstruction alone does not
explain the lower canonical pasture share. The evidence is consistent with a
substantial effect of the change in annual coverage source or related raster
processing, especially in intermediate-year pasture classifications. This is
an inference, not a completed causal decomposition.

The historical result is retained as provenance and must not be treated as a
target that the canonical workflow is required to reproduce. The comparison
will be revisited after all eight canonical intervals are available.

## Acceptance and next step

The 2005-2010 full-domain pilot passes all structural, accounting, partition,
subset, observation-support, and external-reconciliation checks. It is
accepted as the implementation reference for the remaining seven intervals.

Subsequent exports must use the same canonical inputs, complete-cell
population, field schema, temporal rules, and validation tolerances. After all
intervals are complete, they will be assembled into a balanced trajectory
panel and jointly evaluated before any Moran, MAUP, or substantive spatial
analysis is initiated.

# Comparable interval map classes

- **Status:** Phase 3A diagnostic implemented; final share-limit refit pending
- **Decision reference:** `docs/decisions/008_minimum_support_for_nat_tmp_share_maps.md`
- **Analysis script:** `analysis/08a_build_comparable_map_classes.py`
- **Diagnostic script SHA-256:** `01862e215480b897c1ee83eb3a9e40c9b9c67b385c83ec569a894080fd854b01`
- **Validation:** `docs/validation/canonical_map_classes_phase3a.md`

## Purpose

Comparable classes provide a fixed visual and categorical scale for following
the same process among five-year intervals. Limits are calculated once from
the pooled distribution of the seven primary intervals and then applied
unchanged to all primary maps and the diagnostic 2020-2025 map.

Interval-specific quantiles are not used because they would assign the same
map color to different numerical magnitudes through time.

## Temporal fitting population

The fitting population contains 174,223 observations:

```text
24,889 cells × 7 primary intervals, 1985-1990 through 2015-2020
```

The 24,889 observations from 2020-2025 are excluded from limit estimation.
They will be classified using the accepted frozen limits and identified as
diagnostic.

## Positive magnitudes and intensities

For nonnegative metrics, undefined values and observed zeros are separated
before positive quantiles are calculated. Positive values use:

```text
low:       > 0 through pooled positive median
moderate:  > median through pooled positive p90
high:      > pooled positive p90
```

The Phase 3A diagnostic accepted this rule and the following preliminary
limits for ten metrics:

| Metric | Positive median | Positive p90 |
|---|---:|---:|
| `consolidation_ha` | 70.5453 ha | 937.5192 ha |
| `consolidation_rate_initial_pasture` | 0.018789 | 0.255981 |
| `replenishment_ha` | 311.6753 ha | 1,849.4996 ha |
| `replenishment_rate_initial_native` | 0.028805 | 0.165354 |
| `nat_tmp_endpoint_ha` | 13.3531 ha | 357.7932 ha |
| `nat_tmp_intensity_initial_native` | 0.001690 | 0.034065 |
| `nat_tmp_pas_any_ha` | 2.6639 ha | 47.7323 ha |
| `nat_tmp_pas_consecutive2_ha` | 2.7347 ha | 48.1909 ha |

The remaining two accepted class specifications are not positive-quantile
pairs:

- `net_cr_balance_ha` uses symmetric replenishment and consolidation classes
  based on the pooled absolute nonzero median (`348.9704` ha) and p90
  (`1,912.2785` ha); and
- `cr_balance_index` uses the fixed substantive boundaries `-1/3` and `1/3`,
  with inactivity retained separately.

## Trajectory shares

The preliminary limits calculated from every positive endpoint denominator
are rejected for mapping. They remain diagnostic evidence only.

Eligible cell-level share classification requires:

```text
nat_tmp_endpoint_ha > 0.001 × geometry_area_aea_ha
```

The eligible positive median and p90 will be recalculated using the seven
primary intervals. Cells without endpoint flow, cells with low denominator
support, eligible zero shares, and the three eligible positive magnitude
classes will remain distinct.

The support threshold does not remove any observation from absolute-area
accounting and does not redefine domain-level aggregate shares.

## Signed net balance

`net_cr_balance_ha` is classified symmetrically with respect to zero:

```text
replenishment high
replenishment moderate
replenishment low
zero
consolidation low
consolidation moderate
consolidation high
```

The two magnitude breaks are applied identically to the negative and positive
sides. This preserves direction while making consolidation and replenishment
magnitudes visually comparable.

## Undefined values and observed zeros

- An undefined rate or intensity means its process-specific initial stock is
  absent.
- An undefined trajectory share means there is no `NAT→TMP` endpoint flow.
- A low-support trajectory share has a positive endpoint denominator at or
  below 0.1% of the cell area.
- An eligible zero share means endpoint conversion occurred but the specified
  intermediate pasture trajectory was not detected.
- An inactive C-R balance means neither consolidation nor replenishment was
  observed; it is not a numerical balance of zero.

These states must receive separate codes, legend entries, and counts.

## Phase 3A and Phase 3B separation

Phase 3A writes class limits, interval distributions, class populations,
denominator-sensitivity summaries, and a validation JSON. It does not create
maps.

Phase 3B may begin only after the final Phase 3A rerun implements Decision 008
and passes its acceptance criteria. Phase 3B will use the recorded limits
without recalculating them from map-specific subsets.

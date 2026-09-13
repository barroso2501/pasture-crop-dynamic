# Decision 008: Minimum support for cell-level NAT-TMP trajectory shares

- **Status:** Accepted
- **Decision date:** 2026-09-13
- **Applies to:** Comparable maps and spatial analyses of cell-level
  `NAT→TMP` trajectory shares
- **Related plan:** `docs/planning/006_spatiotemporal_investigation_plan.md`

## Context

The two trajectory-share metrics divide an intermediate-pasture trajectory
area by the total `NAT→TMP` endpoint area in the same cell and interval:

```text
nat_tmp_pas_any_share_endpoint =
    nat_tmp_pas_any_ha / nat_tmp_endpoint_ha

nat_tmp_pas_consecutive2_share_endpoint =
    nat_tmp_pas_consecutive2_ha / nat_tmp_endpoint_ha
```

They are mathematically defined whenever `nat_tmp_endpoint_ha > 1e-9` ha.
That computational rule does not ensure that the denominator is large enough
for a stable cell-level proportional comparison.

The initial Phase 3A limits used every positive endpoint denominator. The
pooled positive 90th-percentile limits reached `0.966903` for any detected
pasture and `0.922762` for two consecutive pasture years. A prespecified
denominator-sensitivity analysis was therefore expanded from `0.1` and `1`
ha to `1`, `5`, `10`, `20`, and `50` ha.

The quantiles declined continuously as the denominator threshold increased.
No empirical plateau was observed within the tested range. The threshold is
therefore based on the spatial support of the analytical unit rather than on a
post hoc claim of quantile stabilization.

## Decision

Cell-level trajectory-share maps will require:

```text
nat_tmp_endpoint_ha > 0.001 × geometry_area_aea_ha
```

This is 0.1% of the complete cell area and is approximately 20 ha for the
canonical 20,000 ha hexagons. The relative rule will be calculated for each
cell rather than represented internally as a universal rounded 20 ha value.

The two positive-share class limits will be recalculated from eligible
observations in the seven primary intervals only:

```text
positive low:       > 0 through eligible pooled positive median
positive moderate:  > median through eligible pooled positive p90
positive high:      > eligible pooled positive p90
```

Every share map will preserve six distinct states:

1. no `NAT→TMP` endpoint flow: share not applicable;
2. positive endpoint flow at or below 0.1% of cell area: low denominator
   support;
3. eligible endpoint support and share equal to zero;
4. eligible positive share, low;
5. eligible positive share, moderate; and
6. eligible positive share, high.

Low-support observations remain in endpoint-area maps, trajectory-area maps,
occurrence counts, and complete accounting totals. The rule limits only their
use in cell-level proportional classification and subsequent numerical
spatial analysis of the shares.

Domain-level aggregate shares continue to use the complete accounted areas.
They will not be recomputed as an unweighted mean of eligible cell shares.

## Evidence

Across the seven primary intervals, 56,674 cell-interval observations contain
positive `NAT→TMP` endpoint flow. The approximate 20 ha diagnostic retained
24,303 observations and classified 32,371 as low support.

| Diagnostic result | Any pasture | Two consecutive pasture years |
|---|---:|---:|
| Endpoint area retained | 98.03% | 98.03% |
| Trajectory area retained | 94.83% | 95.02% |
| Complete aggregate share | 8.54% | 8.12% |
| Aggregate share above 20 ha | 8.26% | 7.87% |
| Positive median above 20 ha | 9.87% | 9.24% |
| Positive p90 above 20 ha | 57.07% | 55.41% |

The support rule removes a large number of cell-level ratios while retaining
nearly all endpoint area and most trajectory area. This demonstrates that
many observed ratios are attached to spatially residual flows. It does not
demonstrate that those pixels are classification errors.

## Alternatives considered

### Use every positive denominator

Rejected for spatial share classification. It gives a small number of pixels
the same inferential status as extensive endpoint flows and materially
inflates the upper distribution of unweighted cell shares.

### Use a 1 ha threshold

Rejected as primary support. One hectare is only 0.005% of a 20,000 ha cell
and remains too small for the intended cell-level spatial interpretation.

### Use a 50 ha threshold

Rejected as primary support. It retains only 29.19% of the positive endpoint
cell-interval observations and removes 4.70% of endpoint area and about
11.5%-11.9% of the trajectory area. It may remain a sensitivity check.

### Omit trajectory-share maps

Rejected. The shares answer a distinct compositional question that is not
represented by trajectory-area maps, provided denominator support is explicit.

## Consequences

- The two original share-limit rows in the Phase 3A diagnostic output are not
  canonical and must not be used by the mapping script.
- The other ten metric definitions and limits are unaffected by this decision.
- The Phase 3A script required revision and a successful rerun before Phase
  3B; this condition was subsequently satisfied by the `v2` implementation.
- Map legends and validation tables must distinguish `not applicable`, `low
  support`, and an eligible zero share.
- Temporal comparisons of cell shares use the same 0.1%-of-cell rule in every
  interval, including the diagnostic 2020-2025 extension.
- Sensitivity results at 1, 5, 10, 20, and 50 ha remain part of the validation
  record.

## Acceptance criteria for implementation

- the support threshold is calculated from each cell's AEA area;
- only seven primary intervals contribute to the recalculated share limits;
- 2020-2025 is classified with, but does not influence, the frozen limits;
- all six share-map states are mutually exclusive and exhaustive;
- cell counts and endpoint and trajectory areas reconcile before and after
  support classification; and
- the final class-limit record replaces the two rejected diagnostic rows.

## Implementation outcome

Decision 008 was implemented and validated on 2026-09-13 in map-class version
`canonical-comparable-map-classes-v2`. The cell-relative threshold ranged from
19.999197 to 20.000258 ha across the canonical grid. All six share states
closed exactly for every interval, and the 2020-2025 diagnostic interval was
excluded from limit fitting.

The final frozen positive-share limits are:

| Metric | Eligible positive median | Eligible positive p90 |
|---|---:|---:|
| `nat_tmp_pas_any_share_endpoint` | 0.098669 | 0.570658 |
| `nat_tmp_pas_consecutive2_share_endpoint` | 0.092363 | 0.554050 |

The implementation passed all 22 validation checks. Phase 3B is authorized to
consume `canonical_comparable_map_class_limits_v2.csv`; the preliminary `v1`
share limits remain diagnostic provenance and are not canonical inputs.

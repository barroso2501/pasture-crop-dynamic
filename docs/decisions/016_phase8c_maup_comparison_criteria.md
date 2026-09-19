# Decision 016 — Phase 8C MAUP comparison criteria

- **Status:** Accepted for implementation before Phase 8C result inspection
- **Date:** 2026-09-20
- **Applies to:** comparison of the canonical grid with `hex10k_base`,
  `hex20k_shift` and `hex40k_base`

## Purpose

Phase 8C evaluates whether central descriptive and temporal conclusions are
stable under alternative spatial scale and grid zoning. The canonical
approximately 20,000-ha grid remains the primary analysis. Alternative grids
are sensitivity tests and cannot replace or redefine the canonical result.

## Comparisons

| Alternative | Primary interpretation |
|---|---|
| `hex10k_base` | finer-scale sensitivity |
| `hex20k_shift` | zoning/origin sensitivity at approximately the same scale |
| `hex40k_base` | coarser-scale sensitivity |

No one-to-one cell join will be attempted because the spatial units are not
coincident.

## Metric comparability

Domain totals for consolidation, replenishment and endpoint `NAT → TMP` are
compared directly. Cell-level absolute areas are not directly comparable among
10,000-, 20,000- and 40,000-ha units. They are converted to hectares per
10,000 ha of analytical support before distributional comparison.

The bounded C–R balance index and the three initial-stock rates remain in their
native dimensionless scale. Undefined values remain undefined and their
support coverage is reported separately.

Spatial distributions are weighted by analytical support area. The primary
alternative-grid population requires at least 50% domain support. Thresholds
of 25% and 75% are retained as prespecified sensitivity analyses. Aggregate
domain totals continue to use all positive-support units.

## Temporal windows

Two parallel windows are required:

- `primary_1985_2020` — seven intervals;
- `full_observed_1985_2025` — eight intervals, including the flagged diagnostic
  extension.

The diagnostic interval cannot be omitted, but it cannot silently redefine the
primary-period conclusion.

## Prespecified criteria

### Aggregate values

- focal domain totals: relative difference no greater than `0.002`;
- aggregate rates and C–R index: absolute difference no greater than `0.02`;
- net C–R balance: absolute difference divided by canonical gross C–R activity
  no greater than `0.02`;
- sign of every aggregate metric preserved;
- C–R dominance class preserved for the aggregate balance index.

### Weighted distributions

- support-weighted two-sample KS distance no greater than `0.10`;
- absolute difference in defined-support fraction no greater than `0.05`.

The distributional comparison is conditional for metrics whose denominator or
activity support is undefined. A similar conditional distribution does not
substitute for agreement in the fraction of the landscape where the metric is
defined.

### Temporal configuration

- Spearman rank correlation at least `0.90`;
- maximum interval equal or displaced by no more than one quinquennium;
- minimum interval equal or displaced by no more than one quinquennium;
- sign sequence preserved;
- C–R dominance-class sequence preserved where applicable.

## Assessment rule

Each alternative grid receives separate primary and full-observed assessments.
An assessment is `stable_under_prespecified_criteria` only when all aggregate,
distributional and temporal criteria pass. Otherwise it is
`sensitive_for_at_least_one_criterion`.

A sensitivity result is a scientific outcome, not a validation failure. The
script must finish with `validation_status = PASS` when the calculation and
data checks succeed, even if one or more robustness criteria fail.

## Scope boundary

Phase 8C does not construct alternative-grid neighbor graphs and does not
calculate Global Moran, Local Moran/LISA or cluster overlap. These are reserved
for subsequent spatial-robustness stages after the descriptive comparison is
accepted.


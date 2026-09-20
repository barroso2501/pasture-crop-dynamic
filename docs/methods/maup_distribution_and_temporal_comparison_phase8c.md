# Phase 8C method — MAUP distribution and temporal comparison

## Purpose

Phase 8C tests whether central descriptive and temporal conclusions obtained on
the canonical approximately 20,000-ha grid remain stable under changes in
spatial scale and lattice origin. The canonical grid remains the primary
analysis. The three alternative grids are sensitivity tests:

| Grid | Comparison represented |
|---|---|
| `hex10k_base` | finer spatial scale |
| `hex20k_shift` | changed lattice origin at approximately the canonical scale |
| `hex40k_base` | coarser spatial scale |

The stage compares non-coincident spatial partitions. It does not attempt a
one-to-one cell join or interpolate canonical values onto alternative units.

## Inputs

The accepted execution combines:

| Panel | Rows | SHA-256 |
|---|---:|---|
| canonical Phase 2 spatial metrics | 199,112 | `8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c` |
| Phase 8B alternative-grid metrics | 809,800 | `cdd5d4db2abb7648f8801694de93e6976d8073e271c12bd71b8c972b2a366313` |

The harmonized comparison panel therefore contains 1,008,912 records for four
grids and eight five-year intervals.

## Metric comparability

Domain totals are compared directly for consolidation, replenishment and
endpoint `NAT -> TMP`. Absolute cell areas are not directly comparable among
10,000-, 20,000- and 40,000-ha units. Before distributional comparison, they
are normalized as hectares per 10,000 ha of analytical support.

The following bounded or relative metrics retain their native scale:

- `cr_balance_index`;
- `consolidation_rate_initial_pasture`;
- `replenishment_rate_initial_native`;
- `nat_tmp_intensity_initial_native`.

Undefined conditional values remain undefined. Their analytical-support
coverage is compared explicitly and is not replaced by zero.

## Support populations and weights

Aggregate domain values use every positive-support unit. Cell-distribution
comparisons use support-area weighting so that cells clipped by the fixed
domain boundary do not receive the same influence as fully supported cells.

Three alternative-grid scopes are retained:

| Scope | Rule | Role |
|---|---|---|
| `primary_ge_50pct` | domain support fraction at least 0.50 | primary comparison |
| `sensitivity_ge_25pct` | domain support fraction at least 0.25 | lower-threshold sensitivity |
| `sensitivity_ge_75pct` | domain support fraction at least 0.75 | higher-threshold sensitivity |

The canonical comparison population is fixed and repeated across these scope
labels. The scope sensitivity therefore concerns alternative-grid boundary
units, not a redefinition of the canonical domain.

## Aggregate comparisons

For each alternative grid, interval and aggregate metric, the implementation
records canonical and alternative values, signed and absolute differences,
sign preservation and, for the aggregate C-R index, dominance-class
preservation.

Decision 016 prespecified the following limits:

- focal total relative difference no greater than `0.002`;
- aggregate rate or index absolute difference no greater than `0.02`;
- net C-R difference divided by canonical gross C-R activity no greater than
  `0.02`;
- sign preservation for every aggregate metric;
- C-R dominance-class preservation where applicable.

## Distribution comparisons

Eight cell-level metrics are compared by interval and support scope. Each
comparison reports:

- a support-weighted empirical distribution summary;
- support-weighted quantiles;
- weighted two-sample Kolmogorov-Smirnov distance;
- the fraction of analytical support for which a conditional metric is
  defined.

The distribution criterion passes only when both conditions hold:

```text
weighted KS distance <= 0.10
absolute defined-support-fraction difference <= 0.05
```

The coverage condition matters independently of the conditional distribution.
Two grids can have similar values where a metric is defined while assigning
different fractions of the landscape to defined and undefined support.

## Temporal comparisons

Eight aggregate metrics are evaluated in two windows:

- `primary_1985_2020`, containing seven intervals;
- `full_observed_1985_2025`, containing all eight intervals.

The 2020-2025 interval is included and flagged as diagnostic. It cannot be
silently substituted for the primary-period inference.

The temporal criterion requires:

- Spearman rank correlation of at least `0.90`;
- peak and trough displacement of no more than one interval;
- preservation of the sign sequence;
- preservation of the C-R dominance sequence where applicable.

## Assessment rule

Each grid receives one primary-period and one full-observed assessment. It is
classified as `stable_under_prespecified_criteria` only when every aggregate,
distributional and temporal comparison passes. Any failure produces
`sensitive_for_at_least_one_criterion`.

This classification is intentionally strict. A sensitivity finding is a
scientific result and does not imply a processing or validation failure.

## Implementation

Accepted script:

```text
analysis/14a_compare_maup_distributions_and_temporal_patterns.py
```

Script version:

```text
phase8c-maup-distribution-temporal-comparison-v1
```

SHA-256:

```text
18e2e9f347964ef52cf05d6c05e7373241ec5b06d9e3d37625888f1585a50720
```

The numerical criteria and assessment rule were frozen in Decision 016 before
inspection of the Phase 8C results.

## Scope boundary

Phase 8C evaluates aggregate values, cell distributions and temporal ordering.
It does not construct alternative-grid neighbor graphs, recalculate Global or
Local Moran statistics, or compare the geography of LISA clusters. Those
spatial-configuration tests remain a separate downstream component of the
MAUP evaluation.

# Decision 015 — Geometric support and total-comparison tolerance in Phase 8B

- **Status:** Accepted
- **Date:** 2026-09-19
- **Applies to:** Phase 8B MAUP core-metric extraction and validation
- **Supersedes:** the cross-grid near-equality check in validator revisions 1–3

## Context

Phase 8B extracts the same land-cover processes on three complete alternative
hexagonal lattices while holding the analytical footprint fixed as the union of
the 24,889 canonical cells. The alternative grids differ in nominal cell size
or lattice origin:

- `hex10k_base` — approximately 10,000 ha;
- `hex20k_shift` — approximately 20,000 ha with shifted origin;
- `hex40k_base` — approximately 40,000 ha.

Raster pixels at the exterior boundary are allocated through the Earth Engine
zonal reduction. Consequently, the sum of raster-supported area is expected to
be temporally invariant within a grid but need not be numerically identical
among grids with different boundaries. Requiring cross-grid equality at the
base outcome tolerance of `5e-6` conflated a geometric boundary effect with an
error in the measured processes.

## Decision

The Phase 8B validator will apply three separate support checks.

### 1. Temporal invariance within each grid

For each `grid_code`, the relative range of total raster-domain support across
the eight intervals must not exceed:

```text
1e-10
```

This is a strict reproducibility check because the analytical footprint and
common observation-support mask are fixed across time.

### 2. Agreement with the fixed vector domain

For every grid and interval, the relative difference between total raster
support and the fixed vector-domain area must not exceed:

```text
0.002  (0.2%)
```

The fixed vector-domain area is:

```text
497,776,400.44341594 ha
```

### 3. Bounded variation among alternative grids

Within an interval, the relative range of raster-domain support among the
three grids must not exceed:

```text
0.002  (0.2%)
```

The check retains a guard against material domain inconsistency without
requiring different raster partitions to have identical boundary allocation.

## Outcome-independent comparison tolerance

Aggregate alternative-grid process totals are compared with the accepted
canonical-grid totals. For each grid and interval, the effective relative
tolerance is:

```text
max(5e-6, grid-interval vector–raster support relative difference)
```

The absolute minimum tolerance remains `1.0 ha`. The geometric tolerance is
calculated without reference to consolidation, replenishment or `NAT → TMP`
values and therefore cannot be adjusted in response to the observed outcome.

The tolerance is calculated separately for each grid and interval. The grid
with the largest boundary discrepancy does not set a single global tolerance
for all alternatives.

## Common-mask requirement

Observed and unobserved endpoint areas must be derived from the same raster
support mask used for `raster_domain_support_ha`. Their per-cell partition must
close within `2e-6 ha`. Separate reductions with incompatible masks are not
accepted.

## Empirical verification

The accepted full execution produced:

| Check | Maximum observed value | Acceptance limit |
|---|---:|---:|
| Within-grid temporal support spread | `3.9618e-14` | `1e-10` |
| Cross-grid support spread | `6.2993e-6` | `0.002` |
| Vector–raster support difference | `0.000426549` | `0.002` |
| Cell-level observation-partition residual | below `2e-6 ha` | `2e-6 ha` |

All checks passed.

## Interpretation

This decision does not change the study footprint, process definitions,
canonical results or alternative-grid measurements. It separates three
different questions: temporal reproducibility, approximation of the fixed
vector footprint and harmless variation in raster boundary allocation.

The decision does not authorize outcome-specific tolerance tuning, reselection
of the domain, spatial interpolation of canonical cell values or omission of
the diagnostic 2020–2025 interval.


# Phase 6 method — local spatial association

## Purpose

Phase 6 locates significant local concentrations and spatial outliers after
the positive global Moran results of Phase 5. It evaluates five metrics over
eight intervals, including the flagged 2020–2025 diagnostic extension.

## Statistic and randomization

For each eligible cell, the implementation calculates the local Moran
statistic from the mean-centered, population-standardized metric and its
row-standardized spatial lag. Pseudo p-values are obtained from 9,999 PySAL
conditional randomizations with deterministic per-map seeds. `p_sim` follows
the `esda.Moran_Local` convention and measures extremeness relative to the
conditional simulated distribution.

Cells without neighbors are retained but cannot form a local association.
They receive `analysis_status=island`, no p/q value, and
`lisa_class=not_significant`. Undefined `cr_balance_index` cells receive
`analysis_status=unsupported` and `lisa_class=not_applicable`.

## Multiple testing and classification

BH-adjusted q-values are calculated among tested non-island cells separately
for each metric and interval. At `q_bh <= 0.05`, quadrants are classified:

| Class | Cell z-score | Spatial-lag z-score | Meaning |
|---|---:|---:|---|
| HH | positive | positive | high cell among high neighbors |
| LL | negative | negative | low cell among low neighbors |
| HL | positive | negative | high spatial outlier |
| LH | negative | positive | low spatial outlier |

Other tested cells are `not_significant`. BY q-values are retained only as a
conservative sensitivity result.

## Temporal and regional summaries

The primary persistence window is 1985–2020. The full window includes
2020–2025 and explicitly reports whether the diagnostic interval continues an
HH or LL episode. Persistence means at least two consecutive intervals in the
same significant HH or LL class. Adjacent-map stability is measured by the
Jaccard overlap of the HH and LL cell sets.

Class totals report both cell counts and complete-cell equal-area footprint.
The footprint is not the process area. The separate `metric_value_sum` field
aggregates the analyzed metric and must be interpreted according to its unit.
Biome summaries use the existing primary-biome label while preserving the
fractional biome fields in the canonical spatial support. Boundary-cell
sensitivity remains a downstream interpretation check.

## Reproducibility

The production engine is pinned to `esda 2.7.1` and `libpysal 4.13.0`. It uses
one CPU worker because numba-backed parallel randomization can complicate
strict replay. Each map is checkpointed with its configuration, SHA-256 hash,
seed, and population. An incomplete or mismatched checkpoint stops execution
instead of being silently reused or overwritten.

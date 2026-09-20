# Decision 017 — Phase 8D MAUP Global Moran comparison

- **Status:** Accepted for implementation before alternative-grid Moran results
  are inspected
- **Date:** 2026-09-20
- **Applies to:** Phase 8D comparison of global spatial autocorrelation

## Purpose

Phase 8D tests whether the strength, sign and temporal ordering of global
spatial autocorrelation are stable under the three alternative MAUP grids. It
follows Phase 8C and precedes any alternative-grid Local Moran/LISA analysis.

The canonical approximately 20,000-ha grid remains primary. Alternative grids
are sensitivity tests and cannot replace the canonical result.

## Spatial supports

The comparison uses:

- `hex20k_canonical` — canonical reference;
- `hex10k_base` — finer-scale sensitivity;
- `hex20k_shift` — zoning sensitivity at approximately equal scale;
- `hex40k_base` — coarser-scale sensitivity.

Alternative-grid primary graphs retain cells with fixed-domain support
fraction at least 0.50. Shared-edge neighbors are reconstructed from the six
valid axial-coordinate offsets of each regular hexagonal lattice. Surviving
edges are row-standardized after support selection. Islands remain in the
population, centering and expected value with zero spatial lag. No k-nearest,
distance-band or artificial links are added.

The canonical graph remains the accepted Phase 1 shared-edge graph.

## Metrics

The restricted comparison contains five focal metrics:

1. consolidation density per 10,000 ha of analytical support;
2. replenishment density per 10,000 ha of analytical support;
3. endpoint `NAT -> TMP` density per 10,000 ha of analytical support;
4. net C-R balance density per 10,000 ha of analytical support;
5. the bounded C-R balance index on its declared active support.

Density normalization prevents partial boundary support from being interpreted
as low process intensity. On the nearly equal-area canonical grid it is a
near-constant rescaling of the accepted raw-area metrics. The script must
reproduce the accepted Phase 5 raw canonical Moran values before constructing
the density reference.

## Inference

Alternative-grid statistics use the accepted Phase 5 conventions:

- raw metric values after the declared density normalization;
- 9,999 unrestricted permutations within the observed support;
- deterministic per-test seeds;
- two-sided absolute departure from `E[I] = -1/(N-1)`;
- plus-one Monte Carlo p-values;
- Benjamini-Yekutieli correction at alpha 0.05;
- primary and diagnostic families kept separate;
- complete and conditional supports kept separate.

Correction families include all three alternative grids:

| Family | Tests |
|---|---:|
| complete primary | 3 grids × 4 metrics × 7 intervals = 84 |
| conditional primary | 3 grids × 1 metric × 7 intervals = 21 |
| complete diagnostic | 3 grids × 4 metrics × 1 interval = 12 |
| conditional diagnostic | 3 grids × 1 metric × 1 interval = 3 |

## Prespecified robustness criteria

For each grid, metric and interval:

- absolute difference from canonical Moran's I no greater than `0.10`;
- sign of Moran's I preserved;
- the alternative result significant after the prespecified BY correction.

For each grid, metric and temporal window:

- Spearman correlation of the Moran-I sequence at least `0.90`;
- maximum interval displaced by no more than one quinquennium;
- minimum interval displaced by no more than one quinquennium.

Each grid receives separate assessments for:

- `primary_1985_2020`;
- `full_observed_1985_2025`.

An assessment is stable only if every applicable interval and temporal
criterion passes. A sensitivity result is a scientific finding, not a runtime
validation failure.

## Diagnostic interval

The 2020-2025 interval is included and flagged. It participates in the full
observed assessment but does not alter the seven-interval primary family or
silently redefine the primary-period conclusion.

## Computational staging

Phase 8D uses per-test checkpoints because 120 alternative-grid permutation
tests are required. A resumed test must match the script version, authenticated
inputs, grid, metric, interval, support rule and permutation count.

## Scope boundary

Phase 8D evaluates Global Moran only. It does not calculate alternative-grid
Local Moran/LISA or compare cluster footprints. Those tasks belong to Phase 8E
after the global results are validated and interpreted.

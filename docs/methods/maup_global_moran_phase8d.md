# Phase 8D method — Global Moran robustness across MAUP grids

## Analytical sequence

Phase 8D is the global spatial-autocorrelation component of the MAUP analysis.
It is deliberately separated from Phase 8E local-cluster comparison. This
retains the accepted analytical order:

```text
global association -> validation and interpretation -> selective local analysis
```

## Inputs

The implementation authenticates:

- the canonical Phase 2 metric panel;
- the accepted Phase 1 canonical contiguity graph;
- the accepted Phase 5 Global Moran result table;
- the Phase 8B alternative-grid metric panel;
- the three Phase 8A grid Parquets containing axial coordinates and support.

No Earth Engine processing, spatial interpolation or metric recalculation from
source rasters is required.

## Graph construction

The canonical graph is read from the accepted directed edge table and checked
for symmetry, zero diagonal and the accepted graph diagnostics.

For each alternative lattice, cells with support fraction at least 0.50 are
selected. Undirected shared-edge links are generated from three forward axial
offsets and expanded to symmetric directed adjacency:

```text
(+1, 0), (0, +1), (+1, -1)
```

Their inverse directions complete the six-neighbor regular-hexagon structure.
Centroid distances are checked against the accepted lattice neighbor distance.
Every graph reports cell count, edges, components, islands, largest component,
mean degree and degree distribution.

## Comparable variables

For the four area-valued outcomes:

```text
density per 10,000 ha = process area / analytical support area * 10,000
```

Canonical analytical support is the equal-area cell geometry. Alternative
analytical support is the raster-domain support used in Phase 8B. The bounded
C-R balance index is used without rescaling and only where gross C-R activity
is positive.

## Moran calculation

For centered observations `z` and row-standardized weights `w`:

```text
I = (N / S0) * [sum_i sum_j w_ij z_i z_j] / [sum_i z_i^2]
```

Islands remain in `N`, the mean and the denominator and have spatial lag zero.
For conditional C-R support, the graph is induced on active cells and surviving
rows are standardized again.

Each alternative test uses 9,999 permutations and a stable SHA-256-derived
seed. Full simulated distributions are preserved. Checkpoints allow an
interrupted Colab session to continue without recomputing completed tests.

## Comparisons

The output separates three questions:

1. **inference:** is alternative-grid Moran significant after BY correction?
2. **interval stability:** are sign and magnitude close to the canonical value?
3. **temporal stability:** is the ordering of Moran values through time
   preserved?

Magnitude stability uses an absolute difference in Moran's I, not a relative
difference, because relative differences are unstable near zero.

## Outputs

The stage produces:

- all canonical-reference and alternative Moran estimates;
- interval-level comparisons with the canonical grid;
- temporal comparisons for primary and full-observed windows;
- six grid-window assessments;
- graph diagnostics;
- complete alternative permutation distributions;
- figures, validation JSON and inventory.

The permutation archive and checkpoints may remain outside GitHub. Compact
tables, figures, design documentation and validation records are repository
products.

## Implementation identity

```text
analysis/14b_compute_maup_global_moran_v1.py
script version: phase8d-maup-global-moran-v1
SHA-256: 3d996409ab82498e886051631200c49c5bc463a438759e6f7d7984e83fd28d27
```

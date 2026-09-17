# Decision 014 — Phase 8 MAUP grids and fixed analytical footprint

## Decision

Phase 8 will evaluate scale and zoning while holding the underlying analytical
footprint fixed. The footprint is the union of the 24,889 complete canonical
Phase 1 cells. Alternative grids will not repeat the endpoint anthropogenic
selection and will not expand analysis into pixels outside that footprint.

Three alternative hexagonal grids will be constructed in the project Albers
equal-area CRS:

1. approximately 10,000 ha with the canonical lattice origin and orientation;
2. approximately 40,000 ha with the canonical lattice origin and orientation;
3. approximately 20,000 ha translated by one half of each of the two canonical
   lattice basis vectors.

The 20,000-ha shifted grid isolates zoning sensitivity without also changing
cell size or orientation. A tilted grid is not included because it would add a
second zoning transformation when one prespecified alternative is sufficient.

## Lattice reconstruction

The canonical lattice will be inferred from projected cell centroids rather
than from a hard-coded origin. The procedure estimates:

- median nearest-neighbor center distance;
- the common neighbor-direction angle modulo 60 degrees;
- regular-hexagon side length and implied area;
- an observed canonical centroid as the lattice anchor; and
- residual distances between observed and reconstructed canonical centroids.

The script stops if the inferred lattice is inconsistent with the 20,000-ha
reference or if centroid residuals exceed the prespecified tolerances.

## Fixed-domain support

Every alternative unit intersecting the canonical footprint is retained.
For each unit, Phase 8A records:

- nominal complete-hexagon area;
- vector intersection area with the fixed canonical footprint; and
- the corresponding support fraction.

The alternative-cell geometries remain complete hexagons. The support area is
an attribute and later becomes a raster mask in the process extraction. This
avoids replacing the regular lattice with irregular clipped polygons.

Aggregate process totals in Phase 8B will use every unit with positive support
so that the full canonical footprint closes. A support threshold for
cell-distribution or Moran comparisons is deliberately not chosen in Phase 8A.
Phase 8A reports the geometric support distribution first; any threshold must
be fixed before process results are inspected.

## Consequences

- scale and zoning change, but the underlying pixel footprint does not;
- boundary units may have partial support and must not use nominal area as if
  the entire unit were observed;
- process areas will be measured from source pixels in Phase 8B, not allocated
  from canonical-cell totals;
- areal interpolation of canonical metrics is prohibited;
- Phase 8A generates geometry and support only and cannot produce a scientific
  MAUP conclusion by itself;
- 2020–2025 remains included as a diagnostic interval in later Phase 8 steps.

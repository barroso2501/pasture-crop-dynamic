# Decision 014 — Phase 8 MAUP grids and fixed analytical footprint

- **Status:** Accepted and implemented in Phase 8A
- **Date accepted:** 2026-09-17

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
cell-distribution or Moran comparisons was deliberately not chosen before
Phase 8A. After inspection of the geometric support distribution, and before
any process result is calculated, the following rules are fixed for Phase 8B:

- all cells with positive support contribute to fixed-domain closure and
  aggregate process totals;
- `domain_support_fraction >= 0.50` defines the primary cell-level analytical
  population;
- thresholds of 0.25 and 0.75 define lower- and higher-support sensitivity
  populations;
- relative measures for partially supported cells use the effective supported
  area or the relevant process-specific supported denominator, never the
  nominal complete-hexagon area; and
- process values must be measured directly from source pixels under the fixed
  domain mask and must not be allocated from canonical-cell totals.

These rules were selected from geometry alone. They were not informed by the
direction, magnitude, distribution or spatial autocorrelation of any Phase 8B
process result.

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

## Implementation record

Revision 1 stopped within its synthetic engine test because the test created
25 cells while the production lattice-inference function required at least
100. It did not read the canonical input or create analytical output. Revision
2 increased the synthetic test to 169 cells without changing the production
method, grid specifications, input identity, output paths or tolerances.

The accepted revision-2 script is identified by:

```text
script version: phase8a-maup-alternative-grids-script-v2
SHA-256: d4f0287dd655936293c2f494feb1eadd827911cdf6028877d7eefd59b259b827
```

Production passed for all three grids. The fixed projected domain area was
497,776,400.4434 ha. The generated populations were 56,520 cells for
`hex10k_base`, 29,396 for `hex20k_shift`, and 15,309 for `hex40k_base`.
Relative area-closure differences ranged from approximately `1.2e-15` to
`1.7e-14`. All generated geometries and identifiers passed validation.

At the primary 0.50 support threshold, the retained populations are 49,716,
25,015 and 12,445 cells, respectively. They contain 97.11%, 94.96% and 94.86%
of the corresponding positive-support area. These percentages describe the
analytical subset only; aggregate accounting continues to use every
positive-support unit.

## Rejected alternatives

- redefining the anthropogenic domain independently for each alternative grid;
- clipping exported hexagon geometries and treating the fragments as a new
  irregular lattice;
- using nominal cell area as the denominator for partially supported cells;
- selecting a support threshold after observing process outcomes;
- reconstructing alternative-grid values by areal interpolation of accepted
  canonical-cell totals; and
- adding a rotated grid to the prespecified scale and translation tests.

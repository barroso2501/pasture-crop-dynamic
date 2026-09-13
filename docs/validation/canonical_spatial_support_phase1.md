# Canonical spatial-support validation: Phase 1

- **Status:** Passed
- **Validation date:** 2026-09-13
- **Method:** `docs/methods/canonical_spatial_support_and_contiguity.md`
- **GEE export script:** `gee/05a_export_spatial_support_inputs.js`
- **Spatial build script:** `analysis/06_build_canonical_spatial_support.py`

## Scope

This validation covers the canonical spatial table, biome-overlap attributes,
and fixed shared-edge contiguity graph. It tests input identity, geometry,
panel membership, area support, biome intersections, edge construction,
symmetry, row standardization, connected components, and islands.

It does not evaluate spatial autocorrelation or interpret ecological patterns.

## Earth Engine vector exports

| Export | Task ID | Status | Runtime | EECU-seconds |
|---|---|---|---:|---:|
| `canonical_spatial_grid_input_v1` | `Y457QODSNDFRDDTN36R2XOGL` | Completed, attempt 1 | 26 s | 5.1861 |
| `canonical_biomes_input_ibge2025_v1` | `JE2ALPLLX6V2M6CBQQM7CEW7` | Completed, attempt 1 | 8 s | 2.3183 |

Both tasks started on 2026-09-13 at 06:17:27, UTC-03:00.

| Input | Features | SHA-256 |
|---|---:|---|
| `canonical_spatial_grid_input_v1.geojson` | 24,889 | `c3ce310bc474a05f168a2e7ce5b7644026630038c68457ff5948304d0ce1950f` |
| `canonical_biomes_input_ibge2025_v1.geojson` | 2 | `1f3dfccef176e4de5b64405cc5dacf2c098805e99e2ac4449352b9fb307a38a6` |

## Structural validation

| Check | Result |
|---|---:|
| Cells | 24,889 |
| Distinct `cell_id` values | 24,889 |
| Distinct `GRID_ID` values | 24,889 |
| Panel cells without spatial row | 0 |
| Spatial rows without panel cell | 0 |
| Invalid geometries | 0 |
| Empty geometries | 0 |
| Geometry types | Polygon only |
| Maximum overlap between grid cells | `0.0` m² |
| AEA centroids outside source cells | 0 |

All canonical cells were retained once, and the spatial population matched the
accepted integrated panel exactly.

## Area comparison

| Measure | Minimum (ha) | Mean (ha) | Maximum (ha) |
|---|---:|---:|---:|
| Earth Engine geodesic geometry | 20,042.998 | 20,079.245 | 20,090.050 |
| AEA vector geometry | 19,999.197 | 19,999.855 | 20,000.258 |

The mean absolute relative difference was `0.3954%`, and the maximum was
`0.4470%`, below the predefined `0.5%` diagnostic tolerance. The difference
is systematic rather than random and reflects the different geometric area
representations. Both fields are therefore preserved. AEA area is used for
vector overlap fractions, while accepted raster stock and flow areas retain
their original pixel-area basis.

## Biome support

| Result | Value |
|---|---:|
| Amazon-primary cells | 14,213 |
| Cerrado-primary cells | 10,676 |
| Exact ties | 0 |
| Cells intersecting both Amazon and Cerrado | 582 |
| Cells extending outside the two target biomes | 1,984 |
| Total complete-cell area | 497.7764 Mha |
| Area inside Amazon or Cerrado | 478.6251 Mha |
| Area outside the two target biomes | 19.1513 Mha |

Complete hexagons were not clipped to biome boundaries. Consequently, `3.85%`
of their combined AEA area lies outside the two target-biome polygons. This is
consistent with the accepted domain construction, but it is material for
biome-specific interpretation:

- 946 cells have less than 50% of their area in the target biomes;
- 83 cells have less than 1% target-biome overlap; and
- the minimum target-biome fraction is approximately `3.76e-6`.

The continuous overlap fractions must therefore remain available. The primary
biome label is accepted for descriptive stratification but is not sufficient
by itself for boundary-sensitive inference.

## Fixed contiguity graph

| Check | Result |
|---|---:|
| Undirected shared-edge links | 67,453 |
| Directed weight rows | 134,906 |
| Mean neighbors per cell | 5.4203 |
| Neighbor range | 0-6 |
| Symmetry violations | 0 |
| Self-links | 0 |
| Duplicate links | 0 |
| Maximum row-weight sum difference | `0.0` |
| Connected components | 264 |
| Islands | 163 |

The neighbor-count distribution is:

| Neighbors | Cells | Share |
|---:|---:|---:|
| 0 | 163 | 0.65% |
| 1 | 320 | 1.29% |
| 2 | 644 | 2.59% |
| 3 | 1,214 | 4.88% |
| 4 | 1,743 | 7.00% |
| 5 | 2,146 | 8.62% |
| 6 | 18,659 | 74.97% |

The largest component contains 24,014 cells, or `96.48%` of the domain. The
remaining 875 cells form 263 components and all are Amazon-primary. Of the 163
islands, 149 are completely inside the target biomes. Fragmentation is
therefore not driven mainly by marginal biome intersections. It is consistent
with the reduced-domain rule: retained anthropogenic cells may be separated by
stable natural cells that were excluded from the analytical population.

Islands remain in the table with zero neighbors. No artificial connection was
introduced.

## Output identity

| Output | SHA-256 |
|---|---|
| `canonical_spatial_support_v1.parquet` | `22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc` |
| `canonical_spatial_support_attributes_v1.csv` | `70068e7ccf4bc8f91d5278a358343f5f336cf71b7a89c4466171986bcd094653` |
| `canonical_contiguity_weights_v1.parquet` | `85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f` |
| `canonical_biome_assignment_summary_v1.csv` | `38171243b1b731659ea18d693eb8bf8323dd8f47fce523b00d9642186e5dab47` |
| `canonical_neighbor_count_distribution_v1.csv` | `1c3c1963b6b05a44eab68ab8ec91b6fb1d22cb0e97628e4b47224c88b7960b27` |
| `canonical_connected_components_v1.csv` | `645ac35aa8d0706f06982b69f823794ffcc3e0d75b8dc636156fa46d521925b7` |
| `canonical_spatial_support_summary_v1.csv` | `087d7a9b2c0718d4d0a803cbc974d41a1ed76478b9bc85091270d1453d4283cb` |
| `canonical_spatial_support_validation_v1.json` | `397e497284adfb0e070b6e3e853743a11e254773120258725f64f4f070be8a11` |

## Acceptance

All predefined structural, membership, geometry, overlap, topology, symmetry,
and row-standardization checks passed. The spatial-support table and fixed
edge-contiguity graph are accepted for subsequent analyses.

Two conditions must remain explicit downstream:

1. disconnected components and islands arise from the reduced analytical
   domain and must not be silently connected; and
2. complete-cell values cannot be assigned wholly to one biome in
   boundary-sensitive analysis without using overlap fractions or a documented
   sensitivity rule.

Phase 2 may now calculate spatial metrics using this fixed support.

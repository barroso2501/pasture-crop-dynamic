# Phase 8A — alternative-grid construction

## Purpose

Phase 8A constructs the spatial units required for the MAUP robustness test.
It changes neither accepted process values nor earlier spatial inference. No
MapBiomas raster, class limit, trajectory, Moran statistic, or LISA class is
read or recalculated.

## Input

The only analytical input is:

```text
spatial/phase1/canonical_spatial_support_v1.parquet
```

Accepted SHA-256:

```text
22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc
```

The input must contain exactly 24,889 unique `cell_id` values and valid
geometries with a defined CRS.

## Coordinate systems

Source geometries are read from their stored CRS and transformed to the
project Albers equal-area CRS:

```text
+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42
+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs
```

All lattice inference, polygon construction, support intersections and area
checks occur in this CRS. Public grid geometries are exported in EPSG:4326 for
GIS and Earth Engine interoperability. Their equal-area centroid coordinates
and area attributes remain attached.

## Canonical-lattice inference

A nearest-neighbor search is applied to canonical cell centroids. The median
nearest-neighbor distance estimates the canonical center spacing. Neighbor
vectors within eight percent of that distance estimate the common direction
angle modulo 60 degrees.

For regular hexagons with side length \(s\):

\[
A = \frac{3\sqrt{3}}{2}s^2
\]

and nearest adjacent centers are separated by:

\[
d = \sqrt{3}s.
\]

The side length derived from center spacing must agree within one percent with
the side length derived from the median source-polygon area. The implied
reference area must also agree within one percent with 20,000 ha.

One observed centroid near the middle of the domain becomes the anchor. Every
canonical centroid is expressed in the two inferred lattice basis vectors and
rounded to axial coordinates. The 99th-percentile reconstruction residual must
be no more than one percent of center spacing, and the maximum residual no more
than three percent.

## Alternative grids

| Code | Area multiplier | Approximate area | Origin shift |
|---|---:|---:|---|
| `hex10k_base` | 0.5 | 10,000 ha | none |
| `hex20k_shift` | 1.0 | 20,000 ha | 0.5 q + 0.5 r canonical basis |
| `hex40k_base` | 2.0 | 40,000 ha | none |

Side length and center spacing are multiplied by the square root of the area
multiplier. The alternative lattice is generated beyond the canonical-domain
bounding box and then reduced to cells with positive-area intersection with
the fixed footprint.

## Support accounting

Because the canonical domain is a selected union of complete cells, alternative
hexagons near its edge may be only partly supported. Phase 8A calculates:

```text
domain_support_fraction = vector_domain_support_ha / nominal_area_ha
```

The sum of `vector_domain_support_ha` must reproduce the projected area of the
canonical footprint within a relative tolerance of `2e-7` for every grid.

The distribution is reported using support thresholds of 10%, 25%, 50%, 75%
and 90%. These were geometric diagnostics in Phase 8A. After the distribution
was reviewed, but before process extraction, Decision 014 fixed 50% as the
primary threshold for cell-level Phase 8B comparisons and 25% and 75% as
sensitivity thresholds. Fixed-domain totals continue to use all positive
support.

## Identifiers and exported attributes

Each grid has deterministic axial coordinates and identifiers:

- `maup_cell_id`: sequential integer within the grid;
- `maup_uid`: grid code plus signed q and r axial coordinates;
- `grid_code`;
- `batch_id` for later Earth Engine execution;
- nominal and supported areas;
- support fraction;
- projected centroid coordinates;
- geometry-validity and version fields.

Each grid is exported as GeoParquet, GeoPackage and GeoJSON. All three formats
represent the same cell population.

## Interpretation boundary

Vector support measures the intersection of alternative polygons with the
canonical vector footprint. Phase 8B must independently measure raster support
under the canonical-domain mask. Small vector–raster differences may reflect
the source pixel lattice and must be audited rather than silently overwritten.

Phase 8A provides spatial units only. No difference among grids can yet be
interpreted as robustness or instability of the ecological results.

## Production implementation and results

The accepted production run used script revision 2. Revision 1 had failed only
inside the synthetic verification because its 25-cell fixture was smaller than
the inference engine's minimum population of 100. Revision 2 used a 13 by 13
synthetic lattice (169 cells); no production algorithm or tolerance changed.

The inferred canonical lattice had a center spacing of 15,196.5456 m, a side
length of 8,773.7297 m and an implied reference area of 19,999.5575 ha. The
median source-polygon area was 19,999.8649 ha. The p99 and maximum centroid
reconstruction residuals were 15.5629 m and 16.9130 m, respectively.

| Grid | Cells | Nominal area (ha) | Cells >=50% support | Fixed-domain closure difference |
|---|---:|---:|---:|---:|
| `hex10k_base` | 56,520 | 9,999.7787 | 49,716 | `1.687e-14` |
| `hex20k_shift` | 29,396 | 19,999.5575 | 25,015 | `2.747e-15` |
| `hex40k_base` | 15,309 | 39,999.1149 | 12,445 | `1.177e-15` |

All three grids reproduced the same 497,776,400.4434-ha fixed footprint.
Identifiers were unique and non-null, generated geometries were valid, and the
GeoParquet, GeoPackage and GeoJSON populations agreed with the inventory.

## Phase 8B handoff

Phase 8B must obtain process measurements directly from the accepted source
pixel transitions under the fixed-domain mask. The complete positive-support
population is used for conservation and totals. Cell-distribution and spatial
statistics use the primary and sensitivity support populations fixed in
Decision 014. The vector support values remain the expected geometric
reference against which raster support is audited.

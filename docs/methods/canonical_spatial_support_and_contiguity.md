# Canonical spatial support and fixed contiguity graph

- **Status:** Implemented
- **Implementation date:** 2026-09-13
- **GEE export script:** `gee/05a_export_spatial_support_inputs.js`
- **Spatial build script:** `analysis/06_build_canonical_spatial_support.py`
- **Validation:** `docs/validation/canonical_spatial_support_phase1.md`

## Purpose

This method creates the fixed spatial reference used by all subsequent maps,
cell trajectories, biome comparisons, and spatial-autocorrelation analyses.
It adds geometry and spatial relationships to the canonical analytical
population without changing the accepted stock-flow or annual-trajectory
measurements.

The population contains the same 24,889 complete hexagonal cells represented
in every interval of the canonical integrated panel.

## Inputs

The vector inputs are exported from Earth Engine as GeoJSON:

| Role | Source |
|---|---|
| Canonical grid | `projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3` |
| IBGE 2025 biomes | `projects/ee-barroso2501/assets/biomas_IBGE` |
| Amazon code | `CD_BIOMA = "1"` |
| Cerrado code | `CD_BIOMA = "3"` |

The integrated panel is used only to confirm exact equality of the `cell_id`
population. Its accepted SHA-256 is:

```text
7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28
```

## Coordinate systems and area fields

Source geometries are retained in `EPSG:4326`. Vector area, biome intersection,
centroid, and shared-boundary calculations use the project-defined equal-area
Albers CRS:

```text
+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42
+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs
```

The spatial table preserves two distinct area measures:

- `geometry_area_geodesic_ha`, calculated by Earth Engine from the WGS84
  geometry; and
- `geometry_area_aea_ha`, calculated after transformation to the equal-area
  CRS.

These measures are not interchangeable. The AEA value is used as the
denominator for vector biome-overlap fractions. Raster stock and flow areas
remain the accepted Earth Engine pixel-area measurements. Process-specific
relative metrics retain the denominators defined in the integrated panel and
must not be recomputed from generic vector cell area.

## Centroids

The table retains the Earth Engine centroid and an independent centroid
calculated in the AEA projection and transformed back to WGS84. Their distance
is stored as a quality-control field. The projected centroid must fall within
its source hexagon.

Centroids support visualization and diagnostics. They do not replace polygon
geometry in spatial joins or contiguity calculations.

## Biome overlap and assignment

Amazon and Cerrado overlap areas are obtained through exact polygon
intersection in the AEA projection. For each cell:

```text
target_biome_overlap_ha = amazon_overlap_ha + cerrado_overlap_ha
```

Fractions use the complete AEA cell area as denominator. The table also
retains the cell area outside the two target-biome polygons. This is required
because the canonical domain contains complete hexagons selected by spatial
intersection, rather than geometries clipped to biome boundaries.

The `primary_biome` label is the biome with the larger overlap area. It is a
deterministic summary field, not a replacement for the continuous overlap
fractions. Boundary cells and cells with limited target-biome support must use
the fractional fields or an explicitly documented sensitivity rule in biome
comparisons.

## Fixed edge-contiguity graph

The complete-domain graph uses shared-edge contiguity:

1. geometries are transformed to the AEA CRS;
2. intersecting polygon pairs are identified using a spatial index;
3. pairs sharing more than 1 m of boundary are retained;
4. point-only contacts are excluded;
5. an undirected edge table is converted to symmetric directed weights; and
6. binary weights are standardized to sum to one for every non-island focal
   cell.

The 1 m rule is a numerical tolerance far below the true hexagon edge length.
It excludes zero-length vertex contacts without redefining neighborhood at an
ecologically meaningful distance.

The graph is built once and held fixed across all intervals. Cells with no
retained neighbor remain islands with zero neighbors; no k-nearest-neighbor or
distance link is added. Connected-component and island identifiers are
retained in the spatial table so that subsequent spatial inference can state
its support explicitly.

## Outputs

The principal outputs are:

```text
canonical_spatial_support_v1.parquet
canonical_spatial_support_attributes_v1.csv
canonical_contiguity_weights_v1.parquet
```

Compact biome, neighbor, component, and validation summaries accompany these
files. The two large Parquet files remain in the project data store and are
identified in GitHub by version, dimensions, and cryptographic hash.

## Downstream restrictions

- Do not rebuild the complete-domain graph separately for each interval.
- Do not add artificial links to islands without a new documented decision.
- Do not treat a missing conditional metric as a zero process value.
- Do not use `primary_biome` alone for cells with limited or divided biome
  support.
- Do not mix AEA vector area, Earth Engine geodesic geometry area, and raster
  pixel area without naming the applicable measure and purpose.

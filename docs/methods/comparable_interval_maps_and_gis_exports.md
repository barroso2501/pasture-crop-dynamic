# Comparable interval maps and GIS-ready tables

- **Phase:** 3B and auxiliary GIS export
- **Map product version:** `canonical-comparable-interval-maps-v1`
- **GIS-table version:** `canonical-gis-interval-tables-v1`
- **Final mapping script:** `analysis/08b_build_comparable_interval_maps_v3.py`
- **GIS export script:** `analysis/08c_export_gis_interval_tables.py`

## Purpose

Phase 3B converts the 12 class specifications accepted in Phase 3A into
temporally comparable map series. The accompanying GIS export provides the
same continuous metrics and frozen classes as interval-specific CSV tables
that can be joined to the canonical grid in desktop GIS software.

These products support spatial inspection and figure development. They do not
create new accounting metrics, alter the canonical analytical population, or
refit any class limit.

## Inputs and analytical population

The workflow uses:

- the validated 199,112-row Phase 2 spatial-metrics panel;
- the validated 24,889-cell spatial-support geometry;
- the final Phase 3A `v2` class specifications and class counts; and
- the seven primary intervals from 1985-1990 through 2015-2020, plus the
  diagnostic 2020-2025 extension.

All joins use the canonical identifier `cell_id`. The population remains one
record per cell and interval.

## Comparable-map construction

The final script reproduces each frozen Phase 3A class from the full-precision
limits stored in `canonical_map_classes_validation_v2.json`. The CSV class-limit
table remains an authenticated human-readable record, but its rounded display
values are not used as the numerical source for reclassification.

The 12 metric-specific maps each contain eight panels with identical class
definitions and fixed colors. Limits are not recalculated by interval, mapped
subset, or biome. The 2020-2025 panel uses the same definitions but is visibly
marked as diagnostic and does not contribute to limit fitting.

The source spatial-support geometry is stored in WGS 84. For map construction,
it is explicitly reprojected to the project-defined Albers equal-area CRS:

```text
+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42
+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs
```

Raster processing remains on the native MapBiomas lattice; this Albers CRS is
used only for vector spatial support, area checking, and cartographic output.

Outputs include:

- 12 comparable eight-panel maps in PNG;
- the same 12 maps in SVG;
- a classified cell-by-interval Parquet table;
- a fixed legend table;
- reproduced class counts;
- a map inventory; and
- a machine-readable validation record.

The PNG files are convenient inspection copies. SVG files preserve a
publication-oriented vector representation. Subsequent changes limited to
titles, type size, spacing, legend placement, or similar design elements do
not change the accepted classifications, provided the underlying class fields,
colors, and interval labels remain unchanged.

## GIS interval tables

The auxiliary export creates eight CSV files, one for each interval. Every
file contains 24,889 unique `cell_id` records and 78 fields, including:

- identifiers and interval metadata;
- spatial-support and biome attributes;
- denominators and activity fields;
- 12 continuous spatial metrics;
- support and occurrence flags;
- 12 frozen class-label fields; and
- 12 ordered class-code fields.

The tables are written as UTF-8 with a byte-order mark for desktop-software
compatibility. A generated `schema.ini` assigns ArcGIS-readable field types,
including text types for `cell_id` and `GRID_ID`. The file must remain in the
same directory as the eight CSV files and its section names must continue to
match the CSV filenames.

For each interval, the recommended operation is a one-to-one join from the
canonical grid to the corresponding CSV using `cell_id`. If the joined layer
is materialized, a file geodatabase or GeoPackage should be used. Shapefile
output is unsuitable for the full table because it truncates field names and
has other format limitations.

## Interpretation boundaries

- A GIS class is a cartographic summary of an accepted continuous metric; it
  does not replace that continuous value in analysis.
- `inactive`, `undefined`, `not_applicable`, `low_support`, and observed zero
  retain distinct meanings.
- Pixel trajectories remain distinct from net balance in a 20,000 ha cell.
- Successful opening or joining in ArcGIS is an interoperability check, not an
  independent validation of MapBiomas classification accuracy.


# Phase 8A alternative-grid implementation preflight

## Status

Historical preflight status: **PASSED; PRODUCTION SUBSEQUENTLY ACCEPTED**.

The script passes Python syntax compilation and contains an executable
synthetic geometry-engine verification that runs before access to Google Drive.
The current review environment does not provide the optional geospatial Python
dependencies, so the embedded engine check will be confirmed by the first
lines of the Colab run after the documented installation command.

Production acceptance was completed on 2026-09-17. The final evidence and
independent review are recorded in
`docs/validation/canonical_phase8a_maup_alternative_grids_v1.md`.

The first production attempt stopped before reading analytical input because
the synthetic fixture contained 25 cells while the production inference
function required at least 100. Revision 2 expanded only that fixture to 169
cells. The frozen design and every production tolerance below remained
unchanged.

## Frozen design

- fixed footprint: union of 24,889 canonical Phase 1 cells;
- project Albers equal-area CRS for construction and measurement;
- 10,000-ha and 40,000-ha scale alternatives;
- 20,000-ha grid shifted by half of each canonical lattice basis vector;
- no grid rotation;
- no repeated anthropogenic-domain selection;
- no areal interpolation of process values;
- no process extraction or statistical analysis in Phase 8A;
- no support-fraction threshold selected before geometric diagnostics.

## Production gates

The script must stop unless:

- the source file has the accepted SHA-256 hash;
- source population is exactly 24,889 unique cells;
- all source geometries are present and valid;
- center spacing and polygon area describe the same regular hexagon within 1%;
- inferred reference area is within 1% of 20,000 ha;
- canonical-centroid lattice residuals pass the p99 and maximum tolerances;
- every generated geometry is valid;
- identifiers are unique within each grid;
- support fractions do not exceed one beyond numerical tolerance; and
- every alternative grid closes to the complete fixed-domain area within
  relative tolerance `2e-7`.

## Expected products

For each of the three grids:

```text
maup_grid_<grid_code>_v1.parquet
maup_grid_<grid_code>_v1.gpkg
maup_grid_<grid_code>_v1.geojson
```

And:

```text
canonical_maup_grid_design_v1.json
canonical_maup_grid_summary_v1.csv
canonical_maup_grid_support_distribution_v1.csv
canonical_maup_grid_validation_v1.json
canonical_maup_grid_inventory_v1.csv
canonical_maup_alternative_grids_v1.zip
```

The actual alternative-cell counts are intentionally not prescribed. They
depend on exact intersection with the fixed footprint and must be reported by
the production run rather than anticipated from area ratios.

# Canonical GIS interval tables validation

- **Status:** PASS; GIS export accepted
- **Validation date:** 2026-09-14
- **Output version:** `canonical-gis-interval-tables-v1`
- **Script:** `analysis/08c_export_gis_interval_tables.py`
- **Script SHA-256:** `0bd29003287163dda0ec26a605ab10e64ed681e07788c4a7e83610849ab8c667`
- **Validation record SHA-256:** `130a9d8652f51f232c0d4f0a09e6ceb1d6caac8b0b7fb6a705e2b455dbbd12f3`

## Purpose

The export provides interval-specific tables for one-to-one joins to the
canonical polygon grid in ArcGIS Pro or another GIS. It is an auxiliary access
product derived from the accepted Phase 2 metrics and Phase 3B frozen classes;
it does not create a new analytical result.

## Structure

| Property | Accepted result |
|---|---:|
| Interval CSV files | 8 |
| Rows per CSV | 24,889 |
| Columns per CSV | 78 |
| Continuous map metrics | 12 |
| Frozen class-label fields | 12 |
| Frozen class-code fields | 12 |
| Join field | `cell_id` |
| Within-interval cardinality | one-to-one |
| Diagnostic interval | `2020_2025` |

The field dictionary contains exactly 78 unique field definitions, with no
missing descriptions or units. `cell_id` and `GRID_ID` are explicitly defined
as text fields with width 32. Numeric metrics are defined as `Double`, while
integer flags, years, and ordered codes are defined as `Long` in `schema.ini`.

## Automated checks

All 14 checks in `canonical_gis_interval_tables_validation_v1.json` passed:

- Phase 2 input hashes matched the pinned identities;
- the Phase 2 and Phase 3B validation records passed;
- the classified panel matched the Phase 3B record;
- Phase 2 and Phase 3B keys matched;
- the one-to-one join preserved all rows;
- all class fields were complete;
- all eight expected intervals were present;
- each CSV contained 24,889 rows;
- `cell_id` was unique within every CSV;
- `cell_id` survived a CSV write-read round trip;
- `schema.ini`, the manifest, and the field dictionary were created; and
- ZIP integrity passed.

The portable ZIP has SHA-256
`7d568fba9338348bde4925bc40fc2f4bac83c21da371c0fcdb75e5867693924f`.
The field dictionary has SHA-256
`3fa71bfe3a712fae598e305dd7f40b5583aa49c9e05d0190a5c1da8a59c2a16e`.

## ArcGIS Pro interoperability check

On 2026-09-14, the exported CSV tables were opened in ArcGIS Pro without
errors while `schema.ini` remained in the same directory. This closes the
practical import and schema-interpretation check.

The ArcGIS check confirms that the delivery format can be read in the intended
software. The one-to-one population, identifier uniqueness, class completeness,
and source identities are established by the automated validation record, not
by visual inspection in the GIS.

If a joined result is permanently exported, file geodatabase or GeoPackage is
preferred. Shapefile output must not be used for the complete 78-field table
because it truncates field names.

## Acceptance decision

The eight interval CSV files, manifest, field dictionary, `schema.ini`, and
portable ZIP are accepted as the canonical GIS-ready derivative of Phase 3B.
No rerun is required.


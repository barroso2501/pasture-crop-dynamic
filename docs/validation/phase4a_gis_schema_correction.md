# Phase 4A GIS schema interoperability correction

- **Date:** 2026-09-15.
- **Issue reported:** ArcGIS rejected `CharacterSet=65001` in `schema.ini` while adding `cr_balance_primary_v1.csv`.
- **Cause:** Invalid schema option written by the exporter, not an invalid CSV data type or canonical metric.

## Correction and use

The replacement `schema.ini` removes the unsupported CharacterSet option from
all four GIS CSV sections. Column names, order, types and text ID declarations
are preserved exactly. CSV bytes are unchanged and retain their original UTF-8
BOM. An ANSI override is not applied to UTF-8 CSVs.

Replace `schema.ini` in the folder containing the four Phase 4A GIS CSVs.
Remove any failed table reference from ArcGIS, refresh the folder connection
and add the CSV again. If cached interpretation persists, reopen the project.
Do not rename the CSVs or reorder their columns.

No Colab or upstream rerun is required. The corrected schema definition was
checked against all 42 headers in each of the four received CSVs. The ArcGIS
opening test still requires the user's environment; no successful live ArcGIS
retest is claimed here.

The previous accepted computational validation and its recorded original output
hashes remain unchanged. This replacement schema is an interoperability
revision; retain its separate identity rather than editing old validation hashes.

Script revision 3 removes the same option from future GIS schema generation.
Stages, classes, sequences, numerical data and existing result folders are
unchanged. For GitHub, use its bytes at
`analysis/09a_build_cell_state_trajectories.py` and place this note at
`docs/validation/phase4a_gis_schema_correction.md`.

## Documentation

Microsoft documents ANSI/OEM character-set values for this schema setting:
https://learn.microsoft.com/en-us/sql/odbc/microsoft/schema-ini-file-text-file-driver
Esri documents using schema.ini to override CSV field interpretation:
https://pro.arcgis.com/en/pro-app/3.6/help/data/tables/add-an-ascii-or-text-file-table.htm

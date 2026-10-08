# Pasture-age source-asset anomaly audit

**Scope:** Decision 024, acceptance criterion 11. **Version:** 1. This is an
audit of the public MapBiomas Collection 11 pasture-age asset against the
project's independently reconstructed annual pasture spells. The public age
codes remain source evidence and do not determine corrected analytical origin.

## Inputs and population

The audit uses the 41 annual coverage and pasture-age bands for 1985–2025 on
the assets configured in `lib/constants`, the 24,889 cells of the canonical
Amazon–Cerrado study domain, and the corrected canonical panel v2. The
source-age asset is
`projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_age_v1`.
The accepted panel and spatial-support SHA-256 values are recorded in the
validation JSON. Eight disjoint `source_batch_id` batches cover the cells.

The GEE script `gee/17u_export_pasture_age_source_audit_v1.js` produces a
cell-level and a year-by-cell CSV for a two-cell pilot and each of the eight
batches. The production validator is
`analysis/17v_validate_pasture_age_source_audit_v2.py`. The superseded v1
validator requested a nonexistent spatial-support field; v2 derives the
Amazon–Cerrado overlap flag from the two authenticated biome fractions.

## Definitions

| Measure | Meaning | Unit of the reported `_ha` field |
| --- | --- | --- |
| `raw_code1_any` | A pixel has raw pasture-age value exactly `1` in at least one year, regardless of same-year coverage. | Unique affected area, ha |
| `reuse100_any` | A pixel has raw age `100` in at least one year when coverage alone classifies its current observed PAS spell as a post-1985 entry. | Unique affected area, ha |
| `code100_unresolved_years` | Raw `100` occurs with observed PAS whose current spell origin is unresolved after a coverage gap. This does **not** establish reuse. | ha·year |
| `joint_both` | The **same raster pixel** meets both anomaly definitions at least once across 1985–2025, possibly in different years. | Unique affected area, ha |
| `raw_code1_years`, `reuse100_years` | Annual anomaly area summed over years. | ha·year |
| `reentry_events` | Repeated observed non-PAS→PAS entries after an earlier PAS observation. | Area-weighted ha·event |

The pixel universe for the four mutually exclusive `joint_*` categories is
the union of pixels ever observed as PAS in the annual coverage series and
pixels ever assigned raw age code `1`. Two distinct pixels inside one cell
can carry different anomalies even when `joint_both` is zero. Raw code `100`
after a masked or uncertain interval is counted separately until an observed
non-PAS state establishes a new spell.

Each `_pixel_equiv` field is a polygon-boundary-weighted pixel equivalent,
which may be fractional; it is not an integer count of pixel centers. Annual
`_ha` values can be added as ha·year but must not be described as unique
affected area. The annual summary flags 2021–2025 as the diagnostic extension;
these years remain included in the complete audit.

The biome summary assigns all affected area in a cell to its canonical
`primary_biome`, with a separate `transbiome_flag` for a cell overlapping both
Amazon and Cerrado. It does not split each raster pixel by official biome
polygons or identify every other biome boundary.

## Validation and provenance

The validator requires the authenticated pilot exports, the 16 full exports,
24,889 unique canonical `cell_id` values, the correct batch and `GRID_ID`
for each cell, matching cell and annual populations, and reproduction of the
pilot in the full export. It verifies the 41-year sums, coverage partition of
raw code `1`, four-way joint partition, area bounds, and episode subsets.
The accepted validation JSON records SHA-256 for all 16 raw batch exports and
all four derived outputs, including the cell Parquet.

To reproduce, run the GEE exporter first with `MODE='pilot'` (two tasks),
then with `MODE='batch'` and `BATCH=0` through `7` (two tasks per batch).
Wait for both exports per batch to appear in Drive. Place all 18 original
CSVs in one input directory without changing their bytes; Google Drive can
create homonymous folders for separate exports. From Colab, run:

```python
%run /content/17v_validate_pasture_age_source_audit_v2.py --mode pilot --raw-dir "/content/drive/MyDrive/pasture_age_source_audit_raw_v1"
%run /content/17v_validate_pasture_age_source_audit_v2.py --mode full --raw-dir "/content/drive/MyDrive/pasture_age_source_audit_raw_v1"
```

The full run requires the pilot PASS record and matches the pilot CSV hashes
to it. Adjust only `--raw-dir` if Drive assigned another folder name.

The local GEE script hash is `null` in the accepted JSON because the Colab
validator did not have the JS beside it. The available record therefore does
not cryptographically establish that the text pasted into the GEE Code Editor
was byte-identical to the repository copy. The cross-file and panel checks
validate the exported data under the declared audit definitions, not the
source asset's production code or MapBiomas's official meaning for code `1`.

See `docs/validation/pasture_age_source_asset_impact_audit_v1.md` for the
accepted results and `docs/validation/canonical_unresolved_pasture_age_pixel_diagnostic_v2.md`
for the separate native-pixel diagnosis of code `1`.

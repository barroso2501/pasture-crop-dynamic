# Stock-and-flow validation: 2005-2010

- **Status:** Passed
- **Validation date:** 2026-09-11
- **Method:** `docs/methods/five_year_stock_flow_panel.md`
- **Decision:** `docs/decisions/005_full_domain_stock_flow_processing.md`
- **Pilot script:** `gee/03a_reprocess_stock_flow_pilot_b00.js`
- **Full-domain script:** `gee/03b_reprocess_stock_flow_2005_2010_full_domain.js`

## Purpose

This validation establishes that the canonical stock-and-flow calculation can
be executed over the complete 24,889-cell domain without batch subdivision and
that it reproduces the previously validated `b00` pilot within numerical
precision.

The validation concerns computational integrity and accounting closure. It is
not an ecological interpretation of the 2005-2010 results and does not by
itself establish the thematic accuracy of the source products.

## Canonical inputs

| Role | Asset |
|---|---|
| Coverage | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3` |
| Pasture age | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_age_v1` |
| Canonical grid | `projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3` |
| Interval | 2005-2010 |
| Cells | 24,889 |
| Output version | `canonical-stock-flow-v1` |

## Pilot execution

| Field | Value |
|---|---|
| Task | `canonical_stock_flow_2005_2010_b00_v1` |
| Task ID | `HYSWMZ7UWSQ5ZCWZ3G6QTZOV` |
| Status | Completed, attempt 1 |
| Start | 2026-09-11 15:46:19, UTC-03:00 |
| Runtime | 3 minutes |
| Batch compute usage | 90,009.1875 EECU-seconds |
| Cells | 3,168 (`source_batch_id = 0`) |
| Output file | `canonical_stock_flow_2005_2010_b00_v1.csv` |

## Full-domain execution

| Field | Value |
|---|---|
| Task | `canonical_stock_flow_2005_2010_full_v1` |
| Task ID | `TAPIRJQQUDSDX6GO7TXILEAU` |
| Status | Completed, attempt 1 |
| Start | 2026-09-11 16:21:36, UTC-03:00 |
| Runtime | 17 minutes |
| Batch compute usage | 1,026,345.3750 EECU-seconds |
| Cells | 24,889 |
| Raster metrics | 68 |
| Output columns | 90 |
| Output file | `canonical_stock_flow_2005_2010_full_v1.csv` |

## Structural validation

| Check | Result |
|---|---:|
| Rows | 24,889 |
| Columns | 90 |
| Distinct `cell_id` values | 24,889 |
| Duplicate `cell_id` values | 0 |
| Distinct `GRID_ID` values | 24,889 |
| Duplicate `GRID_ID` values | 0 |
| Rows with missing values | 0 |
| Negative area values below `-1e-9` ha | 0 |
| Flow-bound violations above `1e-6` ha | 0 |
| Unexpected coverage area | 0 ha |
| Class-27 area | 0 ha |

All rows have consistent values for `t0`, `t1`, `interval`,
`output_version`, and `diagnostic_interval`. All eight source batches are
represented:

| `source_batch_id` | Cells |
|---:|---:|
| 0 | 3,168 |
| 1 | 3,128 |
| 2 | 3,061 |
| 3 | 3,118 |
| 4 | 3,104 |
| 5 | 3,105 |
| 6 | 3,088 |
| 7 | 3,117 |
| **Total** | **24,889** |

## Accounting closure

The endpoint states reconcile with the rasterized cell area, all focal origins
and destinations close, and the pasture-to-temporary-agriculture origin
partition is exhaustive.

| Residual | Maximum absolute value (ha) |
|---|---:|
| Initial stock-to-area | `3.274181e-11` |
| Final stock-to-area | `2.546585e-11` |
| Focal origin closure | `1.818989e-11` |
| Focal destination closure | `1.818989e-11` |
| `PAS->TMP` origin partition | `9.094947e-13` |

No row has an absolute accounting residual greater than `1e-9` ha.

## Pilot-to-full regression test

The 3,168 rows with `source_batch_id = 0` were extracted from the full-domain
result, sorted by `cell_id`, and compared with the independent pilot export.

| Check | Result |
|---|---:|
| Row and column dimensions | Identical: 3,168 x 90 |
| `cell_id` sequence | Identical |
| Text metadata mismatches | 0 |
| Maximum numerical difference | `1.240307e-6` ha |
| Differences greater than `2e-6` ha | 0 |
| Maximum difference relative to a 20,000-ha cell | `6.20e-11` |

The minor differences are accepted as floating-point effects caused by the
order of parallel raster aggregation. They do not indicate a change in input,
classification, or accounting logic.

## Pasture-age partition

The full-domain `PAS->TMP` flow is partitioned as follows. These values are
reported as validation diagnostics, not as manuscript conclusions.

| Component | Area (ha) | Share of `PAS->TMP` | Cells with positive area |
|---|---:|---:|---:|
| Censored pasture | 1,352,159.027 | 47.8489% | 7,665 |
| New pasture | 1,473,699.450 | 52.1499% | 10,089 |
| Unresolved age code | 33.497 | 0.001185% | 41 |
| Unattributed age | 0.000 | 0.0000% | 0 |
| **Total `PAS->TMP`** | **2,825,891.974** | **100%** | — |

Age code `1` remains explicitly unresolved. Its treatment follows
`docs/decisions/003_unresolved_pasture_age_code.md` and is not altered by this
validation.

## Spatial-support diagnostics

Rasterized cell area covers at least 99.546% of the complete geometry in every
cell. Valid land-cover area is smaller in boundary cells because the complete
hexagons are preserved while pixels outside valid MapBiomas support remain
masked.

| Diagnostic | 2005 | 2010 |
|---|---:|---:|
| Aggregate valid area / geometry area | 98.6655% | 98.6655% |
| Cells below 99% valid area | 511 | 511 |
| Cells below 95% valid area | 455 | 455 |
| Cells below 50% valid area | 227 | 227 |
| Cells below 10% valid area | 63 | 63 |
| Cells below 1% valid area | 9 | 9 |
| Minimum valid fraction | 0.1683% | 0.1683% |

These cells remain part of the fixed analytical domain. Downstream analyses
must retain the area-support variables and must not interpret a small valid
fraction as a zero-flow intact cell.

## Acceptance

The 2005-2010 full-domain export passes the structural, accounting, and pilot
regression checks. It is accepted as the canonical result for this interval.
The same full-domain design may now be applied to the seven remaining
five-year intervals.


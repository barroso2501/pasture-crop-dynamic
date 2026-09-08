# Canonical input audit

- **Status:** In progress — source structure and retained-grid checks completed; spatial alignment and low-value pasture-age codes remain under review
- **Audit script:** `gee/01_audit_canonical_inputs.js`, version 2
- **Configuration:** `config/constants.js`
- **Method reference:** `docs/methods/data_sources_and_classification.md`
- **Decision reference:** `docs/decisions/002_canonical_mapbiomas_inputs.md`
- **Execution date:** 2026-09-08

## Purpose

This record documents the structural audit of the final public MapBiomas Collection 11 inputs and the analytical grid used by the pasture–crop accounting workflow. The audit precedes canonical reprocessing of stock-and-flow outputs.

It evaluates source identity and structure, raster-grid compatibility, class coverage, pasture-age encoding, analytical-grid integrity, coverage–age agreement, and the consistency of the retained cells with the endpoint selection rule.

The audit does not assess thematic accuracy against independent reference data and does not itself produce scientific results.

## Canonical inputs

### Annual coverage

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

### Pasture age

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_pasture_age_v1
```

### Retained analytical grid

```text
projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao
```

## Execution record

| Field | Value |
|---|---|
| Execution date | 2026-09-08 |
| Earth Engine account/project | `ee-barroso2501` |
| Git commit | Not recorded |
| Script version | Version 2 |
| Annual-summary export | Completed |
| Endpoint-by-cell export | Completed |
| Full code-inventory export | Cancelled after more than eight hours |
| Annual-summary file | `canonical_input_audit_c11_v3_domain.csv` |
| Endpoint file | `canonical_endpoint_rule_c11_v3_by_cell.csv` |

The full code-inventory task was cancelled because it repeated grouped reductions across the complete domain for two variables and nine years. The completed annual audit already tests whether any coverage value falls outside the definitive class lists. A smaller targeted audit will be used only to identify the observed pasture-age values from 1 through 99.

## 1. Band inventory

### Expected

- coverage contains 41 annual bands from `classification_1985` through `classification_2025`;
- no year is missing or duplicated;
- pasture age contains 41 bands ordered from 1985 through 2025.

### Observed

| Check | Expected | Observed | Result |
|---|---:|---:|---|
| Coverage band count | 41 | 41 | Pass |
| Coverage temporal range | 1985–2025 | 1985–2025 | Pass |
| Missing or duplicated coverage years | 0 | 0 | Pass |
| Pasture-age band count | 41 | 41 | Pass |

The first script version incorrectly generated expected names such as `classification_1985.0`. This produced false missing/unexpected-band messages. The displayed source-band inventory itself was complete, and version 2 corrected the formatting to integer years.

## 2. Projection and raster-grid alignment

### Confirmed

| Check | Coverage | Pasture age | Result |
|---|---|---|---|
| CRS | `EPSG:4326` | `EPSG:4326` | Pass |

### Affine transformation under review

An Earth Engine affine transform is represented as:

```text
[xScale, xShear, xOrigin,
 yShear, yScale, yOrigin]
```

The configuration currently records:

```text
[0.000269494585235856472, 0, -180,
 0, -0.000269494585235856472, 90]
```

The following comparisons remain to be recorded from version 2 of the audit:

| Comparison | Required assessment | Observed | Status |
|---|---|---|---|
| Coverage versus pasture-age pixel size | `xScale` and `yScale` equal within numerical precision | Pending | Pending |
| Coverage versus pasture-age shear | `xShear = 0` and `yShear = 0` | Pending | Pending |
| Coverage versus pasture-age origin | Origin differences equal zero or integer pixel offsets | Pending | Pending |
| Coverage versus configured transform | Same grid lattice, allowing integer-pixel origin offsets | Pending | Pending |

Exact equality of the six-element vectors is sufficient but not necessary for grid compatibility. If pixel sizes are identical, shear terms are zero, and the origin differences divided by pixel size are integers, the rasters share the same pixel lattice even if their stored origins differ. A non-integer offset would indicate subpixel misalignment and require an explicit resampling decision.

The values required from the console are `AUDIT 2D` through `AUDIT 2L`.

## 3. Analytical-grid integrity

| Check | Expected | Observed | Result |
|---|---:|---:|---|
| Feature count | 21,869 | 21,869 | Pass |
| Distinct `cell_id` count | 21,869 | 21,869 | Pass |
| Geometry type | Polygon | Polygon | Pass |
| Cells intersecting processing rectangle | 21,869 | 21,869 | Pass |
| Minimum geometry area (ha) | Near 20,000 | 20,043.00 | Pass |
| Mean geometry area (ha) | Near 20,000 | 20,078.35 | Pass |
| Maximum geometry area (ha) | Near 20,000 | 20,090.05 | Pass |
| Total geometry area (ha) | Descriptive | 439,093,417.72 | Recorded |

All retained cells have unique identifiers and areas consistent with the nominal 20,000-ha parent-grid design.

## 4. Coverage-code membership

The definitive coverage-code lists in `config/constants.js` were tested for the nine quinquennial reference years.

| Year | Unexpected coverage area (ha) | Result |
|---:|---:|---|
| 1985 | 0 | Pass |
| 1990 | 0 | Pass |
| 1995 | 0 | Pass |
| 2000 | 0 | Pass |
| 2005 | 0 | Pass |
| 2010 | 0 | Pass |
| 2015 | 0 | Pass |
| 2020 | 0 | Pass |
| 2025 | 0 | Pass |

This confirms that no observed coverage value falls outside the definitive Collection 11 class lists in the audited years. A complete area table for every valid coverage code is not required for this structural decision.

## 5. Coverage–pasture-age agreement

The following results are restricted to the rasterized retained analytical domain.

| Year | Coverage pasture (ha) | Pasture with age (ha) | Pasture without age (ha) | Age outside pasture (ha) |
|---:|---:|---:|---:|---:|
| 1985 | 49,230,180.85 | 49,230,180.85 | 0 | 0 |
| 1990 | 65,991,762.72 | 65,991,762.72 | 0 | 0 |
| 1995 | 79,813,506.01 | 79,813,506.01 | 0 | 0 |
| 2000 | 92,257,258.62 | 92,257,258.62 | 0 | 0 |
| 2005 | 103,241,477.19 | 103,241,477.19 | 0 | 0 |
| 2010 | 106,964,146.57 | 106,964,146.57 | 0 | 0 |
| 2015 | 106,355,143.99 | 106,355,143.99 | 0 | 0 |
| 2020 | 106,828,726.71 | 106,828,726.71 | 0 | 0 |
| 2025 | 109,107,701.29 | 109,107,701.29 | 0 | 0 |

Both disagreement rates are zero in every audited year:

```text
Pasture without age rate = pasture_without_age_ha / coverage_pasture_ha

Age outside pasture rate = age_outside_pasture_ha /
                           (pasture_with_age_ha + age_outside_pasture_ha)
```

The coverage and pasture-age products therefore show complete thematic presence/absence agreement under the grid used for the reduction. Final spatial-alignment acceptance remains conditional on the affine-transform assessment in Section 2.

## 6. Pasture-age encoding

### Confirmed results

| Year | Expected maximum 2xx code | Codes 101–200 (ha) | Above expected maximum (ha) | Codes 1–99 within pasture (ha) |
|---:|---:|---:|---:|---:|
| 1985 | 200 | 0 | 0 | 0.00 |
| 1990 | 205 | 0 | 0 | 294.52 |
| 1995 | 210 | 0 | 0 | 678.37 |
| 2000 | 215 | 0 | 0 | 1,032.33 |
| 2005 | 220 | 0 | 0 | 1,396.20 |
| 2010 | 225 | 0 | 0 | 1,529.50 |
| 2015 | 230 | 0 | 0 | 1,556.28 |
| 2020 | 235 | 0 | 0 | 1,680.48 |
| 2025 | 240 | 0 | 0 | 1,732.52 |

The area represented by values from 1 through 99 is small, reaching 0.00159% of mapped pasture in 2025. Its scientific effect is expected to be negligible, but the exact observed codes must be identified because the current decoding rule recognizes only code `100` and codes greater than `200`.

This is a pending encoding clarification, not evidence of coverage–age presence/absence disagreement.

## 7. Retained-cell endpoint check

The endpoint export contains one complete record for every retained cell, with no duplicated or missing identifiers.

| Endpoint category | Cells | Percentage of retained grid |
|---|---:|---:|
| Anthropogenic area in both 1985 and 2025 | 18,762 | 85.79% |
| Anthropogenic area only in 1985 | 6 | 0.03% |
| Anthropogenic area only in 2025 | 3,015 | 13.79% |
| No relevant anthropogenic area in either endpoint | 86 | 0.39% |
| **Total** | **21,869** | **100.00%** |

Of the retained cells, 21,783 pass the operational endpoint rule under `coverage_v3`. Eighty-six cells have no more than 0.01 ha of anthropogenic cover in either 1985 or 2025 and are therefore flagged as possible retained-cell inconsistencies.

The 86 cells must not simply be deleted from the existing layer. A valid canonical update requires reconstructing the selection from the complete parent grid because cells excluded under the historical working asset may now satisfy the inclusion rule under `coverage_v3`.

This audit checks the retained side of the historical selection only. It cannot identify newly eligible cells outside the retained layer.

## 8. Processing-footprint note

The rasterized retained domain has approximately 437,376,760.23 ha, whereas the sum of vector geometry areas is 439,093,417.72 ha. In addition, valid MapBiomas coverage occupies approximately 431.62 million ha inside the rasterized domain.

These quantities do not use identical measurement representations: the first is a pixel-grid representation, the second is a geodesic vector-area sum, and the third is limited by the valid footprint of the Brazil coverage product. The differences should therefore not be interpreted as missing analytical cells. The processing rectangle should nevertheless be widened or checked against full cell bounds in the reconstruction script so that intersection is not mistaken for complete containment.

## 9. Current audit outcome

### Status

`INCOMPLETE — CANONICAL REPROCESSING NOT YET AUTHORIZED`

### Components passed

- canonical asset identities;
- annual band counts and temporal coverage;
- retained-grid size, geometry, and identifier integrity;
- definitive coverage-code membership for the nine reference years;
- coverage–pasture-age thematic presence/absence agreement;
- upper-bound and 101–200 pasture-age validity tests.

### Pending components

- numerical assessment of the coverage, pasture-age, and configured affine transforms;
- identification and interpretation of pasture-age values from 1 through 99;
- reconstruction of the fixed analytical-domain selection from the complete parent grid using `coverage_v3`.

## 10. Required next decisions

1. Accept or correct the configured raster transform after testing lattice compatibility.
2. Define the treatment of observed pasture-age values from 1 through 99.
3. Reconstruct the endpoint selection from the parent grid using the canonical coverage asset.
4. Compare the reconstructed domain with `grade_hex_CeAmz_selecao` before any cell is added or removed.
5. Begin canonical stock-and-flow reprocessing only after these items are resolved and recorded.

## 11. Files produced

| File | Role | Status |
|---|---|---|
| `gee/01_audit_canonical_inputs.js` | Audit implementation, version 2 | Complete |
| `canonical_input_audit_c11_v3_domain.csv` | Nine-year domain summary | Complete |
| `canonical_endpoint_rule_c11_v3_by_cell.csv` | Retained-cell endpoint audit | Complete |
| `canonical_code_inventory_c11_v3_domain.csv` | Full grouped inventory | Cancelled; superseded by targeted age-code audit |
| `docs/validation/canonical_input_audit.md` | Permanent audit record | Updated; pending final checks |

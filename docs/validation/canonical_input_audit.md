# Canonical input audit

- **Status:** Input audit complete with one documented encoding exception; parent-grid domain reconstruction remains required before canonical reprocessing
- **Audit script:** `gee/01_audit_canonical_inputs.js`, version 3
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
| Script version | Version 3 |
| Annual-summary export | Completed |
| Endpoint-by-cell export | Completed |
| Targeted low-age-code export | Completed |
| Full code-inventory export | Cancelled after more than eight hours |
| Annual-summary file | `canonical_input_audit_c11_v3_native_grid_domain.csv` |
| Endpoint file | `canonical_endpoint_rule_c11_v3_native_grid_by_cell.csv` |
| Low-age-code file | `canonical_low_age_codes_c11_v3_native_grid.csv` |

The full code-inventory task was cancelled because it repeated grouped reductions across the complete domain for two variables and nine years. The completed annual audit already tests whether any coverage value falls outside the definitive class lists. It was replaced by a targeted audit of pasture-age values from 1 through 99.

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

An Earth Engine affine transform is represented as:

```text
[xScale, xShear, xOrigin,
 yShear, yScale, yOrigin]
```

The canonical coverage transform is:

```text
[0.00026949458523585647, 0, -74.02073025380652,
 0, -0.00026949458523585647, 5.405791885246045]
```

| Check | Coverage | Pasture age | Result |
|---|---|---|---|
| CRS | `EPSG:4326` | `EPSG:4326` | Pass |
| Nominal scale | 30.000000000000004 m | 29.999999999999996 m | Pass; numerical precision only |
| Shear terms | 0 | 0 | Pass |
| Origin relationship | Reference | Offset by 76 columns and 2,205 rows | Pass; integer-pixel offsets |

The two source rasters therefore share the same pixel lattice. The former configured origin `[-180, 90]` was not aligned with this lattice and was replaced by the native coverage transform in `config/constants.js`. Coverage is the primary accounting source, so its transform is the canonical processing grid. Version 3 outputs record this CRS and transform explicitly.

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
| 1985 | 49,229,391.04 | 49,229,391.04 | 0 | 0 |
| 1990 | 65,991,036.96 | 65,991,036.96 | 0 | 0 |
| 1995 | 79,812,774.25 | 79,812,774.25 | 0 | 0 |
| 2000 | 92,256,612.50 | 92,256,612.50 | 0 | 0 |
| 2005 | 103,240,899.11 | 103,240,899.11 | 0 | 0 |
| 2010 | 106,963,635.56 | 106,963,635.56 | 0 | 0 |
| 2015 | 106,354,722.69 | 106,354,722.69 | 0 | 0 |
| 2020 | 106,828,345.97 | 106,828,345.97 | 0 | 0 |
| 2025 | 109,107,358.13 | 109,107,358.13 | 0 | 0 |

Both disagreement rates are zero in every audited year:

```text
Pasture without age rate = pasture_without_age_ha / coverage_pasture_ha

Age outside pasture rate = age_outside_pasture_ha /
                           (pasture_with_age_ha + age_outside_pasture_ha)
```

The coverage and pasture-age products therefore show complete thematic presence/absence agreement on the accepted native grid.

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

The targeted inventory established that **code `1` is the only observed value from 1 through 99**. No low code occurs in 1985; code `1` occurs in every audited quinquennial year from 1990 through 2025. The targeted areas reconcile with the annual summary to less than 0.000001 ha, which is numerical reduction noise.

The formal MapBiomas pasture-age legend defines code `100` for pasture established by 1985 and codes `200 + consecutive age` for pasture established after 1985. Under that formal encoding, code `1` has no stated role. The MapBiomas access page also contains an example visualization described as `0 = no pasture` and `1–40+ = consecutive age`, creating an internal documentation ambiguity for the public asset. Source: <https://brasil.mapbiomas.org/iniciativas-e-produtos/cobertura-e-uso-da-terra/pastagem/idade/>.

Code `1` occupies only 1,732.52 ha in 2025, or 0.00159% of mapped pasture in the retained domain. It is retained in total pasture area because coverage class `15` is authoritative for land-cover membership, but it must not be assigned to an age cohort without an explicit rule. The recommended provisional treatment is `age unresolved`: include it in pasture stock and land-cover transitions, exclude it from age-specific cohort statistics, report its area, and test whether its exclusion changes any age-dependent result. Reclassification to `201` requires confirmation from the product documentation or MapBiomas team.

## 7. Retained-cell endpoint check

The endpoint export contains one complete record for every retained cell, with no duplicated or missing identifiers.

| Endpoint category | Cells | Percentage of retained grid |
|---|---:|---:|
| Anthropogenic area in both 1985 and 2025 | 18,761 | 85.79% |
| Anthropogenic area only in 1985 | 6 | 0.03% |
| Anthropogenic area only in 2025 | 3,015 | 13.79% |
| No relevant anthropogenic area in either endpoint | 87 | 0.40% |
| **Total** | **21,869** | **100.00%** |

Of the retained cells, 21,782 pass the operational endpoint rule under `coverage_v3`. Eighty-seven cells have no more than 0.01 ha of anthropogenic cover in either 1985 or 2025 and are therefore flagged as possible retained-cell inconsistencies.

The 87 cells must not simply be deleted from the existing layer. A valid canonical update requires reconstructing the selection from the complete parent grid because cells excluded under the historical working asset may now satisfy the inclusion rule under `coverage_v3`.

Native-grid processing added one flag relative to the provisional transform: `cell_id = 41199`, `GRID_ID = EZ-35`. The non-native reduction had assigned 0.121993 ha of anthropogenic cover to this cell in 2025; the native-grid result is zero. This single-pixel-scale change illustrates why the native transform matters for threshold decisions even though aggregate-area differences are negligible.

This audit checks the retained side of the historical selection only. It cannot identify newly eligible cells outside the retained layer.

## 8. Processing-footprint note

The native-grid rasterized retained domain has approximately 437,376,710.28 ha, whereas the sum of vector geometry areas is 439,093,417.72 ha. In addition, valid MapBiomas coverage occupies approximately 431.62 million ha inside the rasterized domain.

These quantities do not use identical measurement representations: the first is a pixel-grid representation, the second is a geodesic vector-area sum, and the third is limited by the valid footprint of the Brazil coverage product. The differences should therefore not be interpreted as missing analytical cells. The processing rectangle should nevertheless be widened or checked against full cell bounds in the reconstruction script so that intersection is not mistaken for complete containment.

## 9. Current audit outcome

### Status

`INPUT AUDIT COMPLETE WITH DOCUMENTED EXCEPTION — DOMAIN RECONSTRUCTION REQUIRED BEFORE CANONICAL REPROCESSING`

### Components passed

- canonical asset identities;
- annual band counts and temporal coverage;
- retained-grid size, geometry, and identifier integrity;
- definitive coverage-code membership for the nine reference years;
- coverage–pasture-age thematic presence/absence agreement;
- upper-bound and 101–200 pasture-age validity tests;
- native raster-lattice alignment;
- targeted identification of low pasture-age values.

### Documented exception

- code `1` occurs inside a very small area classified as pasture but is not resolved by the formal `100`/`2xx` encoding rule;
- total pasture accounting remains valid because coverage class `15` is authoritative;
- age-dependent analysis requires the provisional `age unresolved` treatment or later source confirmation.

### Remaining prerequisite

- reconstruction of the fixed analytical-domain selection from the complete parent grid using `coverage_v3`.

## 10. Required next decisions

1. Confirm or revise the provisional `age unresolved` treatment for code `1`.
2. Reconstruct the endpoint selection from the parent grid using the canonical coverage asset and native transform.
3. Compare the reconstructed domain with `grade_hex_CeAmz_selecao` before any cell is added or removed.
4. Begin canonical stock-and-flow reprocessing only after the domain comparison is resolved and recorded.

## 11. Files produced

| File | Role | Status |
|---|---|---|
| `gee/01_audit_canonical_inputs.js` | Audit implementation, version 3 | Complete |
| `canonical_input_audit_c11_v3_native_grid_domain.csv` | Nine-year native-grid domain summary | Complete |
| `canonical_endpoint_rule_c11_v3_native_grid_by_cell.csv` | Native-grid retained-cell endpoint audit | Complete |
| `canonical_low_age_codes_c11_v3_native_grid.csv` | Targeted inventory of age values 1–99 | Complete; only code `1` observed |
| `canonical_code_inventory_c11_v3_domain.csv` | Full grouped inventory | Cancelled; superseded by targeted age-code audit |
| `docs/validation/canonical_input_audit.md` | Permanent audit record | Updated with completed input audit |

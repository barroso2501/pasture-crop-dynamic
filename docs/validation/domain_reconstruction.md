# Analytical-domain reconstruction

- **Status:** Endpoint membership completed and validated; final asset materialization pending
- **Last updated:** 2026-09-11
- **Decision:** `docs/decisions/004_canonical_domain_reconstruction.md`
- **Method:** `docs/methods/study_domain.md`
- **Configuration:** `config/constants.js`

## Purpose

This validation reconstructs the fixed Cerrado-Amazon analytical domain from
canonical source assets and an explicit endpoint rule. Agreement with the
historical ArcGIS-derived grid is recorded for provenance only and is not an
acceptance criterion.

## Canonical inputs

| Role | Asset or field |
|---|---|
| Parent 20,000-ha hexagonal grid | `projects/ee-barroso2501/assets/grade_20mil_ha` |
| IBGE 2025 biomes | `projects/ee-barroso2501/assets/biomas_IBGE` |
| Biome-code field | `CD_BIOMA` (string) |
| Target biome codes | Amazonia `1`; Cerrado `3` |
| Materialized candidate grid | `projects/ee-barroso2501/assets/grade_hex_CeAmz_candidates_ibge2025` |
| Historical grid, provenance only | `projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao` |
| Endpoint coverage | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3` |
| Endpoint years | 1985 and 2025 |
| Cell identifier | `cell_id` |
| Processing CRS | `EPSG:4326` |
| Endpoint tolerance | 0.01 ha |

The canonical affine transform is:

```text
0.00026949458523585647, 0, -74.02073025380652,
0, -0.00026949458523585647, 5.405791885246045
```

## Reconstruction rule

Complete parent-grid hexagons intersecting Amazonia or Cerrado are retained as
the spatial candidate population. Their geometries are not clipped to biome
boundaries.

Recognized anthropogenic area is the sum of the canonical `PAS`, `TMP`, `OAG`,
and `OUT` groups. A candidate cell is retained when:

```text
anthropogenic_1985_ha > 0.01
OR
anthropogenic_2025_ha > 0.01
```

Native vegetation, water, class 27, masked area, and unexpected codes are not
silently interpreted as anthropogenic.

## Implemented scripts

| Stage | Script | Function |
|---|---|---|
| Candidate materialization | `gee/02a_materialize_candidate_grid.js` | Materializes the spatial join before raster processing |
| Candidate audit | `gee/02b_audit_candidate_grid.js` | Checks identifiers, geometry, properties, and batches |
| Diagnostic pilot | `gee/02c_reconstruct_domain_endpoints_b00.js` | Processes `b00` with endpoint and coverage diagnostics |
| Lean pilot | `gee/02d_reconstruct_domain_endpoints_b01.js` | Tests the two-band production configuration on `b01` |
| Remaining batches | `gee/02e_reconstruct_domain_endpoints_b02_b07.js` | Processes `b02` through `b07` with the validated lean configuration |

The superseded scripts `gee/02_reconstruct_analytical_domain.js` and
`gee/02_reconstruct_analytical_domain_v3.js` must not be rerun.

## Candidate-grid audit

The materialized candidate grid passed the structural audit.

| Check | Result |
|---|---:|
| Candidate cells | 32,305 |
| Distinct `cell_id` values | 32,305 |
| Distinct `GRID_ID` values | 32,305 |
| Non-polygon geometries | 0 |
| Invalid batch identifiers | 0 |
| Minimum geometry area | 20,042.998 ha |
| Mean geometry area | 20,081.133 ha |
| Maximum geometry area | 20,090.053 ha |

## Endpoint results by batch

| Batch | Candidate cells | Retained | Excluded | Historical members among candidates |
|---:|---:|---:|---:|---:|
| `b00` | 4,040 | 3,168 | 872 | 2,690 |
| `b01` | 4,041 | 3,128 | 913 | 2,727 |
| `b02` | 4,034 | 3,061 | 973 | 2,696 |
| `b03` | 4,043 | 3,118 | 925 | 2,667 |
| `b04` | 4,038 | 3,104 | 934 | 2,691 |
| `b05` | 4,036 | 3,105 | 931 | 2,706 |
| `b06` | 4,037 | 3,088 | 949 | 2,687 |
| `b07` | 4,036 | 3,117 | 919 | 2,667 |
| **Total** | **32,305** | **24,889** | **7,416** | **21,531** |

The reconstructed domain retains 77.044% of the spatial candidate population.

## Combined integrity checks

The eight CSV files were combined and independently checked after export.

| Check | Result |
|---|---:|
| Total rows | 32,305 |
| Unique `cell_id` values | 32,305 |
| Unique `GRID_ID` values | 32,305 |
| Duplicate identifiers | 0 |
| Missing common fields | 0 |
| Missing batches | 0 |
| Incorrect `cell_id modulo 8` assignments | 0 |
| Incorrect maximum-endpoint calculations | 0 |
| Incorrect membership assignments | 0 |
| CRS values | One: `EPSG:4326` |
| Affine transforms | One canonical transform |
| Coverage assets | One canonical `coverage_v3` asset |
| Candidate-grid assets | One materialized candidate asset |

The diagnostic `b00` export also found no unexpected coverage codes and no
class-27 area. Its recognized categories reconciled with valid raster area to
within floating-point precision.

## Numerical-tolerance check

Of the 7,416 excluded cells:

- 7,414 have exactly zero recognized anthropogenic area in both endpoints; and
- two have a positive endpoint area below the 0.01-ha tolerance.

| `cell_id` | `GRID_ID` | Batch | Endpoint | Anthropogenic area |
|---:|---|---:|---:|---:|
| 21,346 | `AJ-111` | `b02` | 1985 | 0.002422 ha |
| 42,381 | `FC-27` | `b05` | 2025 | 0.006657 ha |

Both cells were absent from the historical domain. Retaining all positive
values instead of applying the documented tolerance would increase the
canonical domain from 24,889 to 24,891 cells. The adopted 0.01-ha tolerance is
therefore consequential for only two of 32,305 candidates.

## Historical comparison

The historical grid is not used to determine canonical membership. The full
comparison is:

| Membership status | Cells |
|---|---:|
| Present in both the reconstructed and historical domains | 20,480 |
| Present only in the reconstructed domain | 4,409 |
| Historical candidate cells excluded by the endpoint rule | 1,051 |
| Historical cells outside the canonical candidate population | 338 |
| Total present only in the historical domain | 1,389 |

The reconstructed domain has 3,020 more cells than the 21,869-cell historical
domain. This difference is a provenance result and does not indicate failure
of the canonical reconstruction.

## Boundary-cell observation

The diagnostic `b00` output showed that 118 of 4,040 cells had valid
MapBiomas coverage over less than 99% of their complete geometry. This pattern
is consistent with cells at the edge of the Brazilian raster support because
cells are retained as complete hexagons after spatial intersection, although
the pilot CSV alone does not locate them spatially. Class areas still
reconciled exactly within the valid raster support. Downstream analyses must
preserve the documented distinction between complete cell geometry and the
area represented by valid MapBiomas pixels.

## Execution record

### Diagnostic pilot `b00`

| Field | Value |
|---|---|
| Task | `canonical_domain_endpoints_c11_v3_b00_v1` |
| Task ID | `6GOYDREE2XJQJM4LPXV56J2S` |
| Status | Completed, attempt 1 |
| Start | 2026-09-10 15:35:33, UTC-03:00 |
| Runtime | 13 minutes |
| Batch compute usage | 203,414.7188 EECU-seconds |
| Raster bands | 10 diagnostic bands |

### Lean pilot `b01`

| Field | Value |
|---|---|
| Task | `canonical_domain_endpoints_c11_v3_b01_v1` |
| Task ID | `SBLW7AH7OBHSIOKJDDLEISYZ` |
| Status | Completed, attempt 1 |
| Start | 2026-09-10 18:03:05, UTC-03:00 |
| Runtime | 2 minutes |
| Batch compute usage | 157,960.0938 EECU-seconds |
| Raster bands | 2 production bands |

The `b02`-`b07` output files were received and validated on 2026-09-11. Their
task IDs, runtimes, and EECU use were not supplied and are not required to
validate the analytical content of the exported files.

## Evidence files

The combined evidence archive is:

```text
canonical_domain_endpoints_c11_v3.zip
```

It contains one CSV for each batch, `b00` through `b07`.

## Earlier failed implementations

### Version 1

The first national task failed because `maxPixelsPerRegion = 1,000,000` was
below the number of pixel-band inputs required by the largest cell.

- Task ID: `3IGMS65HK43UTULRSWJF7SPP`
- Batch compute usage: approximately 5,079.50 EECU-seconds

### Version 2

The second national task passed the per-cell limit but timed out after 12
hours. No output was produced.

- Task ID: `MYFZR3NCDR4VYHZL3UXGBTY2`
- Batch compute usage: 72,545.0156 EECU-seconds

### Version 3 before materialization

The first partitioned attempt still embedded an unmaterialized spatial join in
the raster graph. Batch `b00` timed out without producing an output.

- Task ID: `5FJWX2WGF73EHHB25YWJFFMJ`
- Runtime: approximately 29 minutes
- Batch compute usage: 695,217.1250 EECU-seconds

The successful workflow materialized the candidate grid before performing any
raster reduction.

## Validation decision

The endpoint calculation is accepted because:

- all 32,305 candidate cells were processed exactly once;
- identifiers and deterministic batch assignments are complete and unique;
- every membership value reproduces the documented endpoint rule;
- all outputs use one canonical coverage asset, CRS, transform, and tolerance;
- the pilot diagnostics found no unexpected codes or class-27 area; and
- the 0.01-ha tolerance affects only two explicitly identified cells.

No additional cell-level disagreement investigation is required. The next
step is to materialize the 24,889 retained cells as a new versioned Earth
Engine asset and then update `config/constants.js` to reference that asset.

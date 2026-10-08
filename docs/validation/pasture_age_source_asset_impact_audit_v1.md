# Pasture-age source-asset impact audit — Decision 024 criterion 11

**Status:** Full canonical-domain audit validated (`criterion_11: PASS`).  
**Scope:** 24,889 canonical cells; annual observations 1985–2025.  
**Validator:** `17v_validate_pasture_age_source_audit_v2.py`.  
**Decision 024 overall:** still open (`decision_024_fully_implemented: false`).

## Purpose and accepted inputs

The audit measures two issues in the public MapBiomas Collection 11
pasture-age asset: raw value `1`, and raw `100` assigned during a pasture
spell that the annual **coverage** sequence independently classifies as a
post-1985 observed entry. Source age codes are not used to assign corrected
pasture-spell origin. Definitions and units are specified in
`docs/methods/pasture_age_source_asset_audit.md`.

The full validation record authenticates the corrected canonical panel v2
(`ef3589be99e3a2cdc1c2245a15cedd090c8255775b34f14d4f2f27d3f9f8faa7`)
and spatial support v1
(`22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc`),
as well as all 16 raw GEE batch CSVs. The accepted two-cell pilot was
reproduced from the full exports. The per-cell output contains one record per
canonical `cell_id`; eight disjoint batches contain 24,889 cells in total.

## Validated findings

| Longitudinal measure | Affected cells | Unique area (ha) |
| --- | ---: | ---: |
| Raw age code `1` at least once | 350 | 2,142.786 |
| Confirmed reuse of `100` in a post-1985 observed PAS spell | 15,828 | 9,061,284.261 |
| Both anomalies in the **same pixel** in any years | 0 | 0 |

The four-category joint table closes over 160,545,660.889 ha of raster area
in the ever-PAS-or-code-`1` audit cohort. Its categories are `none`
(151,482,233.843 ha), `code1_only` (2,142.786 ha), `reuse100_only`
(9,061,284.261 ha), and `both` (0 ha). **This is a pixel-level partition:**
324 cells have both anomaly types in *different pixels* despite zero
longitudinal overlap within a pixel. The cell counts across joint categories
must not be added as if the categories partitioned cells.

The 350 affected code-`1` cells consist of 312 Amazon–Cerrado transbiome
cells and 38 cells without that specific overlap. The latter are associated
with other study-domain boundaries in the separately accepted native-pixel
diagnosis; the present primary-biome summary alone does not locate the
external biome or pixel-level biome intersection. Across the full audit,
code `1` contributes 46,071.502 ha·year and occurs only with observed PAS:
the non-PAS and uncertain-coverage components are zero. The unique affected
area of 2,142.786 ha must not be confused with its time-integrated area.

Confirmed reused `100` contributes 138,085,523.903 ha·year. Another
892.362 ha·year of code `100` in 63 cells occurs with PAS of **unresolved
spell origin**; it is reported separately and not counted as confirmed
reuse. The annual records include 2021–2025 with
`diagnostic_extension = 1`.

The large confirmed reuse area makes direct use of raw code `100` for
post-1985 origin attribution untenable. These source-asset counts do not
revise the corrected PAS→TMP origin shares, measure an additional conversion
flow, or establish why MapBiomas generated either code behavior.

## Checks and artifacts

The validation JSON reports `status: PASS`, `mode: full`, 41 years,
`criterion_11: PASS`, and a maximum internal residual of
`1.4081633707974106e-06` (below the prespecified `0.001` tolerance for
the cell-level comparisons). An independent check of the submitted raw
CSVs found 24,889 unique cell IDs, reproduced the joint and annual totals,
and confirmed the listed output hashes. The package includes:

| Repository path | SHA-256 in validation JSON |
| --- | --- |
| `outputs/summary/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_annual_v1.csv` | `b03024faf341d9ab92a0ccf31804fcd6b0a288fc64606c210b4d9987472ccd6a` |
| `outputs/summary/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_joint_v1.csv` | `a90634cb75428df47d4c75612e2422f9a2009564710fa16bbbedda14f72c37f6` |
| `outputs/summary/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_biome_v1.csv` | `081d41285778585805a348ce922b38f533a33d311307f32524f5c0fc87c92940` |
| External cell table `spatial/phase9/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_cell_v1.parquet` | `ec09f45c79452b0142495493d6160ff0bf8a3c33641384bfd5ddd851fb0ff2d5` |

`outputs/validation/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_validation_v1.json`
holds the complete list of input hashes and the output status. The 16 raw
batch CSVs and the cell Parquet remain in project storage; their hashes
allow later verification without duplicating these cell-level data in GitHub.

## Limits and next gate

The GEE script hash is `null` in the validation JSON because the script was
run separately in the Code Editor. Thus the record authenticates the
exports and their checks, but cannot prove byte-for-byte identity of the
executed Code Editor text. The audit covers the canonical domain, not the
entire public asset. The cause and official semantics of source code `1`
remain for MapBiomas to confirm.

Criterion 11 is complete. Decision 024 is **not** closed by this result:
the fixed-1985 cohort/RQ1 baseline still requires explicit revalidation,
and criterion 12 requires a final, versioned evidence and status review.
P9A035–P9A037 remain suspended until that review authorizes new findings;
historical evidence files and suspension events must not be rewritten.

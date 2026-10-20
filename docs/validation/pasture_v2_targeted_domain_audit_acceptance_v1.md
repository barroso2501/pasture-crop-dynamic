# Pasture-origin-age v2 — targeted domain audit accepted

Date: 2026-10-20. Status: **ACCEPTED for the specified coding and temporal-consistency controls, selected 21,869-cell domain, 1985–2025.** This closes the 82-cell coverage-list qualification. No canonical source migration or accounting rerun is authorized by this record.

## Evidence and reproducibility

Native recheck `20261020151405` supplies all 82 expected identities with zero missing reductions. The v3 validator passes native synthetic fixtures, image band/output order, runtime metadata, crosswalk, positive geometry areas, constant support, raw-property/CSV equality and all temporal controls. The direct and collection reductions are both complete and identical on the real preflight cell IC-201 (cell_id 5045); production uses the mapped direct reduction. This two-method comparison is for one cell, not all 82. All 82 exported rows separately pass transport and audit validation.

The original return is preserved at `outputs/native/pasture_v2_coverage_recheck82_v3/pasture_v2_coverage_recheck82_20261020151405_v3.csv`, SHA-256 `04eca93b8c1820030241a532afc42014968e55afebc7d1bf7569786d2c322f10`. The accompanying validation JSON pins config, return, parent report, eight parent CSVs and derived outputs. Run from repository root:

```bash
python3 analysis/validate_pasture_v2_recheck82_v3.py outputs/native/pasture_v2_coverage_recheck82_v3/pasture_v2_coverage_recheck82_20261020151405_v3.csv
```

The derived combined panel contains 82 newly rechecked rows and 21,787 explicitly labeled unchanged parent rows. This is not a new full-domain raster execution. Parent CSVs and the immutable parent validation remain unchanged. Added known codes could not affect parent rows without the former unknown-code flag: an observed added code would necessarily have set that flag. Reuse assumes unchanged contents of the referenced age/coverage assets; remote raster bytes were not independently hashed.

## Findings

| Cell occurrence indicator, any pixel/year in selected domain | Cells |
|---|---:|
| Literal age code 1 | 0 |
| Age 100 in PAS after recognized non-PAS | 0 |
| Ordered 100 reuse after observed exit | 0 |
| Age 100 without confirmed continuous initial PAS | 0 |
| Age 100 after gaps only | 0 |
| Age 100 outside recognized PAS | 0 |
| Positive age outside recognized PAS | 0 |
| PAS with masked age | 0 |
| PAS with zero age | 0 |
| Unexpected numeric age code under audited rules | 0 |
| Remaining unknown coverage code | 0 |
| PAS present in at least one year | 21,036 |
| Age family 100 present in at least one year | 16,004 |
| Age family 2xx present in at least one year | 21,033 |
| Recognized coverage present in at least one year | 21,869 |

These are cell-level occurrence flags, not pixels, hectares, event counts or age distributions. The two main temporal anomalies and literal age 1 are not detected on the selected support under these rules. No claim of validated numerical age at every pixel/year follows.

All 82 former unknown-coverage flags are explained by coverage codes 75 and/or 91: 60 cells contain 75, 24 contain 91, and two contain both (58 only 75; 22 only 91). No selected cell lacks both. The other added codes 1, 10, 22, 26 and 84 are absent from this recheck. Coverage 27 remains NODATA; coverage code 1 remains distinct from age code 1. All 82 changed flag values are the old unknown-coverage flag changing from 1 to 0. No other audit flag changes.

## Scope and next work

This result closes the targeted audit of the new MapBiomas pasture-origin-age v2 source on `projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao` (21,869 cells), distinct from the canonical 24,889-cell analytical grid. It supports reporting that the specified anomalies were not detected in the new asset on this support. It does not establish absence across Brazil, a matched old/new national difference, complete correctness of all ages or quantitative improvement outside the audit.

No further 82-cell or eight-batch execution is needed for this audit. Existing rejected v1/v2.1 returns and earlier test failures remain historical evidence. The script's distributed SHA is recorded separately from the still-null operator-attested executed-text hash.

Evidence matrix v4.3 and cumulative events-v5 remain current; accepted canonical accounting is unchanged. Numerical-age 201 native assurance, entry/re-entry chronology, annual uncertain-pair full-domain tables, historical operator hashes and DOI release retain their separate status. The immediate next project step is to validate the full annual uncertain-pair cross-tab, if its outputs are available, or execute its already-prepared full script; this is not required to accept the present targeted audit.

> Historical status/instructions. On 2026-10-20 the targeted audit was accepted; no rerun is needed. Current: [acceptance record](../validation/pasture_v2_targeted_domain_audit_acceptance_v1.md).

# Targeted new-age audit: complete domain, one coverage-list qualification

Review date: 2026-10-19. **File integrity PASS; scientific interpretation remains qualified by 82 coverage-unknown cells.** Native run `20261016150312` covers 1985–2025 on `projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao`. All eight CSVs were received in `drive-download-20261019T145422Z-1-001.zip`. The immutable v1.2 validation JSON and original native CSV bytes are included in the package.

## Observed results

| Measure | Cells |
|---|---:|
| Expected and validated, unique IDs | 21,869 |
| Literal age code 1 detected | 0 |
| Age 100 in PAS after a recognized non-PAS observation | 0 |
| Ordered reuse: 100 in PAS, non-PAS, then 100 in PAS | 0 |
| Age 100 in PAS without confirmed continuous initial PAS | 0 |
| Age 100 after coverage gaps only | 0 |
| Age 100 or positive age outside recognized PAS | 0 |
| PAS with masked or zero age | 0 |
| Unexpected numeric age code | 0 |
| Observed coverage outside the audit's recognized list | **82** |
| PAS detected in some year | 21,036 |
| Age family 100 detected | 16,004 |
| Age family 2xx detected | 21,033 |
| Recognized coverage detected in some year | 21,869 |

Counts are cells with at least one occurrence in any pixel/year; not pixel counts, area or events. The eight batches contain 2,771; 2,741; 2,778; 2,730; 2,700; 2,752; 2,740; and 2,657 rows. Every required indicator is binary and non-null. All grid/cell IDs and runtime metadata are complete and consistent. The remaining metadata qualification is not a missing CSV or failed task.

## Coverage-list defect

The standalone audit's 32-code `KNOWN` list omitted **1, 10, 22, 26, 75, 84 and 91**, which are recognized in the project's canonical class configuration. The source configuration has 40 codes including 27; **27 remains NODATA**, so the corrected audit recognizes 39 observed land-cover codes and does not turn NODATA into confirmed non-PAS. Coverage code 1 must not be confused with the literal **age** code 1 being audited.

The parent `coverage_unknown_code=1` identifies 82 affected cells, including 80 with some PAS and 76 with some age 100. Those cell-level overlaps do not prove that the unknown observation and age 100 occur at the same pixel or time. The CSV contains presence flags, not the actual unknown code, so we cannot yet attribute the 82 cases to any particular omitted code or rule out genuinely unexpected coverage values.

The literal age-code-1 flag does not depend on coverage classification: no literal 1 was detected in the observed age raster on this domain. The 100-consistency flags depend on coverage states. Their zeros are favorable but should retain the coverage qualification until the affected cells are checked. No positive error in the new age raster has been established by the 82-cell control.

The omission is in the standalone auditor's list. It does not establish a defect in the MapBiomas coverage asset, nor alter the canonical project configuration or previously accepted canonical panels.

## Minimal correction and evidence reuse

`gee/recheck_pasture_v2_82cells_v1.js` creates **one new task** on exactly these 82 complete cell geometries, with the same 41 years, coverage/new-age assets, native projection and tileScale 16. It reruns the unchanged temporal engine using the corrected 39-code list, exports separate presence flags for each added coverage code, reproduces the original unknown-coverage condition and records extrema if any true unknown coverage code remains. Age 1, zero, masking and all existing controls remain in the output. No age-old product or whole-domain rerun is included.

The selected IDs and parent validation hash are pinned in `config/pasture_v2_coverage_recheck_82_v1.json`. The accompanying validator requires the exact 82 IDs and metadata, then creates a **new derived combined panel** with 82 rechecked rows and 21,787 labeled reused rows. It never edits parent CSVs or the original validation JSON.

Reuse outside the 82 cells has a specific justification: every newly recognized code is neither 0 nor 27 and lay outside the former known list. Any observed occurrence would therefore have set the former unknown flag. Where that flag is zero, the expanded list cannot change the coverage states or temporal indicators, under the same referenced asset contents. Remote raster content is not independently hashed, and no fresh raster execution is claimed for reused rows.

If any unknown coverage or other control persists, the combined conclusion remains qualified. If a corrected indicator turns positive, it must be reported as a finding. Even an unqualified result is limited to this selected 21,869-cell domain and to the specified coding/consistency tests; it does not validate every numerical age or establish absence across Brazil.

## Governance and assurance

The parent validation's `PASS` concerns file integrity. Its `NAO_DETECTADO_COM_PENDENCIAS` verdicts and recorded coverage control remain unchanged. Its inherited prose limitation mentions smoke mode; the structured `mode: domain`, `rows_validated: 21869`, complete batch inventory and this review specify the actual accepted scope. This wording is documented here rather than silently editing a historical JSON.

The recheck passes 14 retained scalar test cases and three added coverage regressions, including preservation of the NODATA distinction. Six file-validator integration tests pass on temporary synthetic data. These are local software checks; **native execution of the 82-cell recheck is pending**. Original full exports were supplied by the operator; executed-text hashes remain null without operator attestation.

This targeted source audit remains separate from numerical-age 201 assurance, entry/re-entry analysis, the annual uncertain-pair cross-tab and public DOI release. It does not migrate the canonical source, change evidence matrix v4.3/events-v5, or rerun the stock-flow accounting.

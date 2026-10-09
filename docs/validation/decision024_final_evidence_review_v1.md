# Decision 024 — final evidence and acceptance review

**Date:** 2026-10-08. **Status:** PASS. **Current evidence edition:** v4.  
**Governance:** `docs/decisions/024_implementation_closure_v1.md`.  
**Scope:** technical completion of the observed-pasture-spell remediation and corrected RQ2 evidence.

## Checks performed in this review

The original 35-row matrix v3 was authenticated against its accepted terminology-validation hash. The eight final origin-by-destination cell CSVs were read independently, matched to their accepted validation hashes and 17p input inventory, and checked for identical 24,889-cell populations, unique keys, valid numeric areas, diagnostic flags, and complete origin/destination/stock identities. Their TMP-origin totals reproduce the accepted corrected interval and pooled summaries. The 17o, 17p, boundary-event, source-impact, and RQ1 records were reconciled through their shared hashes.

The exact preflight JavaScript functions passed ten prespecified histories and the entry/termination-year check under a local scalar test configuration. The production categorical state-update code passed 9,330 histories of up to five observations across PAS, valid non-PAS, NODATA, masked, and unexpected inputs, plus continuous histories extending through 2025. These checks inspect source logic and are not a new native-raster execution or proof of Code Editor text identity. The accepted complete audits supply the raster/export execution evidence.

Independent full-cell closure residual maximum: **1.45519152284e-11 ha/cell**. Maximum corrected TMP-origin aggregate difference from the accepted interval summary: **2.32830643654e-10 ha**. The accepted 17m tolerance is 0.01 ha/cell; compact summary comparisons in this review use 0.001 ha. The underlying full cell data remain external, with hashes listed in the input inventory.

## Acceptance criteria

| Decision 024 criterion | Status | Basis |
| --- | --- | --- |
| 1. Synthetic temporal tests | PASS | 10 exact preflight cases plus 9,330 production-state histories passed; scalar operations, not a native GEE rerun |
| 2. Annual chronological coverage | PASS | 41 annual audit rows, 1985-2025; ascending production year loops |
| 3. Single reconstructed origin per observed PAS pixel | PASS | Single categorical update, disjoint masks by state; complete accepted origin partitions |
| 4. No reconstructed 100 after observed interruption | PASS | Initial state can continue only from INITIAL; all interrupted test histories follow the reset/gap rules |
| 5. Observed re-entry starts at 201 | PASS | Auxiliary-age synthetic cases and production NEW-state reset after confidently observed non-PAS |
| 6. Uncertain histories explicit | PASS | Gap, masked, unexpected, and 1985-unobserved tests pass; unresolved component retained in all summaries |
| 7. Origin/destination/observation-loss/stock closure | PASS | Eight complete cell CSVs independently read and reconciled; limits and original validators retained |
| 8. Eight intervals, unique canonical cells | PASS | 24,889 unique and identical cell sets in each of eight intervals |
| 9. Non-origin invariance | PASS | Accepted 17o dependency-chain gate plus 17p corrected-panel comparison, linked by hashes; no independent re-export of other raster flows |
| 10. 2024-2025 boundary event type/year | PASS | Full v2 boundary validation PASS, 99,556 rows, zero raster mismatches |
| 11. Source-code anomaly/overlap audit | PASS | Full-domain 41-year audit PASS; annual summary linked to both source audit and RQ1 revalidation |
| 12. Complete records/hashes/corrected evidence | PASS | Matrix v4, exact three-finding revision crosswalk, append-only cumulative status events v2, corrected figure, acceptance record and inventory |

## Finding and status checks

- Matrix v4 has 35 unique findings, with identity and order preserved.
- Only P9A035–P9A037 change their substantive fields; the other 32 retain all prior field values except the edition identifier.
- Corrected source-relative paths and SHA-256 values refer to accepted v2 interval/pooled summaries.
- All causal-claim flags remain zero. The increase in observed-entry share remains descriptive.
- Three historical suspension events are preserved, and three linked rescission events are appended in cumulative v2.
- Rescission permits use of corrected matrix-v4 statements only. The old age-source v3 claims and figure remain superseded.
- A new origin-composition figure and caption are generated from the authenticated interval table; the diagnostic final interval and small nonzero unresolved component are retained.
- RQ1 remains an endpoint-composition analysis, with no survival or annual-path interpretation introduced.

## Reproduction and limits

The compact package includes all records required to reproduce its cross-file hashes, matrix/status reconciliation and figure-source references. `analysis/17x_validate_decision024_closure_v1.py` checks that compact package. An optional `--closure-dir` points to the external eight `full_v3.csv` files for repeat full-cell population and closure checks. No additional run is required to accept the products already checked here.

The full GEE raw batch exports, original Parquets and native rasters are not reprocessed here. Their earlier accepted execution records and hashes are retained. The local scalar tests do not load the remote constants module. Source asset classification accuracy, official raw code semantics, and the physical land-use history before 1985 are outside this technical completion claim.

Historical documents and JSONs are not retrospectively changed. They may list gates that were pending at their dates. Current status is supplied by the final review record, implementation-closure document, matrix v4 and cumulative status events v2.

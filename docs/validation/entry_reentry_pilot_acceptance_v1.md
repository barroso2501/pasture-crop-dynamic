# Entry/re-entry pilot r2: native acceptance

**2026-10-21 — PASS on the complete supplied pilot inventory.** The unchanged distributed `20b_validate_entry_reentry_pilot_v1.py --scope pilot` accepted the four operator-supplied CSVs.

| Criterion | Result |
|---|---|
| Native file inventory | Exactly four CSVs: cells, historical audit, fixtures and manifest |
| Canonical pilot support | GH-123 / 18081 / batch 1; IK-77 / 32173 / batch 5 |
| Intervals | 2015–2020; diagnostic 2020–2025 |
| Cell/interval rows | 4, complete and unique |
| Historical audit | 2 rows, each covering all 41 years, 1985–2025 |
| Native synthetic cases | 31 histories / 302 steps, each with positive weighted support |
| Native expected-value and invariant counters | 496 values, all zero |
| Real historical invariant counters | 20 values, all zero |
| Accepted-origin pixel mismatch | 4 values, all zero |
| Metadata | Config, run identity, 41 ordered bands and 41 CRS/transforms pass |
| Original category partition | Initial + post-1985 entry + unresolved closes for stock and flow |
| Auxiliary partition | First observed + observed re-entry + prior-history uncertain equals original entry component |
| Largest auxiliary cell-area residual | 1.81898940355e-12 ha |
| Historical area comparison | 32 controls; max absolute difference 1.81898940355e-12 ha |
| Tolerances | 0.01 ha per cell; 0.001 ha for pilot aggregates |

## Additional cross-stage event check

The new audit’s entry and termination areas in 2024 and 2025 were compared to the already accepted two-cell uncertain-pair pilot. The reference CSV was authenticated against its unchanged accepted validation JSON. Eight cell/year/event controls pass; the largest absolute difference is 5.6844 × 10⁻¹⁴ ha. The exact CSV and its accepted validation are included as supplementary references. This is a comparison of operator-provided tables, not a new boundary-raster asset comparison.

## Interpretation and accepted scope

The supplied native data now exercise the new server-side iteration and numerical age-201 checks. Positive observed re-entry support exists in both actual cells and intervals, so that component was exercised in the field as well as in fixtures. Prior-history uncertainty and unresolved origin are zero in these particular cell/interval flows; synthetic histories exercise the corresponding gap rules. Their absence in two cells is not evidence of absence in the entire domain.

These results accept the pilot implementation on its two-cell support and fixtures. They permit preparation of the full-domain exporter and complete reference inventory. They do not supply domain-wide entry/re-entry shares or full-domain numerical-age assurance. Both full-domain flags remain false in the unchanged validator JSON.

The operator returned usable r2 exports after the browser fix. No browser timing or responsiveness measurements were supplied. There was no independent observation of remote execution: supplied source hashes remain pinned, while executed-text hash and operator attestation remain null.

All provided native bytes, the distributed exporter, validator, cases, configuration and historical references are preserved. Matrix v4.3, events-v5, earlier accepted pilots and the accounting remain unchanged.

Machine report: `outputs/validation/entry_reentry_v1/pilot_r2/canonical_entry_reentry_pilot_v1_validation.json`. Additional receipt/scope record: `received_pilot_review_v1.json` in the same directory. The local execution stdout/stderr are preserved under `pilot_r2_execution/`.

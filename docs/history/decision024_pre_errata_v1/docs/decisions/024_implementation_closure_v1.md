# Decision 024 — implementation closure v1

**Specification recorded:** 2026-09-26. **Implementation reviewed and completed:** 2026-10-08.  
**Status:** Accepted specification; implementation and final evidence review completed within the documented scope.  
**Original decision:** [Decision 024](024_reconstruction_of_observed_pasture_spell_age.md), preserved unchanged.  
**Acceptance record:** `outputs/validation/decision024_closure_v1/canonical_decision024_closure_validation_v1.json`.

## Closure

The 12 criteria in Decision 024 are satisfied through the accepted observed-spell processing, eight-interval accounting, corrected v2 panel comparison, boundary-event and source-impact audits, and this final versioned evidence review. The separate fixed-1985-cohort RQ1 revalidation also passed. The criteria numbering here is the 12-item list in Decision 024; it must not be confused with the 14-item list in plan 008 v3.

This is an append-only implementation record. Earlier validation JSONs correctly retain `decision_024_fully_implemented: false` because the final review had not occurred at their dates. They are not edited to claim a later status. The original Decision 024 document retains its original acceptance date and pending-implementation wording as history; this record establishes the current implementation status.

## Evidence revision

The 35-statement integrated matrix v4 replaces only P9A035–P9A037 with current observed-spell-origin evidence. Two corrected statements are supported descriptive results and one is qualified. The other 32 statements preserve their previous field values except for the edition identifier. P9A031–P9A034 retain their endpoint-composition interpretation, supported by the independent RQ1 revalidation gate.

Cumulative events v2 preserve all three accepted suspension events and append three rescission events linked to this review and matrix v4. Rescission applies only to the rewritten v4 findings. Source-age v3 origin statements, their percentages, and their historical origin figures remain superseded for current use. Historical files remain immutable.

## Retained limits

The reconstruction identifies the current observed pasture spell at t0, not first-ever pasture establishment. RQ2 concerns PAS→temporary crops; PAS→NAT remains supplementary. Pooled conversion areas can count a pixel in more than one interval. The 2020–2025 interval remains diagnostic, and 2024–2025 boundaries retain limited temporal-filter support. The RQ1 comparison establishes per-cell baseline area equivalence under the original subset mask without independent native-pixel resampling. Non-origin invariance is based on accepted per-cell PAS comparisons and exact preservation of fields along the corrected panel chain, not an independent re-export of all other raster flows. No causal attribution or new trend-significance test is introduced.

The source team's official semantics for raw code `1` remain unconfirmed and may be investigated separately. That confirmation is not required to govern origin attribution, which uses annual coverage. Completion of this remediation is not a validation of MapBiomas source-class accuracy, nor does it complete manuscript preparation.

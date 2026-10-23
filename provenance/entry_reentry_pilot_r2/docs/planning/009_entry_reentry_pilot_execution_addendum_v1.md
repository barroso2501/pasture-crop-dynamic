# Plan 009 — entry/re-entry pilot execution addendum

Date: 2026-10-21. The original Plan 009 and its 2026-10-12 execution addendum are preserved unchanged in this package. Their dated pending statuses are historical. Current status:

| Component | Current status |
|---|---|
| Three-baseline window sensitivity | Accepted native pilot and full validation, unchanged |
| Uncertain-pair cross-tab | Full validation PASS on 2026-10-21; prior package preserved |
| Targeted pasture-age v2 audit | Accepted on 2026-10-20, unchanged |
| First observed entry vs observed re-entry | Pilot software prepared and locally checked; native exports pending |
| Auxiliary numerical-age 201 | Included in new native pilot fixtures and field counters; native pilot and full-domain assurance pending |
| Independent boundary-event raster comparison | Not part of this new pilot |
| Public DOI release and historical execution attestation | Prior pending scope unchanged |

The new pilot directly implements Section 2 without altering its meaning. It evaluates t0 origin and entry kind in 2015–2020 and diagnostic 2020–2025, in the same two known pilot cells. It supplies four hash-authenticated historical native reference files so preservation can be checked without requesting new historical exports.

The operator next runs only `gee/20a_export_entry_reentry_pilot_v1.js` and returns all four CSVs. Acceptance requires the entire inventory, native synthetic cases with positive support, zero error counters, exact cell/interval assignments, preserved categorical control and historical area reconciliation. Until then, there are no accepted entry/re-entry numerical findings. An accepted pilot will gate preparation of full-domain code and complete references. Full execution is not simulated by changing a mode parameter.

The new analysis has claim-dependent scope. It does not require rebuilding the accepted accounting panels, migrate the analytical origin to pasture-age v2, revise RQ1 cohort membership, or alter matrix v4.3/events-v5. First observed entry remains window-specific; a count remains an observed confirmed-entry lower bound.

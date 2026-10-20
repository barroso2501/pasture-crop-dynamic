# Rejected blank native return and explicit export revision

Review date 2026-10-20. Run `20261020134910`, version `pasture-v2-coverage-recheck-v1`, is **not accepted**. All 82 selected cells and their identity metadata are present, but all 25 computed fields are empty in every row: 2,050 missing numeric results. The original v1 validator correctly rejected this file rather than substituting zeros. No recheck-derived combined panel was written or accepted.

The source CSV and a structured rejection report are preserved under `outputs/native/pasture_v2_coverage_recheck82_v1/rejected_20261020134910/` and `outputs/validation/pasture_v2_coverage_recheck82_v1/rejected_20261020134910/`. The complete 21,869-cell parent run remains accepted for file integrity with its 82-cell coverage qualification. The returned blank fields cannot resolve that qualification or demonstrate an additional age-raster defect.

The export did not preserve the actual reducer property dictionary or names, so the CSV alone cannot distinguish absent reduction values from a mismatch in exported result names. The exact remote cause remains unconfirmed. This is a failure of the prepared export contract, not evidence supporting a zero-valued scientific result. The former software tests exercised the temporal logic and file validation on populated fixtures; they did not execute this GEE export contract.

## Revision v2

The revised script retains the temporal engine, corrected coverage rule, selected whole-cell geometries and native projection. It explicitly combines one independent single-input maximum reducer per band and gives every output its intended name. This is a naming/control revision; it does not change an independent maximum into an argmax of multiple inputs.

Before task creation, a tiny native spatial fixture with alternating input patterns must return the expected independent maxima under all 26 names. Native image-band order is checked separately. The actual export adds constant geometric support, a missing-value count/list, and the unmodified native property dictionary/names. Missing values are marked −9999 as an explicit failure sentinel. They are never treated as zero. The new validator requires these controls and equality of native properties with CSV values before accepting any scientific indicator.

This local package verifies syntax, retained/additional scalar cases, a structural software model of reducer input/output composition and v2 file-validator tests, including rejection of the observed all-blank pattern. Those are software checks only. **The revised native fixture and 82-cell run are pending operator execution.** No hash attestation of remote executed text is invented. Raw parent data, old validations, matrix v4.3 and cumulative events-v5 remain unchanged.

Follow `RUN_RECHECK82_V2_PT.md`. Only the single 82-cell task is needed; do not rerun the eight parent batches. Historical v1 files are retained for provenance and are superseded for the next execution.

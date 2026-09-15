# Phase 4A implementation verification

- **Date:** 2026-09-15.
- **Script:** `analysis/09a_build_cell_state_trajectories.py`.
- **Version:** `phase4a-cell-trajectories-v1`.
- **Script SHA-256:** `c34bd6e8935323b84cb37aac99b0a052f9ae5752df8d5802117450428ac1b09e`.
- **Status:** Local implementation verification PASS; canonical execution pending.

## Evidence and scope

The script compiled successfully and its `--self-test` completed successfully.
Verification covered the Decision 010 examples and 2,048 exhaustive five-interval
sequences across the two four-state core axes. Checks included exact episode
expansion, duration partition, independent stage-reentry identity, boundaries,
isolated activity/inactivity, off-axis interruptions, ordinal rank changes,
dominance reversals and diagnostic-dependent classification.

Full-precision magnitude ties and C–R ties at ±1/3 were verified. Unknown support
was checked to prevent fabricated process-entry events. The ten descriptive
metrics were checked to prevent an unconfigured substantive typology.

A three-cell synthetic eight-interval fixture exercised all 12 metrics in both
windows, all product writers, transition marginals, primary/full comparison,
four GIS tables and the schema writer. All written Parquets were read back;
row counts and string identifiers with leading zeros were retained. Expected
synthetic terminal episode continuations were reproduced.

These fixtures test implementation behavior; their numeric values are synthetic
and are not a validation of canonical accounting. The complete panels on the
user's Drive were not executed locally. No production hashes, trajectory
frequencies or scientific conclusions are inferred from this verification.
The Colab execution must authenticate inputs, reproduce the 504 accepted class
counts and produce its own actual validation record before result acceptance.

## Local environment

- **Python:** 3.12.14.
- **numpy:** 2.3.5
- **pandas:** 2.2.3
- **pyarrow:** 25.0.1

## Reproduce implementation verification

```bash
python analysis/09a_build_cell_state_trajectories.py --self-test
```

The terminal report must show status `PASS`,
`exhaustive_sequences_checked = 2048`,
`integration_output_roundtrip = true`, and
`canonical_input_execution = false`.

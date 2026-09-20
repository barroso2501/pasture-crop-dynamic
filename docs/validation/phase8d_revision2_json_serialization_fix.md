# Phase 8D revision 2 — Final JSON serialization correction

- **Status:** serialization correction; analytical design unchanged
- **Date:** 2026-09-20
- **Corrected script:** `analysis/14b_compute_maup_global_moran_v2.py`
- **Script version:** `phase8d-maup-global-moran-script-revision-2`
- **Script SHA-256:** `3a28624bf1e53218537d923a244eac10b5e14b154b3b903e5454c355a234e009`

## Observed failure

Revision 1 completed all 120 alternative-grid permutation tests, reproduced
the accepted canonical Phase 5 results and created the compact tables and
figures. It then stopped while writing the final validation JSON:

```text
ValueError: Out of range float values are not JSON compliant: nan
```

## Cause

Alternative graph records contain
`maximum_neighbor_distance_relative_error`, which measures agreement between
axial and geometric neighbor definitions. The canonical graph is read from its
accepted edge table and does not require that diagnostic. When canonical and
alternative graph records were combined, pandas inserted `NaN` for the
canonical row. The validation writer correctly rejects non-standard JSON
`NaN` values.

The error did not arise in Moran estimation, permutations, BY correction,
comparisons or figures.

## Correction

Revision 2 writes `0.0` for the canonical graph's not-applicable geometric
reconstruction error. Zero is appropriate because the canonical graph is used
directly and no axial-versus-geometric discrepancy exists to measure.

The revision also separates:

- the script revision identifier; and
- the analytical/checkpoint identity.

Seeds and checkpoint fingerprints retain
`phase8d-maup-global-moran-v1`. Therefore all completed revision-1 checkpoints
are accepted and any missing test would use exactly the same seed and design.

## Consequence

No permutation test should be recomputed. On rerun, the Console should report
`RESUMED` for the 120 completed tests and proceed to write the validation JSON
and inventory.

No upstream file, threshold, graph, metric, p-value rule, multiple-testing
family or robustness criterion changed.

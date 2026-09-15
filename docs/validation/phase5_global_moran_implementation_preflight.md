# Phase 5 global Moran implementation preflight

Date: 2026-09-15. Status: statistical engine tests PASS; real-data execution pending.
Script version: phase5-global-moran-v1. Script SHA-256: `f6fb91818f246f89bd2702247b2bd30aeb3dc5f70ad321b519ed0c63553146da`.

The supplied plan identifies Phase 5 as global Moran, Phase 6 as selective local
association. The implementation preserves the complete graph and induced conditional
support; prepares 104 metric-interval rows and 9,999 permutations; records separate
complete/conditional, primary/diagnostic BY correction families.

Six engine checks passed locally: sparse/dense formula agreement, affine invariance,
exact mean −1/(N−1) over all 24 permutations of a four-cell example with an island,
undefined constant-variable handling, reproducible simulated values at fixed seed,
and a reference BY correction vector. This is meaningful algorithm verification,
not a full-data statistical result or acceptance of Phase 5.

The real-data graph Parquet and metric Parquet are available in the user's accepted
Drive workflow but were not supplied locally for this execution. Full-data hashes,
keys, support flags, complete-graph diagnostics and conditional subgraph populations
are enforced when the Colab script runs. Do not infer graph or population correctness
from engine tests alone. No Moran value, significance or Phase 5 acceptance is
reported yet. Full production and figure layout will be reviewed after execution.

The operational instructions specify the files required for result review. The
actual validation JSON must remain distinct from this preflight and the original
Fase 1/2 acceptance records. No upstream GEE processing is necessary.

# Phase 8E implementation preflight

## Status

**Implementation prepared; production results not yet accepted.**

The script passed Python syntax compilation. Its internal preflight includes
reference tests for BH, BY, run length, weighted Spearman correlation and the
PySAL quadrant convention. The Colab runtime must install the pinned PySAL
dependencies before execution.

Implementation identity:

```text
analysis/14c_compare_maup_hh_clusters_v1.py
script version: phase8e-maup-hh-cluster-robustness-v1
SHA-256: 2666bd3c8e2e770325dc9a8f27e24c7d4ea98a1f5787c9f0fddc065f1e3406f5
```

## Expected production populations

| Object | Expected value |
|---|---:|
| Alternative grids | 3 |
| Metrics | 5 |
| Intervals | 8 |
| Alternative Local Moran maps | 120 |
| `hex10k_base` cell-map rows | 1,988,640 |
| `hex20k_shift` cell-map rows | 1,000,600 |
| `hex40k_base` cell-map rows | 497,800 |
| Total alternative cell-map rows | 3,487,040 |
| Interval comparisons, BH + BY | 240 |
| Temporal comparisons, BH + BY | 60 |
| Primary assessments | 30 |

## Required execution order

1. Run the pilot.
2. Return the complete Console output and
   `pilot_maup_hh_cluster_validation_v1.json` for review.
3. Run full production only after pilot acceptance.
4. Return the full validation JSON, inventory, three compact comparison CSVs
   and three figures.

The pilot uses the final 9,999-permutation configuration, so its checkpoint is
not disposable and will be reused in production.


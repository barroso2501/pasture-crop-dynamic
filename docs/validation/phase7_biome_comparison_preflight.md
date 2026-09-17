# Phase 7 implementation preflight

## Status

Implementation preflight: **PASS**.

The script compiles under Python and its independent statistical-engine tests
pass for:

- Moran permutation expectation with an island;
- affine invariance of Global Moran's I;
- deterministic permutation seeds;
- Benjamini–Yekutieli reference values;
- consecutive-episode and target-class run lengths.

## Authenticated production inputs

The production run requires the accepted canonical files at their existing
project paths:

| Phase | File |
|---|---|
| 1 | `spatial/phase1/canonical_spatial_support_v1.parquet` |
| 1 | `spatial/phase1/canonical_contiguity_weights_v1.parquet` |
| 2 | `spatial/phase2/canonical_spatial_metrics_panel_v1.parquet` |
| 3 | `spatial/phase3/canonical_spatial_map_classes_v1.parquet` |
| 5 | `spatial/phase5/global_moran_v1/canonical_global_moran_results_v1.csv` |
| 6 | `spatial/phase6/local_moran_v1/canonical_local_moran_cell_results_v1.parquet` |

The script stops before analysis if a file is absent, its hash differs, keys
are duplicated, or the canonical populations do not agree.

## Expected production structure

- 24,889 cells;
- 199,112 metric rows;
- 199,112 classified rows;
- 995,560 Local Moran cell-map rows;
- 12 metrics in descriptive summaries;
- 2 core temporal axes;
- 2 biome populations;
- 2 boundary treatments;
- 160 biome-specific Global Moran tests;
- 9,999 permutations per spatial test.

## Runtime behavior

Global Moran results are checkpointed separately for every boundary rule,
biome, metric, and interval. A rerun with the identical version, seed, and
permutation count reuses completed checkpoints. A configuration change causes
the affected checkpoint to be recomputed.

This preflight validates implementation logic and expected schemas. Final
scientific acceptance requires the production validation JSON, inventory,
result tables, figures, and independent review of the resulting comparisons.


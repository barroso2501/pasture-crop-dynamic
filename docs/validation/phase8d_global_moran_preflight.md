# Phase 8D preflight — MAUP Global Moran implementation

- **Status:** PASS for implementation; no real Phase 8D outcomes inspected
- **Date:** 2026-09-20
- **Script:** `analysis/14b_compute_maup_global_moran_v1.py`
- **Script version:** `phase8d-maup-global-moran-v1`
- **Script SHA-256:** `3d996409ab82498e886051631200c49c5bc463a438759e6f7d7984e83fd28d27`

## Static and statistical checks

The script compiled successfully and its self-test passed:

- sparse and dense Moran calculations agree;
- Moran is invariant to positive affine rescaling;
- the exhaustive permutation mean with an island equals `-1/(N-1)`;
- constant variables are explicitly undefined;
- deterministic seeds reproduce identical simulations;
- the BY reference calculation passes;
- the axial-neighbor reference recovers the expected hexagon links.

## Real Phase 8A geometry preflight

The accepted Phase 8A GeoJSON geometries were used only to test graph
construction. No process values or Phase 8D Moran outcomes were read.

| Grid | Cells at support >=50% | Undirected edges | Components | Islands | Largest component | Mean degree |
|---|---:|---:|---:|---:|---:|---:|
| `hex10k_base` | 49,716 | 138,782 | 264 | 82 | 48,098 | 5.58299 |
| `hex20k_shift` | 25,015 | 69,656 | 101 | 38 | 24,413 | 5.56914 |
| `hex40k_base` | 12,445 | 33,748 | 113 | 68 | 12,047 | 5.42354 |

Maximum relative disagreement between an axial edge and its expected geometric
centroid distance was below `7.1e-14` for every grid. All graphs were symmetric,
had zero diagonal and maximum degree six.

## Expected production populations

The production run must create:

| Product | Expected rows |
|---|---:|
| canonical plus alternative Moran results | 160 |
| interval comparisons with canonical | 120 |
| temporal comparisons | 30 |
| grid-window assessments | 6 |
| alternative permutation distributions | 120 |
| simulated Moran statistics | 1,199,880 |

The alternative BY families must contain 84 complete-primary, 21
conditional-primary, 12 complete-diagnostic and 3 conditional-diagnostic
tests.

## Runtime gates

Production will stop if:

- any accepted input hash differs;
- grid, interval or support populations differ;
- axial and geometric neighborhood definitions disagree;
- the canonical engine fails to reproduce the accepted Phase 5 raw Moran
  values to `1e-12`;
- conditional C-R support is recoded;
- checkpoints belong to another design;
- any expected result population is incomplete.

This record validates implementation readiness only. Acceptance of Phase 8D
requires the real execution JSON, compact result tables and figures.

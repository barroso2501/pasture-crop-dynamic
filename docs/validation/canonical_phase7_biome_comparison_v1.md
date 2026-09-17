# Canonical Phase 7 biome comparison — production validation

## Acceptance

Phase 7 production status: **PASS and accepted**.

The accepted execution completed on 2026-09-17 using script version
`phase7-biome-comparison-v1`. The execution produced the complete expected
population, temporal, metric and spatial-test structure. Independent review
confirmed the output hashes, row counts, unique keys and population closure.

This acceptance does not change any frozen Phase 3 class, combined-domain
Phase 5 result, or Phase 6 Local Moran/LISA inference.

## Execution identity

| Item | Accepted value |
|---|---|
| Execution UTC | `2026-09-17T08:51:13.128078+00:00` |
| Script version | `phase7-biome-comparison-v1` |
| Script SHA-256 | `46ae207d2c32cc4785b7e679328481ba9ef782d48ed805a2b4c866b9b4330cf1` |
| Permutations per Global Moran test | 9,999 |
| Master seed | 20260917 |
| Validation status | PASS |

## Authenticated inputs

| Input | SHA-256 |
|---|---|
| Phase 2 spatial metrics | `8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c` |
| Phase 3 map classes | `f0860bd2aff2c5bf6f6020bcd5022c86180311229191f58a1ed9600809d12bc3` |
| Phase 1 spatial support | `22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc` |
| Phase 1 contiguity graph | `85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f` |
| Phase 5 Global Moran results | `30ababa6003dc03909819563d7b8389ca11c794f9fb9ed58681f4919864966e5` |
| Phase 6 Local Moran cell results | `ec5906cb86e4044082db91d4cf11440b0d5401f6f8b6484217c7e246449ca2b4` |

## Population closure

| Boundary scope | Amazon | Cerrado | Total |
|---|---:|---:|---:|
| Primary assignment | 14,213 | 10,676 | 24,889 |
| Single-biome sensitivity | 13,920 | 10,387 | 24,307 |
| Difference | 293 | 289 | 582 |

The 582-cell difference is exactly the set with positive overlap in both
target biomes. These cells are included in the primary analysis and assigned
to the biome with the larger equal-area overlap. They are removed only from
the sensitivity population and are not treated as a third biome.

## Statistical coverage

The Global Moran result contains exactly 160 unique tests:

```text
2 boundary treatments × 2 biomes × 5 metrics × 8 intervals = 160
```

All 160 records have status `tested`. The permutation p-value is 0.0001 for
every test, the minimum attainable nonzero value with 9,999 permutations. All
tests remain significant after the prespecified Benjamini–Yekutieli correction;
the adjusted q-values range from 0.0002283 to 0.0004147.

The independent engine checks passed for permutation expectation, affine
invariance, seed reproducibility, Benjamini–Yekutieli reference values, and run
lengths. The 2020–2025 diagnostic interval is present and identified in every
applicable output.

## Output checks

Independent review confirmed:

- all output sizes and SHA-256 hashes match the production validation JSON;
- all 160 Global Moran keys are unique;
- all 12 metrics are represented in process and frozen-state summaries;
- transition totals close to their source populations;
- the primary and full-observed trajectory windows are both present;
- Global Moran was recomputed on induced biome graphs;
- Phase 6 LISA classes were attributed by biome without recomputation;
- no class limit was refitted;
- all three production figures are present and readable.

## Boundary-treatment sensitivity

Removing the 582 transbiome cells did not materially alter the results. Across
the 80 matched biome–metric–interval combinations, the largest absolute change
in Global Moran's I was 0.044848. All tests retained the same significance
decision. The primary-assignment conclusions are therefore not dependent on
the boundary-overlap cells.

## Version-1 field clarification

The field `excluded_biome_cells` in
`canonical_phase7_biome_global_moran_v1.csv` is named imprecisely. The code
calculates it after the boundary scope has been selected:

```text
scope population − metric-supported population
```

It therefore means `unsupported_metric_cells_within_scope`; it is not the
number of transbiome cells excluded by the boundary rule. For the additive
metrics it is zero because every scoped cell is supported. For
`cr_balance_index`, it counts cells where the index is undefined.

The actual sensitivity exclusions are 293 Amazon-assigned cells and 289
Cerrado-assigned cells. This naming issue affects neither populations nor any
statistical calculation. It is retained as a documented version-1 metadata
qualification rather than a reason to rerun the 160 permutation tests.

## Acceptance statement

Phase 7 is accepted as the canonical Cerrado–Amazon comparison. Its principal
results use the complete 24,889-cell primary assignment. The 24,307-cell
single-biome population is a sensitivity analysis. The next planned stage is
Phase 8, which evaluates scale and zoning sensitivity under the prespecified
MAUP design.

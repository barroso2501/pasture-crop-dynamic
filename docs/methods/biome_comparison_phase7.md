# Phase 7 — Cerrado–Amazon biome comparison

## Purpose

Phase 7 compares the Cerrado and Amazon without changing the canonical domain,
the frozen Phase 3 classes, the accepted Phase 5 Global Moran results, or the
accepted Phase 6 Local Moran/LISA inference. The analysis asks whether the two
biomes differ in process magnitude, relative intensity, state composition,
temporal transitions, global spatial autocorrelation, and contribution to
combined-domain local clusters.

## Analytical populations

Two boundary treatments are reported in parallel.

1. **Primary assignment** is the main analysis. Every canonical cell is assigned
   to the deterministic `primary_biome` recorded in Phase 1. The two biome
   populations partition all 24,889 cells.
2. **Single-biome sensitivity** removes cells with positive overlap in both
   Amazon and Cerrado polygons. Removed cells are not reassigned. This analysis
   tests whether conclusions depend materially on boundary cells.

Biome fractions remain in the canonical support, but process areas are not
multiplied by those fractions. Fractional allocation would implicitly assume
that each process is uniformly distributed inside a hexagon, which cannot be
established from a cell aggregate.

## Temporal treatment

The seven intervals from 1985–1990 through 2015–2020 form the primary series.
The 2020–2025 interval is included in every applicable table, trajectory,
transition, spatial statistic, and figure and remains marked as diagnostic.

## Process and state comparisons

All 12 frozen Phase 3 metrics are summarized by biome and boundary treatment.
The outputs report population, support, nonzero cells, sum, mean, median, and
90th percentile. Contributions to the combined-domain sum are reported only
for additive area or balance metrics.

Class composition uses the accepted frozen classes and does not estimate new
biome-specific limits. Therefore, differences in class frequency are directly
comparable between biomes and intervals.

Transitions and compact trajectory summaries are produced for the two Phase 4
core axes:

- `nat_tmp_endpoint_ha`: magnitude of the `NAT → TMP` endpoint flow;
- `cr_balance_index`: direction of the consolidation–replenishment balance.

The summaries cover the primary seven-interval window and the full observed
eight-interval window. They quantify state changes, distinct states, constant
sequences, maximum consecutive episode length, and transition probabilities.
They do not replace or redefine the Decision 010 trajectory typology.

## Biome-specific Global Moran's I

Global Moran's I is recomputed separately for Amazon and Cerrado using induced
subgraphs of the accepted shared-edge graph. Edges crossing the analytical
biome population are removed. Remaining binary edges are row-standardized
within each induced support; islands remain in the population with zero
spatial lag and receive no artificial neighbors.

Five focal metrics are analyzed:

- `consolidation_ha`;
- `replenishment_ha`;
- `nat_tmp_endpoint_ha`;
- `net_cr_balance_ha`;
- `cr_balance_index`, restricted to cells where the index is defined.

Each test uses 9,999 unrestricted permutations within its observed
biome-specific support and a deterministic seed. Two-sided Monte Carlo
p-values use absolute deviation from the permutation expectation. The
Benjamini–Yekutieli correction is applied separately within each combination
of boundary treatment, biome, and primary/diagnostic temporal family.

The accepted combined-domain Phase 5 value is attached as a reference. It is
not treated as a third biome or recalculated by this script.

## Local Moran/LISA attribution

Phase 7 does not recompute LISA within biome-specific graphs. It summarizes the
accepted combined-domain Phase 6 class of each cell according to the cell's
primary biome and repeats the summary after excluding transbiome cells.

Consequently, the output answers: “How much does each biome contribute to the
combined-domain HH, LL, HL, and LH pattern?” It does not answer: “Which cells
would be significant if the LISA null distribution were recalculated within
each biome?”

For absolute activity metrics, HH is the main substantive cluster and LL is a
complementary low-activity pattern. For signed balance metrics, HH and LL are
interpreted jointly as opposing spatial regimes. Persistence is defined as a
run of at least two consecutive primary intervals in the same HH or LL class.

## Acceptance conditions

The phase passes only if:

- all six upstream files match their accepted SHA-256 hashes;
- the 24,889-cell and eight-interval populations remain balanced;
- both biome rules are represented without reassignment;
- all 12 frozen metrics are summarized without refitting;
- core transition counts close exactly to their source populations;
- all 160 biome-specific Global Moran tests are present;
- accepted Local Moran classes are summarized without recomputation;
- the diagnostic interval is included and identified;
- every public output is inventoried and hashed.

## Interpretation boundary

Primary-biome comparisons describe cell-associated patterns, not exact
within-biome pixel totals for boundary cells. Biome-specific Moran statistics
describe autocorrelation under induced canonical graphs and may differ because
of both value distributions and graph topology. Local clusters retain the
combined-domain neighborhood and inferential context of Phase 6.

## Production result

The production run completed on 2026-09-17 with validation status `PASS`.
It produced 160 tested Global Moran combinations from two boundary treatments,
two biomes, five focal metrics and eight intervals. Every test was significant
after the prespecified Benjamini–Yekutieli correction. The exclusion of the 582
transbiome cells produced only small changes in the Global Moran estimates;
the largest absolute difference between boundary treatments was 0.044848.

The primary population and the sensitivity population must remain clearly
distinguished in interpretation. Transbiome cells participate in every primary
summary and spatial test through their Phase 1 `primary_biome` assignment. They
are removed only from records whose `boundary_scope` is
`single_biome_sensitivity`.

## Output-field clarification

In `canonical_phase7_biome_global_moran_v1.csv`, the version-1 field
`excluded_biome_cells` is calculated after the boundary scope has already been
selected. It therefore reports cells within that scope that lack support for
the metric. It does not report the number of transbiome cells removed by the
sensitivity rule.

For version-1 interpretation, read this field as
`unsupported_metric_cells_within_scope`. The boundary exclusions are fixed at
293 Amazon-assigned cells and 289 Cerrado-assigned cells. This naming issue
does not affect the values, graphs, permutation tests, multiplicity correction
or acceptance of the analysis.

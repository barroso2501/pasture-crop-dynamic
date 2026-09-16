# Decision 012 — Interpretation priority for Phase 6 local Moran outputs

- **Status:** Approved
- **Date:** 2026-09-16
- **Scope:** Interpretation and reporting of Phase 6 LISA results
- **Effect on computation:** None; no rerun is required

## Context

Phase 6 produced local Moran classifications for three absolute process-area
metrics and two C–R balance metrics. The same quadrant labels do not answer the
same substantive question for every metric. A reporting hierarchy is therefore
required before selecting maps, persistence results and manuscript findings.

## Decision

For `consolidation_ha`, `replenishment_ha` and `nat_tmp_endpoint_ha`,
significant high-high clusters are the primary local-association outcome. They
identify cells with relatively high process area surrounded by cells with a
high spatial lag and therefore correspond to the spatial concentrations sought
by the investigation.

For these absolute metrics, low-low clusters are complementary results. They
identify spatially structured low activity or absence of the process. Because
the variables contain many zero or near-zero observations, a large LL cluster
must not be described as a second area of high process activity. HL and LH are
retained as spatial-outlier diagnostics and may be used to identify cluster
edges, isolated activity or possible relocation fronts.

For `net_cr_balance_ha` and `cr_balance_index`, HH and LL are co-primary. The
two classes describe opposite spatial poles of the C–R balance rather than a
hotspot and an unimportant background. HH is the relatively high-balance pole;
LL is the relatively low-balance pole.

## Substantive sign and threshold checks

LISA classes are defined relative to the eligible map mean. They are not fixed
substantive classes. Interpretation must therefore combine quadrant and value:

- an HH `net_cr_balance_ha` cell supports a consolidation-favoring statement
  only when its observed balance is positive;
- an LL `net_cr_balance_ha` cell supports a replenishment-favoring statement
  only when its observed balance is negative;
- an HH `cr_balance_index` cell is consolidation-dominant only when the index
  exceeds `+1/3`;
- an LL `cr_balance_index` cell is replenishment-dominant only when the index
  is below `-1/3`.

Cells outside these sign or threshold conditions remain valid relative LISA
results, but they must not receive the stronger process-dominance label.

## Temporal reporting hierarchy

For the three absolute metrics, the primary temporal summaries are:

1. location and cell count of HH clusters by interval;
2. process area contained in HH cells;
3. consecutive HH persistence and duration;
4. entry, exit and adjacent-interval overlap of HH sets;
5. distribution of HH cells between biomes and treatment of boundary cells;
6. retention of the HH result under the BY sensitivity correction.

LL persistence for absolute metrics is reported as structured absence or low
activity. For the two balance metrics, HH and LL persistence, overlap and
regional distribution receive equal analytical status.

## Multiple-testing language

BH at 5% remains the prespecified primary classification. BY remains a
conservative sensitivity diagnostic. Claims based on individual clusters must
state whether the relevant cells also pass BY when that distinction is
material. BY does not replace the accepted BH maps.

## Diagnostic interval

The hierarchy applies to all eight intervals. Results for 2020–2025 remain
included and visibly identified as diagnostic. They may demonstrate observed
continuation, appearance or disappearance through 2025, but they do not alone
determine conclusions about the 1985–2020 primary period.

## Consequence

The Phase 6 calculations, checkpoints and cell classifications remain
unchanged. This decision governs figure emphasis and scientific wording and
prevents extensive LL clusters of zero-valued absolute metrics from being
misread as concentrations of the corresponding process.

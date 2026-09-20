# Phase 8C findings — Robustness to spatial scale and zoning

## Main finding

The study's aggregate and temporal conclusions are robust to the tested MAUP
configurations, but some cell-level distribution and conditional-support
descriptions depend on spatial scale. Changing the origin of an approximately
20,000-ha grid did not materially affect the result. Halving or doubling the
nominal cell area exposed scale effects, with the clearest differences on the
approximately 40,000-ha grid.

## What is robust

Across all alternatives:

- domain totals remain within the prespecified 0.2% difference limit;
- aggregate C-R signs and dominance classes are unchanged;
- all aggregate rates and indices remain within their limits;
- every temporal rank correlation is `1.0`;
- peaks and troughs occur in the same intervals;
- inclusion of 2020-2025 does not change any grid's overall assessment.

The central interpretation of the historical process sequence is therefore
not an artifact of the selected canonical lattice.

## Zoning effect

`hex20k_shift` passes every primary comparison. This is the cleanest test of
zoning because nominal resolution is held near the canonical value while the
lattice origin changes. The finding supports robustness to the particular
placement of the canonical hexagon boundaries.

## Finer-scale effect

`hex10k_base` is formally sensitive because a single coverage statistic exceeds
its limit. In 1985-1990, the fraction of support with a defined consolidation
rate differs by 5.0537 percentage points, only 0.0537 point above the
prespecified limit. The associated KS distance is small.

This is best interpreted as a threshold-edge result. It should be reported
without relabeling the grid as stable, but it does not challenge the aggregate
or temporal conclusions.

## Coarser-scale effect

`hex40k_base` produces a systematic increase in the support fraction for which
the C-R index and consolidation rate are defined. Spatial aggregation makes a
larger unit more likely to contain some C-R activity or initial pasture. This
changes the landscape share represented by the conditional metric even when
the conditional values themselves remain broadly similar.

The coarse grid also slightly exceeds the KS limit for `NAT -> TMP` density and
initial-native intensity in 2015-2020 and again in diagnostic 2020-2025. These
are modest numerical exceedances, but they demonstrate a genuine scale effect
in recent cell-level `NAT -> TMP` distributions.

## Reading the weighted medians

The weighted-median figure displays pronounced differences among cell sizes,
particularly for replenishment and recent consolidation or `NAT -> TMP`.
These medians describe the distribution of spatial units, not domain totals.
When cells become larger, spatially localized nonzero pixels are combined with
surrounding area and exact-zero cells become less frequent. A higher coarse-
grid median can therefore coexist with nearly identical domain totals.

For this reason, cell-level medians are evidence about scale-dependent spatial
concentration, not evidence that one grid measures more total conversion than
another.

## Diagnostic interval

The 2020-2025 extension preserves all aggregate and temporal conclusions. On
the coarse grid it repeats, rather than initiates, the recent distributional
sensitivity. The interval is therefore retained in the full-observed analysis
and explicitly flagged, while the primary 1985-2020 conclusion remains
unchanged.

## Interpretation for subsequent reporting

Results may be stated as robust when they concern:

- domain-wide totals;
- aggregate rates and C-R balance;
- direction and ordering of temporal change;
- broad conclusions that do not rely on a particular cell-size distribution.

Results should be qualified as scale-sensitive when they concern:

- the fraction of the landscape assigned a defined conditional metric;
- the typical or median value among spatial units;
- fine distinctions in recent `NAT -> TMP` cell distributions;
- the number or proportion of units above a cell-level threshold.

The canonical approximately 20,000-ha grid remains scientifically defensible
as the primary support. Phase 8C does not justify replacing it with an
alternative grid.

## Remaining Phase 8 question

Phase 8C does not test whether Global Moran magnitudes or the broad geography
and persistence of significant clusters remain stable across grids. Those
questions require alternative-grid neighborhood graphs and separately
prespecified spatial-comparison rules. They remain the final analytical
component before Phase 8 can be closed.

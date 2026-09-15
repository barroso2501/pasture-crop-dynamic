# Temporal persistence, reversals and flow concentration

## Scope and sources

Descriptive completion of the temporal exploration of Phase 4: all four fixed
primary NAT–TMP magnitude groups, both primary-biome labels, and the two core
classified axes NAT magnitude and C–R balance. Primary7 (1985–2020) and full8
(1985–2025) remain parallel. Include diagnostic 2020–2025, without selecting new
primary-group cells. Existing 12-axis trajectory products and typology remain
unchanged; this interpretation focuses on two core axes.

Authenticate eight 08c GIS tables against their manifest/validation and upstream
metric/class provenance. Read the four accepted core trajectory GIS tables;
record component hashes and require every sequence to reproduce the frozen
cell-interval panel. Check accepted episode counts/maxima and equivalence of
constant pattern code and flag. Reuse accepted entries, exits, interruptions,
resumptions, stage reentries and direct/mediated dominance reversal counts.
Do not reinterpret these fields under an alternate rule.

## Episodes and observed duration

An episode is a maximal consecutive run of the same frozen state. Its observed
length is the number of five-year intervals; observed years = 5 × length.
Persistence is ≥2 intervals. Activity excludes zero for NAT magnitude and inactive
for C–R; persistent same-state episodes may still be zero/inactive. Keep them in
the records and distributions, but exclude them from active-persistent flags.

Mark the first episode left-boundary censored and the last right-boundary
censored, independently in each window. These are observation-boundary flags:
the onset or end beyond the series is unknown. A one-episode series has both
flags. Primary-window right censoring remains a primary description even when
its continuation/end is observed in the diagnostic extension. Full-window
episodes reaching 2025 carry contains_diagnostic_interval=1.

Duration distributions are counts of episodes, stratified by state and both
boundary flags. Do not interpret these distributions as survival curves or
uncensored durations. Episode counts need not equal independent cell counts.
Reentry into a state and reentry into activity are different concepts; preserve
the accepted stage/activity fields separately.

## Consecutive and pooled transition matrices

Count every source→target state for consecutive intervals, including self-
transitions and zero/inactive. Preserve source/target dates. Primary7 has six
transitions per cell/axis; full8 has seven. Flag the transition ending in
2020–2025 as diagnostic. Pooled matrices sum within a window, then divide by
all outgoing transitions from each source state. They describe observed
cell-interval transitions, not independent probabilities or a fitted Markov
process. Each cell can contribute more than once; primary transitions overlap
with full-window transitions and must not be added as unique events.

## Late-primary concordance of consolidation dominance

Within the fixed high group in each primary biome, compare C-dominant sets in
2010–2015 and 2015–2020. Report intersection, union, Jaccard intersection/union,
intersection as fraction of all high-group cells, and its share of consolidation
and replenishment hectares in each interval. This tests observed persistence
on the cell scale; it does not track annual pixel paths or establish a mechanism.

## Concentration and descriptive removal sensitivity

For each high-group biome/interval and flow C, R or NAT endpoint, rank all group
cells by descending hectares. Select ceil(N × fraction) for fractions 1%, 5%,
10%, where N includes zero-flow cells. Report selected count, positive-flow cell
count and selected share of summed hectares. Stable input order resolves ties
for the removal calculation; tied hectares do not affect the concentration sum.
The share does not use the number of positive-flow cells as its denominator.

For each selected set, remove those cells and recompute (sum C−sum R)/(sum C+sum R)
on the remaining population. This is a descriptive check of concentration and
aggregate sign/class sensitivity, not a confidence interval, causal exclusion
or representative population estimate. Group/biome assignments stay fixed.

## Support and deliverables

Primary-biome attribution assigns entire cell flows and does not split pixels
at biome boundaries. Follow the previous transbiome sensitivity qualification.
No clusters, significance tests, causal inference or annual-pixel trajectory
inference are claimed. Areas pooled over intervals are not unique-pixel totals.
Numeric identities allow rtol 1e-10 and atol 1e-6 ha for CSV serialization.

Deliver cell episode records, censored duration distributions, dated and pooled
transition counts, persistence/reversal summaries, late concordance, flow
concentration and GIS late-state flags. The latter supports 1:1 joins by text
cell_id; retain its schema.ini without CharacterSet beside the CSV. Episode
records are one-to-many and must not be used as an unfiltered 1:1 GIS join.

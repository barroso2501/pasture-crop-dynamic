# Decision 013 — Biome assignment and spatial inference in Phase 7

## Decision

Phase 7 will use the deterministic Phase 1 `primary_biome` assignment as its
main categorical comparison and will repeat every principal summary after
excluding cells that overlap both Amazon and Cerrado.

Process areas will not be multiplied by biome-overlap fractions. Such a
calculation would be a geometric allocation under an unverified assumption of
uniform process distribution inside each cell. The retained fractions remain
available for diagnosing boundary support.

Global Moran's I will be recomputed within induced biome-specific subgraphs of
the accepted canonical graph. The same analysis will be performed under the
primary assignment and single-biome sensitivity populations.

Accepted Phase 6 Local Moran/LISA classes will not be recomputed. They will be
summarized by biome as contributions to the combined-domain spatial pattern.
This preserves their original neighborhood, permutation, and multiplicity
context.

## Rationale

The primary label provides a complete, mutually exclusive partition of the
canonical 24,889-cell domain. Excluding transbiome cells provides a transparent
sensitivity analysis without duplicating or fractionally splitting a cell's
observed process value.

Global autocorrelation is a property of both values and the weight graph, so a
biome-specific comparison requires an induced graph. Local significance is
location-specific and depends on its full inferential family; silently
recomputing LISA would create a different analysis rather than an attribution
of accepted Phase 6 results.

## Consequences

- biome totals are totals associated with primary-biome cells, not exact
  clipped-polygon process totals;
- cells removed in the sensitivity analysis are not reassigned;
- within-biome Global Moran values can differ from the combined-domain result
  because both the values and the graph support differ;
- biome LISA summaries describe contributions to the combined-domain pattern;
- any future within-biome LISA analysis must be separately prespecified and
  must not replace the Phase 6 canonical results.

## Diagnostic interval

The 2020–2025 interval is included in all applicable Phase 7 analyses and is
explicitly marked as diagnostic. It is corrected in a separate inferential
family from the seven primary intervals.

## Production confirmation

The production run on 2026-09-17 confirmed the prespecified design without a
change in analytical populations or interpretation.

- the primary assignment contains all 24,889 cells: 14,213 assigned to Amazon
  and 10,676 assigned to Cerrado;
- 582 cells overlap both target biomes, of which 293 are assigned to Amazon
  and 289 to Cerrado by the largest-overlap rule;
- the single-biome sensitivity contains 24,307 cells after removing those 582
  cells: 13,920 Amazon and 10,387 Cerrado;
- the transbiome flag is a geometric boundary condition, not a third biome or
  an ecological-transition class;
- the sensitivity exclusion does not apply to the primary analysis and does
  not remove the cells from the canonical domain.

The small changes in Global Moran's I after boundary-cell exclusion support
the retained design. A separate descriptive study of boundary-overlap cells
may be conducted later, but it would supplement rather than replace the two
accepted Phase 7 populations.

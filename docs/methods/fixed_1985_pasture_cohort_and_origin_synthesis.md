# Fixed 1985 pasture cohort and PAS→TMP origin synthesis

## Fixed-cohort extraction

The extraction uses the frozen canonical grid, coverage collection, pasture-age
collection, projected CRS, affine transform, state groups, and pixel-area
conversion already used by the accepted stock-flow analysis. The baseline mask
is created once from 1985 planted pasture and pasture-age code 100. It is never
redefined in later years.

For each canonical cell and reference year, the cohort area is partitioned into
`nat`, `pas`, `tmp`, `oag`, `out`, `water`, `nodata`, `unexpected`, and `masked`.
The exported state areas must sum to the cell's fixed cohort area at every
reference year. Cells with zero cohort area are retained to preserve the full
canonical population and spatial identity.

The derived summaries report:

- the combined domain;
- Amazon and Cerrado under primary whole-cell biome assignment;
- a nontransbiome sensitivity that excludes boundary-crossing cells.

Because only reference-year states are observed, a pixel classified as pasture
at two endpoints may have changed state between them. The series describes
endpoint fate/composition, not uninterrupted persistence, first transition
date, or a unique transition pathway.

## PAS→TMP origin synthesis

The accepted eight-row stock-flow summary is authenticated by SHA-256 before
use. For each five-year interval, consolidation area is partitioned into
left-censored, new, unresolved-age, and unattributed-age components. Shares are
recomputed from accepted areas and checked against the accepted shares.

Two pooled views are generated:

- primary 1985–2020: seven intervals;
- full observed 1985–2025: eight intervals including the diagnostic extension.

These are sums of interval areas, not unique-pixel areas.

## Evidence integration

Evidence matrix version 1 is authenticated and preserved. Its two explicit gap
rows are removed only in version 2 and replaced by four RQ1 statements and three
RQ2 statements. Each new statement records its exact source file and SHA-256.
Interpretations remain descriptive; no causal claim is introduced.


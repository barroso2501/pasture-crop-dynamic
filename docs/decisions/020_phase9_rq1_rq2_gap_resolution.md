# Decision 020 — Phase 9 RQ1/RQ2 evidence-gap resolution

## Status

Approved for implementation. Acceptance remains conditional on pilot and full
validation.

## Decision

The two evidence gaps retained by Phase 9A will be resolved without modifying
the established analytical design:

1. RQ1 receives one new fixed-cohort extraction from Earth Engine.
2. RQ2 is synthesized from the already accepted stock-flow accounting.
3. The version 1 evidence matrix remains immutable for provenance. A version 2
   matrix replaces only `P9A001` and `P9A002` with authenticated evidence rows.
4. No interval flow, map class, trajectory, Moran statistic, LISA result, biome
   comparison, or MAUP result is recalculated.

## RQ1 cohort definition

The cohort is fixed once at baseline and consists of pixels satisfying both:

- 1985 coverage class belongs to planted pasture (`PAS`); and
- the 1985 pasture-age code equals 100, the left-censored initial pasture stock.

The same pixels are classified at 1985, 1990, …, 2025 into the nine exhaustive
canonical states. Results are endpoint compositions at reference years. They
are not a survival curve and do not prove continuous occupancy between dates.

Whole-cell primary-biome assignment is the main biome comparison. Exclusion of
the 582 transbiome cells is retained as a sensitivity view, not as the primary
population.

## RQ2 origin definition

PAS→TMP consolidation is partitioned by the pasture-age code at the interval
start into:

- left-censored 1985 pasture stock;
- pasture established during the observed series;
- unresolved pasture age;
- unattributed pasture age.

The interval components must sum to the accepted consolidation total. Pooled
areas sum interval conversions and therefore do not deduplicate pixels that may
convert in different intervals.

## Temporal treatment

The primary interpretation ends in 2020. The 2025 endpoint and the 2020–2025
origin interval are included in all complete-series products and explicitly
marked diagnostic. They do not redefine the primary-period conclusions.

## Acceptance conditions

- pilot: 3,168 unique batch-00 cells and exact baseline/partition closure;
- full: 24,889 unique canonical cells and identity with spatial support;
- 224,001 cell-year rows and 45 cohort-summary rows;
- authenticated accepted RQ2 input and exact origin-component closure;
- evidence matrix v2 with 35 unique findings, all five research questions, no
  remaining `evidence_gap`, and no causal claim.


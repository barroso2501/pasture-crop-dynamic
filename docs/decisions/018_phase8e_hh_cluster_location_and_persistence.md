# Decision 018 — Phase 8E HH-cluster location and persistence

- **Status:** Implemented and accepted; criteria frozen before alternative-grid local results were inspected
- **Date:** 2026-09-21
- **Applies to:** final spatial-configuration component of Phase 8

## Purpose

Phase 8D established that positive and significant Global Moran association is
preserved across the three alternative grids, while exact magnitudes and
temporal ordering are partly sensitive to scale and zoning. Phase 8E asks the
remaining question: do high-value clusters occupy broadly the same geographic
areas and persist through time under those grids?

The canonical approximately 20,000-ha Local Moran/LISA analysis remains
primary. Alternative-grid Local Moran results are sensitivity tests and do not
replace the canonical maps or redefine their clusters.

## Primary cluster

The primary object is the `HH` class: a high standardized value surrounded by
high standardized neighboring values and significant after multiplicity
correction. This matches the project's focus on spatial concentration of
consolidation, replenishment, endpoint `NAT -> TMP`, net C-R balance and
consolidation-dominant C-R balance.

All four LISA quadrants are calculated and preserved. `LL`, `HL` and `LH` are
reported as secondary diagnostics, not discarded. They do not determine the
primary Phase 8E robustness classification.

## Inference

- 9,999 conditional permutations per grid × metric × interval map;
- deterministic seeds and restartable checkpoints;
- BH at 5% within each map as the primary classification;
- BY at 5% within the same map as a sensitivity classification;
- islands remain in the declared population but cannot be significant;
- no artificial links are added.

The restricted metric set is identical to Phase 8D. The alternative support
retains cells with fixed-domain support fraction at least 0.50. The primary
period is 1985–2020; 2020–2025 is included and flagged as diagnostic.

## Geographic comparison

Cell identifiers cannot be compared directly across different lattices.
Phase 8E therefore constructs an exact polygon-intersection crosswalk between
the canonical cells and each supported alternative grid. All footprint areas
are calculated on the shared portion of the fixed domain.

For every metric and interval, the BH-significant HH footprints are compared
using:

- area-weighted Jaccard similarity;
- overlap coefficient;
- capture of the canonical HH footprint;
- precision of the alternative HH footprint;
- alternative/canonical footprint-area ratio.

An interval passes the broad-location criterion when both:

```text
Jaccard >= 0.40
overlap coefficient >= 0.60
```

The paired criteria prevent a small footprint nested within a much larger one
from being treated as robust solely because its overlap coefficient is high.

## Temporal persistence

For each grid, metric and inference rule, Phase 8E calculates:

- number of HH intervals per cell;
- maximum consecutive HH run;
- persistent HH status, defined as at least two consecutive intervals;
- full-observed versions including 2020–2025.

Alternative HH frequency is projected to canonical cells by overlap-area
weighting. Temporal robustness requires:

```text
weighted Spearman correlation of HH frequency >= 0.70
persistent-HH Jaccard >= 0.40
persistent-HH overlap coefficient >= 0.60
```

For a metric-grid combination, interval location is accepted when at least
five of seven primary maps pass. In the full-observed window, at least six of
eight maps must pass. Overall robustness additionally requires both temporal
criteria to pass.

The thresholds describe broad geographic agreement, not cell-for-cell
identity. Exact identity is neither expected nor appropriate under changes of
cell size and zoning.

## Interpretation

A failure indicates MAUP sensitivity in the footprint, recurrence or
persistence of HH clusters. It does not invalidate the canonical cluster and
does not imply that Global Moran is absent. Results will be reported by metric
and grid before any aggregate summary.

The BY results are a prespecified sensitivity analysis. They will be reported
but will not retroactively replace BH as the primary Phase 6/8E local
inference rule.

## Implementation outcome

The full execution passed validation with 120 alternative maps and 3,487,040
cell-map records. Twenty-one of 30 primary grid–metric–window assessments met
all prespecified criteria. Replenishment, net C–R balance and the bounded C–R
index passed all assessments; consolidation was partially robust; endpoint
`NAT -> TMP` was sensitive in all six overall assessments.

These outcomes do not amend the decision thresholds. Phase 8 is closed with
the failed criteria retained as substantive MAUP findings and the canonical
approximately 20,000-ha grid retained as primary.

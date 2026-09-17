# Integrated temporal characterization

- **Implementation:** `analysis/05_temporal_characterization.py`.
- **Output version:** `canonical_integrated_temporal_characterization_v1`.
- **Status:** canonical descriptive supporting analysis; not a gate for later spatial phases.

## Purpose

This script summarizes the accepted 199,112-row integrated stock-flow and
within-interval trajectory panel over eight five-year intervals. It provides a
domain-level temporal description before spatial stratification.

It produces:

- totals for consolidation, replenishment, gross and net C–R activity and
  `NAT → TMP` endpoint flows;
- composition of intermediate-pasture trajectories;
- sensitivity to alternative pasture-persistence rules;
- counts and proportions of C–R activity classes;
- distribution of the C–R balance among cells where both processes occur;
- five figures in PNG and SVG.

## Temporal scope

The seven intervals from 1985–1990 through 2015–2020 form the primary series.
The 2020–2025 interval is retained as a diagnostic extension. Lines connecting
the interval summaries are graphical aids, not fitted temporal trends.

## Interpretation

The analysis is descriptive. It does not fit trends, define data-driven
historical phases, estimate change points, compare biomes, identify spatial
clusters or support causal claims. Biome comparison is handled separately by
Phase 7 using the canonical spatial assignment.

## Provenance and checks

The input is authenticated by SHA-256 and must contain exactly 24,889 cells,
eight intervals, 199,112 rows and 150 columns. The script validates unique and
complete keys; nonnegative area fields; gross and net C–R identities;
trajectory partitions; activity-class closure; balance-index support; and
creation of every declared figure.

The script remains in the canonical repository because it supplies the
auditable domain-level temporal summaries used for early interpretation. It is
not required to rerun accepted Phases 4–7 unless its input or specification is
changed.


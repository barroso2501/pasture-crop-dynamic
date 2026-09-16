# Decision 011 — Local Moran/LISA inference for Phase 6

- **Status:** Approved for implementation
- **Date:** 2026-09-16
- **Scope:** Five prespecified metrics, eight five-year intervals, canonical cells

## Decision

Phase 6 will estimate local Moran statistics for `consolidation_ha`,
`replenishment_ha`, `nat_tmp_endpoint_ha`, `net_cr_balance_ha`, and
`cr_balance_index`. The first four metrics use the complete 24,889-cell domain.
`cr_balance_index` uses the induced subgraph of cells for which
`cr_balance_defined == 1` in each interval.

The analysis uses the accepted binary contiguity graph, row-standardized
within the eligible support of each map. No artificial links are added.
Islands are retained for accounting, assigned zero spatial lag, excluded from
the multiple-testing family, and classified as non-significant.

Each location is evaluated with 9,999 conditional random permutations and a
deterministic seed derived from the master seed, metric, and interval. The
PySAL quadrant convention is fixed as 1=HH, 2=LH, 3=LL, and 4=HL.

The primary multiplicity correction is Benjamini-Hochberg (BH) at 5%, applied
separately within every metric-by-interval map. Benjamini-Yekutieli (BY) is
also recorded as a conservative sensitivity diagnostic, but it does not
replace the prespecified BH classification. No correction is claimed across
the collection of 40 maps; inference and wording remain map-specific.

The included 2020–2025 interval is processed identically and marked as a
diagnostic extension. It contributes to full-series persistence descriptions,
but does not determine primary-period conclusions.

## Interpretation

HH and LL mean that a cell and its spatial lag are respectively above or below
the eligible-map mean. HL and LH are spatial outliers. These are relative
local-association labels, not fixed substantive thresholds.

For `net_cr_balance_ha`, HH does not necessarily mean a positive balance and
LL does not necessarily mean a negative balance; the metric value and
standardized score must be inspected. For `cr_balance_index`, centering and
the neighborhood graph apply only to active, defined cells. It must not be
compared as if it used the complete-domain reference distribution.

## Outputs and persistence

The script writes one authenticated checkpoint for each of the 40 maps before
continuing. A rerun reuses a checkpoint only when its configuration and hash
match exactly. Final products include the cell-level panel, class and biome
summaries, HH/LL adjacent-interval Jaccard overlap, multiquinquennial HH/LL
persistence, five comparable eight-panel map series, GIS CSVs, and validation.

## Acceptance criteria

1. All three canonical input hashes match their frozen values.
2. The panel contains 199,112 unique cell-interval rows.
3. The graph contains 134,906 directed links and 163 complete-domain islands.
4. Exactly 40 map checkpoints are produced or validly reused.
5. The final panel contains 995,560 unique cell-metric-interval rows.
6. Unsupported balance-index rows remain `not_applicable`.
7. Islands are never classified as significant.
8. BH and BY adjusted values are recomputed within each map only.
9. Exactly 124,445 cell-metric persistence records are produced.
10. GIS exports preserve one row per `cell_id` and omit the ArcGIS-incompatible
    `CharacterSet=65001` option from `schema.ini`.

## Consequence

This is a confirmatory implementation of a prespecified exploratory local
analysis. Any alternative neighborhood, significance family, metric
transformation, or post-hoc cluster definition requires a separate sensitivity
analysis and cannot silently replace these primary outputs.

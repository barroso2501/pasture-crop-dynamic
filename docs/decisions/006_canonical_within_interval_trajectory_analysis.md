# Canonical within-interval trajectory analysis

- **Status:** Implemented and validated for the complete temporal series
- **Decision date:** 2026-09-12
- **Applies to:** Annual decomposition of five-year `NAT->TMP` endpoint flows
- **Related accounting method:**
  `docs/methods/five_year_stock_flow_panel.md`
- **Related derived metrics:**
  `docs/methods/derived_stock_flow_metrics.md`

## Decision

The canonical workflow will include a separate annual within-interval
trajectory analysis for pixels classified as native vegetation at the
beginning of a five-year interval and temporary agriculture at its end.

This analysis will determine whether planted pasture was observed during the
four intermediate annual observations. It complements the validated
five-year stock-and-flow panel and does not replace, correct, or reopen its
accounting results.

## Accounting status

The five-year accounting is complete within its defined scope:

- endpoint stocks are measured independently;
- directed endpoint flows are quantified;
- focal origin and destination identities close;
- `flow_nat_tmp` contains the complete area classified as `NAT` at `t0` and
  `TMP` at `t1`; and
- all 24,889 cells are retained in every interval.

The missing component is not unallocated area. It is the annual trajectory
composition hidden inside the already measured `NAT->TMP` endpoint flow.

The distinction is:

```text
Five-year accounting question:
How much area was NAT at t0 and TMP at t1?

Within-interval trajectory question:
How much of that area had pasture detected between t0 and t1?
```

The first question has been answered and validated. The second requires the
canonical trajectory analysis defined by this decision.

## Scientific rationale

An endpoint comparison compresses four intermediate annual observations. A
pixel classified as `NAT` at `t0` and `TMP` at `t1` may have passed through
pasture during the interval. Without examining the annual sequence, the role
of pasture as an intermediate stage of agricultural expansion may be
underestimated.

Conversely, a single annual pasture classification may reflect a brief land-
cover state or temporal classification instability. The analysis must
therefore report both an inclusive detection rule and a persistence-sensitive
rule instead of assuming that every one-year pasture observation represents a
stable land-use stage.

## Canonical analytical population

The trajectory analysis will use the same fixed spatial population as the
stock-and-flow panel:

```text
projects/ee-barroso2501/assets/
grade_hex_CeAmz_canonical_c11_v3
```

Every export will contain one row for each of the 24,889 canonical cells,
including cells with zero `NAT->TMP` endpoint flow. Positive-flow filtering
will not be applied in Google Earth Engine.

The eight intervals are:

```text
1985-1990
1990-1995
1995-2000
2000-2005
2005-2010
2010-2015
2015-2020
2020-2025
```

The primary inferential period ends in 2020. The 2020-2025 interval will be
processed with the same schema but marked as diagnostic.

## Canonical input and spatial alignment

The analysis will use the final public MapBiomas Brazil Collection 11 asset:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

It will use the class definitions, CRS, affine transform, years, and asset
identifiers centralized in `config/constants.js`. Raster reductions will
specify the canonical `crs` and `crsTransform`; a generic `scale: 30` will not
be used.

The pasture-age product is not required for detecting annual intermediate
land-cover states. Its unresolved source code is therefore outside the scope
of this stage.

## Required detection rules

At minimum, the canonical analysis will distinguish two forms of evidence for
an intermediate pasture stage.

### Inclusive rule

Pasture is detected in at least one of the four intermediate years:

```text
pasture_any = any intermediate annual state is PAS
```

This rule maximizes sensitivity to short pasture phases.

### Persistence-sensitive rule

Pasture is detected in at least two consecutive intermediate years:

```text
pasture_consecutive2 =
    at least one consecutive intermediate-year pair is PAS-PAS
```

This rule reduces sensitivity to isolated one-year classifications. It is a
robustness definition, not an assertion that shorter pasture phases are
invalid.

The relationship between the two rules must be explicit:

```text
pasture_consecutive2 is a subset of pasture_any
```

Additional annual-sequence diagnostics may be retained if they help evaluate
classification persistence, but they must not obscure these two primary
rules.

## Terminology

The former label `direto_real` will not be used. Absence of an intermediate
pasture observation does not demonstrate direct conversion from native
vegetation to temporary agriculture. Pixels may pass through other mapped
states, including mosaic or other agriculture, exposed or non-vegetated land,
or temporary agriculture before the endpoint year.

The canonical labels will describe only what is observed:

```text
nat_tmp_with_intermediate_pasture
nat_tmp_without_intermediate_pasture
```

Where persistence matters, the label will identify the rule, for example:

```text
nat_tmp_with_consecutive2_pasture
```

Scientific interpretation will use phrases such as “with pasture detected”
and “without pasture detected,” not “direct conversion,” unless a later and
more restrictive trajectory classification supports that claim.

## Required accounting identities

For the inclusive rule, every cell and interval must satisfy:

```text
nat_tmp_endpoint =
    nat_tmp_with_intermediate_pasture
    + nat_tmp_without_intermediate_pasture
```

The trajectory-derived `nat_tmp_endpoint` must also agree, within numerical
tolerance, with `flow_nat_tmp` in the validated canonical stock-and-flow panel.

The persistence-sensitive component must satisfy:

```text
nat_tmp_with_consecutive2_pasture
    <= nat_tmp_with_intermediate_pasture
    <= nat_tmp_endpoint
```

Residuals for these identities will be exported or calculated explicitly and
validated before interpretation.

## Historical implementation status

The earlier script `work/scripts/23_pentefino_1985_2025.js` and the historical
`pentefino_*.csv` outputs are retained only as diagnostic provenance. They are
not canonical results because they used:

- the pre-release `classification-ft` coverage source;
- the historical 21,869-cell grid;
- a generic `scale: 30` reduction;
- positive-flow filtering before export; and
- the unsupported label `direto_real` for the complement of pasture
  detection.

Those outputs must not be joined to the canonical panel or used in manuscript
results. The canonical implementation will be written as a new version-
controlled script.

## Consequences

- The validated stock-and-flow panel and derived metrics remain accepted.
- No existing canonical stock or flow needs to be reprocessed.
- The new trajectory outputs will form a complementary cell-by-interval table.
- The canonical `flow_nat_tmp` field will provide an external closure control
  for the new processing.
- Zero-flow cells will remain in the exports and analytical table.
- Inclusive and persistence-sensitive pasture evidence will be reported
  separately.
- Moran, MAUP, and other spatial analyses of this pathway will occur only
  after the trajectory outputs pass accounting and temporal-rule validation.

## Implementation outcome

The exact bands, field names, residuals, output schema, validation thresholds,
and execution design are defined in:

```text
docs/methods/within_interval_nat_tmp_trajectories.md
```

The complete-domain 2005-2010 implementation was executed and validated. It
passed all structural, accounting, subset, observation-support, and external
reconciliation checks. Its validation record is:

```text
docs/validation/nat_tmp_trajectory_2005_2010.md
```

The remaining seven intervals were then processed without methodological
changes and combined with the pilot. The resulting panel contains 199,112
records: 24,889 canonical cells in each of eight intervals. The panel and
assembly process passed all predefined validation checks. The complete record
is:

```text
docs/validation/canonical_nat_tmp_trajectory_panel_assembly.md
```

The pilot produced a materially smaller inclusive pasture share than the
historical processing, and the complete series confirmed the same directional
difference in every interval. This does not invalidate the canonical results.
The historical output used a preliminary coverage source, the historical
domain, generic scale-based reductions, and positive-flow filtering. The
canonical series is not required to reproduce it and supersedes it for future
analysis.

## Consequence for subsequent analysis

The within-interval processing stage is complete. Subsequent work may join the
trajectory panel to the canonical stock-and-flow analytical table using
`cell_id`, `t0`, and `t1`.

The join must preserve all 199,112 cell-interval records and must not collapse
zero-flow cells. Rule selection, temporal interpretation, biome comparisons,
Moran analysis, and MAUP evaluation remain downstream scientific-analysis
steps. They must not modify the accepted endpoint or trajectory accounting.

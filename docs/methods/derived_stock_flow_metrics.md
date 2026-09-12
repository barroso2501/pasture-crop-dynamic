# Derived stock-and-flow metrics

- **Status:** Implemented and validated
- **Last updated:** 2026-09-12
- **Source panel:** `canonical_stock_flow_panel_1985_2025_v1.parquet`
- **Processing script:** `analysis/02_derive_stock_flow_metrics.py`
- **Canonical panel method:** `docs/methods/five_year_stock_flow_panel.md`
- **Panel assembly validation:**
  `docs/validation/canonical_stock_flow_panel_assembly.md`
- **Integrated analytical table:**
  `docs/methods/integrated_analytical_panel.md`

## Purpose

This stage derives analysis-ready variables from the validated five-year
stock-and-flow panel. It translates canonical areas and directed flows into
explicit measures of consolidation, replenishment, balance, source-stock
conversion rates, pasture origin, spatial support, and analytical-population
membership.

The canonical input remains unchanged. All 90 original columns are preserved,
and the 32 derived columns are appended in a separate Parquet file. The
derived table retains all 199,112 cell-interval observations, including
structural zeros and the diagnostic 2020-2025 interval.

## Temporal scope

The table contains eight five-year intervals from 1985 to 2025. The variable
`primary_inference_interval` distinguishes the primary analytical period from
the diagnostic extension:

```text
primary_inference_interval = 1, for intervals ending no later than 2020
primary_inference_interval = 0, for 2020-2025
```

The diagnostic interval remains in the table and uses the same definitions.
It is not included in primary inferential results unless a later documented
decision changes the temporal boundary.

## Spatial-support metrics

Complete hexagonal geometry, rasterized area, and valid MapBiomas area are
kept distinct. For each cell and interval:

```text
raster_fraction_geometry = raster_area_ha / geometry_area_ha

valid0_fraction_geometry = valid0_area_ha / geometry_area_ha

valid1_fraction_geometry = valid1_area_ha / geometry_area_ha

minimum_valid_fraction_geometry =
    min(valid0_fraction_geometry, valid1_fraction_geometry)
```

The diagnostic flag is:

```text
valid_support_below_99pct =
    1, if minimum_valid_fraction_geometry < 0.99
    0, otherwise
```

This flag does not exclude observations. It supports description and later
sensitivity analysis of boundary cells. A low valid fraction must not be
interpreted as an intact cell, a stable pixel history, or absence of land-use
dynamics.

## Focal stock proportions

The proportions of native vegetation, planted pasture, and temporary
agriculture are calculated relative to valid land-cover area at the
corresponding endpoint:

```text
stock0_<state>_fraction_valid = stock0_<state> / valid0_area_ha

stock1_<state>_fraction_valid = stock1_<state> / valid1_area_ha
```

where `<state>` is `nat`, `pas`, or `tmp`.

These proportions use valid raster support rather than complete cell geometry.
The support fractions remain available so that the amount of valid evidence
can be evaluated separately.

## Net stock changes

For each focal state:

```text
delta_stock_<state>_ha = stock1_<state> - stock0_<state>
```

The derived fields are:

```text
delta_stock_nat_ha
delta_stock_pas_ha
delta_stock_tmp_ha
```

Net stock change is distinct from directed gross flows. A zero net change can
coexist with large and opposing gains and losses within the same cell and
interval.

## Consolidation and replenishment

The two core directed flows are defined as:

```text
consolidation_ha = flow_pas_tmp

replenishment_ha = flow_nat_pas
```

`Consolidation` denotes area classified as planted pasture at the beginning of
the interval and temporary agriculture at the end. `Replenishment` denotes
area classified as native vegetation at the beginning and planted pasture at
the end.

These are operational land-cover accounting terms. They do not by themselves
identify causal mechanisms, land-management intention, commodity drivers, or
the complete annual trajectory followed by a pixel.

The endpoint flow from native vegetation to temporary agriculture is retained
as:

```text
nat_to_tmp_endpoint_flow_ha = flow_nat_tmp
```

It is deliberately not named `direct conversion`. Intermediate annual states
may exist between the two endpoints.

## Gross activity and net balance

Gross consolidation-replenishment activity is:

```text
gross_cr_activity_ha = consolidation_ha + replenishment_ha
```

The directional difference is:

```text
net_cr_balance_ha = consolidation_ha - replenishment_ha
```

Positive values indicate more consolidation than replenishment, and negative
values indicate more replenishment than consolidation. This balance concerns
only the two specified directed flows. It is not equivalent to the net change
in pasture stock because pasture also exchanges area with native vegetation,
other agricultural classes, water, other land-cover states, and masked areas.

## Bounded balance index

The normalized balance is:

```text
cr_balance_index =
    (consolidation_ha - replenishment_ha)
    / (consolidation_ha + replenishment_ha)
```

The index ranges from -1 to +1:

| Value | Meaning |
|---:|---|
| `-1` | Replenishment only |
| Between `-1` and `0` | Both processes, with replenishment larger |
| `0` | Equal consolidation and replenishment |
| Between `0` and `1` | Both processes, with consolidation larger |
| `1` | Consolidation only |
| `NA` | Neither process occurred above the numerical tolerance |

The denominator is considered zero when gross activity is no greater than
`1e-9` ha. In that case the index is undefined and is stored as `NA`, not zero.

## Source-stock conversion rates

The fraction of the initial pasture stock converted to temporary agriculture
is:

```text
consolidation_rate_initial_pasture =
    consolidation_ha / stock0_pas
```

The fraction of the initial native-vegetation stock converted to pasture is:

```text
replenishment_rate_initial_native =
    replenishment_ha / stock0_nat
```

Rates are undefined when the corresponding initial stock is no greater than
`1e-9` ha and are stored as `NA`. These rates measure conversion relative to
the available source stock. They are different from each flow expressed as a
fraction of total valid cell area.

## Origin of pasture converted to temporary agriculture

For observations with positive consolidation, the pasture-age components are
expressed as shares of total `PAS->TMP` area:

```text
pas_tmp_censored_share =
    pas_tmp_censored / consolidation_ha

pas_tmp_new_share =
    pas_tmp_new / consolidation_ha

pas_tmp_unresolved_age_share =
    pas_tmp_unresolved_age / consolidation_ha

pas_tmp_unattributed_age_share =
    pas_tmp_unattributed_age / consolidation_ha
```

The four shares are mutually exclusive and exhaustive. They must sum to one
within numerical tolerance whenever consolidation is positive.

When consolidation is zero, all four shares are undefined and stored as `NA`.
They are not recorded as zero because no composition exists without a
denominator.

The unresolved-age component preserves source code `1` without decoding it as
a numerical pasture age. Its treatment follows
`docs/decisions/003_unresolved_pasture_age_code.md`.

## Analytical-population flags

Occurrence is defined using the `1e-9`-ha numerical tolerance:

```text
has_consolidation = 1, if consolidation_ha > 1e-9

has_replenishment = 1, if replenishment_ha > 1e-9

has_cr_activity = 1, if either process is present

has_both_cr_processes = 1, if both processes are present
```

The categorical field `cr_activity_class` has four mutually exclusive values:

| Class | Consolidation | Replenishment |
|---|---:|---:|
| `none` | 0 | 0 |
| `consolidation_only` | 1 | 0 |
| `replenishment_only` | 0 | 1 |
| `both` | 1 | 1 |

These flags define analytical subsets without changing the fixed spatial
domain or removing structural zeros from the canonical table.

## Aggregate and cell-level quantities

The interval summary reports two different forms of the balance statistic:

```text
aggregate_cr_balance_index =
    (sum(consolidation_ha) - sum(replenishment_ha))
    / (sum(consolidation_ha) + sum(replenishment_ha))
```

and:

```text
median_active_cell_cr_balance_index =
    median(cr_balance_index among cells with has_cr_activity = 1)
```

These quantities answer different questions and must not be used
interchangeably. The aggregate index weights cells according to their flow
areas. The median gives every active cell equal weight regardless of the
amount of activity.

Similarly, aggregate conversion rates are ratios of summed numerators and
denominators, not arithmetic means of cell-level rates:

```text
aggregate_consolidation_rate_initial_pasture =
    sum(consolidation_ha) / sum(stock0_pas)

aggregate_replenishment_rate_initial_native =
    sum(replenishment_ha) / sum(stock0_nat)
```

## Validated output structure

The derived table is:

```text
canonical_stock_flow_derived_metrics_1985_2025_v1.parquet
```

It contains:

| Component | Count |
|---|---:|
| Cell-interval rows | 199,112 |
| Original canonical columns | 90 |
| Derived columns | 32 |
| Total columns | 122 |
| Distinct cells | 24,889 |
| Five-year intervals | 8 |

The accepted file has SHA-256 checksum:

```text
671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302
```

The interval summary and validation record are:

```text
outputs/summary/canonical_stock_flow_derived_metrics_summary_v1.csv

outputs/validation/
canonical_stock_flow_derived_metrics_validation_v1.json
```

## Validation results

The derived table passed the following checks:

| Check | Result |
|---|---:|
| Canonical columns changed | 0 |
| Duplicate cell-interval records | 0 |
| Infinite derived values | 0 |
| Balance values outside `[-1, 1]` | 0 |
| Pasture-origin share closure violations | 0 |
| Maximum share-closure difference | `1.776357e-15` |

Missing derived values occur only where their denominators are absent:

| Variable group | `NA` records | Reason |
|---|---:|---|
| `cr_balance_index` | 38,168 | Neither consolidation nor replenishment |
| `PAS->TMP` origin shares | 123,368 | No consolidation |
| Consolidation rate | 42,127 | No initial pasture stock |
| Replenishment rate | 36 | No initial native-vegetation stock |

## Distributional consequence for spatial analysis

Across the complete table, the activity classes are:

| Class | Cell-interval records |
|---|---:|
| `replenishment_only` | 85,200 |
| `both` | 75,373 |
| `none` | 38,168 |
| `consolidation_only` | 371 |

The balance index therefore has a large mass at `-1`, a much smaller mass at
`+1`, and undefined values for inactive observations. Its median among active
cells is close to `-1` in every interval.

This distribution is a substantive property of the accounting result, not a
calculation error. It also means that the index must not automatically be
treated as an ordinary continuous response across the complete domain.

Spatial analysis should distinguish at least:

1. occurrence of each process;
2. process combination represented by `cr_activity_class`;
3. flow intensity or source-stock conversion rate; and
4. balance composition among cells where both processes occur.

Global or local spatial-autocorrelation analyses must specify which of these
responses and analytical populations they address. Inactive cells must not be
silently recoded from `NA` to zero in the balance index.

## Interpretation boundaries

- Consolidation and replenishment are directed endpoint flows, not complete
  annual trajectories.
- `NAT->TMP` between endpoints does not demonstrate direct conversion without
  examining the intervening annual classifications.
- Net cell-level stock change does not describe pixel alternation or gross
  exchange.
- A zero net balance in a 20,000-ha cell can result from equal opposing flows;
  it does not necessarily indicate an intact or temporally stable cell.
- Conversely, a cell with no consolidation or replenishment may contain other
  land-cover transitions represented in the canonical accounting fields.
- The derived metrics describe spatial and temporal associations and do not
  identify causal drivers.

The derived table is preserved as an independent canonical product. Its
validated integration with the annual `NAT->TMP` trajectory panel is documented
in `docs/methods/integrated_analytical_panel.md`; integration does not alter any
of the 122 stock-flow fields described here.

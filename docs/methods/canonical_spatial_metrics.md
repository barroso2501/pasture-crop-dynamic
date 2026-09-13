# Canonical spatial metrics

- **Status:** Implemented
- **Implementation date:** 2026-09-13
- **Analysis script:** `analysis/07_build_canonical_spatial_metrics.py`
- **Script version:** `canonical-spatial-metrics-v1`
- **Conditional graph version:** `canonical-cr-balance-active-subgraph-v1`
- **Validation:** `docs/validation/canonical_spatial_metrics_phase2.md`

## Purpose

This method prepares the validated integrated cell-by-interval panel for
spatial description, comparable mapping, temporal classification, and later
spatial-autocorrelation analyses. It joins the accepted analytical values to
the Phase 1 spatial-support attributes, derives prespecified process metrics
and support flags, and records the inherited active-cell subgraph for the
conditional consolidation-replenishment balance.

This stage does not calculate map classes, Moran's I, local indicators of
spatial association, or temporal clusters.

## Inputs and fixed identities

| Input | Role | SHA-256 |
|---|---|---|
| `canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet` | Canonical cell-interval measurements | `7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28` |
| `canonical_integrated_stock_flow_trajectory_summary_v1.csv` | Accepted interval totals | `962803ebccc49f6c2aca14f3cbe7a24143ae2324ed4cbb17a18a2ce62970cab8` |
| `canonical_spatial_support_v1.parquet` | Cell geometry attributes, biome support, and graph membership | `22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc` |
| `canonical_contiguity_weights_v1.parquet` | Fixed shared-edge weights | `85ab9f0dd027545a611c5e681d39b5e2ee5aa185b5c1d318196b91d69392694f` |

All four hashes are checked before computation. The expected analytical
population is a balanced panel of 24,889 cells in eight five-year intervals,
or 199,112 unique `cell_id`, `t0`, `t1` observations.

## Spatial join

The spatial-support table is joined to the integrated panel by `cell_id` with
a validated many-to-one relationship. `GRID_ID` and `source_batch_id` already
exist in both sources and must agree exactly. They are validated rather than
duplicated.

The join adds 34 non-geometric Phase 1 attributes covering:

- canonical-domain and geometry quality control;
- geodesic and equal-area cell areas;
- Earth Engine and equal-area centroid coordinates;
- Amazon and Cerrado overlap areas and fractions;
- primary-biome and boundary-support descriptors; and
- fixed-graph neighbor, island, and component attributes.

Polygon geometry remains in the Phase 1 spatial-support file and is not
repeated in the analytical panel. All original integrated-panel columns and
values must remain unchanged by the join.

## Core process metrics

For cell \(i\) and interval \(t\), the principal spatial variables are:

```text
consolidation_ha       = flow_pas_tmp
replenishment_ha       = flow_nat_pas
gross_cr_activity_ha   = consolidation_ha + replenishment_ha
net_cr_balance_ha      = consolidation_ha - replenishment_ha
nat_tmp_endpoint_ha    = flow_nat_tmp
```

The bounded consolidation-replenishment balance is:

```text
cr_balance_index = net_cr_balance_ha / gross_cr_activity_ha
```

It is defined only when `gross_cr_activity_ha > 1e-9`. Its range is `[-1, 1]`:
negative values indicate replenishment dominance, positive values indicate
consolidation dominance, and zero indicates equal positive flows. A missing
value indicates no C-R activity and is not equivalent to balance zero.

The process-specific relative metrics are:

```text
consolidation_rate_initial_pasture = consolidation_ha / stock0_pas
replenishment_rate_initial_native  = replenishment_ha / stock0_nat
nat_tmp_intensity_initial_native   = nat_tmp_endpoint_ha / stock0_nat
```

Each ratio is defined only when its initial-stock denominator exceeds `1e-9`
ha. Undefined ratios remain missing and receive an explicit support flag.
Absolute process areas and their structural zeros remain available for
complete-domain comparisons.

## Support flags and occurrence thresholds

The panel records whether the following quantities are defined:

- consolidation rate;
- replenishment rate;
- NAT-TMP intensity;
- C-R balance;
- trajectory shares using the NAT-TMP endpoint as denominator; and
- persistence shares using detected pasture area as denominator.

Occurrence flags are produced for consolidation, replenishment, gross C-R
activity, NAT-TMP endpoint flow, NAT-TMP with any detected intermediate
pasture, and NAT-TMP with at least two consecutive intermediate pasture years.

The primary occurrence threshold is an area strictly greater than `1e-9` ha,
consistent with the canonical accounting. Fixed thresholds of `0.1` and `1.0`
ha are retained as sensitivity diagnostics. They do not replace the primary
definition, and the script verifies that the three occurrence sets are
nested.

## C-R balance states

The balance categories are fixed before mapping:

| State | Definition | Interpretation |
|---|---|---|
| `inactive` | gross activity `<= 1e-9` ha | balance undefined |
| `replenishment_dominant` | index `< -1/3` | replenishment exceeds twice consolidation |
| `mixed` | `-1/3 <= index <= 1/3` | neither process exceeds the other by more than 2:1 |
| `consolidation_dominant` | index `> 1/3` | consolidation exceeds twice replenishment |

These categories support mapping and transition summaries. Continuous areas,
rates, and the continuous balance index remain the primary measurements.

## Complete and conditional spatial support

Complete-domain variables retain all 24,889 cells and use the fixed Phase 1
shared-edge graph. Zero is an observed absence of the measured process.

Numerical analysis of `cr_balance_index` uses, in each interval, the induced
subgraph containing only cells with positive gross C-R activity. Edges are
inherited from the fixed graph; no new connection is created across an
inactive gap. The conditional record stores each active cell's neighbor count,
island status, component identifier, and component size. An interval summary
records active and inactive populations, edges, components, islands, degree,
and largest-component size.

Because the active-cell population changes among intervals, conditional
spatial statistics are not directly equivalent through time. Complete-domain
occurrence and absolute-area metrics provide the primary support for temporal
spatial comparison; conditional balance statistics provide complementary
information.

## Outputs

```text
canonical_spatial_metrics_panel_v1.parquet
canonical_spatial_metrics_summary_v1.csv
canonical_cr_balance_active_subgraph_nodes_v1.parquet
canonical_cr_balance_active_subgraph_summary_v1.csv
canonical_spatial_metrics_validation_v1.json
```

The two Parquet files remain in the project data store. GitHub retains the
analysis script, compact summaries, validation JSON, and their recorded
cryptographic identities.

## Interpretation restrictions

- Cell occurrence counts do not measure total converted area or intensity.
- Increasing spatial occurrence does not by itself demonstrate geographic
  expansion, movement, persistence, or clustering.
- A zero C-R balance and an undefined C-R balance represent different states.
- Conditional statistics must report their changing active population and
  inherited graph support.
- Sensitivity thresholds are diagnostics, not post hoc replacements for the
  canonical occurrence rule.
- `2020-2025` remains a diagnostic extension and must be identified as such.
- This stage validates deterministic metric construction; it does not yet
  support inference about spatial autocorrelation or local clusters.

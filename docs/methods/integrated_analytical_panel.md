# Integrated stock-flow and NAT-to-TMP trajectory panel

- **Status:** Implemented and validated
- **Last updated:** 2026-09-12
- **Integration script:**
  `analysis/04_integrate_stock_flow_and_nat_tmp_trajectory.py`
- **Validation:** `docs/validation/canonical_integrated_panel.md`
- **Stock-flow method:** `docs/methods/five_year_stock_flow_panel.md`
- **Derived stock-flow metrics:**
  `docs/methods/derived_stock_flow_metrics.md`
- **Trajectory method:**
  `docs/methods/within_interval_nat_tmp_trajectories.md`

## Purpose

The integrated panel provides one canonical analytical table containing the
validated five-year stock-and-flow accounting, its derived metrics, and the
annual decomposition of the `NAT->TMP` endpoint flow.

Integration does not recalculate either source panel. It performs a one-to-one
join and adds a limited set of transparent trajectory metrics required for
cell-level analysis.

## Canonical inputs

| Input | Rows | Columns | SHA-256 |
|---|---:|---:|---|
| Derived stock-flow table | 199,112 | 122 | `671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302` |
| `NAT->TMP` trajectory panel | 199,112 | 28 | `c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9` |

The two inputs contain the same 24,889 canonical cells in each of eight
five-year intervals. The primary inferential period ends in 2020; 2020-2025
remains present with `diagnostic_interval = 1`.

## Join key and cardinality

The integration key is:

```text
cell_id + t0 + t1
```

Each key must occur exactly once in each source. The ordered key sets must be
identical before the join. The join must preserve all 199,112 rows, including
cells with zero focal flows.

No positive-flow filter is applied. Zero-flow cells remain necessary for the
fixed analytical population, spatial analysis, and valid distinction between
absence of a measured process and absence from the dataset.

## Treatment of shared fields

The derived stock-flow table is the base table. The following fields already
exist in both inputs and are used as controls rather than duplicated:

```text
GRID_ID
source_batch_id
interval
diagnostic_interval
geometry_area_ha
raster_area_ha
```

The first four must match exactly. Geometry and raster-area controls must
agree within `2e-6` ha.

The trajectory `output_version` is retained under the unambiguous name:

```text
trajectory_output_version
```

The integrated table receives its own version field:

```text
integrated_output_version =
canonical-integrated-stock-flow-trajectory-v1
```

## Original trajectory fields incorporated

The integration adds 19 original trajectory fields. They include:

- `trajectory_output_version` and `intermediate_years`;
- the independently calculated `nat_tmp_endpoint_ha`;
- complete and incomplete intermediate-observation areas;
- mutually exclusive areas with zero through four pasture years;
- inclusive, two-or-more-year, and consecutive-two-year pasture areas;
- the inclusive area without a consecutive pair; and
- the five exported trajectory residuals.

The independently calculated trajectory endpoint is retained because it is a
useful external closure control. It must agree with both `flow_nat_tmp` and
`nat_to_tmp_endpoint_flow_ha` within `2e-6` ha.

## Complementary trajectory metrics

Eight cell-level fields are calculated after the join.

### Descriptive area aliases

```text
nat_tmp_without_intermediate_pasture_ha =
    nat_tmp_pas_years_0_ha

nat_tmp_pas_one_year_only_ha =
    nat_tmp_pas_years_1_ha

nat_tmp_pas_2plus_nonconsecutive_ha =
    nat_tmp_pas_2plus_ha
    - nat_tmp_pas_consecutive2_ha
```

The first field means no pasture was detected in the four intermediate annual
observations with complete support. It does not demonstrate direct conversion.

### Shares of the endpoint flow

```text
nat_tmp_pas_any_share_endpoint =
    nat_tmp_pas_any_ha / nat_tmp_endpoint_ha

nat_tmp_pas_2plus_share_endpoint =
    nat_tmp_pas_2plus_ha / nat_tmp_endpoint_ha

nat_tmp_pas_consecutive2_share_endpoint =
    nat_tmp_pas_consecutive2_ha / nat_tmp_endpoint_ha

nat_tmp_mid_incomplete_share_endpoint =
    nat_tmp_mid_incomplete_ha / nat_tmp_endpoint_ha
```

### Persistence within detected pasture

```text
nat_tmp_pas_consecutive2_share_any =
    nat_tmp_pas_consecutive2_ha / nat_tmp_pas_any_ha
```

This last metric describes the share of inclusive pasture evidence that meets
the consecutive-two-year persistence definition. It is not the share of the
complete `NAT->TMP` endpoint flow.

## Undefined shares

A share is undefined rather than zero when its denominator is zero:

- endpoint-based shares are `NaN` when `nat_tmp_endpoint_ha <= 1e-9` ha; and
- the persistence share is `NaN` when `nat_tmp_pas_any_ha <= 1e-9` ha.

These missing values are structural and intentional. Replacing them with zero
would conflate absence of the denominator with a measured zero proportion.

## Output

The canonical output is:

```text
canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet
```

It contains:

| Component | Columns |
|---|---:|
| Preserved derived stock-flow table | 122 |
| Original trajectory fields added | 19 |
| Complementary trajectory metrics | 8 |
| Integrated version field | 1 |
| **Total** | **150** |

The output contains 199,112 rows and has SHA-256:

```text
7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28
```

The interval-level companion output is:

```text
canonical_integrated_stock_flow_trajectory_summary_v1.csv
```

## Validation requirements

Integration is accepted only when:

1. both input hashes match their validated versions;
2. both inputs contain 199,112 unique cell-interval keys;
3. the key sets and shared metadata agree;
4. geometry and raster-area differences remain within `2e-6` ha;
5. all 122 stock-flow columns remain unchanged;
6. all 19 incorporated trajectory fields remain unchanged;
7. `nat_tmp_endpoint_ha` reconciles with both endpoint fields;
8. no row is created, lost, or duplicated;
9. derived areas are non-negative within `1e-9` ha;
10. defined shares lie within `[0, 1]`; and
11. undefined shares correspond only to zero denominators.

## Analytical boundaries

The integrated table places distinct measurements in one row but does not make
them conceptually interchangeable:

- net stock balance is not a gross directed flow;
- cell-level balance is not pixel alternation;
- five-year `NAT->TMP` area is not an annual trajectory;
- pasture detected in an intermediate year is not proof of a stable land-use
  stage; and
- absence of detected pasture is not proof of direct conversion.

The integrated panel is the input for subsequent temporal summaries, biome
comparisons, spatial autocorrelation, and MAUP analyses. Those analyses must
preserve the fixed cell population and identify any process-specific subset or
denominator explicitly.

# Canonical integrated analytical panel validation

- **Status:** Passed
- **Validation date:** 2026-09-12
- **Method:** `docs/methods/integrated_analytical_panel.md`
- **Integration script:**
  `analysis/04_integrate_stock_flow_and_nat_tmp_trajectory.py`

## Scope

This document records the validated integration of the canonical derived
stock-flow table and the canonical annual `NAT->TMP` trajectory panel. The
result provides one cell-by-interval analytical table without changing either
source dataset.

Validation covers source identity, join cardinality, shared metadata, spatial
support, endpoint reconciliation, preservation of original fields, derived
trajectory metrics, and interval-level summaries.

## Input identity

| Input | SHA-256 | Status |
|---|---|---|
| `canonical_stock_flow_derived_metrics_1985_2025_v1.parquet` | `671d4ec50023aa3ea4064ef670c7682746a5dc907bff78f51f6213639d731302` | Matched validated input |
| `canonical_nat_tmp_trajectory_panel_1985_2025_v1.parquet` | `c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9` | Matched validated input |

The input checks prevent integration against an unvalidated or silently
modified panel.

## Output identity

| Output | SHA-256 |
|---|---|
| `canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet` | `7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28` |
| `canonical_integrated_stock_flow_trajectory_summary_v1.csv` | `962803ebccc49f6c2aca14f3cbe7a24143ae2324ed4cbb17a18a2ce62970cab8` |

The output version is:

```text
canonical-integrated-stock-flow-trajectory-v1
```

## Structural validation

| Check | Result |
|---|---:|
| Rows | 199,112 |
| Columns | 150 |
| Distinct `cell_id` values | 24,889 |
| Five-year intervals | 8 |
| Duplicate cell-interval keys | 0 |
| Stock-flow columns preserved | 122 of 122 |
| Original trajectory fields added and preserved | 19 of 19 |
| Complementary trajectory metrics added | 8 |

The integration preserved the complete fixed analytical population, including
structural-zero rows. No record was lost, duplicated, or created by the join.

## Shared-field validation

| Shared field | Result |
|---|---:|
| `GRID_ID` mismatches | 0 |
| `source_batch_id` mismatches | 0 |
| `interval` mismatches | 0 |
| `diagnostic_interval` mismatches | 0 |
| Maximum `geometry_area_ha` difference | `7.275958e-12` ha |
| Maximum `raster_area_ha` difference | `7.078052e-7` ha |

The numerical spatial-support differences are below the accepted `2e-6`-ha
tolerance and reflect floating-point serialization rather than different
geometries or raster lattices.

## Endpoint reconciliation

The independently calculated trajectory endpoint was compared with both:

```text
flow_nat_tmp
nat_to_tmp_endpoint_flow_ha
```

| Check | Result |
|---|---:|
| Maximum difference from `flow_nat_tmp` | `2.235197e-8` ha |
| Maximum difference from derived endpoint field | `2.235197e-8` ha |
| Rows above `2e-6` ha | 0 |

The maximum observed difference is approximately 1.12% of the tolerance. The
trajectory fields therefore decompose the same endpoint flow already accepted
in the stock-and-flow accounting.

## Derived-metric validation

| Check | Result |
|---|---:|
| Infinite derived values | 0 |
| Defined shares outside `[0, 1]` | 0 |
| Minimum two-or-more-year nonconsecutive area | 0 ha |
| Area-alias identity violations | 0 |

The integrated table contains intentional undefined shares:

| Field group | `NaN` rows | Reason |
|---|---:|---|
| Endpoint-based pasture shares | 131,811 | `nat_tmp_endpoint_ha <= 1e-9` ha |
| Consecutive share of inclusive pasture | 152,062 | `nat_tmp_pas_any_ha <= 1e-9` ha |

These values represent zero denominators rather than missing joins or failed
calculations. Positive denominators always have defined shares.

## Interval-level integration check

The integrated summary reproduces the validated stock-flow totals exactly.
Trajectory totals differ from their source summary only at floating-point
precision, with a maximum absolute difference below `1e-9` ha.

| Interval | Consolidation (Mha) | Replenishment (Mha) | Balance index | `NAT->TMP` (Mha) | Any pasture share | Consecutive pasture share |
|---|---:|---:|---:|---:|---:|---:|
| 1985-1990 | 1.450 | 16.427 | -0.8378 | 1.402 | 10.3554% | 9.9632% |
| 1990-1995 | 1.639 | 16.854 | -0.8228 | 1.181 | 8.7521% | 8.3180% |
| 1995-2000 | 1.810 | 15.647 | -0.7927 | 1.225 | 6.4570% | 6.1489% |
| 2000-2005 | 3.504 | 16.926 | -0.6569 | 2.295 | 6.8869% | 6.5445% |
| 2005-2010 | 2.826 | 10.058 | -0.5613 | 0.945 | 8.5029% | 8.1016% |
| 2010-2015 | 4.975 | 8.698 | -0.2723 | 1.362 | 9.8415% | 9.3305% |
| 2015-2020 | 3.916 | 9.017 | -0.3944 | 0.741 | 11.0216% | 10.2817% |
| 2020-2025 diagnostic | 2.086 | 10.039 | -0.6559 | 0.682 | 7.4066% | 6.9325% |

The table is a validation summary, not a statistical trend test. Aggregate
balance values are ratios of aggregate areas and must not be substituted for
the distribution of cell-level balance indices.

## Acceptance

The integration passes source-identity, structural, cardinality, preservation,
spatial-support, endpoint-reconciliation, derived-metric, and summary checks.
The Parquet output is accepted as the canonical integrated analytical panel.

The integration does not change the scientific limitations of its sources. In
particular:

- the stock-flow accounting does not measure pixel alternation;
- the trajectory analysis does not identify causation;
- no-pasture observation does not establish direct conversion;
- the 2020-2025 interval remains diagnostic; and
- classification accuracy remains a source-data limitation rather than an
  accounting-closure question.

Subsequent temporal and spatial analyses must use the output hash recorded in
this document or explicitly document any later version.

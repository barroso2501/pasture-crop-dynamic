# Phase 8B method — Core metrics on alternative MAUP grids

## Purpose

Phase 8B reconstructs a restricted set of central land-cover metrics directly
on the three alternative grids created in Phase 8A. It supplies the measurement
panel required for the later MAUP comparison. It does not yet calculate Moran's
I, LISA clusters or a final robustness classification.

## Fixed analytical footprint

The footprint is the union of the 24,889 canonical cells. It is held fixed
across grids and intervals. Alternative cells are not selected from endpoint
land cover, and canonical cell values are not interpolated or redistributed.
Each process is recomputed from the source rasters on the alternative geometry.

The three alternative grids are:

| Grid | Design | Positive-support cells |
|---|---|---:|
| `hex10k_base` | approximately 10,000-ha regular hexagons | 56,520 |
| `hex20k_shift` | approximately 20,000-ha regular hexagons with shifted origin | 29,396 |
| `hex40k_base` | approximately 40,000-ha regular hexagons | 15,309 |

Complete hexagons are retained. `domain_support_fraction` records the share of
each complete cell intersecting the fixed footprint.

## Temporal scope

The panel contains eight five-year intervals:

```text
1985–1990
1990–1995
1995–2000
2000–2005
2005–2010
2010–2015
2015–2020
2020–2025
```

The last interval is included and marked with `diagnostic_interval = 1`. It is
not removed from extraction, validation or descriptive comparison.

## Extracted areas

For each alternative cell and interval, the common-mask Earth Engine export
records:

- fixed raster-domain support;
- observed and unobserved area at both endpoints;
- initial native-vegetation stock;
- initial pasture stock;
- consolidation area, `PAS → TMP`;
- replenishment area, `NAT → PAS`;
- endpoint native-to-temporary-agriculture area, `NAT → TMP`.

Observed and unobserved endpoint areas use the same support mask as the fixed
raster-domain area. This ensures that the identity

```text
observed endpoint area + unobserved endpoint area
= raster-domain support area
```

is testable per cell.

## Derived metrics

The Colab validator derives:

```text
gross_cr_activity_ha = consolidation_ha + replenishment_ha
net_cr_balance_ha = consolidation_ha - replenishment_ha
cr_balance_index = net_cr_balance_ha / gross_cr_activity_ha
```

The balance index is undefined when gross C–R activity is zero.

Three relative metrics use process-specific initial stocks:

```text
consolidation_rate_initial_pasture
    = consolidation_ha / stock0_pas_ha

replenishment_rate_initial_native
    = replenishment_ha / stock0_nat_ha

nat_tmp_intensity_initial_native
    = nat_tmp_endpoint_ha / stock0_nat_ha
```

Each rate has a separate defined flag. A missing denominator is not converted
to zero.

## Support scopes

Four nested scopes are summarized:

| Scope | Rule | Role |
|---|---|---|
| `all_positive` | support fraction > 0 | complete extraction accounting |
| `support_ge_25pct` | support fraction ≥ 0.25 | lower-threshold sensitivity |
| `support_ge_50pct_primary` | support fraction ≥ 0.50 | prespecified primary cell-level support |
| `support_ge_75pct` | support fraction ≥ 0.75 | higher-threshold sensitivity |

The corresponding fixed cell populations are:

| Grid | Positive | ≥25% | ≥50% | ≥75% |
|---|---:|---:|---:|---:|
| `hex10k_base` | 56,520 | 52,404 | 49,716 | 47,191 |
| `hex20k_shift` | 29,396 | 27,352 | 25,015 | 22,426 |
| `hex40k_base` | 15,309 | 13,759 | 12,445 | 11,160 |

The support threshold flags are fixed across time. Phase 8B reports all four
scopes and does not redefine the threshold after inspecting process values.

## Aggregate comparison with the canonical grid

For every grid and interval, total consolidation, replenishment and `NAT → TMP`
are compared with the accepted Phase 2 canonical totals. The comparison uses
all positive-support alternative cells because their complete union represents
the fixed footprint.

Decision 015 defines the geometric tolerance. The effective relative tolerance
is calculated separately for each grid and interval as the maximum of the base
relative tolerance and that grid-interval's vector–raster support discrepancy.
The tolerance is independent of process outcomes.

## Validation sequence

The validator requires:

1. all expected raw exports and populations;
2. unique grid-cell-interval keys;
3. stable grid metadata across intervals;
4. non-negative and finite areas;
5. closure of observed/unobserved partitions;
6. process areas not exceeding their source stocks;
7. derived indices and rates within valid domains;
8. fixed support-threshold populations;
9. temporal support invariance within each grid;
10. agreement with the fixed vector domain;
11. bounded cross-grid support variation;
12. canonical-total agreement under the geometric tolerance;
13. retention of 2020–2025 as diagnostic.

## Implementation

The accepted validator is:

```text
analysis/13d_build_validate_maup_core_metrics_v4.py
```

Script version:

```text
phase8b-build-validate-maup-core-metrics-v4
```

SHA-256:

```text
3cdc9622ce57a7c912636f50529304daf5e722840e9a83fb02aaf68653e904fa
```

Large raw exports and the full alternative-grid Parquet remain outside GitHub.
Their identities are retained in inventories and the validation JSON.

## Interpretation boundaries

Phase 8B establishes measurement consistency across alternative spatial units.
It does not by itself demonstrate that a scientific conclusion is robust to
MAUP. Robustness requires the next stage to compare distributions, temporal
patterns and selected spatial statistics using prespecified criteria.


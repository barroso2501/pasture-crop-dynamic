# Canonical comparable map classes: Phase 3A final validation

- **Status:** PASS; Phase 3A accepted and Phase 3B authorized
- **Validation date:** 2026-09-13
- **Map-class version:** `canonical-comparable-map-classes-v2`
- **Analysis script:** `analysis/08a_build_comparable_map_classes.py`
- **Script SHA-256:** `6400950446f48a0efc8c6477c1140a670196060fa3cfebf1dddc29a3b3a5baf8`
- **Decision:** `docs/decisions/008_minimum_support_for_nat_tmp_share_maps.md`

## Scope

The final Phase 3A run constructed and validated fixed comparable classes for
12 spatial metrics. Limits were fitted from the pooled population of the seven
primary intervals and then applied unchanged to all eight intervals. The
diagnostic 2020-2025 interval did not influence any fitted limit. No maps were
created in this phase.

This run supersedes the preliminary `v1` class-limit artifact for downstream
mapping. The `v1` files remain diagnostic provenance for Decision 008; Phase
3B must consume the final `v2` limits.

## Structural validation

| Check | Result |
|---|---:|
| Input rows | 199,112 |
| Input columns | 211 |
| Distinct cells | 24,889 |
| Intervals | 8 |
| Primary rows used to fit limits | 174,223 |
| Diagnostic rows excluded from fitting | 24,889 |
| Metrics with one frozen specification | 12 |
| Distribution rows | 96 |
| Class-count rows | 504 |
| Final share-support summary rows | 18 |
| Interval sensitivity rows | 112 |
| Pooled sensitivity rows | 14 |
| Automated validation checks passed | 22 of 22 |

Independent review also confirmed that defined and undefined populations,
low-support and eligible populations, zero and nonzero populations, and all
metric-by-interval class counts close exactly. Every metric and interval sums
to 24,889 cells.

## Final frozen limits

| Metric | Break 1 | Break 2 | Method |
|---|---:|---:|---|
| `consolidation_ha` | 70.545271 | 937.519185 | pooled positive median and p90 |
| `consolidation_rate_initial_pasture` | 0.018789 | 0.255981 | pooled positive median and p90 |
| `replenishment_ha` | 311.675287 | 1,849.499623 | pooled positive median and p90 |
| `replenishment_rate_initial_native` | 0.028805 | 0.165354 | pooled positive median and p90 |
| `nat_tmp_endpoint_ha` | 13.353057 | 357.793168 | pooled positive median and p90 |
| `nat_tmp_intensity_initial_native` | 0.001690 | 0.034065 | pooled positive median and p90 |
| `nat_tmp_pas_any_ha` | 2.663890 | 47.732251 | pooled positive median and p90 |
| `nat_tmp_pas_any_share_endpoint` | 0.098669 | 0.570658 | eligible pooled positive median and p90 |
| `nat_tmp_pas_consecutive2_ha` | 2.734693 | 48.190941 | pooled positive median and p90 |
| `nat_tmp_pas_consecutive2_share_endpoint` | 0.092363 | 0.554050 | eligible pooled positive median and p90 |
| `net_cr_balance_ha` | 348.970427 | 1,912.278490 | symmetric pooled absolute median and p90 |
| `cr_balance_index` | -0.333333 | 0.333333 | fixed substantive states |

Full-precision values and class labels are stored in
`canonical_comparable_map_class_limits_v2.csv`.

## Implementation of minimum trajectory-share support

Decision 008 was implemented as:

```text
nat_tmp_endpoint_ha > 0.001 x geometry_area_aea_ha
```

The actual cell-specific threshold ranged from 19.999197 to 20.000258 ha,
confirming that the implementation used 0.1% of each cell's AEA area rather
than a rounded universal 20 ha constant.

Across the seven primary intervals, 56,674 rows have positive `NAT->TMP`
endpoint flow. Of these, 32,371 are low support and 24,303 are eligible for
cell-level share classification.

| Final support result | Any pasture | Consecutive two years |
|---|---:|---:|
| Not applicable | 117,549 | 117,549 |
| Low support | 32,371 | 32,371 |
| Eligible | 24,303 | 24,303 |
| Eligible zero | 3,100 | 3,583 |
| Eligible positive | 21,203 | 20,720 |
| Endpoint area retained | 98.03% | 98.03% |
| Trajectory area retained | 94.83% | 95.02% |
| Aggregate share on eligible support | 8.26% | 7.87% |

All six prescribed share states are mutually exclusive and exhaustive:
`not_applicable`, `low_support`, `zero`, `positive_low`,
`positive_moderate`, and `positive_high`.

The support rule affects only proportional cell classification. Low-support
flows remain part of absolute-area maps, occurrence summaries, and complete
accounting totals. The result does not identify those observations as source
classification errors.

## Diagnostic interval

The 24,889 records from 2020-2025 were classified with the frozen `v2` limits
but excluded from their estimation. Its six-state populations close exactly,
including 7,551 low-support and 14,262 not-applicable records for each share
metric. Its diagnostic designation is unchanged.

## Output identity

| Final output | SHA-256 |
|---|---|
| `canonical_comparable_map_class_limits_v2.csv` | `b8861926a1ceb02ad8c065cbc4ea46ca6b4af2fed61561e4eb615c7aa5fc981d` |
| `canonical_comparable_map_distributions_v2.csv` | `334649109495530148e1a13437804ee71048e4c6aeda8075dde89685ddbbebc3` |
| `canonical_comparable_map_class_counts_v2.csv` | `1740b1fa90d47a2031202426efb0973a02ea93a8e94f20a00323e382fe54a908` |
| `canonical_trajectory_share_support_summary_v2.csv` | `5597577f51a4b2eb344c5d42505d4b1e327e718b612ad21ae145aa255f242fea` |
| `canonical_share_denominator_sensitivity_v2.csv` | `bb079d1798209f33a6756b027eb17292f89b3d29c332b7d6a8555f93c71e81b8` |
| `canonical_share_denominator_sensitivity_pooled_v2.csv` | `4adaca6dcc7693584d02a4c0e662bbef6203ad995fd67295e573e11eb578ec4f` |
| `canonical_map_classes_validation_v2.json` | `cb909c77372c34947d670342db233a51e07f31996a4bb8085947f973937f7343` |

## Acceptance decision and next gate

Phase 3A satisfies all computational and scientific acceptance criteria. Its
final limits are frozen. No Phase 3A reprocessing is required.

Phase 3B is authorized to create comparable maps, provided it:

- reads `canonical_comparable_map_class_limits_v2.csv` as an input;
- does not refit limits by interval, biome, or mapped subset;
- preserves undefined, inactive, not-applicable, low-support, and zero states;
- labels 2020-2025 as diagnostic; and
- records the cartographic CRS and area-reconciliation result.

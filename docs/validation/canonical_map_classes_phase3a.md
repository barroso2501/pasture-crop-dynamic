# Comparable map-class diagnostic: Phase 3A

- **Status:** Diagnostic passed; ten specifications accepted; two share limits
  require refitting
- **Validation date:** 2026-09-13
- **Analysis script:** `analysis/08a_build_comparable_map_classes.py`
- **Decision:** `docs/decisions/008_minimum_support_for_nat_tmp_share_maps.md`

## Scope

Phase 3A tested the construction of fixed comparable map classes from the
seven primary intervals. It verified input identity, panel structure, temporal
scope, numerical ranges, metric support, class-limit uniqueness, category
closure, and denominator sensitivity. No maps were created.

The computational validation status is `PASS`. Scientific review subsequently
accepted ten specifications and rejected the two preliminary trajectory-share
limits as canonical mapping limits. This distinction is intentional: a
successful computation does not by itself establish that a denominator has
adequate spatial support for interpretation.

## Structural validation

| Check | Result |
|---|---:|
| Input rows | 199,112 |
| Input columns | 211 |
| Distinct cells | 24,889 |
| Intervals | 8 |
| Primary rows used for limits | 174,223 |
| Diagnostic rows excluded | 24,889 |
| Metrics examined | 12 |
| Interval distribution rows | 96 |
| Class-count rows | 488 |
| Interval denominator-sensitivity rows | 112 |
| Pooled denominator-sensitivity rows | 14 |
| Validation checks passed | 18 of 18 |

The 2020-2025 interval did not contribute to any fitted limit.

## Corrected zero and undefined accounting

The final diagnostic run records `cr_balance_index` correctly:

| Status in seven primary intervals | Rows |
|---|---:|
| Defined, nonzero balance | 138,894 |
| Defined numerical zero | 0 |
| Inactive and undefined | 35,329 |

For every metric, defined plus undefined rows equal 174,223, and zero plus
nonzero rows equal the defined population. This corrects the ambiguous compact
metadata produced by the first Phase 3A attempt; analytical classes were not
affected by that earlier labeling problem.

## Pooled denominator sensitivity

The two share metrics have the same `NAT→TMP` denominator population. Results
below refer to the seven primary intervals.

| Minimum endpoint area | Eligible rows | Rows excluded | Endpoint area excluded | Any-pasture positive median | Any-pasture positive p90 | Consecutive-2 positive median | Consecutive-2 positive p90 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `>1e-9` ha | 56,674 | 0.00% | 0.000% | 16.67% | 96.69% | 15.69% | 92.28% |
| `>0.1` ha | 55,285 | 2.45% | 0.001% | 16.33% | 92.67% | 15.32% | 88.68% |
| `>1` ha | 50,063 | 11.66% | 0.030% | 14.37% | 82.53% | 13.64% | 79.79% |
| `>5` ha | 37,625 | 33.61% | 0.378% | 11.51% | 66.59% | 10.84% | 64.96% |
| `>10` ha | 31,193 | 44.96% | 0.889% | 10.54% | 61.66% | 9.87% | 60.12% |
| `>20` ha | 24,303 | 57.12% | 1.975% | 9.87% | 57.07% | 9.24% | 55.41% |
| `>50` ha | 16,542 | 70.81% | 4.700% | 8.59% | 51.02% | 8.09% | 49.51% |

The unweighted share quantiles decline throughout the tested range and do not
reach an empirical plateau. In contrast, area-weighted aggregate shares are
stable over the lower and middle thresholds:

| Support | Any pasture | Consecutive 2 years |
|---|---:|---:|
| Complete positive endpoints | 8.54% | 8.12% |
| Endpoints `>20` ha | 8.26% | 7.87% |
| Endpoints `>50` ha | 7.90% | 7.54% |

At the approximate 20 ha threshold, 98.03% of `NAT→TMP` endpoint area remains,
together with 94.83% of any-pasture trajectory area and 95.02% of the
consecutive-two-year trajectory area. Many excluded ratios therefore
represent very small flows, even though they are numerous as cell-interval
observations.

## Interpretation and resulting decision

The diagnostic does not identify the excluded observations as classification
errors. It demonstrates that proportional cell rankings are highly sensitive
when the endpoint denominator occupies a residual fraction of a 20,000 ha
unit.

Decision 008 therefore defines adequate share support as endpoint flow greater
than 0.1% of each cell's AEA area. The approximate 20 ha diagnostic supports
this scale-based choice because it retains nearly all endpoint area while
separating ratios based on spatially residual flows.

## Output identity

| Diagnostic output | SHA-256 |
|---|---|
| `canonical_comparable_map_class_limits_v1.csv` | `13a762b2758fc3904d59121ed8ee4e38876c365e61ee06f5e26dc7402a02542b` |
| `canonical_comparable_map_distributions_v1.csv` | `a11b268abedafdf7d1fb53e94a6891041f1c4df2e4d89bd7ec5e732ca02eba40` |
| `canonical_comparable_map_class_counts_v1.csv` | `2a9e88311d8651b58c4c50dd95c5bc91c3d071b9822a6047b6364e703b8d546e` |
| `canonical_share_denominator_sensitivity_v1.csv` | `53f4f738645a4eb204764cd674c11ebecd2a9437e0cc551766a8fd89305ee090` |
| `canonical_share_denominator_sensitivity_pooled_v1.csv` | `7bb491f07c74c379d9dcbdbab7449c6323bbaf86b26781ab1502c862ef918039` |
| `canonical_map_classes_validation_v1.json` | `1472d6ff76e7f77de970223bba06ab7f60e34aed51043f09d3bccd0c9fe2965d` |

The class-limit CSV listed above is a diagnostic artifact. Its ten non-share
specifications are accepted, but its two share rows are superseded by Decision
008 and must not be consumed by Phase 3B.

## Next gate

Phase 3A must be rerun with cell-relative 0.1% endpoint support. The rerun must
replace the two share limits, add explicit `not applicable` and `low support`
states, and reconcile all populations and areas. Phase 3B remains blocked
until that final validation passes.

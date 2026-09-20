# Phase 8C validation — MAUP distribution and temporal comparison

- **Status:** PASS; accepted
- **Execution date:** 2026-09-20
- **Script:** `analysis/14a_compare_maup_distributions_and_temporal_patterns.py`
- **Script version:** `phase8c-maup-distribution-temporal-comparison-v1`
- **Script SHA-256:** `18e2e9f347964ef52cf05d6c05e7373241ec5b06d9e3d37625888f1585a50720`

## Structural validation

The two authenticated inputs were harmonized without population loss:

| Component | Rows |
|---|---:|
| Canonical grid | 199,112 |
| Alternative grids | 809,800 |
| **Harmonized total** | **1,008,912** |

The execution produced:

| Output family | Rows |
|---|---:|
| Aggregate summary | 32 |
| Aggregate comparisons | 192 |
| Weighted distribution summaries | 768 |
| Distribution comparisons | 576 |
| Temporal comparisons | 48 |
| Robustness assessments | 6 |

All 12 recorded validation checks passed. Input hashes, populations, unique
keys, balanced interval panels, Phase 8A support populations, normalized
absolute-area comparisons, positive distribution weights, conditional support
tracking, separate temporal windows and the diagnostic interval were all
confirmed.

## Prespecified robustness assessments

| Alternative grid | Primary 1985-2020 | Full observed 1985-2025 |
|---|---|---|
| `hex10k_base` | sensitive for at least one criterion | sensitive for at least one criterion |
| `hex20k_shift` | stable under prespecified criteria | stable under prespecified criteria |
| `hex40k_base` | sensitive for at least one criterion | sensitive for at least one criterion |

These classifications are analytical results. They do not conflict with the
overall validation status of `PASS`.

## Aggregate component

All 192 aggregate comparisons passed. No grid changed the sign of an
aggregate metric or the dominance class of the aggregate C-R balance.

The largest ratio between an observed criterion statistic and its allowed
threshold was only `0.0941`. It occurred for consolidation on `hex40k_base` in
1985-1990:

```text
relative difference = 0.0001881
accepted limit       = 0.002
```

Thus, the largest aggregate discrepancy used less than 10% of its accepted
tolerance.

## Temporal component

All 48 temporal comparisons passed in both temporal windows. For every grid
and metric:

- Spearman rank correlation was exactly `1.0`;
- peak interval displacement was zero;
- trough interval displacement was zero;
- sign sequences were preserved;
- C-R dominance sequences were preserved where applicable.

The diagnostic 2020-2025 interval changed neither the assessment of any grid
nor the temporal ordering conclusion.

## Primary distribution component

### Finer 10,000-ha grid

Only one of the 64 full-observed primary-scope comparisons failed. The same
failure lies in the primary period:

| Metric | Interval | Canonical defined support | Alternative defined support | Difference | Limit | KS |
|---|---|---:|---:|---:|---:|---:|
| consolidation rate over initial pasture | 1985-1990 | 0.659769 | 0.609232 | 0.050537 | 0.05 | 0.028680 |

The failure exceeds the coverage limit by `0.000537`, equivalent to 0.0537
percentage point. Its KS distance passes comfortably. The strict assessment is
therefore retained, but the result is described as marginal conditional-
support sensitivity rather than broad distributional instability.

### Shifted 20,000-ha grid

Every primary-scope aggregate, distributional and temporal comparison passed.
The largest primary weighted KS distance was `0.033407`, well below `0.10`.
The results are robust to the prespecified change in lattice origin at
approximately the canonical scale.

### Coarser 40,000-ha grid

The primary period contains 16 failed distribution comparisons. Four
additional failures occur in the diagnostic interval, producing 20 failures
in the full-observed assessment.

In the primary period, 14 failures concern defined-support coverage for:

- `cr_balance_index`; and
- `consolidation_rate_initial_pasture`.

The difference is systematic. In 1985-1990, for example, defined support rises
from 0.708184 to 0.794540 for the C-R index and from 0.659769 to 0.746896 for
the consolidation rate. This is consistent with a scale effect: a larger cell
is more likely to contain some activity or some initial pasture and therefore
to enter the defined population of a conditional metric.

Two primary-period failures concern distributional shape in 2015-2020:

| Metric | Weighted KS | Limit | Excess |
|---|---:|---:|---:|
| `nat_tmp_density_per_10kha` | 0.101381 | 0.10 | 0.001381 |
| `nat_tmp_intensity_initial_native` | 0.101244 | 0.10 | 0.001244 |

The diagnostic 2020-2025 interval repeats these two small KS exceedances and
adds two conditional-support failures. It confirms an existing coarse-scale
effect and does not create a different substantive conclusion.

## Support-threshold sensitivity

Across all three support scopes and eight intervals, 109 of 576 distribution
comparisons failed. Their distribution is:

| Grid and scope | KS failures | Defined-support failures | Total |
|---|---:|---:|---:|
| 10k, primary >=50% | 0 | 1 | 1 |
| 10k, sensitivity >=25% | 0 | 16 | 16 |
| 10k, sensitivity >=75% | 0 | 0 | 0 |
| shifted 20k, primary >=50% | 0 | 0 | 0 |
| shifted 20k, sensitivity >=25% | 0 | 0 | 0 |
| shifted 20k, sensitivity >=75% | 0 | 14 | 14 |
| 40k, primary >=50% | 4 | 16 | 20 |
| 40k, sensitivity >=25% | 0 | 6 | 6 |
| 40k, sensitivity >=75% | 36 | 16 | 52 |

This sensitivity confirms that boundary-support selection affects conditional
coverage and, for the coarse grid at the strictest support threshold, the
shape of several weighted cell distributions. It does not alter the accepted
primary-scope assessment.

## Figure verification

All four figures listed in the inventory were received, visually inspected and
matched their recorded SHA-256 identities. They show:

1. aggregate relative differences far below the 0.2% limit;
2. expected scale dependence of support-weighted cell medians;
3. low zoning sensitivity and larger coarse-scale KS distances;
4. essentially coincident aggregate C-R balance and rate trajectories.

The median-density figure illustrates why cell-level summaries should not be
interpreted independently of spatial resolution. Larger units reduce the mass
of exact-zero cells and can shift the median even when domain totals and
temporal ordering remain stable.

## Output identities

The authoritative inventory is:

```text
outputs/validation/phase8c_maup_comparison_v1/
  canonical_maup_comparison_inventory_v1.csv
```

It authenticates the seven compact numerical tables, the validation JSON and
the four figures. Every received file matched its recorded SHA-256 hash.

## Acceptance statement

Phase 8C is accepted as a valid descriptive and temporal MAUP comparison. The
canonical approximately 20,000-ha grid remains the primary analytical unit.
Aggregate magnitude, process direction and temporal conclusions are robust;
zoning sensitivity at the same nominal scale is low. Cell-distribution and
conditional-support interpretations are scale-sensitive, especially under the
40,000-ha aggregation.

No rerun of Phase 8C is required. Phase 8 is not yet closed because
alternative-grid spatial-autocorrelation and broad cluster-location robustness
remain outside this stage's declared scope.

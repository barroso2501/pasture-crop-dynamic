# Global spatial autocorrelation — Phase 5

## Status and scope

Implementation prepared before real-data Moran results are inspected. Implements
Phase 5 of `docs/planning/006_spatiotemporal_investigation_plan.md`. Phase 4
provided descriptive spatial/temporal findings; Phase 5 evaluates global spatial
association. Local cluster inference belongs to Phase 6. The preliminary biome
comparison in Phase 4 does not complete Phase 7's global/local requirements.

Use all 24,889 canonical cells, not only the selected high NAT–TMP cohort. Process
eight intervals, retaining seven primary and flagged diagnostic 2020–2025.
No class thresholds, neighborhood definitions or primary populations are refitted.

## Fixed metric specifications

Complete-domain primary results:

- raw `consolidation_ha`, `replenishment_ha`, `nat_tmp_endpoint_ha`,
  `gross_cr_activity_ha`, `net_cr_balance_ha`;
- binary occurrence (>1e-9 ha) for C, R, NAT endpoint and gross C–R activity.

These nine specifications produce 72 rows across eight intervals. Preserve
observed zeros. Occurrence and absolute magnitude address different questions;
there is no automatic logarithmic or rank transformation in this implementation.

Conditional complementary results:

| Metric | Accepted support flag |
|---|---|
| `cr_balance_index` | `cr_balance_defined` |
| `consolidation_rate_initial_pasture` | `consolidation_rate_defined` |
| `replenishment_rate_initial_native` | `replenishment_rate_defined` |
| `nat_tmp_intensity_initial_native` | `nat_tmp_intensity_defined` |

These four specifications produce 32 rows. Use declared supported cells and
require unsupported values to remain missing. Undefined balance is not zero.
No intermediate-pasture share metric is added to the inferential family here.

## Neighborhood graph, support and islands

Read accepted Phase 1 directed shared-edge weights: 67,453 undirected links,
134,906 directed records, 264 components, 163 islands, largest component 24,014.
Validate hashes, cell references, uniqueness, zero diagonal, symmetric binary
adjacency and agreement with stored row-standardized weights. Row-standardized
weights need not have symmetric numerical values; binary contiguity must.

Complete specifications use the same fixed graph. Conditional specifications
inherit induced subgraphs on supported cells. Re-standardize surviving binary
edges within each row. No new edges, distance neighbors or k-nearest-neighbor
links are created. Retain every supported island with zero spatial lag. Report
N, excluded population, S0, components, islands, edge count and mean degree for
every metric/interval. Conditional support may vary, so its temporal comparison
is secondary to complete-domain comparison.

## Moran statistic and permutation test

For centered z = y−mean(y), compute:

```text
I = (N/S0) × [sum_i sum_j w_ij z_i z_j] / [sum_i z_i²]
S0 = sum_i sum_j w_ij
```

N and centering include retained islands. With zero-diagonal fixed weights,
E[I] under unrestricted value permutation is −1/(N−1). Constant variables,
N<3 or S0=0 yield an explicitly undefined statistic and no simulated test.

Use 9,999 unrestricted permutations within the observed metric support. The
master seed is 20260915; derive a stable per-metric/transformation/interval seed
from SHA-256, independent of loop ordering. Preserve the simulated I values.
Permutation generation uses fixed batches of up to 64 to limit memory.

The prespecified two-sided Monte Carlo p-value compares absolute departures
from the exact null expectation:

```text
p = [1 + count(|I_perm−E[I]| ≥ |I_obs−E[I]|)] / [9999 + 1]
```

Apply a 1e-12-scaled tolerance to floating-point ties. This definition is explicit;
it is not silently substituted with a package's minimum-tail p-value. Record
observed I, exact expectation, simulated mean/SD, null quantiles and p. The
simulation quantiles describe a permutation reference, not an uncertainty
interval for the true spatial effect or a temporal-difference test.

Random spatial permutations are a standard ESDA reference approach described
by [PySAL](https://pysal.org/). The specific p-value and island conventions above
are the implementation's declared choices.

## Multiple comparisons and temporal status

Use Benjamini–Yekutieli FDR correction at alpha 0.05, retaining the prespecified
family size and allowing dependence among tests. Families are:

| Family | Prespecified rows |
|---|---:|
| Complete-domain primary: nine specifications × seven intervals | 63 |
| Conditional primary: four specifications × seven intervals | 28 |
| Complete-domain diagnostic: nine specifications × one interval | 9 |
| Conditional diagnostic: four specifications × one interval | 4 |

Untestable rows contribute p=1 for conservative family accounting; their status
remains undefined and they are never marked significant. Report raw p and adjusted
q. Diagnostic results do not change primary adjusted values. Do not correct
within each interval only or change the family after seeing results.

## Interpretation and outputs

I estimates global spatial association under the selected graph and metric.
Significance does not replace effect size, locate local clusters, prove a causal
mechanism or establish a significant change between dates. Complete and conditional
I are displayed separately. Global significance is not a mandatory gate for a
prespecified Phase 6 local analysis, as stated in the plan.

Deliver results CSV, support CSV, full permutation NPZ, design JSON, figure and
actual execution validation JSON with input/output hashes. A design/preflight
record is distinct from acceptance of real-data results. This phase needs no
GEE, geometry reconstruction, new coorte selection or upstream rerun.

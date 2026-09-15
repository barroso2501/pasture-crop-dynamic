# Canonical global Moran — Phase 5 execution verification

Date: 2026-09-15. Status: accepted execution; compact outputs and full simulated
reference distributions independently verified.
Execution UTC: `2026-09-15T19:41:37.990348+00:00`.
Script SHA-256: `f6fb91818f246f89bd2702247b2bd30aeb3dc5f70ad321b519ed0c63553146da`.

## Received components and integrity

First archive: results CSV, support CSV and execution validation JSON. Additional
archive: design JSON and full permutation NPZ. Transport CRC checks passed.
All four referenced component hashes match the execution inventory. The source
metrics, weights and support hashes match accepted upstream identities. The
executed script SHA matches the prepared repository-target script bytes.
The original output PNG was not supplied and its bytes/layout were not checked.

## Independent verification

- 104 unique metric/transformation/interval rows: 72 complete, 32 conditional.
- All rows tested with 9,999 permutations; no undefined statistics.
- BY families contain 63/28 primary and 9/4 diagnostic tests, as prespecified.
- Expected I reproduces −1/(supported N−1) for every row.
- Supported plus excluded cells equals 24,889.
- Results/support CSVs match in all shared fields.
- Neighbor histograms reconcile N, islands, edge counts and S0=N−islands.
- Complete graph retains 67,453 undirected links, 264 components, 163 islands
  and largest component of 24,014 cells, consistent with the execution record.
- All 104 NPZ arrays contain 9,999 finite values: 1,039,896 simulated statistics.
- Every simulated mean, sample SD and .025/.975 quantile matches the CSV.
- Recomputed two-sided absolute-deviation p-values with tie tolerance and
  plus-one correction match exactly; all have zero extreme permutations and
  Monte Carlo p=0.0001, the simulation resolution floor.
- All BY adjusted q-values are independently reproduced; all are below .05.

Full machine-readable review is in
`canonical_global_moran_independent_review_v1.json`. It is a later verification
record, not an edit to the original execution JSON. The additional interpretation
figure was rebuilt from the authenticated CSV and visually inspected separately.

## What was not independently replicated

Observed I was not recalculated from the source metric Parquet and graph Parquet;
those full inputs were not received. Runtime acceptance of those inputs is
reported by the identified script, checked against accepted hashes. Simulated
values were reread and their output statistics reproduced, not regenerated from
the seed and graph. No temporal-difference significance test, local association,
cluster map, survival or causal inference is accepted by this verification.

## Outcome

Global Phase 5 production is accepted under the stated review scope and can be
closed after documentary registration. Primary and diagnostic evidence remain
separate. Conditional support changes prohibit treating its I as directly
equivalent to complete-domain results. Phase 6 must prespecify its selective
local analysis and local testing correction; significance is not effect size or
proof of a causal mechanism. No Colab/GEE rerun is required for this acceptance.

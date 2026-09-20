# Canonical MAUP Global Moran validation — Phase 8D

## Status

**Accepted — validation PASS.** Phase 8D reproduced the canonical Phase 5
Global Moran results, constructed the three prespecified alternative-grid
graphs, completed 120 alternative-grid permutation tests, and applied the
frozen Phase 8D comparison criteria.

The accepted implementation is
`analysis/14b_compute_maup_global_moran_v2.py`. Revision 2 changes only the
strict JSON serialization of a non-applicable canonical graph diagnostic to
the declared numeric sentinel `0.0`. It
reused the completed v1 checkpoints and did not change any Moran statistic,
permutation distribution, p-value, corrected q-value, or robustness result.

## Evaluated design

- Canonical grid: 24,889 complete approximately 20,000-ha cells.
- Alternative grids at domain support fraction `>= 0.50`:
  - `hex10k_base`: 49,716 cells and 138,782 undirected edges;
  - `hex20k_shift`: 25,015 cells and 69,656 undirected edges;
  - `hex40k_base`: 12,445 cells and 33,748 undirected edges.
- Metrics: consolidation, replenishment, endpoint `NAT -> TMP`, net C-R
  balance densities per 10,000 ha, and the bounded C-R balance index.
- Temporal coverage: seven primary intervals through 2020 plus the flagged
  diagnostic interval 2020-2025.
- Inference: 9,999 permutations per alternative-grid test; two-sided
  pseudo-p-values; Benjamini-Yekutieli correction within the prespecified
  primary/diagnostic and complete/conditional families.

The graph populations, support rules, permutation seeds and comparison
thresholds were fixed before inspecting the Phase 8D results in Decision 017.

## Structural validation

The accepted files contain:

| Object | Verified count |
|---|---:|
| Moran result rows | 160 |
| Canonical reproduction rows | 40 |
| Alternative-grid permutation tests | 120 |
| Interval-level alternative/canonical comparisons | 120 |
| Temporal comparisons | 30 |
| Grid-window assessments | 6 |
| Stored alternative permutation values | 1,199,880 |

All source validation checks are true. The canonical Phase 5 values were
reproduced exactly within the specified numerical tolerance. Every
alternative graph has a valid axial-neighbor construction; its reported
maximum relative distance error is below `7.1e-14`.

## Independent review

The independent review authenticated all nine files named in the source
inventory and reproduced the inferential calculations from the NPZ archive:

- 120 arrays were present;
- every array contained exactly 9,999 finite values;
- all two-sided pseudo-p-values were reproduced exactly;
- the maximum absolute discrepancy in stored permutation summaries was
  `9.92e-17`;
- the maximum absolute discrepancy in independently recomputed BY q-values
  was `9.28e-17`.

The independent record is
`canonical_maup_global_moran_independent_review_v1.json`. The 9.2 MB NPZ
archive is retained with the full analytical outputs outside GitHub; its
SHA-256 is recorded by the source inventory as
`4af6b60bf6c62dbb51efbc447a3aa3e769382739140b67f0e10c738151495098`.

## Acceptance results

All 120 alternative-grid Moran coefficients were positive and significant
after BY correction. Sign and inferential significance were therefore
preserved in every interval-level comparison. Of the 120 magnitude checks,
119 satisfied the prespecified absolute-difference limit of 0.10.

The single magnitude failure was:

| Grid | Metric | Interval | Canonical I | Alternative I | Absolute difference |
|---|---|---|---:|---:|---:|
| `hex40k_base` | `nat_tmp_density_per_10kha` | 2005-2010 | 0.405113 | 0.507941 | 0.102828 |

Eight of 30 temporal comparisons failed the strict conjunction of Spearman
rank correlation `>= 0.90` and peak/trough displacement `<= 1` interval:

- `hex10k_base`: endpoint `NAT -> TMP` and C-R balance index in both windows;
- `hex20k_shift`: endpoint `NAT -> TMP` in both windows, because its peak was
  displaced by two intervals despite Spearman correlations above 0.95;
- `hex40k_base`: endpoint `NAT -> TMP` in the primary window and C-R balance
  index in the full-observed window.

Consequently, none of the six grid-window assessments passes every
prespecified criterion. This is a conservative aggregate classification, not
evidence that global spatial autocorrelation disappears or changes direction.
The correct interpretation is that the existence, positive direction and
formal significance of global clustering are robust, while the exact
magnitude and temporal ordering are partially scale- and zoning-sensitive,
especially for endpoint `NAT -> TMP`.

## Diagnostic interval

The 2020-2025 interval was included in calculation and inference and remained
explicitly flagged. It did not introduce a sign or significance failure. Its
main effect on the strict temporal evaluation was the full-window trough of
the 40,000-ha C-R balance-index series, which occurred in 1985-1990 rather
than the canonical 2020-2025 trough.

## Decision

Phase 8D is accepted. The canonical approximately 20,000-ha grid remains the
primary analytical support. Claims about positive, significant global spatial
autocorrelation are supported across all tested grids. Claims about the exact
relative ordering of intervals, peak timing, or the magnitude of endpoint
`NAT -> TMP` autocorrelation require the Phase 8D sensitivity qualification.

Phase 8 remains open for the final broad cluster-location and persistence
comparison. Phase 8D does not replace or reinterpret the canonical Local
Moran/LISA analysis.

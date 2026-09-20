# Phase 8D findings — MAUP sensitivity of Global Moran's I

## Main finding

Global spatial autocorrelation is a robust feature of all five focal metrics.
Every tested coefficient was positive, and every one of the 120
alternative-grid tests remained significant after the prespecified
Benjamini-Yekutieli correction. Changing cell size or shifting the lattice did
not reverse the direction of spatial association or remove its inferential
support.

The sensitivity lies in **how large** Moran's I is and **how intervals are
ranked**, not in whether spatial clustering exists.

## Canonical temporal pattern

On the canonical grid, consolidation, replenishment and net C-R balance
density all show strong but declining spatial autocorrelation. From
1985-1990 to 2015-2020, Moran's I declined by 0.240 for consolidation, 0.156
for replenishment and 0.163 for net C-R balance. The diagnostic 2020-2025
interval continued those declines.

Endpoint `NAT -> TMP` was more variable. Its canonical Moran's I peaked at
0.592 in 1990-1995, fell to 0.361 in 2015-2020, and rose to 0.422 in the
diagnostic interval. This non-monotonic profile is also the result most
sensitive to scale and zoning.

The C-R balance index remained consistently and strongly clustered, ranging
from 0.747 to 0.799. Its comparatively narrow range means that small changes
can alter the rank order or the nominal trough without changing the broader
conclusion of persistent spatial structure.

## Scale and zoning comparison

The shifted 20,000-ha grid most closely reproduced canonical magnitudes. Its
mean absolute differences ranged from 0.003 for the C-R balance index and net
balance density to 0.014 for endpoint `NAT -> TMP`. It preserved all interval
magnitude, sign and significance criteria. Its only strict temporal failures
were the two `NAT -> TMP` windows, because the peak moved from 1990-1995 to
2000-2005; their Spearman correlations nevertheless remained 0.964 and 0.952.

The 10,000-ha grid generally produced lower Moran coefficients than the
canonical grid. Its largest absolute difference was 0.086 for endpoint
`NAT -> TMP`; no interval-level threshold failed. Temporal rank sensitivity
occurred for endpoint `NAT -> TMP` and the C-R balance index.

The 40,000-ha grid generally produced higher Moran coefficients, as expected
when coarser aggregation smooths local variation. Endpoint `NAT -> TMP` had
the largest scale effect. Its difference reached 0.102828 in 2005-2010, the
only interval-level magnitude failure among 120 comparisons.

## Interpretation boundaries

These results support statements that all focal processes exhibit positive,
statistically supported global spatial clustering and that the broad decline
in clustering of consolidation, replenishment and net C-R balance is not an
artifact of the canonical lattice.

They do not support treating the exact `NAT -> TMP` peak interval, the exact
C-R balance-index trough, or small differences among adjacent intervals as
grid-invariant. Those details should be reported as sensitive to scale or
zoning.

The six aggregate assessments are all labelled
`sensitive_for_at_least_one_criterion` because the decision rule requires
every interval and every temporal check to pass. That label should not be
summarized as “Global Moran is not robust.” A faithful summary is:

> Positive and significant global spatial autocorrelation is robust across
> the prespecified grids. Exact magnitudes and temporal rankings show partial
> MAUP sensitivity, concentrated in endpoint NAT-to-temporary-crop dynamics.

## Consequence for the next analysis

Global Moran establishes that clustering persists under alternative spatial
supports, but it does not show whether the same geographic areas form the
clusters. The remaining Phase 8 task is therefore a broad cluster-location and
persistence comparison using outcome-independent overlap criteria. The
canonical Local Moran/LISA results remain primary; the alternative grids are
sensitivity supports rather than replacement analyses.


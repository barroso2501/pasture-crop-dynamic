# Phase 8E findings — HH-cluster location and persistence

## Main result

The broad location and persistence of HH clusters are robust for
replenishment, net consolidation–replenishment balance and the bounded C–R
balance index; partially robust for consolidation; and sensitive to scale and
zoning for endpoint `NAT → TMP`.

This conclusion applies to the prespecified BH-primary analysis. It does not
state that alternative grids should replace the canonical approximately
20,000-ha grid.

## Results by metric

| Metric | BH interval passes | Overall assessments passing | Interpretation |
|---|---:|---:|---|
| Replenishment density | 24/24 | 6/6 | Robust across scale, zoning and window |
| Net C–R balance density | 23/24 | 6/6 | Robust overall; one marginal interval failure |
| C–R balance index | 24/24 | 6/6 | Strongest and most consistent agreement |
| Consolidation density | 16/24 | 3/6 | Partial robustness; interval footprints are scale-sensitive |
| Endpoint `NAT → TMP` density | 7/24 | 0/6 | Clear location and persistence sensitivity |

Median interval Jaccard similarity was `0.759` for the C–R index, `0.683` for
replenishment, `0.681` for net C–R balance, `0.482` for consolidation and
`0.319` for endpoint `NAT → TMP`.

## Results by grid

The shifted approximately 20,000-ha grid had the highest median interval
Jaccard (`0.676`) and 33 of 40 interval passes. The approximately 40,000-ha
grid also passed 33 of 40, with median Jaccard `0.639`. The approximately
10,000-ha grid passed 28 of 40, with median Jaccard `0.634`.

These totals should not be read as a single ranking of grid quality. Failures
are concentrated in particular processes, and the three alternative grids
represent different scale or zoning perturbations.

## Consolidation

Consolidation passes all recurrence and persistent-HH temporal criteria, but
several interval footprints fail the joint location rule. The 10,000-ha grid
passes only four of seven primary and four of eight full-observed interval
maps. The 40,000-ha grid passes the primary window but falls to five of eight
in the full window, below the required six.

The appropriate conclusion is partial robustness: persistent geographic
structure remains recognizable, but the significant footprint depends on
cell size in some intervals.

## Endpoint NAT → TMP

Endpoint `NAT → TMP` is the clearest MAUP-sensitive outcome.

- the 10,000-ha grid passes one of seven primary interval maps;
- the shifted 20,000-ha grid passes two of seven;
- the 40,000-ha grid passes four of seven;
- no grid–window assessment meets every prespecified criterion.

For the 10,000-ha primary window, the weighted HH-frequency correlation is
`0.669`, below the `0.70` threshold, and persistent-HH Jaccard is `0.320`.
The full-window frequency correlation rises to `0.714`, but persistent-HH
Jaccard remains `0.311`. The shifted grid has acceptable frequency correlation
but persistent-HH Jaccard of `0.385` in the primary window and `0.382` in the
full window, both just below the `0.40` limit. The 40,000-ha temporal criteria
pass, but too few interval footprints pass.

Many failed `NAT → TMP` comparisons have high overlap coefficients. This
means that one footprint is often largely nested within the other while their
areas differ substantially. The result is not generally wholesale relocation;
it is instability in the extent of the significant HH footprint. The
prespecified paired rule correctly treats this as sensitivity because high
overlap alone cannot compensate for low Jaccard similarity.

An extreme diagnostic case occurs for the 10,000-ha grid in 2020–2025: the
alternative BH-HH footprint is empty while the canonical footprint is not.
This interval is reported as diagnostic and does not create the primary-period
finding; `NAT → TMP` is already sensitive in 1985–2020.

## Relation to Phase 8D

Phase 8D found positive and significant Global Moran coefficients on every
alternative grid. Phase 8E nevertheless finds local HH sensitivity for
`NAT → TMP`. These results are compatible. A stable global tendency toward
positive spatial association does not require the same cells or footprint
extent to be classified as significant local HH clusters under every spatial
partition.

## BY sensitivity

BY results are secondary. Seventy-seven of 120 interval comparisons pass, but
23 of those have empty HH footprints on both supports and therefore receive a
mathematical Jaccard of 1.0. Such empty–empty agreement is not evidence of a
shared hotspot. Only eight of 30 BY temporal comparisons pass. These results
support retaining BH as the primary analysis and BY as a conservative
sensitivity bound.

## Reporting statement

The preferred concise statement is:

> Significant HH-cluster location and persistence were stable across spatial
> supports for replenishment and the two consolidation–replenishment balance
> measures, partially stable for consolidation, and sensitive to scale and
> zoning for endpoint NAT→TMP, mainly through expansion or contraction of
> hotspot footprints around partly shared cores.

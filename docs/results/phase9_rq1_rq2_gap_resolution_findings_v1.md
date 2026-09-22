# Phase 9A.1 findings — fixed 1985 pasture cohort and PAS→TMP origins

## Scope

Phase 9A.1 resolves the two explicit evidence gaps retained by the accepted
Phase 9A evidence matrix. The analysis is descriptive and introduces neither
new causal inference nor new spatial hypothesis testing.

The primary period is 1985–2020. Results for 2025 are included as a diagnostic
extension and do not redefine the primary-period conclusions.

## RQ1 — endpoint fate of the fixed 1985 pasture cohort

The fixed cohort contains pixels classified as planted pasture in 1985 and
carrying pasture-age code 100 in that year. Its initial area is
49.036 million ha, distributed among 16,421 of the 24,889 canonical cells.

At the 2020 endpoint, the cohort is distributed as follows:

| Endpoint state | Area (million ha) | Share |
|---|---:|---:|
| Pasture | 30.957 | 63.13% |
| Temporary agriculture | 9.779 | 19.94% |
| Other agriculture | 4.522 | 9.22% |
| Native vegetation | 3.346 | 6.82% |
| Other, water, or unobserved | 0.432 | 0.88% |

The pasture endpoint share decreases from 100% in 1985 to its primary-period
minimum of 63.13% in 2020. Temporary-agriculture share rises to 19.94% and
other-agriculture share to 9.22% by 2020.

This is an endpoint-composition series, not a survival curve. A pixel may leave
and later return to pasture between reference years. The analysis therefore
does not identify uninterrupted persistence, first transition date, or a
unique intervening pathway.

### Biome contrast

Under whole-cell primary-biome assignment, the 2020 endpoint composition
differs clearly:

| Primary biome | Initial cohort (million ha) | Pasture in 2020 | Temporary agriculture in 2020 |
|---|---:|---:|---:|
| Amazon | 7.747 | 74.82% | 12.02% |
| Cerrado | 41.289 | 60.94% | 21.43% |

Excluding the 582 transbiome cells changes these percentages only slightly:
Amazon pasture and temporary agriculture become 74.90% and 12.01%; Cerrado
becomes 60.91% and 21.44%. The primary-assignment result is therefore not
driven by the treatment of boundary-crossing cells.

### Diagnostic 2025 endpoint

In 2025, pasture represents 58.22% of the fixed cohort, temporary agriculture
21.42%, native vegetation 6.43%, and other agriculture 12.95%. These values
extend the observed description but remain explicitly diagnostic.

## RQ2 — origin of pasture converted to temporary agriculture

PAS→TMP consolidation is partitioned by the pasture-age code at the beginning
of each interval. The origin shifts progressively from the left-censored 1985
pasture stock toward pasture established during the observed series.

| Interval | Left-censored stock | Pasture established during series |
|---|---:|---:|
| 1985–1990 | 100.00% | 0.00% |
| 1990–1995 | 71.01% | 28.99% |
| 1995–2000 | 61.05% | 38.95% |
| 2000–2005 | 53.81% | 46.19% |
| 2005–2010 | 47.85% | 52.15% |
| 2010–2015 | 40.02% | 59.97% |
| 2015–2020 | 37.29% | 62.71% |
| 2020–2025, diagnostic | 30.25% | 69.75% |

Across the seven primary intervals, accumulated consolidation is
20.119 million ha: 51.73% originates from the left-censored stock and 48.27%
from pasture established during the series. The unresolved pasture-age
component is 151.015 ha and the unattributed component is zero.

Across the complete observed series, accumulated consolidation is
22.206 million ha. The unresolved-age component totals 176.720 ha and remains
explicit rather than being assigned an assumed age.

Pooled areas sum interval conversions and do not deduplicate pixels that may
convert in different intervals. Pasture origin is defined at interval start;
it is not the complete historical trajectory of each pixel.

## Evidence integration

Version 2 of the evidence matrix replaces only the two explicit gap rows:

- `P9A001` is replaced by `P9A031`–`P9A034` for RQ1;
- `P9A002` is replaced by `P9A035`–`P9A037` for RQ2.

The resulting matrix contains 35 unique statements, covers RQ1–RQ5, contains
no `evidence_gap`, and introduces no causal claim. Version 1 remains preserved
as the provenance baseline.


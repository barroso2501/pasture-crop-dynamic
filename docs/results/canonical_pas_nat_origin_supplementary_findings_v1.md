# Supplementary PAS→NAT observed-spell origin summaries

**Date:** 2026-10-09. **Status:** produced and validated from the eight authenticated full-v3 cell CSVs. This satisfies the supplementary reporting/direction item in plan 008 v3; it does not expand RQ2 or add new integrated findings.

| Interval | PAS→NAT (ha) | Initial (%) | Observed entry (%) | Unresolved (ha) | Role |
|---|---:|---:|---:|---:|---|
| 1985–1990 | 2,045,589.848 | 100.00 | 0.00 | 0.000000 | primary |
| 1990–1995 | 2,516,271.675 | 46.02 | 53.98 | 4.414564 | primary |
| 1995–2000 | 2,729,629.912 | 28.33 | 71.67 | 6.337890 | primary |
| 2000–2005 | 2,903,185.953 | 19.28 | 80.72 | 4.928283 | primary |
| 2005–2010 | 3,053,048.077 | 13.42 | 86.58 | 9.074479 | primary |
| 2010–2015 | 3,571,444.760 | 10.62 | 89.38 | 9.062548 | primary |
| 2015–2020 | 3,566,997.870 | 8.33 | 91.67 | 7.381772 | primary |
| 2020–2025 | 2,084,952.836 | 9.50 | 90.50 | 10.718206 | diagnostic |

| Window | Interval-conversion sum (ha) | Initial (%) | Observed entry (%) | Unresolved (ha) |
|---|---:|---:|---:|---:|
| primary_1985_2020 | 20,386,168.095 | 27.582266 | 72.417532 | 41.199537 |
| full_observed_1985_2025 | 22,471,120.931 | 25.904213 | 74.095556 | 51.917743 |

Across the six successive primary-period comparisons, initial-origin shares decline for both PAS→NAT and PAS→TMP. In the diagnostic final interval, PAS→NAT initial share increases from 8.334529% to 9.496611%, while PAS→TMP decreases from 31.083175% to 20.115615%. Direction agreement is therefore 6/6 for primary comparisons and absent in the diagnostic comparison. This is a descriptive sign comparison, not a trend-significance test.

The first bar is 100% initial by construction for both destinations. All shares and pooled windows are conditional on 1985; re-entry is included. PAS→NAT is a classified endpoint change, not proof of ecological recovery, and may be sensitive to pasture/native-grassland confusion. Pooled areas count interval conversions and may count the same pixel repeatedly. The same native alignment, source maps and diagnostic-boundary limits are inherited.

Reproduction: `analysis/17y_summarize_pas_nat_origins_v1.py --closure-dir <eight-CSV-directory>`. Input hashes, row checks, TMP reference reproduction, partition residuals and output hashes are in `outputs/summary/decision024_review_v1/canonical_pas_nat_origin_summary_validation_v1.json`. This adds aggregation, not a new raster execution.

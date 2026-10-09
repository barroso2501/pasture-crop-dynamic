# Corrected RQ2 findings — Decision 024 closure

**Numerical review:** 2026-10-08. **Interpretation erratum:** 2026-10-09. **Evidence edition:** v4.1.

RQ2 concerns PAS→temporary-crop endpoint conversion. The origin category is the current observed pasture spell reconstructed from annual coverage at t0. PAS→NAT origin remains supplementary and is not promoted into the integrated matrix by this record.

## Corrected interval composition

| Interval | PAS→TMP (ha) | Initial spell (%) | Post-1985 entry (%) | Unresolved (ha) | Role |
| --- | ---: | ---: | ---: | ---: | --- |
| 1985–1990 | 1,450,003.979 | 100.00 | 0.00 | 0.000000 | primary |
| 1990–1995 | 1,638,736.606 | 70.39 | 29.61 | 1.217689 | primary |
| 1995–2000 | 1,809,550.135 | 57.20 | 42.80 | 5.220582 | primary |
| 2000–2005 | 3,504,280.627 | 48.76 | 51.24 | 11.580808 | primary |
| 2005–2010 | 2,825,891.974 | 41.20 | 58.80 | 13.114257 | primary |
| 2010–2015 | 4,974,529.591 | 34.35 | 65.64 | 21.825613 | primary |
| 2015–2020 | 3,916,475.186 | 31.08 | 68.92 | 9.609858 | primary |
| 2020–2025 | 2,086,326.750 | 20.12 | 79.88 | 9.046015 | diagnostic |

## Pooled interval conversions

| Window | Interval-conversion sum (ha) | Initial (%) | Post-1985 entry (%) | Unresolved (ha) | Unresolved (%) |
| --- | ---: | ---: | ---: | ---: | ---: |
| primary_1985_2020 | 20,119,468.099 | 46.91 | 53.09 | 62.568807 | 0.000311 |
| full_observed_1985_2025 | 22,205,794.849 | 44.39 | 55.61 | 71.614822 | 0.000323 |

## P9A035

Within the fixed 1985-defined window, the observed initial-spell share of PAS-to-temporary-crop endpoint conversions declines across the seven primary intervals; this is a window-conditioned composition, not evidence by itself of a changing land-use regime.

Initial/post-1985-entry shares: 1985-1990 100.00%/0.00% by construction; 2015-2020 31.08%/68.92%. The first observed share above 50% is 2000-2005 (51.24%); this date is window-specific and is not a process threshold.

1985 is the earliest observed state, not a process origin (Decision 022). The first interval is 100% initial by construction. Shares depend on window start, follow-up length and selection into the changing conversion denominator; finite-duration stationary renewal can also produce decline. Initial membership is non-increasing, but its conversion share need not be monotonic. Window-start sensitivity has not been executed. Origin is reconstructed from annual coverage at t0. A post-1985 observed entry includes re-entry; it is not first-ever establishment. The shift is descriptive, with no trend-significance or causal claim. Endpoint flow does not determine the annual path between t0 and t1.

## P9A036

For the fixed 1985-2020 window, pooled interval conversion area attributed to observed post-1985 entry spells is 53.09%, compared with 46.91% for uninterrupted left-censored 1985 spells; these proportions are conditional on the chosen baseline and interval weights.

Primary interval-conversion sum = 20.119468 million ha; initial 46.91% (9.438022 million ha), post-1985 entry 53.09% (10.681383 million ha), unresolved 62.568807 ha (0.000311%).

1985 is the earliest observed state, not a process origin (Decision 022). The first interval is 100% initial by construction. Shares depend on window start, follow-up length and selection into the changing conversion denominator; finite-duration stationary renewal can also produce decline. Initial membership is non-increasing, but its conversion share need not be monotonic. Window-start sensitivity has not been executed. Observed entry includes re-entry and does not identify first-ever establishment. Pooled values sum interval conversion areas and do not deduplicate pixels converted in different intervals. Initial origin is a continuous observed 1985 spell at t0, not membership in the fixed RQ1 cohort after interruptions. No causal attribution or inferential majority test is claimed.

## P9A037

The corrected three-way origin partition retains a small unresolved observed-spell component, with the 2020-2025 extension reported separately as diagnostic.

Unresolved interval-conversion sum: primary 62.568807 ha (0.000311%); full observed 71.614822 ha (0.000323%). Diagnostic 2020-2025 post-1985-entry share = 79.88%; full-observed initial/post-1985-entry shares = 44.39%/55.61%.

Unresolved means annual coverage gaps prevent current-spell origin attribution; it is not a numerical decoding of raw source age code 1. The retired source-age unattributed category is not part of the corrected three-state estimand. A small unresolved origin component does not measure total classification error. 2020-2025 is diagnostic with limited boundary support.

## Change from the retired source-age interpretation

The old primary source-age split was 51.73% censored and 48.27% new. The corrected primary observed-spell split is 46.91% initial and 53.09% observed post-1985 entry. In 2015–2020, the old 37.29%/62.71% split becomes 31.08%/68.92%. The old 176.720-ha full-series source-age unresolved component is replaced by 71.614822 ha of unresolved observed-spell origin. These categories have different definitions; the old source-age numerical statements are superseded, not reinstated.

The primary pooled denominator is a sum of interval conversion areas, not a unique converted area. Pixels converted in more than one interval may contribute repeatedly. Percentages use the complete PAS→TMP denominator and retain the unresolved component. Displayed two-decimal percentages may round without summing to exactly 100.00%.

The descriptive increase is not an estimated causal effect or an inferential trend test. No claim of uninterrupted first-ever establishment after 1985 is made. Source classification accuracy and limited 2024–2025 boundary support remain interpretation limits.

Current evidence authority: `outputs/summary/decision024_review_v1/canonical_integrated_evidence_matrix_v4_1.csv`; event index: `outputs/validation/decision024_review_v1/canonical_evidence_status_events_v3.csv`. The first origin bar is 100% initial by construction, not a process baseline. Window sensitivity is pending.

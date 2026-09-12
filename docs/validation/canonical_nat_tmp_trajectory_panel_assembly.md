# Canonical NAT-to-TMP trajectory panel assembly and validation

- **Status:** Passed
- **Validation date:** 2026-09-12
- **Method:** `docs/methods/within_interval_nat_tmp_trajectories.md`
- **Decision:** `docs/decisions/006_canonical_within_interval_trajectory_analysis.md`
- **Pilot script:**
  `gee/04a_reprocess_nat_tmp_trajectory_2005_2010_full_domain.js`
- **Production script:**
  `gee/04b_reprocess_nat_tmp_trajectory_remaining_intervals.js`
- **Assembly script:**
  `analysis/03_build_canonical_nat_tmp_trajectory_panel.py`

## Scope

This document records the production, assembly, and validation of the complete
canonical within-interval trajectory panel for the `NAT->TMP` endpoint flow.
The panel contains the same 24,889 canonical hexagonal cells in each of eight
five-year intervals from 1985 to 2025.

The analysis classifies annual pasture evidence in the four years between each
pair of endpoints. It complements the canonical stock-and-flow panel and does
not modify or reallocate its `flow_nat_tmp` values.

The primary inferential period ends in 2020. The 2020-2025 interval is retained
with the same schema and validation requirements but is explicitly marked as
diagnostic.

## Canonical inputs and outputs

| Role | Source or output |
|---|---|
| Annual land cover | MapBiomas Brazil Collection 11 `coverage_v3` |
| Spatial domain | `grade_hex_CeAmz_canonical_c11_v3` |
| Spatial and class constants | `config/constants.js` |
| External endpoint control | `canonical_stock_flow_panel_1985_2025_v1.parquet` |
| Trajectory output version | `canonical-nat-tmp-trajectory-v1` |
| Canonical trajectory panel | `canonical_nat_tmp_trajectory_panel_1985_2025_v1.parquet` |
| Source manifest | `canonical_nat_tmp_trajectory_panel_manifest_v1.csv` |
| Validation record | `canonical_nat_tmp_trajectory_panel_validation_v1.json` |
| Interval summary | `canonical_nat_tmp_trajectory_summary_v1.csv` |

The pasture-age product is not used in the trajectory analysis.

## Earth Engine execution record

All eight exports completed on the first attempt at default priority 100.

| Interval | Task ID | Start (UTC-03:00) | Runtime | EECU-seconds |
|---|---|---|---:|---:|
| 1985-1990 | `U4KMLGUTE6ZOGW4ZK4NFBLCE` | 2026-09-12 06:26:03 | 30 min | 520,963.3438 |
| 1990-1995 | `YWVDN75WBNOCE6JTBMZ73R4H` | 2026-09-12 06:17:59 | 8 min | 505,706.5000 |
| 1995-2000 | `DOBOMJKKRP2HHOBJ7NBLAAN5` | 2026-09-12 06:08:58 | 9 min | 538,691.1875 |
| 2000-2005 | `RTUO4WY4G72G4MENP2OC2CUV` | 2026-09-12 06:54:30 | 7 min | 512,876.6250 |
| 2005-2010 | `GM52H5ZMLAQ7HOQTQTFKFF6U` | 2026-09-11 21:57:19 | 7 min | 461,640.1875 |
| 2010-2015 | `MUMWSY6AGSBCMIIMCCSDGRSU` | 2026-09-12 06:43:22 | 10 min | 517,216.4375 |
| 2015-2020 | `RPSL3GJJWIJOFHLFPQO3ETKO` | 2026-09-12 06:57:29 | 8 min | 544,604.6250 |
| 2020-2025 | `DNDGSLA32HHJQJUPLWEERBOZ` | 2026-09-12 07:03:41 | 8 min | 516,639.0313 |
| **Total** | — | — | **87 task-minutes** | **4,118,337.9376** |

The total runtime is the sum of individual task runtimes, not elapsed wall
time, because some tasks overlapped. The longer 1985-1990 runtime did not
produce a structural, numerical, or reconciliation anomaly.

## Source manifest verification

The manifest contains exactly eight entries in chronological order. Every
source CSV has:

- 24,889 rows;
- 28 columns;
- one unique `cell_id` and one unique `GRID_ID` per row;
- the expected interval and diagnostic metadata; and
- a recorded SHA-256 checksum.

The eight manifest sizes and checksums were independently compared with the
source CSVs and matched exactly. The 2020-2025 file is the only source marked
with `diagnostic_interval = 1`.

## Panel assembly

The eight CSVs were concatenated and sorted by `cell_id`, `t0`, and `t1`.
Source rows and columns were preserved without deriving or overwriting fields.

| Check | Result |
|---|---:|
| Interval files | 8 |
| Rows per interval | 24,889 |
| Columns per interval | 28 |
| Panel rows | 199,112 |
| Panel columns | 28 |
| Distinct `cell_id` values | 24,889 |
| Intervals per cell | 8 |
| Duplicate cell-interval keys | 0 |
| Diagnostic rows | 24,889 |
| Missing values | 0 |
| Area values below `-1e-9` ha | 0 |

The canonical panel SHA-256 is:

```text
c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9
```

The stock-and-flow panel used as the external control retained its accepted
SHA-256:

```text
2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64
```

## Accounting and subset validation

All five exported identities were tested in every row. Across 199,112
cell-interval records:

| Check | Result |
|---|---:|
| Maximum absolute residual | `1.818989e-12` ha |
| Rows with a residual above `1e-9` ha | 0 |
| `consecutive2 > 2plus` violations | 0 |
| `2plus > any` violations | 0 |
| `any > all observed` violations | 0 |
| `all observed > endpoint` violations | 0 |

The observed values are floating-point precision and do not represent
measurable unallocated area.

## Reconciliation with canonical endpoint accounting

For each interval, `nat_tmp_endpoint_ha` was joined by `cell_id`, `t0`, and
`t1` to `flow_nat_tmp` in the validated canonical stock-and-flow panel.

| Interval | Matched rows | Maximum absolute difference (ha) | Rows above `2e-6` ha |
|---|---:|---:|---:|
| 1985-1990 | 24,889 | `2.235197e-8` | 0 |
| 1990-1995 | 24,889 | `9.094947e-13` | 0 |
| 1995-2000 | 24,889 | `1.490116e-8` | 0 |
| 2000-2005 | 24,889 | `1.490116e-8` | 0 |
| 2005-2010 | 24,889 | `1.818989e-12` | 0 |
| 2010-2015 | 24,889 | `1.818989e-12` | 0 |
| 2015-2020 | 24,889 | `1.490115e-8` | 0 |
| 2020-2025 | 24,889 | `7.450588e-9` | 0 |

There are no unmatched cell-interval records. The maximum difference is less
than 1.12% of the accepted tolerance and reflects numerical precision. The
trajectory panel therefore decomposes exactly the accepted `NAT->TMP` endpoint
population.

## Intermediate observation support

Incomplete support across the four intermediate annual observations totals
14.115718 ha in 40 cell-interval occurrences. This equals 0.0001436% of the
accumulated endpoint flow.

| Interval | Incomplete area (ha) | Positive cell records |
|---|---:|---:|
| 1985-1990 | 3.478066 | 8 |
| 1990-1995 | 1.045425 | 5 |
| 1995-2000 | 2.882011 | 11 |
| 2000-2005 | 3.485785 | 6 |
| 2005-2010 | 2.093614 | 4 |
| 2010-2015 | 0.086109 | 1 |
| 2015-2020 | 0.783428 | 3 |
| 2020-2025 | 0.261280 | 2 |

This area remains explicitly separated and is not assigned to the no-pasture
class. It is immaterial to aggregate results but must remain available in
cell-level analyses.

## Canonical interval results

| Interval | `NAT->TMP` (Mha) | Any pasture | Two or more years | Two consecutive years |
|---|---:|---:|---:|---:|
| 1985-1990 | 1.402 | 10.3554% | 9.9657% | 9.9632% |
| 1990-1995 | 1.181 | 8.7521% | 8.3201% | 8.3180% |
| 1995-2000 | 1.225 | 6.4570% | 6.1503% | 6.1489% |
| 2000-2005 | 2.295 | 6.8869% | 6.5459% | 6.5445% |
| 2005-2010 | 0.945 | 8.5029% | 8.1036% | 8.1016% |
| 2010-2015 | 1.362 | 9.8415% | 9.3327% | 9.3305% |
| 2015-2020 | 0.741 | 11.0216% | 10.2852% | 10.2817% |
| 2020-2025 diagnostic | 0.682 | 7.4066% | 6.9349% | 6.9325% |

For the primary 1985-2020 inferential period:

| Component | Area (ha) | Share of `NAT->TMP` |
|---|---:|---:|
| `NAT->TMP` endpoint | 9,150,804.298 | 100% |
| Any intermediate pasture | 781,748.183 | 8.5429% |
| At least two pasture years | 743,439.236 | 8.1243% |
| At least two consecutive pasture years | 743,258.986 | 8.1223% |

For the complete 1985-2025 panel, including the diagnostic interval:

| Component | Area (ha) | Share of `NAT->TMP` |
|---|---:|---:|
| `NAT->TMP` endpoint | 9,832,668.124 | 100% |
| Any intermediate pasture | 832,251.332 | 8.4641% |
| At least two pasture years | 790,725.679 | 8.0418% |
| At least two consecutive pasture years | 790,529.151 | 8.0398% |

Across the complete panel, the consecutive-two-year area is 94.987% of the
inclusive pasture area. Only 196.528 ha have at least two pasture observations
without containing a consecutive pasture pair. The difference between the
inclusive and persistence-sensitive estimates is therefore driven almost
entirely by one-year pasture observations.

## Historical provenance diagnostic

The historical `pentefino` outputs produce a larger inclusive pasture share in
every interval.

| Interval | Historical inclusive share | Canonical inclusive share |
|---|---:|---:|
| 1985-1990 | 16.9974% | 10.3554% |
| 1990-1995 | 14.8965% | 8.7521% |
| 1995-2000 | 10.6036% | 6.4570% |
| 2000-2005 | 13.3048% | 6.8869% |
| 2005-2010 | 13.6974% | 8.5029% |
| 2010-2015 | 15.8850% | 9.8415% |
| 2015-2020 | 17.1394% | 11.0216% |
| 2020-2025 | 12.4730% | 7.4066% |

The difference also persists when comparisons are restricted to shared cell
identifiers. Domain reconstruction alone therefore cannot explain it. The
evidence is consistent with a systematic effect of changing from the
preliminary `classification-ft` source to final `coverage_v3`, particularly in
intermediate annual pasture classifications. This remains an inference rather
than a causal decomposition of every processing difference.

Historical outputs remain provenance only. They must not be joined to the
canonical panel or used as manuscript results.

## Acceptance and analytical boundary

The complete trajectory series passes source-integrity, structural,
accounting, subset, observation-support, and stock-flow reconciliation checks.
It is accepted as the canonical annual decomposition of the five-year
`NAT->TMP` endpoint flow.

The validation establishes computational and accounting integrity. It does
not independently establish thematic classification accuracy or demonstrate
that absence of observed pasture represents direct conversion. It also does
not select the primary manuscript rule.

The next analytical step is a one-to-one join with the canonical stock-and-flow
analytical table using `cell_id`, `t0`, and `t1`. The join must retain all
199,112 records and preserve the distinction between endpoint accounting,
annual trajectory evidence, and net cell-level balance. Moran, MAUP, and other
spatial analyses remain downstream of that integration and its validation.

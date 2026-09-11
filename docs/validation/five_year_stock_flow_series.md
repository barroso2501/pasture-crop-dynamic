# Five-year stock-and-flow series validation

- **Status:** Passed
- **Validation date:** 2026-09-11
- **Method:** `docs/methods/five_year_stock_flow_panel.md`
- **Processing decision:** `docs/decisions/005_full_domain_stock_flow_processing.md`
- **Production scripts:**
  `gee/03b_reprocess_stock_flow_2005_2010_full_domain.js` and
  `gee/03c_reprocess_stock_flow_remaining_intervals.js`

## Scope

This validation covers the eight complete-domain stock-and-flow exports from
1985 to 2025. Every export contains the same 24,889 canonical cells, including
cells with zero focal flows. The resulting balanced panel has 199,112
cell-interval observations.

The primary inferential series ends in 2020. The 2020-2025 export uses the same
calculation and schema but is marked with `diagnostic_interval = 1`.

## Execution record

All eight exports completed on the first attempt.

| Interval | Task ID | Start (UTC-03:00) | Runtime | EECU-seconds |
|---|---|---|---:|---:|
| 1985-1990 | `T2W7M6O4KV5KEW5LWAG45T6P` | 2026-09-11 17:21:32 | 12 min | 786,358.0000 |
| 1990-1995 | `PMGIGSDY3SFIJIQFBEFOYNKL` | 2026-09-11 17:33:41 | 22 min | 847,660.7500 |
| 1995-2000 | `V4M7R375A3K3YFFP5O4RTC5B` | 2026-09-11 17:55:18 | 15 min | 739,796.1875 |
| 2000-2005 | `WL3BLHIJKKUFZNGRX6FA22VL` | 2026-09-11 18:43:19 | 18 min | 877,668.5000 |
| 2005-2010 | `TAPIRJQQUDSDX6GO7TXILEAU` | 2026-09-11 16:21:36 | 17 min | 1,026,345.3750 |
| 2010-2015 | `BWNLLBDTYFJFX35FOYBEBDQ2` | 2026-09-11 18:10:40 | 16 min | 804,498.8125 |
| 2015-2020 | `ZR3BCI7BDT5ZLL5Y673VIOZK` | 2026-09-11 18:27:09 | 16 min | 745,799.2500 |
| 2020-2025 | `64A26PRVWCJTPR7FBTFOIYV3` | 2026-09-11 19:01:27 | 14 min | 874,566.5000 |
| **Total** | — | — | **130 task-minutes** | **6,702,693.3750** |

Mean runtime was 16.25 minutes per interval. All tasks used the default
priority of 100.

## Structural validation

| Check | Result |
|---|---:|
| Expected interval files | 8 of 8 |
| Rows per interval | 24,889 |
| Columns per interval | 90 |
| Total panel rows | 199,112 |
| Distinct `cell_id` values per interval | 24,889 |
| Duplicate `cell_id` or `GRID_ID` values | 0 |
| Differences in cell membership among intervals | 0 |
| Rows with missing values | 0 |
| Area values below `-1e-9` ha | 0 |
| Flow-bound violations above `1e-6` ha | 0 |
| Class-27 area | 0 ha |
| Unexpected coverage area | 0 ha |

All exports use `output_version = canonical-stock-flow-v1`. Only 2020-2025
has `diagnostic_interval = 1`.

The copy of `canonical_stock_flow_2005_2010_full_v1.csv` delivered with the
complete series is byte-identical to the file independently validated during
the full-domain production test.

## Accounting closure

The nine endpoint stocks reconcile with rasterized cell area. All focal origin
and destination identities close, and the pasture-to-temporary-agriculture
origin partition is exhaustive.

Across all files:

- the maximum absolute exported accounting residual is
  `3.274181e-11` ha;
- no row has an absolute residual greater than `1e-9` ha; and
- no directed flow exceeds its relevant origin or destination stock by more
  than `1e-6` ha.

These values represent floating-point precision, not measurable unallocated
area.

## Longitudinal continuity

For every cell and state, the ending stock of one interval was compared with
the opening stock of the next interval.

| Shared year | Maximum absolute difference (ha) |
|---:|---:|
| 1990 | `3.725308e-7` |
| 1995 | `2.682209e-7` |
| 2000 | `3.352761e-7` |
| 2005 | `4.246831e-7` |
| 2010 | `4.172325e-7` |
| 2015 | `4.321337e-7` |
| 2020 | `4.246831e-7` |

No comparison exceeded the accepted `2e-6`-ha numerical tolerance. The panel
is therefore continuous across all seven shared endpoints.

## Pasture-to-temporary-agriculture partition

The table below is retained as a processing diagnostic. It does not substitute
for the subsequent scientific analysis.

| Interval | `PAS->TMP` (Mha) | Censored | New | Unresolved age |
|---|---:|---:|---:|---:|
| 1985-1990 | 1.450 | 100.0000% | 0.0000% | 0.000000% |
| 1990-1995 | 1.639 | 71.0121% | 28.9877% | 0.000159% |
| 1995-2000 | 1.810 | 61.0480% | 38.9514% | 0.000606% |
| 2000-2005 | 3.504 | 53.8123% | 46.1867% | 0.000974% |
| 2005-2010 | 2.826 | 47.8489% | 52.1499% | 0.001185% |
| 2010-2015 | 4.975 | 40.0245% | 59.9747% | 0.000806% |
| 2015-2020 | 3.916 | 37.2898% | 62.7094% | 0.000758% |
| 2020-2025 | 2.086 | 30.2466% | 69.7521% | 0.001232% |

Unattributed pasture age is zero in every interval. The explicitly unresolved
age component totals 176.720 ha across the eight exports and remains governed
by `docs/decisions/003_unresolved_pasture_age_code.md`.

The 1985-1990 result contains no new-pasture component because all pasture
present at the beginning of the observed series belongs to the left-censored
initial stock by definition.

## Spatial support

The minimum rasterized-area-to-geometry ratio is 99.546% in every interval.
Valid land-cover support is lower in complete hexagons that cross the edge of
the MapBiomas raster support. Each endpoint generally has 511 cells below 99%
valid support; the 1995-2000 and 2000-2005 pair contains one endpoint with 512.

These boundary cells remain valid members of the fixed domain. Downstream
analysis must preserve the geometry, rasterized-area, valid-area, and masked-
area fields. A small valid fraction must not be interpreted as an intact cell,
a zero-flow cell, or evidence of pixel-level stability.

## Interpretation boundary

This output is a cell-level accounting panel for endpoint stocks and directed
five-year flows. It does not describe annual pixel trajectories or temporal
alternation within an interval. Net balance, gross directed flows, annual
trajectory, and pixel alternation remain distinct quantities.

## Acceptance

The complete 1985-2025 stock-and-flow series passes the structural,
accounting, regression, spatial-support, and longitudinal-continuity checks.
It is accepted as the canonical five-year accounting panel. The primary
inferential analyses will use intervals ending no later than 2020; 2020-2025
will remain a diagnostic extension.


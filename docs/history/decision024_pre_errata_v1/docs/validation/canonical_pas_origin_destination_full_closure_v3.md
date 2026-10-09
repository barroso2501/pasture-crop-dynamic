# Full-domain PAS origin × endpoint destination closure (1985–2025)

**Status:** validated accounting checkpoint for Decision 024 criteria 7 and 8; Decision 024 remains open.  
**Reviewed:** 2026-09-30.  
**Related records:** Decision 024; plan 008 v3; `canonical_pas_tmp_origin_series_reassessment_v1.md`.

## Analytical object and provenance

For each canonical cell and five-year interval, the CSV partitions pasture at the interval start (`stock0_pas`) by the reconstructed origin of its *current observed pasture spell*: uninterrupted 1985 spell (`initial`), observed post-1985 entry (`new`), or uncertain origin (`unresolved`). It then cross-tabulates each origin with the endpoint classes PAS, TMP, NAT, OAG, OUT, WATER, NODATA, unexpected, and masked. Origin is fixed at `t0`; these endpoint columns do not represent all intervening annual pathways. `initial` does not mean that pasture was first established in 1985.

The eight `canonical_pas_origin_destination_YYYY_YYYY_full_v3.csv` files and eight matching `validation_v3.json` files were supplied in `drive-download-20260930T200647Z-1-001.zip` (SHA-256 `84c0a9521840923b9d95b52ce69152d8f3ff6599920cd0b13cc3de24ee31e37a`). The ZIP also contains a superseded `2015_2020_full_v2.csv` and its JSON, which are retained as history and excluded from this review. The `v3` JSONs record SHA-256 hashes of their own final CSVs, the authenticated baseline and accepted RQ2 validation, and the eight contributing closure and RQ2 batches. The raw GEE batch CSVs are external and were not provided in this review ZIP; their hashes were therefore not independently recomputed here.

The validator `17m_validate_pas_origin_destination_full_v3.py` checks every cell against the authenticated canonical stock-flow baseline, including each PAS endpoint destination, and matches each PAS→TMP origin component to the accepted RQ2 batch. The wrapper `17n_run_all_pas_origin_destination_closure_v1.py` ran all eight intervals. This independent review also read the supplied final CSV bytes and JSON records without relying only on their `PASS` fields.

## Independent checks and results

| Check | Result |
|---|---|
| CSV integrity | All eight `full_v3.csv` SHA-256 values match their `validation_v3.json` records. |
| Population | Exactly 24,889 unique `cell_id` values in each interval; the cell sets are identical across intervals. Eight source batches per interval reconcile with the JSON inventory. |
| Keys and scope | `t0`, `t1`, batch, and `diagnostic_interval` are consistent; 2020–2025 alone has diagnostic flag `1`. |
| Numeric domain | All area fields finite and nonnegative. |
| Origin and destination | `stock0_pas = initial + new + unresolved`; every destination equals its three origin components; each origin equals the sum of its nine destinations. |
| Stock closure | `stock0_pas = PAS→PAS + observed outflow + observation loss`, where observed outflow is TMP + NAT + OAG + OUT + WATER, and observation loss is NODATA + unexpected + masked. |
| Per-cell numerical residual | Maximum absolute recalculated identity residual was below `1.5e-11 ha`, compared with the validator's acceptance tolerance of `0.01 ha/cell`. |
| Recorded totals | Recomputed CSV totals agree with their JSON totals to below `0.000002 ha`, allowing for ordinary floating-point accumulation order. |

The JSONs report the following totals (ha; rounded here to two decimals):

| Interval | PAS at t0 | PAS→PAS | Observed outflow | Observation loss | PAS→TMP within outflow |
|---|---:|---:|---:|---:|---:|
| 1985–1990 | 49,035,870.57 | 44,419,613.45 | 4,616,223.45 | 33.66 | 1,450,003.98 |
| 1990–1995 | 65,765,175.48 | 59,996,834.82 | 5,768,321.93 | 18.73 | 1,638,736.61 |
| 1995–2000 | 79,576,949.48 | 73,202,693.03 | 6,374,213.12 | 43.34 | 1,809,550.13 |
| 2000–2005 | 92,013,450.83 | 83,396,579.87 | 8,616,832.87 | 38.09 | 3,504,280.63 |
| 2005–2010 | 103,006,331.16 | 94,155,152.99 | 8,851,107.57 | 70.59 | 2,825,891.97 |
| 2010–2015 | 106,760,181.06 | 94,638,005.38 | 12,122,093.85 | 81.83 | 4,974,529.59 |
| 2015–2020 | 106,174,810.21 | 95,281,668.61 | 10,893,106.83 | 34.78 | 3,916,475.19 |
| 2020–2025¹ | 106,649,767.91 | 96,197,438.68 | 10,452,296.49 | 32.74 | 2,086,326.75 |

¹ Included in the complete observed series and flagged as the diagnostic interval. These are interval flows and stocks, so summing the `PAS at t0` column across intervals is not a unique pasture area.

The previously resolved **1985–1990** baseline is included in the full-domain `17m v3` validation: its record reports 24,889 cells, authenticates the accepted baseline by SHA-256 and checks the source PAS stock and endpoint flows cell by cell. This review independently checked the final `full_v3` CSV and its hash; the original source files would be needed to rerun the validator from scratch.

## Scope of acceptance and remaining gates

The evidence supports **Decision 024 criterion 7** for the eight five-year PAS origin × endpoint destination partitions and **criterion 8** for full canonical cell coverage. It also supports use of the eight `full_v3` tables as versioned cell-level accounting checkpoints. The files preserve `cell_id` for spatial joins. This is not a validation of every annual pathway, the fixed 1985 pixel cohort, or the entire downstream system.

The following gates remain open:

- **Criterion 9:** run and record the complete downstream invariance comparison for non-origin fields; the selected PAS flow checks here are not that full gate.
- **Criterion 10:** export and reconcile event type, event year, and boundary-adjacent flags for 2024–2025 on the full domain. The endpoint closure files do not contain these annual event fields.
- **Criterion 11:** finish the source code `1`/reused-`100` impact and overlap audit with explicit denominators.
- **Criterion 12:** complete the remaining evidence, manifest and status-event revisions. In particular, do not rescind suspension of P9A035–P9A037 on the basis of this accounting checkpoint alone.
- Revalidate the fixed 1985 pasture cohort (RQ1) and its source hashes as a separate object. No such revalidation is asserted here.

The eight JSONs explicitly set `decision_024_fully_implemented: false`. Earlier accepted records remain immutable. This checkpoint adds no revised finding or evidence-status event.

## GitHub placement

Commit this document under `docs/validation/`. Commit the eight small JSON records under `outputs/validation/pasture_age_remediation_v1/` and the compact interval summary under `outputs/summary/pasture_age_remediation_v1/`. Keep the eight complete cell CSVs in the versioned external product directory `spatial/phase9/pasture_spell_closure_full_v1/`; do not add the large tables or the source download ZIP to GitHub. Commit the final `17m` validator and `17n` wrapper under `analysis/` and the GEE exporter under `gee/` if those versions are not already present. Do not replace a newer README based on an older local copy; add a short status link to this validation document when editing the current repository README.

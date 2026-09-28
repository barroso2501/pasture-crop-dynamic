# PAS→temporary-crop origin remediation: validated 2015–2020 checkpoint

**Status:** accepted as an interval-specific diagnostic checkpoint; the
1985–2020 and 1985–2025 RQ2 conclusions remain pending.

**Date of review:** 2026-09-28. **Authority for reconstructed origin:** annual
MapBiomas Collection 11 coverage sequence, interpreted as an observed
consecutive pasture episode. The public pasture-age asset is used only to
reproduce and compare the previous origin assignment. An observed departure
from PAS followed by a return begins a new pasture episode. Missing or
uncertain coverage does not establish a new observed entry.

## Evidence and population

Eight CSV exports, `canonical_pas_tmp_origin_2015_2020_b00_v3.csv` through
`..._b07_v3.csv`, cover all **24,889** distinct canonical cells. The source
archive supplied for independent review has SHA-256
`96b1312c84db34fb64b6caa086575dca001e4526db0ab99cf7e67d65e0b2e13e`.
Per-export SHA-256 hashes, byte counts and cell counts are in the validation
JSON committed with this checkpoint. The uncompressed export CSVs are kept as
external computation outputs and are not copied into this repository package.

The review reran `analysis/17f_validate_pas_tmp_origin_full_2015_2020_v1.py`
against the accepted `canonical_stock_flow_2015_2020_full_v1.csv` and all
eight CSV exports. Validation status: **PASS**. Cell IDs match the accepted
population exactly, with no missing or duplicate cells; each batch agrees
with its original `source_batch_id`. Within the specified 0.01 ha per-cell
tolerance, PAS→temporary-crop flow, NAT→PAS flow, and PAS stock at 2015 are
invariant relative to the baseline. The old and reconstructed partitions,
and each row and column of the old-to-new origin matrix, close by cell. The
full-domain old categories and the two tested total flows match the accepted
CSV. The comparison is restricted to these fields; it is not a full
revalidation of every stock-flow variable or a new test of other endpoints.

## Result for 2015–2020

| Origin of PAS→temporary-crop conversion | Previous assignment | Reconstructed episode |
|---|---:|---:|
| Continuous since 1985 / previously censored | 37.28982% | 31.08318% |
| Observed entry after 1985 | 62.70942% | 68.91658% |
| Unresolved | 0.00076% | 0.00025% |

The PAS→temporary-crop denominator is **3,916,475.186 ha**. The previous
`censored` group loses **6.20664 percentage points** relative to the
reconstructed continuous-1985 group. Its directly observed transfer to the
post-1985 entry group is **243,081.186 ha** across **8,156** cells. Other,
much smaller cross-category transfers appear in the machine-readable matrix;
therefore the direct area transfer must not be assumed equal to every change
in category totals. See the committed JSON for the complete matrix.

The reproduced NAT→PAS total is **9,016,705.140 ha**. Its age-specific
origin is not evaluated in this checkpoint. In particular, this checkpoint
does not complete the supplementary PAS→NAT assessment or full
PAS-outflow/observation-loss closure in remediation plan 008.

## Scope and evidence status

This is the corrected **single-interval** RQ2 origin comparison. It does not
replace the primary pooled 1985–2020 result or the observed 1985–2025 series.
Findings **P9A035, P9A036 and P9A037 remain suspended** under the existing
evidence-status event record; this checkpoint is not a rescission event.
2020–2025 remains part of the future full series and must be flagged as a
diagnostic interval. Original v1 exports and evidence records remain preserved
as provenance. The next action is reconstruction for the seven remaining
intervals followed by full-series validation and evidence review.

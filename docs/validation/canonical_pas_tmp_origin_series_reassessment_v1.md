# RQ2 pasture-episode origin reassessment, 1985–2025

**Status:** interval and pooled RQ2 PAS→temporary-crop origin comparisons
validated. **Date reviewed:** 2026-09-29. This validation addresses the
origin partition of the observed PAS→temporary-crop endpoint flow. It does
not close the remaining destination and downstream invariance gates of
remediation plan 008.

## Inputs and provenance

The accepted 2015–2020 interval was recorded in
`docs/validation/canonical_pas_tmp_origin_2015_2020_checkpoint_v1.md`.
Seven more intervals were exported as eight canonical `source_batch_id` lots
each. The 56 cell-level CSV exports supplied for review are archived outside
GitHub. The separate 18-file validation-and-summary ZIP supplied for review
has SHA-256
`b51867bca9b67df4dd079bb942b453876fc14944d1830002057ff4b78a78d41e`
and contains the nine validation JSONs and nine summaries. Individual export
hashes and byte counts are in each committed interval JSON. The full export
archive is distinct from this validation ZIP. The 2015–2020 lots and their
hashes remain in its checkpoint.

The GEE calculation compares the public pasture-age category at t0 with a
project-derived origin for the **current observed pasture episode**, built
chronologically from the Collection 11 annual coverage class 15. A confirmed
non-pasture year terminates an episode; later PAS begins a post-1985 observed
entry. Missing, masked and unexpected observations make a subsequent PAS
origin unresolved until a later confirmed non-PAS establishes a new entry.
This reconstruction is not described as a corrected official MapBiomas asset.

## Checks performed

All eight interval JSONs report `PASS`, with 24,889 unique canonical cells
and eight complete batches per interval. Validation against the corresponding
accepted v1 stock-flow CSV checks, per cell, the invariant PAS→TMP total,
NAT→PAS total, PAS stock at t0, reproduction of the old PAS→TMP origin
components, closure of the new components, and row/column closure of the
4×3 old-to-new transfer matrix. The stated per-cell tolerance is 0.01 ha.
The pooled validator independently reconciles the old areas to the accepted
primary and full-observed v1 summaries. The 2020–2025 interval is included
with `diagnostic_interval=1`.

The machine-readable record is
`outputs/validation/pasture_age_remediation_v1/canonical_pas_tmp_origin_series_reassessment_validation_v1.json`.
The eight interval JSONs, eight interval CSV summaries and two-row pooled
CSV accompany it in this package. Their fields and population counts should
be consulted for exact values and per-interval changes.

This set of checks establishes the RQ2 origin comparison. It is not a
comprehensive invariance audit of all stock-flow variables, the PAS→NAT
supplementary origin analysis, or the full PAS outflow and observation-loss
destination closure specified in plan 008.

## Decision 024: acceptance gates still open

The PASS above is specific to PAS→temporary-crop origin attribution. It is
**not** a PASS for full implementation of Decision 024. In particular:

| Decision 024 criterion | Current evidence | Remaining work |
|---|---|---|
| 7 — origin, destination, observation-loss and initial-stock identities | PAS→TMP origin closes per cell; PAS stock, PAS→TMP and NAT→PAS totals reproduce v1 | Export and close PAS→NAT, PAS→other observed destinations and PAS→observation-loss separately; complete initial-stock and endpoint identities |
| 9 — downstream invariance | Three selected non-origin measures reproduce their v1 values | Compare all dependent non-origin fields and determine whether Phases 2–8 require any rerun |
| 10 — 2024–2025 episode boundaries | Synthetic and small-tile checks exercise event type/year | Export and validate event type, year and `boundary_adjacent` on the full canonical domain; the v3/v4 PAS→TMP lot CSVs and interval JSONs do not contain these fields |
| 11 — source-code anomalies and overlap | Code-`1` pixels have a separate pixel-history diagnosis; the known reused-`100` example is independently sampled | Quantify the complete reused-`100` population and its intersection with the code-`1` population under explicit pixel and temporal denominators; publish the source-impact audit |
| 12 — records and corrected evidence | PAS→TMP interval JSONs, hashes and pooled summary exist | Complete the remaining validation records and formally revise evidence statements, figures and status events |

The population of **24,692** pixels with code `1` in the existing diagnostic
is restricted to the study domain. Across their exported 41-year histories,
none has a source age `100`; this is a *conditional observation for that
population*, not yet a complete overlap audit of both anomaly populations.
The separate national full-asset count task timed out and supplied no
national denominator. These limits must remain explicit.

Criterion 10 can be met with a separately versioned, full-domain annual-event
product using the same chronological state logic. No PAS→TMP origin CSV needs
replacement solely to add event flags, provided that product reconciles with
the accepted origin states and does not change their classification. The
reconciliation and boundary-event results must be recorded before declaring
the criterion satisfied.

## Evidence status

The new RQ2 numbers are validated for their stated object and windows.
Accepted v1 outputs remain immutable provenance. Existing suspension events
for P9A035–P9A037 remain in force until the dependent evidence matrix,
figures and manuscript claims have been revised and a separate versioned
status event records the review. Decision 024 must not be described as fully
implemented while the gates above remain open. This document does not rescind
the suspension events.

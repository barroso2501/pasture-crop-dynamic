# First observed entry and observed re-entry: auxiliary decomposition v1

Date: 2026-10-21. Status: implementation and local software checks complete; native pilot pending. Governing semantics: Section 2 of Plan 009. Matrix v4.3 and events-v5 remain unchanged.

## Analytical object

This is an auxiliary label attached to the current **confirmed post-1985 pasture spell**. It subdivides the accepted observed-entry origin. It does not replace or reinterpret the accepted three origin classes and does not use public pasture-age codes.

At an observed non-PAS→PAS transition, inspect only years strictly before that entry, starting in 1985:

| Auxiliary code | Label | Entry-time evidence |
|---|---|---|
| 0 | none | Not a currently confirmed post-1985-entry spell: non-PAS, initial, unresolved or uncertain observation |
| 1 | first observed entry | No earlier observed PAS and every earlier annual coverage observation valid |
| 2 | observed re-entry | PAS observed before this entry, whether or not other earlier years have gaps |
| 3 | prior-history uncertain | No earlier observed PAS, but at least one earlier masked, NODATA or unexpected observation |

These labels are frozen at entry and carried unchanged through the consecutive confirmed PAS spell. Updating `everPAS` after classifying the entry is essential: the first entry's own PAS observation must not make it a re-entry on the following year. A later confirmed entry can be a re-entry even if the earlier PAS spell had unresolved origin: the prior PAS observation itself is evidence of earlier PAS.

First observed entry is window-specific. Pre-1985 establishment remains unknown. Neither no earlier observed PAS nor the absence of PAS observations under a mask means first-ever pasture establishment.

## Gaps and resets

The exact accepted categorical engine is embedded as a separate control. Coverage 15 is PAS; valid expected codes other than 15/27 are observed non-PAS. Code 27, masks and unexpected codes are uncertain. Coverage code 1 is valid observed non-PAS; it has no relation to the old pasture-age code 1.

Any gap breaks confirmed continuity. A PAS observation immediately after a gap is unresolved, not a newly confirmed entry. A later observed non-PAS resets the **current origin**; a subsequent PAS becomes confirmed observed entry. The cumulative earlier-history flags are retained: that reset cannot erase an earlier gap or a prior PAS observation for auxiliary classification. No gap bridging is used.

## Auxiliary age and chronology

The numerical code is project-derived consecutive observed age: 100 for a continuous initial episode, 201 at every confirmed entry, previous age + 1 on continuation, and 0 outside initial/confirmed-entry spells. Re-entry restarts at 201. The longest post-1985 run in 1985–2025 reaches 240. Unresolved PAS and uncertain observations have auxiliary numerical code zero; their categorical states remain distinct.

`entryYear` is frozen through the confirmed spell and cleared outside it. An entry year of 2024 or 2025 retains its boundary-adjacent meaning. In the real-history audit, entry and termination areas are separately retained for each of those years. The 2020–2025 interval remains diagnostic. No event-raster asset comparison is performed.

`observed_confirmed_entry_count` is a monotone lower bound formed by detected observed non-PAS→PAS transitions. Baseline PAS is not counted as an entry; unobserved transitions are not inferred. The exported history counts aggregate these observed events over pixels and years, not a unique spatial area or a complete historical spell count.

## Stock and PAS→TMP flow

Origin and auxiliary kind are evaluated at t0. The endpoint flow is PAS(t0)→TMP(t1). Annual changes between t0 and t1 do not replace t0 attribution.

Both the PAS stock and its PAS→TMP endpoint-flow component satisfy:

```text
accepted observed post-1985 entry
  = first observed entry
  + observed re-entry
  + prior-history uncertain
```

The original identity remains total = initial + observed entry + unresolved. Every flow category must be no larger than its corresponding t0 stock. The stock must not exceed its cell area support. Any fractions in the pilot summary divide summed areas, not averaged cell fractions. Zero denominators produce blank fractions.

## References and invariance

The pilot uses 2015–2020 and 2020–2025 in cells GH-123/18081/b1 and IK-77/32173/b5. Four original native sensitivity files are shipped under `config/reference_native/`, unchanged. Their hashes are authenticated against the unchanged accepted full sensitivity JSON under `config/reference_validation/`. The local validator re-extracts their baseline-1985 rows, reproduces the supplied four-row subset and checks the eight historical control fields per cell/interval. These native sensitivity rows were previously reconciled with the accepted origin-destination reference chain; this does not constitute a fresh independent export of the entire accounting system.

Revision r2 replaces 42 synchronous metadata queries with a single asynchronous `Image.evaluate` request. The returned band metadata supply all 41 CRS/affine transforms. The actual and synthetic annual recurrences now use server-side `List.iterate`, packing the prior state and accumulators into image bands. The step function and expected histories are unchanged. Snapshot years, boundary events, counters, support and tolerances are retained. The two t0 categorical controls still use the exact historical function.

The old `reconstruct` control function is included byte-for-byte from the accepted sensitivity pilot snapshot. The auxiliary recurrence is separately compared to that control at both t0 values with a zero native state-mismatch counter and area controls. No canonical output, cohort membership or origin partition is overwritten.

## Verification and scope

Local checks execute the extracted production function using a scalar image adapter and compare it to a separate whole-history oracle based on backwards contiguous-run and strict-prefix scans. They exercise 31 explicitly specified cases (302 year steps), 46,656 complete six-year histories and their 55,986 shared prefix steps. These are software checks, not native GEE reducers, footprint or projection execution.

Native synthetic images exercise the same production recurrence, comparing expected state, age, auxiliary kind, count, entry year and boundary flag at every step. Six expected-value error fields and ten invariant error fields must all be zero in all 31 cases. The cases include maximum age 240, initial continuity, repeated re-entry, gaps, reset after gaps, masked stored PAS, valid code 1 and entry/termination in 2024/2025. All synthetic cases share one small native reduction; each must have positive reduction-weighted support.

For each real pilot cell, ten invariant counters accumulate over all 41 annual steps. The audit also exports support, confirmed entry counts by kind, and 2024/2025 event areas. Positive entry-kind stock must have corresponding positive history-event support. Counters sum pixel-year equivalents and may be fractional. The audit rows are per cell, not repeated once for each interval.

A native pilot PASS would accept only these two cells and fixtures. Domain-wide percentages, absence of rare anomalies and full-domain numerical-age assurance remain unavailable. An operator-provided CSV is not an independently witnessed remote execution: supplied-text hashes are pinned, while executed-text hash and operator attestation remain null unless explicitly supplied later.

## API references

- [Image.evaluate](https://developers.google.com/earth-engine/apidocs/ee-image-evaluate): asynchronous metadata callback.
- [List.iterate](https://developers.google.com/earth-engine/apidocs/ee-list-iterate): state carried across annual server-side steps.
- [Image.unmask](https://developers.google.com/earth-engine/apidocs/ee-image-unmask): explicit retained footprint and masked-value handling.
- [Image.reduceRegions](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregions): fixed CRS/transform and per-region reduction limits.

These references document API behavior; the native result remains pending until the operator returns the four exports.

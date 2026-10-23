# Full-domain entry/re-entry execution v1

2026-10-21. Local implementation prepared; native full-domain execution pending. The accepted r2 pilot remains unchanged under `provenance/entry_reentry_pilot_r2/`.

## Unchanged scientific definitions

The production `advanceEntry` function is copied byte-for-byte from the accepted pilot. It classifies the current confirmed post-1985 entry spell as first observed entry with complete earlier observations, observed re-entry with prior PAS evidence, or prior-history uncertain. The label and entry year are frozen for that spell. Gaps break continuity and are never bridged. Earlier observed PAS remains evidence of re-entry even when its earlier spell origin was unresolved. The numerical age starts/restarts at 201, increases on confirmed continuation, remains 100 for the initial continuous spell, and is zero outside those two attributable spell states.

The original three-way origin estimator, coverage codes, CRS, transform, pixel-area calculation, analytical grid and interval attribution at t0 remain unchanged. No public pasture-age image is read. RQ1 cohort membership and the original accounting are not redefined.

## Export design

There are 64 endpoint tables (eight intervals × eight canonical source batches), eight 1985–2025 history-audit tables and one manifest. Per-interval reductions have 21 area bands and one native state-mismatch counter; they are kept separate from the full-history audit reductions. The expected 199,112 endpoint rows and 24,889 audit rows are controlled by a hash-pinned canonical crosswalk.

Metadata are requested asynchronously in one `Image.evaluate` call, as in the successful r2. Task preparation yields to the Code Editor between exports using `ui.util.setTimeout`. It does not wait for or launch server tasks automatically. The operator launches the created tasks in Tasks. No raster preview or domain-wide Console aggregation is added.

## Server-side recurrences

For each t0, the endpoint walker iterates from 1986 to t0 over a packed image containing the exact accepted eight state variables plus a separate categorical control. At t0=1985, it uses the initial seed directly and does not create a backwards or nonempty subsequent-year sequence. The separate categorical step uses the accepted categorical formula and its own previous state, with no auxiliary-history inputs. Local exhaustive tests compare this adapted control to the exact retained historical control function and the independent chronological oracle. Native output must have zero categorical mismatches and must reconcile all historical areas.

The actual 41-year audit walker, including its r2 iteration code and its ten counters, is preserved byte-for-byte from the accepted pilot. It is run separately by batch, accumulating error and event pixel-year equivalents and retaining the entry/termination areas for 2024/2025. The auxiliary-age and frozen-label native fixtures are not regenerated: the exact accepted 31-case / 302-step native CSV and its acceptance are preserved and revalidated by the original validator.

## Historical controls and native/reused provenance

A compact reference extracts the 1985-baseline rows from the accepted 472,891-row window-sensitivity panel. The original panel hash and validation are retained, and the supplied extraction program reproduces the reference and crosswalk from the exact source data ZIP. The compact table has 199,112 rows: 49,778 explicitly reused historical references for the first two intervals and 149,334 fresh native sensitivity rows for the remaining six. Their accepted eight stock/flow/origin fields are the invariance controls. No historic native audit counts are imputed to reused records.

The complete validator authenticates the critical bytes, re-runs the original native-pilot validator against its preserved data/products, verifies the 73-file inventory and manifest, checks every unique canonical cell and batch assignment, verifies partitions, positive support, all zero native error fields and historical per-cell and aggregate controls, and compares the four endpoint rows plus two history rows to the accepted pilot. Flow subcategories must be bounded by their corresponding stocks. Cell support stays fixed among intervals.

Per-cell area tolerance is 0.01 ha. Aggregate area tolerance is 0.001 ha. Error counters must be zero exactly, while independently reduced weighted event-count partitions and pilot count comparisons tolerate 1e-6 pixel equivalents. Fractions use ratios of summed areas, not mean cell fractions. The entry denominator in the baseline interval is zero and yields blank ratios.

## Scope

Implementation tests are local software evidence, including an eager adapter for the asynchronous gate, server wrappers and export assembly. They do not execute Earth Engine or validate whole-domain scientific results. A real full PASS will require all operator-provided native files and preserved fixtures. Operator execution is not independently witnessed; supplied-text hashes are fixed, while executed-text hash and operator attestation remain null unless explicitly supplied. No independent boundary-raster comparison is claimed. Scientific matrix v4.3 and events-v5 remain unchanged.

API sources: [Image.evaluate](https://developers.google.com/earth-engine/apidocs/ee-image-evaluate), [List.iterate](https://developers.google.com/earth-engine/apidocs/ee-list-iterate), [ui.util.setTimeout](https://developers.google.com/earth-engine/apidocs/ui-util-settimeout), [Image.reduceRegions](https://developers.google.com/earth-engine/apidocs/ee-image-reduceregions).

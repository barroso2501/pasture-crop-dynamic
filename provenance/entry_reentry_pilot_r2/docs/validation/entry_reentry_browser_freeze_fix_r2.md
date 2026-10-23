# Browser freeze after Run: implementation revision r2

Date: 2026-10-21. Operator symptom: the Code Editor page became unresponsive after Run. No evidence was supplied of a server task error or a source-data problem.

Inspection found 41 synchronous projection requests and one synchronous band-list request before task creation. Those calls block the browser. The first implementation also unrolled every actual and synthetic annual recurrence in JavaScript. These are concrete design problems compatible with the symptom. They were not isolated experimentally in the operator's browser, so the exact contribution of each is not established.

Revision r2:

- Makes one asynchronous asset-metadata request with `coverage.evaluate` and checks all 41 band IDs, CRSs and six affine coefficients before creating any export.
- Builds the 41-year actual recurrence as server-side `ee.List.iterate` with image-band state/accumulators and fixed 2015/2020 snapshots.
- Builds each of the 31 native fixture recurrences with server-side iteration. All fixtures still share one reduction and retain all expected step comparisons.
- Preserves the exact production step recurrence, all explicit expected sequences, all four output schemas, all ten real invariant counters, all 16 synthetic error fields, both boundary years and historical area controls.
- Retains the exact accepted categorical function for the two t0 comparisons.
- Uses `er1_20261021_r2` and a separate Drive folder to reject mixed old/new attempts.
- Leaves only the runnable 20a in `gee/`; the old scripts and first implementation are preserved in history.

A local eager adapter executes the entire new script, including the metadata callback, server-iteration wrappers, reductions and export assembly. It checks that one asynchronous call is made, no tasks exist before metadata succeeds, invalid metadata creates none, and success produces exactly the four expected tables with the exact schemas. It evaluates all 31 native fixture histories for each successful scenario, including frozen labels, numerical ages, count and year fields; all expected mismatches are zero. This is a local adapter, not Earth Engine execution or browser performance proof.

The extracted step-function/whole-history-oracle checks and the Python integration tests are repeated against r2. Historical native reference inputs remain byte-identical. Native pilot execution and native acceptance remain pending. The revised script must still be run in the operator's GEE session.

References: [client versus server](https://developers.google.com/earth-engine/guides/client_server), [Image.evaluate](https://developers.google.com/earth-engine/apidocs/ee-image-evaluate), [List.iterate](https://developers.google.com/earth-engine/apidocs/ee-list-iterate).

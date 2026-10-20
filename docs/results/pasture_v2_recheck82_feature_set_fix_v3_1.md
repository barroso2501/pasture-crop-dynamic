# Recheck82 code revision v3.1 — Feature property assignment

Date: 2026-10-20. CSV protocol/version remains v3; corrected native export remains pending.

The operator reported 14 original and 3 additional scalar cases passing, then `Line 368: f.setMulti is not a function`. This stops construction of the mapped direct-reduction export. No CSV or complete numerical preflight diagnostics accompanied the report, and no scientific acceptance is inferred.

The active script now returns `ee.Feature(f).set(values)` in the mapped callback. The explicit cast identifies the Feature; `set` accepts a property dictionary and preserves the feature and existing properties. Reference: https://developers.google.com/earth-engine/apidocs/ee-feature-set . The unsupported `setMulti` call was an implementation error in the delivered script.

No other executable line changes. Cell IDs, temporal engine, coverage rules, reducer, geometry support, preflight selection, output fields, protocol version and filename remain unchanged. The v3 validator remains unchanged and compatible. The new guard rejects any future active `.setMulti(` call. Local Node syntax and the 14+3 scalar and five method-selection scenarios pass; these are software checks. The previously passed 17 validator integration tests are not new native evidence.

The original script and original source guard are preserved under `outputs/provenance/pasture_v2_recheck82_v3_before_set_fix/`. The earlier software verification retains historical source hashes; the v3.1 addendum records the updated active hashes. Eight native parent CSVs and all validation inputs remain unchanged. Matrix v4.3/events-v5 and scientific closure status remain unchanged.

Rerun the complete corrected `gee/recheck_pasture_v2_82cells_v3.js`. If Run creates a task after all checks, execute only its one 82-cell export and return the CSV ending `_v3.csv`. Do not repeat the eight parent batches.

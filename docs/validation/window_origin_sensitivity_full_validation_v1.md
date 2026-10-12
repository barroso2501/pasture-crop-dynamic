# Window-origin sensitivity — full validation v1

Date: 2026-10-12. **Status: FULL VALIDATION PASS.**

The supplied 18d validator was executed unchanged against all 48 newly submitted cell CSVs and the full manifest. It authenticated eight accepted full_v3 reference CSVs and the accepted pilot gate JSON. The native synthetic fixture file matches the pilot hash. No synthetic-tabular substitutes were used as scientific data.

The 24,889-cell domain is complete in all 19 normalized baseline/interval populations. There are 423,113 new native rows and 49,778 reused accepted early b=1985 rows, totaling 472,891. New native partition, continuity and confirmed-entry counters are zero. Reused early-row audit fields remain missing. The three baselines have 8, 6 and 5 intervals, respectively. The five-year 2020–2025 interval is diagnostic.

All population, crosswalk, finite/nonnegative fields, unique keys, scope/version/run identifiers, runtime constants, native projection, baseline stock, origin closure, origin/stock bounds, fixed-calendar denominator, b=1985 reference, baseline nesting and time-continuity checks passed. The largest control difference is 3.2782554626464844e-07 ha per cell. Maximum row partition residuals are 2.7284841053187847e-12 ha (flow) and 1.4551915228366852e-11 ha (stock). Both are below their prespecified tolerances. The native 30-case fixtures passed categorical checks; this does not close auxiliary numerical-age or unrelated boundary-raster assurance items.

Output populations: 19 interval rows, 15 calendar-comparison rows, 12 elapsed-comparison rows, 15 pooled rows, three primary crossing descriptors and the 472,891-row normalized panel. Original validator outputs are retained byte-for-byte and have the hashes in `canonical_window_origin_sensitivity_validation_v1.json`. Additional review, display/context tables and figures are derived products, not replacement validation outputs.

Supplied code snapshots are hashed. Operator execution-text attestation was not supplied and remote-script identity is not independently verified, so the executed-script hash remains null. Input/export hashes identify the received files, not mutable upstream asset contents. Phases 2–8, source classification accuracy, first-entry/re-entry decomposition, numerical age 201 and uncertain-pair endpoint cross-tabs are outside this execution.

The full descriptive window sensitivity is accepted. See [scientific findings](../results/window_origin_sensitivity_full_findings_v1.md), [method v2](../methods/window_origin_sensitivity_v2.md), and [machine-readable validation](../../outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_sensitivity_validation_v1.json). The canonical matrix v4.1 is preserved; new sensitivity results supplement its interpretation boundaries.

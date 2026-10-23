# Entry/re-entry pilot: implementation verification

Date: 2026-10-21. **Status: local software verification only. Native pilot pending.**

The distributed exporter passes JavaScript syntax checks. The exact production auxiliary recurrence passes 31 specified histories (302 steps), 46,656 exhaustive length-six histories and 55,986 shared prefix steps. A separate whole-history oracle checks classification, age, frozen entry kind/year and observed entry count. The accepted categorical control function is retained byte-for-byte and compared to the new recurrence.

The standard-library Python validator passes 30 synthetic integration cases. They exercise valid input and immutable reuse, exact inventory, cell/grid/batch identities, interval flags, partitions, historical controls, stock/flow bounds, native support and fixture inventory, runtime and projection metadata, age-201 and frozen-label errors, negative/nonfinite values, duplicate columns, audit completeness, positive-stock/event consistency, and overwrite refusal.

The software and reference inputs are pinned in `config/entry_reentry_source_snapshots_v1.json`. The unchanged accepted sensitivity report authenticates all four source native CSVs; their baseline-1985 subset contains four historical control rows. Native pilot selectors are checked against the validator's exact schemas.

Detailed logs and the machine-readable software verification are under `outputs/validation/entry_reentry_v1/implementation/`. Synthetic integration exports and their temporary PASS reports exist only in disposable test directories and are not included as native or scientific results. No GEE task was executed here and no pilot acceptance JSON is fabricated.

The native return should contain four actual cell/interval rows, two actual historical-audit rows, 31 native fixture rows and one manifest. All six expected-value errors and ten invariant errors must be zero for every fixture; the ten real historical counters and the two-interval reference-state counter must also be zero. Area identities and historical differences must satisfy the declared tolerances. The 31 fixtures cover 302 pixel-year steps, not 302 independent pixels.

Matrix v4.3/events-v5, existing pilots, previous accepted validations and analytical origin remain unchanged. Native pilot acceptance, full decomposition and full-domain age-201 assurance remain pending.

# Decision 024 — observation-window interpretation erratum v4.1

**Date:** 2026-10-09. **Status:** current interpretation edition. **Scope:** P9A035 and P9A036 only; source data, numerical origin summaries, matrix v4 and historical events are unchanged.

The current integrated matrix is `outputs/summary/decision024_review_v1/canonical_integrated_evidence_matrix_v4_1.csv`. P9A035/P9A036 are qualified descriptions of a specified observation window. P9A037 and the other 32 rows retain every substantive field from v4. The updated figure is under `figures/decision024_review_v1/`.

## Correction

Decision 022 already identifies 1985 as an observation boundary. At t0=1985 every observed PAS pixel is initial by definition; therefore the first PAS→TMP origin bar is 100% initial by construction. It is not an empirical comparison of old and newly established pasture populations. A surviving continuous-baseline cohort loses membership after interruption. Later entrants accumulate opportunities to contribute conversions. A stationary finite-duration renewal process can produce such a compositional decline without a changing process.

That explanation is a possibility, not an estimate of how much of the observed decline is mechanical. Neither the magnitude of that contribution nor stationarity has been tested. A cohort's non-increasing membership does not guarantee a non-increasing share in selected conversions. For example, shares of 60/100 then 50/60 increase from 60% to 83.33% while the selected initial area decreases; the denominator matters.

The first >50% observed-entry share in 2000–2005 remains an accurate descriptive statistic for this window. It must not be called a transition date, breakpoint, process threshold or independent evidence of regime change. The pooled 46.91%/53.09% split is also conditional on baseline year, horizon and interval weights. Re-entry is included; 'observed entry' is not 'first-ever establishment'.

## Consequences for use

The numerical results remain usable with the window qualification. Claims that a changing temporal process drives the composition, or that the 50% crossing identifies a process transition, are not supported by these results alone. A 1995/2000 rebasing analysis is specified in `docs/planning/009_observation_window_sensitivity_and_entry_semantics_v1.md` and remains unexecuted. It is required before using rebasing robustness to strengthen an analytical interpretation, not before reporting the existing qualified descriptive values.

The events-v3 CSV is a quoted, normalized index with a dedicated validation-record field. It preserves all original eight field values for the six historical events and appends two interpretation amendments. The v1/v2 event artifacts remain unchanged. The alleged unquoted-comma parse failure was not reproduced: every v2 row has eight fields; the JSON path within `reason` was intentional prose. Explicit quoting and the new field improve interoperability without inventing a historical corruption.

Matrix v4.1 uses UTF-8 with BOM for compatibility with the earlier v3 distribution; both BOM and non-BOM UTF-8 files must be read using `utf-8-sig`. The absence of BOM in v4 was an encoding change, not a finding-name change. Consumers that treat the BOM as part of the first column name must be corrected.

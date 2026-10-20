> Historical status/instructions. On 2026-10-20 the targeted audit was accepted; no rerun is needed. Current: [acceptance record](../validation/pasture_v2_targeted_domain_audit_acceptance_v1.md).

# Native preflight stop: explicit spatial fixture v2.1

Date 2026-10-20. The operator's v2 preflight returned all 26 correctly named outputs, with a systematic alternating pattern: the first input family returned zero; its complement returned 2, 4, …, 26. The assertion expected a maximum of i+1 in every band. It therefore stopped before creating the 82-cell export task. This is a synthetic preflight result, not an observation of age-code anomalies or the 82-cell data. No new scientific acceptance follows.

The console result alone does not establish whether the coordinate-based fixture failed to exercise both patterns or whether the reduction failed the intended independence condition. It does show that skipping the assertion would not be justified. V2.1 keeps that condition and removes the unverified coordinate-parity assumption.

The new fixture uses a four-column by four-row window aligned to the explicit native affine transform. The left geometric half and its complement must each show both values 0 and 1; their union must be 1. This independent fixture check precedes a constant-band naming test and the opposing-half independence test. Both latter tests now use `reduceRegions` on one synthetic feature, matching the API used for the actual 82 cells. All checks must pass before any export task is created.

The temporal engine, audit imagery construction, real geometries, class rules and actual-cell named reducer are unchanged. Existing missing-value guards, raw native diagnostics and failure sentinels remain in force. Only preflight construction and its diagnostic fields change. The versioned validator additionally verifies those fields; parent results and previous rejection records remain immutable.

Local verification covers the 17 retained/added scalar cases, a structural model of 26 independent reducer inputs/outputs, the new four-pixel window geometry calculations and 12 validator integration tests. This is software-only assurance. **Native v2.1 execution is pending.** Follow `RUN_RECHECK82_V2_1_PT.md`; only one new 82-cell export is needed if the native preflight passes.

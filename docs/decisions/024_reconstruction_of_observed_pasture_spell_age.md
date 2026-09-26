# Decision 024 — Reconstruct observed pasture-spell origin from annual coverage

- **Status:** Accepted; implementation and empirical validation pending
- **Date recorded:** 2026-09-26
- **Scope:** Pasture-episode origin, PAS-outflow attribution, and dependent Phase 9 evidence
- **Related decisions:** 003, 009, 020, 022
- **Related plan:** `docs/planning/008_pasture_age_asset_remediation_and_reprocessing_plan_v3.md`
- **Related method:** `docs/methods/observed_pasture_spell_age_reconstruction.md`

## Context

Two independent anomalies were identified in the public MapBiomas Collection
11 pasture-age asset. First, raw value `1` occurs where coverage class `15`
identifies pasture, although `1` is not part of the documented analytical age
encoding used by the project. Second, code `100` can reappear after a pixel
leaves pasture and later returns to class `15`.

The second anomaly invalidates the use of the source code as a direct indicator
of continuous membership in the pasture stock observed in 1985. For example,
the source can encode the following sequence:

```text
Coverage:         PAS  PAS  PAS  TMP  TMP  PAS  PAS
Source age code:  100  100  100   NA   NA  100  100
```

The later pasture spell began after an observed non-pasture state and is not a
continuation of the left-censored 1985 spell. If source code `100` is used
without reconstruction, pasture entering after 1985 can be attributed
incorrectly to the baseline stock.

## Decision

The public pasture-age asset is retained as a source product for provenance and
impact auditing, but it is no longer the analytical authority for pasture-spell
origin or age.

The project will reconstruct **observed pasture-spell origin** directly from
annual Collection 11 coverage classes for 1985–2025. The reconstruction will
distinguish:

1. `not_pasture`;
2. `initial_1985_continuous_stock`;
3. `post_1985_observed_entry`; and
4. `unresolved_episode_origin`.

The associated auxiliary age sequence may use `100` for an uninterrupted
left-censored spell, `201` for the first observed year of a pasture spell that
follows a confidently observed non-pasture year, and `202+` for its consecutive
continuation. A reconstructed code `1` is prohibited.

Any confidently observed transition from PAS to NAT, TMP, OAG, OUT, or WATER
terminates the current pasture spell. This includes PAS→NAT. A later PAS
observation after such a state begins a new observed spell. NODATA, masked, and
unexpected states instead break observed continuity without proving an exit;
PAS after such a gap remains unresolved until a confidently observed non-PAS
state provides a reset.

## Five-year estimand

For every five-year endpoint flow `PAS(t0)→D(t1)`, pasture origin is fixed by
the reconstructed pasture-spell state at `t0`. An exit, re-entry, and later exit
inside the interval does not replace that `t0` origin. Annual pathways remain a
separate analytical object.

RQ2 remains restricted to the origin composition of PAS→temporary-crop
conversion. The same reconstructed origin classification will be applied to
PAS→NAT as a supplementary diagnostic, not as an expansion of RQ2.

## Accounting rules

Every destination-specific origin partition must satisfy:

```text
PAS→destination total =
    initial continuous origin
  + post-1985 observed-entry origin
  + unresolved origin
```

Observed land-cover outflow and observation loss must remain separate:

```text
observed PAS outflow = PAS→TMP + PAS→NAT + PAS→OAG + PAS→OUT + PAS→WATER

PAS endpoint non-persistence =
    observed PAS outflow
  + PAS→NODATA
  + PAS→unexpected
  + PAS→masked

PAS stock at t0 = PAS→PAS persistence + PAS endpoint non-persistence
```

`PAS→other_observed` may group OAG, OUT, and WATER for presentation.
`PAS→observation_loss` may group NODATA, unexpected, and masked. These two
groups must never be merged into one substantive transition class.

## Temporal boundaries

The reconstructed 1985 spell is a **left-censored continuous pasture episode**,
not evidence of when pasture was first established. Entry or termination
events triggered in 2024 or 2025 must preserve event type and year and be
flagged as boundary-adjacent, consistent with Decision 022.

The 2020–2025 interval remains included in full-series outputs and explicitly
identified as the diagnostic temporal-boundary interval. The primary
inferential period remains 1985–2020.

## Evidence status and versioning

Findings P9A035, P9A036, and P9A037 are suspended because they depend on the
source-based PAS→temporary-crop origin partition. They must not be cited as
accepted results until the corrected pilot and full run pass the criteria in
the approved plan.

Accepted earlier files remain immutable for provenance. Suspension is recorded
in `canonical_evidence_status_events_v1.csv`. A future rescission must be a new
versioned event linked to the validating evidence; it must not overwrite the
accepted suspension record.

The suspension does not apply to total PAS→TMP area, total PAS→NAT area,
coverage-based stocks, NAT→PAS replenishment, NAT→TMP endpoint transitions, or
other fields whose invariance is demonstrated by the remediation validation.

## Consequences

- Decisions 003 and 020 remain part of the provenance record but are
  superseded where they authorize direct analytical attribution from the
  public pasture-age code.
- RQ1's fixed 1985 pixel cohort remains conceptually distinct from the current
  pasture spell. A baseline-cohort pixel remains in that fixed cohort after it
  leaves pasture, while a later pasture re-entry is a post-1985 episode.
- Source code `1` and source code `100` reuse will be measured in an impact
  audit, including their overlap, but neither will control corrected origin
  attribution.
- Phases 2–8 will be rerun only if the downstream invariance gate finds a
  change in a non-origin field.
- Corrected analytical products will use new versioned filenames and will not
  overwrite accepted version-1 records.

## Acceptance criteria

This decision is fully implemented only when:

1. all synthetic temporal sequences pass;
2. all 41 annual coverage bands are processed chronologically;
3. every observed PAS pixel has exactly one reconstructed origin state;
4. reconstructed `100` never reappears after an observed interruption;
5. every observed re-entry begins at `201`;
6. uncertain histories remain explicit;
7. origin, destination, observation-loss, and initial-stock identities close;
8. all eight interval outputs contain the 24,889 canonical cells exactly once;
9. non-origin fields pass the downstream invariance gate;
10. 2024–2025 episode boundaries retain event type and year;
11. source-code anomaly and overlap audits are complete; and
12. validation records, manifests, hashes, and corrected evidence products are
    complete.

Until then, the decision is accepted as the governing specification, but the
remediation must not be described as empirically completed.

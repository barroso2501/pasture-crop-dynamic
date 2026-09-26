# Pasture-age asset remediation and reprocessing plan

**Version:** 3
**Status:** approved methodological remediation plan; implementation pending
**Scope:** reconstruction of observed pasture episodes; correction of the PAS→temporary-crop origin attribution used for RQ2; supplementary PAS→NAT origin diagnosis; explicit separation of observed PAS outflow from observation loss in endpoint accounting; and controlled reprocessing of dependent products
**Primary period:** 1985–2020
**Diagnostic extension:** 2020–2025 remains included and explicitly flagged
**Related decisions:** 003 (unresolved pasture-age code `1`), 009 (multiquinquennial episodes and 2020–2025), 020 (Phase 9 RQ1/RQ2 gap resolution), 022 (temporal boundary symmetry and 2020–2025 uncertainty sources)

## Version history

### Version 3 amendments

Version 3 resolves six issues identified in the review of version 2:

1. **RQ2 remains restricted to PAS→temporary crops.** PAS→NAT retains the
   same reconstructed origin classification but is treated as a supplementary
   diagnostic and accounting product, not as an expansion of RQ2 or of
   findings P9A035–P9A037.
2. **The five-year origin estimand is fixed at `t0`.** For an endpoint flow
   `PAS(t0)→D(t1)`, the origin category is the reconstructed pasture-episode
   state at the interval start. A different pasture episode beginning and
   ending inside the interval does not replace that origin. Annual pathways
   remain available as a separate analytical object.
3. **Endpoint accounting now separates substantive observed outflow from
   observation loss.** `NODATA`, `unexpected`, and `masked` are not described
   as land-cover transitions and are not absorbed into a substantive
   `PAS→other` residual.
4. **Uncertain histories can become attributable again.** After a gap, a
   confidently observed non-PAS year resets uncertainty; the next PAS year is
   a new observed entry (`201`).
5. **Boundary-adjacent events receive year-specific fields.** Entry and
   termination flags retain the triggering year rather than collapsing all
   2024–2025 events into a single series-level indicator.
6. **Evidence-status records remain immutable.** Suspension is recorded as a
   versioned event. A later rescission creates another versioned event linked
   to the validating evidence rather than modifying the accepted suspension
   record in place.

These amendments clarify the estimand and accounting identities without
changing the reconstruction principle adopted in version 2.

### Version 2 amendments

Version 2 incorporates seven corrections identified in review of version 1, plus one editorial consistency fix. Each is justified below; none reverses a version-1 decision, all are extensions or connective tissue.

1. **Scope generalized from PAS→temporary crops only to all PAS-outflow destinations.** Version 1's reconstruction rules (Section 4.4) were already destination-agnostic, but the plan's purpose, evidence status, impact table, and implementation steps narrowed to PAS→temporary crops only. This left PAS→NAT — a principal focal flow under `docs/methods/data_sources_and_classification.md` — exposed to exactly the same code-`100` reuse defect without a correction path. The project's own stock-flow closure discipline ("no component may be inferred solely by omission without also being exported or audited explicitly") requires the same treatment. Scope now covers PAS→temporary crops and PAS→NAT explicitly, with PAS→other (mosaic/other agriculture, other anthropogenic, water) carried as a closing residual.
2. **Added a synthetic verification case for 1985 itself unobserved (NODATA or masked).** Version 1's test table covered gaps occurring after 1985 but not at 1985.
3. **Step 3's audit now cross-checks overlap between the code-`1` population (Decision 003) and the code-`100`-reuse population (this plan).** Both are defects in the same source asset and could compound within the same pixel trajectory; version 1's audit treated them independently.
4. **Explicit linkage to Decision 022.** The reconstructed variable's reliability at the two ends of the series is not independent of the boundary limits Decision 022 already established for the underlying coverage classification. A new Section 4.6 makes this inheritance explicit rather than leaving it implicit.
5. **The evidence suspension in Section 6 is now backed by a structured, checkable artifact**, not only by plan prose, so that suspension and eventual rescission can be verified programmatically.
6. **Step 9 now names the decisions the future Decision 024 must cite (003, 009, 020, 022)** and adds `docs/methods/data_sources_and_classification.md` to the documents requiring revision, since its current "Pasture-origin classification" section is scoped to PAS→TMP only.
7. **Step 2 now requires a small-tile computational feasibility and timing check** before full-domain commitment, mirroring the precedent set for full-domain processing in Decision 005.
8. *(Editorial, not a scope change.)* Section 5's terminology for gap years is made consistent: the gap year itself (NODATA/masked) is labeled `uncertain`; a PAS year whose origin cannot be attributed because of a preceding gap is labeled `unresolved`. Version 1 used both words for the gap year itself in different rows (compare its rows 5 and 6); this was inconsistent, not a substantive disagreement.

## 1. Purpose

This plan defines the response to two independent anomalies identified in the
public MapBiomas Collection 11 pasture-age asset:

1. the occurrence of raw value `1`, which behaves as pasture presence without
   an attributable numerical age; and
2. the reuse of code `100` after a pixel leaves pasture and later returns to
   coverage class `15`.

The second anomaly is methodologically material. Code `100` was interpreted as
the pasture stock already present at the beginning of the series and therefore
left-censored in 1985. When the code returns after an observed interruption, it
no longer identifies the same continuous pasture episode. Using it without
reconstruction can incorrectly transfer post-1985 pasture episodes into the
left-censored baseline stock.

The project will no longer use the public pasture-age asset as the analytical
source for PAS-outflow origin attribution. Instead, it will derive an
auditable sequence of observed pasture episodes directly from the annual
MapBiomas coverage series.

The corrected PAS→temporary-crop origin partition remains the analytical
product that answers RQ2. The same reconstructed origin state will also be
reported for PAS→NAT as a supplementary diagnostic because the source defect
is destination-independent. Remaining PAS endpoint destinations will be
retained for accounting closure, with substantive destinations kept separate
from loss of observation.

## 2. Observed failure

The source asset can represent the following sequence as:

```text
Coverage:         PAS  PAS  PAS  TMP  TMP  PAS  PAS
Source age code:  100  100  100   NA   NA  100  100
```

The expected episode logic is:

```text
Coverage:                  PAS  PAS  PAS  TMP  TMP  PAS  PAS
Observed pasture episode:  100  100  100   NA   NA  201  202
```

The first episode is left-censored because it is already present in 1985. The
second episode begins inside the observed series and therefore has an observed
entry year. It must not inherit the left-censored status of the earlier
episode.

The same source defect can affect a pixel whose endpoint destination is NAT
rather than temporary crops. This supports applying the reconstructed origin
state to PAS→NAT as a supplementary analysis, but it does not change the scope
of RQ2.

## 3. Analytical object to be reconstructed

The new variable is defined as **observed consecutive pasture-spell age**: the
number of consecutive annual observations in the current pasture episode,
subject to left censoring at the beginning of the series.

It is not presented as a corrected official MapBiomas product. It is a
project-derived analytical variable based on the annual coverage classifications.

The principal categorical variable will be **pasture-spell origin**, with the
following states:

| Code | State | Definition |
|---:|---|---|
| 0 | `not_pasture` | Current annual coverage is not PAS |
| 1 | `initial_1985_continuous_stock` | PAS in 1985 and continuously PAS through the reference year |
| 2 | `post_1985_observed_entry` | Current pasture episode began after an observed non-PAS year |
| 3 | `unresolved_episode_origin` | Current PAS episode cannot be attributed because its backward history encounters unobserved, masked, or unexpected coverage before a confirmed entry or 1985 |

The categorical state, rather than a numerical code alone, will control:

- the PAS→temporary-crop origin partition used for RQ2;
- the supplementary PAS→NAT origin partition; and
- accounting checks for other PAS-outflow destinations.

`PAS→other_observed` comprises OAG, OUT, and WATER. Observation-loss
destinations (`NODATA`, `unexpected`, and `masked`) remain separate and must
not be absorbed into this substantive residual.

## 4. Temporal reconstruction rules

### 4.1 Initial year

For 1985:

- PAS receives `initial_1985_continuous_stock` and auxiliary age code `100`;
- confidently observed non-PAS receives `not_pasture`;
- missing, masked, or unexpected coverage does not establish a pasture origin.
  This third case is not a terminal state: it seeds an `uncertain` starting
  condition that Section 4.5 resolves for any later PAS observation (see the
  1985-masked case added to Section 5).

### 4.2 Continuation of an initial episode

An initial episode retains code `100` only while PAS is observed in every
consecutive year from 1985 through the reference year.

Code `100` must never reappear after the initial episode has ended.

### 4.3 Observed entry after 1985

When current coverage is PAS and the immediately preceding year is a
confidently observed non-PAS class, a new episode begins:

```text
non-PAS → PAS → PAS → PAS
   NA     201   202   203
```

Any later return to PAS after another observed non-PAS year restarts the age at
`201`.

### 4.4 Episode termination

Any observed transition from PAS to another valid coverage state terminates
the pasture episode. This includes:

- PAS→NAT;
- PAS→temporary crops;
- PAS→other agriculture;
- PAS→water;
- PAS→OUT or another valid non-PAS state.

The ecological interpretation of the transition does not change the temporal
rule. PAS→NAT terminates the episode even when it may represent regeneration,
classification noise, or a short-lived alternation.

Episode termination is used to reconstruct the annual state sequence, but the
five-year endpoint-flow estimand remains anchored at the interval start. For
each flow `PAS(t0)→D(t1)`, origin is defined by the reconstructed pasture-
episode state at `t0`.

An exit, re-entry, and second exit occurring between `t0` and `t1` does not
replace the origin category observed at `t0`. Such within-interval changes may
be examined separately as annual pathway information but must not silently
change the endpoint-flow estimand.

### 4.5 Missing or uncertain observations

`NODATA`, masked pixels, and unexpected coverage states break observed
continuity but do not prove a non-PAS transition. A later return to PAS after
such a gap is assigned `unresolved_episode_origin`, not automatically `201`.

```text
PAS → NODATA → PAS
100 → uncertain → unresolved
```

This state may later become attributable if the reconstruction design adopts
an explicitly validated gap rule. No gap bridging is authorized in
reconstruction specification version 1.

Uncertainty does not persist after a confidently observed non-PAS state. If a
gap is followed by NAT, TMP, OAG, OUT, or WATER and PAS occurs later, that PAS
observation begins a new attributable episode at `201`.

Terminology note (version 2): the gap year itself (NODATA or masked) is
reported as `uncertain`. A PAS year whose origin cannot be attributed because
its backward history crosses that gap is reported as `unresolved`. These are
kept distinct because the first describes an observation problem in a single
year and the second describes an attribution problem in a pasture episode
that may span many subsequent years.

### 4.6 Inherited boundary reliability (new in version 2)

This reconstruction is a project-derived refinement of the same annual
coverage series whose 1985 and 2024–2025 boundaries Decision 022 already
characterizes. It does not remove those limits; it inherits them at the
episode level:

- At 1985, `initial_1985_continuous_stock` is the same left-censored cohort
  object Decision 022 already describes as bounded by Landsat availability
  rather than by any land-use-process-relevant event. This reconstruction
  changes how that cohort is *tracked forward* (preventing later re-entries
  from being folded back into it); it does not change what can be known about
  its *establishment date*.
- At 2024–2025, an episode entry or termination detected only in the final
  one to two years of the series inherits Decision 022's
  `temporal-filter-limited` uncertainty: an episode boundary cannot be more
  reliable than the annual coverage classification it is built from, and that
  classification carries reduced temporal-filter support in exactly those
  years (class- and year-specific, per Decision 022's filter specification).

Implementation requirement: any episode entry (`post_1985_observed_entry`) or
termination whose triggering year is 2024 or 2025 must retain a year-specific
boundary qualification, distinct from `unresolved_episode_origin`. At minimum,
the reconstructed output must provide:

```text
entry_boundary_adjacent_<year>
termination_boundary_adjacent_<year>
episode_boundary_year
```

Equivalent long-format event fields are acceptable if they preserve event
type and triggering year. This lets downstream analyses apply Decision 022's
caveats at the episode level, not only at the annual coverage level.

## 5. Synthetic verification cases

The temporal engine must pass at least the following cases before processing
the canonical domain:

| Coverage sequence | Expected auxiliary age sequence |
|---|---|
| `PAS, PAS, PAS` from 1985 | `100, 100, 100` |
| `PAS, PAS, TMP, PAS, PAS` | `100, 100, NA, 201, 202` |
| `NAT, PAS, PAS, NAT, PAS` | `NA, 201, 202, NA, 201` |
| `PAS, NAT, PAS, NAT, PAS` | `100, NA, 201, NA, 201` |
| `PAS, NODATA, PAS` | `100, uncertain, unresolved` |
| `TMP, PAS, NODATA, PAS` | `NA, 201, uncertain, unresolved` |
| `NODATA, PAS, PAS` (1985 itself unobserved) | `uncertain, unresolved, unresolved` |
| `NODATA, PAS, NAT, PAS` | `uncertain, unresolved, NA, 201` |
| `PAS, NODATA, PAS, NAT, PAS` | `100, uncertain, unresolved, NA, 201` |

Required invariants are:

- no derived code `1`;
- `100` occurs only in an uninterrupted episode beginning in 1985;
- every `201` follows a confidently observed non-PAS year;
- every `202+` increments the preceding derived episode age by one;
- every confidently observed non-PAS pixel is outside the current pasture
  episode;
- every current PAS pixel receives exactly one origin state;
- no origin state overlaps another;
- every episode boundary triggered in 2024 or 2025 retains its event type and
  triggering year and is flagged as boundary-adjacent (Section 4.6).

## 6. Immediate evidence status

Until remediation is completed:

- findings P9A035, P9A036, and P9A037 are suspended;
- existing PAS-to-temporary-crop origin shares must not be cited in manuscripts,
  abstracts, presentations, or releases;
- figures showing the censored/new pasture-origin composition are provisional;
- accepted version-1 files remain preserved for provenance and must not be
  silently overwritten;
- no PAS→NAT origin partition has been published or cited to date, so there is
  nothing to formally suspend on that flow; but any such analysis produced
  before this remediation is complete is subject to the same restriction as
  P9A035–P9A037 above.

The suspension applies to pasture-origin attribution on any destination, not
to total observed transition area by destination class.

The suspension is additionally recorded in a structured, machine-checkable
event record (new in version 2; see Step 1) rather than being auditable only
from this plan's prose. Rescission requires a later versioned status event, not
an overwrite of the accepted suspension record and not merely regeneration of
the figure or statistic.

## 7. Expected impact by analytical component

| Component | Expected status | Required action |
|---|---|---|
| Annual coverage states | Unaffected | Retain |
| Total stocks by coverage class | Unaffected | Verify invariance |
| NAT→PAS replenishment | Unaffected | Verify invariance |
| PAS→temporary-crop conversion total | Unaffected | Verify invariance |
| PAS→NAT conversion total | Unaffected | Verify invariance |
| NAT→temporary-crop endpoint transition and pathways | Unaffected | Verify invariance |
| Consolidation–replenishment balance | Unaffected | Verify invariance |
| Fixed 1985 PAS pixel cohort used for RQ1 | Expected to remain valid | Revalidate baseline definition and output hashes |
| PAS-to-temporary-crop origin partition used for RQ2 | Invalid pending correction | Reconstruct and reprocess |
| PAS→NAT origin partition | Not previously accepted; source-dependent if produced | Reconstruct as a supplementary diagnostic, outside RQ2 |
| PAS→other observed (OAG, OUT, WATER) origin | Not previously computed | Compute as a substantive closing group; no manuscript claim required |
| PAS→observation loss (NODATA, unexpected, masked) | Explicit coverage diagnostic | Retain separately from substantive outflows and include in full closure |
| Cell trajectories, Moran, LISA, biome comparisons, and MAUP | Expected to remain valid | Apply formal invariance gate before deciding whether to rerun |
| Integrated evidence matrix | Partly invalid | Replace dependent evidence rows after corrected execution |

The fixed RQ1 cohort and the reconstructed episode origin represent different analytical
objects. A pixel that was PAS in 1985 remains a member of the fixed spatial
cohort even after leaving and returning to pasture. Its later pasture episode,
however, is classified as post-1985. This classification answers RQ2 when the
endpoint flow is PAS→temporary crops and is supplementary when the endpoint
flow is PAS→NAT.

## 8. Implementation sequence

### Step 1 — Preserve and register the source anomaly

Create a decision record describing:

- raw value `1` in the public asset;
- reuse of `100` after observed pasture interruption;
- suspension of affected evidence;
- reconstruction rule adopted by the project;
- distinction between a source product and a project-derived variable.

The public asset and all accepted version-1 outputs remain immutable evidence.

In addition, produce a structured suspension-event record as an immediate,
checkable artifact rather than plan prose alone:

```text
outputs/validation/pasture_age_remediation_v1/
canonical_evidence_status_events_v1.csv
```

with columns `event_id, finding_id, event_status, effective_date, reason,
governing_record, rescission_criteria, source_version`. Initial rows are
P9A035, P9A036, and P9A037, each with `event_status = suspended`,
`governing_record = 008`, and `rescission_criteria = corrected origin
partition passes Step 4/Step 8 acceptance criteria`.

The accepted file is immutable. If remediation later permits rescission, a
new versioned event file records `event_status = rescinded` and references the
validation artifact that satisfied the criterion.

### Step 2 — Build the reconstruction engine

Implement an Earth Engine script that reads only annual coverage bands and
produces:

1. 41 bands of observed pasture-spell origin;
2. 41 optional bands of auxiliary consecutive episode age;
3. year- and event-specific boundary-adjacent fields per Section 4.6 for
   episode entries or terminations triggered in 2024 or 2025;
4. annual validation summaries;
5. counts and areas of unresolved origins;
6. a reproducible configuration record with asset identifiers, native CRS,
   transform, class definitions, and script version.

Recommended analytical names are:

```text
canonical_observed_pasture_spell_origin_c11_v1
canonical_observed_pasture_spell_age_c11_v1
```

Computational feasibility check (new in version 2): before committing to a
full 24,889-cell, 41-band export, run the reconstruction engine on a small
tile or single biome subset, measure computation time and export size, and
extrapolate to the full domain. Confirm the extrapolated job stays within
Earth Engine's computation and export limits before proceeding to Step 3.
This mirrors the full-domain commitment precedent already established in
Decision 005.

### Step 3 — Audit the magnitude of the source error

Compare the public pasture-age asset against the reconstructed series for every
year and report:

- area and pixel count where source `100` conflicts with a post-1985 episode;
- number of affected canonical cells;
- first and last occurrence years;
- spatial distribution by primary biome and boundary context;
- number and duration of pasture re-entry episodes;
- area currently represented by source code `1`;
- area affected by missing or uncertain coverage histories;
- overlap between the code-`1` population (Decision 003) and the
  code-`100`-reuse population addressed by this plan, reported as a joint
  contingency table (new in version 2), since both are defects in the same
  source asset and could compound within the same pixel trajectory.

The audit must distinguish source discrepancies from the analytical
reclassification adopted by the project.

### Step 4 — Run a pasture-origin remediation pilot

Use 2015–2020 as the first pilot because it supports a central RQ2 comparison.
Calculate the old and reconstructed PAS→temporary-crop origin partitions side
by side. Apply the same reconstructed origin state to PAS→NAT as a
supplementary diagnostic. For the same interval, calculate
`PAS→other_observed` and `PAS→observation_loss` separately.

Pilot acceptance requires:

- exact closure of the origin partition within every destination;
- exact closure of PAS endpoint non-persistence across observed outflow and
  observation-loss destinations;
- zero overlap among origin components;
- reproduction of synthetic sequences;
- exact invariance of every non-age stock and flow field;
- documented transfer from the old censored category to the reconstructed
  post-1985 category for PAS→temporary crops and, separately, for the
  supplementary PAS→NAT diagnostic;
- explicit unresolved component where history is insufficient;
- correct `boundary_adjacent` flagging is not exercised by this interval
  (2015–2020 predates the 2024–2025 boundary) and is instead checked in Step 5
  once the 2020–2025 interval is reprocessed.

### Step 5 — Reprocess all eight intervals

After pilot acceptance, execute the corrected full-domain stock-flow extraction
for:

```text
1985–1990
1990–1995
1995–2000
2000–2005
2005–2010
2010–2015
2015–2020
2020–2025
```

The new exports must use versioned filenames and must not overwrite the
original CSV files.

### Step 6 — Rebuild canonical dependent products

Create version-2 products, including at least:

```text
canonical_stock_flow_panel_1985_2025_v2.parquet
canonical_stock_flow_derived_metrics_v2.parquet
canonical_integrated_stock_flow_trajectory_1985_2025_v2.parquet
canonical_pas_tmp_origin_interval_summary_v2.csv
canonical_pas_tmp_origin_pooled_summary_v2.csv
canonical_pas_nat_origin_interval_summary_v2.csv
canonical_pas_nat_origin_pooled_summary_v2.csv
canonical_pas_outflow_destination_and_origin_closure_v2.csv
```

The last file verifies three separate identities per interval and pooled:

```text
PAS→destination total =
    initial continuous origin
  + post-1985 observed-entry origin
  + unresolved origin

observed PAS outflow =
    PAS→TMP
  + PAS→NAT
  + PAS→OAG
  + PAS→OUT
  + PAS→WATER

PAS endpoint non-persistence =
    observed PAS outflow
  + PAS→NODATA
  + PAS→unexpected
  + PAS→masked

PAS stock at t0 =
    PAS→PAS persistence
  + PAS endpoint non-persistence
```

For presentation, OAG, OUT, and WATER may be grouped as
`PAS→other_observed`; NODATA, unexpected, and masked may be grouped as
`PAS→observation_loss`. The two groups must remain distinguishable.

Regenerate RQ2 figures, tables, evidence statements, and manuscript-ready
language from these corrected products.

### Step 7 — Apply the downstream invariance gate

Compare version 1 and version 2 for all fields unrelated to pasture origin.

If stocks, total flows, trajectory metrics, mapped metrics, and spatial inputs
are identical within their prespecified tolerances, Fases 2–8 do not need full
statistical recomputation. Their validity will be documented through an
invariance record.

If any non-age field changes unexpectedly, stop and reprocess every downstream
phase that depends on that field.

### Step 8 — Revalidate RQ1 and rebuild RQ2

For RQ1:

- confirm that the 1985 fixed cohort remains identical;
- confirm that its subsequent endpoint states depend only on coverage;
- retain results only after hash and population reconciliation.

For RQ2:

- replace all PAS→temporary-crop origin shares and temporal comparisons;
- reassess the direction and strength of the censored-to-post-1985 shift for
  PAS→temporary crops;
- revise P9A035–P9A037;
- regenerate the relevant figure and evidence matrix rows.

Separately from RQ2:

- report the PAS→NAT origin partition as a supplementary diagnostic;
- compare its temporal direction with PAS→temporary crops without treating it
  as an answer to RQ2; and
- create new evidence identifiers only if this supplementary result is later
  admitted to the integrated evidence matrix.

### Step 9 — Update documentation and releases

Add or revise:

```text
docs/decisions/024_reconstruction_of_observed_pasture_spell_age.md
docs/methods/observed_pasture_spell_age_reconstruction.md
docs/validation/canonical_pasture_spell_age_validation_v1.md
docs/validation/pasture_age_source_asset_impact_audit_v1.md
docs/methods/data_sources_and_classification.md
```

Decision 024 must explicitly cite and remain consistent with Decisions 003
(unresolved code `1`), 009 (multiquinquennial episodes and 2020–2025), 020
(Phase 9 RQ1/RQ2 gap resolution), and 022 (temporal boundary symmetry and
2020–2025 uncertainty sources) — new in version 2, so that the reconstruction
is legible as an extension of the project's existing censoring and boundary
framework rather than a freestanding fix.

The revision to `docs/methods/data_sources_and_classification.md` must replace
the source-age rule with the reconstructed `t0` origin state. It must preserve
PAS→temporary crops as the RQ2 estimand, describe PAS→NAT as supplementary,
and state the separate identities for `PAS→other_observed` and
`PAS→observation_loss` established in Sections 7 and 8 of this plan.

README product lists, data dictionaries, manifests, release notes, and the
dual-manuscript plan must point to the corrected version-2 products.

## 9. Full-run acceptance criteria

The remediation is accepted only if:

1. all synthetic temporal tests pass, including the 1985-unobserved case;
2. all 41 annual coverage bands are processed in chronological order;
3. every current PAS pixel has exactly one origin state;
4. code `100` never reappears after an observed interruption;
5. every observed re-entry begins at auxiliary code `201`;
6. all uncertain histories remain explicit rather than being silently assigned;
7. the origin components close exactly within each destination; substantive
   destinations close to observed PAS outflow; and observed outflow plus
   observation loss closes to PAS endpoint non-persistence while preserving
   `PAS→other_observed` and `PAS→observation_loss` as separate groups;
8. all eight intervals contain 24,889 unique canonical cells;
9. non-age stocks and flows reconcile with version 1 within the accepted
   numerical tolerance;
10. corrected summaries reproduce their underlying cell-level totals;
11. primary and diagnostic periods remain separately identified;
12. every episode boundary triggered in 2024 or 2025 retains event type and
    triggering year and is flagged as boundary-adjacent;
13. the code-`1`/code-`100` overlap audit (Step 3) is complete and reconciled;
14. output inventories, hashes, validation JSON files, and method records are
    complete.

## 10. Interpretation and publication language

The corrected categories should be described as:

- **left-censored continuous 1985 pasture episode**, rather than pasture known
  to have been established before 1985;
- **pasture episode with observed post-1985 entry**, rather than necessarily a
  first-ever pasture establishment at that location;
- **unresolved episode origin** when the annual history does not support either
  classification.

This terminology recognizes that the series identifies the beginning of the
current observed pasture spell, not the complete land-use history before 1985.

Any statement about an episode boundary occurring in 2024 or 2025 should
carry the same qualification Decision 022 requires for the underlying
coverage classification in those years: the boundary is `boundary_adjacent`
and should be described as provisional pending fuller temporal-filter support
in a future MapBiomas release, not as a confirmed entry or termination on the
same footing as boundaries observed mid-series.

## 11. Communication with MapBiomas

The source team should receive:

- a minimal pixel sequence demonstrating the reappearance of `100`;
- the exact asset identifier, coordinates, and affected band names;
- the shared diagnostic point asset;
- the quantitative source-impact audit after it is completed;
- a request for confirmation of intended code semantics and production logic.

The project-derived reconstruction can proceed independently of the source
response. Any later corrected MapBiomas asset should be compared against the
project reconstruction before replacing accepted analytical products.

## 12. Next operational artifact

The next deliverable is the pilot implementation package containing:

```text
gee/17a_reconstruct_observed_pasture_spell_age_v1.js
gee/17b_compare_source_and_reconstructed_pasture_age_v1.js
gee/17c_reprocess_stock_flow_origin_pilot_v2.js
analysis/17d_validate_pasture_age_remediation_pilot_v1.py
```

No full-series product should be replaced before the reconstruction engine and
2015–2020 pilot satisfy the acceptance criteria in this plan.

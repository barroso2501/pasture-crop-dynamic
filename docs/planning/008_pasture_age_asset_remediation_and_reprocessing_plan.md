> **Status notice — 2026-10-09:** This is a superseded plan-v2 record; statuses and source-age percentages in its body apply to its original edition. Current status: [Decision 024 closure and qualifications](../decisions/024_implementation_closure_v2.md); current RQ2 interpretation: [erratum v4.1](../results/decision024_origin_window_erratum_v4_1.md).

# Pasture-age asset remediation and reprocessing plan

**Version:** 2
**Status:** approved methodological remediation plan; implementation pending
**Scope:** reconstruction of observed pasture episodes, correction of PAS-outflow origin attribution (temporary crops and native vegetation, closed against a residual), and controlled reprocessing of dependent products
**Primary period:** 1985–2020
**Diagnostic extension:** 2020–2025 remains included and explicitly flagged
**Related decisions:** 003 (unresolved pasture-age code `1`), 009 (multiquinquennial episodes and 2020–2025), 020 (Phase 9 RQ1/RQ2 gap resolution), 022 (temporal boundary symmetry and 2020–2025 uncertainty sources)

## Version 2 amendments

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
MapBiomas coverage series, and will apply that reconstruction to every
PAS-outflow destination that the project treats as a principal focal flow
(PAS→temporary crops and PAS→NAT), closing the remainder as a residual rather
than leaving it undefined by omission.

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

The same defect affects a pixel that later transitions PAS→NAT rather than
PAS→temporary crops: the origin of the pasture episode immediately preceding
either transition is misattributed in exactly the same way, regardless of the
destination class.

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

The categorical state, rather than a numerical code alone, will control the
origin partition for every PAS-outflow destination the project analyzes as a
principal focal flow — PAS→temporary crops and PAS→NAT — with PAS→other
(mosaic/other agriculture, other anthropogenic uses, water) closed as a
residual so the partition is never incomplete by omission.

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

The origin state attached to the episode that just terminated is what feeds
the origin partition at whichever destination the pixel transitions to. The
reconstruction engine itself does not need to know the destination class to
compute the origin state — the destination-specific partitions in Section 7
and the implementation steps are simply different groupings of the same
per-pixel, per-year output by the transition each pixel happens to make.

### 4.5 Missing or uncertain observations

`NODATA`, masked pixels, and unexpected coverage states break observed
continuity but do not prove a non-PAS transition. A later return to PAS after
such a gap is assigned `unresolved_episode_origin`, not automatically `201`.

```text
PAS → NODATA → PAS
100 → uncertain → unresolved
```

This state may later become attributable if the reconstruction design adopts
an explicitly validated gap rule. No gap bridging is authorized in version 1.

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
termination whose triggering year is 2024 or 2025 must be flagged
`boundary_adjacent = true` in the reconstructed output, distinct from
`unresolved_episode_origin`. This lets downstream analyses apply Decision
022's caveats at the episode level, not only at the annual coverage level.

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

Required invariants are:

- no derived code `1`;
- `100` occurs only in an uninterrupted episode beginning in 1985;
- every `201` follows a confidently observed non-PAS year;
- every `202+` increments the preceding derived episode age by one;
- every confidently observed non-PAS pixel is outside the current pasture
  episode;
- every current PAS pixel receives exactly one origin state;
- no origin state overlaps another;
- every episode boundary triggered in 2024 or 2025 is flagged
  `boundary_adjacent` (Section 4.6).

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
to total PAS-outflow conversion area by destination class.

The suspension is additionally recorded in a structured, machine-checkable
log (new in version 2; see Step 1) rather than being auditable only from this
plan's prose. Rescinding the suspension for a given finding requires updating
that log, not only regenerating the figure or statistic.

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
| PAS→NAT origin partition | Invalid pending correction (newly scoped in version 2) | Reconstruct and reprocess |
| PAS→other (mosaic/other agriculture, other anthropogenic, water) origin, as closure residual | Not previously computed | Compute as a closing term against total PAS outflow; no manuscript claims required beyond the closure check itself |
| Cell trajectories, Moran, LISA, biome comparisons, and MAUP | Expected to remain valid | Apply formal invariance gate before deciding whether to rerun |
| Integrated evidence matrix | Partly invalid | Replace dependent evidence rows after corrected execution |

The fixed RQ1 cohort and the RQ2 episode origin represent different analytical
objects. A pixel that was PAS in 1985 remains a member of the fixed spatial
cohort even after leaving and returning to pasture. Its later pasture episode,
however, is classified as post-1985 for RQ2, on whichever destination it
eventually transitions to.

## 8. Implementation sequence

### Step 1 — Preserve and register the source anomaly

Create a decision record describing:

- raw value `1` in the public asset;
- reuse of `100` after observed pasture interruption;
- suspension of affected evidence;
- reconstruction rule adopted by the project;
- distinction between a source product and a project-derived variable.

The public asset and all accepted version-1 outputs remain immutable evidence.

In addition (new in version 2), produce a structured suspension log as an
immediate, checkable artifact rather than plan prose alone:

```text
docs/validation/evidence_suspension_log_v1.csv
```

with columns `finding_id, status, suspended_date, reason, governing_plan,
rescission_criteria, rescinded_date`. Initial rows: P9A035, P9A036, P9A037,
each `status = suspended`, `governing_plan = 008`, `rescission_criteria =
corrected origin partition passes Step 4/Step 8 acceptance criteria`.

### Step 2 — Build the reconstruction engine

Implement an Earth Engine script that reads only annual coverage bands and
produces:

1. 41 bands of observed pasture-spell origin;
2. 41 optional bands of auxiliary consecutive episode age;
3. a `boundary_adjacent` flag band per Section 4.6 for episode boundaries
   triggered in 2024 or 2025;
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

### Step 4 — Run a PAS-outflow origin pilot

Use 2015–2020 as the first pilot because it supports a central RQ2 comparison.
Calculate the old and reconstructed origin partitions side by side for both
PAS→temporary crops and PAS→NAT, and compute the PAS→other closure residual
for the same interval.

Pilot acceptance requires:

- exact closure to total PAS-outflow area, by destination and in aggregate;
- zero overlap among origin components;
- reproduction of synthetic sequences;
- exact invariance of every non-age stock and flow field;
- documented transfer from the old censored category to the reconstructed
  post-1985 category, for both destinations;
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
canonical_pas_outflow_origin_closure_v2.csv
```

The last file (new in version 2) verifies, per interval and pooled, that
PAS→temporary-crop origin totals + PAS→NAT origin totals + PAS→other residual
reconcile exactly to total PAS outflow, closing the accounting identity by
construction rather than by omission.

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

- replace all origin shares and temporal comparisons for both PAS→temporary
  crops and PAS→NAT, and report the PAS→other closure residual alongside
  them;
- reassess the direction and strength of the censored-to-post-1985 shift on
  each destination separately, noting whether the two destinations show
  consistent or divergent shifts;
- revise P9A035–P9A037;
- regenerate the relevant figure and evidence matrix rows.

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

The revision to `docs/methods/data_sources_and_classification.md` must
generalize its current "Pasture-origin classification" section, which is
scoped to `PAS→TMP` only, to state the identity for all three components
(PAS→temporary crops, PAS→NAT, PAS→other residual) established in Section 7
of this plan.

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
7. the origin components close exactly to the total PAS-outflow, both for
   PAS→temporary crops and PAS→NAT individually and for the PAS→other residual
   in aggregate;
8. all eight intervals contain 24,889 unique canonical cells;
9. non-age stocks and flows reconcile with version 1 within the accepted
   numerical tolerance;
10. corrected summaries reproduce their underlying cell-level totals;
11. primary and diagnostic periods remain separately identified;
12. every episode boundary triggered in 2024 or 2025 is flagged
    `boundary_adjacent`;
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

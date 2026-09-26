# Observed pasture-spell age and origin reconstruction

## Purpose

This method reconstructs the origin and consecutive observed age of each
current pasture spell from annual MapBiomas Collection 11 coverage. It replaces
direct analytical dependence on the public pasture-age codes after the source
asset was found to contain an unexpected value `1` and to reuse code `100`
after observed interruptions in pasture.

The output is a project-derived analytical variable. It is not a corrected or
republished MapBiomas product.

## Inputs

The reconstruction uses the 41 annual bands `classification_1985` through
`classification_2025` from:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

Processing must preserve the native CRS and affine transform recorded in
`docs/methods/data_sources_and_classification.md`. The public pasture-age asset
is used only for the source-impact comparison, not to derive the reconstructed
state.

## Observation categories

Each annual coverage observation is classified as one of:

| Observation | Definition |
|---|---|
| `PAS` | Coverage class 15 |
| `confident_non_pas` | Valid NAT, TMP, OAG, OUT, or WATER class |
| `uncertain` | NODATA, masked, or unexpected coverage value |

An uncertain observation is not treated as proof of either pasture persistence
or pasture exit.

## Reconstructed states

| State | Meaning |
|---|---|
| `not_pasture` | Current year is confidently observed non-PAS |
| `initial_1985_continuous_stock` | PAS has been observed continuously from 1985 through the current year |
| `post_1985_observed_entry` | Current pasture spell began after a confidently observed non-PAS year |
| `unresolved_episode_origin` | Current PAS spell cannot be connected either to 1985 or to a confirmed non-PAS→PAS entry because its backward history crosses uncertainty |

The annual observation status `uncertain` is retained separately from the
pasture-origin states. It describes a missing or unreliable annual observation,
whereas `unresolved_episode_origin` describes a later PAS observation whose
spell origin cannot be attributed.

## Recurrence

### Initial year

For 1985:

- PAS becomes `initial_1985_continuous_stock`, auxiliary code `100`;
- confident non-PAS becomes `not_pasture`;
- uncertain coverage initializes an uncertain history.

### Subsequent years

For year `y > 1985`:

| Previous history | Current observation | Result |
|---|---|---|
| initial continuous spell | PAS | initial continuous spell; auxiliary `100` |
| post-1985 spell with age `a` | PAS | post-1985 spell; auxiliary `a + 1` |
| unresolved spell | PAS | unresolved spell |
| confident non-PAS | PAS | post-1985 observed entry; auxiliary `201` |
| uncertain history | PAS | unresolved spell |
| any pasture spell | confident non-PAS | `not_pasture`; current spell terminates |
| uncertain history | confident non-PAS | `not_pasture`; uncertainty resets |
| any history | uncertain | annual observation `uncertain`; continuity becomes unverified |

Thus, a gap may produce an unresolved pasture spell, but uncertainty is not
permanent. If a confidently observed non-PAS year occurs after the gap, the
next PAS year is again an attributable observed entry with auxiliary code
`201`.

## Required synthetic tests

| Coverage sequence | Expected auxiliary sequence |
|---|---|
| `PAS, PAS, PAS` from 1985 | `100, 100, 100` |
| `PAS, PAS, TMP, PAS, PAS` | `100, 100, NA, 201, 202` |
| `NAT, PAS, PAS, NAT, PAS` | `NA, 201, 202, NA, 201` |
| `PAS, NAT, PAS, NAT, PAS` | `100, NA, 201, NA, 201` |
| `PAS, NODATA, PAS` | `100, uncertain, unresolved` |
| `TMP, PAS, NODATA, PAS` | `NA, 201, uncertain, unresolved` |
| `NODATA, PAS, PAS` | `uncertain, unresolved, unresolved` |
| `NODATA, PAS, NAT, PAS` | `uncertain, unresolved, NA, 201` |
| `PAS, NODATA, PAS, NAT, PAS` | `100, uncertain, unresolved, NA, 201` |

The implementation must also prove that reconstructed code `1` never occurs,
`100` cannot reappear after interruption, and each current PAS pixel receives
exactly one mutually exclusive origin state.

## Five-year origin attribution

For endpoint flow `PAS(t0)→D(t1)`, origin is the reconstructed pasture-spell
state at `t0`. This definition is deliberately fixed before inspecting
within-interval annual events.

For RQ2, `D = TMP`. The required partition is:

```text
PAS→TMP total =
    left-censored continuous 1985 episode
  + observed post-1985 entry episode
  + unresolved episode origin
```

The same partition is calculated for PAS→NAT as a supplementary diagnostic.
It does not redefine RQ2. OAG, OUT, and WATER are retained as other observed
destinations for full stock closure.

An episode that begins and ends inside `[t0, t1]` may be described in an annual
pathway product, but it does not replace the origin state of the PAS stock
observed at `t0`.

## Destination and observation closure

Origin closure is required separately for every PAS destination. Observed
outflows and observation loss are then reconciled as follows:

```text
observed PAS outflow = PAS→TMP + PAS→NAT + PAS→OAG + PAS→OUT + PAS→WATER

PAS endpoint non-persistence =
    observed PAS outflow
  + PAS→NODATA
  + PAS→unexpected
  + PAS→masked

PAS stock at t0 = PAS→PAS persistence + PAS endpoint non-persistence
```

For presentation only, the three auxiliary observed destinations may be
grouped as `PAS→other_observed`, and the three observation-loss destinations
as `PAS→observation_loss`. These groups remain analytically distinct.

## Boundary events

Entry or termination triggered in 2024 or 2025 must retain:

- event type;
- triggering year; and
- a boundary-adjacent flag.

Acceptable fields include `entry_boundary_adjacent_<year>`,
`termination_boundary_adjacent_<year>`, and `episode_boundary_year`, or an
equivalent long event table. This qualification is separate from unresolved
origin: a boundary event can be attributable and still carry reduced temporal-
filter support.

## Source-impact audit

The public pasture-age asset remains necessary to quantify the defect. The
audit must report, by year and relevant geography:

- source `100` conflicting with reconstructed post-1985 entry;
- source code `1`;
- overlap between those populations;
- number and duration of affected re-entry episodes;
- affected canonical cells;
- first and last occurrence years; and
- unresolved reconstructed histories caused by uncertain coverage.

These are source-discrepancy diagnostics, not alternative analytical origin
classes.

## Pilot and full processing

The implementation sequence is:

1. run the state engine on synthetic cases;
2. benchmark a small spatial subset;
3. run the source-impact audit;
4. process a 2015–2020 pilot;
5. verify origin and endpoint closure and invariance of non-origin fields;
6. process all eight intervals; and
7. rebuild only products that depend on the corrected origin variable, unless
   the invariance gate detects a wider change.

The pilot interval does not exercise 2024–2025 boundary flags. Those are tested
when the full 2020–2025 interval is processed.

## Interpretation

Use:

- **left-censored continuous 1985 pasture episode**;
- **pasture episode with observed post-1985 entry**; and
- **unresolved episode origin**.

Do not describe the reconstructed variable as the complete historical age of
pasture, as evidence of first-ever establishment at a pixel, or as an official
correction to the MapBiomas product. It measures the current observed pasture
spell within the 1985–2025 observation window.

## Validation products not yet available

The following records are created only after computation and are not part of
the pre-implementation documentation package:

```text
docs/validation/canonical_pasture_spell_age_validation_v1.md
docs/validation/pasture_age_source_asset_impact_audit_v1.md
```

Their absence at this stage is intentional.

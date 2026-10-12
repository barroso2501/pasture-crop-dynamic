# Data sources and analytical classification

## Purpose

This document defines the canonical land-cover inputs, temporal coverage,
spatial grid, class groups, reconstructed pasture-spell origin, and area
calculation conventions for the project.

Authoritative processing must use the sources and definitions recorded here,
in `config/constants.js`, and in the applicable decision records. Historical
results produced from a pre-release MapBiomas asset or from direct pasture-age
source codes are retained only for provenance and impact comparison.

## Canonical MapBiomas inputs

### Annual land cover

The analytical land-cover authority is the final public MapBiomas Brazil
Collection 11 coverage product:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

It is a multiband `ee.Image` with annual bands named
`classification_<year>` for 1985–2025. Scripts must select those names
explicitly, verify all 41 expected bands, and must not silently fall back to a
pre-release `classification-ft` asset.

### Public pasture-age product: provenance and audit status

The public source product is:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_pasture_age_v1
```

It uses the same native pixel grid as the coverage product and remains an
important provenance source. It is no longer the analytical authority for
pasture-spell origin or age.

Two independent anomalies motivate that restriction:

1. raw value `1` occurs where annual coverage identifies pasture, although it
   is not part of the expected project age encoding; and
2. code `100` can reappear after an observed non-pasture interruption, causing
   a post-1985 pasture spell to resemble continuous membership in the
   left-censored 1985 stock.

Coverage class `15` remains authoritative for pasture membership. The source
pasture-age asset is retained for the quantitative impact audit, including the
frequency, area, spatial distribution, and overlap of code `1` and code-`100`
reuse. It must not determine corrected PAS-outflow origin shares.

This rule supersedes the direct source-code origin attribution described in
earlier versions of this document and in Decisions 003 and 020. Those records
remain immutable provenance for the previously accepted workflow.

### Project-derived observed pasture-spell origin

Pasture origin is reconstructed from annual coverage according to Decision 024
and `docs/methods/observed_pasture_spell_age_reconstruction.md`.

The mutually exclusive current-PAS states are:

| State | Definition |
|---|---|
| `initial_1985_continuous_stock` | PAS observed continuously from 1985 through the reference year; left-censored at the start of the series |
| `post_1985_observed_entry` | Current PAS spell began after a confidently observed non-PAS year |
| `unresolved_episode_origin` | Current PAS spell cannot be attributed because its backward history crosses NODATA, masked, or unexpected coverage before reaching either 1985 or a confirmed non-PAS→PAS entry |

The auxiliary sequence may use `100` for the uninterrupted left-censored spell,
`201` for the first PAS observation after a confirmed non-PAS year, and `202+`
for consecutive continuation. These are project-derived values and must not be
presented as corrected official MapBiomas codes.

Any observed PAS→NAT, PAS→TMP, PAS→OAG, PAS→OUT, or PAS→WATER transition
terminates the current pasture spell. NODATA, masked, and unexpected coverage
break observed continuity but do not prove termination. A later confident
non-PAS observation resets uncertainty, allowing a subsequent PAS year to begin
again at `201`.

## Historical source retained for provenance

Exploratory processing used the pre-release Collection 11 working asset:

```text
projects/mapbiomas-brazil/assets/LAND-COVER/COLLECTION-11/
INTEGRATION/classification-ft
```

with working version `0-4-13-w3y-5`. It is not acceptable for final repository
outputs or manuscript results. Historical outputs may be used only to measure
changes introduced by source replacement.

## Temporal framework

The reference years are:

```text
1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025
```

They define eight five-year intervals from 1985–1990 through 2020–2025. The
primary inferential period is 1985–2020. The 2020–2025 interval remains fully
processed and explicitly flagged as the diagnostic temporal-boundary interval.

The 1985 state is the earliest observed state, not the origin of the land-use
process. A continuous pasture spell present in 1985 is left-censored. Episode
entry or termination triggered in 2024 or 2025 must retain event type and year
and be flagged as boundary-adjacent because the reconstruction inherits the
coverage product's temporal-edge limitations.

Annual bands inside each five-year interval support trajectory analyses, but
the origin of an endpoint flow `PAS(t0)→D(t1)` is fixed by the reconstructed
pasture state at `t0`.

## Spatial grid and projection

The canonical coverage grid is:

```text
CRS: EPSG:4326
Transform:
[0.00026949458523585647, 0, -74.02073025380652,
 0, -0.00026949458523585647, 5.405791885246045]
```

All pixel-level Boolean operations must preserve this alignment. Canonical area
reductions specify `crs` and `crsTransform`; a generic `scale: 30` is not an
acceptable substitute. Pixel area is obtained from `ee.Image.pixelArea()` and
converted from square metres to hectares by division by 10,000.

## Analytical class groups

| Group | Meaning | MapBiomas codes |
|---|---|---|
| `NAT` | Native vegetation | 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 29, 32, 49, 50, 84 |
| `PAS` | Planted pasture | 15 |
| `TMP` | Temporary crops | 19, 20, 39, 40, 41, 62 |
| `OAG` | Mosaic and other agricultural uses | 9, 21, 35, 36, 46, 47, 48 |
| `OUT` | Other anthropogenic, non-vegetated, or non-focal uses | 22, 23, 24, 25, 30, 75, 91 |
| `WATER` | Water-related classes | 26, 31, 33 |
| `NODATA` | Not observed | 27 |

`Temporary crops` is the required human-readable English label for TMP.
`Temporary agriculture` must not be used because it can imply that agriculture
itself is temporary rather than identifying annual or seasonal crop classes.
Stable machine names such as `nat_tmp_endpoint_ha` remain unchanged.

## Internal reclassification codes

| Internal value | Group |
|---:|---|
| 1 | `NAT` |
| 2 | `PAS` |
| 3 | `TMP` |
| 4 | `OAG` |
| 5 | `OUT` |
| 6 | `WATER` |
| 0 | `NODATA` or unexpected code |

Unexpected values must first be detected and reported. They must not be
silently accepted as valid NODATA, even if the compact raster uses value `0`
for downstream representation.

## Interpretation of class groups

### Native vegetation

`NAT` combines forest, savanna, grassland, wetland, and other native
formations. It does not support conclusions requiring those formations to be
distinguished. PAS↔NAT transitions may be sensitive to confusion between
planted pasture and native grassland and require that limitation to be stated.

### Mosaic and other agricultural uses

`OAG` remains separate rather than being forced into PAS or TMP. It is needed
to close initial-stock destinations while preserving its ambiguous and
heterogeneous land-use meaning.

### Water and other uses

`WATER` remains separate from `OUT` because it has a distinct interpretation
and contributes separately to domain and endpoint rules.

### Observation loss

Class 27, masked pixels, and unexpected codes are represented explicitly in
validation and closure calculations. They are observation conditions, not
substantive land-cover destinations.

## Core transition notation

Directed transitions are written `ORIGIN→DESTINATION`. Principal flows are:

- `NAT→PAS`: pasture-stock replenishment;
- `PAS→TMP`: pasture-to-temporary-crop conversion;
- `NAT→TMP`: within-interval native-to-temporary-crop endpoint transition;
- `PAS→NAT`: pasture-to-native-vegetation endpoint transition;
- `TMP→PAS`: temporary-crop-to-pasture endpoint transition; and
- `TMP→NAT`: temporary-crop-to-native-vegetation endpoint transition.

Persistence and auxiliary destinations are retained wherever needed for stock
closure. `NAT→TMP` is an endpoint transition and is not automatically a direct
conversion because intervening annual states may occur.

## Pasture-origin classification for endpoint flows

For `PAS(t0)→D(t1)`, origin is the reconstructed pasture-spell state at `t0`.
The required destination-specific identity is:

```text
PAS→destination total =
    initial continuous origin
  + post-1985 observed-entry origin
  + unresolved origin
```

RQ2 uses this partition for `D = TMP`. The PAS→NAT partition is a supplementary
diagnostic and does not expand RQ2. An annual re-entry occurring after `t0` does
not replace the endpoint-flow origin fixed at `t0`.

Observed PAS outflow and observation loss close separately:

```text
observed PAS outflow = PAS→TMP + PAS→NAT + PAS→OAG + PAS→OUT + PAS→WATER

PAS endpoint non-persistence =
    observed PAS outflow
  + PAS→NODATA
  + PAS→unexpected
  + PAS→masked

PAS stock at t0 = PAS→PAS persistence + PAS endpoint non-persistence
```

OAG, OUT, and WATER may be summarized as `PAS→other_observed`. NODATA,
unexpected, and masked may be summarized as `PAS→observation_loss`. They must
remain distinguishable in canonical outputs.

## Fixed 1985 cohort versus current pasture spell

The RQ1 fixed cohort and the reconstructed current pasture spell are different
objects. A pixel classified as PAS in 1985 remains a member of the fixed RQ1
pixel cohort throughout follow-up, whatever its later class. If it leaves PAS
and later returns, its new current pasture spell is classified as an observed
post-1985 entry for RQ2. Cohort membership does not restore left-censored spell
status.

## Source and mask validation

Before corrected products are accepted, the pipeline must verify:

1. exact presence and chronological order of all 41 coverage bands;
2. native CRS, transform, and pixel alignment;
3. presence of only expected land-cover codes, with unexpected values reported;
4. complete coverage of the fixed 24,889-cell analytical domain;
5. one and only one reconstructed origin state for every current PAS pixel;
6. no reconstructed code `1` and no reappearance of `100` after interruption;
7. correct restart at `201` after observed non-PAS→PAS entry;
8. explicit unresolved status after uncertain histories;
9. source-code `1` and code-`100`-reuse audits, including their overlap;
10. separate observed-destination and observation-loss closure;
11. correct 2024–2025 event-year boundary flags; and
12. invariance of all non-origin stocks and flows within accepted tolerances.

## Reprocessing and provenance

Corrected products use new versioned filenames. Accepted earlier products are
not overwritten and remain available to document the impact of the change.

The suspensions of P9A035–P9A037 were rescinded on 2026-10-08 only for
the corrected matrix-v4 statements, through new immutable events. The retired
source-age statements remain superseded. Current manuscript-facing evidence
is matrix v4.3, incorporating the accepted 1985/1995/2000 window sensitivity
into P9A035/P9A036 while preserving P9A037 and the other findings. The
2026-10-09 erratum remains historical provenance. The technical closure
and its assurance limits are recorded in
`docs/decisions/024_implementation_closure_v2.md`. Historical events and
validation JSONs retain their original statuses. Events-v3 supplied structured
validation references and the interpretation amendments; events-v4 preserved its entire byte sequence and appended two supplementary-evidence events. Current events-v5 preserves all ten events-v4 rows and appends two endpoint-fraction events.
No qualified status is promoted. See
`docs/results/rq2_evidence_consolidation_v4_2.md`.

## Observation-window dependence of RQ2 origin composition

1985 is the earliest observed state, not a process origin (Decision 022).
For the 1985–1990 endpoint flow, origin is assigned at t0=1985, so every
observed PAS origin belongs to the initial category: its 100% share is true
by construction, subject to numerical area-reduction precision. That first
bar is not evidence for a historical predominance of old over new pastures.

Membership in the uninterrupted 1985 spell can only be lost through time.
Its share among PAS→TMP conversions, however, can increase or decrease:
the denominator and conversion selection also change between intervals.
A finite-duration stationary renewal process can generate a declining
baseline-origin component without a temporal change in the process. The
observed share trajectory alone cannot separate these explanations.

The first observed-entry share above 50% in 2000–2005 is a statistic of
this observation window, not an identified process threshold. Primary
pooled shares 46.91%/53.09% also depend on the window start, its length,
and interval conversion weights. Re-entry is included in observed entry;
neither category identifies first-ever pasture establishment. The 1985/1995/2000
rebasing sensitivity has been executed and validated on the fixed 24,889-cell
domain. On identical 2000–2020 conversions, initial shares are 38.10%, 64.70%
and 78.07%, respectively. First-20-year pooled shares are 63.64%, 72.25% and
78.07%, with different calendar periods and baseline populations. The first
primary >50% entry crossing occurs in 2000–2005 only under b=1985; the later
windows cross only in separately diagnostic 2020–2025. These results qualify
origin composition as window-dependent and do not identify an artifact
fraction, stationarity, physical establishment age or a process threshold.
The first-observed-entry/re-entry decomposition remains unperformed. Native
categorical fixtures and field invariants passed; auxiliary numerical age 201
and unrelated boundary-raster checks are not included in this execution.
The executed method is `docs/methods/window_origin_sensitivity_v2.md`.

## Meaning of boundary-event uncertain-pair area

For event year y, `uncertain_pair_ha` is the area of pixels for which either
coverage(y−1) or coverage(y) is NODATA, masked, or unexpected, preventing a
confident PAS/non-PAS pair classification. Equivalently, it is the complement
of the union of valid entry, valid termination, PAS→PAS, and non-PAS→non-PAS
pairs, within the canonical cell reductions. It covers all land-cover states,
not only pixels with a PAS endpoint. It is a shared pair-quality denominator
and is repeated in the entry and termination summary rows; those repetitions
must not be added as independent areas.

The 2024 pair is 2023/2024 and has 4,688,518.25661 ha; the 2025 pair is
2024/2025 and has 4,688,463.67044 ha. They are identical across event types
within a year, not exactly identical between years (difference 54.58617 ha).
These values do not measure unresolved PAS-origin area. `pas_observation_loss_ha`
instead conditions on PAS at a five-year interval start and an unobserved
interval-end coverage. It uses a different population and different dates;
the 2020/2025 PAS observation-loss area is 32.743600 ha. Large pair uncertainty
and small PAS endpoint loss therefore are not contradictory. The hypothesis
that most uncertain-pair pixels are non-PAS has not been quantified: a
pair-level cross-tabulation of previous/current PAS membership is needed
before making that assertion. Spatial overlap across the two annual pairs
is also not measured by the repeated summary numbers.

## Execution and invariance assurance

The closure uses exact production-source categorical logic under a local
scalar adapter and source checks, accepted GEE export records, and cell-level
accounting. It is not a fresh native GEE synthetic run or an independent
all-pixel audit of criteria 3 and 5. The versioned panel gate preserved
non-origin fields along the accepted chain, including retained downstream
fields where present; NAT→TMP and TMP→* raster flows were not independently
re-exported, and phases 2–8 were not rerun during remediation. Future GEE runs
must retain the exact executed script snapshot and SHA-256, repository path,
commit when available, constants snapshot, run identifier and export hashes.
Current-source hashes must not retrospectively substitute for missing
historical execution hashes.

## Evidence edition synchronization — 2026-10-12

The current governing evidence edition is matrix v4.3 and cumulative events-v5; matrix v4.2/events-v4 are preceding editions. The
pre-update normative text is archived unchanged under
`docs/history/rq2_pre_consolidation_v4_2/docs/methods/`. The core classification,
assets, masks and origin estimator are unchanged. The completed sensitivity
and documentary consolidation do not reexecute phases 2–8 or declare the
public data/DOI release complete.

## Stock-normalized endpoint fractions — v4.3

Origin composition combines class-stock composition and per-stock endpoint conversion fractions. At t0, define f_o=C_o/S_o and R=f_initial/f_entry from national sums. The first entry-stock-zero interval has undefined R. These are descriptive five-year endpoint fractions, not annual rates or exposure-integrated hazards; unresolved origin is retained separately. The algebraic identity C_initial/C_entry=(S_initial/S_entry)R does not identify a causal contribution. Calendar-paired monotonicity of initial shares follows set nesting. Follow-up and stock/conversion comparisons also change periods/cohorts and do not isolate a mechanical artifact fraction. The unchanged canonical definitions and the new derivative are documented in `docs/methods/relative_endpoint_conversion_fractions_v1.md`.

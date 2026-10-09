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

The affected findings P9A035–P9A037 remain suspended until the reconstructed
pilot and full series pass the approved acceptance criteria. A successful run
will create new validation and impact-audit records and a new versioned status
event rescinding the suspension. It will not modify the accepted suspension
event in place.

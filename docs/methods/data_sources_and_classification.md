# Data sources and analytical classification

## Purpose

This document defines the canonical land-cover inputs, temporal coverage, spatial grid, class groups, pasture-age encoding, and area-calculation conventions for the project.

All authoritative processing must use the sources and definitions recorded here and in `config/constants.js`. Historical results produced with a pre-release MapBiomas asset are retained only as regression references and must be reproduced with the final public Collection 11 product.

## Canonical MapBiomas inputs

### Annual land cover

The canonical land-cover source is the final public MapBiomas Brazil Collection 11 coverage product:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

The asset is loaded as a multiband `ee.Image`. Annual bands follow the convention:

```text
classification_<year>
```

The analytical series covers 1985–2025.

No `ImageCollection` filtering, tile casting, or mosaicking is required for this canonical source. Scripts must not silently fall back to the pre-release `classification-ft` asset.

### Pasture age

The canonical pasture-age source is:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_pasture_age_v1
```

The pasture-age asset uses the same native pixel grid as the Collection 11 coverage product.

The project uses the following encoding:

- `100`: pasture present in 1985, defining the initial pasture cohort;
- `2xx`: pasture age encoded as `200 + age in years`.

The value `100` identifies pasture already present at the first observation. Its precise establishment date is left-censored and is not observed by the series. It should therefore be described as the **initial 1985 pasture stock** or **left-censored pasture cohort**, rather than assigned a specific pre-1985 establishment year.

Annual pasture-age bands are selected by their zero-based position from 1985 unless a stable official band-name convention is confirmed and documented.

## Historical source retained for provenance

Exploratory processing used the pre-release Collection 11 working asset:

```text
projects/mapbiomas-brazil/assets/LAND-COVER/COLLECTION-11/
INTEGRATION/classification-ft
```

with working version:

```text
0-4-13-w3y-5
```

This asset was used before the official release of Collection 11. It is not an acceptable source for final repository outputs or manuscript results.

All calculations derived from it must be rerun with `mapbiomas_brazil_collection11_coverage_v3`. Historical outputs may be used to quantify changes introduced by the source replacement, but they must not be mixed with canonical outputs.

## Temporal framework

The reference years are:

```text
1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025
```

They define eight five-year intervals:

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

The primary inferential period is 1985–2020. The 2020–2025 interval will be processed for completeness and diagnosis but will not support the principal conclusions while endpoint filtering effects remain a concern.

Annual bands within each five-year interval are used for the within-interval trajectory analysis.

## Spatial grid and projection

Coverage and pasture-age products use the same native grid. All pixel-level Boolean operations between them must preserve this alignment.

The canonical grid parameters are:

```text
CRS: EPSG:4326
Transform:
[0.000269494585235856472, 0, -180,
 0, -0.000269494585235856472, 90]
```

Area reductions must specify `crs` and `crsTransform`. A generic `scale: 30` must not replace the native transform in canonical scripts because it does not fully specify pixel alignment.

Pixel area is obtained from `ee.Image.pixelArea()` and converted from square metres to hectares by division by 10,000.

## Analytical class groups

The detailed MapBiomas Collection 11 legend is aggregated into the following project classes.

| Group | Meaning | MapBiomas codes |
|---|---|---|
| `NAT` | Native vegetation | 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 29, 32, 49, 50, 84 |
| `PAS` | Planted pasture | 15 |
| `TMP` | Temporary agriculture | 19, 20, 39, 40, 41, 62 |
| `OAG` | Mosaic and other agricultural uses | 9, 21, 35, 36, 46, 47, 48 |
| `OUT` | Other anthropogenic, non-vegetated, or non-focal uses | 22, 23, 24, 25, 30, 75, 91 |
| `WATER` | Water-related classes | 26, 31, 33 |
| `NODATA` | Not observed | 27 |

These lists are definitive for the current Collection 11 analysis. No valid Collection 11 code is known to be absent from the classification scheme.

## Internal reclassification codes

When a compact categorical raster is required, the project uses:

| Internal value | Group |
|---:|---|
| 1 | `NAT` |
| 2 | `PAS` |
| 3 | `TMP` |
| 4 | `OAG` |
| 5 | `OUT` |
| 6 | `WATER` |
| 0 | `NODATA` or unexpected code |

Unexpected source values must be detected by an audit before processing. They must not be silently accepted as valid `NODATA`.

## Interpretation of the groups

### Native vegetation

`NAT` intentionally combines forest, savanna, grassland, wetland, and other native formations. This aggregation matches the stock-and-flow question but does not support conclusions that require distinguishing forest from open native vegetation.

In particular, transitions between planted pasture and native grassland may be sensitive to classification confusion. Analyses of `PAS→NAT` or `NAT→PAS` must recognize this limitation or use a parallel disaggregated diagnostic.

### Mosaic and other agricultural uses

`OAG` is retained as an auxiliary category rather than merged with pasture or temporary agriculture. It contains ecologically and operationally different land uses, including mosaic class 21, and is required to close stock destinations without forcing ambiguous pixels into a focal class.

### Water and other uses

`WATER` remains separate from `OUT` because water contributes to the endpoint rule used to define fully natural cells in the analytical domain and has a distinct spatial interpretation.

### Not observed

Class 27 and masked pixels must be represented explicitly in validation and closure calculations. Absolute and changing amounts of unobserved area must not be absorbed into a substantive land-cover group.

## Core transition notation

Directed transitions are written as `ORIGIN→DESTINATION`. The principal focal flows are:

- `NAT→PAS`: pasture expansion or replenishment;
- `NAT→TMP`: endpoint conversion from native vegetation to temporary agriculture;
- `PAS→TMP`: agricultural consolidation over pasture;
- `PAS→NAT`: transition from pasture to native vegetation;
- `TMP→PAS`: transition from temporary agriculture to pasture;
- `TMP→NAT`: transition from temporary agriculture to native vegetation.

Persistence and auxiliary destinations must be retained wherever required to close a stock accounting identity.

## Pasture-origin classification

For a `PAS→TMP` pixel in interval `[t0, t1]`, the pasture-age value at `t0` defines its observed origin class:

- `age(t0) = 100`: member of the left-censored 1985 pasture cohort still present as pasture at `t0`;
- `age(t0) > 200`: pasture established during the observed series with an attributable age;
- no valid age value: pasture without attributable age.

The required identity is:

```text
PAS→TMP total = censored origin + new-pasture origin + unattributed-age origin
```

No component may be inferred solely by omission without also being exported or audited explicitly.

## Source and mask validation

Before producing analytical outputs, the canonical pipeline must verify:

1. expected coverage bands from 1985 through 2025;
2. expected pasture-age band count and ordering;
3. identical native projections and transforms;
4. presence of only expected land-cover codes;
5. agreement between `PAS` in the coverage product and the valid pasture-age mask;
6. frequency and spatial distribution of pasture without attributable age;
7. treatment of class 27 and masked pixels;
8. use of the complete fixed analytical domain before process-specific filtering.

## Reprocessing and regression comparison

Every historical calculation based on `classification-ft` must be regenerated from the final public coverage product. For each reconstructed output, the project will compare the new and historical results using, as applicable:

- total area by field and interval;
- absolute and percentage differences;
- cell-level differences by `cell_id`;
- changes in accounting residuals;
- changes in temporal ordering or spatial patterns;
- differences in the selected analytical domain, if the historical domain used the pre-release asset.

Small differences do not invalidate the analysis, but all final reported values must originate from the canonical public inputs.


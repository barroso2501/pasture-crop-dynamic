# Study domain

## Purpose

This document describes the spatial unit and the construction of the fixed analytical domain used to study native vegetation, planted pasture, and temporary agriculture in the Brazilian Cerrado and Amazon.

The analytical domain was originally produced in ArcGIS Pro through attribute and spatial selection. The procedure described here records that historical workflow as it was performed. A scripted implementation may later reproduce the same logical rule and verify its agreement with the original layer.

## Spatial reference data

### Brazilian biome boundaries

The spatial reference was the **2025 Brazilian biome shapefile produced by the Brazilian Institute of Geography and Statistics (IBGE)**.

The Cerrado and Amazon features were selected from this layer and used to identify the grid cells belonging to the study region.

### Parent grid

The parent spatial framework was a regular hexagonal grid constructed for the Brazilian territory. Each cell has an area of approximately **20,000 ha** and a unique `cell_id`.

The hexagons are the accounting units of the analysis. Land-cover areas and transitions are aggregated over complete cells rather than interpreted as individual pixel trajectories.

## Historical ArcGIS Pro procedure

### Step 1 — Cerrado–Amazon spatial selection

The `Cerrado` and `Amazônia` features were selected from the 2025 IBGE biome layer.

ArcGIS Pro's **Select Layer By Location** operation was then applied using the `INTERSECT` relationship. Every parent-grid hexagon intersecting either selected biome was retained as a candidate cell.

Formally, if \(G_0\) is the parent grid and \(B_{CA}\) is the union of the Cerrado and Amazon biome polygons, the candidate set is:

\[
G_{CA}=\{h\in G_0:h\cap B_{CA}\neq\varnothing\}.
\]

The selected hexagons were **not clipped** to the biome boundaries. A boundary hexagon remains a complete 20,000 ha accounting unit and may contain land outside the Cerrado or Amazon.

### Step 2 — Endpoint land-cover calculation

MapBiomas Brazil Collection 11 land-cover data were used for the endpoint years **1985** and **2025**.

For every candidate hexagon, the areas classified as native vegetation and water were summed over the full cell area:

\[
NW_y(h)=NAT_y(h)+WATER_y(h),
\]

where \(y\) is 1985 or 2025.

The canonical class groups currently used by the project are:

- native vegetation: `1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 29, 32, 49, 50, 84`;
- water: `26, 31, 33`.

These lists must remain synchronized with the canonical class-remapping configuration used by the processing pipeline.

The denominator was the **total area of the complete hexagonal cell**, not only the area assigned to a particular biome and not a biome-clipped portion of the cell.

### Step 3 — Exclusion of fully natural cells

A candidate cell was excluded only when native vegetation plus water represented 100% of its area in **both** endpoint years:

\[
EXCLUDE(h)=
\left[NW_{1985}(h)=AREA(h)\right]
\land
\left[NW_{2025}(h)=AREA(h)\right].
\]

The final analytical domain is therefore:

\[
D=\left\{h\in G_{CA}:
NW_{1985}(h)<AREA(h)
\lor
NW_{2025}(h)<AREA(h)
\right\}.
\]

The resulting layer is `grade_hex_CeAmz_selecao`, containing approximately **21,869 cells**.

## Interpretation of the domain

The domain contains cells with land cover other than native vegetation or water in at least one endpoint year. It is best described as a:

> Fixed Cerrado–Amazon analytical domain with anthropogenic land-cover presence at either endpoint.

It should not be described as a set containing only cells with land-cover change. A cell may remain in the domain even if its anthropogenic cover is stable between 1985 and 2025.

The domain definition also should not be confused with pixel-level alternation. Pixel trajectories and annual class changes are analyzed separately from the cell-level rule used to establish the study domain.

## Fixed domain and time-varying activity

The 21,869-cell domain is fixed for all analytical periods. Every cell should be retained in the balanced analytical panel, including intervals in which its measured flows are zero.

Within this fixed domain, process-specific activity may vary among five-year intervals. Separate analytical subsets may identify cells with:

- native vegetation to pasture flow;
- native vegetation to temporary agriculture flow;
- pasture to temporary agriculture flow;
- any focal transition;
- no focal transition during the interval.

A cell with `PAS→TMP > 0` belongs to the consolidation-active subset for that interval. This subset is not equivalent to the complete domain or to the set of cells with any form of activity.

## Boundary-cell implications

Because cells were selected by intersection and retained as complete hexagons:

- some boundary cells contain areas outside the Cerrado or Amazon;
- biome boundaries determine cell inclusion but do not mask the internal accounting area;
- total cell-level estimates refer to the selected hexagonal lattice, not to an exact polygon-clipped biome area;
- comparisons among alternative grids must apply the same intersection and full-cell accounting rules.

Biome composition may later be included as a cell attribute or covariate. It should not be inferred from the selection operation alone.

## Reproducibility requirements

A future scripted reconstruction of the domain must document and fix:

1. the exact 2025 IBGE biome layer and its spatial reference;
2. the parent-grid asset and unique identifier field;
3. the `INTERSECT` spatial-selection rule;
4. the MapBiomas Collection 11 asset and product version;
5. the native vegetation and water class codes;
6. the cell-area calculation method and projection;
7. the numerical tolerance used to interpret 100% coverage;
8. the treatment of masked, unobserved, or unclassified pixels;
9. the expected final cell count;
10. agreement between the reconstructed domain and the original ArcGIS-derived layer.

## Validation checks

The domain is considered successfully reconstructed when:

- every output feature is a complete hexagonal polygon;
- `cell_id` is present and unique;
- every retained cell intersects the Cerrado or Amazon biome polygon;
- no excluded cell contains anthropogenic land cover in either endpoint under the canonical classification;
- the number of reconstructed cells matches the original domain, or every difference is explicitly explained;
- spatial disagreement with the original layer is reported by `cell_id` and mapped for inspection.

## Role in later analyses

This domain is the common spatial support for:

- five-year stock and flow accounting;
- the fixed 1985 pasture cohort;
- within-interval annual trajectory analysis;
- consolidation–replenishment balance metrics;
- spatial autocorrelation analysis;
- sensitivity tests for the modifiable areal unit problem (MAUP).

For MAUP tests, alternative zoning and cell-size configurations must repeat the same domain-selection logic so that differences can be attributed to the spatial support rather than to inconsistent inclusion criteria.


# Decision 001 — Fixed Cerrado–Amazon analytical domain

- **Status:** Accepted
- **Date recorded:** 2026-09-07
- **Scope:** Spatial domain and analytical population
- **Related method:** `docs/methods/study_domain.md`

## Context

The parent dataset is a regular hexagonal grid covering the Brazilian territory, with cells of approximately 20,000 ha. Processing the complete national grid would include extensive areas that are fully covered by native vegetation and water and do not belong to the land-use context addressed by this study.

The scientific analysis focuses on the native vegetation–pasture–temporary agriculture system in the Cerrado and Amazon. A fixed spatial domain was therefore required before calculating time-varying stocks and flows.

The original domain was constructed manually in ArcGIS Pro using the 2025 IBGE biome shapefile and MapBiomas Brazil Collection 11 endpoint land-cover data.

## Decision

The project will use `grade_hex_CeAmz_selecao` as its fixed reference domain. The layer contains approximately 21,869 complete hexagonal cells of about 20,000 ha.

A cell belongs to the domain when both conditions below are met:

1. it intersects the Cerrado or Amazon feature in the 2025 IBGE biome layer; and
2. it contains land cover other than native vegetation or water in 1985 or 2025.

Equivalently, a cell is excluded only when native vegetation plus water represents 100% of the complete cell area in both endpoint years:

\[
EXCLUDE(h)=
\left[NW_{1985}(h)=AREA(h)\right]
\land
\left[NW_{2025}(h)=AREA(h)\right].
\]

The spatial selection uses `INTERSECT`. Selected cells are not clipped to biome boundaries, and all subsequent accounting is performed over each complete cell.

## Terminology

The selected layer will be described as a:

> Fixed Cerrado–Amazon analytical domain with anthropogenic land-cover presence at either endpoint.

The term **dynamic domain** will be avoided when it implies that every included cell changed between 1985 and 2025. Stable anthropogenic cells may also belong to the domain.

The following populations will remain distinct:

- **fixed analytical domain:** all 21,869 selected cells;
- **interval-active cells:** cells with a defined focal flow during a particular interval;
- **consolidation-active cells:** cells with `PAS→TMP > 0` during a particular interval.

## Rationale

This decision:

- removes structural zero areas that are fully natural or water at both endpoints;
- retains cells with anthropogenic land cover at either endpoint;
- retains stable anthropogenic cells rather than selecting only observed transitions;
- defines the spatial support independently of whether consolidation occurs in a particular five-year interval;
- preserves equal-area, complete hexagons as the accounting units;
- separates domain definition from pixel-level trajectory and alternation analyses.

The domain is intended to represent the landscape in which the focal land-use system is present or can be observed, while time-varying activity is derived later from the transition accounting.

## Consequences

### Positive consequences

- The same spatial population can be used in every five-year interval.
- Zero-flow cells can be retained in a balanced panel.
- Stock trajectories can be compared without changes in the underlying cell population.
- Activity filters can be applied transparently during analysis rather than embedded in data export.
- MAUP and spatial autocorrelation analyses can use a documented reference support.

### Constraints and interpretation limits

- The domain is not an exact polygon-clipped Cerrado-plus-Amazon area.
- Boundary hexagons may contain land outside the two focal biomes.
- Cell-level results refer to complete selected hexagons.
- Use of 2025 in the domain definition must remain explicit even when 2020–2025 is excluded from the main inferential results.
- The original selection was performed manually and must not be described as script-generated.
- A reproducible implementation must define a numerical tolerance for 100% coverage and explicitly handle masked or unclassified pixels.

## Alternatives considered

### Full national parent grid

Rejected as the primary domain because it includes extensive structural-zero regions outside the focal Cerrado–Amazon land-use system and imposes unnecessary processing costs.

### Exact clipping to biome polygons

Not adopted because it would create irregular boundary units and abandon the complete equal-area hexagon as the accounting support.

### Cells with change between 1985 and 2025 only

Not adopted. The selected domain also retains cells with stable anthropogenic cover and therefore is not defined solely by endpoint change.

### Cells active in each five-year interval

Not adopted as the reference domain because the underlying cell population would change through time. Interval activity remains an analytical attribute within the fixed domain.

### Cells with `PAS→TMP > 0`

Not adopted as a general activity or domain definition. This criterion identifies only consolidation-active cells and is appropriate solely for analyses explicitly conditioned on consolidation.

## Implementation record

### Historical implementation

1. Construct or load the national 20,000 ha parent hexagonal grid.
2. Select `Cerrado` and `Amazônia` from the 2025 IBGE biome shapefile.
3. Select grid cells by location using `INTERSECT`.
4. Calculate native vegetation plus water area for 1985 and 2025 using MapBiomas Collection 11.
5. exclude cells with 100% native vegetation plus water in both years;
6. export the retained layer as `grade_hex_CeAmz_selecao`.

### Future reproducible implementation

A canonical script will reproduce this logic from the source layers. Its output will be compared with the historical ArcGIS-derived layer using cell counts, `cell_id` agreement, and spatial inspection of any discrepancies.

## Acceptance criteria

This decision is considered fully implemented in the reconstructed workflow when:

- the parent grid and source layers are versioned or uniquely identified;
- a script reproduces the documented logical rule;
- the output contains unique `cell_id` values and complete hexagons;
- the reconstructed output agrees with the historical 21,869-cell layer or all discrepancies are accounted for;
- every downstream interval export contains the complete fixed domain before analytical filtering;
- MAUP variants apply equivalent biome-intersection and endpoint-selection rules.

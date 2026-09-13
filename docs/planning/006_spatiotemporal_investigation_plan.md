# Spatiotemporal investigation plan

- **Status:** Approved; Phase 0 passed and Phase 1 is authorized
- **Date recorded:** 2026-09-12
- **Scope:** Spatial variation and temporal change in the canonical integrated panel
- **Canonical domain:** 24,889 Cerrado-Amazon hexagonal cells
- **Canonical panel:** `canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet`
- **Canonical panel SHA-256:** `7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28`

## Purpose

The preceding workflow established interval-level totals and distributions for
the complete study domain. This phase will determine where the measured
processes occur, whether their spatial configurations persist or move among
five-year intervals, and whether the observed patterns are robust to spatial
aggregation and zoning.

The plan defines the investigation horizon before additional processing. New
analyses must answer one of the questions below or be documented as an
explicit amendment to this plan.

## Primary questions

1. Where are consolidation, replenishment, native-to-temporary-crop
   transitions, and their balances concentrated in each five-year interval?
2. Do high- and low-intensity areas persist, intensify, weaken, reverse, or
   move between intervals?
3. Is the domain-level temporal pattern spatially widespread or driven by a
   limited set of cell clusters?
4. How do spatial patterns differ between the Cerrado and Amazon biomes?
5. Are cell values spatially autocorrelated, and where do significant local
   clusters and spatial outliers occur?
6. Are the principal findings stable under changes in cell size and grid
   zoning?

## Analytical scope and guardrails

- The analytical population remains the fixed set of 24,889 canonical cells.
- A zero process value is distinct from missing raster support.
- Pixel trajectories must not be interpreted as cell-level net balances, and
  cell-level balances must not be interpreted as individual pixel
  trajectories.
- Absolute areas and relative intensities answer different questions and will
  be reported separately.
- Relative metrics will use process-specific denominators rather than a single
  generic cell-area denominator.
- Map class limits will be fixed across intervals. Interval-specific quantile
  classes will not be used for temporal comparison.
- Global spatial autocorrelation will be evaluated before local cluster
  statistics.
- Global significance is not a mandatory gate for a prespecified local
  analysis because opposing local structures may cancel in the global
  statistic.
- The canonical grid provides the main results. MAUP analyses are robustness
  tests and will not redefine the primary result after inspection.
- No data-driven historical phases, clusters, or change points will be adopted
  without a separate documented analytical decision.
- The neighborhood graph for the complete canonical domain will be constructed
  once and held fixed across intervals. Analyses with incomplete metric
  support will inherit a documented subgraph rather than silently rebuild an
  unrelated neighborhood definition.

## Temporal scope

The primary analysis uses seven intervals:

```text
1985-1990
1990-1995
1995-2000
2000-2005
2005-2010
2010-2015
2015-2020
```

The `2020-2025` interval will initially remain a diagnostic extension. It will
be processed, mapped, and compared with the preceding intervals, but it will
not determine the primary temporal conclusions while the comparability of the
terminal 2025 map remains unresolved.

This designation is precautionary. It does not result from a failed accounting
check, an anomalous total, or the unresolved pasture-age code `1`. All
structural and accounting validations for `2020-2025` passed. The concern
recorded earlier in the project was that the final year of the source series
may not have the same temporal-filter support as internal years because no
subsequent observations are available.

The public Collection 11 documentation examined by the project has not yet
provided a specific confirmation that the 2025 coverage band is less filtered
or less suitable for inference. The diagnostic designation must therefore be
reassessed before manuscript inference. It may be removed if MapBiomas
documentation or direct technical clarification confirms equivalent treatment
and comparability of the terminal year.

## Phase 0 — Runtime configuration and upstream provenance

### Objective

Close the remaining provenance question about the Earth Engine module used by
the accepted canonical processing before investing in spatial derivatives.

### Required checks

1. Run a lightweight Earth Engine configuration audit that records the hosted
   module values for:
   - coverage and pasture-age assets;
   - canonical analytical grid;
   - expected cell count;
   - CRS;
   - affine transform; and
   - output version.
2. Compare the hosted values with `config/constants.js` in the repository.
3. Compare `K.CRS_TRANSFORM` with the native transform read directly from the
   Collection 11 `coverage_v3` image.
4. Reprocess only the `b00` 2005-2010 pilot with the native transform written
   explicitly in the verification script.
5. Compare every exported accounting metric by `cell_id` with the previously
   accepted `canonical_stock_flow_2005_2010_b00_v1.csv`.

### Acceptance gate

- hosted and repository configuration values match exactly;
- the hosted transform and explicit native coverage transform match exactly;
- the verification export contains the expected 3,168 `b00` cells with no
  duplicate or missing identifiers;
- cell-level accounting differences do not exceed `2e-6` ha; and
- no categorical, version, grid-membership, or interval metadata differs.

Failure of any condition pauses spatial implementation and triggers a decision
on targeted or complete upstream reprocessing. Passing the gate closes the
configuration-provenance issue without reopening accepted accounting logic.

### Implementation outcome

Phase 0 passed on 2026-09-12. The hosted module matched the repository and the
native coverage transform. The coverage and pasture-age products shared the
same lattice, with integer origin offsets of 76 pixels in X and 2,205 pixels
in Y. The explicit-native-transform `b00` replication was byte-identical to
the accepted pilot: all 3,168 cells, seven metadata fields, and 82 numeric
fields matched, with a maximum difference of `0.0` ha.

The configuration-provenance issue is closed, no upstream interval requires
reprocessing for this reason, and Phase 1 may begin. Evidence and the resulting
decision are recorded in:

```text
docs/validation/runtime_configuration_and_native_transform.md
docs/decisions/007_accept_canonical_outputs_after_transform_verification.md
```

## Phase 1 — Spatial support table

### Objective

Create one validated spatial reference table that can be joined to every row
of the integrated panel.

### Required content

- `cell_id` and `GRID_ID`;
- canonical polygon geometry;
- cell area;
- centroid coordinates for visualization and diagnostics;
- biome overlap area and fraction for Cerrado and Amazon;
- a documented primary-biome assignment, if categorical stratification is
  required;
- geometry and neighborhood quality-control fields.

The complete-domain contiguity graph will be created in this phase and reused
across periods. The graph record will include neighbor counts, connected
components, islands, symmetry checks, and the weight-standardization rule.

Cells crossing a biome boundary will retain their overlap fractions. A
dominant-biome label must not replace the fractional information in the
canonical spatial table.

### Acceptance gate

- exactly 24,889 unique `cell_id` values;
- one geometry per cell;
- no unmatched panel cells;
- valid geometries and documented handling of any islands;
- biome fractions reconcile with the relevant cell area within tolerance.

## Phase 2 — Spatial metrics

The following minimum set will be calculated for each cell and interval.

| Process | Absolute metric | Relative metric | Primary denominator |
|---|---|---|---|
| Consolidation | `consolidation_ha` | consolidation intensity | initial pasture area |
| Replenishment | `replenishment_ha` | replenishment intensity | initial native area |
| Native to temporary crops | `nat_tmp_endpoint_ha` | NAT-TMP intensity | initial native area |
| C-R balance | `net_cr_balance_ha` | `cr_balance_index` | gross C-R activity |
| Intermediate pasture | trajectory area | trajectory share | NAT-TMP endpoint area |

Valid raster support and denominator size will be retained as quality-control
variables. Undefined ratios will remain undefined rather than being replaced
with zero.

### Spatial-support strategy

Spatial analysis will use a two-part design.

#### Complete-domain component

Variables defined for all 24,889 cells will use the fixed complete-domain
neighborhood graph. They include:

- occurrence of consolidation;
- occurrence of replenishment;
- occurrence of any C-R activity;
- `gross_cr_activity_ha`;
- `net_cr_balance_ha`; and
- occurrence and absolute area of `NAT->TMP`.

Zero is retained as an observed absence of the measured process.

#### Conditional component

`cr_balance_index` is defined only where gross C-R activity is positive. A
missing balance index must not be recoded as zero because zero represents
equal positive consolidation and replenishment, whereas missing represents an
undefined balance with no activity.

Conditional balance analysis will therefore:

- retain inactive cells as a separate map category;
- use only active cells for numerical balance summaries;
- inherit the active-cell subgraph from the complete contiguity graph;
- avoid automatic k-nearest-neighbor connections across inactive gaps;
- report active sample size, connected components, islands, and neighbor-count
  distribution in every interval; and
- treat cross-period comparison of conditional Moran's I as secondary because
  the active-cell population changes through time.

Relative consolidation, replenishment, and NAT-TMP intensities may also be
undefined when their process-specific initial-stock denominators are zero.
Their spatial support will be recorded explicitly. Complete-domain occurrence
and absolute-area metrics provide the primary spatial comparison; conditional
rates provide complementary exposure-based interpretation.

### Activity tolerance and sensitivity

The primary occurrence rule will remain consistent with the canonical
accounting tolerance: an area greater than `1e-9` ha is positive. To determine
whether single-pixel-scale observations control activity classes, sensitivity
summaries will additionally use fixed minimum areas of `0.1` ha and `1.0` ha.
These alternatives are diagnostics and will not silently replace the primary
definition.

### Acceptance gate

- all formulas reproduce the values already validated in the integrated panel;
- aggregation of cell-level absolute metrics reproduces interval totals;
- denominators and undefined-value rules are recorded for every relative
  metric;
- no distinction between zero and missing support is lost;
- complete-domain and conditional populations reconcile with the expected
  active and inactive counts in every interval;
- sensitivity thresholds are applied identically to every interval.

## Phase 3 — Comparable interval maps

For each core metric, create maps of absolute area and relative intensity for
the seven primary intervals. The diagnostic interval will use the same class
limits and graphical design but will be visibly identified.

Raster processing remains on the native MapBiomas `EPSG:4326` lattice. Final
area maps and distance-based spatial operations will use the following custom
equal-area Albers projection based on the GRS 1980 ellipsoid used by SIRGAS
2000:

```text
+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42
+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs
```

This is a project-defined cartographic CRS rather than an EPSG code. Its full
PROJ definition will be stored with each spatial output. Before map production,
transformed areas will be compared with geodesic cell areas; material failure
of area reconciliation triggers review of the cartographic CRS. EPSG:5880 may
be retained for compatibility checks but will not be described as equal-area.

Class limits for positive magnitudes will be calculated once from the pooled
distribution of the seven primary intervals and then frozen. The primary
categorization is:

```text
zero or inactive
positive low:       > 0 through pooled positive median
positive moderate:  > median through pooled positive 90th percentile
positive high:      > pooled positive 90th percentile
```

The numerical limits will be exported to a versioned table before maps are
interpreted. Interval-specific quantiles are prohibited. A fixed substantive
threshold may replace this distribution-based rule only through a documented
decision made before examining its mapped consequences.

### Required outputs

- one comparable map series per core metric;
- a table containing the fixed class limits;
- distribution summaries supporting the chosen limits;
- a record of missing, undefined, and zero-valued cells;
- the cartographic CRS definition and area-reconciliation result.

## Phase 4 — Cell trajectories and temporal transitions

Track each `cell_id` through the ordered interval sequence to quantify:

- persistence of high, intermediate, low, or zero activity;
- intensification and weakening;
- directional change in the C-R balance;
- reversals between balance states;
- entry into and exit from active-process classes;
- persistence or relocation of high NAT-TMP activity;
- persistence of NAT-TMP trajectories with detected intermediate pasture.

Categories must use fixed definitions across time. Consecutive-period
transition matrices will be produced from the same definitions.

For the C-R balance, the canonical state definitions are:

| State | Definition | Process interpretation |
|---|---|---|
| Inactive | gross C-R activity `<= 1e-9` ha | balance undefined |
| Replenishment-dominant | `cr_balance_index < -1/3` | replenishment exceeds twice consolidation |
| Mixed | `-1/3 <= cr_balance_index <= 1/3` | neither process exceeds the other by more than 2:1 |
| Consolidation-dominant | `cr_balance_index > 1/3` | consolidation exceeds twice replenishment |

Magnitude trajectories will use the pooled median and 90th-percentile limits
defined in Phase 3. Continuous metrics remain the primary analytical values;
categories support mapping and transition summaries rather than replace the
continuous measurements.

### Acceptance gate

- every trajectory contains the expected seven primary observations unless a
  documented support rule excludes a value;
- transition matrices reconcile with their source populations;
- categories are defined before spatial patterns are interpreted;
- results distinguish persistence from repeated occurrence in different
  locations.

## Phase 5 — Global spatial autocorrelation

Global Moran's I will be calculated by metric and interval only after the
spatial metrics and neighborhood structure pass validation.

Primary global autocorrelation estimates will use complete-domain variables
and the fixed complete-domain weights. Conditional Moran's I for
`cr_balance_index` or process-specific rates will be reported separately with
their changing support diagnostics and will not be interpreted as directly
equivalent to a statistic calculated on the complete grid.

The analysis will record:

- neighborhood definition and weight standardization;
- island treatment;
- variable transformation, if any;
- observed Moran's I;
- permutation-based reference distribution and p-value;
- correction used for multiple comparisons;
- primary versus diagnostic temporal status.

Statistical significance will not substitute for effect size. Moran's I and
its temporal variation will be interpreted together with maps and
distributions.

## Phase 6 — Local spatial association

Local Moran/LISA will be used selectively for metrics prespecified as
substantively important and supported by a justified global or mapping
question. Global Moran's I will be examined first, but a non-significant global
result does not automatically prohibit a prespecified local analysis because
opposing local structures can cancel in the global statistic. The output will
distinguish:

- high-high clusters;
- low-low clusters;
- high-low spatial outliers;
- low-high spatial outliers;
- non-significant cells.

Permutation settings and multiple-testing control will be fixed before final
cluster maps are interpreted. LISA will not be run automatically for every
available field.

## Phase 7 — Biome comparison

The Cerrado and Amazon will first be summarized separately using the canonical
cell framework. Boundary cells will be handled using the biome fractions from
Phase 1 or a clearly documented categorical rule appropriate to the specific
analysis.

The comparison will examine:

- absolute and relative process distributions;
- cell-state composition and transitions;
- global autocorrelation;
- location and persistence of local clusters;
- contribution of each biome to the combined-domain pattern.

## Phase 8 — MAUP robustness design

MAUP evaluation will follow the baseline canonical-grid analysis and will use:

1. one alternative grid zoning based on a shifted or tilted origin; and
2. two alternative cell-size evaluations.

The robustness test will repeat a restricted set of central outcomes rather
than the complete exploratory workflow. At minimum, it will compare:

- aggregate totals and distributions;
- core relative metrics;
- global Moran's I;
- broad location and persistence of significant clusters;
- conclusions about spatial concentration and temporal change.

The alternative units, aggregation rules, comparison statistics, and criteria
for substantive stability will be defined before the alternative-grid results
are examined.

## Phase 9 — Synthesis

The final synthesis will distinguish:

- persistent spatial patterns;
- changing or relocating patterns;
- biome-specific and combined-domain behavior;
- results robust to alternative metric definitions;
- results robust to scale and zoning;
- descriptive findings from formal spatial inference;
- primary-period evidence from the `2020-2025` diagnostic extension.

## Planned repository records

Each implemented phase will add only the documentation needed to reproduce and
evaluate it:

- a version-controlled analysis script;
- a methods document for new analytical definitions;
- a validation record containing input and output identities;
- compact derived tables rather than the full canonical panel;
- final figures used for interpretation;
- a decision document only when a methodological choice changes the canonical
  workflow.

Large panels and intermediate spatial files will remain outside GitHub and will
be identified by path, version, dimensions, and cryptographic hash.

Before every new Earth Engine production round, the repository and hosted GEE
configuration will be compared and a compact runtime configuration record will
be saved. Production records will include the relevant Git commit, script
version, GEE task identifier, input asset identifiers, analytical-grid asset,
CRS, affine transform, expected cell count, execution date, and output hash.

## Stop and review conditions

Implementation will pause for a documented decision if:

- the Phase 0 configuration or pilot-comparison gate fails;
- the geometry-to-panel join is not one-to-one;
- biome assignment materially changes results under plausible boundary rules;
- denominator choice changes the substantive spatial interpretation;
- neighborhood definitions yield materially conflicting autocorrelation
  results;
- changing conditional support prevents meaningful temporal comparison of a
  spatial statistic;
- the equal-area cartographic transformation fails area reconciliation;
- local statistics produce unstable clusters under reasonable settings;
- the MAUP test reverses a central conclusion; or
- authoritative information changes the interpretation of the 2025 terminal
  year.

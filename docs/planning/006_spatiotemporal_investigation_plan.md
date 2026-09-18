# Spatiotemporal investigation plan

- **Status:** Approved; Phases 0–7 and Phase 8A complete and accepted; Phase 8B is next
- **Date recorded:** 2026-09-12
- **Last implementation update:** 2026-09-17 — Phase 8A completed and accepted
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

The `2020-2025` interval remains an included and flagged diagnostic extension. It will
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

### Implementation outcome

Phase 1 passed on 2026-09-13. The spatial table contains exactly 24,889 valid
and unique polygon records and matches the integrated-panel population without
loss. Amazon and Cerrado overlap areas and fractions were retained together
with a deterministic primary-biome label.

The fixed shared-edge graph contains 67,453 undirected links and 134,906
directed row-standardized weights. Its largest component contains 24,014 cells;
163 cells are islands and retain zero neighbors without artificial links. The
fragmentation is consistent with the reduced-domain selection and is not
primarily caused by marginal biome intersections.

Complete hexagons include 19.1513 Mha outside the two target-biome polygons.
This accepted consequence of the domain definition requires fractional or
sensitivity treatment in biome-specific analysis. Detailed definitions and
evidence are recorded in:

```text
docs/methods/canonical_spatial_support_and_contiguity.md
docs/validation/canonical_spatial_support_phase1.md
```

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

### Implementation outcome

Phase 2 passed on 2026-09-13. The validated output contains 199,112 unique
cell-interval rows, 24,889 cells, eight intervals, and 211 columns. The
spatial join added 34 Phase 1 support fields without changing any accepted
integrated-panel value. All metric identities, undefined-value rules,
occurrence-threshold checks, accepted interval totals, and graph
reconciliations passed.

The C-R balance is defined for 160,944 active cell-interval rows and remains
undefined for 38,168 inactive rows. The interval-specific conditional graphs
inherit only shared-edge links from the fixed complete graph and retain their
components and islands without artificial connections.

The observed increase in cells with C-R activity is robust to fixed 0.1 ha and
1.0 ha sensitivity thresholds. This is an occurrence result, not evidence by
itself of increasing total area, intensity, persistence, movement, or spatial
clustering. The latter questions remain for Phases 3-6. Detailed definitions
and evidence are recorded in:

```text
docs/methods/canonical_spatial_metrics.md
docs/validation/canonical_spatial_metrics_phase2.md
```

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

### Trajectory-share support decision

The Phase 3A denominator diagnostic showed that cell-level trajectory shares
were sensitive to spatially residual `NAT→TMP` endpoint areas. Decision 008
therefore requires endpoint support greater than 0.1% of each cell's AEA area
for numerical share classification. For the approximately 20,000 ha canonical
cells, this is approximately 20 ha.

Cells without endpoint flow, cells with positive but low endpoint support,
eligible zero shares, and eligible positive low, moderate, and high shares
will be mapped separately. Low-support cells remain in all absolute-area and
complete accounting results.

The final Phase 3A run implemented this support rule and passed all 22
validation checks. It retained 24,303 eligible primary cell-interval records
for each trajectory-share metric, while classifying 32,371 positive-endpoint
records as low support. The eligible pooled median and p90 were frozen at
`0.098669` and `0.570658` for any detected pasture and at `0.092363` and
`0.554050` for two consecutive pasture years.

All 12 class specifications are now accepted. The final limits are stored in
`canonical_comparable_map_class_limits_v2.csv`; 2020-2025 was classified with
these limits but did not contribute to their estimation. Phase 3B map
production is authorized and must consume the frozen limits without refitting
them by interval, biome, or mapped subset. Evidence and definitions are
recorded in:

```text
docs/decisions/008_minimum_support_for_nat_tmp_share_maps.md
docs/methods/comparable_interval_map_classes.md
docs/validation/canonical_map_classes_phase3a.md
```

### Required outputs

- one comparable map series per core metric;
- a table containing the fixed class limits;
- distribution summaries supporting the chosen limits;
- a record of missing, undefined, and zero-valued cells;
- the cartographic CRS definition and area-reconciliation result.

### Implementation outcome

Phase 3B passed on 2026-09-14. The accepted script reproduced the 12 frozen
Phase 3A classifications for all 199,112 cell-interval observations and
matched every accepted class count exactly. No limit was refitted. Twelve
comparable eight-panel series were produced in PNG and SVG, with 2020-2025
visibly retained as a diagnostic extension.

The source WGS 84 spatial geometry was explicitly reprojected to the project
Albers equal-area CRS for cartography and area validation. A preliminary
attempt using the rounded display values from the class-limit CSV was rejected;
the accepted script uses the authenticated full-precision limits from the
Phase 3A validation JSON.

An auxiliary GIS export produced eight one-to-one interval CSV tables, each
with 24,889 rows and 78 fields. All automated integrity checks passed, and the
tables opened successfully in ArcGIS Pro with the accompanying `schema.ini`.
Detailed evidence is recorded in:

```text
docs/methods/comparable_interval_maps_and_gis_exports.md
docs/validation/canonical_comparable_maps_phase3b.md
docs/validation/canonical_gis_interval_tables.md
```

Phase 3 is therefore closed as a computational production stage. Minor future
cartographic refinements remain permissible if they do not change class
membership or temporal comparability. Phase 4 may begin.

## Phase 4 — Cell trajectories and temporal transitions

### Design status and temporal scope

Decision 009 establishes multiquinquennial episodes and the inclusion of the
diagnostic extension. Decision 010, accepted as analytical design on
2026-09-15, defines stages and computable trajectory descriptors. Phase 4A temporal implementation and validation passed on 2026-09-15.
Interpretation and spatial-relocation assessment remain subsequent work.

Track all 24,889 cells through two parallel windows: seven intervals for
`primary` (1985–2020), and eight for `full_observed` (1985–2025). Include
2020–2025 in full sequences, episodes, durations, classifications and the final
transition, retaining `diagnostic_interval = 1`. Produce both sets of results
and expose changes caused by appending the diagnostic interval. Do not
exclude it or overwrite the primary outputs.

### Independent stage axes

The first axis reuses the accepted C–R balance classes:

| State | Definition | Process interpretation |
|---|---|---|
| inactive | gross C–R activity <= 1e-9 ha | balance undefined |
| replenishment_dominant | active index < -1/3 | replenishment exceeds twice consolidation |
| mixed | active index between -1/3 and +1/3 inclusive | neither flow exceeds the other by more than 2:1 |
| consolidation_dominant | active index > +1/3 | consolidation exceeds twice replenishment |

The second axis reuses the frozen `nat_tmp_endpoint_ha__class` magnitude
classes, preserving `zero`, `positive_low`, `positive_moderate`,
`positive_high` and upstream support labels.
Use the authenticated full-precision Phase 3 limits without refitting.
Intermediate-pasture composition remains a complementary measurement or a
separately declared later axis. Its share-support threshold does not exclude
small absolute endpoint flows from the magnitude analysis.

Both axes are required products; implementation may deliver C–R first.
Sequences and episodes for the other Phase 3 metrics are permitted, but their
ordinal and support semantics must be declared before applying a typology.
Never merge different processes into one undocumented stage field.

### Episodes and trajectory descriptors

Reconstruct maximal consecutive equal-stage runs separately by cell, axis and
window. Retain the original ordered interval sequence. Report observed duration
as the number of intervals and the sum of their t1−t0 spans, with persistence
at two or more intervals. This describes consecutive quinquennial assignments,
not proven continuous annual persistence of a process or individual pixels.

Retain independent left/right boundary flags: a single episode can touch both.
Report unknown continuation beyond window boundaries using Decision 009's
boundary/censoring language. Distinguish isolated episodes, isolated activity
and isolated inactivity.

Expose stage reentries, stage-specific occurrence and duration, changes of
ordinal direction, activity entry/exit, interruptions and resumptions. Inactive
C–R stages are not ordinal ranks. Direction among active stages and direct
changes within uninterrupted active blocks are separate descriptors.
Endpoint magnitude includes zero in its ordinal order. Unknown support is never
inactivity, zero or an ordinary process transition.

Classify each complete-support trajectory using Decision 010's ordered rules:
`constant`, `returning`, `recurrent`, `nonmonotonic_without_return`,
`monotonic_without_return`, or `activity_change_without_ordinal_change`.
Strict repeated two-state alternation is an independent flag, not a synonym
for every recurrence or direction change. Support-limited optional axes retain
all support states and require a separate substantive classification rule.

### Required products

- interval-stage tables and uncompressed primary/full sequences;
- episode tables with durations, boundaries and independent isolation flags;
- cell-window summaries with patterns and auditable descriptors;
- primary/full comparison with diagnostic-dependent changes;
- adjacent-interval transition matrices for each axis and window;
- an implementation script and an actual validation record with input/output hashes.

Continuous gross activity, net balance, endpoint magnitude and support remain
available alongside the categories. A balance-state order does not establish
a necessary agricultural-development sequence. Cell-level episodes do not
substitute for within-interval pixel trajectories or demonstrate relocation.
Changes in the location of high-activity cells require comparison of the
spatial sets across periods, not merely a single cell's pattern code.

### Acceptance gate

- exactly 24,889 cells per axis, seven primary and eight full observations;
- accepted stages reproduced without refitting or loss of support distinctions;
- episode partition reconstructs the original interval sequence exactly;
- duration, reentry, boundary, isolation and pattern rules verified, including
  meaningful inactive and single-episode edge cases;
- per-axis matrices reconcile with 149,334 primary and 174,223 full adjacent
  transitions;
- one pattern per complete-support cell-window-axis, with primary/full codes
  preserved and diagnostic effects explicitly exposed;
- episode persistence distinguished from whole-window constancy and spatial
  repeated occurrence distinguished from persistence at the same cell;
- actual data validation reported separately from this accepted design.

Operational rules and examples are recorded in:

```text
docs/decisions/010_stage_definition_and_trajectory_typology.md
```

### Phase 4A implementation outcome

Phase 4A temporal production passed on 2026-09-15 in run
`run_20260915T091255_865443Z`, using script revision 2. All 12 metrics
received primary and full observed sequences, episodes, occupancy and
transitions. Decision 010 typologies were applied to both declared core axes;
the remaining ten metrics retain descriptive outputs without an undocumented
substantive classification.

The execution produced 597,336 cell-window-metric summaries, 1,515,075 episodes
and 1,135,618 occupancy rows. Adjacent transition events total 1,792,008 for the
primary window and 2,090,676 for the full observed window. All 13 runtime
checks passed. Independent review confirmed compact output hashes, all 117
inventory records, transition sums/marginals, exact frozen limits and identical
overlapping primary/full transition pairs.

Four GIS summaries supplied 99,556 complete-support core records. Independent
cell-level review found no divergence between the `constant` pattern, the
constancy flag and an episode count of one. `no_change` was also observed with
`activity_change_without_ordinal_change`, confirming that its reachability is
part of the existing design rather than requiring an amendment.

The 2020–2025 interval is included and flagged. The temporal production stage
is accepted; interpretation, figure development and assessment of spatial
relocation remain separate work. Full episode Parquets were validated by the
script and their reported identities/dimensions reviewed through the inventory;
they were not independently reread during the compact-output review.

Evidence and implementation are recorded in:

```text
analysis/09a_build_cell_state_trajectories.py
docs/methods/cell_state_trajectories_and_multiquinquennial_episodes.md
docs/validation/phase4a_revision2_verification.md
docs/validation/canonical_cell_trajectories_phase4a.md
```

The actual Colab execution used revision 2 with SHA-256
`8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec`.
The current repository implementation is revision 3, which retains the
revision-2 analytical logic and only removes an invalid GIS schema option while
updating its version/banner. No analytical rerun is required.

### Phase 4 interpretation and closure outcome

Phase 4 was subsequently completed with spatial exploration of the fixed
2,598-cell high-magnitude `NAT → TMP` cohort, comparison of four primary
magnitude groups, continuous-flow comparison, primary-biome and transbiome
sensitivity analyses, and synthesis of episodes, persistence, reentries,
reversals, transition matrices and flow concentration.

The high group contains 10.44% of domain cells and accounts for 87.5% of the
summed primary-period `NAT → TMP` endpoint area. Primary-biome membership is
648 Amazon and 1,950 Cerrado cells. The four fixed domain groups are 11,213
cells with no primary occurrence, 4,887 with a low maximum, 6,191 with a
moderate maximum and 2,598 with a high maximum. The interpretation remained
descriptive and retained 2020–2025 as an included diagnostic extension.

The C–R `returning + recurrent` share rises from 20.76% in the primary window
to 30.85% in the full window because the appended diagnostic state creates
2,512 newly returning cells. This is recorded as extension sensitivity rather
than a claim that historical recurrence nearly doubled.

Phase 4 is closed in its agreed scope. Its consolidated findings are recorded
in `docs/analysis/phase4_spatial_findings_and_closure_v1.md`.

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

### Phase 5 implementation outcome

Phase 5 completed and passed on 2026-09-15. The accepted analysis contains 104
prespecified Global Moran tests using 9,999 permutations and Benjamini–Yekutieli
correction in four declared families. All 104 observed Moran values are
positive and significant after correction. Complete-domain and conditional
supports remain separate; islands retain zero spatial lag and receive no
artificial neighbors. The result establishes positive spatial association, not
cluster location, process dominance, temporal trend or causality.

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

### Phase 6 implementation outcome

Phase 6 completed and passed on 2026-09-16 for five focal metrics across eight
intervals: 40 maps and 995,560 cell-map records. Each map used 9,999 conditional
permutations, Benjamini–Hochberg as the prespecified primary within-map
correction and Benjamini–Yekutieli as sensitivity.

BH identified 168,860 significant records: 52,867 HH, 113,044 LL, 497 HL and
2,452 LH. BY retained 72,221. For consolidation, replenishment and `NAT → TMP`
area, HH is the main process-concentration result and LL describes structured
low activity or absence. For net balance and the C–R index, HH and LL are
co-primary opposing regimes whose substantive interpretation also requires
the observed sign or dominance threshold. Decisions 011 and 012 govern the
inferential and interpretive rules.

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

### Phase 7 implementation status

Phase 7 was completed and accepted on 2026-09-17. The primary comparison partitions all
cells using the deterministic Phase 1 `primary_biome`; a sensitivity analysis
excludes the 582 cells intersecting both target biomes without reassignment or
fractional allocation of their observed processes.

The implementation summarizes all 12 frozen metrics and the two core temporal
axes. Global Moran is recalculated in induced biome-specific graphs for five
focal metrics. Accepted Phase 6 LISA classes are not recomputed; they are
attributed by biome as contributions to the combined-domain spatial pattern.
The production design included two biomes, two boundary treatments, eight
intervals and 160 biome-specific Global Moran tests with 9,999 permutations.
All 160 tests were significant after the prespecified Benjamini–Yekutieli
correction. Output hashes, populations, transition closure and graph-specific
statistics passed independent review.

The primary population contains all 24,889 cells. The 582 transbiome cells are
included through the deterministic largest-overlap assignment: 293 in Amazon
and 289 in Cerrado. They are excluded only from the 24,307-cell
single-biome-sensitivity population. Their exclusion produced small changes in
Global Moran's I, with a maximum absolute difference of 0.044848, and did not
change the substantive conclusions.

The phase identified a temporal convergence in the biome contributions to
consolidation, a growing Amazon contribution to replenishment, and more dynamic
`NAT → TMP` cell-state trajectories in Cerrado. Cerrado contributed more and
more persistent HH cells for consolidation, `NAT → TMP`, and the C–R balance,
whereas Amazon had the larger persistent-HH population for replenishment.

Phase 7 is closed. Phase 8 will evaluate sensitivity to spatial scale and
zoning through the prespecified MAUP design.

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

### Phase 8A implementation outcome

Phase 8A was completed and accepted on 2026-09-17. It constructed three
alternative regular-hexagon lattices in the project equal-area CRS: an
approximately 10,000-ha grid, an approximately 40,000-ha grid, and a
20,000-ha grid shifted by half of both canonical lattice basis vectors.

The analytical footprint is held fixed as the union of the 24,889 canonical
cells. Alternative units retain complete hexagonal geometries and record their
intersection area and support fraction within that footprint. The domain is
not reselected from endpoint land cover, and canonical process values are not
spatially interpolated.

The accepted populations are 56,520 `hex10k_base` cells, 29,396
`hex20k_shift` cells and 15,309 `hex40k_base` cells. Each grid closes to the
same 497,776,400.4434-ha fixed footprint, with relative discrepancies from
approximately `1.2e-15` to `1.7e-14`. The inferred lattice, generated
geometries, deterministic identifiers and three export formats passed the
production validation.

Phase 8A calculated geometry and support only. After its geometric support
distribution was accepted, and before process results were inspected,
Decision 014 fixed all positive-support cells for totals, support fraction
`>=0.50` for primary cell-level comparisons, and 0.25 and 0.75 as sensitivity
thresholds. Process extraction, restricted metric construction and statistical
comparison remain for Phase 8B. Process values must be measured directly from
source pixels under the fixed-domain mask and may not be allocated from
canonical-cell totals.

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

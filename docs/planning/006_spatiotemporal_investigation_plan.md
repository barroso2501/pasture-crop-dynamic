# Spatiotemporal investigation plan

- **Status:** Approved; Phases 0-3B passed and Phase 4 is next
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

## Temporal interpretation rule

The five-year intervals are fixed accounting windows, not presumed complete land-use episodes.
The investigation will retain all eight intervals from 1985–1990 through 2020–2025. The final interval will be identified as the **diagnostic temporal-boundary interval** because episodes continuing in 2025 cannot be observed to completion.

Results will distinguish:
- the **primary period**, containing intervals ending in or before 2020;
- the **full observed series**, including the flagged 2020–2025 interval.

The final interval will not be excluded from maps, trajectories, episode reconstruction, or descriptive summaries. Conclusions sensitive to its inclusion will be reported through a direct comparison of primary-period and full-series results.

Phase 4 will treat analytical stages as potentially persistent across more than one five-year interval. It will also retain progression, return, recurrence, and alternation among stages. Detailed rules are established in `docs/decisions/009_multiquinquennial_episodes_and_2020_2025.md`.

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

## Phase 4 — Cell trajectories and multiquinquennial episodes

### Objective

Describe how each cell moves through analytical stages across the ordered five-year intervals, explicitly representing persistence, duration, progression, return, and alternation.

The five-year interval remains the accounting unit. Multiquinquennial episodes are derived by joining consecutive intervals assigned to the same preregistered stage.

The analysis will retain all eight intervals:

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

The interval 2020–2025 will remain part of the analysis but will be identified as the **diagnostic temporal-boundary interval**. Episodes reaching 2025 may have a known minimum observed duration but an unknown complete duration.

Detailed rules are established in `docs/decisions/009_multiquinquennial_episodes_and_2020_2025.md`.

### 4.1 Preregister interval-level stages

Before inspecting trajectory maps, episode frequencies, or spatial patterns, create a stage-definition record specifying:

- variables included in the classification;
- analytical denominators;
- treatment of structural zeros;
- treatment of undefined ratios;
- minimum material-flow tolerance;
- numerical thresholds;
- reference population used to define empirical thresholds;
- rules for ties and boundary values;
- stage-definition version.

The same stage definitions and thresholds must be applied to every interval.

If empirical thresholds are required, they will be estimated once from a declared reference population within the primary 1985–2020 period and then applied unchanged to all eight intervals, including 2020–2025.

Interval-specific quantiles are not permitted for longitudinal stage assignment because changing class boundaries could produce artificial stage changes.

The initial candidate stage vocabulary is:

- low or absent focal activity;
- pasture-expansion dominant;
- agricultural-consolidation dominant;
- mixed expansion and consolidation;
- replacement- or expansion-favoured balance;
- consolidation-favoured balance;
- balanced active configuration;
- undefined balance because neither focal component is materially present.

This vocabulary may be simplified before implementation. However, the final definitions must be fixed and documented before substantive interpretation of the resulting trajectories.

### 4.2 Construct the complete interval-stage panel

Produce one row for every:

```text
cell_id × five-year interval
```

The panel must contain all 24,889 cells and all eight intervals, for a total of:

```text
199,112 cell-interval observations
```

Required fields include:

- `cell_id`;
- `interval`;
- `interval_order`;
- `interval_start_year`;
- `interval_end_year`;
- `stage_code`;
- `stage_label`;
- `stage_definition_version`;
- `primary_period_flag`;
- `diagnostic_interval_flag`;
- variables used to assign the stage;
- structural-zero indicator;
- undefined-balance indicator;
- material-activity indicator.

The intervals ending in or before 2020 will receive:

```text
primary_period_flag = 1
diagnostic_interval_flag = 0
```

The interval 2020–2025 will receive:

```text
primary_period_flag = 0
diagnostic_interval_flag = 1
```

Structural zero, low activity, and undefined balance must remain distinct analytical conditions.

An undefined value of `cr_balance_index` caused by the absence of both consolidation and replacement must not be converted automatically to zero or interpreted as a balanced configuration.

### 4.3 Construct ordered cell-stage sequences

For each cell, sort the eight interval-stage observations chronologically and preserve the complete ordered sequence.

For example:

```text
low → expansion → expansion → mixed → consolidation
    → consolidation → low → low
```

The ordered sequence must be stored in a form that permits exact reconstruction of:

- the stage assigned to every interval;
- the order of stage changes;
- repeated stages;
- returns to previously occupied stages;
- the contribution of 2020–2025 to the final trajectory.

A summary trajectory category must not replace the underlying ordered sequence.

### 4.4 Reconstruct episodes

An episode is defined as one or more consecutive five-year intervals assigned to the same analytical stage.

For each cell, consecutive intervals with the same stage will be combined into one episode.

A stage persisting for two or more consecutive intervals constitutes a **multiquinquennial episode**.

Produce an episode table containing at least:

- `cell_id`;
- `episode_id`;
- `episode_order`;
- `episode_start_year`;
- `episode_end_year`;
- `episode_interval_count`;
- `episode_observed_duration_years`;
- `episode_stage_code`;
- `episode_stage_label`;
- `previous_stage`;
- `next_stage`;
- `left_boundary_flag`;
- `right_boundary_flag`;
- `includes_2020_2025`;
- `multiquinquennial_flag`.

Observed episode duration will be calculated as:

\[
D_e = 5n_e,
\]

where \(n_e\) is the number of consecutive five-year intervals assigned to episode \(e\).

Thus:

- one interval represents five years of observed duration;
- two consecutive intervals represent ten years;
- three consecutive intervals represent fifteen years.

This measure represents duration observed within the analytical series. It is not necessarily the complete duration of the underlying land-use process.

An episode beginning in the first interval may have started before 1985 and will receive:

```text
left_boundary_flag = 1
```

An episode containing 2020–2025 and still present at the end of the observed sequence will receive:

```text
right_boundary_flag = 1
includes_2020_2025 = 1
```

A right-boundary episode must be described using minimum observed duration. For example:

> The consolidation-dominant episode persisted for at least ten observed years.

It must not be described as having ended in 2025 unless an observed subsequent transition supports that conclusion.

### 4.5 Classify complete cell trajectories

Using the ordered stage sequence and reconstructed episodes, classify each cell according to its temporal pattern.

At minimum, distinguish:

- persistent single-stage trajectory;
- multiquinquennial persistence followed by change;
- one-directional progression;
- return to a previously occupied stage;
- repeated alternation;
- isolated activity episode;
- late entry into focal activity;
- apparent exit from focal activity;
- trajectory containing an undefined stage;
- trajectory ending in an open right-boundary episode.

These categories describe cell-level analytical trajectories. They do not imply that every pixel within a cell followed the same temporal sequence.

### 4.6 Quantify persistence, return, and alternation

For every cell, calculate at least:

- number of episodes;
- number of stage changes;
- number of distinct stages;
- number of multiquinquennial episodes;
- maximum observed episode duration;
- mean observed episode duration;
- number of returns to a previously occupied stage;
- alternation count;
- alternation flag;
- left-boundary episode flag;
- right-boundary episode flag;
- trajectory-category code;
- trajectory-category label.

A return occurs when a stage reappears after at least one intervening interval assigned to another stage.

For example:

```text
expansion → mixed → expansion
```

contains a return to the expansion stage.

Alternation refers to repeated movement between previously occupied cell-level stages. For example:

```text
expansion → consolidation → expansion → consolidation
```

represents repeated alternation.

Alternation must not automatically be interpreted as pixel-level land-use reversal. Different portions of an approximately 20,000 ha cell may contribute to the interval-level pattern.

The preferred term is therefore:

```text
cell-level stage alternation
```

A stronger interpretation will require supporting annual pixel-trajectory evidence.

### 4.7 Compare primary-period and full-series trajectories

Produce two trajectory summaries:

1. **primary-period summary:** intervals from 1985–1990 through 2015–2020;
2. **full observed-series summary:** all intervals through 2020–2025.

The 2020–2025 interval will not be excluded from the full-series analysis.

The comparison must identify:

- cells whose trajectory category changes after including 2020–2025;
- episodes already present in 2015–2020 that are extended by 2020–2025;
- new episodes beginning in 2020–2025;
- episodes receiving a right-boundary flag;
- changes in maximum observed episode duration;
- changes in stage-change or alternation counts;
- changes in the direction of the substantive temporal interpretation.

A conclusion will be considered temporally robust when its direction and substantive interpretation remain consistent in the primary-period and full-series summaries.

Material differences must be retained and reported as temporal-boundary sensitivity. The final interval must not be removed merely because its inclusion changes a result.

### 4.8 Map trajectory and episode outcomes

Map only a restricted set of interpretable Phase 4 outcomes:

- longest-duration stage;
- maximum observed episode duration;
- number of stage changes;
- number of multiquinquennial episodes;
- occurrence of repeated alternation;
- occurrence of return to a previous stage;
- trajectory category;
- open right-boundary episode;
- change in classification caused by inclusion of 2020–2025.

Maps must use the equal-area cartographic projection established in Phase 3.

Class definitions and map limits must remain comparable across the domain. The diagnostic status of 2020–2025 must be visible in titles, captions, legends, or accompanying notes whenever the final interval contributes to the mapped outcome.

### 4.9 Interpretation constraints

The Phase 4 analysis must preserve the distinction between:

1. five-year interval accounting;
2. cell-level analytical stages;
3. multiquinquennial cell-level episodes;
4. annual pixel-level land-cover trajectories.

Episode reconstruction is a classification layer derived from the validated interval panel. It must not modify:

- interval stock values;
- interval flow values;
- pasture-origin partitions;
- accounting identities;
- cell-level closure;
- annual intermediate-trajectory measurements.

Persistence of a cell-level stage does not demonstrate that the same pixels remained in that state throughout the episode.

Likewise, cell-level alternation does not demonstrate that individual pixels repeatedly reversed land use.

### 4.10 Phase 4 stop-and-review conditions

Phase 4 must stop for methodological review if:

- stage definitions have not been fixed before inspection of trajectory results;
- thresholds differ among intervals;
- thresholds were selected after inspecting maps or temporal patterns;
- interval-specific quantiles are being used to define longitudinal stages;
- structural zeros, low activity, and undefined balance cannot be distinguished;
- any expected `cell_id × interval` combination is absent;
- interval-stage keys are not unique;
- any interval-stage observation is assigned to zero episodes;
- any interval-stage observation is assigned to more than one episode;
- episode duration is inconsistent with the number of included intervals;
- nonconsecutive occurrences of the same stage are merged into one episode;
- an episode reaching 2025 is interpreted as complete without an observed subsequent transition;
- inclusion of 2020–2025 reverses a central temporal conclusion;
- primary-period and full-series classifications differ materially without an explicit sensitivity account;
- cell-level alternation is interpreted as pixel-level reversal without supporting evidence;
- episode reconstruction changes any validated interval-level stock or flow value;
- a summary trajectory category cannot be reconstructed from the retained interval-stage sequence.

A stop condition does not imply removal of 2020–2025. It requires documentation and review of the sensitivity or interpretation involved.

### 4.11 Required outputs

Phase 4 must produce:

1. an interval-stage panel with one row per `cell_id × interval`;
2. an ordered stage sequence for every cell;
3. an episode table with one row per reconstructed episode;
4. a cell-level trajectory summary;
5. a stage-definition and threshold record;
6. primary-period and full-series comparison tables;
7. selected trajectory and episode maps;
8. a Phase 4 validation record.

Suggested canonical output names are:

```text
canonical_interval_stage_panel_v1.parquet
canonical_cell_stage_sequences_v1.parquet
canonical_multiquinquennial_episodes_v1.parquet
canonical_cell_trajectory_summary_v1.parquet
canonical_stage_definition_v1.json
canonical_phase4_temporal_boundary_comparison_v1.csv
canonical_phase4_validation_v1.json
```

### 4.12 Acceptance criteria

Phase 4 is accepted when:

- all 24,889 cells are represented;
- all eight intervals are represented;
- all 199,112 expected `cell_id × interval` observations are present;
- interval-stage keys are unique;
- stage definitions are documented and versioned;
- stage thresholds are identical across intervals;
- structural zeros, low activity, and undefined balance remain distinguishable;
- the ordered stage sequence is reconstructable for every cell;
- every interval-stage observation belongs to exactly one episode;
- consecutive intervals with the same stage are combined reproducibly;
- nonconsecutive occurrences remain separate episodes;
- episode duration equals five times the episode interval count;
- multiquinquennial episodes are explicitly identifiable;
- persistence, progression, return, and alternation can be distinguished;
- episodes touching 1985 or 2025 carry the appropriate boundary flag;
- 2020–2025 remains included and explicitly flagged;
- primary-period and full-series results can be compared directly;
- episode reconstruction leaves the validated interval accounting unchanged;
- summary trajectory classes can be reconstructed from the retained ordered sequences;
- every triggered stop-and-review condition has been resolved through a documented decision.

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

### Temporal-boundary synthesis

Every central temporal conclusion must identify whether it is supported by:

- the primary 1985–2020 period;
- the complete 1985–2025 observed series; or
- both.

The 2020–2025 interval will remain visible in final analytical products but will be identified as the diagnostic temporal-boundary interval.

The synthesis must report whether inclusion of 2020–2025:

- preserves the direction and magnitude of the main pattern;
- extends an episode already present in 2015–2020;
- initiates a new episode;
- changes the assigned trajectory category;
- changes the substantive interpretation.

Episodes that remain active in 2025 will be described using minimum observed duration, for example “persisted for at least ten years”, rather than as complete episodes.

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

> **GitHub browser packaging — 2026-10-23.** Extract both `entry_reentry_github_parte1_v1.zip` and `entry_reentry_github_parte2_v1.zip` into the same directory. Upload the extracted tree in batches of at most 100 files. All distributed files are below 25 MB. The accepted large normalized panel is stored losslessly as `.csv.gz`; run `python analysis/restore_entry_reentry_large_csv_v1.py` before reproducing validation. The original PASS JSON, critical source pins, native data and scientific results remain unchanged. See [Portuguese upload instructions](SUBIR_NO_GITHUB_PT.md).

> **Current status — 2026-10-23: full native entry/re-entry validation PASS.** All 73 returned CSVs, 24,889 cells, 199,112 cell/interval rows and 24,889 complete history audits are accepted. Coverage-derived auxiliary age-201 checks pass. Earlier dated pending statements below are historical and superseded for this component by the full acceptance. Public pasture-age asset validation, remote executed-text attestation and release obligations retain their separate scope.
>
> See [full acceptance](docs/validation/entry_reentry_full_acceptance_v1.md), [domain findings](docs/results/entry_reentry_full_findings_v1.md), [machine PASS](outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_validation.json) and [Portuguese result/next step](RESULTADO_E_PROXIMO_PASSO_PT.md). Matrix v4.3/events-v5 remain unchanged.

# Pasture–Crop Dynamics in the Brazilian Cerrado and Amazon

## Overview

This repository supports a research project on the long-term dynamics among native vegetation, planted pasture, and temporary crops in the Brazilian Cerrado and Amazon.

The project moves beyond net land-cover change to examine **directed flows**, **land-stock origins**, and **conversion pathways**. Its central purpose is to determine how pre-existing pasture stocks and newly established pastures contribute to agricultural consolidation across space and time.

The canonical workflow has been reproduced and validated through the complete MAUP assessment and integrated evidence review. It includes the study domain, five-year stock-and-flow and annual `NAT → TMP` trajectory panels, integrated cell-by-interval metrics, fixed spatial support and contiguity graph, comparable map classes, cell-state trajectories, temporal synthesis, Global Moran, Local Moran/LISA, biome-specific comparisons, alternative-grid metric reconstruction, prespecified comparison of aggregate values and weighted cell distributions, Global Moran sensitivity, broad HH-cluster location and persistence robustness, a fixed-1985-pasture-cohort endpoint analysis, and an authenticated evidence matrix. Phases 1–8 and the executions of Phase 9A/9A.1 have been accepted; Phase 9A.2 terminology harmonization is complete. The observed-pasture-spell remediation has a recorded technical closure under Decision 024; the 2026-10-09 erratum qualifies its scientific interpretation and assurance scope. Matrix v4.1 introduced the rewritten P9A035–P9A037; matrix v4.2 incorporated the accepted window sensitivity into P9A035/P9A036, and current matrix v4.3 adds stock-normalized endpoint fractions while preserving P9A037 and the other 32 findings. Current cumulative status events-v5 retain the earlier rescission for these corrected statements only; source-age v3 claims remain superseded. The corrected version-2 stock-flow, derived, and integrated panels passed the documented non-origin invariance comparison. The full-domain 2024–2025 boundary-event audit, source-impact audit, and RQ1 fixed-cohort revalidation have also passed. The 2026-10-08 closure is retained as history, supplemented by the 2026-10-09 qualifications. Phases 2–8 were not re-executed in the remediation; non-origin invariance is a versioned-chain comparison, not an independent re-export of NAT→TMP or TMP→* raster flows. Current authority: matrix v4.3 and events-v5. Events v1–v4 are historical cumulative editions.

## Scientific motivation

Net change indicates how much of a land-cover class was gained or lost, but it does not fully describe the underlying transitions. Similar net outcomes may arise from different combinations of persistence, conversion, replacement, and spatial exchange.

This distinction is especially important for the native vegetation–pasture–agriculture system. Pasture is often treated as a universal intermediate stage between native vegetation and crops. In practice, agricultural expansion may involve several pathways:

- conversion of long-established pasture to agriculture;
- conversion of pasture established during the observation period;
- transition from native vegetation to agriculture after a brief pasture phase;
- transition from native vegetation to agriculture with no pasture phase detected in the annual land-cover series;
- trajectories involving other intermediate states, such as mosaic land uses or exposed soil.

The project treats these pathways as measurable components of a spatial land-stock and flow accounting system rather than assuming a single frontier sequence.

## Research questions

The project is organized around five questions:

1. How has the pasture stock already present in 1985 been redistributed over time?
2. What share of pasture-to-temporary-crop conversion originated from a pasture episode observed continuously since 1985, an episode with observed post-1985 entry, or an episode of unresolved origin?
3. Among pixels classified as native vegetation at the beginning of a five-year interval and temporary crops at its end, what share passed through pasture during the intervening years?
4. How do these stocks, flows, and pathway compositions vary across space and time?
5. How robust are the results to temporal resolution, spatial scale, zoning, and spatial-weight definitions?

## Conceptual framework

### Core land-cover states

The main analytical system contains three focal states:

- **NAT** — native vegetation;
- **PAS** — planted pasture;
- **TMP** — temporary crop.

Additional categories are retained where necessary to close the accounting system, including mosaic or other agricultural uses, other anthropogenic or non-vegetated uses, water, and unobserved or masked pixels.

### Stocks and flows

Land-cover stocks describe the area occupied by each state at a given time. Directed flows describe transitions between two time points, such as:

- `NAT → PAS`: pasture expansion or pasture-stock replenishment;
- `PAS → TMP`: pasture-to-temporary-crop conversion;
- `NAT → TMP`: native-to-temporary-crop endpoint transition between observation points.

The accounting framework is designed to track all relevant destinations of an initial stock and to quantify residual or unclassified components explicitly.

### Pasture-spell origin

The governing method for `PAS → TMP` origin attribution reconstructs the current observed pasture spell from annual Collection 11 coverage, rather than taking the public pasture-age code as the analytical origin. At the beginning of each five-year interval, a pasture pixel belongs to one of three exclusive states:

- **left-censored continuous 1985 pasture episode** — pasture observed without interruption from the earliest observed year, 1985, to the interval start; its establishment date before or at that boundary is unknown;
- **observed post-1985 entry episode** — the current pasture spell began after a confidently observed non-pasture year, including a return to pasture by a pixel belonging to the fixed 1985 cohort;
- **unresolved episode origin** — an unobserved, masked, or unexpected annual coverage value prevents attribution of the current spell to either of the preceding states.

Any confidently observed exit from pasture, including `PAS → NAT`, ends the spell. A missing observation breaks confirmed continuity without proving an exit. This classification describes the *current observed spell*, not the first-ever establishment of pasture at a location. The `PAS → TMP` origin composition addresses RQ2; applying the same classification to `PAS → NAT` is supplementary and does not expand that research question. The eight-interval reassessment has been computed for the primary 1985–2020 series and the full observed 1985–2025 series. The accepted corrected products and completed window sensitivity support the qualified RQ2 statements in evidence matrix v4.3.

The public pasture-age asset remains available for provenance and impact auditing. Its unexpected raw code `1` and reuse of code `100` after observed pasture interruption are the reasons for the present remediation. Neither source code determines the corrected analytical origin class.

### Two complementary temporal views

The project combines:

1. **Five-year accounting intervals**, used to obtain more stable measurements of land stocks and directed flows.
2. **Annual within-interval trajectories**, used to identify short pasture phases that are compressed by five-year comparisons.

The annual analysis is treated explicitly as sensitive to temporal classification instability. The canonical trajectory panel retains an inclusive pasture-detection rule and persistence-sensitive alternatives requiring at least two pasture years or two consecutive pasture years.

## Study domain

The study focuses on the Cerrado and Amazon biomes. The canonical spatial framework is a fixed set of **24,889 complete hexagonal cells** of approximately 20,000 hectares each. These cells were reconstructed reproducibly from 32,305 parent-grid cells intersecting the two biomes and were retained when recognized anthropogenic land cover exceeded a numerical tolerance of 0.01 ha in either 1985 or 2025.

The reduced domain excludes 7,416 candidate cells without recognized anthropogenic land cover above that tolerance at either endpoint. The domain definition concerns cell-level analytical support and should not be confused with pixel-level alternation, individual pixel trajectories, or interval-specific activity. Stable anthropogenic cells may belong to the domain.

The domain remains fixed across time. Within it, the number and identity of cells with a particular process—such as pasture expansion or agricultural consolidation—may vary among five-year intervals.

## Temporal coverage

The source time series spans **1985–2025**, with the following five-year reference points:

```text
1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025
```

The primary inferential period ends in 2020. The 2020–2025 interval is included in descriptions, trajectories, transitions, maps, and spatial statistics, but remains explicitly identified as a diagnostic extension. Primary-period and full-observed results are reported separately where the additional interval can alter episode duration or recurrence.

## Data sources

The current workflow uses:

- **MapBiomas Brazil Collection 11 `coverage_v3`** annual land-cover maps;
- **MapBiomas Collection 11 pasture-age product**, retained for provenance and source-impact auditing, not as the governing source of pasture-spell origin;
- an equal-area hexagonal grid with cells of approximately 20,000 ha;
- the reproducibly reconstructed Cerrado–Amazon canonical domain.

Exact asset identifiers, product versions, class remapping rules, coordinate reference systems, and grid transforms are recorded in the technical methods and configuration. The approved reconstruction is described in `docs/decisions/024_reconstruction_of_observed_pasture_spell_age.md` and `docs/methods/observed_pasture_spell_age_reconstruction.md`.

## Main analytical components

### 1. Five-year stock and flow accounting

For each cell and interval, the workflow quantifies focal transitions, persistence, auxiliary destinations, masked areas, and pasture-to-temporary-crop conversion. The earlier source-age origin partition remains a provenance record and is not used as accepted evidence. The reconstructed observed-spell partition is available for all eight intervals, with pooled primary and full-observed summaries, and its corrected findings are accepted in evidence matrix v4.3 within the documented evidence scope.

The principal origin identity is:

```text
PAS→TMP total = left-censored continuous 1985 episode
              + observed post-1985 entry episode
              + unresolved episode origin
```

### 2. Fixed 1985 pasture cohort

The previously accepted RQ1 extraction fixed the pixel cohort using pasture coverage class `15` and source pasture-age code `100` in 1985. The same pixels are reclassified at the nine reference years from 1985 through 2025. The number and identity of cohort pixels remain fixed; only their endpoint distribution among land-cover states changes. The explicit Decision 024 revalidation passed on 2026-10-08: the original export and accepted references were authenticated, the baseline population reconciled, and per-cell cohort area matched the coverage-only PAS-1985 stock in both the original CSV and corrected panel v2. Cohort membership and the origin of a *later* pasture spell are different analytical objects.

This component measures endpoint-state composition, not uninterrupted persistence or pixel-level alternation. Because the exported results are aggregated by cell, they do not identify a unique sequence of transitions for individual pixels between reference years. The revalidated extraction contains 49,035,870.567 ha in 16,421 cells with positive cohort area, within the 24,889-cell canonical domain. At the 2020 endpoint, 63.13% is classified as pasture, 19.94% as temporary crops, 9.22% as other agriculture, and 6.82% as native vegetation. The 2025 endpoint is included as a diagnostic extension. The revalidation reproduced all 45 summary rows across nine dates and five reporting strata. The maximum per-cell difference from the original PAS-1985 stock was 2.6822 × 10⁻⁷ ha, and the maximum summary-state difference was 4.8429 × 10⁻⁸ ha, both below the 0.001-ha tolerance. This supports retention of the unchanged original cohort and its endpoint compositions within the documented scope; it does not independently resample native pixels or prove continuous pasture persistence. See [the RQ1 revalidation record](docs/validation/canonical_fixed_1985_pasture_cohort_revalidation_v1.md).

### 3. Within-interval trajectory analysis

For pixels classified as `NAT` at the beginning and `TMP` at the end of an interval, the canonical trajectory panel uses annual observations to distinguish:

- endpoint flow with pasture detected in at least one intermediate year;
- endpoint flow with pasture detected in at least two intermediate years;
- endpoint flow with pasture detected in at least two consecutive intermediate years; and
- endpoint flow with no pasture detected in the annual series.

The latter will not automatically be called “direct conversion,” because other intermediate land-cover states may be present.

### 4. Consolidation–replenishment balance

The relationship between pasture-to-cropland consolidation and native-to-pasture replenishment is evaluated for explicitly defined analytical populations, including the full dynamic domain and process-specific subsets.

For spatial analyses, a bounded balance index may be used:

```text
(consolidation - replenishment) / (consolidation + replenishment)
```

### 5. Spatial robustness and structure

The spatial analysis includes:

- sensitivity to grid positioning and orientation;
- sensitivity to cell sizes around the 20,000 ha reference scale;
- global spatial autocorrelation;
- selected local spatial association analyses where supported by the global pattern;
- comparison of alternative spatial-weight matrices for the reduced domain.

### 6. Integrated analytical panel

The validated derived stock-flow table and the annual `NAT → TMP` trajectory
panel are joined one to one using `cell_id`, `t0`, and `t1`. The integrated
table retains all 199,112 cell-interval observations, including structural
zeros, and preserves the conceptual distinction among net balance, directed
endpoint flows, and annual pixel trajectories.

## Validation principles

The canonical workflow is evaluated through explicit checks, including:

- a balanced cell-by-period panel;
- unique cell identifiers;
- non-negative area values;
- complete and mutually exclusive transition partitions;
- closure of the fixed 1985 pasture cohort;
- separate accounting for substantive observed destinations and observation loss;
- mutually exclusive reconstructed pasture-spell origins and explicit unresolved histories;
- source pasture-age code and mask audits for provenance; the raw code-`1` diagnostic and the full-domain source-impact/overlap audit have passed, with official source-code semantics still requiring confirmation by the source team;
- audits of source class codes and remapping completeness;
- sensitivity to annual persistence rules;
- sensitivity to spatial scale, zoning, and neighborhood definitions.

Accounting closure is an internal consistency test. It does not, by itself, demonstrate that the source classification or class remapping is accurate.

## Repository status

**Current status: Phases 1–8 and the accepted Phase 9 executions are complete; Decision 024 has a recorded technical closure and a subsequent interpretation erratum. Matrix v4.3 is the current integrated evidence edition, incorporating completed sensitivity into P9A035/P9A036 and preserving P9A037; historical source-age statements remain superseded.** The canonical analytical panel contains 199,112 cell-interval observations for 24,889 cells and eight five-year intervals. Comparable mapping and GIS exports are complete. Phase 4 characterized cell-state sequences, multiquinquennial episodes, recurrence, persistence, reversals, and the 2,598-cell high-magnitude `NAT → TMP` cohort. Phase 5 accepted 104 positive and significant combined-domain Global Moran tests. Phase 6 produced the canonical Local Moran/LISA results with 9,999 permutations and multiplicity correction. Phase 7 compared Amazon and Cerrado across all 12 frozen metrics and recomputed 160 biome-specific Global Moran tests under two boundary treatments.

The Phase 7 primary comparison retains all 24,889 cells using the deterministic largest-overlap `primary_biome` assignment. A sensitivity analysis removes the 582 cells overlapping both target biomes. The small differences between the two boundary treatments support the stability of the biome comparison.

Phase 8A created and validated approximately 10,000-ha and 40,000-ha grids and a shifted approximately 20,000-ha grid over the fixed canonical footprint. Phase 8B recomputed consolidation, replenishment, `NAT → TMP` and derived balance and rate metrics directly on those units for all eight intervals. The accepted Phase 8B panel contains 809,800 grid-cell-interval records.

Phase 8C compared these results under criteria frozen before result inspection. All 192 aggregate and 48 temporal comparisons passed, with Spearman correlation equal to 1.0 and identical peak and trough intervals throughout. The shifted 20,000-ha grid was stable under every primary criterion. The 10,000-ha grid had one marginal defined-support failure, while the 40,000-ha grid showed systematic scale sensitivity in conditional-metric coverage and small recent distributional differences for `NAT → TMP`.

Phase 8D recomputed Global Moran's I on all three alternative grids with 9,999 permutations per test. All 120 alternative coefficients were positive and significant after Benjamini-Yekutieli correction; signs and significance were preserved in every comparison. Of 120 interval-level magnitude checks, 119 passed. The sole failure was endpoint `NAT → TMP` on the 40,000-ha grid in 2005–2010, where the absolute difference from the canonical coefficient was 0.102828 against a 0.10 limit. Eight of 30 strict temporal checks failed, mainly for `NAT → TMP`. Thus, the existence and positive direction of global spatial clustering are robust, while exact magnitudes and temporal ordering require scale and zoning qualifications.

Phase 8E completed the MAUP assessment by comparing the location, recurrence and persistence of BH-significant HH clusters. The computation covered 120 alternative-grid maps and 3,487,040 cell-map records. Twenty-one of 30 prespecified grid–metric–window assessments passed. Replenishment, net C–R balance and the bounded C–R index passed all six assessments per metric. Consolidation passed three of six and therefore requires a scale qualification. Endpoint `NAT → TMP` passed none of its six overall assessments: its interval footprints and persistent-HH extent are sensitive to grid scale and zoning, even though many failed comparisons retain high overlap coefficients and therefore represent contraction or expansion around a shared core rather than complete relocation.

Phase 8 is closed because the prespecified robustness tests were completed and their sensitivities were retained as results, not because every comparison passed. The canonical approximately 20,000-ha grid remains the primary analytical support.

Phase 9A authenticated and integrated findings from the preceding phases into a curated 30-statement evidence matrix. Two gaps were retained explicitly for RQ1 and RQ2 rather than being filled by unsupported inference. Phase 9A.1 generated a targeted fixed-1985-pasture-cohort extraction for RQ1 and a source-based PAS→TMP origin accounting for RQ2. Evidence matrix version 2 contains 35 unique statements across RQ1–RQ5, no originally identified evidence gaps, and no causal claims. The subsequently discovered pasture-age defect led to suspension of three dependent findings. Those source-age statements remain historical; the rewritten v4.1 statements replace them after the completed final review. Absence of an `evidence_gap` row in an older matrix is not a clearance of its source-age origin results.

For RQ1, the analysis follows the same fixed baseline pixels at nine reference years; it does not treat endpoint composition as a survival curve or reconstruct pixel-level alternation. Its full-domain baseline population and hashes were explicitly revalidated under Decision 024 on 2026-10-08; per-cell area equivalence and all nine-date summaries passed. The endpoint interpretation remains composition of the fixed cohort, with no independent native-pixel resampling or reconstruction of annual paths. Historical source-age RQ2 origin shares must not be cited as current findings: the public pasture-age asset can reuse code `100` after a pixel leaves and later returns to pasture. Total `PAS → TMP` conversion area is distinct from its source-based origin partition; the accepted corrected-panel comparison reconciled that total within tolerance and preserved non-origin fields exactly.

Phase 9A.2 — TMP terminology harmonization: complete. The preferred English class label is Temporary Crop, with temporary crops in running prose. Stable codes and fields remain unchanged. The terminology-harmonized evidence matrix v3 supersedes v2 for English-language terminology, while v1 and v2 remain immutable provenance records. Version 3 is not a corrected pasture-origin analysis; its P9A035–P9A037 are superseded by the rewritten matrix-v4.1 statements. The v3 file remains unchanged as provenance.

Decision 024 and the approved version-3 remediation plan replace direct attribution from the public pasture-age codes with a project-derived reconstruction of observed pasture spells from annual coverage. The original suspension of P9A035–P9A037 is preserved in the immutable v1 event record. Cumulative v2 appends rescission events for corrected matrix-v4 statements; events-v3 adds the v4.1 interpretation qualifications. The eight-interval reconstruction and RQ2 reassessment are complete, and their arithmetic closure has been validated for both primary 1985–2020 and full-observed 1985–2025 summaries. The eight-interval, 24,889-cell PAS origin-by-endpoint destination and observation-loss accounting has also passed the full-domain closure checks in `docs/validation/canonical_pas_origin_destination_full_closure_v3.md` (Decision 024 criteria 7 and 8). The corrected stock-flow, derived, and integrated panels passed the versioned-panel comparison for criterion 9, preserving non-origin fields exactly; this gate did not independently re-export other raster flows. The full-domain 2024–2025 episode-boundary audit passed criterion 10, and the full-domain code-`1`/reused-code-`100` source-impact and overlap audit passed criterion 11. The fixed-1985 cohort and RQ1 endpoint summaries passed explicit revalidation on 2026-10-08. Criterion 12 and the final versioned evidence/status revisions were accepted in the original review; the [current closure supplement](docs/decisions/024_implementation_closure_v2.md) qualifies its assurance scope and records unexecuted follow-up tasks. Accepted historical files remain available for provenance, while matrix v4.3, the canonical composition figure and the separate window-sensitivity figure provide the current manuscript-facing evidence. Source-age claims and figures remain historical. Other analytical claims remain usable within their existing limitations.

The accepted historical gates and their current scope qualifications are explicit:

- **Validated accounting:** annual observed-spell reconstruction, eight-interval RQ2 reassessment, pooled primary and full-observed arithmetic closure, and eight-interval PAS origin-by-endpoint destination and observation-loss closure for all 24,889 cells per interval (Decision 024 criteria 7 and 8).
- **Validated criterion 9:** corrected v2 stock-flow, derived, and integrated panels, with 199,112 cell-interval records and exact preservation of non-origin fields in the versioned-panel comparison. This is not an independent re-export of every other raster flow.
- **Validated criterion 10:** full-domain entry/termination event accounting for 2024 and 2025, retaining event type, triggering year, and `boundary_adjacent` qualifications.
- **Validated criterion 11:** full-domain source code-`1`/reused-code-`100` impact and pixel-overlap audit.
- **Revalidated RQ1:** unchanged fixed-1985 cohort export, area-equivalent baseline membership per cell, and all 45 endpoint-summary rows; PASS on 2026-10-08.
- **Validated criterion 12:** the final evidence review, 35-row matrix v4, three-finding revision crosswalk, append-only cumulative status events v2, corrected figure, input inventory and hashes are complete. The official semantics of source code `1` remain unconfirmed; the project-derived reconstruction does not depend on that confirmation.
- **Interpretation:** current RQ2 evidence is the matrix-v4.3 observed-spell result, retaining the canonical 1985 definition and recording the completed three-baseline sensitivity. The rescission events apply to those corrected statements; the previous source-age percentages and explanations remain superseded. Pooled conversion areas are sums across intervals rather than unique converted areas.

### Accepted remediation checkpoints

The criterion-9 record is [the corrected panel v2 validation](outputs/validation/pasture_spell_panel_v2/canonical_pasture_spell_panel_v2_validation.json). It reports `decision_024_criterion_9_versioned_panel_comparison: PASS`, 199,112 records, and `nonorigin_fields_preserved_exactly: true`. Source-age fields were replaced by reconstructed observed-spell fields in versioned products, while the historical products remain preserved.

The criterion-10 record is [the full-domain boundary-event validation v2](outputs/validation/pasture_spell_boundary_events_v2/canonical_pasture_spell_boundary_events_validation_v2.json). It covers 24,889 cells and 99,556 cell/event/year records from the saved event raster, with zero raster-event mismatches. Entries and terminations in 2024 and 2025 retain the `temporal_filter_limited` qualification inherited from Decision 022. An ongoing PAS episode in 2025 has no observed subsequent termination.

The criterion-11 [source-impact audit](docs/validation/pasture_age_source_asset_impact_audit_v1.md) passed for the complete 24,889-cell domain. Raw code `1` affected 350 cells and 2,142.786 ha at least once; confirmed reuse of `100` affected 15,828 cells and 9,061,284.261 ha. The same-pixel overlap of the two anomaly types was zero, although 324 cells contained both types in different pixels. These are unique affected areas, distinct from time-integrated ha·year totals. The audit does not establish the official meaning or cause of either source-code behavior.

The [RQ1 fixed-cohort revalidation](docs/validation/canonical_fixed_1985_pasture_cohort_revalidation_v1.md) passed on 2026-10-08. It authenticated the unchanged original export and reproduced the fixed-cohort endpoint summaries, with 2025 remaining diagnostic. It supports retaining RQ1 composition results within their endpoint interpretation. The separate final evidence review authorized corrected matrix-v4 statements; matrix v4.3 supplies their current interpretation qualifications and incorporates the accepted window sensitivity.

Key Phase 9 records are:

- `docs/methods/fixed_1985_pasture_cohort_and_origin_synthesis.md`;
- `docs/results/phase9_rq1_rq2_gap_resolution_findings_v1.md`;
- `docs/validation/phase9_gap_resolution_acceptance_v1.md`;
- `outputs/validation/phase9_gap_resolution_v1/canonical_integrated_evidence_matrix_v2.csv`;
- `outputs/validation/phase9_gap_resolution_v1/canonical_phase9_gap_resolution_validation_v1.json`.
- `spatial/phase9/pasture_spell_series_v1/canonical_pas_tmp_origin_series_reassessment_v1.csv`;
- `spatial/phase9/pasture_spell_series_v1/canonical_pas_tmp_origin_series_reassessment_validation_v1.json`;

The terminology-harmonized evidence matrix v3 is a preserved historical edition; the terminology update alone did not clear its source-age origin findings. The current authority is [matrix v4.3](outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv), also available as a [readable evidence record](outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.md). The current remediation governance records are:

- `docs/decisions/024_reconstruction_of_observed_pasture_spell_age.md`;
- `docs/methods/observed_pasture_spell_age_reconstruction.md`;
- `docs/planning/008_pasture_age_asset_remediation_and_reprocessing_plan_v3.md`;
- `docs/validation/pasture_age_evidence_suspension_v1.md`;
- `docs/validation/canonical_pas_origin_destination_full_closure_v3.md`;
- `docs/validation/pasture_age_source_asset_impact_audit_v1.md`;
- `docs/methods/pasture_age_source_asset_audit.md`;
- `docs/validation/canonical_fixed_1985_pasture_cohort_revalidation_v1.md`;
- `outputs/validation/pasture_spell_panel_v2/canonical_pasture_spell_panel_v2_validation.json`;
- `outputs/validation/pasture_spell_boundary_events_v2/canonical_pasture_spell_boundary_events_validation_v2.json`;
- `outputs/validation/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_validation_v1.json`;
- `outputs/validation/fixed_1985_cohort_revalidation_v1/canonical_fixed_1985_cohort_revalidation_validation_v1.json`;
- `outputs/validation/pasture_age_remediation_v1/canonical_evidence_status_events_v1.csv`.

### Decision 024 closure, interpretation and pending follow-up

The historical [v1 closure](docs/decisions/024_implementation_closure_v1.md) records the 2026-10-08 acceptance under the documented source/execution/panel evidence chain. The [current supplement](docs/decisions/024_implementation_closure_v2.md) and [erratum v4.1](docs/results/decision024_origin_window_erratum_v4_1.md) qualify that scope. Local synthetic checks use extracted source logic with a scalar adapter; they are not native GEE image/reducer execution. The original closure did not have a new independent all-pixel invariant export for criteria 3/5. The completed sensitivity adds native categorical fixtures and full-domain partition/continuity/confirmed-entry counters; auxiliary numerical-age 201 and unrelated boundary-raster checks remain outside this run. **Phases 2–8 were not re-executed**; NAT→TMP and TMP→* raster flows were not independently re-exported. Historical null execution hashes remain null.

The qualified primary PAS→TMP split remains **46.91% continuous baseline-1985 spell / 53.09% observed post-1985 entry**, with **62.568807 ha unresolved (0.000311%)**, from 20.119468 million ha of interval conversions. In 2015–2020 it is 31.08%/68.92%. Pooled areas may count the same pixel across intervals; observed entry includes re-entry and is not first-ever establishment.

**1985–1990 is 100% initial by construction.** 1985 is an observation boundary, not a process origin. The trajectory and the first >50% entry share in 2000–2005 depend on that window and do not identify a process threshold or demonstrate a regime change. The [current figure](figures/decision024_review_v1/fig02_pas_tmp_origin_composition_v4_1.png) and [current caption](figures/decision024_review_v1/fig02_pas_tmp_origin_composition_v4_3_caption.md) make that boundary explicit. See [current corrected findings](docs/results/canonical_pas_tmp_origin_corrected_findings_v5.md) and the [events-v5 index](outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv).

The [supplementary PAS→NAT summaries](docs/results/canonical_pas_nat_origin_supplementary_findings_v1.md) are now produced and authenticated; they do not expand RQ2. Qualified numerical description can proceed. The three-baseline window-start sensitivity is now complete with native pilot and full validation PASS. The [plan 009 execution addendum](docs/planning/009_window_sensitivity_execution_addendum_v1.md) records completed categorical assurance and the then-pending entry/re-entry decomposition, numerical-age 201 assurance and uncertain-pair cross-tab. The uncertain-pair cross-tab now has accepted native pilot and full-domain validation, as recorded below. Those remaining analyses must not be presented as completed. A [partial DOI-release inventory](config/public_release_decision024_required_files_v1.csv) now explicitly requires the eight cell CSVs and corrected v2 Parquets. Those large data files are external to this compact GitHub ZIP; public DOI access and release-byte verification are pending.

### Observation-window sensitivity — full validation accepted

**Current status, 2026-10-12: native pilot and full-domain window sensitivity PASS.** The 48 new cell tables and full run manifest have been validated against the eight accepted reference CSVs and the accepted pilot. The normalized panel contains 19 baseline/interval populations on 24,889 cells, totaling 472,891 rows: 423,113 new native rows and 49,778 explicitly labeled reused early b=1985 rows. Native categorical/field invariants are zero in the new exports; no new native counters are invented for reused data. Maximum reference/control difference is 3.28e-7 ha per cell. Runtime projection/configuration, accounting, set nesting and continuous-stock membership checks passed.

On identical 2000–2020 endpoint conversions (15.221177 Mha summed by interval), baseline-continuous origin is 38.10% with baseline 1985, 64.70% with baseline 1995 and 78.07% with baseline 2000. The first four intervals of every baseline begin at 100% initial by construction and then decline, but their conversion-share curves differ. The primary >50% observed-entry crossing occurs in 2000–2005 only under baseline 1985; the two later baselines cross only in the diagnostic 2020–2025 interval. Thus origin shares and crossing descriptors remain observation-window-conditioned. No artifact fraction, stationarity or process threshold is identified.

See [full scientific findings](docs/results/window_origin_sensitivity_full_findings_v1.md), [native validation](docs/validation/window_origin_sensitivity_full_validation_v1.md), [method v2](docs/methods/window_origin_sensitivity_v2.md), [machine-readable validation](outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_sensitivity_validation_v1.json), and [the figure and caption](figures/window_origin_sensitivity_v1/fig01_window_origin_sensitivity_v1_caption.md). The five compact validator summaries and additional review tables are included here; the 472,891-row panel and native CSVs are delivered separately in the data package, with hash inventories. [Reproduction and package instructions](RUN_REPRODUCE_PT.md) distinguish repository files from external data.

The corrected scripts retain the projection-metadata fix and supplied code snapshot hashes. Executed remote text is not independently authenticated, and no operator hash attestation was supplied. Matrix v4.1 is preserved as the preceding edition. Matrix v4.3 is current, retaining the completed sensitivity and adding stock-normalized endpoint fractions and explicit set-nesting interpretation. First-entry/re-entry decomposition, auxiliary numerical-age 201 tests and public DOI release remain separate pending tasks. The uncertain-pair endpoint cross-tab is now fully validated, as recorded below. Phases 2–8 were not re-executed in this sensitivity.

### Preceding scientific consolidation — evidence matrix v4.2

**Preceding edition, 2026-10-12: v4.2 consolidation retained as provenance. Current authority is v4.3 below.** [Matrix v4.2 CSV](outputs/summary/rq2_evidence_consolidation_v4_2/canonical_integrated_evidence_matrix_v4_2.csv) and [readable matrix](outputs/summary/rq2_evidence_consolidation_v4_2/canonical_integrated_evidence_matrix_v4_2.md) preserve 35 finding IDs and the existing schema. Only P9A035/P9A036 change substantive content; P9A037 and the other 32 findings are unchanged except for the edition identifier. Canonical b1985 numerical sources and hashes remain unchanged. Both revised findings stay qualified, now with completed boundary-sensitive validation rather than sensitivity-not-executed status. All causal flags remain zero.

The [scientific consolidation record](docs/results/rq2_evidence_consolidation_v4_2.md), [source-to-claim inventory](config/rq2_evidence_v4_2_source_inventory_v1.csv), [structured numerical claims](outputs/summary/rq2_evidence_consolidation_v4_2/canonical_rq2_numerical_claims_v4_2.json), [field crosswalk](outputs/summary/rq2_evidence_consolidation_v4_2/canonical_evidence_matrix_v4_1_to_v4_2_crosswalk_v1.csv), and [validation record](outputs/validation/rq2_evidence_consolidation_v4_2/canonical_rq2_evidence_consolidation_validation_v1.json) connect the new statements to accepted exports. [Events-v4](outputs/validation/rq2_evidence_consolidation_v4_2/canonical_evidence_status_events_v4.csv) retains the eight historical events byte-for-byte and adds two supplementary-evidence events, without a suspension, rescission or status promotion.

[Complete proposed Methods, Results and Discussion wording](manuscript/results/rq2_observed_pasture_spell_origins_v4_2.md) is ready for integration into the manuscript. No full manuscript file was supplied or edited. The qualified descriptive RQ2 wording retains the observation boundary, first-interval construction, observed-entry/re-entry semantics, distinct pooling comparisons and diagnostic extension. It does not identify an artifact fraction, stationarity, physical establishment age or a process threshold. The canonical image remains unchanged, with a new caption; the separate sensitivity figure is retained.

This closes the specified sensitivity and its incorporation into the scientific evidence. The next release task is public data-package preparation and DOI deposition. First-entry/re-entry decomposition and auxiliary age 201 remain distinct optional/claim-dependent follow-ups, not declared completed. The uncertain-pair cross-tab has now passed full validation. See [package instructions](UPLOAD_INSTRUCTIONS.md).

### Current RQ2 interpretation — matrix v4.3 and endpoint fractions

**Current matrix: v4.3. Current cumulative events: v5; v1–v4 are historical cumulative editions.** The [new matrix](outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv) updates only P9A035/P9A036; the other 33 substantive findings, qualified statuses, zero causal flags and all canonical anchors/hashes are preserved. [Evidence navigation](docs/results/EVIDENCE_NAVIGATION.md) identifies which document to cite for each purpose.

The [new 19-row derivative](outputs/summary/rq2_relative_conversion_v1/canonical_relative_endpoint_conversion_fractions_v1.csv) reports class stock at t0, endpoint conversion area, both class fractions, their initial/entry ratio and missing-value reasons. National ratios divide summed areas, not averages of cell ratios. There are 16 estimable ratios; the first interval of each baseline has zero entry stock and an undefined ratio. Estimable primary ranges are 1.1674–1.3979 (b1985), 1.0046–1.1964 (b1995) and 0.8164–1.1016 (b2000); diagnostics are 0.8072, 0.7209 and 0.6712. The b1985/b1995 primary ratios fluctuate; the three b2000 primary ratios increase. These are stock-at-t0 endpoint fractions, not annual hazards, exposure-adjusted risks or causal effects.

Calendar-paired monotonicity of initial origin follows set nesting. Its direction alone cannot support a changing process. Magnitude describes reclassification; matched-follow-up and stock/conversion contrasts provide complementary descriptions while changing periods/cohorts. The origin-share ratio factorizes algebraically into stock ratio and endpoint-fraction ratio; no causal artifact fraction is estimated. See [method](docs/methods/relative_endpoint_conversion_fractions_v1.md), [findings](docs/results/rq2_relative_conversion_findings_v1.md), [short English synthesis](docs/results/window_origin_sensitivity_full_findings_en_v1.md), [updated manuscript wording](manuscript/results/rq2_observed_pasture_spell_origins_v4_3.md), and [new figure](figures/rq2_relative_conversion_v1/fig01_relative_endpoint_conversion_v1.png).

[Legacy hash meanings](docs/validation/legacy_hash_field_dictionary_v1.md) clarify `rq2_validation_sha256` without editing v3 JSONs. [Operator-addendum instructions](docs/validation/operator_execution_addendum_instructions_v1.md) and the recording tool are prepared; no operator attestation has been supplied, so the original executed-script hash remains null. [The coordinated native protocol](docs/planning/009_joint_native_followup_protocol_v1.md) remains the umbrella plan. The uncertain-pair native pilot and full-domain validation are now accepted, as described below. Entry/re-entry and auxiliary numerical-age 201 now have an accepted native pilot, described below; complete-domain execution remains pending. [Release preparation](docs/planning/007_release_preparation_addendum_v2.md) supplies a partial known-product inventory and byte verifier; three Parquet byte checks and complete Stage 0 scope remain pending. No DOI is minted.

### Annual uncertain-pair cross-tab — full-domain validation accepted

**2026-10-21: native pilot preserved; full-domain validation PASS.** The unchanged [validator](analysis/19b_validate_uncertain_pair_crosstab_v1.py), executed with `--scope full`, accepted all nine received CSVs: eight batches containing **49,778 rows on 24,889 cells** for 2023→2024 and 2024→2025, plus the full manifest. The exact accepted 34-case pilot synthetic CSV was reused as the tenth validation input. No pilot or GEE task was rerun. All original pilot bytes, scripts, configuration and historical machine reports are retained.

Exact inventories, canonical cell/batch assignments, 41 annual coverage bands, native projections, runtime constants, all area partitions and all 149,334 actual raster error-counter values passed. The 204 error values in the 34 reused native fixtures are zero. The eight historical uncertain/entry/termination controls reproduce the accepted boundary summary within 0.001 ha; the largest absolute difference is **0.000005024 ha**. A supplementary comparison also matched the four real pilot rows to the complete output, with a maximum metric difference of 3.64 × 10⁻¹² ha.

| Annual pair | All-class uncertain area (ha) | Uncertain with previous PAS (ha) | Uncertain with current PAS (ha) | Observed PAS share of uncertain area (%) |
|---|---:|---:|---:|---:|
| 2023→2024 | 4,688,518.256609 | 11.914080 | 9.019542 | 0.00044649 |
| 2024→2025 | 4,688,463.670441 | 6.205013 | 12.186375 | 0.00039227 |

Observed PAS at either endpoint accounts for **20.933621 ha** and **18.391388 ha**, respectively. Almost all uncertain area is masked at both endpoints: **99.99656962%** in 2023→2024 and **99.99791799%** in 2024→2025. All nonzero uncertain classes involve masking; NODATA and unexpected-code categories are zero. “No observed PAS” does not establish true non-pasture coverage under the masks or absence of pasture in other years. The geographic or technical cause of the masked area is not established here. The two annual areas are not a unique spatial union and must not be added as such. The ~4.69 Mha uncertainty and 62.568807 ha unresolved pasture-origin conversion retain their distinct populations and temporal definitions.

See [full acceptance](docs/validation/uncertain_pair_crosstab_full_acceptance_v1.md), [scientific interpretation](docs/results/uncertain_pair_crosstab_full_findings_v1.md), [machine validation](outputs/validation/uncertain_pair_crosstab_v1/full/canonical_uncertain_pairs_full_v1_validation.json), [supplementary review](outputs/validation/uncertain_pair_crosstab_v1/full/received_full_review_v1.json), and [reproduction instructions](RUN_VALIDATE_UNCERTAIN_PAIRS_FULL_PT.md). The [method](docs/methods/uncertain_pair_crosstab_v1.md) records support and denominators. Native full CSVs and all five validator-derived tables are included. The [pilot acceptance](docs/validation/uncertain_pair_crosstab_pilot_acceptance_v1.md) remains unchanged. Earlier implementation and handoff JSONs retain their dated historical status; the new full report is current for this step.

Acceptance concerns operator-provided exports and aggregate historical reproduction. There was no independent new boundary-raster comparison or independently witnessed remote execution. Supplied script hashes are pinned; executed-text hashes and operator attestation remain null. This coverage-only step is independent of the targeted age-v2 audit below and does not migrate analytical origin to the new age asset. **Matrix v4.3 and events-v5 remain current and unchanged.** The uncertain-pair component of item 3.6 is complete. Entry/re-entry chronology, numerical-age 201, historical operator attestation and public DOI deposition retain their previous scope/status.


### First observed entry versus observed re-entry — native pilot accepted

**2026-10-21: complete revision-r2 native pilot PASS; full-domain decomposition PENDING.** The [acceptance record](docs/validation/entry_reentry_pilot_acceptance_v1.md) validates all four received CSVs: four cell/interval rows, two 1985–2025 historical-audit rows, 31 native synthetic histories covering 302 steps, and one manifest. The supplied code and all native bytes remain unchanged. The earlier browser fix is retained; usable r2 exports have now been returned, but no browser-performance measurement was supplied.

All 496 native fixture error values, 20 actual historical invariant values and four accepted-origin pixel mismatch values are zero. Runtime constants, exact cell/grid/batch identities, interval flags, 41 bands and 41 native CRS/transforms pass. All 32 historical stock/flow/origin controls reconcile, with maximum absolute per-cell difference **1.82 × 10⁻¹² ha**. An additional comparison with the accepted uncertain-pair pilot reproduces eight 2024/2025 cell/event areas within **5.69 × 10⁻¹⁴ ha**; no new event-raster comparison is claimed.

| Pilot interval | Accepted post-1985-entry PAS→TMP (ha) | First observed entry (ha) | Observed re-entry (ha) | Re-entry share of entry flow (%) |
|---|---:|---:|---:|---:|
| 2015–2020 | 15,654.720431 | 14,643.967411 | 1,010.753020 | 6.456538 |
| 2020–2025, diagnostic | 924.391309 | 845.722341 | 78.668968 | 8.510353 |

The denominator is the accepted post-1985-entry component, not total PAS→TMP. Continuous initial-episode flow remains separate. Prior-history uncertainty and unresolved origin are zero in these pilot flows; gap cases pass in native fixtures. These two cells do not support domain-wide shares or a temporal trend. First observed entry is limited to the window starting in 1985, not first-ever establishment.

See [pilot findings](docs/results/entry_reentry_pilot_findings_v1.md), [unchanged native validator report](provenance/entry_reentry_pilot_r2/outputs/validation/entry_reentry_v1/pilot_r2/canonical_entry_reentry_pilot_v1_validation.json), [additional receipt review](provenance/entry_reentry_pilot_r2/outputs/validation/entry_reentry_v1/pilot_r2/received_pilot_review_v1.json), [method](docs/methods/entry_reentry_auxiliary_decomposition_v1.md), and [current Plan 009 addendum](docs/planning/009_entry_reentry_pilot_acceptance_addendum_v1.md). The [software verification](docs/validation/entry_reentry_implementation_verification_v1.md) and [r2 browser-fix record](docs/validation/entry_reentry_browser_freeze_fix_r2.md) retain their earlier local-stage status. The new native acceptance supplements those records.

The full-domain implementation and complete historical controls are now prepared, as described below, preserving this accepted pilot and the unchanged recurrence. The complete domain and full-domain auxiliary-age assurance remain pending. The accepted pilot package is preserved unchanged under `provenance/entry_reentry_pilot_r2/`; this handoff adds a separate full exporter. **Matrix v4.3/events-v5 and the analytical accounting remain unchanged.** Supplied script hashes are pinned; independently authenticated executed-text hash and operator attestation remain null.


### First-entry/re-entry full execution — native validation accepted

**2026-10-23: full-domain native PASS.** The unchanged [full validator](analysis/20d_validate_entry_reentry_full_v1.py) accepted 64 interval/batch tables, eight history audits and one manifest: **199,112 cell/interval records on 24,889 cells**, plus 24,889 audits covering 1985–2025. All 248,890 actual historical-error values and 199,112 accepted-origin pixel-error values are zero. Runtime metadata, exact inventories, stock/flow partitions and auxiliary-age recurrence checks pass.

All **1,592,896** historical per-cell field comparisons pass (maximum difference 3.7998e-07 ha); all 64 aggregate controls pass (maximum difference 3.59118e-06 ha). All 126 controls against the unchanged accepted native pilot pass. The pilot's 31 native fixture histories / 302 steps are preserved and revalidated without re-export. Complete-domain decomposition and auxiliary age-201 flags are now true in the unchanged machine JSON.

Observed re-entry contributes **516,010.727646 ha / 19.117876%** of post-1985-entry PAS→TMP flow in 2015–2020 and **541,458.935683 ha / 32.488051%** in diagnostic 2020–2025. The denominator is the accepted entry component, not total PAS→TMP. Full eight-interval flow and stock results are in [domain findings](docs/results/entry_reentry_full_findings_v1.md). First observed entry is window-specific since 1985, not first-ever establishment. Baseline entry fractions remain blank because their denominator is zero.

See [acceptance](docs/validation/entry_reentry_full_acceptance_v1.md), [unchanged machine report](outputs/validation/entry_reentry_v1/full/canonical_entry_reentry_full_v1_validation.json), [receipt/scope review](outputs/validation/entry_reentry_v1/full/received_full_review_v1.json), [reproduction](RUN_ENTRY_REENTRY_FULL_PT.md) and [current Plan 009 addendum](docs/planning/009_entry_reentry_full_acceptance_addendum_v1.md). Original implementation and handoff documents retain their historical status. All critical code/configuration/reference and preserved-pilot bytes remain unchanged.

This acceptance concerns operator-supplied coverage-derived accounting exports and auxiliary-age checks; no full public pasture-age asset validation, remote executed-text authentication or new event-raster comparison is claimed. **Matrix v4.3/events-v5 and canonical accounting remain unchanged.** Next is coordinated scientific incorporation of this decomposition; no new GEE run is needed for the accepted step.

### New pasture-origin-age v2 source — targeted domain audit accepted

**2026-10-20: targeted audit ACCEPTED on 21,869 selected cells, 1985–2025; 82-cell coverage qualification resolved.** The [acceptance record](docs/validation/pasture_v2_targeted_domain_audit_acceptance_v1.md) and [native validation](outputs/validation/pasture_v2_coverage_recheck82_v3/pasture_v2_coverage_recheck82_20261020151405_v3_validation.json) document the complete 82-cell native recheck, zero missing reductions, passing native fixtures and agreeing direct/collection results on the single real preflight cell. The [combined panel](outputs/validation/pasture_v2_coverage_recheck82_v3/pasture_v2_coverage_recheck82_20261020151405_v3_combined_cells.csv) labels 82 rechecked rows and 21,787 unchanged reused rows from the eight accepted parent CSVs. Those parent files and their validation remain unchanged; this is not a fresh full-domain raster execution.

Literal age 1, age 100 after observed non-PAS, ordered reuse of 100, unconfirmed initial 100, age/coverage inconsistencies, unavailable or zero PAS age, unexpected age codes and remaining unknown coverage all have **zero cell-occurrence flags** under the audited rules. PAS is present in 21,036 cells, age family 100 in 16,004, family 2xx in 21,033 and valid coverage in all 21,869. Counts are cells with some occurrence, not hectares, pixels or events; this does not validate every numerical age.

The earlier coverage-list qualification is fully explained by codes 75 and/or 91: 60 cells have 75, 24 have 91 and two have both. All 82 changed flag values concern `coverage_unknown_code`, from 1 to 0; other flags are unchanged. The [code-pattern table](outputs/summary/pasture_v2_targeted_audit_closure_v1/coverage_code_patterns_82cells_v1.csv) records the disjoint counts. Coverage 27 remains NODATA, and coverage code 1 remains distinct from age code 1.

**No additional run of the 82 cells or the eight parent batches is needed.** Reproduce acceptance with [the v3 validator](analysis/validate_pasture_v2_recheck82_v3.py) and the archived [native CSV](outputs/native/pasture_v2_coverage_recheck82_v3/pasture_v2_coverage_recheck82_20261020151405_v3.csv). The [original review](docs/results/pasture_v2_domain_targeted_audit_review_v1.md), [all-null rejection](docs/results/pasture_v2_recheck82_null_return_and_real_geometry_fix_v3.md), [API correction](docs/results/pasture_v2_recheck82_feature_set_fix_v3_1.md) and earlier failed returns remain historical provenance. Current executable code is revision v3.1 of the v3 CSV protocol; distributed-script hashes do not substitute for the still-null operator execution-text attestation.

**Matrix v4.3/events-v5 and canonical accounting remain unchanged.** The selected 21,869-cell grid differs from the canonical 24,889-cell support. Reuse assumes unchanged contents of referenced assets; remote raster bytes are not independently hashed. This closes the specified coding/consistency audit only. Numerical-age 201 native assurance, entry/re-entry chronology, annual uncertain-pair full-domain validation and public DOI release remain separate. No national absence claim, complete numerical-age validation or canonical source migration is made. See [Portuguese result and next step](RESULTADO_E_PROXIMO_PASSO_PT.md).

### Superseded products and historical status

| Historical product | Current use or replacement |
|---|---|
| Source-age matrix v3, original P9A035–P9A037, gap-resolution findings and source-age figures | Preserved provenance; current origin evidence is matrix v4.3. The retired 51.73%/48.27% split must not be cited as current. |
| Corrected matrices v4/v4.1 and origin figure v4 | Numerical sources unchanged; interpretation edition v4.3 and its updated caption are current. |
| Status-event v1/v2/v3/v4 | Historical cumulative editions; current events-v5 preserves all events-v4 bytes and appends two endpoint-fraction events. |
| Plan 008 without suffix (v2) | Superseded by plan 008 v3; retained at its path with a status banner to preserve old links. |
| Plan 008 v3 and dated checkpoints/audits/closure v1 | Body retains historical statuses; banner points to closure v2 and erratum v4.1. |
| 17x and original closure validation JSON | Reproduce against the original closure ZIP; 17z checks this updated package using archived original document bytes. |

Original texts before the navigation banners are archived under `docs/history/decision024_pre_errata_v1/` and mapped by [the historical snapshot inventory](outputs/validation/decision024_review_v1/canonical_historical_document_snapshot_map_v1.csv). This retains byte-level provenance while making current status discoverable. The normative methods document is updated to the current status rather than preserving obsolete future-tense instructions.

The repository is being organized from the ground up. Historical scripts and preliminary outputs may be used as diagnostic references, but only the validated canonical pipeline and its reproduced outputs will be treated as authoritative.

The continuing repository consolidation prioritizes:

1. a single version-controlled processing chain;
2. complete exports for the fixed analytical domain;
3. separation of interval flows from fixed-cohort trajectories;
4. formal accounting audits;
5. temporal and spatial sensitivity analyses;
6. reproducible figures, tables, and manuscript results.

## Planned repository structure

The structure below is provisional and will evolve with the reconstruction:

```text
pasture-crop-dynamic/
├── README.md
├── config/          # Canonical parameters, classes, assets, and versions
├── gee/             # Google Earth Engine processing scripts
├── analysis/        # Statistical and spatial analysis code
├── docs/            # Methods, decisions, limitations, and data dictionaries
├── outputs/         # Reproducible tables and figure-ready results
├── figures/         # Final figures and maps
└── manuscript/      # Manuscript-facing material
```

Large source rasters, restricted assets, and temporary processing files should not be committed to the repository. Their provenance and access requirements will instead be documented.

## Reproducibility

Reproducibility requirements include:

- pinned data-product versions;
- centralized constants and class definitions;
- explicit spatial projection and transform parameters;
- documented Earth Engine asset dependencies;
- deterministic output naming;
- per-stage validation logs;
- traceability from manuscript figures and tables back to source scripts and outputs.

## Interpretation boundaries

This project measures spatial and temporal associations among land stocks and land-cover transitions. It does not, in its current design, identify causal effects of commodity prices, infrastructure, environmental policies, land tenure, or legal restrictions.

Any explanatory covariates incorporated later will initially be interpreted descriptively unless accompanied by an appropriate causal design.

## Citation

Citation information will be added when a stable release or manuscript preprint becomes available.

## License

The code and documentation in this repository are released under the MIT License. Source datasets and external products remain subject to their respective licenses and terms of use.

## Contact

**Mario Barroso Ramos Neto**  
Project lead and repository maintainer

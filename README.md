# Pasture–Crop Dynamics in the Brazilian Cerrado and Amazon

## Overview

This repository supports a research project on the long-term dynamics among native vegetation, planted pasture, and temporary crops in the Brazilian Cerrado and Amazon.

The project moves beyond net land-cover change to examine **directed flows**, **land-stock origins**, and **conversion pathways**. Its central purpose is to determine how pre-existing pasture stocks and newly established pastures contribute to agricultural consolidation across space and time.

The canonical workflow has been reproduced and validated through the complete MAUP assessment and integrated evidence review. It includes the study domain, five-year stock-and-flow and annual `NAT → TMP` trajectory panels, integrated cell-by-interval metrics, fixed spatial support and contiguity graph, comparable map classes, cell-state trajectories, temporal synthesis, Global Moran, Local Moran/LISA, biome-specific comparisons, alternative-grid metric reconstruction, prespecified comparison of aggregate values and weighted cell distributions, Global Moran sensitivity, broad HH-cluster location and persistence robustness, a fixed-1985-pasture-cohort endpoint analysis, and an authenticated evidence matrix. Phases 1–8 and the execution of Phase 9A/9A.1 have been accepted; Phase 9A.2 terminology harmonization is complete. Pasture-origin findings P9A035–P9A037 are now suspended pending reconstruction and validation of observed pasture spells. Other accepted evidence remains subject to a downstream invariance check.

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

Any confidently observed exit from pasture, including `PAS → NAT`, ends the spell. A missing observation breaks confirmed continuity without proving an exit. This classification describes the *current observed spell*, not the first-ever establishment of pasture at a location. The `PAS → TMP` origin composition addresses RQ2; applying the same classification to `PAS → NAT` is supplementary and does not expand that research question. Corrected origin outputs are pending implementation and validation.

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

For each cell and interval, the workflow quantifies focal transitions, persistence, auxiliary destinations, masked areas, and pasture-to-temporary-crop conversion. The accepted source-based origin partition remains a provenance record, but its findings are suspended pending the corrected reconstruction.

The principal origin identity is:

```text
PAS→TMP total = left-censored continuous 1985 episode
              + observed post-1985 entry episode
              + unresolved episode origin
```

### 2. Fixed 1985 pasture cohort

The previously accepted RQ1 extraction fixed the pixel cohort using pasture coverage class `15` and source pasture-age code `100` in 1985. The same pixels are reclassified at the nine reference years from 1985 through 2025. The number and identity of cohort pixels remain fixed; only their endpoint distribution among land-cover states changes. Decision 024 requires revalidation of this baseline definition and cohort hashes; cohort membership and the origin of a *later* pasture spell are different analytical objects.

This component measures endpoint-state composition, not uninterrupted persistence or pixel-level alternation. Because the exported results are aggregated by cell, they do not identify a unique sequence of transitions for individual pixels between reference years. The previously accepted extraction contains 49.036 million ha in 16,421 canonical cells. At the 2020 endpoint, 63.13% is classified as pasture, 19.94% as temporary crops, 9.22% as other agriculture, and 6.82% as native vegetation. The 2025 endpoint is included as a diagnostic extension. These RQ1 results are expected to remain valid but must pass the specified revalidation gate.

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
- source pasture-age code and mask audits for provenance, including the overlap of codes `1` and reused `100`;
- audits of source class codes and remapping completeness;
- sensitivity to annual persistence rules;
- sensitivity to spatial scale, zoning, and neighborhood definitions.

Accounting closure is an internal consistency test. It does not, by itself, demonstrate that the source classification or class remapping is accurate.

## Repository status

**Current status: Phases 1–8 are complete; Phase 9A/9A.1 executions were accepted, but three pasture-origin findings are suspended; Phase 9A.2 terminology harmonization is complete.** The canonical analytical panel contains 199,112 cell-interval observations for 24,889 cells and eight five-year intervals. Comparable mapping and GIS exports are complete. Phase 4 characterized cell-state sequences, multiquinquennial episodes, recurrence, persistence, reversals, and the 2,598-cell high-magnitude `NAT → TMP` cohort. Phase 5 accepted 104 positive and significant combined-domain Global Moran tests. Phase 6 produced the canonical Local Moran/LISA results with 9,999 permutations and multiplicity correction. Phase 7 compared Amazon and Cerrado across all 12 frozen metrics and recomputed 160 biome-specific Global Moran tests under two boundary treatments.

The Phase 7 primary comparison retains all 24,889 cells using the deterministic largest-overlap `primary_biome` assignment. A sensitivity analysis removes the 582 cells overlapping both target biomes. The small differences between the two boundary treatments support the stability of the biome comparison.

Phase 8A created and validated approximately 10,000-ha and 40,000-ha grids and a shifted approximately 20,000-ha grid over the fixed canonical footprint. Phase 8B recomputed consolidation, replenishment, `NAT → TMP` and derived balance and rate metrics directly on those units for all eight intervals. The accepted Phase 8B panel contains 809,800 grid-cell-interval records.

Phase 8C compared these results under criteria frozen before result inspection. All 192 aggregate and 48 temporal comparisons passed, with Spearman correlation equal to 1.0 and identical peak and trough intervals throughout. The shifted 20,000-ha grid was stable under every primary criterion. The 10,000-ha grid had one marginal defined-support failure, while the 40,000-ha grid showed systematic scale sensitivity in conditional-metric coverage and small recent distributional differences for `NAT → TMP`.

Phase 8D recomputed Global Moran's I on all three alternative grids with 9,999 permutations per test. All 120 alternative coefficients were positive and significant after Benjamini-Yekutieli correction; signs and significance were preserved in every comparison. Of 120 interval-level magnitude checks, 119 passed. The sole failure was endpoint `NAT → TMP` on the 40,000-ha grid in 2005–2010, where the absolute difference from the canonical coefficient was 0.102828 against a 0.10 limit. Eight of 30 strict temporal checks failed, mainly for `NAT → TMP`. Thus, the existence and positive direction of global spatial clustering are robust, while exact magnitudes and temporal ordering require scale and zoning qualifications.

Phase 8E completed the MAUP assessment by comparing the location, recurrence and persistence of BH-significant HH clusters. The computation covered 120 alternative-grid maps and 3,487,040 cell-map records. Twenty-one of 30 prespecified grid–metric–window assessments passed. Replenishment, net C–R balance and the bounded C–R index passed all six assessments per metric. Consolidation passed three of six and therefore requires a scale qualification. Endpoint `NAT → TMP` passed none of its six overall assessments: its interval footprints and persistent-HH extent are sensitive to grid scale and zoning, even though many failed comparisons retain high overlap coefficients and therefore represent contraction or expansion around a shared core rather than complete relocation.

Phase 8 is closed because the prespecified robustness tests were completed and their sensitivities were retained as results, not because every comparison passed. The canonical approximately 20,000-ha grid remains the primary analytical support.

Phase 9A authenticated and integrated findings from the preceding phases into a curated 30-statement evidence matrix. Two gaps were retained explicitly for RQ1 and RQ2 rather than being filled by unsupported inference. Phase 9A.1 generated a targeted fixed-1985-pasture-cohort extraction for RQ1 and a source-based PAS→TMP origin accounting for RQ2. Evidence matrix version 2 contains 35 unique statements across RQ1–RQ5, no originally identified evidence gaps, and no causal claims. The subsequently discovered pasture-age defect suspends the three dependent findings; absence of an `evidence_gap` row in the historical matrix must not be read as current clearance of RQ2.

For RQ1, the analysis follows the same fixed baseline pixels at nine reference years; it does not treat endpoint composition as a survival curve or reconstruct pixel-level alternation. Its baseline population and hashes will be revalidated during remediation. Previously reported RQ2 origin shares must not be cited as accepted findings: the public pasture-age asset can reuse code `100` after a pixel leaves and later returns to pasture. Total `PAS → TMP` conversion area is distinct from its source-based origin partition and is expected to remain invariant, subject to a formal check.

Phase 9A.2 — TMP terminology harmonization: complete. The preferred English class label is Temporary Crop, with temporary crops in running prose. Stable codes and fields remain unchanged. The terminology-harmonized evidence matrix v3 supersedes v2 for English-language terminology, while v1 and v2 remain immutable provenance records. Version 3 is not a corrected pasture-origin analysis; findings P9A035–P9A037 within it are suspended.

Decision 024 and the approved version-3 remediation plan replace direct attribution from the public pasture-age codes with a project-derived reconstruction of observed pasture spells from annual coverage. Findings P9A035, P9A036, and P9A037 are formally suspended in a versioned event record. The 2015–2020 pilot, full eight-interval reprocessing, source-impact audit, RQ1 revalidation, and downstream invariance gate are pending. Accepted historical files remain available for provenance; corrected outputs and validation reports are not yet available. Manuscript-facing synthesis of pasture-origin shares must wait for their acceptance. Other analytical claims remain usable within their existing limitations and subject to the invariance gate.

Key Phase 9 records are:

- `docs/methods/fixed_1985_pasture_cohort_and_origin_synthesis.md`;
- `docs/results/phase9_rq1_rq2_gap_resolution_findings_v1.md`;
- `docs/validation/phase9_gap_resolution_acceptance_v1.md`;
- `outputs/validation/phase9_gap_resolution_v1/canonical_integrated_evidence_matrix_v2.csv`;
- `outputs/validation/phase9_gap_resolution_v1/canonical_phase9_gap_resolution_validation_v1.json`.

The terminology-harmonized evidence matrix is `spatial/phase9/terminology_harmonization_v1/canonical_integrated_evidence_matrix_v3.csv`; its three suspended pasture-origin findings are not cleared by the terminology update. The current remediation governance records are:

- `docs/decisions/024_reconstruction_of_observed_pasture_spell_age.md`;
- `docs/methods/observed_pasture_spell_age_reconstruction.md`;
- `docs/planning/008_pasture_age_asset_remediation_and_reprocessing_plan_v3.md`;
- `docs/validation/pasture_age_evidence_suspension_v1.md`;
- `outputs/validation/pasture_age_remediation_v1/canonical_evidence_status_events_v1.csv`.

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

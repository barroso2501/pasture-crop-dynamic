# Plan 007 — Public data release and dual-manuscript pathway (ESSD and Land Use Policy)

* **Status:** Accepted for implementation, as amended by Decision 023. Stage 0 has not yet been executed.
* **Date:** 2026-09-23
* **Last amended:** 2026-09-23
* **Scope:** preparation of a coherent public data release, submission of a data-description manuscript to *Earth System Science Data* (ESSD), and submission of a distinct analytical and policy-facing manuscript to *Land Use Policy* (LUP)
* **Precondition:** analytical Phases 1–9A.2 and their accepted validation records remain the scientific basis of the publication pathway
* **Related decisions:** 009, 010, 014–023

## 1. Purpose

The project has produced more than a set of manuscript results. It has produced a documented spatial–temporal data system containing canonical spatial support, stock–flow accounting, trajectory classifications, fixed-cohort reconstructions, pathway partitions, spatial statistics, and sensitivity analyses. The publication strategy will therefore separate two legitimate and complementary contributions:

1. an openly archived, versioned, reusable, and validated data product, with ESSD as the preferred data-description venue; and
2. an analytical article in LUP that uses the released product to answer the research questions and develop their land-use-policy implications.

This separation is not based merely on manuscript length. It reflects two different scholarly objects: the **data product and its fitness for reuse**, and the **substantive interpretation and policy contribution derived from that product**.

The public release is a scientific product independently of the editorial outcome at ESSD. If the ESSD-fit checkpoint defined in Section 4.4 recommends a different data-publication venue, the release and the LUP pathway remain valid; only the destination of the data-description manuscript changes.

## 2. Governing principles

1. **The public release is a designed product, not a dump of project outputs.** Only canonical, documented, reusable files will be included.
2. **Accepted provenance is preserved.** Existing accepted records remain immutable. Public-release files are versioned derivatives with explicit links to their canonical sources.
3. **One result has one primary manuscript home.** A claim, table, or figure may be cited by both manuscripts, but its full presentation belongs primarily to only one.
4. **The ESSD manuscript is data-centred.** Its principal questions are how the data were constructed, validated, structured, and made reusable.
5. **The LUP manuscript is inference- and policy-centred.** Its principal questions are what the patterns mean and how they inform land-use monitoring, governance, and policy.
6. **Terminology is harmonized before release.** Human-readable English uses `temporary crops`, not `temporary agriculture`; machine-readable codes remain stable.
7. **Temporal-boundary and spatial-sensitivity limitations are first-class metadata.** Left censoring, right censoring, temporal-filter limitations, classification uncertainty, and MAUP sensitivity must not be confined to narrative caveats.
8. **The DOI release is immutable.** Corrections after release create a new version; the LUP manuscript cites the exact dataset version used.
9. **The release is venue-resilient.** Its scientific value and minimum contents do not depend on acceptance by ESSD or any other specific journal.
10. **Authorship is contribution-based and output-specific.** Dataset, ESSD, and LUP authorship may differ; each list is determined by verified contribution to that specific output and documented using CRediT.

## 3. Overall sequence

The pathway contains four stages. Stage 0 is short but necessary to make the three principal stages safe and efficient.

| Stage | Main outcome | Exit gate |
|---|---|---|
| 0. Editorial and release governance | Frozen division between public data, ESSD content, and LUP content | Scope and claim-allocation records accepted |
| 1. Public data release | Reusable dataset deposited with DOI, license, metadata, code, and validation | Release candidate passes technical and scientific audit and DOI is active |
| 2. Data-paper submission — ESSD preferred | Data-description manuscript submitted and available through the selected journal's public process | ESSD submission/preprint and dataset citation are public, or an alternative venue is formally recorded |
| 3. LUP submission | Distinct analytical and policy manuscript submitted | Overlap audit passes and LUP submission is complete |

Drafting tasks may overlap, but the deliberate project sequence remains: the dataset DOI precedes the data-paper submission, and the data paper's public record and exact dataset citation precede LUP submission. This is a governance choice, not a stated editorial requirement. Final acceptance of the data paper is not required before LUP submission unless an editor requests it.

If project timelines change, overlapping review periods may be reconsidered only when the manuscripts remain substantively distinct, both submissions disclose the related manuscript, and the current policies of both journals have been checked. Overlapping review is a fallback, not the default assumed by this plan.

## 4. Stage 0 — Editorial and release governance

### 4.1 Objectives

* define the exact public data product;
* distinguish public release files from internal provenance and temporary processing files;
* allocate research questions, claims, tables, and figures between the manuscripts;
* establish versioning, licensing, change-control, and contribution-based authorship rules before packaging begins;
* evaluate whether the scoped release remains a strong fit for ESSD before full manuscript production.

### 4.2 Required tasks

1. Inventory all accepted products from Phases 1–9A.2, including their validation records, hashes, row counts, schemas, and upstream dependencies.
2. Assign every product to one of three tiers:
   * **Tier 1 — public scientific data:** canonical data required for independent reuse;
   * **Tier 2 — reproducibility support:** crosswalks, weights, code, configuration, validation summaries, and examples;
   * **Tier 3 — internal records:** checkpoints, transient exports, redundant copies, execution logs, and other files not needed for scientific reuse.
3. Create a claim-allocation matrix identifying the primary home of every major result: ESSD, LUP, both by citation only, or neither.
4. Create a figure-and-table registry to prevent duplicate central displays.
5. Initiate authorship and contributor-role discussions as a parallel, continuously tracked workstream for the dataset, ESSD manuscript, and LUP manuscript. Early discussion creates an opportunity for substantive contribution but does not reserve authorship in advance.
6. Maintain provisional CRediT records for each output and update them as verified contributions occur.
7. Confirm the license compatibility and required attribution for MapBiomas-derived products, code, documentation, and the public dataset.
8. Prepare a draft data-paper title, abstract, scope statement, and reuse case sufficient for the ESSD-fit checkpoint in Section 4.4.
9. Record the frozen strategy in Decision 024 before release packaging begins.

### 4.3 Minimum-viable release boundary and scope-control gate

The `v1.0.0` release must contain every dataset, spatial support, crosswalk, weight definition, configuration, metadata element, validation record, and code component required to interpret or reproduce any claim, table, or figure in either manuscript. An item needed by either submission cannot be deferred to `v1.1.0`, regardless of its Tier 1 or Tier 2 classification.

Items may be deferred to `v1.1.0` only when they are not required for scientific interpretation or reproduction of either manuscript. Eligible examples include:

* additional convenience formats duplicating canonical content;
* tutorials beyond the minimum worked examples;
* supplementary visualizations not used in either manuscript;
* extended sensitivity products that support no submitted claim;
* usability improvements that do not change data meaning, validation, or access.

The Stage 0 inventory must assign every proposed Tier 1 and Tier 2 item to `required_for_v1.0.0` or `deferrable_to_v1.1.0`, with a recorded reason. Tier 3 files remain internal unless a later reproducibility finding justifies reclassification.

After the Stage 0 scope freeze, no new component may enter `v1.0.0` unless it resolves a reproducibility, interpretation, licensing, validation, or journal-compliance blocker. Other improvements enter the `v1.1.0` backlog. If the inventory shows that the minimum defensible release is materially larger than anticipated, the scope gate must be reviewed before packaging continues.

### 4.4 ESSD-fit checkpoint

After the release scope, draft data-paper abstract, and principal reuse cases are available, Stage 0 must assess whether ESSD remains the best data-publication venue. The checkpoint evaluates:

* whether the released product has independent reuse value beyond the LUP analysis;
* whether the value added over the source MapBiomas products is explicit and substantial;
* whether the dataset, validation, uncertainty documentation, and repository plan satisfy the intended data-paper contribution;
* whether the proposed ESSD manuscript is demonstrably distinct from the LUP manuscript;
* whether a presubmission enquiry is available and useful.

The checkpoint may affirm ESSD, recommend a presubmission enquiry, or formally redirect the data paper to another suitable venue. Redirection does not weaken or cancel the public-release requirement and does not alter accepted analytical results.

### 4.5 Deliverables

```text
docs/decisions/024_public_release_and_dual_publication_governance.md
config/public_release_source_inventory_v1.csv
config/manuscript_claim_allocation_v1.csv
config/manuscript_figure_table_registry_v1.csv
config/public_release_version_allocation_v1.csv
docs/validation/public_release_gap_analysis_v1.md
docs/validation/data_paper_venue_fit_assessment_v1.md
```

### 4.6 Exit criteria

* every accepted product has a release-tier classification;
* every proposed Tier 1 and Tier 2 item is assigned to `v1.0.0` or the `v1.1.0` backlog with a reason;
* every major claim and planned display has a primary manuscript home;
* no unresolved license or attribution issue blocks public distribution;
* dataset boundaries and the intended release version are frozen;
* provisional, output-specific authorship and CRediT records exist and remain open to documented contributions;
* the ESSD-fit checkpoint is completed and its outcome recorded;
* Decision 024 records the frozen governance state.

## 5. Stage 1 — Public data release

### 5.1 Release object

The public dataset should be framed as an observation-window-aware, spatially explicit account of native vegetation, pasture, and temporary-crop dynamics across the canonical study domain from 1985 to 2025. Its value-added elements include stock–flow accounting, five-year transitions, fixed-cohort reconstruction, conversion-origin partitions, pathway composition, cell trajectories, spatial clustering outputs, and scale/zoning sensitivity records.

The release must not reproduce every intermediate file generated during development. It must expose the minimum complete set from which every claim, table, and figure in either manuscript can be interpreted and reproduced, together with sufficient documentation for legitimate independent reuse. The file-level `v1.0.0` boundary is fixed through Section 4.3 before packaging begins.

### 5.2 Proposed release architecture

```text
dataset_release_v1/
├── README.md
├── CITATION.cff
├── LICENSE_DATA.txt
├── LICENSE_CODE.txt
├── CHANGELOG.md
├── data/
│   ├── core/
│   ├── trajectories_and_cohorts/
│   ├── spatial_statistics/
│   └── sensitivity/
├── spatial_support/
├── metadata/
├── validation/
├── code/
└── examples/
```

### 5.3 Format policy

* **Parquet:** primary format for large tabular panels and cell-level outputs;
* **CSV:** compact summaries, dictionaries, manifests, and selected interoperable tables;
* **GeoPackage or GeoParquet:** canonical and alternative spatial supports;
* **JSON:** machine-readable validation and provenance records;
* **Markdown/PDF:** human-readable documentation;
* **Python and Earth Engine scripts:** reproducibility code;
* **Shapefile:** not used as a canonical release format because of field-name and type limitations.

### 5.4 Metadata and documentation requirements

The release must include:

1. dataset title, creators, affiliations, ORCIDs, abstract, keywords, spatial extent, temporal extent, and version;
2. complete field dictionary, units, valid ranges, missing-value semantics, and key definitions;
3. explicit definitions of `NAT`, `PAS`, and `TMP`, with `TMP` rendered as `temporary crops` in human-readable English;
4. provenance from MapBiomas Collection 11 through each public derived product;
5. temporal-window definitions and treatment of the diagnostic 2020–2025 interval;
6. left-censoring, right-censoring, temporal-filter, classification-confusion, and MAUP metadata;
7. spatial-support definitions, CRS information, cell identifiers, joins, weights, and crosswalks;
8. explanation of primary versus sensitivity products;
9. worked examples for reading, joining, mapping, and reproducing selected summaries;
10. a clear boundary between observed quantities, derived metrics, classified states, statistical results, and diagnostics.

### 5.5 Validation requirements

The release candidate must pass an automated audit covering at least:

* file completeness and unexpected-file detection;
* SHA-256 inventory;
* schema, type, key, uniqueness, row-count, and join checks;
* geometry validity and CRS checks;
* equivalence with accepted canonical totals and class counts;
* cross-file identifier integrity;
* presence and consistency of uncertainty flags;
* terminology audit for human-readable fields and documentation;
* code/configuration references resolving to included or persistently archived resources;
* clean installation and execution of the documented examples in a fresh environment.

Independent scientific spot checks should complement, not replace, the automated audit.

### 5.6 Repository and versioning

The release must be deposited in a repository that provides long-term access, a persistent DOI, explicit licensing, and versioned records. GitHub remains the development and code-provenance repository but is not the sole archival location for the scientific data.

The initial public release should use a stable semantic version such as `v1.0.0`. Subsequent corrections must produce a new version and changelog entry. Manuscripts must cite both the version-specific DOI or identifier and, where supported, the concept DOI.

The `v1.1.0` backlog is not part of the release gate. Deferrable improvements must not delay either manuscript once `v1.0.0` satisfies the minimum boundary and all blocking validation requirements.

### 5.7 Stage 1 deliverables

* release candidate directory and portable archive;
* public-release manifest and validation record;
* data dictionary and provenance graph;
* code environment specification;
* repository record with active DOI;
* final data citation;
* short release note suitable for the project README;
* version-allocation record distinguishing `v1.0.0` requirements from the `v1.1.0` backlog.

### 5.8 Exit criteria

* all required files are public, readable, documented, and licensed;
* automated validation passes;
* independent review finds no unresolved blocking inconsistency;
* DOI resolves to the intended immutable release;
* the release can be used without access to the project's private Drive structure;
* every claim, table, and figure planned for either manuscript resolves to the necessary public data, metadata, configuration, and code.

## 6. Stage 2 — Data-description manuscript (ESSD preferred)

### 6.1 Manuscript role

The data paper describes the public dataset and demonstrates its quality and reuse potential, with ESSD as the preferred venue when affirmed by the Section 4.4 checkpoint. Methodological detail is included to explain and validate the data product, not to claim a separate methods paper. Policy interpretation is deliberately limited. If another data journal is selected, the same separation of contributions and release requirements remains in force.

### 6.2 Proposed manuscript structure

1. Introduction: data gap and reuse need;
2. source data and study domain;
3. conceptual stock–flow and pathway framework;
4. spatial and temporal support;
5. construction of the integrated data products;
6. quality control and validation;
7. data records and file structure;
8. technical validation and descriptive characterization;
9. uncertainty and appropriate-use limits;
10. code and data availability;
11. user notes and reproducible examples.

### 6.3 Results appropriate for ESSD

* completeness and coverage;
* internal consistency and accounting closure;
* class and state distributions used to characterize the dataset;
* validation of cohorts, trajectories, and pathway partitions;
* spatial-support and MAUP sensitivity as fitness-for-use information;
* examples demonstrating possible analyses without developing the full policy argument.

### 6.4 Results reserved primarily for LUP

* substantive answers to the five research questions;
* interpretation of pasture legacies and temporary-crop expansion pathways;
* territorial concentration and policy targeting;
* implications for traceability, restoration, intensification, deforestation governance, and monitoring design;
* normative or decision-oriented recommendations.

### 6.5 Data-paper submission package

* manuscript and supplement;
* dataset DOI and formal data citation;
* code archive and software citation;
* data-availability and code-availability statements;
* CRediT author-contribution statement agreed by all listed authors;
* competing-interest and funding statements;
* cover letter explaining originality, data reuse value, and relationship to the planned analytical paper;
* completed cross-manuscript overlap declaration.

### 6.6 Exit criteria

* the manuscript describes the exact released version;
* all dataset references and links resolve;
* no central LUP result is fully developed in the data paper;
* internal and external prereview comments are resolved;
* ESSD submission is complete and its public discussion/preprint record is available, or the formally selected alternative data venue has received the manuscript and the related record is documented.

## 7. Stage 3 — Land Use Policy manuscript

### 7.1 Manuscript role

The LUP paper uses the released dataset to answer the research questions and explain their policy relevance. It does not reproduce the data paper's technical documentation. Its methods section provides sufficient analytical transparency while citing the public dataset and the ESSD or alternative data-paper description for full construction and validation details.

### 7.2 Analytical spine

The manuscript should be organized around the five established questions:

1. redistribution of the pasture stock already observed in 1985;
2. temporal origin of pasture converted to temporary crops;
3. pasture mediation in `NAT→TMP` pathways;
4. spatial and temporal variation in stocks, flows, pathways, and clusters;
5. robustness to temporal resolution, spatial scale, zoning, and spatial-weight definitions.

### 7.3 Policy spine

The discussion should connect the evidence to clearly delimited policy domains, potentially including:

* deforestation-free and conversion-free supply-chain monitoring;
* distinction between direct conversion and pasture-mediated crop expansion;
* legacy land stocks and the temporal reach of accountability systems;
* prioritization of restoration and pasture-intensification interventions;
* spatial targeting versus the documented MAUP sensitivity of local clusters;
* treatment of temporal-boundary uncertainty in monitoring and evaluation;
* implications for Cerrado–Amazon transition-zone governance.

Policy claims must follow from the evidence and distinguish descriptive findings, causal interpretations, and recommendations. The study does not establish causal effects merely because it reconstructs temporal pathways.

### 7.4 Proposed manuscript structure

1. Introduction and policy problem;
2. conceptual framing and research questions;
3. concise data and methods, with citation to the public release and data-paper record;
4. results organized by the research questions;
5. integrated discussion;
6. policy implications;
7. uncertainty, transferability, and limitations;
8. conclusions.

### 7.5 Distinctiveness audit

Before submission, the LUP package must demonstrate that:

* its central contribution is analytical and policy-facing;
* text reused from the data paper is limited to unavoidable definitions and is appropriately cited;
* central figures and tables are distinct;
* any shared descriptive value is cited to the dataset or data paper rather than presented as a second original result;
* the cover letter discloses the related data-paper submission and explains the non-overlapping contribution;
* the exact dataset version used for analysis is cited.

### 7.6 Exit criteria

* all five research questions have evidence-backed answers;
* policy implications are specific, bounded, and traceable to results;
* robustness findings calibrate the strength and spatial precision of the conclusions;
* manuscript, supplement, code references, and data citation are internally consistent;
* overlap audit passes;
* LUP submission is complete.

## 8. Cross-cutting workstreams

The following workstreams span all stages:

### 8.1 Terminology and scientific language

Maintain one glossary across the release and both manuscripts. Machine codes remain stable; human-readable English follows the accepted terminology decisions. Boundary and uncertainty terms follow Decision 022.

### 8.2 Reproducibility

Every manuscript figure and table must be generated from the DOI release or from explicitly versioned analysis code that consumes that release. Private Drive paths must not appear in public scripts or manuscripts.

### 8.3 Provenance and change control

Changes after the release freeze require a recorded reason, affected-file list, rerun of relevant validation, and version decision. Silent replacement of DOI-release files is prohibited.

### 8.4 Authorship and credit

Authorship and contributor-role discussion begins with Stage 0 and runs in parallel with the technical work. Dataset creation, software, validation, conceptualization, analysis, and policy interpretation must be credited explicitly using CRediT. Dataset, ESSD, and LUP author lists may differ because eligibility is determined separately from verified contributions to each output. CRediT documents contributions but does not itself determine authorship eligibility. Dataset creators must receive formal dataset citation independently of manuscript citation.

Prospective collaborators must have a genuine opportunity to contribute substantively, but invitation, seniority, funding, or association with the project does not reserve authorship. Provisional contribution records remain editable until the relevant author list is finalized and approved by all authors.

### 8.5 External review

At least three prereview perspectives are desirable:

* a data/reproducibility reviewer;
* a land-change or remote-sensing domain reviewer;
* a land-use-policy reviewer unfamiliar with the internal project history.

### 8.6 Calibrated methodological-discipline claims

Public-facing text may state that protocols and thresholds were fixed and dated before the accepted analyses that used them, and that identified provenance gaps were resolved through documented artifact and hash verification. It must not claim that repository auditing proves the absence of every possible informal or result-contingent adjustment. Any numerical count of earlier provenance incidents must enumerate the corresponding records.

## 9. Milestones

| Milestone | Definition |
|---|---|
| M0 | Plan and dual-publication strategy accepted; Decision 023 incorporated |
| M1 | Release scope, claims, figures, licensing, and `v1.0.0` boundary frozen; authorship/CRediT workstream active |
| M1A | ESSD-fit checkpoint completed and data-paper venue recorded |
| M2 | Public release candidate assembled and validation passed |
| M3 | Dataset `v1.0.0` deposited and DOI active |
| M4 | ESSD or formally selected alternative data-paper manuscript submitted and public record documented |
| M5 | LUP manuscript and distinctiveness audit completed |
| M6 | LUP manuscript submitted |

## 10. Immediate next implementation step

The next task should not yet be manuscript drafting or repository upload. It should be **Stage 0A — canonical product inventory and public-release gap analysis**.

This task will:

1. enumerate all accepted Phase 1–9A.2 outputs;
2. authenticate them against their validation and inventory records;
3. classify them as Tier 1, Tier 2, or Tier 3;
4. identify missing metadata, licenses, dictionaries, examples, or portable formats;
5. identify outputs that are redundant, internal-only, or unsuitable for public release;
6. produce the initial claim-allocation and figure/table registries;
7. assign each proposed Tier 1 and Tier 2 item to `v1.0.0` or the `v1.1.0` backlog;
8. identify the minimum draft abstract and reuse cases needed for the ESSD-fit checkpoint;
9. provide an evidence-based estimate of the work required for the release candidate.

No public release should be assembled until this audit is accepted. This prevents the release structure from inheriting the historical order in which project files happened to be generated.

## 11. Completion definition

This plan is complete only when the project has produced:

1. a DOI-bearing, independently usable public data release;
2. an ESSD data-description submission — or a formally justified alternative data-paper submission — anchored to that release;
3. a distinct LUP analytical submission anchored to the same exact release;
4. a public documentation structure in which a new user can understand the dataset, its provenance, its limitations, and its legitimate uses without access to private project history.

# Pasture–Crop Dynamics in the Brazilian Cerrado and Amazon

## Overview

This repository supports a research project on the long-term dynamics among native vegetation, planted pasture, and temporary agriculture in the Brazilian Cerrado and Amazon.

The project moves beyond net land-cover change to examine **directed flows**, **land-stock origins**, and **conversion pathways**. Its central purpose is to determine how pre-existing pasture stocks and newly established pastures contribute to agricultural consolidation across space and time.

The analytical workflow and documentation are currently being rebuilt and validated. Results should therefore be considered provisional until they are reproduced by the canonical processing pipeline described in this repository.

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
2. What share of pasture-to-cropland conversion originated from pasture established before 1985, pasture established during the observed series, or pasture without an attributable age?
3. Among pixels classified as native vegetation at the beginning of a five-year interval and temporary agriculture at its end, what share passed through pasture during the intervening years?
4. How do these stocks, flows, and pathway compositions vary across space and time?
5. How robust are the results to temporal resolution, spatial scale, zoning, and spatial-weight definitions?

## Conceptual framework

### Core land-cover states

The main analytical system contains three focal states:

- **NAT** — native vegetation;
- **PAS** — planted pasture;
- **TMP** — temporary agriculture.

Additional categories are retained where necessary to close the accounting system, including mosaic or other agricultural uses, other anthropogenic or non-vegetated uses, water, and unobserved or masked pixels.

### Stocks and flows

Land-cover stocks describe the area occupied by each state at a given time. Directed flows describe transitions between two time points, such as:

- `NAT → PAS`: pasture expansion or pasture-stock replenishment;
- `PAS → TMP`: agricultural consolidation over pasture;
- `NAT → TMP`: conversion from native vegetation to temporary agriculture between observation points.

The accounting framework is designed to track all relevant destinations of an initial stock and to quantify residual or unclassified components explicitly.

### Pasture origin

Pasture involved in `PAS → TMP` is separated into:

- **left-censored pasture** — pasture established before the beginning of the series and therefore not precisely dated;
- **new pasture** — pasture established during the observed series, with an attributable age;
- **pasture without attributable age** — pasture identified in the land-cover series but not assigned an age by the pasture-age product.

This distinction is used both to characterize the origin of agricultural consolidation and to follow the long-term fate of the pasture stock already present in 1985.

### Two complementary temporal views

The project combines:

1. **Five-year accounting intervals**, used to obtain more stable measurements of land stocks and directed flows.
2. **Annual within-interval trajectories**, used to identify short pasture phases that are compressed by five-year comparisons.

The annual analysis is treated explicitly as sensitive to temporal classification instability. Alternative persistence rules will be evaluated rather than assuming that every single-year pasture observation represents a true land-use stage.

## Study domain

The study focuses on the dynamic portions of the Cerrado and Amazon biomes. The reference spatial framework is a fixed set of approximately 21,869 equal-area hexagonal cells of about 20,000 hectares each.

The reduced domain excludes cells representing effectively intact areas, including extensive portions of protected areas and Indigenous lands. This domain definition concerns change measured at the cell level and should not be confused with pixel-level alternation or individual pixel trajectories.

The domain remains fixed across time. Within it, the number and identity of cells with a particular process—such as pasture expansion or agricultural consolidation—may vary among five-year intervals.

## Temporal coverage

The source time series spans **1985–2025**, with the following five-year reference points:

```text
1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025
```

The main inferential period is expected to end in 2020. The 2020–2025 interval may be processed for diagnostic purposes but is not currently intended to support the primary conclusions because temporal filtering is incomplete at the end of the source series.

## Data sources

The current workflow uses:

- **MapBiomas Brazil Collection 11 `classification-ft`** annual land-cover maps;
- **MapBiomas Collection 11 pasture-age product**;
- an equal-area hexagonal grid with cells of approximately 20,000 ha;
- a preselected Cerrado–Amazon dynamic-domain layer.

Exact asset identifiers, product versions, class remapping rules, coordinate reference systems, grid transforms, and processing dates will be recorded in the technical documentation and centralized configuration files.

## Main analytical components

### 1. Five-year stock and flow accounting

For each cell and interval, the workflow will quantify focal transitions, persistence, auxiliary destinations, masked areas, and the origin of pasture converted to temporary agriculture.

The principal origin identity is:

```text
PAS→TMP total = censored origin + new-pasture origin + unattributed-age origin
```

### 2. Fixed 1985 pasture cohort

Pixels classified as pasture in 1985 and identified as established before 1985 will form a fixed initial cohort. The same pixels will be followed through all subsequent reference years to measure persistence and redistribution among land-cover states.

### 3. Within-interval trajectory analysis

For pixels classified as `NAT` at the beginning and `TMP` at the end of an interval, annual observations will be used to distinguish:

- conversion with pasture detected in an intermediate year;
- conversion with no pasture detected in the annual series.

The latter will not automatically be called “direct conversion,” because other intermediate land-cover states may be present.

### 4. Consolidation–replenishment balance

The relationship between pasture-to-cropland consolidation and native-to-pasture replenishment will be evaluated for explicitly defined analytical populations, including the full dynamic domain and process-specific subsets.

For spatial analyses, a bounded balance index may be used:

```text
(consolidation - replenishment) / (consolidation + replenishment)
```

### 5. Spatial robustness and structure

The spatial analysis will include:

- sensitivity to grid positioning and orientation;
- sensitivity to cell sizes around the 20,000 ha reference scale;
- global spatial autocorrelation;
- selected local spatial association analyses where supported by the global pattern;
- comparison of alternative spatial-weight matrices for the reduced domain.

## Validation principles

The canonical workflow will be evaluated through explicit checks, including:

- a balanced cell-by-period panel;
- unique cell identifiers;
- non-negative area values;
- complete and mutually exclusive transition partitions;
- closure of the fixed 1985 pasture cohort;
- explicit accounting for masked and unattributed-age components;
- agreement between land-cover and pasture-age masks;
- audits of source class codes and remapping completeness;
- sensitivity to annual persistence rules;
- sensitivity to spatial scale, zoning, and neighborhood definitions.

Accounting closure is an internal consistency test. It does not, by itself, demonstrate that the source classification or class remapping is accurate.

## Repository status

**Current status: analytical reconstruction and validation.**

The repository is being organized from the ground up. Historical scripts and preliminary outputs may be used as diagnostic references, but only the validated canonical pipeline and its reproduced outputs will be treated as authoritative.

The reconstruction will prioritize:

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

Reproducibility requirements will include:

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

A repository license has not yet been specified. Until a license is added, reuse rights should not be assumed.

## Contact

**Mario Barroso Ramos Neto**  
Project lead and repository maintainer


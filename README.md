# Pasture–Crop Dynamics in the Brazilian Cerrado and Amazon

**Project status updated: 16 September 2026**

## Overview

This repository supports a research project on the long-term dynamics among native vegetation, planted pasture, and temporary agriculture in the Brazilian Cerrado and Amazon.

The project moves beyond net land-cover change to examine **directed flows**, **land-stock origins**, **conversion pathways**, **cell-level temporal trajectories**, and **spatial concentration**. Its central purpose is to determine how pre-existing pasture stocks and newly established pastures contribute to agricultural consolidation across space and time.

The canonical workflow has been reconstructed and validated through Phase 6. It now includes the fixed analytical domain; five-year stock-and-flow and annual `NAT → TMP` trajectory panels; process-specific spatial metrics; comparable map classes; cell-state trajectories and multiquinquennial episodes; a temporal-spatial synthesis of the high-magnitude `NAT → TMP` cohort; Global Moran's I; and Local Moran/LISA results. The next analytical stage is the consolidated comparison between the Cerrado and Amazon biomes, followed by spatial-support robustness tests.

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
4. How do these stocks, flows, pathways, temporal trajectories, and spatial clusters vary across time and between the Cerrado and Amazon?
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

The accounting framework tracks all relevant destinations of an initial stock and quantifies residual or unclassified components explicitly.

### Pasture origin

Pasture involved in `PAS → TMP` is separated into:

- **left-censored pasture** — pasture established before the beginning of the series and therefore not precisely dated;
- **new pasture** — pasture established during the observed series, with an attributable age;
- **pasture with unresolved age** — pasture associated with source code `1`, retained in accounting but not interpreted as a numerical age while the source anomaly remains unresolved;
- **pasture without attributable age** — pasture identified in the land-cover series but not assigned an age by the pasture-age product.

This distinction is used both to characterize the origin of agricultural consolidation and to follow the long-term fate of the pasture stock already present in 1985.

### Two complementary temporal views

The project combines:

1. **Five-year accounting intervals**, used to obtain stable measurements of land stocks and directed flows.
2. **Annual within-interval trajectories**, used to identify short pasture phases compressed by five-year comparisons.

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

All eight intervals are processed and retained. The **primary analytical series** covers 1985–2020. The 2020–2025 interval is included in tables, maps, sequences, transitions, episode durations, and spatial statistics, but is consistently marked as a **diagnostic extension** because temporal filtering is incomplete at the end of the source series. Results depending on that interval are identified explicitly and do not alone determine conclusions for the primary period.

## Data sources

The canonical workflow uses:

- **MapBiomas Brazil Collection 11 `coverage_v3`** annual land-cover maps;
- **MapBiomas Collection 11 pasture-age product**;
- an equal-area hexagonal grid with cells of approximately 20,000 ha;
- the reproducibly reconstructed Cerrado–Amazon canonical domain.

Asset identifiers, product versions, class-remapping rules, coordinate reference systems, grid transforms, and processing decisions are recorded in the technical documentation and centralized configuration files.

## Main analytical components

### 1. Five-year stock and flow accounting

For each cell and interval, the workflow quantifies focal transitions, persistence, auxiliary destinations, masked areas, and the origin of pasture converted to temporary agriculture.

The principal origin identity is:

```text
PAS→TMP total = censored origin + new-pasture origin
                + unresolved-age origin + unattributed-age origin
```

### 2. Fixed 1985 pasture cohort

Pixels classified as pasture in 1985 and identified as established before 1985 form a fixed initial cohort. The same pixels are followed through all subsequent reference years to measure persistence and redistribution among land-cover states.

### 3. Within-interval trajectory analysis

For pixels classified as `NAT` at the beginning and `TMP` at the end of an interval, the canonical trajectory panel uses annual observations to distinguish:

- endpoint flow with pasture detected in at least one intermediate year;
- endpoint flow with pasture detected in at least two intermediate years;
- endpoint flow with pasture detected in at least two consecutive intermediate years;
- endpoint flow with no pasture detected in the annual series.

The last category is not automatically interpreted as “direct conversion,” because other intermediate land-cover states may be present.

### 4. Consolidation–replenishment balance

The relationship between pasture-to-cropland consolidation and native-to-pasture replenishment is evaluated for the full dynamic domain and process-specific subsets. The bounded balance index is:

```text
(consolidation - replenishment) / (consolidation + replenishment)
```

The index describes the relative direction of the balance, whereas the corresponding area balance describes its magnitude. Inactive, undefined, low-support, zero, and not-applicable states remain conceptually distinct.

### 5. Cell trajectories and episodes

Phase 4 represents each cell as a sequence of classified five-year states. It measures state changes, entries, exits, reentries, reversals, consecutive episodes, persistence, duration, and temporal censoring in both the primary and full observed series.

The analysis also defines a fixed **high-magnitude `NAT → TMP` cohort** of 2,598 cells: cells that reached the frozen high-magnitude class in at least one primary interval. This is a historical membership criterion, not a claim that every cohort cell is highly active in every period. The remaining cells are classified as no primary occurrence, low-magnitude maximum, or moderate-magnitude maximum.

### 6. Spatial structure

The canonical spatial support has a fixed shared-edge graph with **67,453 undirected links**, **134,906 directed links**, 163 islands, and 264 connected components. Global and local spatial autocorrelation are evaluated on this support.

Phase 5 completed the prespecified Global Moran's I analysis. Phase 6 completed Local Moran/LISA for five focal metrics across all eight intervals, using 9,999 permutations, Benjamini–Hochberg correction as the primary within-map multiplicity rule, and Benjamini–Yekutieli as a sensitivity analysis.

For absolute activity metrics, **HH clusters** are the primary substantive focus and **LL clusters** describe structured low activity or absence. For signed balance metrics, HH and LL are interpreted jointly as opposing spatial regimes. HL and LH are treated as spatial outliers rather than core clusters.

### 7. Integrated analytical panel

The validated stock-flow and annual `NAT → TMP` trajectory panels are joined one to one using `cell_id`, `t0`, and `t1`. The integrated table retains all **199,112 cell-interval observations**, including structural zeros, while preserving the conceptual distinction among net balance, directed endpoint flows, and annual pixel trajectories.

## Validation principles

The canonical workflow uses explicit machine-readable checks, including:

- balanced cell-by-period panels and unique analytical keys;
- non-negative area values;
- complete and mutually exclusive transition partitions;
- closure of the fixed 1985 pasture cohort;
- explicit accounting for masked and unattributed-age components;
- agreement between land-cover and pasture-age masks;
- audits of source class codes and remapping completeness;
- exact reproduction of accepted class counts;
- sequence-engine, episode, transition, and censoring invariants;
- independent statistical-engine checks for spatial autocorrelation;
- permutation, multiplicity-correction, quadrant-sign, and support checks for Local Moran/LISA;
- sensitivity to temporal persistence rules and diagnostic-period inclusion;
- planned sensitivity to spatial scale, zoning, and neighborhood definitions.

Accounting closure is an internal consistency test. It does not, by itself, demonstrate that source classification or class remapping is accurate. Likewise, statistically significant spatial association does not establish a causal process.

## Analytical phases and status

| Phase | Scope | Status |
|---|---|---|
| 0 | Canonical inputs, provenance, runtime, and domain reconstruction | Complete and accepted |
| 1 | Spatial support, biome overlap, and shared-edge graph | Complete and accepted |
| 2 | Process-specific spatial metrics panel | Complete and accepted |
| 3 | Comparable classes, maps, and GIS interval tables | Complete and accepted |
| 4 | Cell trajectories, episodes, high-magnitude cohort, and temporal-spatial synthesis | Complete and accepted |
| 5 | Prespecified Global Moran's I analysis | Complete and accepted |
| 6 | Local Moran/LISA, cluster summaries, maps, and interpretive decision rules | Complete and accepted |
| 7 | Consolidated Cerrado–Amazon comparison | Next phase |
| 8 | MAUP, grid, scale, and weights robustness | Planned |
| 9 | Integrated synthesis and manuscript-facing outputs | Planned |

## Repository status

**Current status: the canonical pipeline is validated through Phase 6.** The repository contains the 24,889-cell spatial support, the 199,112-row cell-by-interval panel, comparable classes and maps for 12 metrics, cell trajectories and multiquinquennial episodes, the four-level `NAT → TMP` maximum-magnitude grouping, the Phase 4 temporal-spatial synthesis, 104 prespecified Global Moran results, and 40 Local Moran/LISA cell maps covering five metrics and eight intervals.

The main outstanding work is analytical rather than reconstructive:

1. consolidate the Cerrado–Amazon comparison using the accepted Phase 4–6 outputs;
2. run the planned spatial-scale, zoning, and weights sensitivity analysis;
3. integrate the accepted results into manuscript-facing figures, tables, and narrative;
4. rerender any presentation-only map panels whose titles or labels require adjustment, without recomputing accepted statistics.

Historical scripts and preliminary outputs may be retained as diagnostic references, but only the validated canonical pipeline and its reproduced outputs are authoritative.

## Repository structure

```text
pasture-crop-dynamic/
├── README.md
├── config/          # Canonical parameters, classes, assets, and versions
├── gee/             # Google Earth Engine processing scripts
├── analysis/        # Statistical and spatial analysis code
├── docs/            # Plans, methods, decisions, findings, and dictionaries
├── outputs/         # Reproducible analyses, validations, tables, and figures
└── manuscript/      # Manuscript-facing material
```

Large source rasters, restricted assets, and temporary processing files should not be committed. Their provenance and access requirements are documented instead.

## Reproducibility

The project uses:

- pinned data-product versions;
- centralized constants and class definitions;
- explicit spatial projections and transforms;
- documented Earth Engine asset dependencies;
- deterministic output naming;
- hashes and per-stage validation records;
- frozen analytical populations and classification thresholds;
- explicit separation of primary and diagnostic temporal windows;
- traceability from figures and tables back to scripts and accepted outputs.

## Interpretation boundaries

This project measures spatial and temporal associations among land stocks and land-cover transitions. It does not, in its current design, identify causal effects of commodity prices, infrastructure, environmental policies, land tenure, or legal restrictions.

Cell-level trajectories summarize successive five-year states and must not be confused with annual pixel trajectories. Local Moran/LISA classes describe a cell in relation to its neighbors under a fixed graph; they do not identify mechanisms or causal spillovers. Any explanatory covariates incorporated later will initially be interpreted descriptively unless accompanied by an appropriate causal design.

## Citation

Citation information will be added when a stable release or manuscript preprint becomes available.

## License

The code and documentation in this repository are released under the MIT License. Source datasets and external products remain subject to their respective licenses and terms of use.

## Contact

**Mario Barroso Ramos Neto**  
Project lead and repository maintainer

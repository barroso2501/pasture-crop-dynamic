# Verified literature register

- **Version:** 1.0
- **Record date:** 2026-09-23
- **Scope:** literature used to position the public dataset, the ESSD data paper and the Land Use Policy analytical paper
- **Companion file:** `docs/literature/002_claim_to_literature_crosswalk.csv`

## Purpose

This register separates external scientific literature from the project's internal evidence records. It documents what each publication contributes, where it overlaps with the project, which distinctions remain defensible and how it may be used in the two planned manuscripts.

This file does not validate project results. Numerical evidence produced by the project remains governed by the accepted analytical outputs and by the Phase 9 integrated evidence matrix. External publications provide conceptual foundations, precedents, comparison points and interpretation boundaries.

## Verification levels

| Status | Meaning |
|---|---|
| `full_text_verified` | The full publication was read directly and its relevance was assessed from the original text. |
| `abstract_and_key_excerpts_reviewed` | The assessment used the abstract and selected passages. Claims about novelty remain provisional until the full text is reviewed. |
| `methodological_source` | The publication primarily documents a source dataset or mapping method used to contextualize MapBiomas-derived analyses. |

The verification status concerns this project's literature review. It is not an assessment of publication quality.

## Positioning summary

The literature establishes that the project does not introduce land-change accounting, net-change-versus-swap analysis, pasture-to-cropland conversion, national MapBiomas transition analysis, annual land-cover trajectories or the dating of native-vegetation-to-cropland conversion as isolated concepts. The defensible contribution is their integration in one auditable architecture: directed stock-flow accounting, pasture-origin attribution, explicit intermediate-pathway detection, multi-interval cell trajectories, spatial inference and sensitivity to temporal boundaries, scale and zoning.

Caballero et al. (2023) is the most direct broad-scale empirical precedent identified so far. It documents the transformation among native vegetation, pasture and agriculture across Brazilian biomes and provides a national and biome-level benchmark. Its Sankey diagrams connect selected temporal states rather than reconstructing every intervening annual pixel path. The publication therefore motivates, but does not answer, the project's questions concerning fixed pasture cohorts, pasture age of origin, annual intermediate pathways, episode duration and spatial robustness.

## Core methodological foundations

### LIT001 Pontius Shusas and McEachern 2004

**Reference:** Pontius, R. G., Shusas, E., and McEachern, M. (2004). Detecting important categorical land changes while accounting for persistence. *Agriculture, Ecosystems and Environment*, 101(2-3), 251-268. https://doi.org/10.1016/j.agee.2003.09.008

- **Verification:** `full_text_verified`.
- **Contribution:** decomposes categorical change into persistence, gross gains and losses, net change and swap using cross-tabulation between two dates.
- **Relevance:** provides the conceptual basis for distinguishing apparently stable margins from substantial opposing flows.
- **Project distinction:** the project extends the logic to eight five-year intervals, attributes the origin of pasture stocks, reconstructs trajectories and evaluates spatial sensitivity.
- **Manuscript use:** ESSD methods and conceptual data model; LUP interpretation of why net change alone is insufficient.

### LIT002 Pendrill et al. 2019

**Reference:** Pendrill, F., Persson, U. M., Godar, J., and Kastner, T. (2019). Deforestation displaced: Trade in forest-risk commodities and the prospects for a global forest transition. *Environmental Research Letters*, 14, 055003. https://doi.org/10.1088/1748-9326/ab0d41

- **Verification:** `full_text_verified`.
- **Contribution:** uses physical land-balance accounting and temporal attribution to connect deforestation with commodities and trade.
- **Relevance:** establishes that stock-flow accounting and multi-year attribution windows are accepted approaches.
- **Project distinction:** Pendrill et al. use proportional attribution at coarser scales and impose sequence assumptions. The project observes pathways and pasture origin spatially rather than assigning them proportionally.
- **Manuscript use:** ESSD methodological context; limited LUP discussion of traceability and commodity attribution.

### LIT003 Matos et al. 2025

**Reference:** Matos, A. P., Hunter, M., Pontius, R. G., Baumann, L. R., Parente, L. L., and Ferreira, L. G. (2025). Accounting for alternation in temporal quality analysis in MapBiomas Brazil. *International Journal of Digital Earth*, 18(1). https://doi.org/10.1080/17538947.2025.2528604

- **Verification:** `full_text_verified`.
- **Contribution:** shows that annual class alternation is much more frequent in MapBiomas than in reference data, particularly in pasture-native-vegetation transitions, while aggregate change totals remain more stable.
- **Relevance:** supports the use of five-year endpoint accounting as the primary stock-flow framework and requires caution when interpreting short annual intermediate sequences.
- **Project distinction:** the project uses annual data selectively for within-interval pathway detection while anchoring inclusion and accounting to declared endpoints.
- **Manuscript use:** ESSD temporal-quality rationale and uncertainty metadata; LUP limitation when discussing short pasture-mediated paths.

## Closest empirical and analytical precedents

### LIT004 Caballero et al. 2023

**Reference:** Caballero, C. B., Biggs, T. W., Vergopolan, N., West, T. A. P., and Ruhoff, A. (2023). Transformation of Brazil's biomes: The dynamics and fate of agriculture and pasture expansion into native vegetation. *Science of the Total Environment*, 896, 166323. https://doi.org/10.1016/j.scitotenv.2023.166323

- **Verification:** `full_text_verified` from the supplied publication PDF.
- **Data and design:** MapBiomas Collection 6, 1985-2020, all Brazilian biomes; annual trends, operational primary-secondary-unstable clearing rules, two broad transition periods and 10 km by 10 km trend mapping.
- **Contribution:** establishes the national and biome-specific transformation among native vegetation, pasture and crops, including pasture expansion, later crop replacement and frontier hotspots.
- **Direct overlap:** native-vegetation loss, pasture expansion, pasture-to-cropland conversion, biome contrasts and spatial concentration.
- **Project distinction:** the project uses Collection 11, a fixed selected-cell domain in Cerrado and Amazon, explicit five-year stock-flow identities, fixed-1985 pasture-cohort accounting, pasture-origin partitions, annual intermediate-pathway detection, cell episodes, Moran-LISA inference and MAUP sensitivity.
- **Interpretation boundary:** the article's Sankey links selected states and must not be described as a complete annual reconstruction of individual pixel pathways. Its operational use of primary vegetation means vegetation observed as native at the start of the series, not proof of an undisturbed pre-1985 history.
- **Manuscript use:** central predecessor in both manuscripts; external plausibility benchmark rather than a numerical reproduction target.

### LIT005 Macedo et al. 2012

**Reference:** Macedo, M. N., DeFries, R. S., Morton, D. C., Stickler, C. M., Galford, G. L., and Shimabukuro, Y. E. (2012). Decoupling of deforestation and soy production in the southern Amazon during the late 2000s. *Proceedings of the National Academy of Sciences*, 109(4), 1341-1346. https://doi.org/10.1073/pnas.1111374109

- **Verification:** `full_text_verified`.
- **Contribution:** demonstrates substantial soybean expansion over previously cleared and pasture land in Mato Grosso and identifies a temporal policy-market transition.
- **Relevance:** independently supports the importance of pasture-to-cropland consolidation and the distinction between old and recent clearings.
- **Project distinction:** the project covers multiple intervals and a broader Cerrado-Amazon domain, partitions pasture origin explicitly and closes stock-flow accounts.
- **Manuscript use:** LUP empirical precedent; ESSD example of a question enabled at broader temporal and spatial coverage by the released data.

### LIT006 Seixas et al. 2025

**Reference:** Seixas et al. (2025). Conversion from forest to agriculture in the Brazilian Amazon from 1985 to 2021. *Land*, 14(2), 300. https://doi.org/10.3390/land14020300

- **Verification:** `full_text_verified`.
- **Contribution:** explicitly links the year of deforestation to the year of agricultural establishment and estimates conversion length.
- **Relevance:** it is the closest precedent for temporal linkage between native vegetation loss and crop establishment.
- **Project distinction:** conversion length is a single elapsed-time measure. The project decomposes the intervening pathway, distinguishes pasture by origin and integrates the result with stock-flow closure and spatial robustness.
- **Manuscript use:** direct novelty boundary in both manuscripts. The project must not claim that temporal linkage between deforestation and agriculture is itself new.

### LIT007 Mas et al. 2019

**Reference:** Mas, J.-F., Vasconcelos, R. N., and Franca-Rocha, W. (2019). Analysis of high temporal resolution land use and land cover trajectories. *Land*, 8(2), 30. https://doi.org/10.3390/land8020030

- **Verification:** `abstract_and_key_excerpts_reviewed`.
- **Contribution:** applies categorical sequence analysis, entropy, turbulence, permanence and clustering to annual land-cover trajectories in northeastern Brazil.
- **Relevance:** anticipates trajectory clustering as a general technique.
- **Project distinction:** the project's trajectory states represent directed process balance and activity, with episodes, re-entry and reversal rules, rather than raw land-cover sequences alone.
- **Next action:** read the full text before finalizing any novelty claim concerning trajectory analysis.

## Dataset and biome mapping foundations

### LIT008 Souza et al. 2020

**Reference:** Souza, C. M. et al. (2020). Reconstructing three decades of land use and land cover changes in Brazilian biomes with Landsat archive and Earth Engine. *Remote Sensing*, 12(17), 2735. https://doi.org/10.3390/rs12172735

- **Verification:** `methodological_source`; abstract and methodological description reviewed.
- **Contribution:** documents the MapBiomas national annual land-use and land-cover mapping architecture.
- **Relevance:** background for the data source and its intended uses.
- **Project distinction:** it produces the underlying classification rather than the stock-flow, pathway and spatial-inference products developed here.
- **Manuscript use:** ESSD data-source section.

### LIT009 Alencar et al. 2020

**Reference:** Alencar, A. et al. (2020). Mapping three decades of changes in the Brazilian savanna native vegetation using Landsat data processed in the Google Earth Engine platform. *Remote Sensing*, 12(6), 924. https://doi.org/10.3390/rs12060924

- **Verification:** `methodological_source`; abstract and key methodological passages reviewed.
- **Contribution:** documents long-term Cerrado native-vegetation mapping and the challenges of separating forest, savanna and grassland formations.
- **Relevance:** biome-specific MapBiomas foundation and interpretation boundary for native-vegetation changes.
- **Manuscript use:** ESSD data-source and classification context.

### LIT010 Franca Rocha et al. 2024

**Reference:** Franca Rocha, W. J. S. et al. (2024). Towards uncovering three decades of LULC in the Brazilian drylands: Caatinga biome dynamics (1985-2019). *Land*, 13(8), 1250. https://doi.org/10.3390/land13081250

- **Verification:** `abstract_and_key_excerpts_reviewed`.
- **Contribution:** provides regional context for long-term MapBiomas land-use and land-cover dynamics outside the focal domain.
- **Relevance:** demonstrates the broader biome-specific literature but is not a direct analytical competitor.
- **Manuscript use:** optional contextual citation; low priority for the central argument.

## Regeneration and secondary vegetation

### LIT011 Rosa et al. 2021

**Reference:** Rosa, M. R. et al. (2021). Hidden destruction of older forests threatens Brazil's Atlantic Forest and challenges restoration programs. *Science Advances*, 7(4), eabc4547. https://doi.org/10.1126/sciadv.abc4547

- **Verification:** `abstract_and_key_excerpts_reviewed`.
- **Contribution:** shows that stable total forest cover can conceal loss of older forest, gain of younger forest and repeated clearing of regenerating vegetation.
- **Relevance:** establishes that net stability can hide substantial turnover and that regeneration durability matters.
- **Project distinction:** different biome and an age-of-forest framework rather than the directed NAT-PAS-TMP stock-flow system.
- **Next action:** full-text review before using the paper to delimit a regeneration-related novelty claim.

### LIT012 Nunes et al. 2020

**Reference:** Nunes, S., Oliveira, L., Siqueira, J., Morton, D. C., and Souza, C. M. (2020). Unmasking secondary vegetation dynamics in the Brazilian Amazon. *Environmental Research Letters*, 15(3). https://doi.org/10.1088/1748-9326/ab76db

- **Verification:** `abstract_and_key_excerpts_reviewed`.
- **Contribution:** quantifies the extent, age and repeated loss of secondary vegetation in the Brazilian Amazon.
- **Relevance:** constrains claims concerning regeneration durability and repeated clearing.
- **Project distinction:** focuses on secondary-vegetation age rather than pasture-crop stock-flow balance and pathway composition.
- **Next action:** full-text review before final manuscript synthesis of regeneration-related findings.

## Context and external convergence

### LIT013 Parente and Ferreira 2018

**Reference:** Parente, L. and Ferreira, L. (2018). Assessing the spatial and occupation dynamics of the Brazilian pasturelands based on the automated classification of MODIS images from 2000 to 2016. *Remote Sensing*, 10(4), 606. https://doi.org/10.3390/rs10040606

- **Verification:** `full_text_verified`.
- **Contribution:** maps Brazilian pasture dynamics and supports the interpretation of a national pasture expansion-to-stabilization inflection around the mid-2000s.
- **Relevance:** external temporal benchmark for changes in pasture stock and land-use intensification.
- **Project distinction:** coarser MODIS-based pasture mapping without directed origin-destination accounting.
- **Manuscript use:** LUP temporal context and discussion.

### LIT014 Li et al. 2026

**Reference:** Li, C., Harris, A., Marimon, B. S., et al. (2026). Three decades of habitat fragmentation dynamics and landscape transformation in the Cerrado-Amazon transition. *Landscape Ecology*, 41, 95. https://doi.org/10.1007/s10980-026-02343-w

- **Verification:** `full_text_verified`.
- **Contribution:** documents heterogeneous fragmentation histories and landscape transformation across the Cerrado-Amazon transition.
- **Relevance:** independently supports spatial heterochrony between older agricultural occupation and more recent frontier transformation.
- **Project distinction:** landscape-pattern and fragmentation metrics rather than stock-flow origin and pathway accounting.
- **Manuscript use:** LUP spatial interpretation; possible ESSD domain context.

### LIT015 Silveira et al. 2022

**Reference:** Silveira, J. G. et al. (2022). Land use, land cover change and sustainable intensification of agriculture and livestock in the Amazon and the Atlantic Forest in Brazil. *Sustainability*, 14(5), 2563. https://doi.org/10.3390/su14052563

- **Verification:** `full_text_verified`.
- **Contribution:** provides aggregate land-cover trends and a sustainable-intensification discussion for the Amazon and Atlantic Forest.
- **Relevance:** broad contextual comparison.
- **Project distinction:** aggregate biome totals without the project's trajectory, origin, pathway and spatial-robustness architecture.
- **Manuscript use:** optional LUP context; not central to novelty.

## Implications for the two manuscripts

### ESSD

The data paper should position the release as an integration and reproducibility contribution. It must not claim that annual MapBiomas trajectories, land-balance methods or vegetation-pasture-crop transitions are individually new. Its strongest distinction is a reusable data architecture that joins endpoint accounting, pasture origin, within-interval pathway information, cell trajectories, uncertainty flags and spatial-sensitivity products.

The most important ESSD references are Pontius et al. (2004), Pendrill et al. (2019), Souza et al. (2020), Alencar et al. (2020), Matos et al. (2025), Seixas et al. (2025) and Caballero et al. (2023).

### Land Use Policy

The policy paper should begin from the established broad transformation documented by Macedo et al. (2012), Caballero et al. (2023), Parente and Ferreira (2018) and related studies. Its contribution is to show how interpretation changes when pasture history, intermediate pathways, temporal recurrence and spatial robustness are made explicit.

The paper should avoid treating every NAT-to-TMP endpoint transition without detected pasture as direct conversion. It should also avoid interpreting vegetation present in 1985 as demonstrably primary or pasture present in 1985 as established in that year. These states are left-censored.

## Outstanding literature tasks

1. Complete full-text review of Rosa et al. (2021), Nunes et al. (2020) and Mas et al. (2019).
2. Search specifically for directed native-vegetation-pasture-temporary-crop accounting in the MATOPIBA, Zalles and Souza-Filho literature.
3. Reassess each novelty statement after the targeted search and before freezing either manuscript abstract.
4. Confirm journal-specific reference formatting only during manuscript preparation; retain DOI-based canonical identities in this register.
5. Update the companion crosswalk when a paper changes verification status or manuscript role.

## Governance

- Add literature here only after recording the source, verification level and project relevance.
- Do not silently change `abstract_and_key_excerpts_reviewed` to `full_text_verified`.
- Do not copy external claims into the Phase 9 internal evidence matrix.
- Version this register when a new publication changes the project's novelty boundary, interpretation or manuscript allocation.

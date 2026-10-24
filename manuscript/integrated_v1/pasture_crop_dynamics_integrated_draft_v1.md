# Pasture stocks, observed conversion pathways and spatially uneven agricultural change in the Brazilian Cerrado and Amazon

**Integrated analytical manuscript — first working draft, 24 October 2026.** Evidence authority: matrix v4.4 and cumulative events-v6. This draft brings RQ1–RQ5 together without changing accepted findings or fitting new models. Internal evidence markers connect paragraphs to the accompanying claim register and can be removed for submission. Authorship, the final dataset citation, literature coverage and journal formatting remain to be finalized. Figure numbering is provisional; Figs. 1 and 4 are specified in the display plan but have not been assembled.

## Abstract

Land-cover stocks, endpoint conversions and observed histories describe different aspects of agricultural change. We integrated annual land-cover observations with five-year accounting across 24,889 fixed hexagonal cells in the Brazilian Cerrado and Amazon, using 1985–2020 as the primary period and 2020–2025 as a diagnostic extension. The analysis combined the endpoint fate of a fixed 1985 pasture cohort, origins of pasture-to-temporary-crop conversion, intermediate pasture detection, cell trajectories, spatial association and scale/zoning sensitivity. Of the 49.036 million ha baseline pasture cohort, 63.13% was classified as pasture and 19.94% as temporary crops in 2020; these are endpoint compositions, not uninterrupted survival. Primary pasture-to-crop interval conversions summed to 20.119 million ha, of which 46.91% originated in spells continuously observed since 1985 and 53.09% in confirmed post-1985 entries. Observed re-entry contributed 15.42% of the entry component. At domain scale, native-vegetation-to-pasture replenishment exceeded pasture-to-crop consolidation in every interval. Nevertheless, 2,598 retrospectively selected cells contained 87.5% of primary native-to-crop endpoint conversion, with contrasting regional trajectories. All canonical Global Moran tests indicated positive association, whereas local hotspot stability depended on the metric and spatial support. Aggregate comparisons were robust across alternative grids, but native-to-crop hotspot footprints were scale- and zoning-sensitive. Agricultural monitoring therefore requires simultaneous reporting of stocks, directed flows, observation-conditioned histories and spatial uncertainty. The results describe mapped transitions and associations; they do not establish causal displacement, first-ever pasture establishment or a universal frontier succession.

## 1. Introduction

Agricultural change can involve conversion of native vegetation, replacement of existing agricultural uses and continued turnover within previously modified landscapes. Soy-specific research has documented the relevance of both previously cleared land and native vegetation to agricultural expansion, while distinguishing the conditions under which production and deforestation change together or diverge (Macedo et al., 2012; Song et al., 2021). Those studies motivate careful separation of transitions and histories; their commodity-specific results cannot be transferred directly to the broader temporary-crop class analyzed here.

A pasture stock is not a dated pasture-establishment event, and land classified as pasture at two dates need not have remained pasture between them. Similarly, native vegetation at the beginning and temporary crops at the end of an interval do not establish a direct pathway. Spatial aggregation adds another distinction: a cell can simultaneously contain pasture-to-crop conversion and native-to-pasture conversion, even when those processes occur on different pixels. Their relative magnitudes need not imply a sequence followed by individual land parcels.

Annual land-cover histories provide a way to examine these distinctions over longer periods. The MapBiomas framework reconstructs annual land-cover series from Landsat observations (Souza Jr. et al., 2020). Here, a common raster lattice, fixed spatial support and explicit observational states allow stocks, endpoint flows and selected annual histories to be compared without silently changing populations or denominators. The common support also permits tests of spatial association and sensitivity to aggregation.

We address five questions: (RQ1) how the fixed pasture cohort observed in 1985 is redistributed among later endpoint states; (RQ2) which observed pasture-spell origins contribute to pasture-to-temporary-crop conversion; (RQ3) how often pasture is detected between native-to-crop endpoints; (RQ4) how process magnitudes, temporal trajectories and spatial concentrations differ across the domain and biomes; and (RQ5) which findings remain stable under alternative grid scales and zoning. The aim is an integrated description of the land system, rather than a causal model of commodity expansion or a chronology of first-ever land conversion.

## 2. Methods

### 2.1 Study domain, observations and temporal boundaries

The fixed analytical domain contains 24,889 complete hexagonal cells of approximately 20,000 ha each, reconstructed from a parent set of 32,305 cells intersecting the Cerrado and Amazon. Cells were retained when recognized anthropogenic land cover exceeded 0.01 ha in either 1985 or 2025. The domain is therefore a defined, non-random analytical population, not a complete pixel partition of the two biomes. Its selection uses both endpoint years even though primary temporal interpretation ends in 2020. Complete hexagons also contain 19.1513 million ha outside the two target-biome polygons. Findings must be interpreted on this support rather than generalized to all land in either biome.

We used the project-pinned MapBiomas Brazil Collection 11 `coverage_v3` annual land-cover image, with 41 bands from 1985 through 2025. The primary reporting dates were 1985, 1990, 1995, 2000, 2005, 2010, 2015 and 2020. The 2025 endpoint and interval 2020–2025 were retained but flagged as diagnostic, reflecting terminal-observation and temporal-filter-support qualifications. The designation does not indicate a failed accounting check. Existing observations cannot identify events before 1985 or a subsequent termination after the final observation.

Pixel-area reductions retained the native geographic raster lattice and affine transformation; areas were computed in hectares from pixel area rather than by assuming that every geographic pixel has identical area. Spatial geometries and overlap calculations used the project's equal-area representation. NAT denotes the accepted group of native-vegetation classes, PAS planted pasture, and TMP the accepted temporary-crop group. Other agriculture, other states, water, nodata, unexpected codes and masked observations remained explicit. TMP is not a soybean-only class. NAT includes forest and non-forest native formations, so NAT conversion is not a forest-only deforestation metric. The exact class-code groups and raster transform are retained in the versioned configuration.

The evidence audit in this paper is not a new estimate of Collection 11 thematic accuracy. Souza Jr. et al. (2020) provides background on the annual mapping framework; accuracy results from an earlier product are not treated as validation of the specific collection and trajectories used here.

### 2.2 Common accounting and distinct estimands

For each cell and five-year interval, we distinguished land-cover stocks at the endpoints from directed endpoint flows. Consolidation, C, was PAS at t0 and TMP at t1; replenishment, R, was NAT at t0 and PAS at t1. Native-to-crop endpoint conversion was NAT at t0 and TMP at t1. These operational names describe mapped states, not management intent, the full intermediate sequence or a causal effect.

The net C–R balance was C−R and the bounded index was (C−R)/(C+R), defined only where C+R was positive. Replenishment dominance required an index below −1/3, consolidation dominance above +1/3, and intermediate values were mixed. A cell with neither flow was inactive, not balanced at zero. The index does not equal net pasture-stock change because pasture exchanges area with additional states. Positive net balance alone does not establish consolidation dominance under the 2:1 rule.

Process-specific relative metrics divided directed areas by their corresponding initial stocks. Observed zeros were retained; undefined ratios remained missing. Domain fractions divided sums of areas rather than averaging cell ratios. Sums across intervals can include a pixel more than once and are not spatially deduplicated converted areas. [Table 1](table01_estimands_and_populations_v1.md) separates the populations and denominators used across RQ1–RQ5.

### 2.3 Fixed 1985 pasture cohort and observed pasture-spell origins

RQ1 followed a fixed baseline pixel population at the nine reference dates. The original export defined membership from PAS in 1985 together with the original pasture-age code 100 at that boundary; membership was not redefined after departures or returns. Following discovery of source-age encoding anomalies, the unchanged baseline cohort was revalidated against coverage-only PAS-1985 stock. Per-cell area equivalence and the accepted endpoint summaries passed the recorded checks. This revalidation did not independently resample every baseline pixel. RQ1 therefore retains its fixed-cohort, endpoint-composition interpretation.

RQ2 used a different estimand: the origin of the current observed PAS spell at t0 among PAS→TMP endpoint conversions. Corrected origin was reconstructed from annual coverage, not decoded from public pasture-age values. PAS continuously observed since 1985 was initial; PAS whose current spell began after a confidently observed non-PAS state was confirmed entry; and insufficient annual observations yielded unresolved current-spell origin. A confident exit ended the current spell. Missing observations broke confirmation of continuity but did not themselves prove an exit or create a confirmed entry. Initial indicates continuity since an observation boundary, not physical establishment age.

Within confirmed entry, any PAS observed strictly before the current entry identified observed re-entry. No earlier observed PAS with complete valid earlier history since 1985 identified first observed entry; no earlier observed PAS with an earlier gap identified uncertain prior history. The label was fixed at entry and carried during the confirmed spell. Earlier PAS could establish re-entry despite intervening gaps, but gaps were never bridged. Uncertain earlier history after a confident non-PAS reset differed from unresolved origin of the current spell. First observed entry did not establish first-ever implantation.

Each subclass was exported for both PAS stock at t0 and PAS→TMP flow. We distinguished its contribution to all conversion, its conditional share within confirmed-entry conversion, and its conditional share within entry stock. In the first 1985–1990 interval, entry stock and conversion were zero by construction, so conditional entry fractions were undefined. Native assurance covered the coverage-derived engine, including auxiliary age-201 resets and preserved synthetic histories; it did not establish complete numerical accuracy of the public pasture-age v2 asset.

Boundary sensitivity repeated the categorical origin reconstruction with observation boundaries in 1995 and 2000. We compared identical endpoint conversions during the common calendar period 2000–2020 and the first four five-year intervals after each boundary. Equal-follow-up comparisons changed calendar periods, baseline populations and conversion weights. Stock-normalized endpoint conversion fractions were C_origin/S_origin(t0), with an initial/entry fraction ratio where both denominators permitted it. Initial stock was not time-integrated exposure, and these fractions were not annual hazards or adjusted preferences.

### 2.4 Intermediate pasture and cell trajectories

For RQ3, the endpoint NAT(t0)→TMP(t1) population was evaluated in the four intervening annual observations. Complete and incomplete intermediate support remained separate. Among completely observed histories, pasture detection rules retained any intermediate PAS year, at least two PAS years, and at least two consecutive PAS years. Absence of detected pasture was not labeled direct conversion. Annual sampling and class uncertainty can conceal short or misclassified intermediate episodes.

Cell-state classes used thresholds estimated once from the declared seven-interval primary reference population and then held fixed, including for the diagnostic interval. The principal temporal axes were NAT→TMP magnitude and the C–R index. Runs of the same cell state formed observed multiquinquennial episodes; returns and reversals were retained, with boundary flags. These are cell-level states and durations, not continuous land use on identical pixels.

The high-NAT→TMP group consisted of cells reaching the frozen high-magnitude class in at least one primary interval, with a threshold of approximately 357.793 ha per interval. This retrospective selection remained fixed during temporal comparisons and was distinct from the baseline pasture cohort. It was not a random sample or a statistically delineated cluster. Spatial summaries included process-area-weighted centers of the fixed cell group; movement of those centers described changing activity weights, not movement of the same converted land.

### 2.5 Spatial association, persistence and biome attribution

The fixed shared-edge graph contained 67,453 undirected links, 134,906 directed row-standardized weights and 163 islands. Islands were retained without artificial links. Complete-domain metrics used the common graph; conditional metrics inherited support-specific subgraphs with surviving edges re-standardized. Structural zeros remained distinct from undefined support.

Global Moran's I was calculated for 13 specifications over eight intervals: nine complete-domain specifications covering raw area/balance and occurrence, and four conditional specifications. Tests used 9,999 unrestricted permutations on the observed support. Two-sided Monte Carlo p-values compared absolute departures from the exact permutation expectation. Benjamini–Yekutieli correction used the prespecified complete/conditional and primary/diagnostic families. Individual interval tests did not test differences between dates.

Local Moran analysis provided map-specific HH, LL and spatial-outlier classes, following the local-association framework of Anselin (1995). Five focal metrics used 9,999 conditional randomizations. BH correction at q≤0.05 was the primary map-level rule; BY correction was retained as a conservative sensitivity. Unsupported cells and islands received explicit statuses. HH for an absolute-area metric identified locally high mapped activity; it did not define a causal region. For the signed C–R index, relative HH did not automatically imply a positive index or consolidation dominance.

Primary persistence meant at least two consecutive primary intervals in the same significant HH or LL class. Adjacent-map stability used Jaccard overlap. Cell-map records, persistent-cell counts and footprint hectares were kept distinct. Repeated observations from the same cell were not treated as independent transition probabilities from a fitted model.

The primary biome comparison assigned each whole cell to the biome with greatest equal-area overlap, partitioning the domain into 14,213 Amazon-associated and 10,676 Cerrado-associated cells. A sensitivity excluded all 582 transbiome cells. Cell process totals were not multiplied by biome-overlap fractions because that would assume uniform within-cell process distribution. Biome-specific Global Moran tests were recomputed on induced graphs; local-cluster summaries attributed the accepted combined-domain LISA classes without refitting within-biome local models.

### 2.6 Scale, zoning and evidence synthesis

RQ5 compared approximately 10,000-ha, shifted 20,000-ha and 40,000-ha grids over the fixed canonical footprint. Process metrics were reconstructed on the alternatives rather than interpolated from canonical cell values. Area-valued cell metrics were normalized per 10,000 ha of analytical support where needed, and distribution comparisons were support-area weighted. The primary alternative-grid support rule retained units with at least 50% domain support, with 25% and 75% sensitivities.

Documented criteria separated aggregate signs and magnitudes, temporal ordering/extrema, conditional-support coverage, Global Moran magnitude/significance, and HH location, recurrence and persistence. Global and local tests retained 9,999 permutations. Local footprints were compared through area-overlap crosswalks on common support. Passing numerical validation did not require every substantive robustness criterion to pass. The canonical approximately 20,000-ha grid remained primary throughout.

The integrated evidence matrix contained 35 findings: four for RQ1, three for RQ2, two for RQ3, 18 for RQ4 and eight for RQ5. This draft retained their supported/qualified statuses and interpretation boundaries. Historical source-anchor paths were resolved by exact content hashes when possible; four biome findings were additionally checked directly against accepted numerical outputs because their original narrative anchor was absent from the current repository. This was a documentary/numerical synthesis, not a rerun of the complete analytical chain or independent field validation.

## 3. Results

### 3.1 RQ1 — Redistribution of the fixed baseline pasture cohort

The fixed 1985 pasture cohort covered 49.036 million ha. By 2020, 63.13% was classified as PAS, 19.94% as TMP, 6.82% as NAT and 9.22% as other agricultural uses. The PAS share reached its primary-period minimum in 2020. These endpoint proportions did not identify uninterrupted pasture persistence, departure dates or pathways between reference years. [E:P9A031;P9A032]

The Amazon-associated cohort had 74.82% PAS and 12.02% TMP in 2020, compared with 60.94% PAS and 21.43% TMP for the Cerrado-associated cohort. The denominators were the respective fixed cohort areas, not all land in each biome. In diagnostic 2025, combined-domain PAS, TMP and NAT shares were 58.22%, 21.42% and 6.43%, respectively. The diagnostic endpoint extended the description without replacing the primary-period conclusions. [E:P9A033;P9A034]

[Figure 2](../../figures/manuscript_integrated_v1/fig02_fixed_1985_cohort_endpoints_v1.png) displays the complete endpoint series and the 2020 biome-associated compositions.

### 3.2 RQ2 — Observed origins of pasture-to-crop conversion

Primary PAS→TMP conversions summed to 20.119468 million ha across seven intervals: 46.91% was attributed to PAS spells continuously observed since 1985, 53.09% to confirmed post-1985 entry and 0.000311% to unresolved origin, the latter corresponding to 62.568807 ha. The first interval was 100% initial by construction. In 2015–2020, initial and entry shares were 31.08% and 68.92%. The first entry share above 50% occurred in 2000–2005 under the canonical boundary; that crossing was not a process threshold. [E:P9A035;P9A036;P9A037]

Boundary sensitivity materially changed origin composition on identical endpoint conversions. Across 15.221177 million ha of 2000–2020 interval conversions, initial shares were 38.10%, 64.70% and 78.07% for boundaries in 1985, 1995 and 2000. The two later boundaries did not produce a primary-period entry majority; they crossed only in diagnostic 2020–2025. Calendar-paired ordering follows set nesting. First-20-year initial shares were 63.64%, 72.25% and 78.07%, but those comparisons used different periods and baseline populations. The sensitivity did not estimate an artifact fraction. [E:P9A035;P9A036]

Within the 10.681383 million ha primary confirmed-entry component, first observed entry contributed 9.034642 million ha (84.583066%), observed re-entry 1.646645 million ha (15.416026%), and uncertain prior history 96.952164 ha (0.000907674%). First-observed and re-entry contributions to all primary PAS→TMP flow were 44.904973% and 8.184336%, respectively. The uncertain-prior-history class had a confirmed current entry and was distinct from unresolved current-spell origin. These interval-area sums were not unique converted hectares. [E:P9A036;P9A037]

Re-entry was 19.117876% of entry conversion in 2015–2020 and 32.488051% in diagnostic 2020–2025. Its entry-stock shares at t0 were 15.853277% and 17.906327%. The primary flow-share sequence was not monotonic: it decreased from 17.005648% in 2005–2010 to 15.574771% in 2010–2015 before rising again. Baseline conditional entry fractions were undefined. [E:P9A035]

Stock-normalized initial/entry endpoint-fraction ratios ranged from 1.1674 to 1.3979 across the six estimable canonical primary intervals. Corresponding primary ranges were 1.0046–1.1964 for the 1995 boundary and 0.8164–1.1016 for 2000. Diagnostic ratios were 0.8072, 0.7209 and 0.6712. Origin shares combined stock composition and per-stock endpoint fractions; they were not themselves relative conversion propensities. [E:P9A035;P9A036]

[Figure 3](../../figures/rq2_entry_reentry_v4_4/fig01_entry_reentry_composition_v4_4.png) separates flow origins and conditional re-entry flow/stock shares. The existing boundary-sensitivity and endpoint-fraction figures are proposed as supplementary displays.

### 3.3 RQ3 — Pasture detected between native-to-crop endpoints

Within the fixed high-NAT→TMP cell group, pasture detected in at least one intermediate year represented 6.51% of summed primary NAT→TMP endpoint area. This was a selected-group result, not a full-domain pathway fraction. It did not establish that the remaining area underwent direct NAT→TMP conversion: other intermediate classes, incomplete observations, short episodes between annual maps and classification instability remained possible. [E:P9A003;P9A004]

The pathway result therefore describes detected intermediate pasture in the observed annual sequence. It does not identify all prior land-use history or whether pasture was a necessary intermediate stage across the wider domain.

### 3.4 RQ4 — Aggregate balance, concentration and changing cell states

Replenishment exceeded consolidation in aggregate in all eight intervals, including every primary interval. The domain C–R index was −0.838 in 1985–1990 and −0.656 in diagnostic 2020–2025. Domain-level dominance nevertheless coexisted with locally consolidation-dominant cells. [E:P9A005]

The retrospectively selected high-NAT→TMP group contained 2,598 cells, 10.44% of the domain, but 87.5% of accumulated primary NAT→TMP endpoint area. Group activity peaked at 2.116 million ha in 2000–2005 and declined to 0.546 million ha in 2015–2020, 74.2% below the peak. The decline in high-class area did not mean disappearance of endpoint conversion. The activity-weighted center shifted approximately 692 km north/northeast between the first and last primary intervals. This measured redistribution of weights among fixed cells, not migration of identical pixels or a causally identified frontier. [E:P9A006;P9A007;P9A008]

Within that group, Amazon-associated aggregate C–R indices were +0.621 and +0.415 in 2010–2015 and 2015–2020, both consolidation-dominant; corresponding Cerrado-associated indices were +0.095 and −0.037, both mixed. Consolidation dominance in both late primary intervals occurred in 367/648 Amazon-associated cells (56.6%) and 427/1,950 Cerrado-associated cells (21.9%). These denominators referred to the selected group, not all biome-assigned cells. [E:P9A009;P9A010]

Persistent late states coexisted with earlier reversals: 83.0% of Amazon-associated and 57.2% of Cerrado-associated high-group cells showed at least one direct or mediated dominance reversal during the primary period. The sequence therefore did not support a universal, one-way cell-level progression from replenishment to consolidation. It also did not identify pixel-level reversal probabilities. [E:P9A011]

### 3.5 RQ4 — Global association and local spatial structure

All 104 canonical Global Moran tests were positive and BY-significant. For several absolute metrics, coefficients were lower in the last primary interval than initially: consolidation changed from 0.799 to 0.559, replenishment from 0.770 to 0.614, and NAT→TMP from 0.550 to 0.361. Separate permutation tests did not establish significant between-date differences or a temporal trend. [E:P9A012;P9A013]

Across the mapped series, replenishment produced 18,067 HH cell-map records and 4,354 cells with primary HH persistence, with mean adjacent HH Jaccard overlap 0.389. NAT→TMP produced 3,134 HH records, 664 primary persistent cells and lower overlap, 0.260. Cell-map counts over the eight mapped intervals and persistent-cell counts in the seven-interval primary window describe different populations. Large significant totals for zero-rich absolute metrics included extensive LL structure and were not interpreted as extensive hotspots. [E:P9A014;P9A015]

The C–R index had the strongest adjacent HH stability among the focal local results: 19,358 HH cell-map records, 3,543 primary persistent cells and mean Jaccard 0.620. Relative HH in this conditional index did not itself establish consolidation dominance. The conservative BY correction retained 72,221 of 168,860 BH-significant cell-map records (42.77%), showing that the multiple-testing choice materially affected mapped significance. Primary BH patterns and BY-robust subsets were not conflated. [E:P9A016;P9A017]

### 3.6 RQ4 — Contrasts between biome-associated populations

Across primary intervals, Amazon-associated and Cerrado-associated consolidation summed to 5.10 and 15.02 million ha, respectively. Replenishment sums were 47.81 and 45.81 million ha, and NAT→TMP endpoint sums 2.04 and 7.11 million ha. These were whole-cell primary-biome totals, not exact within-biome pixel totals or unique areas across intervals. [E:P9A018]

Mean primary NAT→TMP magnitude-state changes were 0.79 per Amazon-associated cell and 2.13 per Cerrado-associated cell. Constant cell-state sequences accounted for 68.0% and 18.0%, respectively. Persistent replenishment HH involved 2,785 Amazon-associated and 1,569 Cerrado-associated cells, whereas persistent NAT→TMP HH involved 153 and 511 cells. These local counts attributed the accepted combined-domain LISA pattern; they were not new within-biome local models. [E:P9A019;P9A020]

Removing all 582 transbiome cells retained the 160 biome-specific Global Moran significance decisions. The largest absolute difference in I between boundary treatments was 0.044848. This supported stability of the principal biome comparison under that exclusion, without converting whole-cell assignments into exact pixel partitions. [E:P9A021]

[Figure 5](../../figures/manuscript_integrated_v1/fig05_primary_biome_process_totals_v1.png) summarizes the primary process totals with separate vertical scales and explicit whole-cell attribution.

### 3.7 RQ5 — Different robustness profiles for aggregates and local footprints

All 192 aggregate and 48 temporal comparisons passed the prespecified Phase 8C criteria. The shifted 20,000-ha grid passed all comparison components, while the 10,000-ha and 40,000-ha grids retained conditional distribution/support sensitivities. Robust aggregate behavior did not imply invariant cell-value distributions. [E:P9A022]

All 120 alternative-grid Global Moran coefficients were positive and BY-significant; 119/120 interval magnitude checks passed. One magnitude failure and 8/30 strict temporal failures showed that exact coefficient magnitudes and ordering were less stable than the existence and positive direction of association. All six composite grid-window assessments failed at least one strict Global Moran criterion. That did not imply absence of clustering. [E:P9A023;P9A024]

Local HH robustness was metric-dependent. Replenishment, net C–R balance and the bounded C–R index each passed all six grid-window assessments. Consolidation passed three of six complete assessments and 16/24 interval maps. NAT→TMP passed none of the six complete assessments and only 7/24 interval comparisons. Many sensitive comparisons retained overlapping cores while changing footprint extent, rather than indicating universal relocation. [E:P9A025;P9A026;P9A027]

The canonical approximately 20,000-ha support remained primary after these comparisons. The diagnostic interval affected some full-window assessments, including coarse-grid consolidation, but did not create the primary NAT→TMP footprint sensitivity. Acceptance of the robustness analysis meant that its specified comparisons were completed and their sensitivities retained, not that every criterion passed. [E:P9A028;P9A029]

[Figure 6](../../figures/manuscript_integrated_v1/fig06_hh_maup_robustness_v1.png) displays the 30 composite HH assessments. [Table 2](table02_key_results_v1.md) summarizes the five research questions without merging their denominators.

## 4. Discussion

### 4.1 Coexisting consolidation and replenishment are not a universal succession

The integrated evidence connects changing pasture stocks with spatially uneven conversion and persistent replenishment. A substantial share of the fixed baseline pasture cohort was classified as temporary crops by 2020, yet NAT→PAS replenishment exceeded PAS→TMP consolidation in every interval. These findings are compatible because they concern different populations and transitions. They do not show that the specific pasture removed for crops was replaced by native-vegetation conversion elsewhere, nor quantify a displacement effect.

This distinction matters when interpreting agricultural change through a simple frontier sequence. The data show simultaneous flows and cell-level persistence/reversals rather than a universal, one-way progression. Earlier soy research considered cropland expansion on previously cleared land together with native-vegetation conversion and policy context (Macedo et al., 2012; Song et al., 2021). Our broader TMP endpoint accounting supplies complementary history and spatial descriptors, but does not replicate those commodity studies or identify their drivers. More pasture-to-crop conversion cannot, by itself, be labeled land sparing or proof of reduced native-vegetation pressure.

### 4.2 Pasture history changes the meaning of an entry contribution

The confirmed-entry component is not synonymous with first-time pasture establishment. Its observed re-entry contribution—15.42% of primary entry conversion, or 8.18% of all primary PAS→TMP flow—makes that distinction measurable. Even the larger first-observed subclass only establishes absence of earlier PAS in the available complete history since 1985. Physical establishment before the observation boundary remains unidentified, and recurrent mapped PAS may include classification effects as well as actual land-use changes.

RQ1 and RQ2 also cannot be substituted for one another. A pixel can remain part of the fixed 1985 cohort after leaving and returning to PAS, while the later current spell belongs to a post-1985 entry in RQ2. Conversely, a current spell continuously observed since a later sensitivity boundary may have begun after 1985. The 100% initial share at the first boundary and the set-nesting behavior of later boundaries explain why composition alone cannot identify a process transition. The results retain their substantive descriptive meaning without assigning a causal or mechanical artifact fraction.

The comparison between flow and stock composition further qualifies interpretation. Conversion-origin shares combine the amount of available stock with the fraction of that stock observed in the endpoint flow. Stock-at-t0 normalization adds information, but is not time-integrated exposure and does not adjust for spatial or cohort differences. Inferences about comparative risks, physical renewal processes or changing hazards would require a separately specified event-history design.

### 4.3 Endpoint pathways require observations beyond a two-date label

The 6.51% detected-intermediate-pasture result does not imply that all remaining high-group NAT→TMP conversion was direct. Annual observations improve on a two-date comparison but do not necessarily resolve short episodes, unobserved years or all other intermediate states. The selected group is also retrospective and contains most, but not all, primary endpoint conversion. A full-domain direct-conversion claim therefore exceeds this evidence.

For monitoring, the useful distinction is between the endpoint event and the annual history that can actually be observed. Retaining incomplete support and alternative persistence-sensitive detection rules avoids turning missing or unstable observations into a substantive no-pasture pathway. It also prevents crop destination, recent pasture presence and original vegetation clearance from being treated as interchangeable dates.

### 4.4 Spatial organization is clearer at some inferential levels than others

Aggregate replenishment dominance, concentrated NAT→TMP activity and positive global association coexisted with changing local footprints. The 2,598-cell high group described concentration of accepted conversion, while Moran/LISA described spatial association under a declared graph. The group was not a spatial cluster, and a locally high value was not necessarily a substantively consolidation-dominant state. These distinctions explain why aggregate totals, cell trajectories and statistical clusters can support different but compatible conclusions.

The MAUP comparisons make this hierarchy operational. Replenishment and C–R balance retained broad HH robustness, whereas native-to-crop hotspot extent and persistence were sensitive to scale and zoning even though global association remained positive. A single hotspot map should therefore not be used as an invariant delineation of priority areas. Reporting support, statistical rule and cross-grid footprint agreement is more defensible than claiming exact local stability from robust totals alone.

The biome contrast also operates at a declared level of aggregation. Whole-cell attribution supports a reproducible comparison across the canonical domain, and transbiome exclusion tests one important boundary sensitivity. It does not assign every converted pixel to a biome or remove all effects of graph topology and spatial selection. Differences in constant-state frequencies should be read alongside structural zeros and the fixed-domain definition, rather than as direct measures of management inertia.

### 4.5 Implications for monitoring and land-use governance

An implication of the combined findings is that monitoring systems should track native-vegetation-to-pasture and pasture-to-crop flows together, while retaining their different stocks, histories and geographic supports. A favorable change in one indicator cannot be assumed to offset the other. Linking those flows into a displacement mechanism or evaluating a policy intervention would require additional identification, commodity, actor or parcel information.

History labels should also be explicit when interpreting conversion from pasture. Continuous observed spells, first observed entries, observed re-entries and uncertain histories describe different evidence. Their meanings depend on the observation boundary and cannot serve as interchangeable proxies for physical pasture age or first clearance. Metadata should preserve those limits, the diagnostic terminal interval and missing-observation states rather than compressing them into one age category.

Finally, spatial targeting can use persistent concentrations as a reason for further verification, with the degree of local robustness reported alongside the map. The current results do not establish which policies, infrastructure changes, prices or tenure arrangements caused the patterns, and they cannot determine parcel compliance or policy effectiveness. These are monitoring implications drawn from descriptive evidence, not estimated treatment effects. [E:P9A030]

### 4.6 Limitations and scope of assurance

Several limits apply across the synthesis. First, the fixed domain was selected using anthropogenic presence at 1985 or 2025 and includes complete-cell area outside the target polygons. It is a coherent analytical population but is not an unbiased sample of all biome land. Second, temporal observations are annual and the main accounting is quinquennial. Endpoint composition is not survival, cell-state duration is not uninterrupted pixel history, and summed interval areas are not unique land converted.

Third, accounting closure and hash authentication demonstrate consistency and traceability within the accepted evidence chain; they do not establish thematic accuracy or quantify classification-induced transition error. Rigorous accuracy assessment requires an appropriate reference, sampling and analysis design (Stehman and Foody, 2019). Our results do not supply such a new assessment. Small unresolved-origin areas cannot be interpreted as low total classification error, and instability in annual labels may affect observed re-entry and short pathways.

Fourth, the terminal 2025 observation remains diagnostic, and events beyond either series boundary are unavailable. The primary/diagnostic distinction is precautionary and retains its source-support qualification; it is not evidence of a failed 2025 accounting reduction. Fifth, spatial permutations evaluate association under specified graphs and supports. They do not remove geographic confounding, provide a causal model or test between-date changes merely because separate dates are significant. Local BH and BY results and metric-specific MAUP sensitivities remain consequential.

The accepted source-age remediation revalidated the original fixed cohort and reconstructed current-spell origin from coverage. Coverage-derived auxiliary-age checks do not constitute complete numeric validation of the public pasture-age asset or retrospectively execute the separate proposed seeded pixel-sampling protocol. Historical executed-text attestations remain absent where recorded as null. The integrated manuscript uses the accepted evidence; it does not independently rerun every preceding stage or establish that no informal exploration occurred before the documented production records.

## 5. Conclusions

The combined RQ1–RQ5 evidence describes agricultural change as coexisting stock redistribution, directed conversion and spatially uneven observed histories. A substantial baseline pasture contribution to later crops coexists with persistent domain-level replenishment; the post-1985-entry contribution contains both first observed entries and observed returns to pasture. Native-to-crop endpoints do not identify complete pathways, and concentrated activity does not imply a universal temporal succession. Aggregate comparisons and positive global spatial association are more robust than some exact local hotspot footprints. These distinctions support observation-window-aware, denominator-explicit and scale-qualified monitoring while defining the additional evidence required for claims about physical age, direct conversion, displacement or causal policy effects.

## Data, code and manuscript status

The development repository is [barroso2501/pasture-crop-dynamic](https://github.com/barroso2501/pasture-crop-dynamic). The exact project evidence and method files used for this draft are recorded in the accompanying source inventory and hash pins. Compact summaries and code are available there; a complete immutable public data release and version-specific DOI have not been declared complete. Final data-availability wording must follow that release, including its unresolved minimum-scope and licensing/attribution checks. No DOI is invented or reserved by this draft.

This is the first integrated analytical draft, not a submission-ready manuscript. The companion data-description manuscript remains a separate product under the accepted project pathway. Proposed claim/display allocation does not freeze Stage 0 governance, settle authorship or establish current journal requirements. Internal evidence markers, final figure assembly, reference expansion and journal formatting remain editorial tasks.

## References

Anselin, L. (1995). Local Indicators of Spatial Association—LISA. *Geographical Analysis*, 27(2), 93–115. https://doi.org/10.1111/j.1538-4632.1995.tb00338.x

Macedo, M. N., DeFries, R. S., Morton, D. C., Stickler, C. M., Galford, G. L., and Shimabukuro, Y. E. (2012). Decoupling of deforestation and soy production in the southern Amazon during the late 2000s. *Proceedings of the National Academy of Sciences*, 109(4), 1341–1346. https://doi.org/10.1073/pnas.1111374109

Song, X.-P., et al. (2021). Massive soybean expansion in South America since 2000 and implications for conservation. *Nature Sustainability*, 4, 784–792. https://doi.org/10.1038/s41893-021-00729-z

Souza Jr., C. M., et al. (2020). Reconstructing Three Decades of Land Use and Land Cover Changes in Brazilian Biomes with Landsat Archive and Earth Engine. *Remote Sensing*, 12(17), 2735. https://doi.org/10.3390/rs12172735

Stehman, S. V., and Foody, G. M. (2019). Key issues in rigorous accuracy assessment of land cover products. *Remote Sensing of Environment*, 231, 111199. https://doi.org/10.1016/j.rse.2019.05.018

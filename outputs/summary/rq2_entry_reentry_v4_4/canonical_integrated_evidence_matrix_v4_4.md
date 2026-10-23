# Integrated evidence matrix v4.4

2026-10-23. 35 finding IDs retained; only P9A035/P9A036 supplemented. Qualified statuses, causal flags, canonical anchors and prior evidence retained. Supplemental chronology uses the accepted 1985-boundary full-domain exports.

## P9A003 — RQ3 / within_interval_pathways

Detected intermediate pasture represents a small share of accumulated endpoint NAT-to-TMP area in the primary high-magnitude cohort.

**Numerical evidence:** Pasture detected in at least one intermediate year = 6.51% of accumulated NAT-to-TMP area in the cohort.

**Interpretation boundary:** This percentage is cohort-specific and sums interval areas; it is not the full-domain share and does not deduplicate pixels across intervals.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Section 7 — Composition of trajectories

## P9A004 — RQ3 / within_interval_pathways

Absence of detected pasture in the annual series does not establish direct native-vegetation-to-crop conversion.

**Numerical evidence:** Other intermediate states and classification instability remain possible.

**Interpretation boundary:** Use 'no pasture detected' rather than 'direct conversion' unless every intermediate state is evaluated.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Sections 1 and 7

## P9A005 — RQ4 / aggregate_process_balance

Replenishment exceeds consolidation in aggregate in every five-year interval.

**Numerical evidence:** Aggregate C-R index is negative in all eight intervals, from -0.838 in 1985-1990 to -0.656 in diagnostic 2020-2025.

**Interpretation boundary:** Aggregate dominance does not imply that every cell is replenishment-dominant.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase2/canonical_spatial_metrics_summary_v1.csv`; SHA256 `4d9a4ee8d9fefa5e281be3a765e20509756c7bb29f86046aaf6d87a1b9314bdf`.

**Source locator:** Eight interval rows; aggregate_cr_balance_index

## P9A006 — RQ4 / nat_tmp_concentration

A small fixed group of high-magnitude cells contains most accumulated endpoint NAT-to-TMP area.

**Numerical evidence:** 2,598 cells = 10.44% of the domain and 87.5% of accumulated 1985-2020 NAT-to-TMP area.

**Interpretation boundary:** The cohort is selected retrospectively and is not random or itself a statistical cluster.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Section 2

## P9A007 — RQ4 / nat_tmp_temporal_concentration

High-cohort NAT-to-TMP activity peaks in 2000-2005 and declines strongly by 2015-2020.

**Numerical evidence:** 2.116 million ha in 2000-2005 versus 0.546 million ha in 2015-2020; decline = 74.2%.

**Interpretation boundary:** Decline in high-class area does not mean disappearance of all NAT-to-TMP activity.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Section 2

## P9A008 — RQ4 / nat_tmp_spatial_redistribution

The activity-weighted center of the high cohort shifts north/northeast over the primary period.

**Numerical evidence:** Approximate net displacement = 692 km between 1985-1990 and 2015-2020.

**Interpretation boundary:** This is redistribution of activity weights among fixed cells, not tracking of identical pixels or a causal frontier trajectory.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Section 3

## P9A009 — RQ4 / regional_cr_balance

Recent high-cohort balance differs between biomes: Amazon is consolidation-dominant while Cerrado remains mixed.

**Numerical evidence:** 2010-2015: Amazon +0.621, Cerrado +0.095; 2015-2020: Amazon +0.415, Cerrado -0.037.

**Interpretation boundary:** These are ratios of regional flow sums, not means of cell indices or classifications of all cells.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

**Source locator:** Section 4

## P9A010 — RQ4 / late_consolidation_persistence

Recent consolidation dominance is more persistent among high-cohort Amazon cells than Cerrado cells.

**Numerical evidence:** Dominant in both late intervals: Amazon 367/648 = 56.6%; Cerrado 427/1,950 = 21.9%.

**Interpretation boundary:** Persistence is defined at five-year cell state, not annual or pixel-level continuity.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_temporal_synthesis_v1.md`; SHA256 `671f34296136545c54fcb1b8090352ceb5b0964d60b1cb818d19a007f6aedf23`.

**Source locator:** Late-primary persistence

## P9A011 — RQ4 / cr_balance_reversals

Persistent late consolidation and earlier reversals coexist; there is no universal linear replenishment-to-consolidation succession.

**Numerical evidence:** Any direct or mediated reversal: Amazon 83.0%; Cerrado 57.2%.

**Interpretation boundary:** Repeated transitions from the same cell are descriptive and are not independent probabilities from a fitted model.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase4/phase4_temporal_synthesis_v1.md`; SHA256 `671f34296136545c54fcb1b8090352ceb5b0964d60b1cb818d19a007f6aedf23`.

**Source locator:** Reversals and recurrence

## P9A012 — RQ4 / global_spatial_autocorrelation

All canonical Global Moran tests show positive spatial association and remain significant after BY correction.

**Numerical evidence:** 104/104 tests positive and BY-significant; 9,999 permutations per test.

**Interpretation boundary:** Global Moran establishes overall association but does not locate clusters or imply causal processes.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase5/global_moran_findings_phase5_v1.md`; SHA256 `6ab0fa6790ea802a5816f8e52aea45862a276a26ab1172f58363280183f1e554`.

**Source locator:** Achado principal

## P9A013 — RQ4 / global_temporal_change

Several absolute process metrics have lower Global Moran coefficients late in the primary period than initially.

**Numerical evidence:** Consolidation 0.799 to 0.559; replenishment 0.770 to 0.614; NAT-to-TMP 0.550 to 0.361.

**Interpretation boundary:** Separate interval permutation tests do not test the significance of between-date differences or a temporal trend.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase5/global_moran_findings_phase5_v1.md`; SHA256 `6ab0fa6790ea802a5816f8e52aea45862a276a26ab1172f58363280183f1e554`.

**Source locator:** Magnitudes in the full domain

## P9A014 — RQ4 / local_hotspots

Replenishment has the broadest and most persistent absolute-process HH structure.

**Numerical evidence:** 18,067 HH cell-map records; 4,354 cells with primary HH persistence; mean adjacent HH Jaccard = 0.389.

**Interpretation boundary:** HH denotes locally high values relative to the map and significant neighbors; it is not a causal region.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

**Source locator:** Replenishment

## P9A015 — RQ4 / local_hotspots

Endpoint NAT-to-TMP HH clusters are fewer and more temporally variable than replenishment clusters.

**Numerical evidence:** 3,134 HH cell-map records; 664 persistent cells; mean adjacent HH Jaccard = 0.260.

**Interpretation boundary:** Large significant totals in some maps are dominated by LL zero-rich structure and must not be described as extensive hotspots.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

**Source locator:** NAT-to-TMP endpoint area

## P9A016 — RQ4 / local_balance_structure

The bounded C-R index has the strongest adjacent HH stability among the primary local results.

**Numerical evidence:** 19,358 HH cell-map records; 3,543 persistent HH cells; mean adjacent HH Jaccard = 0.620.

**Interpretation boundary:** HH means relatively high index within active support; substantive consolidation dominance still requires index > +1/3.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

**Source locator:** C-R balance index

## P9A017 — RQ4 / multiplicity_sensitivity

Local significance is materially sensitive to the conservative BY correction.

**Numerical evidence:** BY retains 72,221 of 168,860 BH-significant cell-map records = 42.77%.

**Interpretation boundary:** BH remains the prespecified primary rule; highlighted clusters may be labelled BY-robust only when they pass BY.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

**Source locator:** Multiple-testing sensitivity

## P9A018 — RQ4 / biome_process_totals

Consolidation and endpoint NAT-to-TMP are Cerrado-associated over the primary period, while replenishment totals are similar with a slightly larger Amazon contribution.

**Numerical evidence:** Million ha: consolidation Amazon 5.10 vs Cerrado 15.02; replenishment 47.81 vs 45.81; NAT-to-TMP 2.04 vs 7.11.

**Interpretation boundary:** Primary-biome assignment attributes whole cells and is not an exact pixel partition by biome.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

**Source locator:** Process magnitude and changing biome contributions

## P9A019 — RQ4 / biome_trajectory_dynamics

NAT-to-TMP magnitude classes are more dynamic through time in Cerrado than Amazon.

**Numerical evidence:** Mean state changes: Amazon 0.79, Cerrado 2.13; constant trajectories: 68.0% vs 18.0%.

**Interpretation boundary:** State changes are five-year cell classes and do not track annual pixel trajectories.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

**Source locator:** Cell-state trajectories

## P9A020 — RQ4 / biome_hh_contribution

Cerrado contributes more persistent HH cells for consolidation, NAT-to-TMP and C-R balance, whereas Amazon contributes more for replenishment.

**Numerical evidence:** Persistent replenishment HH: Amazon 2,785 vs Cerrado 1,569; persistent NAT-to-TMP HH: 153 vs 511.

**Interpretation boundary:** These are biome contributions to the accepted combined-domain LISA pattern, not newly fitted within-biome Local Moran models.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

**Source locator:** HH occurrence and persistence

## P9A021 — RQ4 / biome_boundary_sensitivity

The principal biome comparisons are stable when all 582 transbiome cells are removed.

**Numerical evidence:** All 160 Global Moran significance decisions retained; maximum absolute I change = 0.044848.

**Interpretation boundary:** Stability does not make primary-biome totals exact within-biome pixel totals.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

**Source locator:** Boundary-cell sensitivity

## P9A022 — RQ5 / aggregate_and_temporal_maup

Aggregate signs, dominance classes and temporal extrema are robust to alternative scale and zoning, while some conditional distributions are sensitive.

**Numerical evidence:** All 192 aggregate and 48 temporal comparisons pass; shifted 20k passes all components; 10k and 40k have distribution/support sensitivities.

**Interpretation boundary:** Robust aggregate behavior does not guarantee invariance of cell-level distributions.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase8c/phase8c_maup_robustness_findings_v1.md`; SHA256 `b152701ea505df61ceb54640b2246650b4b4c00ee22a38d157016dc28f22f886`.

**Source locator:** Main findings and qualifications

## P9A023 — RQ5 / global_moran_maup

The positive direction and formal significance of global spatial clustering are robust across alternative grids.

**Numerical evidence:** 120/120 alternative coefficients positive and BY-significant; 119/120 interval magnitude checks pass.

**Interpretation boundary:** Exact coefficient magnitudes and temporal ranking are separate robustness criteria.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase8d/phase8d_maup_global_moran_findings_v1.md`; SHA256 `fbcf709035c7f40cd5a2de6682a94b05568d12cc3d1f1d64be22c399768c4eb4`.

**Source locator:** Main outcome

## P9A024 — RQ5 / global_moran_temporal_maup

Exact Global Moran magnitudes and temporal ordering show partial MAUP sensitivity concentrated in NAT-to-TMP.

**Numerical evidence:** One interval magnitude failure and 8/30 strict temporal failures; all six aggregate grid-window assessments fail at least one strict criterion.

**Interpretation boundary:** Failure of a strict comparison does not imply absence of positive spatial autocorrelation.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase8d/canonical_maup_global_moran_assessment_v1.csv`; SHA256 `fac984fff7abf20b4cb9c284c8bdc082e775d0d656a369d77617bae6282d8e39`.

**Source locator:** Six grid-window assessment rows

## P9A025 — RQ5 / hh_cluster_maup

HH location and persistence are robust for replenishment, net C-R balance and the bounded C-R index.

**Numerical evidence:** Each metric passes 6/6 grid-window assessments; interval passes are 24/24, 23/24 and 24/24 respectively.

**Interpretation boundary:** Agreement is broad area-weighted footprint agreement, not cell-for-cell identity.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase8e/canonical_maup_hh_robustness_assessment_v1.csv`; SHA256 `cbdfb3825948ab7f7e81535c9d06fb110dec846881096b06c657e328092687b4`.

**Source locator:** Metric-specific assessment rows

## P9A026 — RQ5 / hh_cluster_maup

Consolidation HH recurrence and persistence are recognizable, but interval footprint location is scale-sensitive.

**Numerical evidence:** 3/6 complete assessments pass; 16/24 interval maps pass.

**Interpretation boundary:** Describe as partial robustness rather than either full invariance or invalidity.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase8e/phase8e_maup_hh_cluster_findings_v1.md`; SHA256 `0384f689779e489a85452d1b560e55cee574fe1a591a14384f729b1c1bfc93b7`.

**Source locator:** Consolidation

## P9A027 — RQ5 / hh_cluster_maup

Endpoint NAT-to-TMP HH footprint location and persistence are sensitive to spatial scale and zoning.

**Numerical evidence:** 0/6 complete assessments and 7/24 interval comparisons pass.

**Interpretation boundary:** Many failures retain high overlap coefficients, indicating footprint expansion or contraction around partly shared cores rather than universal relocation.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase8e/phase8e_maup_hh_cluster_findings_v1.md`; SHA256 `0384f689779e489a85452d1b560e55cee574fe1a591a14384f729b1c1bfc93b7`.

**Source locator:** Endpoint NAT-to-TMP

## P9A028 — RQ5 / canonical_support_decision

The canonical approximately 20,000-ha grid remains the primary analytical support after the MAUP assessment.

**Numerical evidence:** Phase 8A-E completed; alternative grids remain sensitivity analyses.

**Interpretation boundary:** Primary status does not erase metric-specific MAUP sensitivity and must be reported with qualifications.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `phase8e/phase8_maup_robustness_synthesis_v1.md`; SHA256 `8cfe0400f61ebf805f166ed100b68f8b290456f986a011aa4fac89ef2ec25c5a`.

**Source locator:** Final Phase 8 decision

## P9A029 — RQ5 / diagnostic_extension

The diagnostic interval reinforces some sensitivity findings but does not create the principal NAT-to-TMP MAUP result.

**Numerical evidence:** NAT-to-TMP is already sensitive in 1985-2020; 2020-2025 additionally affects full-window 40k consolidation.

**Interpretation boundary:** Diagnostic evidence is included and flagged but does not replace primary-period conclusions.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `phase8e/phase8_maup_robustness_synthesis_v1.md`; SHA256 `8cfe0400f61ebf805f166ed100b68f8b290456f986a011aa4fac89ef2ec25c5a`.

**Source locator:** Diagnostic extension

## P9A030 — RQ4 / causal_boundary

The accepted evidence supports spatial and temporal association, concentration and persistence statements, not causal attribution.

**Numerical evidence:** No commodity-price, infrastructure, policy, tenure or causal-design model is included in Phases 1-8.

**Interpretation boundary:** Do not translate descriptive or spatial-inference results into causal drivers.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `planning/006_spatiotemporal_investigation_plan.md`; SHA256 `43f59b644cc47ecc5b8b853909086309db2692bf0a7c27179cfd5b7384109b37`.

**Source locator:** Interpretation boundaries

## P9A031 — RQ1 / fixed_1985_pasture_cohort_endpoint_fate

The fixed 1985 pasture cohort was redistributed among endpoint land-cover states by 2020.

**Numerical evidence:** Initial cohort = 49.036 million ha; 2020 shares: pasture 63.13%, temporary crops 19.94%, native vegetation 6.82%, other agriculture 9.22%.

**Interpretation boundary:** Endpoint state is not continuous pixel persistence and does not identify the date or pathway of an intervening transition.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

**Source locator:** Combined-domain rows for 1985 and 2020

## P9A032 — RQ1 / fixed_cohort_pasture_endpoint_change

The share of fixed-cohort area classified as pasture changes substantially across the primary reference years.

**Numerical evidence:** Pasture endpoint share is 100% in 1985 and reaches its primary minimum of 63.13% in 2020.

**Interpretation boundary:** The series is not a survival curve: pixels may leave and later return to pasture between reference years.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

**Source locator:** Combined-domain primary endpoint series

## P9A033 — RQ1 / fixed_cohort_biome_contrast

The 2020 endpoint composition of the fixed cohort differs between primary-biome assignments.

**Numerical evidence:** Amazon-assigned cohort: pasture 74.82%, temporary crops 12.02%; Cerrado-assigned cohort: pasture 60.94%, temporary crops 21.43%.

**Interpretation boundary:** Whole-cell primary-biome assignment is not pixel-level partitioning; the non-transbiome sensitivity is reported separately.

**Evidence status:** supported; **causal flag:** 0.

**Canonical source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

**Source locator:** Primary-assignment biome rows for 2020

## P9A034 — RQ1 / fixed_cohort_diagnostic_endpoint

The 2025 endpoint extends the fixed-cohort composition descriptively.

**Numerical evidence:** 2025 shares: pasture 58.22%, temporary crops 21.42%, native vegetation 6.43%.

**Interpretation boundary:** The 2025 map is diagnostic and does not replace primary-period conclusions.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

**Source locator:** Combined-domain row for 2025

## P9A035 — RQ2 / observed_pasture_spell_origin_composition_and_window_sensitivity

Origin-share trajectories are window-conditioned, and calendar-paired monotonicity follows set nesting. Matched-follow-up curves, stock retention and stock-normalized endpoint conversion fractions characterize observed contrasts; the estimable primary initial/entry fraction ratio is 1.17-1.40 under b1985, without identifying a process threshold. Full-domain chronology now separates first observed entry, observed re-entry and uncertain prior history within confirmed entry; the conditional re-entry share is descriptive and not monotonic over primary intervals.

**Numerical evidence:** Canonical b1985: first interval 100.00% initial by construction; 2015-2020 initial/entry 31.08%/68.92%; first primary entry share >50% in 2000-2005 (51.24%). At 15 elapsed years to interval start (fourth five-year interval): initial b1985: 48.7592%; b1995: 59.8974%; b2000: 66.3582%. No primary-period entry crossing occurs for b1995 or b2000; their crossings occur only in separately reported diagnostic 2020-2025. Stock-normalized initial/entry endpoint-fraction ratios: b1985 primary estimable range 1.1674-1.3979, diagnostic 0.8072; b1995 primary estimable range 1.0046-1.1964, diagnostic 0.7209; b2000 primary estimable range 0.8164-1.1016, diagnostic 0.6712. Three first-interval ratios undefined; stock denominators measured at t0. Re-entry / confirmed-entry flow: 2.354410% in 1990-1995, 19.117876% in 2015-2020 and 32.488051% in diagnostic 2020-2025. Corresponding last-primary and diagnostic re-entry / entry-stock shares: 15.853277% and 17.906327%. The 1985-1990 conditional entry denominators are zero and fractions undefined.

**Interpretation boundary:** Initial means PAS continuously observed from the chosen boundary to t0, not physical pasture age. The first positive-conversion interval is 100% initial by construction. At fixed calendar time, later baselines expand the initial category without changing endpoint conversions. Equal follow-up also changes calendar time, baseline cohort composition and conversion weights. The completed sensitivity does not identify an artifact fraction, stationarity, a process threshold or regime change. Continuous-cohort membership cannot gain pixels, but its share of selected conversions need not be monotonic. Observed entry includes re-entry and is not first-ever establishment. No trend-significance, causal or source-classification-accuracy claim is made. 1985 is an observation boundary (Decision 022). Origin is assigned at t0 and endpoint flow does not reconstruct the annual path between t0 and t1. A finite-duration renewal process can generate decline, but no renewal/hazard model was fitted. Calendar-paired monotonicity follows set nesting; its direction alone is not evidence of process change. Magnitude describes reclassification, while matched-follow-up curves and stock-versus-conversion contrasts also change periods/cohorts and do not isolate an artifact fraction. Relative conversion fractions use stock at t0, not exposure through the quinquennium; they are aggregate descriptive endpoint fractions, not annual hazards, adjusted preferences or causal effects. National ratios divide summed areas, not mean cell ratios. First-interval initial/entry ratios are undefined because entry stock is zero. Primary ratios fluctuate for b1985 and b1995; the three estimable b2000 primary ratios increase. All three diagnostic ratios are below one. No pooled exposure-normalized ratio is claimed. First observed entry requires no earlier observed PAS and complete valid pre-entry coverage since 1985; it is not first-ever establishment. Re-entry requires any earlier observed PAS, and the label is frozen at entry. Prior-history uncertainty after a confirmed nonPAS reset differs from unresolved current-spell origin. Earlier PAS can identify re-entry despite intervening gaps; gaps alone never establish an exit or a new confirmed entry. Longer observable history and changing stock/cohort composition can change subclass shares; no inferential trend, renewal model, physical land-use-cycle identification or causal claim follows. Classification instability can contribute to observed recurrence. The auxiliary age-201 checks concern coverage-derived code, not complete numeric validation of the public pasture-age v2 asset.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv`; SHA256 `8b24c1c3475f1f19bca6abc09c425df43400f573e04d41df7afd0473b088c897`.

**Source locator:** Canonical seven primary interval rows; sensitivity interval/elapsed and separate crossing-review rows. Canonical anchor and all supplemental sources: config/rq2_evidence_v4_3_source_inventory_v1.csv#P9A035 Entry/re-entry supplementary sources and derivatives: config/rq2_evidence_v4_4_source_inventory_v1.csv#P9A035

## P9A036 — RQ2 / pooled_observed_pasture_spell_origins_and_window_sensitivity

The canonical 46.91% initial / 53.09% observed-entry split measures origin composition, not relative conversion propensity. Composition combines class stock and class endpoint fractions; calendar-paired initial-share growth is imposed by nesting. The b1985 primary initial/entry fraction ratio is 1.17-1.40, and matched-follow-up contrasts remain descriptive. The accepted confirmed-entry component is now subdivided: first observed entry accounts for 84.58% and observed re-entry for 15.42% of summed primary entry flow, with prior-history uncertainty retained separately.

**Numerical evidence:** Canonical primary sum 20.119468 million ha: initial 46.91% (9.438022 million ha), observed entry 53.09% (10.681383 million ha), unresolved 62.568807 ha (0.000311%). Common-calendar 2000-2020 sum 15.221177 million ha: b1985: 38.1006% initial / 61.8991% observed entry; b1995: 64.6950% initial / 35.3047% observed entry; b2000: 78.0709% initial / 21.9290% observed entry. First-20-year initial shares: b1985: 63.6392%; b1995: 72.2535%; b2000: 78.0709%; these use different calendar periods and denominators. Stock-normalized initial/entry endpoint-fraction ratios: b1985 primary estimable range 1.1674-1.3979, diagnostic 0.8072; b1995 primary estimable range 1.0046-1.1964, diagnostic 0.7209; b2000 primary estimable range 0.8164-1.1016, diagnostic 0.6712. Three first-interval ratios undefined; stock denominators measured at t0. Within primary entry flow (10681383.426750 ha), first observed = 9034641.627062 ha (84.583066%); re-entry = 1646644.847524 ha (15.416026%); prior-history uncertain = 96.952164 ha (0.000907674%). Relative to all primary PAS-to-TMP flow, first observed and re-entry are 44.904973% and 8.184336%.

**Interpretation boundary:** Initial means PAS continuously observed from the chosen boundary to t0, not physical pasture age. The first positive-conversion interval is 100% initial by construction. At fixed calendar time, later baselines expand the initial category without changing endpoint conversions. Equal follow-up also changes calendar time, baseline cohort composition and conversion weights. The completed sensitivity does not identify an artifact fraction, stationarity, a process threshold or regime change. Continuous-cohort membership cannot gain pixels, but its share of selected conversions need not be monotonic. Observed entry includes re-entry and is not first-ever establishment. No trend-significance, causal or source-classification-accuracy claim is made. Pooled areas sum interval conversions and do not deduplicate pixels across intervals. Canonical 1985-2020 pooling and common-calendar 2000-2020 pooling are different comparisons. Initial-spell membership is not fixed RQ1-cohort membership after interruptions. No inferential majority test is claimed. Calendar-paired monotonicity follows set nesting; its direction alone is not evidence of process change. Magnitude describes reclassification, while matched-follow-up curves and stock-versus-conversion contrasts also change periods/cohorts and do not isolate an artifact fraction. Relative conversion fractions use stock at t0, not exposure through the quinquennium; they are aggregate descriptive endpoint fractions, not annual hazards, adjusted preferences or causal effects. National ratios divide summed areas, not mean cell ratios. First-interval initial/entry ratios are undefined because entry stock is zero. Primary ratios fluctuate for b1985 and b1995; the three estimable b2000 primary ratios increase. All three diagnostic ratios are below one. No pooled exposure-normalized ratio is claimed. First observed entry requires no earlier observed PAS and complete valid pre-entry coverage since 1985; it is not first-ever establishment. Re-entry requires any earlier observed PAS, and the label is frozen at entry. Prior-history uncertainty after a confirmed nonPAS reset differs from unresolved current-spell origin. Earlier PAS can identify re-entry despite intervening gaps; gaps alone never establish an exit or a new confirmed entry. Longer observable history and changing stock/cohort composition can change subclass shares; no inferential trend, renewal model, physical land-use-cycle identification or causal claim follows. Classification instability can contribute to observed recurrence. The auxiliary age-201 checks concern coverage-derived code, not complete numeric validation of the public pasture-age v2 asset.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv`; SHA256 `7771a36808a95832f5b2e21f00d81cbe303da7d5c5c91c3e808e2345ce5e64d3`.

**Source locator:** Canonical window=primary_1985_2020; sensitivity common_calendar_primary_2000_2020 and equal_followup_first_20_years. Canonical anchor and all supplemental sources: config/rq2_evidence_v4_3_source_inventory_v1.csv#P9A036 Entry/re-entry supplementary sources and derivatives: config/rq2_evidence_v4_4_source_inventory_v1.csv#P9A036

## P9A037 — RQ2 / unresolved_observed_pasture_spell_origin

The corrected three-way origin partition retains a small unresolved observed-spell component, with the 2020-2025 extension reported separately as diagnostic.

**Numerical evidence:** Unresolved interval-conversion sum: primary 62.568807 ha (0.000311%); full observed 71.614822 ha (0.000323%). Diagnostic 2020-2025 post-1985-entry share = 79.88%; full-observed initial/post-1985-entry shares = 44.39%/55.61%.

**Interpretation boundary:** Unresolved means annual coverage gaps prevent current-spell origin attribution; it is not a numerical decoding of raw source age code 1. The retired source-age unattributed category is not part of the corrected three-state estimand. A small unresolved origin component does not measure total classification error. 2020-2025 is diagnostic with limited boundary support.

**Evidence status:** qualified; **causal flag:** 0.

**Canonical source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv`; SHA256 `7771a36808a95832f5b2e21f00d81cbe303da7d5c5c91c3e808e2345ce5e64d3`.

**Source locator:** Both pooled windows; diagnostic interval share from canonical_pas_tmp_origin_interval_summary_v2.csv


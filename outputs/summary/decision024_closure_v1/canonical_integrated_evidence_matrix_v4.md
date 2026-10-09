# Integrated evidence matrix v4 — Decision 024 corrected origins

**Review date:** 2026-10-08. **Rows:** 35. **Authority:** criterion-12 closure record and versioned status events v2.

This edition replaces only P9A035–P9A037 with corrected observed-spell evidence. The other 32 statements retain their prior field values, apart from the edition identifier. Historical v3 statements and source-based figures remain provenance and must not be cited as current origin results.

## P9A003 — RQ3 / within_interval_pathways

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Detected intermediate pasture represents a small share of accumulated endpoint NAT-to-TMP area in the primary high-magnitude cohort.

Pasture detected in at least one intermediate year = 6.51% of accumulated NAT-to-TMP area in the cohort.

**Interpretation:** This percentage is cohort-specific and sums interval areas; it is not the full-domain share and does not deduplicate pixels across intervals.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A004 — RQ3 / within_interval_pathways

**Status:** qualified. **Temporal role:** primary. **Window:** 1985_2020.

Absence of detected pasture in the annual series does not establish direct native-vegetation-to-crop conversion.

Other intermediate states and classification instability remain possible.

**Interpretation:** Use 'no pasture detected' rather than 'direct conversion' unless every intermediate state is evaluated.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A005 — RQ4 / aggregate_process_balance

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

Replenishment exceeds consolidation in aggregate in every five-year interval.

Aggregate C-R index is negative in all eight intervals, from -0.838 in 1985-1990 to -0.656 in diagnostic 2020-2025.

**Interpretation:** Aggregate dominance does not imply that every cell is replenishment-dominant.

**Source:** `phase2/canonical_spatial_metrics_summary_v1.csv`; SHA-256 `4d9a4ee8d9fefa5e281be3a765e20509756c7bb29f86046aaf6d87a1b9314bdf`.

## P9A006 — RQ4 / nat_tmp_concentration

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

A small fixed group of high-magnitude cells contains most accumulated endpoint NAT-to-TMP area.

2,598 cells = 10.44% of the domain and 87.5% of accumulated 1985-2020 NAT-to-TMP area.

**Interpretation:** The cohort is selected retrospectively and is not random or itself a statistical cluster.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A007 — RQ4 / nat_tmp_temporal_concentration

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

High-cohort NAT-to-TMP activity peaks in 2000-2005 and declines strongly by 2015-2020.

2.116 million ha in 2000-2005 versus 0.546 million ha in 2015-2020; decline = 74.2%.

**Interpretation:** Decline in high-class area does not mean disappearance of all NAT-to-TMP activity.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A008 — RQ4 / nat_tmp_spatial_redistribution

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

The activity-weighted center of the high cohort shifts north/northeast over the primary period.

Approximate net displacement = 692 km between 1985-1990 and 2015-2020.

**Interpretation:** This is redistribution of activity weights among fixed cells, not tracking of identical pixels or a causal frontier trajectory.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A009 — RQ4 / regional_cr_balance

**Status:** supported. **Temporal role:** primary. **Window:** 2010_2020.

Recent high-cohort balance differs between biomes: Amazon is consolidation-dominant while Cerrado remains mixed.

2010-2015: Amazon +0.621, Cerrado +0.095; 2015-2020: Amazon +0.415, Cerrado -0.037.

**Interpretation:** These are ratios of regional flow sums, not means of cell indices or classifications of all cells.

**Source:** `phase4/phase4_spatial_findings_and_closure_v1.md`; SHA-256 `1be8540936dfdbcf25894b00a9d7c92058b3bbf23a56501c6d81eac0977f8631`.

## P9A010 — RQ4 / late_consolidation_persistence

**Status:** supported. **Temporal role:** primary. **Window:** 2010_2020.

Recent consolidation dominance is more persistent among high-cohort Amazon cells than Cerrado cells.

Dominant in both late intervals: Amazon 367/648 = 56.6%; Cerrado 427/1,950 = 21.9%.

**Interpretation:** Persistence is defined at five-year cell state, not annual or pixel-level continuity.

**Source:** `phase4/phase4_temporal_synthesis_v1.md`; SHA-256 `671f34296136545c54fcb1b8090352ceb5b0964d60b1cb818d19a007f6aedf23`.

## P9A011 — RQ4 / cr_balance_reversals

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Persistent late consolidation and earlier reversals coexist; there is no universal linear replenishment-to-consolidation succession.

Any direct or mediated reversal: Amazon 83.0%; Cerrado 57.2%.

**Interpretation:** Repeated transitions from the same cell are descriptive and are not independent probabilities from a fitted model.

**Source:** `phase4/phase4_temporal_synthesis_v1.md`; SHA-256 `671f34296136545c54fcb1b8090352ceb5b0964d60b1cb818d19a007f6aedf23`.

## P9A012 — RQ4 / global_spatial_autocorrelation

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

All canonical Global Moran tests show positive spatial association and remain significant after BY correction.

104/104 tests positive and BY-significant; 9,999 permutations per test.

**Interpretation:** Global Moran establishes overall association but does not locate clusters or imply causal processes.

**Source:** `phase5/global_moran_findings_phase5_v1.md`; SHA-256 `6ab0fa6790ea802a5816f8e52aea45862a276a26ab1172f58363280183f1e554`.

## P9A013 — RQ4 / global_temporal_change

**Status:** qualified. **Temporal role:** primary. **Window:** 1985_2020.

Several absolute process metrics have lower Global Moran coefficients late in the primary period than initially.

Consolidation 0.799 to 0.559; replenishment 0.770 to 0.614; NAT-to-TMP 0.550 to 0.361.

**Interpretation:** Separate interval permutation tests do not test the significance of between-date differences or a temporal trend.

**Source:** `phase5/global_moran_findings_phase5_v1.md`; SHA-256 `6ab0fa6790ea802a5816f8e52aea45862a276a26ab1172f58363280183f1e554`.

## P9A014 — RQ4 / local_hotspots

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Replenishment has the broadest and most persistent absolute-process HH structure.

18,067 HH cell-map records; 4,354 cells with primary HH persistence; mean adjacent HH Jaccard = 0.389.

**Interpretation:** HH denotes locally high values relative to the map and significant neighbors; it is not a causal region.

**Source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA-256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

## P9A015 — RQ4 / local_hotspots

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Endpoint NAT-to-TMP HH clusters are fewer and more temporally variable than replenishment clusters.

3,134 HH cell-map records; 664 persistent cells; mean adjacent HH Jaccard = 0.260.

**Interpretation:** Large significant totals in some maps are dominated by LL zero-rich structure and must not be described as extensive hotspots.

**Source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA-256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

## P9A016 — RQ4 / local_balance_structure

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

The bounded C-R index has the strongest adjacent HH stability among the primary local results.

19,358 HH cell-map records; 3,543 persistent HH cells; mean adjacent HH Jaccard = 0.620.

**Interpretation:** HH means relatively high index within active support; substantive consolidation dominance still requires index > +1/3.

**Source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA-256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

## P9A017 — RQ4 / multiplicity_sensitivity

**Status:** qualified. **Temporal role:** both. **Window:** 1985_2025.

Local significance is materially sensitive to the conservative BY correction.

BY retains 72,221 of 168,860 BH-significant cell-map records = 42.77%.

**Interpretation:** BH remains the prespecified primary rule; highlighted clusters may be labelled BY-robust only when they pass BY.

**Source:** `phase6/local_moran_lisa_findings_phase6_v1.md`; SHA-256 `18844dba41319df03e47828a0f84a4da040575f35e53c5a26f31d64f565dbb9c`.

## P9A018 — RQ4 / biome_process_totals

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Consolidation and endpoint NAT-to-TMP are Cerrado-associated over the primary period, while replenishment totals are similar with a slightly larger Amazon contribution.

Million ha: consolidation Amazon 5.10 vs Cerrado 15.02; replenishment 47.81 vs 45.81; NAT-to-TMP 2.04 vs 7.11.

**Interpretation:** Primary-biome assignment attributes whole cells and is not an exact pixel partition by biome.

**Source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA-256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

## P9A019 — RQ4 / biome_trajectory_dynamics

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

NAT-to-TMP magnitude classes are more dynamic through time in Cerrado than Amazon.

Mean state changes: Amazon 0.79, Cerrado 2.13; constant trajectories: 68.0% vs 18.0%.

**Interpretation:** State changes are five-year cell classes and do not track annual pixel trajectories.

**Source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA-256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

## P9A020 — RQ4 / biome_hh_contribution

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Cerrado contributes more persistent HH cells for consolidation, NAT-to-TMP and C-R balance, whereas Amazon contributes more for replenishment.

Persistent replenishment HH: Amazon 2,785 vs Cerrado 1,569; persistent NAT-to-TMP HH: 153 vs 511.

**Interpretation:** These are biome contributions to the accepted combined-domain LISA pattern, not newly fitted within-biome Local Moran models.

**Source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA-256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

## P9A021 — RQ4 / biome_boundary_sensitivity

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

The principal biome comparisons are stable when all 582 transbiome cells are removed.

All 160 Global Moran significance decisions retained; maximum absolute I change = 0.044848.

**Interpretation:** Stability does not make primary-biome totals exact within-biome pixel totals.

**Source:** `phase7/phase7_biome_comparison_findings_v1.md`; SHA-256 `7dbc6c0f7d7744fd37c524a3383066af806b4403cbb3a375cbcbee88536b34f1`.

## P9A022 — RQ5 / aggregate_and_temporal_maup

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

Aggregate signs, dominance classes and temporal extrema are robust to alternative scale and zoning, while some conditional distributions are sensitive.

All 192 aggregate and 48 temporal comparisons pass; shifted 20k passes all components; 10k and 40k have distribution/support sensitivities.

**Interpretation:** Robust aggregate behavior does not guarantee invariance of cell-level distributions.

**Source:** `phase8c/phase8c_maup_robustness_findings_v1.md`; SHA-256 `b152701ea505df61ceb54640b2246650b4b4c00ee22a38d157016dc28f22f886`.

## P9A023 — RQ5 / global_moran_maup

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

The positive direction and formal significance of global spatial clustering are robust across alternative grids.

120/120 alternative coefficients positive and BY-significant; 119/120 interval magnitude checks pass.

**Interpretation:** Exact coefficient magnitudes and temporal ranking are separate robustness criteria.

**Source:** `phase8d/phase8d_maup_global_moran_findings_v1.md`; SHA-256 `fbcf709035c7f40cd5a2de6682a94b05568d12cc3d1f1d64be22c399768c4eb4`.

## P9A024 — RQ5 / global_moran_temporal_maup

**Status:** qualified. **Temporal role:** both. **Window:** 1985_2025.

Exact Global Moran magnitudes and temporal ordering show partial MAUP sensitivity concentrated in NAT-to-TMP.

One interval magnitude failure and 8/30 strict temporal failures; all six aggregate grid-window assessments fail at least one strict criterion.

**Interpretation:** Failure of a strict comparison does not imply absence of positive spatial autocorrelation.

**Source:** `phase8d/canonical_maup_global_moran_assessment_v1.csv`; SHA-256 `fac984fff7abf20b4cb9c284c8bdc082e775d0d656a369d77617bae6282d8e39`.

## P9A025 — RQ5 / hh_cluster_maup

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

HH location and persistence are robust for replenishment, net C-R balance and the bounded C-R index.

Each metric passes 6/6 grid-window assessments; interval passes are 24/24, 23/24 and 24/24 respectively.

**Interpretation:** Agreement is broad area-weighted footprint agreement, not cell-for-cell identity.

**Source:** `phase8e/canonical_maup_hh_robustness_assessment_v1.csv`; SHA-256 `cbdfb3825948ab7f7e81535c9d06fb110dec846881096b06c657e328092687b4`.

## P9A026 — RQ5 / hh_cluster_maup

**Status:** qualified. **Temporal role:** both. **Window:** 1985_2025.

Consolidation HH recurrence and persistence are recognizable, but interval footprint location is scale-sensitive.

3/6 complete assessments pass; 16/24 interval maps pass.

**Interpretation:** Describe as partial robustness rather than either full invariance or invalidity.

**Source:** `phase8e/phase8e_maup_hh_cluster_findings_v1.md`; SHA-256 `0384f689779e489a85452d1b560e55cee574fe1a591a14384f729b1c1bfc93b7`.

## P9A027 — RQ5 / hh_cluster_maup

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

Endpoint NAT-to-TMP HH footprint location and persistence are sensitive to spatial scale and zoning.

0/6 complete assessments and 7/24 interval comparisons pass.

**Interpretation:** Many failures retain high overlap coefficients, indicating footprint expansion or contraction around partly shared cores rather than universal relocation.

**Source:** `phase8e/phase8e_maup_hh_cluster_findings_v1.md`; SHA-256 `0384f689779e489a85452d1b560e55cee574fe1a591a14384f729b1c1bfc93b7`.

## P9A028 — RQ5 / canonical_support_decision

**Status:** supported. **Temporal role:** both. **Window:** 1985_2025.

The canonical approximately 20,000-ha grid remains the primary analytical support after the MAUP assessment.

Phase 8A-E completed; alternative grids remain sensitivity analyses.

**Interpretation:** Primary status does not erase metric-specific MAUP sensitivity and must be reported with qualifications.

**Source:** `phase8e/phase8_maup_robustness_synthesis_v1.md`; SHA-256 `8cfe0400f61ebf805f166ed100b68f8b290456f986a011aa4fac89ef2ec25c5a`.

## P9A029 — RQ5 / diagnostic_extension

**Status:** qualified. **Temporal role:** diagnostic. **Window:** 2020_2025.

The diagnostic interval reinforces some sensitivity findings but does not create the principal NAT-to-TMP MAUP result.

NAT-to-TMP is already sensitive in 1985-2020; 2020-2025 additionally affects full-window 40k consolidation.

**Interpretation:** Diagnostic evidence is included and flagged but does not replace primary-period conclusions.

**Source:** `phase8e/phase8_maup_robustness_synthesis_v1.md`; SHA-256 `8cfe0400f61ebf805f166ed100b68f8b290456f986a011aa4fac89ef2ec25c5a`.

## P9A030 — RQ4 / causal_boundary

**Status:** qualified. **Temporal role:** both. **Window:** 1985_2025.

The accepted evidence supports spatial and temporal association, concentration and persistence statements, not causal attribution.

No commodity-price, infrastructure, policy, tenure or causal-design model is included in Phases 1-8.

**Interpretation:** Do not translate descriptive or spatial-inference results into causal drivers.

**Source:** `planning/006_spatiotemporal_investigation_plan.md`; SHA-256 `43f59b644cc47ecc5b8b853909086309db2692bf0a7c27179cfd5b7384109b37`.

## P9A031 — RQ1 / fixed_1985_pasture_cohort_endpoint_fate

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

The fixed 1985 pasture cohort was redistributed among endpoint land-cover states by 2020.

Initial cohort = 49.036 million ha; 2020 shares: pasture 63.13%, temporary crops 19.94%, native vegetation 6.82%, other agriculture 9.22%.

**Interpretation:** Endpoint state is not continuous pixel persistence and does not identify the date or pathway of an intervening transition.

**Source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA-256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

## P9A032 — RQ1 / fixed_cohort_pasture_endpoint_change

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

The share of fixed-cohort area classified as pasture changes substantially across the primary reference years.

Pasture endpoint share is 100% in 1985 and reaches its primary minimum of 63.13% in 2020.

**Interpretation:** The series is not a survival curve: pixels may leave and later return to pasture between reference years.

**Source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA-256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

## P9A033 — RQ1 / fixed_cohort_biome_contrast

**Status:** supported. **Temporal role:** primary. **Window:** 2020.

The 2020 endpoint composition of the fixed cohort differs between primary-biome assignments.

Amazon-assigned cohort: pasture 74.82%, temporary crops 12.02%; Cerrado-assigned cohort: pasture 60.94%, temporary crops 21.43%.

**Interpretation:** Whole-cell primary-biome assignment is not pixel-level partitioning; the non-transbiome sensitivity is reported separately.

**Source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA-256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

## P9A034 — RQ1 / fixed_cohort_diagnostic_endpoint

**Status:** qualified. **Temporal role:** diagnostic. **Window:** 2020_2025.

The 2025 endpoint extends the fixed-cohort composition descriptively.

2025 shares: pasture 58.22%, temporary crops 21.42%, native vegetation 6.43%.

**Interpretation:** The 2025 map is diagnostic and does not replace primary-period conclusions.

**Source:** `canonical_fixed_1985_pasture_cohort_summary_v1.csv`; SHA-256 `f2e69d49999ec12e172a42365b3ffa4ff29d4afbd8c743057e92cde69b04fb85`.

## P9A035 — RQ2 / observed_pasture_spell_origin_shift_in_consolidation

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

The share of PAS-to-temporary-crop endpoint conversion attributed to an uninterrupted left-censored 1985 pasture spell decreases across the seven primary intervals, while observed post-1985 entry spells increase.

Initial/post-1985-entry shares: 1985-1990 100.00%/0.00%; 2015-2020 31.08%/68.92%. Post-1985-entry share first exceeds 50% in 2000-2005 (51.24%).

**Interpretation:** Origin is reconstructed from annual coverage at t0. A post-1985 observed entry includes re-entry; it is not first-ever establishment. The shift is descriptive, with no trend-significance or causal claim. Endpoint flow does not determine the annual path between t0 and t1.

**Source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_interval_summary_v2.csv`; SHA-256 `8b24c1c3475f1f19bca6abc09c425df43400f573e04d41df7afd0473b088c897`.

## P9A036 — RQ2 / pooled_primary_observed_pasture_spell_origins

**Status:** supported. **Temporal role:** primary. **Window:** 1985_2020.

Across 1985-2020, observed post-1985 entry spells contribute a modest majority of pooled PAS-to-temporary-crop endpoint conversion area; uninterrupted left-censored 1985 spells remain substantial.

Primary interval-conversion sum = 20.119468 million ha; initial 46.91% (9.438022 million ha), post-1985 entry 53.09% (10.681383 million ha), unresolved 62.568807 ha (0.000311%).

**Interpretation:** Pooled values sum interval conversion areas and do not deduplicate pixels converted in different intervals. Initial origin is a continuous observed 1985 spell at t0, not membership in the fixed RQ1 cohort after interruptions. No causal attribution or inferential majority test is claimed.

**Source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv`; SHA-256 `7771a36808a95832f5b2e21f00d81cbe303da7d5c5c91c3e808e2345ce5e64d3`.

## P9A037 — RQ2 / unresolved_observed_pasture_spell_origin

**Status:** qualified. **Temporal role:** both. **Window:** 1985_2025.

The corrected three-way origin partition retains a small unresolved observed-spell component, with the 2020-2025 extension reported separately as diagnostic.

Unresolved interval-conversion sum: primary 62.568807 ha (0.000311%); full observed 71.614822 ha (0.000323%). Diagnostic 2020-2025 post-1985-entry share = 79.88%; full-observed initial/post-1985-entry shares = 44.39%/55.61%.

**Interpretation:** Unresolved means annual coverage gaps prevent current-spell origin attribution; it is not a numerical decoding of raw source age code 1. The retired source-age unattributed category is not part of the corrected three-state estimand. A small unresolved origin component does not measure total classification error. 2020-2025 is diagnostic with limited boundary support.

**Source:** `outputs/summary/pasture_spell_panel_v2/canonical_pas_tmp_origin_pooled_summary_v2.csv`; SHA-256 `7771a36808a95832f5b2e21f00d81cbe303da7d5c5c91c3e808e2345ce5e64d3`.

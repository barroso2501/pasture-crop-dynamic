# Canonical integrated evidence matrix — gap-resolved version 2

RQ1 and RQ2 are resolved by authenticated Phase 9A.1 extractions.
The original version 1 matrix remains unchanged for provenance.

## Coverage

| Research question | Rows | Supported | Qualified | Gaps |
|---|---:|---:|---:|---:|
| RQ1 | 4 | 3 | 1 | 0 |
| RQ2 | 3 | 2 | 1 | 0 |
| RQ3 | 2 | 1 | 1 | 0 |
| RQ4 | 18 | 15 | 3 | 0 |
| RQ5 | 8 | 5 | 3 | 0 |

## RQ1

### P9A031 — fixed_1985_pasture_cohort_endpoint_fate

The fixed 1985 pasture cohort was redistributed among endpoint land-cover states by 2020.

- **Evidence:** Initial cohort = 49.036 million ha; 2020 shares: pasture 63.13%, temporary agriculture 19.94%, native vegetation 6.82%, other agriculture 9.22%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Endpoint state is not continuous pixel persistence and does not identify the date or pathway of an intervening transition.
- **Source:** Phase 9A.1, `canonical_fixed_1985_pasture_cohort_summary_v1.csv` — Combined-domain rows for 1985 and 2020

### P9A032 — fixed_cohort_pasture_endpoint_change

The share of fixed-cohort area classified as pasture changes substantially across the primary reference years.

- **Evidence:** Pasture endpoint share is 100% in 1985 and reaches its primary minimum of 63.13% in 2020.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** The series is not a survival curve: pixels may leave and later return to pasture between reference years.
- **Source:** Phase 9A.1, `canonical_fixed_1985_pasture_cohort_summary_v1.csv` — Combined-domain primary endpoint series

### P9A033 — fixed_cohort_biome_contrast

The 2020 endpoint composition of the fixed cohort differs between primary-biome assignments.

- **Evidence:** Amazon-assigned cohort: pasture 74.82%, temporary agriculture 12.02%; Cerrado-assigned cohort: pasture 60.94%, temporary agriculture 21.43%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (2020)
- **Robustness:** not_assessed
- **Boundary:** Whole-cell primary-biome assignment is not pixel-level partitioning; the non-transbiome sensitivity is reported separately.
- **Source:** Phase 9A.1, `canonical_fixed_1985_pasture_cohort_summary_v1.csv` — Primary-assignment biome rows for 2020

### P9A034 — fixed_cohort_diagnostic_endpoint

The 2025 endpoint extends the fixed-cohort composition descriptively.

- **Evidence:** 2025 shares: pasture 58.22%, temporary agriculture 21.42%, native vegetation 6.43%.
- **Mode/status:** descriptive / qualified
- **Temporal role:** diagnostic (2020_2025)
- **Robustness:** not_assessed
- **Boundary:** The 2025 map is diagnostic and does not replace primary-period conclusions.
- **Source:** Phase 9A.1, `canonical_fixed_1985_pasture_cohort_summary_v1.csv` — Combined-domain row for 2025


## RQ2

### P9A035 — pasture_origin_shift_in_consolidation

The origin of pasture converted to temporary agriculture shifts from the left-censored 1985 stock toward pasture established during the observed series.

- **Evidence:** Censored/new shares: 1985-1990 100.00%/0.00%; 2015-2020 37.29%/62.71%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Origin is defined by pasture-age code at interval start; it is not the complete historical trajectory of the pixel.
- **Source:** Phase 9A.1, `canonical_pas_tmp_origin_interval_summary_v1.csv` — Primary interval series

### P9A036 — pooled_primary_pasture_origins

Across the primary period, consolidation draws from both the fixed 1985 pasture stock and pasture established during the series.

- **Evidence:** Primary consolidation = 20.119 million ha; censored 51.73%, new 48.27%, unresolved age 0.00%, unattributed 0.00%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Pooled areas sum interval conversions and do not deduplicate pixels converted in different intervals.
- **Source:** Phase 9A.1, `canonical_pas_tmp_origin_pooled_summary_v1.csv` — Primary pooled row

### P9A037 — pasture_age_ambiguity_components

The unresolved pasture-age component is retained explicitly and the unattributed component is zero in the accepted series.

- **Evidence:** Full observed unresolved area = 176.720 ha (0.00%); unattributed area = 0.000 ha. Diagnostic 2020-2025 new-pasture share = 69.75%.
- **Mode/status:** descriptive / qualified
- **Temporal role:** both (1985_2025)
- **Robustness:** not_assessed
- **Boundary:** Pasture-age code 1 remains unresolved and is not decoded as a numerical age.
- **Source:** Phase 9A.1, `canonical_pas_tmp_origin_pooled_summary_v1.csv` — Full pooled and diagnostic rows


## RQ3

### P9A003 — within_interval_pathways

Detected intermediate pasture represents a small share of accumulated endpoint NAT-to-TMP area in the primary high-magnitude cohort.

- **Evidence:** Pasture detected in at least one intermediate year = 6.51% of accumulated NAT-to-TMP area in the cohort.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** This percentage is cohort-specific and sums interval areas; it is not the full-domain share and does not deduplicate pixels across intervals.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Section 7 — Composition of trajectories

### P9A004 — within_interval_pathways

Absence of detected pasture in the annual series does not establish direct native-vegetation-to-crop conversion.

- **Evidence:** Other intermediate states and classification instability remain possible.
- **Mode/status:** descriptive / qualified
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_applicable
- **Boundary:** Use 'no pasture detected' rather than 'direct conversion' unless every intermediate state is evaluated.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Sections 1 and 7


## RQ4

### P9A005 — aggregate_process_balance

Replenishment exceeds consolidation in aggregate in every five-year interval.

- **Evidence:** Aggregate C-R index is negative in all eight intervals, from -0.838 in 1985-1990 to -0.656 in diagnostic 2020-2025.
- **Mode/status:** descriptive / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** not_assessed
- **Boundary:** Aggregate dominance does not imply that every cell is replenishment-dominant.
- **Source:** Phase 2, `phase2/canonical_spatial_metrics_summary_v1.csv` — Eight interval rows; aggregate_cr_balance_index

### P9A006 — nat_tmp_concentration

A small fixed group of high-magnitude cells contains most accumulated endpoint NAT-to-TMP area.

- **Evidence:** 2,598 cells = 10.44% of the domain and 87.5% of accumulated 1985-2020 NAT-to-TMP area.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** The cohort is selected retrospectively and is not random or itself a statistical cluster.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Section 2

### P9A007 — nat_tmp_temporal_concentration

High-cohort NAT-to-TMP activity peaks in 2000-2005 and declines strongly by 2015-2020.

- **Evidence:** 2.116 million ha in 2000-2005 versus 0.546 million ha in 2015-2020; decline = 74.2%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Decline in high-class area does not mean disappearance of all NAT-to-TMP activity.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Section 2

### P9A008 — nat_tmp_spatial_redistribution

The activity-weighted center of the high cohort shifts north/northeast over the primary period.

- **Evidence:** Approximate net displacement = 692 km between 1985-1990 and 2015-2020.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** This is redistribution of activity weights among fixed cells, not tracking of identical pixels or a causal frontier trajectory.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Section 3

### P9A009 — regional_cr_balance

Recent high-cohort balance differs between biomes: Amazon is consolidation-dominant while Cerrado remains mixed.

- **Evidence:** 2010-2015: Amazon +0.621, Cerrado +0.095; 2015-2020: Amazon +0.415, Cerrado -0.037.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (2010_2020)
- **Robustness:** not_assessed
- **Boundary:** These are ratios of regional flow sums, not means of cell indices or classifications of all cells.
- **Source:** Phase 4, `phase4/phase4_spatial_findings_and_closure_v1.md` — Section 4

### P9A010 — late_consolidation_persistence

Recent consolidation dominance is more persistent among high-cohort Amazon cells than Cerrado cells.

- **Evidence:** Dominant in both late intervals: Amazon 367/648 = 56.6%; Cerrado 427/1,950 = 21.9%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (2010_2020)
- **Robustness:** not_assessed
- **Boundary:** Persistence is defined at five-year cell state, not annual or pixel-level continuity.
- **Source:** Phase 4, `phase4/phase4_temporal_synthesis_v1.md` — Late-primary persistence

### P9A011 — cr_balance_reversals

Persistent late consolidation and earlier reversals coexist; there is no universal linear replenishment-to-consolidation succession.

- **Evidence:** Any direct or mediated reversal: Amazon 83.0%; Cerrado 57.2%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Repeated transitions from the same cell are descriptive and are not independent probabilities from a fitted model.
- **Source:** Phase 4, `phase4/phase4_temporal_synthesis_v1.md` — Reversals and recurrence

### P9A012 — global_spatial_autocorrelation

All canonical Global Moran tests show positive spatial association and remain significant after BY correction.

- **Evidence:** 104/104 tests positive and BY-significant; 9,999 permutations per test.
- **Mode/status:** global_inference / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** not_assessed
- **Boundary:** Global Moran establishes overall association but does not locate clusters or imply causal processes.
- **Source:** Phase 5, `phase5/global_moran_findings_phase5_v1.md` — Achado principal

### P9A013 — global_temporal_change

Several absolute process metrics have lower Global Moran coefficients late in the primary period than initially.

- **Evidence:** Consolidation 0.799 to 0.559; replenishment 0.770 to 0.614; NAT-to-TMP 0.550 to 0.361.
- **Mode/status:** global_inference / qualified
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Separate interval permutation tests do not test the significance of between-date differences or a temporal trend.
- **Source:** Phase 5, `phase5/global_moran_findings_phase5_v1.md` — Magnitudes in the full domain

### P9A014 — local_hotspots

Replenishment has the broadest and most persistent absolute-process HH structure.

- **Evidence:** 18,067 HH cell-map records; 4,354 cells with primary HH persistence; mean adjacent HH Jaccard = 0.389.
- **Mode/status:** local_inference / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** HH denotes locally high values relative to the map and significant neighbors; it is not a causal region.
- **Source:** Phase 6, `phase6/local_moran_lisa_findings_phase6_v1.md` — Replenishment

### P9A015 — local_hotspots

Endpoint NAT-to-TMP HH clusters are fewer and more temporally variable than replenishment clusters.

- **Evidence:** 3,134 HH cell-map records; 664 persistent cells; mean adjacent HH Jaccard = 0.260.
- **Mode/status:** local_inference / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** Large significant totals in some maps are dominated by LL zero-rich structure and must not be described as extensive hotspots.
- **Source:** Phase 6, `phase6/local_moran_lisa_findings_phase6_v1.md` — NAT-to-TMP endpoint area

### P9A016 — local_balance_structure

The bounded C-R index has the strongest adjacent HH stability among the primary local results.

- **Evidence:** 19,358 HH cell-map records; 3,543 persistent HH cells; mean adjacent HH Jaccard = 0.620.
- **Mode/status:** local_inference / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** not_assessed
- **Boundary:** HH means relatively high index within active support; substantive consolidation dominance still requires index > +1/3.
- **Source:** Phase 6, `phase6/local_moran_lisa_findings_phase6_v1.md` — C-R balance index

### P9A017 — multiplicity_sensitivity

Local significance is materially sensitive to the conservative BY correction.

- **Evidence:** BY retains 72,221 of 168,860 BH-significant cell-map records = 42.77%.
- **Mode/status:** sensitivity / qualified
- **Temporal role:** both (1985_2025)
- **Robustness:** sensitive
- **Boundary:** BH remains the prespecified primary rule; highlighted clusters may be labelled BY-robust only when they pass BY.
- **Source:** Phase 6, `phase6/local_moran_lisa_findings_phase6_v1.md` — Multiple-testing sensitivity

### P9A018 — biome_process_totals

Consolidation and endpoint NAT-to-TMP are Cerrado-associated over the primary period, while replenishment totals are similar with a slightly larger Amazon contribution.

- **Evidence:** Million ha: consolidation Amazon 5.10 vs Cerrado 15.02; replenishment 47.81 vs 45.81; NAT-to-TMP 2.04 vs 7.11.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** robust
- **Boundary:** Primary-biome assignment attributes whole cells and is not an exact pixel partition by biome.
- **Source:** Phase 7, `phase7/phase7_biome_comparison_findings_v1.md` — Process magnitude and changing biome contributions

### P9A019 — biome_trajectory_dynamics

NAT-to-TMP magnitude classes are more dynamic through time in Cerrado than Amazon.

- **Evidence:** Mean state changes: Amazon 0.79, Cerrado 2.13; constant trajectories: 68.0% vs 18.0%.
- **Mode/status:** descriptive / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** robust
- **Boundary:** State changes are five-year cell classes and do not track annual pixel trajectories.
- **Source:** Phase 7, `phase7/phase7_biome_comparison_findings_v1.md` — Cell-state trajectories

### P9A020 — biome_hh_contribution

Cerrado contributes more persistent HH cells for consolidation, NAT-to-TMP and C-R balance, whereas Amazon contributes more for replenishment.

- **Evidence:** Persistent replenishment HH: Amazon 2,785 vs Cerrado 1,569; persistent NAT-to-TMP HH: 153 vs 511.
- **Mode/status:** local_inference / supported
- **Temporal role:** primary (1985_2020)
- **Robustness:** robust
- **Boundary:** These are biome contributions to the accepted combined-domain LISA pattern, not newly fitted within-biome Local Moran models.
- **Source:** Phase 7, `phase7/phase7_biome_comparison_findings_v1.md` — HH occurrence and persistence

### P9A021 — biome_boundary_sensitivity

The principal biome comparisons are stable when all 582 transbiome cells are removed.

- **Evidence:** All 160 Global Moran significance decisions retained; maximum absolute I change = 0.044848.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** robust
- **Boundary:** Stability does not make primary-biome totals exact within-biome pixel totals.
- **Source:** Phase 7, `phase7/phase7_biome_comparison_findings_v1.md` — Boundary-cell sensitivity

### P9A030 — causal_boundary

The accepted evidence supports spatial and temporal association, concentration and persistence statements, not causal attribution.

- **Evidence:** No commodity-price, infrastructure, policy, tenure or causal-design model is included in Phases 1-8.
- **Mode/status:** limitation / qualified
- **Temporal role:** both (1985_2025)
- **Robustness:** not_applicable
- **Boundary:** Do not translate descriptive or spatial-inference results into causal drivers.
- **Source:** Phase 0-9, `planning/006_spatiotemporal_investigation_plan.md` — Interpretation boundaries


## RQ5

### P9A022 — aggregate_and_temporal_maup

Aggregate signs, dominance classes and temporal extrema are robust to alternative scale and zoning, while some conditional distributions are sensitive.

- **Evidence:** All 192 aggregate and 48 temporal comparisons pass; shifted 20k passes all components; 10k and 40k have distribution/support sensitivities.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** partially_robust
- **Boundary:** Robust aggregate behavior does not guarantee invariance of cell-level distributions.
- **Source:** Phase 8C, `phase8c/phase8c_maup_robustness_findings_v1.md` — Main findings and qualifications

### P9A023 — global_moran_maup

The positive direction and formal significance of global spatial clustering are robust across alternative grids.

- **Evidence:** 120/120 alternative coefficients positive and BY-significant; 119/120 interval magnitude checks pass.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** robust
- **Boundary:** Exact coefficient magnitudes and temporal ranking are separate robustness criteria.
- **Source:** Phase 8D, `phase8d/phase8d_maup_global_moran_findings_v1.md` — Main outcome

### P9A024 — global_moran_temporal_maup

Exact Global Moran magnitudes and temporal ordering show partial MAUP sensitivity concentrated in NAT-to-TMP.

- **Evidence:** One interval magnitude failure and 8/30 strict temporal failures; all six aggregate grid-window assessments fail at least one strict criterion.
- **Mode/status:** sensitivity / qualified
- **Temporal role:** both (1985_2025)
- **Robustness:** partially_robust
- **Boundary:** Failure of a strict comparison does not imply absence of positive spatial autocorrelation.
- **Source:** Phase 8D, `phase8d/canonical_maup_global_moran_assessment_v1.csv` — Six grid-window assessment rows

### P9A025 — hh_cluster_maup

HH location and persistence are robust for replenishment, net C-R balance and the bounded C-R index.

- **Evidence:** Each metric passes 6/6 grid-window assessments; interval passes are 24/24, 23/24 and 24/24 respectively.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** robust
- **Boundary:** Agreement is broad area-weighted footprint agreement, not cell-for-cell identity.
- **Source:** Phase 8E, `phase8e/canonical_maup_hh_robustness_assessment_v1.csv` — Metric-specific assessment rows

### P9A026 — hh_cluster_maup

Consolidation HH recurrence and persistence are recognizable, but interval footprint location is scale-sensitive.

- **Evidence:** 3/6 complete assessments pass; 16/24 interval maps pass.
- **Mode/status:** sensitivity / qualified
- **Temporal role:** both (1985_2025)
- **Robustness:** partially_robust
- **Boundary:** Describe as partial robustness rather than either full invariance or invalidity.
- **Source:** Phase 8E, `phase8e/phase8e_maup_hh_cluster_findings_v1.md` — Consolidation

### P9A027 — hh_cluster_maup

Endpoint NAT-to-TMP HH footprint location and persistence are sensitive to spatial scale and zoning.

- **Evidence:** 0/6 complete assessments and 7/24 interval comparisons pass.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** sensitive
- **Boundary:** Many failures retain high overlap coefficients, indicating footprint expansion or contraction around partly shared cores rather than universal relocation.
- **Source:** Phase 8E, `phase8e/phase8e_maup_hh_cluster_findings_v1.md` — Endpoint NAT-to-TMP

### P9A028 — canonical_support_decision

The canonical approximately 20,000-ha grid remains the primary analytical support after the MAUP assessment.

- **Evidence:** Phase 8A-E completed; alternative grids remain sensitivity analyses.
- **Mode/status:** sensitivity / supported
- **Temporal role:** both (1985_2025)
- **Robustness:** robust
- **Boundary:** Primary status does not erase metric-specific MAUP sensitivity and must be reported with qualifications.
- **Source:** Phase 8, `phase8e/phase8_maup_robustness_synthesis_v1.md` — Final Phase 8 decision

### P9A029 — diagnostic_extension

The diagnostic interval reinforces some sensitivity findings but does not create the principal NAT-to-TMP MAUP result.

- **Evidence:** NAT-to-TMP is already sensitive in 1985-2020; 2020-2025 additionally affects full-window 40k consolidation.
- **Mode/status:** sensitivity / qualified
- **Temporal role:** diagnostic (2020_2025)
- **Robustness:** partially_robust
- **Boundary:** Diagnostic evidence is included and flagged but does not replace primary-period conclusions.
- **Source:** Phase 8E, `phase8e/phase8_maup_robustness_synthesis_v1.md` — Diagnostic extension

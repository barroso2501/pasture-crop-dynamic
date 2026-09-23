# Decision 022 — Temporal-boundary symmetry: the 1985 baseline and the stacked uncertainty sources in 2020–2025

* **Status:** Accepted. The MapBiomas Collection 11 temporal-filter specification (Filter specification section below) is recorded for TMP, PAS, and NAT, including the PAS edge-year rule and the formal source citations (Source citations section below). All acceptance criteria are satisfied; see Acceptance criteria.
* **Date recorded:** 2026-09-23
* **Scope:** manuscript-level and documentation-level interpretation of both temporal boundaries of the canonical eight-interval series (the 1985 baseline and the 2020–2025 diagnostic interval), and consolidation of the distinct uncertainty sources that affect claims made near either boundary.
* **Related plan:** `docs/planning/006\_spatiotemporal\_investigation\_plan.md`
* **Related decisions:** 005 (full-domain stock-flow processing), 009 (multiquinquennial episodes and 2020–2025), 014–018 (Phase 8 MAUP grid design and comparison criteria), 020 (Phase 9 RQ1/RQ2 gap resolution)
* **Related outputs:** canonical integrated panel, RQ1 fixed-cohort table, RQ2 origin-partition table, Phase 8E HH cluster-persistence tables, Phase 9A/9A.1 evidence matrix
* **Related methods doc:** `docs/methods/data\_sources\_and\_classification.md` (defines the `NAT`/`PAS`/`TMP` MapBiomas code groups referenced in the Filter specification section)

## Context

Three prior decisions each documented a true and independently correct fact about one edge of the canonical series, but the three facts were never connected into a single explicit statement, and the series' two temporal boundaries have consequently been treated asymmetrically in downstream discussion:

* Decision 005 recorded that 2020–2025 is processed with the same schema but flagged diagnostic **because the final years of the source series do not have the same temporal filtering support as earlier years** — a statement about classification data quality, not about inference.
* Decision 009 recorded that episodes and trajectories reaching 2025 are right-boundary censored, and, separately, that processes beginning before 1985 may be left-boundary censored — a statement about what can and cannot be inferred from an observation window of fixed length.
* Decision 020 operationalized the left boundary through the pasture-age code, defining the RQ1 cohort as pixels whose 1985 pasture-age code equals 100, "the left-censored initial pasture stock," and partitioning RQ2 consolidation accordingly.

None of the accepted documentation states plainly that **1985 is not a land-use-process reference date**: it is the earliest year for which the source Landsat-based classification series is treated as consistent, and its selection reflects image-archive availability, not a methodological judgment that land-use dynamics began there. Absent an explicit statement, the 1985 pasture stock risks being read informally — including in manuscript text — as an initial condition or point of origin, while the 2020–2025 interval is read as the series' only weak edge. Both readings are unsupported by the data-generating process: both temporal boundaries are artifacts of the observation window, not of the phenomenon under study.

Separately, three independent sources of uncertainty currently converge on the same claim type — NAT→TMP magnitude and location in the 2020–2025 interval — and have so far been referred to collectively, in informal discussion, under the single label "diagnostic." Collapsing them loses information a reviewer needs, because each has a different cause, a different scope (series-wide versus interval-specific), and a different remedy:

1. reduced temporal-filter support in the final years of the source classification series (Decision 005) — a data-quality property of the input product, independent of any real trend, likely concentrated in the last one to two years of the series depending on the filter window used;
2. right-boundary censoring of episodes and trajectories that reach 2025 (Decision 009) — an inferential property of the fixed observation window, affecting only claims about episode fate or completion;
3. MAUP sensitivity of NAT→TMP density at the local-cluster level, with zero of six Phase 8E assessments passing (Decisions 014–018) — a spatial-scale and zoning property that applies to the full 1985–2025 series, not specifically to the final interval, but that compounds with (1) and (2) when the claim in question is about 2020–2025 NAT→TMP specifically.

This decision states the boundary symmetry explicitly and requires the three 2020–2025 uncertainty sources to be named individually rather than folded into one blanket caveat.

## Decision

### 1\. The 1985 baseline is an observation-window artifact, not a process origin

The 1985 pasture stock (and, more generally, the 1985 coverage state of any cell) will be described in all manuscript-facing text and future documentation as **the earliest observed state**, never as **the origin**, **the initial conversion**, or **the starting point** of the underlying land-use process. Pixels carrying pasture-age code 100 may have been pasture for an unknown and potentially long duration before 1985; the code records left-censoring, not recency.

### 2\. The left-censoring partition already in place is reaffirmed, not altered

The RQ1 cohort definition and the RQ2 origin partition established in Decision 020 (left-censored 1985 pasture stock vs. pasture established during the observed series vs. unresolved vs. unattributed) remain the accepted operational treatment of left-censoring. This decision adds the epistemic statement in Section 1; it does not modify any accepted computation, cohort, or partition.

### 3\. The 2020–2025 interval carries three distinct, independently sourced uncertainties, unevenly distributed within it

Any documentation or manuscript text discussing results for the 2020–2025 interval — and, in particular, NAT→TMP results within it — must identify which of the following apply, rather than using "diagnostic" as a single undifferentiated label:

* **temporal-filter-limited**: classification in part of this sub-period has reduced or absent temporal-filter support relative to earlier years (Decision 005; quantified per class in the Filter specification section below); this is a statement about input data quality and applies to simple magnitude and area claims, not only to trajectory claims. Its severity is class- and year-specific, not uniform across 2020–2025 — see the Filter specification section;
* **right-boundary-censored**: episode or trajectory fate beyond 2025 is unknown (Decision 009); this applies only to claims about persistence, reversal, or completion, not to endpoint-composition claims, and applies uniformly across 2020–2025 rather than concentrating at 2025 specifically;
* **MAUP-sensitive**: NAT→TMP density at the local-cluster level did not pass the prespecified Phase 8E spatial-sensitivity tests (Decisions 014–018); this applies across the full series and is not unique to 2020–2025, but must be flagged wherever NAT→TMP density is reported at cluster or local scale, including within the diagnostic interval.

A given claim about 2020–2025 NAT→TMP may be subject to all three simultaneously; the manuscript must say so explicitly rather than defaulting to the single term "diagnostic," which does not by itself convey which limitation governs which part of the claim, nor that the temporal-filter limitation is concentrated at the 2024–2025 edge rather than spread evenly across the interval.

### 4\. Terminology requirement

The existing label `diagnostic temporal-boundary interval` (Decision 009) is retained for 2020–2025 as a general marker of series-boundary status. It is not sufficient, on its own, to satisfy the reporting requirement in Section 3 wherever the specific claim is about NAT→TMP magnitude or location; in those cases the applicable term(s) from Section 3 must also be used.

### 5\. Reporting requirement extends to the 1985 boundary symmetrically

Wherever a table, figure caption, or manuscript passage flags the temporal-boundary status of 2020–2025, any co-presented claim resting on the 1985 baseline (e.g., RQ1 redistribution shares, RQ2 left-censored-origin shares) must carry an equivalent, equally visible left-boundary statement using the "earliest observed state" language from Section 1. Neither boundary may be presented as unqualified while the other is flagged.

## Filter specification (MapBiomas Collection 11 ATBD)

**Source:** MapBiomas Collection 11 Algorithm Theoretical Basis Document (ATBD), General Handbook and the appendices for Agriculture and Forest Plantation, Pasture, Cerrado, and Amazônia, as supplied by the project's science lead. Full bibliographic citations are recorded in the Source citations section below.

The temporal-filter degradation at the series edges is not uniform across the project's aggregated classes (`docs/methods/data\_sources\_and\_classification.md`), and within 2020–2025 it is concentrated in the final one to two years rather than spread evenly across the interval.

### TMP (MapBiomas codes 19, 20, 39, 40, 41, 62)

TMP aggregates three ATBD-defined groups with distinct edge treatment:

* **Culturas Temporárias — Soja (39), Algodão (62), Outras Temporárias (41), and the generic aggregate class (19).** Raw soy and cotton classifications are masked by a 3-year window with a 2-year threshold applied to an aggregated "temporary crops" mask. This filter covers 1986–2024. At 1985, a single-sided rule applies (a pixel is retained only if also classified as temporary crop in 1986). **At 2025, no temporal filter is applied at all.** This is the most severe edge effect identified for any class used in this project, and it affects what is plausibly the dominant sub-component of TMP in the Cerrado agricultural frontier.
* **Arroz Irrigado (40).** A national 5-year window with a 3-year threshold, plus a regional 3-year window with a 2-year threshold (the South is excepted from the second filter). Coverage is described as the full series except the extreme edges, which lack neighborhood support under the general rule; 1985 and 2025 are therefore also reduced for this sub-class, though the source does not specify the mechanism as precisely as for temporary crops above.
* **Cana-de-Açúcar (20).** Four chained filters. The interior 3-year/2-year filter explicitly excludes both 1985 and 2025. Unlike temporary crops, sugarcane receives a dedicated border filter at 2025 (a 5-year window with a 2-year threshold), so its 2025 classification is differently filtered from the interior years, not unfiltered.

**Net effect for TMP:** 2025 classification reliability is heterogeneous across its sub-classes. The temporary-crops component (soy, cotton, other annual crops) — plausibly the largest contributor to `NAT→TMP` and `PAS→TMP` flows in the Cerrado — carries no temporal-filter correction whatsoever in 2025. 2020–2023 fall within the interior window for all three sub-classes and are not subject to this specific degradation.

### PAS (MapBiomas code 15)

Pasture classification is stabilized at three complementary levels, none of which is a single symmetric window: the cross-cutting thematic algorithm, biome-specific integration rules (Amazônia and Cerrado), and general post-integration rules.

* **Cross-cutting thematic level.** A combined 3×3 spatial and 5-year temporal median filter (`scipy.ndimage.median`, 45 probability values per pixel), with the Collection 11 confirmation threshold lowered from >51% to ≥40%. Because the 5-year window is centered and requires both `t-2` and `t+2`, 1985–1986 lack historical support and 2024–2025 lack future support; the source states that resulting omission/commission inconsistencies at the series extremes are corrected downstream, at integration.
* **General post-integration level.** The dedicated pasture post-integration filter (5-year kernel, fixing 1–3-year `Mosaico de Usos` (21) interruptions inside stable pasture sequences) applies corrections only to central years (`Y-1, Y, Y+1`) and explicitly preserves border values (`Y-2, Y+2`) unmodified; it operates on 1987–2023, leaving 1985–1986 and 2024–2025 to the transition filters and biome-specific rules below. A spurious border-transition filter separately converts `\[15→21→15]` to continuous pasture and reverts isolated one-year pasture noise inside forest (`\[3→15→3]→\[3→3→3]`). A minimum-transition-unit filter discards any native-vegetation↔pasture/mosaic transition smaller than 6 contiguous pixels (\~0.5 ha) occurring specifically within the 1985–1986 or 2024–2025 pairs, suppressing border "dancing-pixel" noise.
* **Amazônia biome level.** Pasture from the cross-cutting layer is reconciled against the biome's annual map through a deterministic 50-rule matrix. At the initial border (1985, rule RG04): if `t-1 = Not Observed`, `t = Pasture`, `t+1 = Pasture`, then `t` is confirmed as Pasture — preventing 1985 pasture from being discarded as spectral noise when confirmed the following year. At the final border (2025, rule RG10): if `t-1 = Pasture`, `t = Pasture`, `t+1 = Not Observed`, `t` is retained as Pasture. A formal prevalence exception in Amazônia gives the cross-cutting Pasture class (15, ordinarily precedence order 30) priority over the biome's Forest Formation class (3, ordinarily order 23), so that anthropogenic conversion is preserved rather than reverted to forest at the point of integration.
* **Cerrado biome level.** Pasture (15) and Agriculture (18) are merged into `Mosaico de Usos` (21) in the biome's internal post-processing before integration with the cross-cutting theme, which changes what "PAS" reconciliation means structurally in this biome relative to Amazônia. At the initial border (1985): trajectories where a pixel was anthropic/pasture in 1985 but consistently native (forest, savanna, or grassland) in 1986–1987 are forced to that native class in 1985; separately, pixels classified as anthropic (21 or 25) in 1985 with 13 or more years of `Campo Limpo/Sujo` (12) across the series and classified as `Campo` in 2024 are reclassified to `Formação Campestre` for the entire series, including 1985. At the recent/final border (2023–2025): from 2023 onward, moving-window corrections are blocked from letting any native-vegetation class revert a pixel already classified as `Mosaico de Usos` (21), preserving recent deforestation; pixels stable in 2022–2023 that shift to `Campo` (12) or bare soil (25) in 2024–2025 are forced back to their 2023 class; a closing rule sets 2025 to the 2024 value when 2023 and 2024 are identical, unless the divergent 2025 value is `Mosaico de Usos` (21), which is retained, or unless the pixel was anthropic in 2024 (supported by 2022 or 2023) and diverges in 2025, in which case 2025 is forced to `Mosaico de Usos`.

A separate, non-edge-specific Collection 11 scheme change is worth flagging even though it falls outside this decision's temporal-boundary scope: outside Conservation Units, Pasture (15) now precedes `Campo` (12) and `Área Úmida` (11) in the Cerrado prevalence hierarchy, and the historical rule giving pasture precedence over Formação Savânica (4) was removed. This changes `PAS`↔`NAT` boundary behavior across the whole series, not only at 1985 or 2025, and bears directly on the confusion risk already flagged in `docs/methods/data\_sources\_and\_classification.md` ("transitions between planted pasture and native grassland may be sensitive to classification confusion"). It is noted here for provenance because it surfaced in the same source material, but it is a classification-scheme property, not a temporal-boundary one, and is out of scope for this decision; it may warrant its own decision or a note in that methods document.

**Net effect for PAS:** 2020–2023 fall within full filter support at the cross-cutting and post-integration levels. 2024–2025 do not: the cross-cutting filter loses future support, the post-integration pasture filter excludes this pair from its corrections, and (in the Amazônia biome) 2025 is stabilized only by the single-neighbor rule RG10 rather than the full window used in the interior. 1985–1986 are symmetrically affected on the left, with 1985 additionally subject to biome-specific reclassification rules in the Cerrado (the `X-A-A` and 13-year-Campo rules above) that do not apply to any other year in the series.

### NAT (Cerrado and Amazônia aggregate groups)

Native-vegetation classes are stabilized primarily through biome-specific edge mechanisms rather than a single symmetric window: bidirectional gap-fill (1985–2025), a frequency-based modal-class filter using the most recent nine years (2017–2025) as its reference window, and, in Amazônia, dedicated first-year (1985) and last-year (2025) rules that propagate a class only when the two adjacent years are stable. These mechanisms provide coverage across the full 1985–2025 series, unlike the TMP temporary-crops component above, but rely on fewer neighboring years and different logic (propagation and modal-frequency assignment rather than a centered multi-year window) at both edges than in the interior of the series.

**Net effect for NAT:** edge years are covered, but by structurally weaker mechanisms than interior years. This differs in kind from the TMP finding above, where the 2025 temporary-crops component has no correction mechanism at all.

### Post-integration filters

After biome layers are merged, a further harmonization pass applies. The agriculture post-integration filter (3-year window) covers 1986–2024, again excluding both 1985 and 2025. The pasture post-integration filter (5-year window) covers 1987–2023, excluding 1985–1986 and 2024–2025. Both series edges therefore sit outside the final harmonization step for the two classes central to RQ1–RQ3 (`PAS`, `TMP`), independent of and in addition to the class-specific filters above.

### Implication for Decision 022, Section 3

The `temporal-filter-limited` label should not be applied uniformly to 2020–2025:

* **2020–2023** `NAT→TMP` and `PAS→TMP` claims are not subject to the temporal-filter degradation described here for TMP's temporary-crops component or for PAS. The right-boundary-censoring and MAUP-sensitivity limitations (Section 3, items 2–3) still apply to this sub-window as previously stated.
* **2024–2025** carry the temporal-filter limitation for PAS at both the cross-cutting level (loss of future window support) and the post-integration level (excluded from the dedicated pasture correction filter); in Amazônia, 2025 is stabilized only by the single-neighbor rule RG10 rather than the full window.
* **2025 alone** carries the most severe form of this limitation for TMP's temporary-crops sub-component (no filter applied) and a distinct, dedicated but weaker filter for its sugarcane sub-component.

Manuscript text reporting `NAT→TMP` or `PAS→TMP` results at annual or near-terminal resolution within 2020–2025 must distinguish 2025 specifically from 2020–2023, rather than treating the whole diagnostic interval as uniformly affected. This also means the case for treating 2020–2023 as substantively weaker than the primary period, solely on temporal-filter grounds, is not supported by this specification — the right-boundary-censoring and MAUP-sensitivity limitations remain the operative caveats for that sub-window.

## Source citations (MapBiomas Collection 11 ATBD)

The following are recorded as supplied by the project's science lead; they have not been independently verified against the publisher's site by this decision.

1. **General Handbook.** MapBiomas. *MapBiomas General Handbook — Algorithm Theoretical Basis Document (ATBD): Collection 11.* Version 1.0, August 2026. General coordination: Tasso Azevedo; technical coordination: Marcos Rosa; scientific coordination: Julia Shimbo. Available at https://mapbiomas.org/en/download-of-atbds ; data repository https://data.mapbiomas.org/ ; platform https://brasil.mapbiomas.org/ ; source code https://github.com/mapbiomas-brazil . No DOI supplied.
2. **Pasture Appendix.** Ferreira Jr., L.; Matos, A. P.; Mesquita, V. (2026). *MapBiomas Land Use and Land Cover — Algorithm Theoretical Basis Document (ATBD) — Collection 11 — Pasture Appendix.* Version 1.0, August 2026, 41 p. General coordination: Laerte Guimarães Ferreira Jr.; technical coordination: Ana Paula Matos and Vinicius Vieira Mesquita; technical team: Ana Paula Carlos Assunção, Amanda Rosa Falcão, Leandro Parente, Luís Bauman, Mariana Gomes, Nathalia Teles, Tharles Andrade, Wilton Ladeira da Silva. Available at https://mapbiomas.org/en/download-of-atbds ; LAPIG/UFG repository https://maps.lapig.iesa.ufg.br/ . No DOI supplied.
3. **Cerrado Appendix.** Alencar, A. A.; Souza, A. G. P.; Silva, B. C.; Conciani, D. E.; Pereira, J. J. S. P.; Shimbo, J. Z.; Arruda, V. L. S.; Silva, W. V. (2026). *MapBiomas Land Use and Land Cover — Algorithm Theoretical Basis Document (ATBD) — Collection 11 — Cerrado Appendix.* Version 1.0, August 2026, 44 p. General coordination: Ane A. Alencar (IPAM). Available at https://mapbiomas.org/en/download-of-atbds ; source code https://github.com/mapbiomas/brazil-cerrado . No DOI supplied.
4. **Amazon Appendix.** Ferreira, B.; Siqueira, J. V.; Amorim, L.; Damasceno, C.; Brandão, I.; Ferreira, R.; Athaíde, M. (2026). *MapBiomas Land Use and Land Cover — Algorithm Theoretical Basis Document (ATBD) — Collection 11 — Amazon Appendix.* Version 1.0, August 2026, 18 p. General and technical coordination: Bruno Ferreira (IMAZON). Available at https://mapbiomas.org/en/download-of-atbds ; source code https://github.com/mapbiomas/brazil-amazon . No DOI supplied.
5. **Agriculture and Forest Plantation Appendix.** Weber, E.; Santos, K. S. M.; Teixeira Junior, P. D. P.; Silva, C. I. S.; Santos, G. V.; Mourão, M. C. (2026). *MapBiomas Land Use and Land Cover — Algorithm Theoretical Basis Document (ATBD) — Collection 11 — Agriculture and Forest Plantation Appendix.* Version 1.0, August 2026, 37 p. General coordination: Eliseu Weber (Remap Geotecnologia). Available at https://mapbiomas.org/en/download-of-atbds ; agriculture source code https://github.com/mapbiomas/brazil-agriculture ; forest plantation source code https://github.com/mapbiomas/brazil-forest-plantation . No DOI supplied.

None of the five documents was supplied with a DOI; citation relies on the publisher's download page and, where given, the source-code repository. If a DOI or a permanent archival link (e.g., a Zenodo record) is minted for these documents, it should be added here and to the manuscript's reference list.

## Rationale

* Prevents an implicit and unjustified asymmetry in which the 1985 baseline reads as solid ground and 2020–2025 reads as uniformly weak, when both are in fact bounded by the same kind of artifact: a fixed observation window imposed by data availability, not by the land-use process itself.
* Separating the three 2020–2025 uncertainty sources allows each claim to carry only the caveats that actually apply to it, instead of either overstating risk (attaching all three to a simple magnitude claim that only inherits temporal-filter limitation) or understating it (using "diagnostic" as a soft gloss that a technically informed reviewer will read as vague hedging rather than a specific, defensible limitation).
* Naming the temporal-filter mechanism (Decision 005) precisely, once its specification is available, is expected to read as a sign of technical command of the MapBiomas classification pipeline rather than as generic caution — this is judgment about reviewer reception, not a documented fact, and should be treated as such in any manuscript-strategy discussion.
* Consistent with the project's existing practice (Decisions 008, 009, 010, 019, 020) of making temporal- and inferential-boundary treatment an explicit, auditable decision rather than an implicit convention.

## Consequences

### Positive consequences

* Manuscript and documentation language about both series boundaries becomes precise and symmetric.
* Reviewers encounter three named, individually defensible limitations instead of one generic caveat, reducing the likelihood that a single sharp question ("how reliable is your last year?" or "how do you know 1985 pasture wasn't already decades old?") is left only partially answered.
* No accepted computation, cohort definition, partition, or validated output is altered by this decision.

### Constraints and interpretation limits

* The Filter specification and Source citations sections record the temporal-filter mechanism for TMP, PAS, and NAT and the formal bibliographic citations for the five source ATBD documents, as supplied by the project's science lead. Neither the mechanism descriptions nor the citations have been independently verified by this decision against the publisher's site; that verification is recommended before the manuscript's reference list is finalized, but is not treated as a blocking condition here.
* No DOI was supplied for any of the five ATBD documents; citation currently relies on the publisher's download page and, where given, the source-code repository.
* The Collection 11 Cerrado prevalence-rule change noted in the PAS subsection above (removal of pasture's historical precedence over Formação Savânica) is a classification-scheme property affecting the full series, not a temporal-boundary artifact. It is recorded here for provenance only; it is out of scope for this decision and is not covered by any acceptance criterion below.
* The three 2020–2025 uncertainty sources are conceptually distinct but may co-occur on the same cell or metric; this decision requires them to be named separately, not that they be shown to be statistically independent of one another.
* The Filter specification section's identification of the temporary-crops sub-component as "plausibly the largest contributor" to Cerrado `NAT→TMP`/`PAS→TMP` flows is a judgment, not a value computed from the project's own accepted outputs; it should be verified against the project's own class-composition statistics before being asserted as fact in manuscript text.
* This is an interpretation- and reporting-layer decision, structurally analogous to Decision 009: it governs how existing, already-accepted results are described, not how they are computed.

## Alternatives considered

### Leave the 1985 baseline implicitly treated as solid ground

Rejected. It misrepresents the data-generating process (Landsat-archive availability, not a land-use-process milestone) and is inconsistent with the left-censoring partition the project has already adopted in Decision 020.

### Continue using "diagnostic temporal-boundary interval" as the sole label for 2020–2025 results

Rejected. It conflates three uncertainty sources with different causes, different scopes, and different manuscript implications, and risks reading as generic hedging to a technically informed reviewer rather than as a specific, defensible limitation.

### Defer this decision until the MapBiomas temporal-filter specification is obtained

Rejected. Sections 1, 2, 4, and 5, and the qualitative part of Section 3, do not depend on that specification. Following the precedent of Decision 020 (approved for implementation with an explicit open acceptance condition), the specification is recorded here as a named, pending acceptance criterion rather than a blocking dependency for the whole decision.

## Implementation requirements

1. Manuscript and methods text describing the 1985 pasture stock or any 1985 coverage state must use "earliest observed state" and must not use "origin," "initial conversion," or "starting point" without that qualification.
2. Manuscript and methods text reporting 2020–2025 NAT→TMP results must name the applicable term(s) from Section 3 (`temporal-filter-limited`, `right-boundary-censored`, `MAUP-sensitive`) rather than "diagnostic" alone.
3. Table and figure captions presenting both a 1985-baseline claim and a 2020–2025 claim side by side must flag both boundaries with equivalent visibility, per Section 5.
4. Any future methods note or manuscript draft section citing Decision 005, 009, or 020 for boundary treatment should also cite this decision where the reporting language in Sections 3–5 applies.
5. The MapBiomas Collection 11 temporal-filter specification, including the exact PAS edge-year rules and the formal bibliographic citations for the five source ATBD documents, is recorded in the Filter specification and Source citations sections above. Independent verification of the citations against the publisher's site (title, authorship, DOI if later minted) is recommended before the manuscript's reference list is finalized.
6. Manuscript text reporting `NAT→TMP` or `PAS→TMP` results within 2020–2025 must distinguish 2025 from 2020–2023 wherever the temporal-filter limitation is invoked, per the Filter specification section's Implication subsection.
7. Before manuscript text asserts that the temporary-crops sub-component is the largest contributor to Cerrado `NAT→TMP`/`PAS→TMP` flows, that claim must be checked against the project's own accepted class-composition outputs rather than asserted on the basis of this decision alone.

## Acceptance criteria

This decision is implemented when:

* no accepted document or manuscript draft describes the 1985 pasture stock as a process origin;
* every accepted document or manuscript passage reporting 2020–2025 NAT→TMP results names the applicable uncertainty source(s) from Section 3;
* tables or captions presenting both boundaries together flag both, per Section 5;
* manuscript text invoking the temporal-filter limitation for 2020–2025 distinguishes 2025 from 2020–2023, per the Filter specification section;
* the exact PAS edge-year rules for 1985–1986 and 2024–2025 are recorded — satisfied, per the Filter specification section;
* formal bibliographic citations for the source MapBiomas Collection 11 ATBD documents are recorded — satisfied, per the Source citations section; independent verification against the publisher's site remains recommended, not blocking;
* no accepted computation, cohort definition, partition, or validated numerical output is changed as a result of this decision.

All acceptance criteria above are satisfied as of 2026-09-23.

## Terminology

Preferred terms:

* **earliest observed state** (1985 baseline, in place of "origin" or "initial conversion");
* **left-censored 1985 pasture stock** (pasture-age code 100, per Decision 020);
* **temporal-filter-limited** (2020–2025 classification-quality property, per Decision 005 and the Filter specification section; class- and year-specific, not uniform across the interval);
* **2025 unfiltered temporary-crops component** (the specific finding that TMP's soy/cotton/other-temporary-crops sub-classes carry no temporal filter in 2025, per the Filter specification section);
* **right-boundary-censored** (2020–2025 episode/trajectory-fate property, per Decision 009; applies uniformly across the interval);
* **MAUP-sensitive** (NAT→TMP local-cluster scale/zoning property, per Decisions 014–018);
* **diagnostic temporal-boundary interval** (retained general marker, per Decision 009, insufficient alone for NAT→TMP-specific claims).

Terms to avoid without additional qualification:

* 1985 pasture "origin," "initial conversion," or "starting point";
* 2020–2025 results described only as "diagnostic" when the claim concerns NAT→TMP magnitude or location;
* "2020–2025" used as if the temporal-filter limitation applied evenly across the interval, when the Filter specification section shows it concentrates in 2024–2025 (PAS) and 2025 specifically (TMP temporary-crops component);
* any statement implying the 1985 baseline is free of the kind of observation-window limitation flagged for 2020–2025.


# Decision 022 — Temporal-boundary symmetry: the 1985 baseline and the stacked uncertainty sources in 2020–2025

* **Status:** Accepted. Acceptance condition 3 (MapBiomas Collection 11 temporal-filter specification) remains open; see Acceptance criteria.
* **Date recorded:** 2026-09-23
* **Scope:** manuscript-level and documentation-level interpretation of both temporal boundaries of the canonical eight-interval series (the 1985 baseline and the 2020–2025 diagnostic interval), and consolidation of the distinct uncertainty sources that affect claims made near either boundary.
* **Related plan:** `docs/planning/006\_spatiotemporal\_investigation\_plan.md`
* **Related decisions:** 005 (full-domain stock-flow processing), 009 (multiquinquennial episodes and 2020–2025), 014–018 (Phase 8 MAUP grid design and comparison criteria), 020 (Phase 9 RQ1/RQ2 gap resolution)
* **Related outputs:** canonical integrated panel, RQ1 fixed-cohort table, RQ2 origin-partition table, Phase 8E HH cluster-persistence tables, Phase 9A/9A.1 evidence matrix

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

### 3\. The 2020–2025 interval carries three distinct, independently sourced uncertainties

Any documentation or manuscript text discussing results for the 2020–2025 interval — and, in particular, NAT→TMP results within it — must identify which of the following apply, rather than using "diagnostic" as a single undifferentiated label:

* **temporal-filter-limited**: classification in this sub-period has reduced temporal-filter support relative to earlier years (Decision 005); this is a statement about input data quality and applies to simple magnitude and area claims, not only to trajectory claims;
* **right-boundary-censored**: episode or trajectory fate beyond 2025 is unknown (Decision 009); this applies only to claims about persistence, reversal, or completion, not to endpoint-composition claims;
* **MAUP-sensitive**: NAT→TMP density at the local-cluster level did not pass the prespecified Phase 8E spatial-sensitivity tests (Decisions 014–018); this applies across the full series and is not unique to 2020–2025, but must be flagged wherever NAT→TMP density is reported at cluster or local scale, including within the diagnostic interval.

A given claim about 2020–2025 NAT→TMP may be subject to all three simultaneously; the manuscript must say so explicitly rather than defaulting to the single term "diagnostic," which does not by itself convey which limitation governs which part of the claim.

### 4\. Terminology requirement

The existing label `diagnostic temporal-boundary interval` (Decision 009) is retained for 2020–2025 as a general marker of series-boundary status. It is not sufficient, on its own, to satisfy the reporting requirement in Section 3 wherever the specific claim is about NAT→TMP magnitude or location; in those cases the applicable term(s) from Section 3 must also be used.

### 5\. Reporting requirement extends to the 1985 boundary symmetrically

Wherever a table, figure caption, or manuscript passage flags the temporal-boundary status of 2020–2025, any co-presented claim resting on the 1985 baseline (e.g., RQ1 redistribution shares, RQ2 left-censored-origin shares) must carry an equivalent, equally visible left-boundary statement using the "earliest observed state" language from Section 1. Neither boundary may be presented as unqualified while the other is flagged.

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

* This decision does not itself supply the MapBiomas Collection 11 temporal-filter specification; until that specification is recorded, the "temporal-filter-limited" label in Section 3 can be asserted qualitatively (per Decision 005) but not quantified (window size, years affected).
* The three 2020–2025 uncertainty sources are conceptually distinct but may co-occur on the same cell or metric; this decision requires them to be named separately, not that they be shown to be statistically independent of one another.
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
5. When the MapBiomas Collection 11 temporal-filter specification (window size, algorithm) becomes available, it should be appended to this decision under a new "Filter specification" subsection rather than recorded only in manuscript text, so the source remains auditable from the repository.

## Acceptance criteria

This decision is implemented when:

* no accepted document or manuscript draft describes the 1985 pasture stock as a process origin;
* every accepted document or manuscript passage reporting 2020–2025 NAT→TMP results names the applicable uncertainty source(s) from Section 3;
* tables or captions presenting both boundaries together flag both, per Section 5;
* the MapBiomas Collection 11 temporal-filter specification is obtained and appended to this decision — **open**;
* no accepted computation, cohort definition, partition, or validated numerical output is changed as a result of this decision.

## Terminology

Preferred terms:

* **earliest observed state** (1985 baseline, in place of "origin" or "initial conversion");
* **left-censored 1985 pasture stock** (pasture-age code 100, per Decision 020);
* **temporal-filter-limited** (2020–2025 classification-quality property, per Decision 005);
* **right-boundary-censored** (2020–2025 episode/trajectory-fate property, per Decision 009);
* **MAUP-sensitive** (NAT→TMP local-cluster scale/zoning property, per Decisions 014–018);
* **diagnostic temporal-boundary interval** (retained general marker, per Decision 009, insufficient alone for NAT→TMP-specific claims).

Terms to avoid without additional qualification:

* 1985 pasture "origin," "initial conversion," or "starting point";
* 2020–2025 results described only as "diagnostic" when the claim concerns NAT→TMP magnitude or location;
* any statement implying the 1985 baseline is free of the kind of observation-window limitation flagged for 2020–2025.


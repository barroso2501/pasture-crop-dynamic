# Decision 023 — Review and amendments to Plan 007 (public data release and dual-manuscript pathway)

- **Status:** Accepted. Plan 007 remains "Proposed" and is amended by this decision, not superseded; Plan 007's own Stage 0 tasks are unaffected in substance.
- **Date recorded:** 2026-09-23
- **Scope:** external review of `docs/planning/007_public_release_essd_lup_submission_plan.md`, recording which of its provisions are affirmed as-is and which are amended before Stage 0 execution begins.
- **Related plan:** `docs/planning/007_public_release_essd_lup_submission_plan.md`
- **Related decisions:** 009, 010, 014–022
- **Related outputs:** none altered; this is a planning- and governance-layer review, not a computational or reporting-layer decision.

## Context

Plan 007 proposes a dual-manuscript pathway: a public, DOI-bearing, versioned data release; a data-description manuscript for *Earth System Science Data* (ESSD); and a distinct analytical and policy-facing manuscript for *Land Use Policy* (LUP), both anchored to the same released dataset version. The plan was reviewed before any Stage 0 task began, at the project's own request, following the same practice already applied to prior methodological and reporting decisions (009, 019, 020, 022): review before execution, not after.

The review found the plan's core architecture sound — separating the two manuscripts by the *kind* of contribution (data product and its fitness for reuse, versus substantive interpretation and policy contribution) rather than by splitting the five research questions across two policy-facing papers, which would have fragmented the integrated evidence synthesis built in Phase 9A/9A.1 for no clear benefit. Several provisions were identified for review; they are recorded individually below, each as affirmed, amended, or flagged as a residual risk requiring no immediate action.

This review also draws on two points the project's science lead raised directly and that bear on how the plan's findings and any related public-facing text should be phrased: (a) an explicit, calibrated statement of what audit-based review can and cannot establish about the absence of result-contingent methodological drift; and (b) confirmation that the project is not time-constrained on the ESSD stage, which changes the weight of one of the amendments below.

## Decision

### 1. Affirmed without change

The following provisions of Plan 007 are reviewed and affirmed as written, with no amendment required:

- the separation of manuscripts by contribution type (Section 1, governing principle 3: one primary manuscript home per claim, table, or figure, with citation permitted across both);
- the reciprocal distinctiveness requirement (Section 6.6: no central LUP result fully developed in the ESSD paper; Section 7.5: distinctiveness audit before LUP submission);
- the decision to push temporal-boundary and MAUP-sensitivity information into structured dataset metadata (Section 2, governing principle 7; Section 5.4, items 5–6) rather than confining it to manuscript narrative. This is a stronger design than Decision 022 itself requires — Decision 022 governs manuscript-text reporting language; Plan 007 additionally proposes encoding the same distinctions (temporal-filter-limited, right-boundary-censored, MAUP-sensitive, left-censored) as first-class, machine-readable dataset metadata. This is affirmed as a genuine improvement, not a duplication.

### 2. Amendment — the ESSD-before-LUP submission sequencing is affirmed as a deliberate choice, not a default

Plan 007, Section 3, requires the ESSD manuscript's public submission record and exact dataset citation to precede LUP submission, though final ESSD acceptance is not required. Neither ESSD's nor *Land Use Policy*'s editorial policies require this sequencing; a parallel-submission pathway, with LUP citing an active dataset DOI and an ESSD preprint or discussion-paper record under review, is an equally legitimate and commonly used pattern for companion data/analysis publications.

Because the project is not time-constrained at this stage, the sequencing in Plan 007 is affirmed, but its rationale is recorded explicitly so it is not read, later, as an editorial requirement it is not: the delay is accepted deliberately because it is inexpensive at this stage of the project and creates space for additional collaborators to form a genuine, contribution-based relationship to the work before authorship on either manuscript is finalized (see Section 5 below). If project timelines change, parallel submission remains available as a fallback without requiring any change to the data-release or ESSD-manuscript content itself.

### 3. Amendment — Stage 0/1 requires an explicit minimum-viable-release scope and time-box

Plan 007's Stage 0 and Stage 1 (Sections 4–5) specify a full research-data-engineering scope: persistent DOI outside GitHub, licensing, ORCID-linked metadata, a complete field dictionary, worked examples that install and run cleanly in a fresh environment, and a nine-part automated validation suite. This scope is substantially larger than any single prior project phase.

The project's own audit history (documented across Decisions and prior audit records) shows a recurring pattern in which documentation declares an artifact canonical before that exact artifact is delivered — resolved each time via hash verification, but recurring nonetheless across four earlier, smaller-scale instances. Stage 0/1, as currently scoped, carries materially higher exposure to the same pattern because of its size and because it has no stated minimum-defensible-release criterion; "the minimum complete set from which the scientific claims can be understood, reused, and, where feasible, reproduced" (Section 5.1) is a statement of intent, not an operational boundary.

Plan 007 should be amended to add an explicit minimum-viable-scope statement for the `v1.0.0` release candidate: which Tier 1/Tier 2 items are required for `v1.0.0` and which may be deferred to a `v1.1.0` release without blocking either manuscript submission. This does not reduce the rigor of Stage 1; it defines, in advance, what "done enough to submit" means, consistent with the same before-the-fact discipline already applied to stage-definition thresholds in Decision 009.

### 4. Amendment — authorship negotiation should run in parallel with Stage 0, not sequenced within it

Plan 007, Section 4.2, item 5, lists "confirm authorship roles separately for the dataset, ESSD manuscript, and LUP manuscript" as one Stage 0 task among technical inventory and licensing tasks. Authorship negotiation is typically the slowest and least technical element of a multi-author publication process, and the project's own stated intent — using the ESSD-stage delay to let additional collaborators form a genuine relationship to the work (Section 2 above) — depends on that negotiation starting early, not waiting on the technical inventory to complete first.

Plan 007 should be amended to list authorship and contributor-role discussion as a parallel, continuously tracked workstream starting at Stage 0 initiation, rather than a single checklist item inside it.

### 5. Clarification — the dataset, the ESSD manuscript, and the LUP manuscript may each have a distinct, non-identical author or contributor list

This is a factual clarification, not an amendment: Plan 007's own Section 4.2 (item 5) and Section 8.4 already treat dataset authorship, ESSD authorship, and LUP authorship as three separately confirmed matters, which is correct and requires no change. It is recorded here explicitly because it was raised as an open question during review.

Neither ESSD/Copernicus's publication policy and author obligations nor Elsevier's *Land Use Policy* guide for authors require an identical author list across companion manuscripts derived from the same project or dataset. ICMJE authorship criteria (substantial contribution to conception/design/data; drafting or revising; final approval; accountability) are defined per manuscript, not per project. COPE's guidance on overlapping or redundant content addresses disclosure and mutual citation between related papers — both already required by Plan 007 Sections 6.5 and 7.5 — not authorship-list consistency.

CRediT (Contributor Roles Taxonomy) statements are mandatory for *Land Use Policy*/Elsevier and not required, though not precluded, by ESSD/Copernicus. CRediT is the appropriate mechanism for documenting a case in which a contributor's role differs materially between the dataset, the ESSD manuscript, and the LUP manuscript — for example, a collaborator joining primarily for policy interpretation and discussion, without a data-curation contribution, would reasonably appear on the LUP author list without appearing on the ESSD or dataset-citation lists, provided their contribution to the LUP manuscript itself meets the applicable authorship criteria. Authorship should continue to be determined by verified contribution to each specific manuscript, not by convenience or by an invitation extended independent of actual contribution.

### 6. Calibration — what audit-based review does and does not establish about absence of result-contingent drift

The project's development process has shown a consistent pattern: analytical protocols and thresholds fixed and documented before the results they govern were produced (for example, Decision 009's requirement that empirical stage thresholds be estimated once from a declared reference population and held fixed, recorded before Phases 8–9 executed against those thresholds), and every instance in which documentation declared an artifact canonical before its delivery was resolved, via hash verification, within the same or the immediately following audit cycle, without propagating into any accepted result.

This review affirms both of those specific, verifiable observations. It does not extend to a stronger claim that no informal, result-contingent adjustment occurred upstream of what was committed to the repository. Hash and provenance auditing, as practiced throughout this project, verifies internal consistency and the resolution of declared-but-undelivered artifacts; it is not equivalent to a full research-integrity audit and cannot rule out an exploratory attempt that was adjusted after an informal look at its result and only then formally documented, since such an attempt would leave the same clean committed history as one that was not. Any manuscript, cover-letter, or data-paper text describing the project's methodological discipline should be phrased to match what has actually been verified — protocols fixed and dated before use, and a clean resolution record for every identified provenance gap — rather than an unqualified claim that no result-contingent adjustment of any kind occurred at any stage.

### 7. Numbering hygiene

Plan 007, Section 4.3, reserves `docs/decisions/023_public_release_and_dual_publication_governance.md` as a Stage 0 deliverable, to be created once release scope, claims, figures, licensing, and authorship are frozen. Because this review itself occupies decision number 023, Plan 007 should be amended to reserve `024` for that future governance decision instead, to avoid a numbering collision when Stage 0 completes.

## Rationale

- Reviewing a proposed plan before execution, and recording the review as a numbered decision, follows the same discipline already applied to methodological and reporting decisions in this project (009, 019, 020, 022): decide the rules before generating the results they will govern.
- Distinguishing affirmed provisions from amended ones, rather than issuing a general endorsement or a general rewrite, preserves Plan 007's own authorship and keeps the amendment surface minimal and auditable.
- Recording the ESSD-before-LUP sequencing as a deliberate, reasoned choice (Section 2) rather than leaving it as an unexamined default protects against it later being cited, incorrectly, as an editorial requirement of either journal.
- Recording the calibration in Section 6 protects the project's own credibility claim: an overstated claim about the absence of result-contingent drift is a more serious risk to the project's integrity narrative than a precisely bounded one.

## Consequences

### Positive consequences

- Plan 007 proceeds into Stage 0 with a recorded, auditable review rather than an informal conversation.
- The minimum-viable-scope requirement (Section 3) reduces the risk that Stage 0/1 becomes an open-ended engineering effort disconnected from either manuscript's submission timeline.
- The authorship clarification (Section 5) is available to be shared directly with prospective collaborators, reducing ambiguity as they join.

### Constraints and interpretation limits

- This decision does not alter any accepted computation, cohort definition, partition, spatial statistic, or validated numerical output; it governs planning and governance text only.
- The minimum-viable-scope statement required by Section 3 is not itself defined here; it is a required amendment to Plan 007 and remains open until Plan 007 is updated accordingly.
- This review reflects the plan and the repository state as of 2026-09-23. It should be re-checked if Plan 007 is substantially revised before Stage 0 begins.

## Alternatives considered

### Rewrite Plan 007 directly instead of recording a separate review decision

Rejected. Plan 007 was authored and proposed by the project; amending it silently would remove the record of what was originally proposed and why specific provisions were changed. A separate, numbered review decision preserves both versions and the reasoning that connects them, consistent with how prior decisions in this project have been layered rather than overwritten (e.g., Decision 020 layering onto Decision 019 rather than replacing it).

### Treat the review as informal discussion only, without a recorded decision

Rejected. The project's own established practice treats methodological and governance choices of this kind as recorded decisions specifically so that a later contributor or reviewer can trace why the plan reads as it does, without relying on conversation history that is not part of the repository.

### Require ESSD final acceptance before LUP submission

Considered and not adopted; Plan 007 already relaxes this to submission-with-public-record rather than acceptance, and this review found no reason to tighten it further.

## Implementation requirements

1. Plan 007, Section 4.3, should add a minimum-viable-scope subsection defining required-for-`v1.0.0` versus deferrable-to-`v1.1.0` items among the Tier 1/Tier 2 products.
2. Plan 007, Section 4.2, item 5, should be revised to describe authorship and contributor-role discussion as a parallel workstream starting at Stage 0 initiation, not a sequenced checklist item.
3. Plan 007, Section 4.3, should reserve `024` rather than `023` for its own future governance decision, per Section 7 above.
4. Plan 007, Section 3, should record the rationale in Section 2 above (deliberate sequencing choice, not editorial requirement) alongside the existing dependency statement.
5. Any manuscript, cover-letter, or public-facing text asserting the project's methodological discipline should be checked against the calibration in Section 6 before submission.
6. CRediT contributor-role statements should be prepared for the ESSD and LUP manuscripts as authorship for each is confirmed, per Section 5 above.

## Acceptance criteria

This decision is implemented when:

- Plan 007 is updated to reflect Implementation requirements 1–4 above;
- no accepted computation, cohort definition, partition, or validated numerical output is changed as a result of this decision;
- the numbering collision identified in Section 7 is resolved in Plan 007 before any Stage 0 deliverable is created.

## Terminology

Preferred terms:

- **minimum-viable release scope** (the required-for-`v1.0.0` subset of Tier 1/Tier 2 products, per Section 3);
- **deliberate sequencing** (the ESSD-before-LUP submission order, recorded as a reasoned choice rather than an editorial requirement, per Section 2);
- **contribution-based authorship** (authorship on each manuscript determined by verified contribution to that specific manuscript, per Section 5);
- **audit-verified discipline** (the specific, bounded claims this review affirms: protocols fixed before use, and clean resolution of every identified provenance gap) as distinct from an unqualified claim of no result-contingent adjustment (not affirmed by this review; see Section 6).

Terms to avoid without additional qualification:

- describing the ESSD-before-LUP sequencing as required by either journal's editorial policy;
- describing the absence of result-contingent methodological drift as established or proven by repository audit, rather than as consistent with what repository audit can verify;
- treating dataset, ESSD, and LUP authorship as a single list to be decided once.

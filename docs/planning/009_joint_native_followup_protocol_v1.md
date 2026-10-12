# Plan 009 — coordinated native follow-up protocol v1

Date/freeze: 2026-10-12. **Status: PREPARED, NOT EXECUTED.** This plans sections 2–4 jointly. It is not an exporter, native run or PASS record; a GEE implementation and its pilot are the next native work. Current v4.3 descriptive conclusions do not depend on completing these extensions.

## A. First observed entry versus observed re-entry

Use the accepted annual coverage, native lattice, 24,889 cells and canonical b1985 categorical origin engine. Track valid PAS observed strictly before the current confirmed entry, plus any uncertain observation strictly before entry. At a valid nonPAS→PAS entry, assign confirmed observed reentry if prior PAS exists; otherwise assign first observed entry with complete previous history if no uncertainty exists; otherwise assign prior-history uncertain. Freeze this label at entry and carry it only while the current confirmed spell continues. Never relabel a continued first spell using its own later PAS observations.

Baseline PAS in 1985 is not a dated entry. An earlier observed PAS proves reentry even if intervening gaps exist; absence of earlier PAS does not prove first-ever establishment. A gap breaks confirmed continuity and cannot create a confirmed entry without a valid nonPAS reset. An optional `confirmed_observed_nonpas_to_pas_entry_count` is a lower bound, not a complete lifetime episode count or pre1985 history flag.

Export the three entry subclasses for both PAS→TMP conversion and current entry-class PAS stock, by cell and interval. Their sums must reproduce the accepted observed-entry conversion/stock components; canonical initial/unresolved and total flow must remain unchanged. Include chronology fixtures for a continued first spell, baseline exit/reentry, repeated reentry, gap→nonPAS reset→entry, and no prior PAS with earlier uncertainty.

## B. Specific native age and event assurance

Reuse the accepted auxiliary-age update: initial=100; confirmed entry=201; confirmed continuation increments age; nonPAS/uncertain/unresolved use their explicit states without restoring initial status. Native fixtures must compare categorical state, auxiliary integer age, entry year and termination year against explicit expected histories. Include entry in 2024 and termination in 2025. Existing native categorical checks remain accepted and are not recast as scalar-only evidence.

For real pixels, use the seeded strata and caps in the JSON protocol. The pilot uses the two accepted cells, at most 20 sampled pixels per nonempty stratum; a later full-domain sample uses at most 200 per nonempty stratum. Retain sampling frame, actual support, inclusion/selection rule, pixel keys and all annual observation/mask values needed to reproduce the scalar comparison. Compare exported native states/ages/events with the documented scalar transition over the same chronology. All categorical/age/event mismatches must be exactly zero. An empty rare stratum is explicitly uncovered, not a PASS. Preserve the sample's scope; it does not prove exhaustive pixel correctness.

## C. PAS-conditioned uncertain annual pairs

For 2023/2024 and 2024/2025, classify each endpoint exclusively as observed PAS, observed valid nonPAS, NODATA, masked or unexpected. Preserve the original raster footprint and unmask convention. Export the 5×5 cross-tab by cell/pair, avoiding double counts. Define validity as both endpoints in the first two observed classes. Sum all invalid combinations to reproduce the accepted `uncertain_pair_ha` once per pair; do not sum its repeated event-type rows.

Derive invalid-pair area with an observed previous-PAS endpoint, with an observed current-PAS endpoint, and without an observed PAS endpoint. In an invalid pair the first two cannot both apply, so these categories form a partition. Endpoint-invalid types are available in the full cross-tab, without overlapping reason marginals. Compare with accepted totals: 4,688,518.25661 ha for event year 2024 and 4,688,463.67044 ha for 2025. Use the accepted tolerances (0.01 ha/cell, 0.001 ha aggregate).

The 62.568807-ha unresolved PAS→TMP origin sum for 1985–2020 is a different population from these all-class annual-pair totals. The cross-tab tests empirical PAS overlap; it does not redefine either quantity or show that uncertain pixels were never PAS. A pair-only exporter can be implemented independently using the three 2023–2025 bands, before the chronology-heavy decomposition, if that is the chosen next task.

## Execution gates and provenance

Code must preserve accepted estimands, constants, mask/footprint and all canonical data. Record exact code/constant snapshots before the pilot. Export a manifest, synthetic fixtures and support/mismatch results. Accept the pilot before scheduling full exports. Report all class partitions, zero mismatches and uncovered sample strata. Actual task counts/runtime are not claimed by this plan; they must be confirmed when the exporter is implemented. No GEE task or native PASS was produced here.

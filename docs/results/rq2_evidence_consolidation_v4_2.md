# RQ2 — evidence consolidation v4.2

**Date:** 2026-10-12. **Status:** completed documentary and numerical consolidation following native sensitivity PASS. **Scope:** P9A035 and P9A036; no new native computation or causal identification.

The current integrated evidence edition is v4.2. It incorporates the real 1985/1995/2000 observation-window sensitivity into two previously qualified findings. All 35 IDs and their order are preserved. The original 23-column schema is retained. The 33 other findings, including P9A037 and all RQ1 findings, retain every substantive field; only their common edition identifier changes. The canonical v2 source anchors, SHA-256 values and authentication flags remain unchanged for every row. Supplemental sources for the two updates are explicitly enumerated in the new inventory, so the old canonical hashes are not presented as authentication of the new sensitivity values.

## What changes scientifically

P9A035 now records observed decline under all three boundaries, unequal same-follow-up shares, and window-specific majority crossings. The 1985-window first primary crossing remains 2000–2005. The later windows cross only in separately diagnostic 2020–2025. The finding remains qualified and does not describe a process threshold or regime change.

P9A036 retains the canonical 46.91% initial / 53.09% observed-entry split for 1985–2020. It adds an explicitly separate, identical-calendar comparison for 2000–2020: initial shares 38.10%, 64.70% and 78.07% for boundaries 1985, 1995 and 2000. Thus majority attribution is conditional on the boundary. The respective first-20-year initial shares are 63.64%, 72.25% and 78.07%; their periods and denominators differ. No comparison of unequal horizons is used to claim robustness.

Both rows change robustness status from sensitivity-not-executed to `window_boundary_sensitive_full_domain_validated`. This means the specified sensitivity was run and its accounting passed; it does not mean origin composition is invariant or that the evidence became causal/unqualified. All causal flags remain zero. The first positive-conversion interval remains 100% initial by construction. Physical establishment age, first-ever pasture entry, an artifact fraction and stationary renewal are not identified.

## Append-only status record

Events-v4 preserves the entire events-v3 byte sequence and all eight historical rows, then appends two supplementary-evidence events dated 2026-10-12. These are neither suspensions nor rescissions; qualified statuses stay qualified. Older matrices, event files, errata and findings remain unchanged as dated records. The new event rows link this governing record and the consolidation validation JSON.

## Manuscript wording and scope of closure

`manuscript/results/rq2_observed_pasture_spell_origins_v4_2.md` provides complete Methods, Results and Discussion paragraphs in English for integration. No full manuscript was supplied; no claim is made that the entire paper has been edited. The canonical origin-composition image is unchanged because its numerical inputs are unchanged; the v4.2 caption adds the completed sensitivity context. The separate window-sensitivity figure remains available in PNG, SVG and PDF.

The observation-window sensitivity and its incorporation into these two conclusions are now complete. First-observed-entry/re-entry decomposition, auxiliary numerical-age 201 assurance and uncertain-pair cross-tabulation remain distinct unexecuted items. Their necessity depends on stronger claims the manuscript chooses to make; they are not relabeled as completed by this documentary closure. Public data packaging and DOI release remain the next release task and are not declared complete.

## Validation and reproducibility

Run `analysis/18g_validate_rq2_evidence_consolidation_v4_2.py`. It checks predecessor hashes, the 35-row schema/identity/order, exactly two substantive revisions, unchanged canonical anchors, retained qualified statuses and zero causal flags, exact historical-event prefix, nine source-inventory entries, accepted native sensitivity status, structured numerical claims and core manuscript wording. It reuses the real native full-domain PASS and does not reauthenticate remote Code Editor text or the original contents of the other 33 sources.

Current matrix: `outputs/summary/rq2_evidence_consolidation_v4_2/canonical_integrated_evidence_matrix_v4_2.csv`. Validation: `outputs/validation/rq2_evidence_consolidation_v4_2/canonical_rq2_evidence_consolidation_validation_v1.json`. Numerical claim map and v4.1→v4.2 field crosswalk are under the same summary directory. Source inventory: `config/rq2_evidence_v4_2_source_inventory_v1.csv`.

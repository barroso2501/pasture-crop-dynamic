# Phase 9A.2 method — TMP terminology harmonization

## Objective

Phase 9A.2 removes an ambiguous English rendering of the `TMP` class from the
current synthesis products while preserving analytical and provenance
identities.

## Inputs

The procedure reads the accepted Phase 9A.1 output directory:

```text
spatial/phase9/gap_resolution_v1
```

The acceptance JSON and every compact input used by the procedure are checked
against their frozen SHA-256 digests. The canonical matrix v2 must contain 35
unique evidence statements and no remaining evidence gaps.

## Transformation

Only the exact phrase `temporary agriculture`, matched without regard to case,
is changed in four human-readable matrix fields:

- `main_result`;
- `numeric_evidence`;
- `interpretation_boundary`;
- `source_locator`.

Lower-case prose becomes `temporary crops`; an initial capital becomes
`Temporary Crops`. The accepted matrix contains five phrase occurrences in
four fields, within P9A031, P9A033, P9A034, and P9A035. P9A033 contains two
occurrences because it reports Amazon and Cerrado separately. A different count
blocks execution.

The two Phase 9A.1 figures are regenerated from the accepted compact summaries
with corrected legend/title text. Their data are not recomputed.

## Protection rules

All non-target matrix columns must remain equivalent at the value level.
Finding order, source hashes, research-question coverage, evidence status,
diagnostic flags, and causal-claim flags must be unchanged. Technical
identifiers and the separate Other Agriculture class are protected.

## Outputs

The procedure writes to:

```text
spatial/phase9/terminology_harmonization_v1
```

Outputs include the terminology crosswalk, occurrence-level audit, matrix v3
in CSV and Markdown, coverage v3, terminology note, two corrected figures,
validation JSON, and inventory CSV.

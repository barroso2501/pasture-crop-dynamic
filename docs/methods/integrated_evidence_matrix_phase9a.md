# Phase 9A method — integrated evidence matrix

## Objective

Phase 9A creates a traceable bridge between accepted analytical outputs and
the final scientific narrative. It assembles claims; it does not estimate new
scientific quantities.

## Source snapshots

The implementation package contains 16 compact accepted records from Phases
2–8 and the governing investigation plan. Every source has a frozen SHA-256 in
`config/phase9a_source_manifest_v1.csv`. The script refuses to continue if a
source is absent or differs byte-for-byte.

The snapshots exist to make the synthesis reproducible in Colab. They do not
replace their canonical GitHub locations or external full-size products.

## Curated claim registry

`config/phase9a_evidence_claims_v1.csv` contains 30 evidence statements. Each
row is associated with one research question and one authenticated source. The
registry uses controlled values for evidence mode, status, temporal role,
robustness and manuscript use.

The matrix preserves four distinctions:

1. **primary versus diagnostic time**;
2. **descriptive versus formal spatial inference**;
3. **scientific evidence versus validation evidence**;
4. **robust, partially robust, sensitive and unassessed conclusions**.

## Automated verification

The script checks:

- source hashes and unique source identifiers;
- claim schema, identifiers and controlled vocabularies;
- representation of all five research questions;
- absence of causal claims;
- explicit RQ1 and RQ2 evidence-gap rows;
- eight Phase 2 intervals and the aggregate C–R direction;
- 96 Phase 3 distribution rows;
- accepted Phase 7 validation;
- Phase 8C aggregate, temporal and overall counts;
- Phase 8D sign, significance, magnitude and temporal decisions;
- Phase 8E overall and metric-level robustness decisions.

These checks protect against transcription drift between accepted outputs and
the synthesis registry. They do not independently reproduce the upstream
spatial statistics.

## Outputs

The stage writes:

- `canonical_integrated_evidence_matrix_v1.csv`;
- `canonical_integrated_evidence_matrix_v1.md`;
- `canonical_phase9a_evidence_coverage_v1.csv`;
- `canonical_phase9a_open_evidence_gaps_v1.csv`;
- `canonical_phase9a_source_inventory_v1.csv`;
- `canonical_phase9a_evidence_validation_v1.json`;
- `canonical_phase9a_output_inventory_v1.csv`.

The open-gap table is an analytical safeguard. It prevents absence of a
dedicated synthesis from being mistaken for absence of a process.

## Interpretation boundary

The matrix is a structured scientific index, not a meta-analysis and not a
causal model. Counts of evidence rows do not measure strength of evidence.
Final narrative priority must follow the research questions, analytical design
and magnitude of results rather than the number of rows assigned to a topic.

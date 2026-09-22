# Phase 9A.1 validation and acceptance

## Decision

The Phase 9A.1 RQ1/RQ2 gap-resolution workflow is accepted. The production run
reports `PASS`, and independent inspection of the submitted compact outputs
confirms their hashes, populations, closure checks, and evidence-matrix state.

## Authenticated inputs

| Input | SHA-256 |
|---|---|
| Full fixed-cohort GEE export | `2c6dd05d69f5851477dee856c23530d2d0f1979dcc40c6bb5d83964c4d9f755f` |
| Canonical spatial support | `22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc` |
| Accepted stock-flow derived summary | `f104c4f6ec8b50fc7c276284af9386e25d32e01f80ec2c51dfaad17f4493405e` |
| Phase 9A evidence matrix v1 | `c01d351085fecd5585d53dc9b331cfa8f1df46744dfdd8125b4f8d4a0e0f48c5` |
| Accepted pilot validation | `2ece3a65d4c5583647d412317cced4bc8decc005fecc4851eec4ea4e554c92c5` |

## Population checks

| Product | Expected | Observed | Status |
|---|---:|---:|---|
| Canonical cells | 24,889 | 24,889 | PASS |
| Reference years | 9 | 9 | PASS |
| Cell-year rows | 224,001 | 224,001 | PASS |
| Cohort-summary rows | 45 | 45 | PASS |
| Origin-interval rows | 8 | 8 | PASS |
| Pooled-origin rows | 2 | 2 | PASS |
| Evidence matrix v1 | 30 | 30 | PASS |
| Evidence matrix v2 | 35 | 35 | PASS |
| Remaining evidence gaps | 0 | 0 | PASS |

## Numerical and structural checks

All checks in `canonical_phase9_gap_resolution_validation_v1.json` are true:

- full canonical-cell population;
- correct cell-year population;
- raw endpoint-state partition closure;
- complete pasture baseline in 1985;
- exact canonical cell identity;
- fixed cohort total invariant across reference years;
- aggregate cohort-summary closure;
- interval and pooled PAS→TMP origin closure;
- authenticated Phase 9A matrix v1;
- valid 35-row matrix v2;
- RQ1/RQ2 gaps resolved;
- diagnostic 2025 endpoint included;
- no causal claim introduced.

The fixed-cohort raw export contains 106 columns. The maximum cell-level
partition residual is `1.0913936421275139e-11` ha, which is numerically zero
and well below the prespecified tolerance.

## Independent compact-output review

The submitted ZIP contains nine compact products. Every attached file listed
in the canonical inventory matches both its recorded byte count and SHA-256.
The inventory also records the cell-year Parquet and two PNG figures, which
were not included in the compact review ZIP but remain canonical Drive
products. Their omission from the review bundle is not a validation failure.

## Interpretation boundaries

- RQ1 measures endpoint-state composition of a fixed cohort, not continuous
  pixel survival or a unique transition pathway.
- RQ2 classifies pasture origin using age at interval start, not the full
  historical sequence of a pixel.
- Pooled PAS→TMP areas are interval sums and do not deduplicate pixels.
- 2025 is included and flagged as diagnostic.
- The workflow adds no spatial or causal inference.

## Acceptance status

**PASS — Phase 9A.1 is accepted and the explicit RQ1/RQ2 evidence gaps are
closed.**


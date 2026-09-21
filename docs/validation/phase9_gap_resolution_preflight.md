# Phase 9A.1 implementation preflight

## Scope

This preflight evaluates the implementation package before any production GEE
export is accepted. It does not constitute scientific acceptance of RQ1.

## Checks completed

- Python syntax compilation passed.
- JavaScript syntax checking passed.
- A synthetic 3,168-cell, 106-column pilot export passed the complete pilot
  validator and produced a standards-compliant JSON record plus inventory.
- The accepted stock-flow derived summary was located and its SHA-256 matched
  `f104c4f6ec8b50fc7c276284af9386e25d32e01f80ec2c51dfaad17f4493405e`.
- The RQ2 loader enforces eight intervals, one diagnostic interval, exact origin
  partition closure, and agreement between component areas and shares.
- The accepted RQ2 file passed authentication and produced eight interval and
  two pooled rows in the preflight environment.
- The GEE exporter defines one immutable 1985 cohort and uses exhaustive
  endpoint-state partitions for all nine reference years.
- Pilot and full filenames are distinct.
- Full processing is blocked without a `PASS` pilot record.
- The version 1 evidence matrix is preserved and authenticated before version 2
  is constructed.
- Integration against the accepted 30-row matrix produced the expected 35-row
  version 2 with unique finding identifiers and no remaining evidence gap.
- JSON serialization converts non-finite diagnostic values to `null` and forbids
  non-standard `NaN` output.

## Required runtime validation

The pilot must still verify the real GEE output for batch 00. Production
acceptance requires the full 24,889-cell export, exact cell identity with the
canonical spatial support, all population checks, all closure checks, and a
zero-gap 35-row evidence matrix.

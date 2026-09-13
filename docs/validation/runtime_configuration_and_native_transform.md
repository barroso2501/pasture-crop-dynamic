# Runtime configuration and native-transform validation

- **Status:** Passed
- **Validation date:** 2026-09-12
- **Decision:**
  `docs/decisions/007_accept_canonical_outputs_after_transform_verification.md`
- **Runtime audit script:** `gee/00_audit_runtime_configuration.js`
- **Controlled replication script:**
  `gee/00b_verify_native_transform_stock_flow_b00.js`
- **Comparison script:**
  `analysis/00_validate_runtime_configuration_and_b00.py`

## Purpose

This validation determines whether the accepted canonical Earth Engine
outputs were produced on the native MapBiomas Collection 11 coverage lattice.
It addresses a provenance question raised after `config/constants.js` was
synchronized with the hosted Earth Engine module.

The validation does not reopen the accepted accounting definitions. It tests
the runtime configuration and reproduces one previously accepted batch with
an explicit native transform.

## Expected runtime configuration

| Item | Expected value |
|---|---|
| Coverage | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3` |
| Pasture age | `projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_age_v1` |
| Analytical grid | `projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3` |
| Expected cells | 24,889 |
| CRS | `EPSG:4326` |
| Output version | `canonical-c11-coverage-v3-native-grid` |

The expected affine transform was:

```text
[0.00026949458523585647, 0, -74.02073025380652,
 0, -0.00026949458523585647, 5.405791885246045]
```

## Runtime audit

The hosted module was loaded from:

```text
users/barroso2501/pasture-crop:lib/constants
```

| Check | Result |
|---|---:|
| Audit rows | 1 |
| Audit columns | 49 |
| Configuration checks passed | 20 of 20 |
| Observed grid cells | 24,889 |
| Distinct `cell_id` values | 24,889 |
| Coverage bands | 41 |
| Pasture-age bands | 41 |
| Complete runtime configuration pass | 1 |

The runtime transform matched both the repository transform and the native
coverage transform exactly.

## Source-lattice check

Both source products report `EPSG:4326` and the same pixel dimensions. Their
native origins differ by integer numbers of pixels:

| Axis | Offset in coverage pixels | Integer-offset check |
|---|---:|---:|
| X | `75.99999999998411` | Passed |
| Y | `2204.9999999999986` | Passed |

The small deviations from exact integers are floating-point representations.
The products therefore belong to the same raster lattice; the different
stored origins do not imply a fractional-pixel displacement.

## Controlled `b00` replication

The accepted 2005-2010 stock-flow pilot was reproduced with the CRS and native
coverage transform written as literals in the verification script. All other
inputs, masks, accounting expressions, reducers, selectors, and metadata were
kept identical to the accepted pilot implementation.

| Field | Value |
|---|---|
| Task | `canonical_stock_flow_2005_2010_b00_native_transform_verification_v1` |
| Task ID | `3FBL3WCEPS4Z5BJHMVHS5THQ` |
| Status | Completed, attempt 1 |
| Start | 2026-09-12 10:48:30, UTC-03:00 |
| Runtime | 25 seconds |
| Batch compute usage | 1.3695 EECU-seconds |
| Interval | 2005-2010 |
| Batch | `source_batch_id = 0` |
| Cells | 3,168 |
| Output columns | 90 |

## Cell-by-cell comparison

The accepted and verification CSV files were sorted by `cell_id`. Seven
metadata fields were compared exactly, and all other numeric fields were
compared using a tolerance of `2e-6` ha.

| Check | Result |
|---|---:|
| Rows in each file | 3,168 |
| Columns in each file | 90 |
| Unique `cell_id` values | 3,168 |
| Metadata fields compared | 7 |
| Metadata mismatches | 0 |
| Numeric fields compared | 82 |
| Maximum absolute difference | `0.0` ha |
| Cells above tolerance | 0 |
| Columns above tolerance | 0 |

The accepted and explicit-transform exports were byte-identical:

```text
SHA-256: bad0505b70a8ed1c408edc8290d5e9c5dfca22913edd8d0447db1c12112b1636
```

## Validation artifacts

| Artifact | Dimensions | SHA-256 |
|---|---:|---|
| `canonical_runtime_configuration_audit_v1.csv` | 1 x 49 | `d45a38826f8be931e330622ac00b15f41cd96521a788fe0eac8d5687ec87b233` |
| `canonical_phase0_b00_column_comparison_v1.csv` | 82 x 7 | `93054efcdd2b653d578bd07785a0b5dc6ddf66de466fdd9937387ba65947a5e0` |
| `canonical_phase0_b00_cell_comparison_v1.csv` | 3,168 x 6 | `f4431abefcb63df05dd932c8145acce0ac97a4edf9a7de32b2e216bae5c9b590` |
| `canonical_phase0_provenance_validation_v1.json` | validation record | `9b7fe797d678c310b28390aefe09dc961bceb8d49dbb978679945ae54f8f71d0` |

The validation JSON also pins the identities of the accepted reference and
the explicit-transform replication. The complete comparison can therefore be
repeated without storing duplicate copies of both b00 CSV files in the
repository.

## Acceptance

The runtime configuration, source lattice, and explicit-transform regression
tests passed every predefined acceptance criterion. The accepted canonical
outputs are consistent with processing on the native coverage lattice.

No stock-flow or trajectory interval requires reprocessing because of the
`CRS_TRANSFORM` provenance question. This conclusion concerns configuration
and computational alignment, not source-classification accuracy.

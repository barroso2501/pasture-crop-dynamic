# Canonical Phase 8A MAUP alternative grids — production validation

## Acceptance

- **Status:** PASS — Phase 8A accepted
- **Production execution:** 2026-09-17
- **Review completed:** 2026-09-17
- **Script version:** `phase8a-maup-alternative-grids-script-v2`
- **Script SHA-256:** `d4f0287dd655936293c2f494feb1eadd827911cdf6028877d7eefd59b259b827`

Phase 8A is accepted as the canonical construction of the alternative spatial
units for the prespecified MAUP robustness analysis. No production rerun is
required.

## Authenticated input

```text
spatial/phase1/canonical_spatial_support_v1.parquet
SHA-256: 22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc
Cells: 24,889
```

The analytical footprint is the projected union of these complete canonical
cells. Its area is 497,776,400.4434 ha. No endpoint selection or process filter
was repeated for an alternative grid.

## Revision history

Revision 1 stopped during its synthetic geometry-engine verification. The
fixture contained 25 cells, whereas the shared lattice-inference function
requires at least 100. The run stopped before reading the production input and
created no analytical output.

Revision 2 changed the fixture to a 13 by 13 lattice with 169 cells. The
production algorithm, input hash, grid definitions, coordinate systems,
tolerances, paths and output schema were unchanged. The embedded engine
verification then passed before the production run.

## Lattice validation

| Quantity | Accepted value |
|---|---:|
| Canonical center spacing | 15,196.5456 m |
| Canonical side length | 8,773.7297 m |
| Implied reference area | 19,999.5575 ha |
| Median source-polygon area | 19,999.8649 ha |
| Relative side-length difference | `7.686e-06` |
| Reconstruction residual, p99 | 15.5629 m |
| Reconstruction residual, maximum | 16.9130 m |

The inferred area agrees with the 20,000-ha reference, and both residual gates
pass with wide margins.

## Grid populations and area closure

| Grid | Cells | Nominal area (ha) | Supported-area total (ha) | Relative closure difference |
|---|---:|---:|---:|---:|
| `hex10k_base` | 56,520 | 9,999.7787 | 497,776,400.4434 | `1.687e-14` |
| `hex20k_shift` | 29,396 | 19,999.5575 | 497,776,400.4434 | `2.747e-15` |
| `hex40k_base` | 15,309 | 39,999.1149 | 497,776,400.4434 | `1.177e-15` |

Every discrepancy is far below the prespecified relative tolerance of `2e-7`.
The three grids therefore represent the same fixed footprint despite their
different size and origin.

## Boundary-support diagnostics

| Grid | Cells >=25% | Area retained at 25% | Cells >=50% | Area retained at 50% | Cells >=75% | Area retained at 75% |
|---|---:|---:|---:|---:|---:|---:|
| `hex10k_base` | 52,404 | 99.13% | 49,716 | 97.11% | 47,191 | 93.95% |
| `hex20k_shift` | 27,352 | 99.24% | 25,015 | 94.96% | 22,426 | 89.33% |
| `hex40k_base` | 13,759 | 98.75% | 12,445 | 94.86% | 11,160 | 88.35% |

Very small positive fractions occur where a complete alternative hexagon only
touches a narrow part of the fixed footprint. They are expected boundary
support, not invalid geometries. Decision 014 consequently separates complete
positive-support accounting from thresholded cell-level comparison.

## Independent file review

The returned audit archive and portable spatial archive passed ZIP integrity
tests. Their five shared metadata files were byte-identical. Independent hash
calculation reproduced every SHA-256 value declared for the nine spatial
exports and the four non-self-referential audit records.

Direct GeoPackage inspection confirmed:

- 56,520, 29,396 and 15,309 feature rows;
- unique, non-null `maup_cell_id` and `maup_uid` values;
- EPSG:4326 public geometries;
- one consistent grid code and grid version per layer; and
- `geometry_valid = 1` for every record.

Direct GeoJSON feature counts matched the corresponding GeoPackages and
inventory. The production validation records the same populations for the
GeoParquet exports, whose bytes match the accepted hashes.

## Acceptance checks

All ten production checks in
`canonical_maup_grid_validation_v1.json` are true:

1. geometry-engine verification;
2. authenticated canonical source;
3. canonical source population;
4. inferred equal-area lattice;
5. reference area consistent with 20,000 ha;
6. unique grid identifiers;
7. valid generated geometries;
8. fixed-domain support closure;
9. no outcome-informed support threshold in Phase 8A; and
10. no process metric calculated in Phase 8A.

## Frozen Phase 8B handoff

- Aggregate totals use every cell with positive support.
- Primary cell-level comparisons require
  `domain_support_fraction >= 0.50`.
- Sensitivity populations use thresholds of 0.25 and 0.75.
- Partial-cell relative measures use effective supported denominators.
- Process values are extracted directly from source pixels under the canonical
  domain mask.
- Areal interpolation of canonical-cell totals is prohibited.
- The 2020–2025 interval remains included and diagnostically flagged.

Phase 8A validates geometry and analytical support. It does not yet establish
whether the ecological results are robust to scale or zoning; that conclusion
requires the restricted Phase 8B process and spatial comparisons.

# Phase 8B validation — Alternative-grid core metrics

- **Status:** PASS; accepted
- **Execution date:** 2026-09-19
- **Mode:** full
- **Script:** `analysis/13d_build_validate_maup_core_metrics_v4.py`
- **Script version:** `phase8b-build-validate-maup-core-metrics-v4`
- **Script SHA-256:** `3cdc9622ce57a7c912636f50529304daf5e722840e9a83fb02aaf68653e904fa`

## Accepted population

The execution loaded all 24 expected grid-interval exports:

| Grid | Cells per interval | Intervals | Panel rows |
|---|---:|---:|---:|
| `hex10k_base` | 56,520 | 8 | 452,160 |
| `hex20k_shift` | 29,396 | 8 | 235,168 |
| `hex40k_base` | 15,309 | 8 | 122,472 |
| **Total** | — | — | **809,800** |

The assembled panel contained no duplicate `grid_code × maup_cell_id × t0 ×
t1` keys. All 24 raw files had distinct recorded hashes and the expected grid,
interval and row population.

The accepted canonical comparison panel retained SHA-256:

```text
8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c
```

## Support validation

The fixed vector-domain area was `497,776,400.44341594 ha`.

| Grid | Mean raster support (ha) | Maximum relative vector difference | Maximum temporal spread |
|---|---:|---:|---:|
| `hex10k_base` | 497,985,589.457399 | 0.000420247 | `3.0641e-14` |
| `hex20k_shift` | 497,987,485.750167 | 0.000424056 | `3.9618e-14` |
| `hex40k_base` | 497,988,726.444958 | 0.000426549 | `1.6757e-14` |

The maximum cross-grid support spread was `6.2993e-6`. These values are below
the accepted limits of `1e-10` for within-grid temporal variation and `0.002`
for vector–raster and cross-grid geometric variation.

## Canonical-total comparison

All 72 outcome comparisons passed: three metrics for 24 grid-interval
combinations.

| Metric | Maximum relative difference | Largest share of allowed difference |
|---|---:|---:|
| Consolidation | 0.000188116 | 44.10% |
| Replenishment | 0.000055211 | 12.94% |
| `NAT → TMP` endpoint area | 0.000011506 | 2.70% |

The most restrictive case was consolidation on `hex40k_base` in 1985–1990:

```text
absolute difference = 272.7693 ha
allowed difference  = 618.4977 ha
```

No outcome approached the rejection boundary.

## Summary-table reconciliation

The compact summary contains 96 rows:

```text
3 grids × 8 intervals × 4 support scopes
```

Support populations are constant across intervals and match the accepted
Phase 8A values. The diagnostic interval contributes 12 rows, one for each
grid-scope combination.

Recalculated identities from the compact summary produced maximum residuals
of approximately `3.73e-9 ha` for net balance and `2.22e-16` for the aggregate
C–R balance index, consistent with floating-point serialization.

## Automated checks

All 14 recorded checks passed:

- raw file set complete;
- expected populations match;
- keys unique;
- metadata consistent;
- areas non-negative;
- observation partitions close;
- processes do not exceed source stocks;
- derived metric domains valid;
- raster support matches the fixed vector domain;
- raster support temporally invariant within each grid;
- cross-grid variation within geometric tolerance;
- alternative totals match canonical totals;
- diagnostic interval retained;
- support-threshold flags preserved.

## Revision history

- **Revision 1:** rejected because separately reduced endpoint support did not
  close the observed/unobserved partition against the fixed raster support.
- **Revision 2:** required the common-mask export schema; row-level partitions
  then closed, but the canonical-total threshold did not account for raster
  boundary support.
- **Revision 3:** introduced an outcome-independent vector–raster geometric
  tolerance and passed the pilot. The full run exposed an inappropriate
  cross-grid near-equality threshold.
- **Revision 4:** retained the common mask and per-grid outcome tolerance,
  replacing cross-grid near-equality with temporal invariance, vector-domain
  agreement and bounded geometric variation. The full run passed.

Only revision 4 is accepted for the complete Phase 8B production panel.

## Output identities

The compact GitHub record includes:

```text
canonical_maup_core_metric_total_comparison_v4.csv
canonical_maup_core_metric_summary_v4.csv
canonical_maup_core_metrics_validation_v4.json
canonical_maup_core_metrics_inventory_v4.csv
```

The full panel remains external:

```text
spatial/phase8/maup_metrics_v1/canonical_maup_core_metrics_panel_v4.parquet
rows: 809,800
bytes: 73,523,343
SHA-256: cdd5d4db2abb7648f8801694de93e6976d8073e271c12bd71b8c972b2a366313
```

The raw-export inventory also remains external but is authenticated in the
output inventory:

```text
canonical_maup_raw_export_inventory_v4.csv
bytes: 3,618
SHA-256: 8345148d199d5233b37985ff6bea3c7191695b07ea39a28f2ce343e2b1a421d2
```

## Acceptance statement

Phase 8B is accepted as a complete and reproducible measurement stage. No
additional Earth Engine export or validator rerun is required. The result
authorizes the comparative MAUP analysis but does not predetermine its
substantive conclusions.


# Canonical stock-and-flow panel assembly

- **Status:** Passed
- **Assembly date:** 2026-09-11
- **Last updated:** 2026-09-12
- **Assembly script:** `analysis/01_build_canonical_stock_flow_panel.py`
- **Series validation:** `docs/validation/five_year_stock_flow_series.md`
- **Method:** `docs/methods/five_year_stock_flow_panel.md`
- **Processing decision:** `docs/decisions/005_full_domain_stock_flow_processing.md`

## Purpose

This stage combines the eight independently validated five-year stock-and-flow
CSV exports into one canonical longitudinal panel. The assembly does not
derive new indicators, filter cells, or modify source measurements. It only
validates, concatenates, and orders the existing cell-interval records.

## Source exports

The panel contains the following intervals:

```text
1985-1990
1990-1995
1995-2000
2000-2005
2005-2010
2010-2015
2015-2020
2020-2025
```

Each source file contains 24,889 rows and 90 columns. The fixed set of
`cell_id` and `GRID_ID` values is identical across all intervals. The
2020-2025 records are preserved in the same schema but identified with
`diagnostic_interval = 1`.

The identity of each source file is recorded by filename, size, and SHA-256
checksum in:

```text
outputs/manifests/canonical_stock_flow_panel_manifest_v1.csv
```

## Assembly procedure

Script `analysis/01_build_canonical_stock_flow_panel.py` performs the following
operations:

1. locates the eight expected CSV files;
2. validates row and column counts;
3. checks column names and order;
4. verifies unique cell identifiers and fixed domain membership;
5. validates interval metadata and the diagnostic flag;
6. checks missing values, negative areas, accounting residuals, flow bounds,
   and the `PAS->TMP` origin partition;
7. tests stock continuity at all seven shared interval endpoints;
8. concatenates the source rows without changing their values;
9. orders the panel by `cell_id`, `t0`, and `t1`; and
10. writes the validated panel in Parquet format.

The source CSV files remain unchanged and continue to provide the primary
per-interval evidence.

## Output

The canonical consolidated panel is:

```text
canonical_stock_flow_panel_1985_2025_v1.parquet
```

The accepted Parquet file has SHA-256 checksum:

```text
2f05464b0362ac3fe17cd6f25cabc22f41674ab5c6f0e71678ad6ea2f6c6ce64
```

The full machine-readable validation record is:

```text
outputs/validation/canonical_stock_flow_panel_validation_v1.json
```

## Structural validation

| Check | Result |
|---|---:|
| Source interval files | 8 |
| Rows per interval | 24,889 |
| Columns per interval | 90 |
| Total panel rows | 199,112 |
| Distinct `cell_id` values | 24,889 |
| Duplicate cell-interval rows | 0 |
| Intervals per cell | 8 |
| Rows marked diagnostic | 24,889 |
| Missing values | 0 |
| Negative area values | 0 |
| Flow-bound violations | 0 |
| Class-27 area | 0 ha |
| Unexpected coverage area | 0 ha |

Only the 2020-2025 interval is marked diagnostic. The primary inferential
period remains 1985-2020.

## Accounting validation

The maximum absolute accounting residual across all intervals is:

```text
3.2741809263825417e-11 ha
```

No cell has an accounting residual greater than the accepted `1e-9`-ha
tolerance. All `PAS->TMP` origin partitions close, and no directed flow exceeds
its relevant origin or destination stock.

## Longitudinal continuity

For every cell and land-cover state, the final stock of one interval was
compared with the initial stock of the following interval.

| Shared year | Maximum absolute difference (ha) |
|---:|---:|
| 1990 | `3.725308e-7` |
| 1995 | `2.682209e-7` |
| 2000 | `3.352761e-7` |
| 2005 | `4.246831e-7` |
| 2010 | `4.172325e-7` |
| 2015 | `4.321337e-7` |
| 2020 | `4.246831e-7` |

The maximum difference across all shared endpoints is
`4.3213367462158203e-7` ha. No value exceeds the accepted `2e-6`-ha continuity
tolerance.

## Runtime-path note

The machine-readable validation record contains the runtime source directory:

```text
/content/drive/MyDrive/Trabalho/Contabilidade/cvs
```

The directory had previously been described as ending in `csv`. This local
folder-name difference does not affect data identity or panel validity. The
eight files were found and validated, and their identities are fixed by the
SHA-256 checksums in the manifest. The Google Drive path is an execution detail
and is not part of the canonical analytical definition.

## Interpretation boundary

The consolidated file is a balanced cell-by-interval accounting panel. It
contains endpoint stocks and directed five-year flows. It does not by itself
represent annual pixel trajectories, temporal alternation, or net balance
within a 20,000-ha cell. These quantities must remain distinct in downstream
analyses.

## Repository policy

The assembly script, manifest, validation JSON, and this validation document
should be version controlled. The large Parquet panel and the source CSV files
should remain outside GitHub. Their filenames and checksums provide the link
between external data storage and the reproducible repository workflow.

## Acceptance

The canonical panel assembly passes structural, accounting, and longitudinal-
continuity validation. The Parquet file identified by the checksum above is
accepted as the immutable input for subsequent analytical transformations.

# Validation of the integrated temporal characterization

- **Validation status:** PASS.
- **Output version:** `canonical_integrated_temporal_characterization_v1`.
- **Analysis type:** descriptive temporal characterization.
- **Domain:** combined canonical Cerrado–Amazon domain.

## Input identity

| Item | Value |
|---|---:|
| Input | `canonical_integrated_stock_flow_trajectory_1985_2025_v1.parquet` |
| SHA-256 | `7487b884ca19ad2572c7a445352cdce2b55d678ebfd80022a6155b79c2b16e28` |
| Rows | 199,112 |
| Columns | 150 |
| Cells | 24,889 |
| Intervals | 8 |

## Compact outputs

| Output | Rows | SHA-256 |
|---|---:|---|
| `canonical_integrated_temporal_summary_v1.csv` | 8 | `11c0abe72e0a7cf66f589edf408a40642192153342a91646e28fc4672c82da49` |
| `canonical_integrated_temporal_activity_classes_v1.csv` | 32 | `8afe8cbd95285f7cad794582cbd819ef5a21f22886098486fdad0a92599a09dd` |
| `canonical_integrated_temporal_balance_distribution_v1.csv` | 8 | `55c4667e7f6def21f9d750af1d32118c0c98a99f01f73720e0af9050f84c5152` |

Five figures were created in PNG and SVG. Their individual hashes remain in
the machine-readable validation JSON produced by the script.

## Checks passed

- canonical input hash and expected shape;
- unique `cell_id × t0 × t1` keys;
- complete eight-interval cell panel;
- primary/diagnostic assignment;
- nonnegative area metrics;
- gross and net C–R identities;
- pasture-year and observation-support trajectory partitions;
- exhaustive activity classes;
- complete-support composition equal to one;
- valid balance index for cells with both processes;
- creation of all declared figures.

## Boundaries

This record validates a descriptive supporting analysis. It does not establish
temporal trends, change points, biome differences, spatial autocorrelation or
causality. Its absence as a phase gate does not affect the accepted downstream
spatial products, but documenting it closes the repository traceability gap for
`analysis/05_temporal_characterization.py`.


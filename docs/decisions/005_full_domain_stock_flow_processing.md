# Full-domain stock-and-flow processing

- **Status:** Accepted
- **Date:** 2026-09-11
- **Applies to:** Canonical five-year stock-and-flow panel
- **Supersedes:** Batch processing as the default design for this stage

## Decision

Each five-year interval will be processed as one Google Earth Engine export
over the complete canonical analytical domain of 24,889 cells. The domain will
not be divided into `source_batch_id` subsets unless a future interval fails
under the full-domain configuration.

The eight intervals are:

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

The primary inferential period ends in 2020. The 2020-2025 interval will be
processed with the same schema but identified as diagnostic because the final
years of the source series do not have the same temporal filtering support as
earlier years.

## Basis

The implementation was tested in two stages:

1. a pilot export for the 3,168 canonical cells in `source_batch_id = 0`; and
2. a full-domain export for all 24,889 cells.

Both used interval 2005-2010 and produced the same 90-column schema. The full
export completed successfully in 17 minutes. Comparison of the `b00` subset
inside the full export with the pilot found identical identifiers and metadata.
The maximum numerical difference was `1.240307e-6` ha and no difference
exceeded `2e-6` ha. This magnitude is negligible relative to the approximately
20,000-ha cell area and is attributed to floating-point aggregation order.

## Accepted implementation

| Item | Accepted value |
|---|---|
| Coverage | MapBiomas Brazil Collection 11 `coverage_v3` |
| Pasture age | MapBiomas Collection 11 `pasture_age_v1` |
| Spatial domain | `grade_hex_CeAmz_canonical_c11_v3` |
| Domain size | 24,889 complete hexagonal cells |
| Spatial support | Fixed across all intervals |
| Export unit | One CSV per five-year interval |
| Rows per export | 24,889, including structural zeros |
| Raster metrics | 68 |
| Output columns | 90 |
| Batch field | Retained as provenance, not used to split routine exports |

## Failure fallback

If a particular interval cannot complete as a single task, it may be exported
by `source_batch_id` and recombined after validation. This is a computational
fallback only and does not change the analytical population, metrics, spatial
support, or output schema.

## Consequences

- The completed 2005-2010 full-domain export is the canonical result for that
  interval and must not be rerun solely to conform to a new task sequence.
- The seven remaining intervals will use the same logic and field schema.
- Process-specific subsets will be constructed only after export.
- Zero-flow cells remain observations in every interval.
- Runtime, task identifier, attempt number, and EECU use will be recorded for
  every completed export.


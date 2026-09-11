# Five-year stock-and-flow panel

- **Status:** Full-domain implementation validated for 2005-2010
- **Pilot script:** `gee/03a_reprocess_stock_flow_pilot_b00.js`
- **Validated full-domain script:** `gee/03b_reprocess_stock_flow_2005_2010_full_domain.js`
- **Configuration:** `config/constants.js`
- **Spatial domain:** `docs/methods/study_domain.md`
- **Validation:** `docs/validation/stock_flow_2005_2010.md`

## Purpose

This stage constructs the balanced cell-by-interval panel used to quantify
land-cover stocks, directed flows, and the origin of pasture converted to
temporary agriculture. It replaces historical exports conditioned on
`PAS→TMP > 0` and therefore retains structural zeros as analytical
observations.

The five-year panel is distinct from the longitudinal analysis of the fixed
1985 pasture cohort and from the annual within-interval trajectory analysis.

## Analytical population

Every interval uses the same 24,889-cell canonical domain:

```text
projects/ee-barroso2501/assets/
grade_hex_CeAmz_canonical_c11_v3
```

The complete panel will contain one row for every cell in each of the eight
five-year intervals. Process-specific subsets are defined after export and do
not alter the analytical population.

## Canonical inputs

The panel reads the final public MapBiomas Brazil Collection 11 `coverage_v3`
image and the Collection 11 pasture-age image directly. It uses the class
groups, years, CRS, affine transform, and asset identifiers maintained in
`config/constants.js`.

Raster reductions specify both `crs` and `crsTransform`. A generic
`scale: 30` is not used.

## Endpoint states

Each endpoint pixel is assigned to exactly one of nine states:

| State | Meaning |
|---|---|
| `nat` | Native vegetation |
| `pas` | Planted pasture |
| `tmp` | Temporary agriculture |
| `oag` | Mosaic and other agriculture |
| `out` | Other anthropogenic or non-focal land cover |
| `water` | Water-related classes |
| `nodata` | MapBiomas class 27 |
| `unexpected` | Unrecognized value inside the valid raster mask |
| `masked` | Pixel outside the valid raster mask |

The `unexpected` and `masked` states remain explicit so that incomplete or
unrecognized observations cannot be silently assigned to a substantive class.

## Independently measured stocks

For every state, the panel measures area at the beginning and end of each
interval:

```text
stock0_<state>
stock1_<state>
```

The nine stocks at each endpoint must sum to the rasterized complete-cell area.
The independent endpoint measurements provide checks on the transition
accounting rather than being inferred from transition sums.

The export also records complete geometry area, rasterized area, and valid
coverage area at each endpoint. These quantities remain distinct for boundary
cells whose complete hexagons extend beyond the valid MapBiomas footprint.

## Directed flows and closure

The pilot exports:

1. every destination for the three focal origins `NAT`, `PAS`, and `TMP`; and
2. flows from every auxiliary origin into the three focal destinations.

This design measures 45 unique directed flows. It is sufficient to close:

- the complete initial stocks of `NAT`, `PAS`, and `TMP`; and
- the complete final stocks of `NAT`, `PAS`, and `TMP`.

For example:

```text
stock0_pas = Σ flow_pas_<destination>
stock1_pas = Σ flow_<origin>_pas
```

The same identities apply to `nat` and `tmp`. Residuals are exported directly
for every focal-origin and focal-destination closure.

The complete 9 × 9 transition matrix is not exported because auxiliary-to-
auxiliary transitions do not contribute to closure of the three focal stocks
or to the central research questions. Omitting those 36 fields reduces raster
and export cost without conditioning or filtering the analytical population.

## Origin of pasture converted to temporary agriculture

For `PAS→TMP`, pasture age is read at the beginning of the interval, when the
pixel is still classified as pasture. The total is partitioned exhaustively as:

```text
flow_pas_tmp = pas_tmp_censored
             + pas_tmp_new
             + pas_tmp_unresolved_age
             + pas_tmp_unattributed_age
```

Definitions:

- `censored`: age code `100`;
- `new`: code greater than `200` and no greater than the maximum possible code
  at `t0`;
- `unresolved_age`: source code `1`, retained without numerical age;
- `unattributed_age`: all remaining age states, including absent or invalid
  values.

Code `1` is not interpreted as code `201` or as one-year-old pasture.

## Processing and validation design

The initial pilot used interval 2005–2010 and the 3,168 canonical cells whose
`source_batch_id` is `0`. This interval was chosen because it can exercise all
four pasture-origin components while remaining inside the primary inferential
period.

The pilot created one CSV containing all 3,168 cells. No filter based on a
positive flow was applied. It was checked for:

- row count and identifier uniqueness;
- absence of missing or negative areas;
- consistency of metadata and field structure;
- endpoint stock-to-area residuals;
- focal origin and destination closure residuals; and
- closure of the `PAS→TMP` origin partition.

The same calculation was then run as one task over all 24,889 canonical cells.
The full-domain task completed successfully and reproduced the `b00` pilot
within a maximum numerical difference of `1.240307e-6` ha. The complete
validation is recorded in `docs/validation/stock_flow_2005_2010.md`.

Each interval will therefore be exported as one complete-domain CSV with
24,889 rows and the same 90-column schema. `source_batch_id` is preserved for
provenance and regression checks, but routine stock-and-flow exports are not
split by batch. Batch subdivision remains available only as a computational
fallback.

The accepted intervals are 1985-1990, 1990-1995, 1995-2000, 2000-2005,
2005-2010, 2010-2015, 2015-2020, and 2020-2025. The last interval is flagged as
diagnostic and is excluded from the primary inferential period unless a later
decision changes that boundary.

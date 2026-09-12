# Within-interval NAT-to-TMP trajectories

- **Status:** Implemented and validated for the complete 1985-2025 series
- **Last updated:** 2026-09-12
- **Decision:**
  `docs/decisions/006_canonical_within_interval_trajectory_analysis.md`
- **Pilot script:**
  `gee/04a_reprocess_nat_tmp_trajectory_2005_2010_full_domain.js`
- **Pilot validation:**
  `docs/validation/nat_tmp_trajectory_2005_2010.md`
- **Production script:**
  `gee/04b_reprocess_nat_tmp_trajectory_remaining_intervals.js`
- **Panel assembly script:**
  `analysis/03_build_canonical_nat_tmp_trajectory_panel.py`
- **Full-series validation:**
  `docs/validation/canonical_nat_tmp_trajectory_panel_assembly.md`
- **Related endpoint accounting:**
  `docs/methods/five_year_stock_flow_panel.md`

## Purpose

This analysis decomposes the already measured five-year `NAT->TMP` endpoint
flow according to annual evidence of planted pasture during the four
intermediate years. It measures land-cover sequences hidden by five-year
endpoint comparisons without changing the validated stock-and-flow panel.

The unit exported by Google Earth Engine is a complete canonical hexagonal
cell in one five-year interval. Pixel-level annual classifications are
aggregated to area in hectares within each cell.

## Canonical inputs

| Role | Canonical source |
|---|---|
| Annual land cover | MapBiomas Brazil Collection 11 `coverage_v3` |
| Spatial domain | `grade_hex_CeAmz_canonical_c11_v3` |
| Cells per interval | 24,889 |
| Classes | `config/constants.js` |
| CRS | `EPSG:4326` |
| Affine transform | Canonical coverage transform in `config/constants.js` |
| Area unit | Hectares |

The pasture-age product is not used. This stage evaluates observed annual
land-cover states rather than pasture establishment dates.

## Endpoint population

For an interval beginning at `t0` and ending at `t1 = t0 + 5`, the pixel-level
endpoint population is:

```text
nat_tmp_endpoint = NAT at t0 AND TMP at t1
```

The four intermediate years are:

```text
t0 + 1, t0 + 2, t0 + 3, t0 + 4
```

Every canonical cell is exported even when `nat_tmp_endpoint = 0`.

## Intermediate observation support

Before classifying pasture evidence, the method checks whether all four
intermediate annual pixels are observed within the coverage raster mask.

```text
nat_tmp_mid_all_observed =
    nat_tmp_endpoint AND all four intermediate years observed

nat_tmp_mid_incomplete =
    nat_tmp_endpoint AND at least one intermediate year masked
```

The required identity is:

```text
nat_tmp_endpoint =
    nat_tmp_mid_all_observed + nat_tmp_mid_incomplete
```

Pixels with incomplete intermediate support are not silently assigned to the
no-pasture category.

## Number of intermediate pasture years

For pixels with complete intermediate observations, the method counts the
number of years classified as planted pasture:

```text
pas_year_count = sum(PAS at each of the four intermediate years)
```

The count ranges from zero to four. Five mutually exclusive bands are
exported:

```text
nat_tmp_pas_years_0_ha
nat_tmp_pas_years_1_ha
nat_tmp_pas_years_2_ha
nat_tmp_pas_years_3_ha
nat_tmp_pas_years_4_ha
```

They must satisfy:

```text
nat_tmp_mid_all_observed =
    sum(nat_tmp_pas_years_0_ha ... nat_tmp_pas_years_4_ha)
```

This distribution preserves more information than a single binary rule and
allows alternative persistence definitions to be reconstructed.

## Pasture-detection rules

### Any intermediate pasture

```text
nat_tmp_pas_any =
    nat_tmp_mid_all_observed AND pas_year_count >= 1
```

This reproduces the inclusive rule used by the historical pente-fino
analysis.

The corresponding no-pasture category is:

```text
nat_tmp_without_intermediate_pasture =
    nat_tmp_mid_all_observed AND pas_year_count = 0
```

The latter describes absence of observed pasture, not direct conversion.

### At least two pasture years

```text
nat_tmp_pas_2plus =
    nat_tmp_mid_all_observed AND pas_year_count >= 2
```

The years do not need to be consecutive. This definition is retained as a
secondary sensitivity metric.

### At least two consecutive pasture years

For intermediate years `y1`, `y2`, `y3`, and `y4`:

```text
pasture_consecutive2 =
    (PAS_y1 AND PAS_y2)
    OR (PAS_y2 AND PAS_y3)
    OR (PAS_y3 AND PAS_y4)
```

The exported area is:

```text
nat_tmp_pas_consecutive2 =
    nat_tmp_mid_all_observed AND pasture_consecutive2
```

This is the primary persistence-sensitive alternative to the inclusive rule.

The remaining inclusive pasture evidence is:

```text
nat_tmp_pas_any_nonconsecutive2 =
    nat_tmp_pas_any - nat_tmp_pas_consecutive2
```

It includes single-year pasture observations and multi-year patterns without
an adjacent pasture pair.

## Required subset relationships

Every cell and interval must satisfy:

```text
nat_tmp_pas_consecutive2
    <= nat_tmp_pas_2plus
    <= nat_tmp_pas_any
    <= nat_tmp_mid_all_observed
    <= nat_tmp_endpoint
```

The method exports explicit residuals for the main partitions. Subset
violations are checked after export.

## Reconciliation with endpoint accounting

The trajectory-derived `nat_tmp_endpoint_ha` must agree cell by cell with
`flow_nat_tmp` in the canonical stock-and-flow panel for the same interval.

This comparison is performed after export because the stock-and-flow panel is
stored outside Google Earth Engine. The accepted numerical tolerance is:

```text
2e-6 ha per cell
```

Agreement demonstrates that the trajectory analysis decomposes the same
endpoint population. It does not create additional endpoint area.

## Output fields

The pilot exports identifiers and metadata:

```text
cell_id
GRID_ID
source_batch_id
t0
t1
interval
output_version
diagnostic_interval
intermediate_years
geometry_area_ha
```

The raster-derived area fields are:

```text
nat_tmp_endpoint_ha
nat_tmp_mid_all_observed_ha
nat_tmp_mid_incomplete_ha
nat_tmp_pas_years_0_ha
nat_tmp_pas_years_1_ha
nat_tmp_pas_years_2_ha
nat_tmp_pas_years_3_ha
nat_tmp_pas_years_4_ha
nat_tmp_pas_any_ha
nat_tmp_pas_2plus_ha
nat_tmp_pas_consecutive2_ha
nat_tmp_pas_any_nonconsecutive2_ha
raster_area_ha
```

The exported audit fields are:

```text
residual_endpoint_observation_partition
residual_pas_count_partition
residual_pas_any_partition
residual_pas_2plus_partition
residual_pas_consecutive_partition
```

The pilot therefore contains 28 columns.

## Validation sequence

The first execution used the complete 24,889-cell domain for 2005-2010. It was
accepted after checking:

1. 24,889 rows and unique identifiers;
2. no missing or negative area values;
3. correct interval metadata;
4. all five exported residuals within `1e-9` ha;
5. all subset relationships;
6. zero or explicitly quantified incomplete intermediate support;
7. cell-level agreement with canonical `flow_nat_tmp` within `2e-6` ha; and
8. consistency of the inclusive-rule magnitude with the historical result,
   treated only as a diagnostic comparison.

All structural, accounting, subset, and external-reconciliation checks passed.
The historical magnitude was not reproduced, but this was not an acceptance
criterion because the historical analysis used a preliminary coverage source
and a different analytical domain. The diagnostic difference is recorded in
`docs/validation/nat_tmp_trajectory_2005_2010.md` and was subsequently found
in all eight intervals.

## Implementation status

The 2005-2010 pilot provided the validated implementation reference. The
remaining seven intervals were subsequently processed with the same:

- canonical inputs and spatial alignment;
- complete 24,889-cell population;
- 28-column output schema;
- inclusive, two-or-more-year, and consecutive-two-year rules;
- incomplete-observation treatment;
- residual fields; and
- cell-level reconciliation against canonical `flow_nat_tmp`.

The eight exports were assembled into a balanced panel with 199,112
cell-interval records. The panel passed structural, partition, subset, support,
and external-reconciliation checks. Its canonical SHA-256 is:

```text
c888ff6403a0c39065bdfa3eb25bbd2146fe8b4c12aade7a070a4c08181803b9
```

The primary inferential period ends in 2020. The complete and technically
equivalent 2020-2025 interval remains in the panel with
`diagnostic_interval = 1`.

Across the full 1985-2025 panel, the inclusive rule identifies 832,251.332 ha
and the consecutive-two-year rule identifies 790,529.151 ha. The latter is
94.987% of the inclusive area. The difference between the two-or-more-year and
consecutive-two-year definitions is only 196.528 ha across the complete
series.

These results show that the temporal pattern is not materially sensitive to
whether multi-year pasture observations must be consecutive. The inclusive
rule remains the sensitive definition, while the consecutive-two-year rule
remains the persistence-sensitive robustness definition. Final designation of
one rule as the primary manuscript measure will be made during integrated
scientific analysis rather than during data validation.

## Interpretation

`nat_tmp_pas_any_ha` measures endpoint `NAT->TMP` pixels with at least one
intermediate annual pasture observation. It is sensitive to brief pasture
phases and isolated annual classifications.

`nat_tmp_pas_consecutive2_ha` requires stronger temporal persistence but may
exclude genuine pasture phases shorter than two annual observations. The
difference between the two measures quantifies sensitivity to the persistence
rule. Neither rule is assumed to be error-free.

Absence of intermediate pasture does not demonstrate direct conversion. Other
states and unobserved transitions may occur within the interval. The analysis
does not infer causal drivers or management intention.

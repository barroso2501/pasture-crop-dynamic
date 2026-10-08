# RQ1 fixed-1985 pasture cohort — revalidation v1

**Record date:** 2026-10-08.  
**Status:** PASS for the RQ1 fixed-baseline cohort revalidation gate.  
**Governing decision:** Decision 024, pasture-age source remediation.  
**Validator:** `analysis/17w_revalidate_fixed_1985_pasture_cohort_v1.py`.  
**Decision 024 overall:** remains open.  
**Evidence status:** P9A035–P9A037 remain suspended pending criterion 12 and a versioned evidence/status review.

## Purpose and population

The revalidation checks the existing RQ1 fixed cohort against the independently accepted coverage-only PAS stock at 1985. The cohort comprises pixels satisfying `coverage_1985_is_pas_and_pasture_age_1985_equals_100` in the original 15b export. Membership stays fixed even when a pixel later leaves pasture or returns. A later return can be a new observed pasture spell in RQ2 without changing that pixel's membership in the RQ1 baseline cohort.

The original export is retained unchanged. No new GEE processing or native-pixel resampling was performed for this gate. Source age codes do not determine corrected post-1985 pasture-spell origin.

| Population or area | Accepted result |
| --- | ---: |
| Canonical domain cells | 24,889 |
| Cells with positive fixed-cohort area | 16,421 |
| Fixed-cohort area | 49,035,870.567182116 ha |
| Reference years | 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025 |
| Reproduced summary rows | 45 |

The 45 rows represent nine dates and five reporting strata: combined domain; primary-biome assignment to Amazon or Cerrado; and sensitivity excluding Amazon–Cerrado transbiome cells for each primary biome. Sensitivity rows are subsets, not additional areas to add to the combined domain.

| Reporting stratum | Cells | Fixed-cohort area (ha, rounded) |
| --- | ---: | ---: |
| Combined domain | 24,889 | 49,035,870.567 |
| Amazon, primary assignment | 14,213 | 7,747,336.725 |
| Cerrado, primary assignment | 10,676 | 41,288,533.842 |
| Amazon, nontransbiome sensitivity | 13,920 | 7,252,775.615 |
| Cerrado, nontransbiome sensitivity | 10,387 | 40,990,102.191 |

## Accepted execution and checks

The submitted full-domain Colab execution reports `status: PASS` and `rq1_fixed_cohort_baseline_revalidated: true`. The validator authenticates six prespecified input SHA-256 values, checks the accepted Phase 9 full PASS and its cohort/summary references, and authenticates the annual source-age audit summary through its full-domain PASS JSON.

The checks compare `cohort_total_ha` against `stock0_pas` by `cell_id` in both the original 1985–1990 stock-flow CSV and the corrected panel v2. They also validate cohort schema and metadata, cell populations, spatial strata, all nine per-cell state partitions, and reproduction of the 45 accepted summary rows. The nine states are NAT, PAS, TMP, OAG, OUT, water, nodata, unexpected, and masked. The source-audit record reports zero raw age-code-1 area in 1985.

| Comparison or closure | Maximum absolute difference |
| --- | ---: |
| Per-cell cohort versus original PAS-1985 stock | 2.682209014892578e-7 ha |
| Per-cell cohort versus corrected panel v2 PAS-1985 stock | 2.6822272047866136e-7 ha |
| Original versus corrected PAS-1985 stock | 3.637978807091713e-12 ha |
| Per-cell state-partition closure | 1.0913936421275139e-11 ha |
| Per-cell reported state total versus fixed cohort | 1.0913936421275139e-11 ha |
| Reproduced summary state areas | 4.842877388000488e-8 ha |
| Reproduced summary state shares | 6.661338147750939e-16 |

These differences are negligible relative to the prespecified area tolerance of 0.001 ha and share tolerance of 1e-9. The fixed area and population of each reporting stratum are constant across the nine dates. Only the 2025 endpoint carries `diagnostic_endpoint = 1`; its diagnostic status is retained.

A separate review of the submitted ZIP confirmed the comparison CSV's SHA-256, agreement of the six prespecified input hashes with the recovered validator, 45 unique stratum/year keys, five strata per year, constant stratum areas and cell populations, diagnostic flags, and agreement of the JSON maxima with the CSV. The complete input datasets were not included in that ZIP, so this review did not independently rerun all per-cell comparisons. Their PASS is supplied by the authenticated-input Colab execution report.

## Accepted artifacts and provenance

| Repository artifact | SHA-256 |
| --- | --- |
| `outputs/summary/fixed_1985_cohort_revalidation_v1/canonical_fixed_1985_cohort_revalidation_comparison_v1.csv` | `0e725601dfb58fb65f7ee026b84ce99dd3b3a8127f314c714d1526d96ccdf306` |
| `outputs/validation/fixed_1985_cohort_revalidation_v1/canonical_fixed_1985_cohort_revalidation_validation_v1.json` | `4a9864dcfed4203d192da742c8f9219d25809b4e34377d6a5c0c5559430396be` |
| `analysis/17w_revalidate_fixed_1985_pasture_cohort_v1.py` | `ad04154abcac1231de33365f51e6b8fccbe9e62c5f75e78b0cd6792b0f585528` |

The JSON contains the complete eight-file input hash inventory. These are the six pinned references plus the source-audit validation and annual summary. Input locations relative to `MyDrive` are:

| Input | Location |
| --- | --- |
| Original fixed-cohort export | `pasture_crop_dynamic_canonical/canonical_fixed_1985_pasture_cohort_states_full_v1.csv` |
| Original stock-flow baseline | `Trabalho/Contabilidade/csv/canonical_stock_flow_1985_1990_full_v1.csv` |
| Corrected panel v2 | `Trabalho/Contabilidade/panel/canonical_stock_flow_panel_1985_2025_v2.parquet` |
| Spatial support | `Trabalho/Contabilidade/spatial/phase1/canonical_spatial_support_v1.parquet` |
| Accepted Phase 9 validation | `Trabalho/Contabilidade/spatial/phase9/gap_resolution_v1/canonical_phase9_gap_resolution_validation_v1.json` |
| Accepted fixed-cohort summary | `Trabalho/Contabilidade/spatial/phase9/gap_resolution_v1/canonical_fixed_1985_pasture_cohort_summary_v1.csv` |
| Full source-age audit validation | `Trabalho/Contabilidade/spatial/phase9/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_validation_v1.json` |
| Full source-age audit annual summary | `Trabalho/Contabilidade/spatial/phase9/pasture_age_source_audit_v1/canonical_pasture_age_source_audit_annual_v1.csv` |

The validator writes its two products under `Trabalho/Contabilidade/spatial/phase9/fixed_1985_cohort_revalidation_v1/`. The CSV and JSON in the repository are byte-identical copies of the submitted outputs. The script hash above identifies the recovered and delivered source file; the submitted JSON does not independently record the hash of the Python file actually executed in Colab.

Related records: [source-age audit methods](../methods/pasture_age_source_asset_audit.md) and [Decision 024 criterion-11 validation](pasture_age_source_asset_impact_audit_v1.md).

## Interpretation and remaining gate

Accept this result as revalidation of the unchanged original cohort export, area-equivalent baseline membership per canonical cell under the original subset mask, and the existing nine-date endpoint summaries. This supports retaining the RQ1 fixed-cohort composition results within that scope.

The area comparison does not independently reobserve or identify every source pixel. Endpoint compositions do not establish continuous pasture persistence, a survival curve, annual alternation, or paths between reference dates. A return to PAS does not imply that the pixel remained continuously in PAS since 1985. This gate does not resolve the official source-product semantics or reinstate age-dependent RQ2 findings.

Decision 024 remains open. Criterion 12 requires a final, versioned review of the evidence and finding statuses. P9A035–P9A037 remain suspended; historical evidence files and suspension events are preserved. Do not create a reinstatement/rescission event on the basis of this RQ1 gate alone.

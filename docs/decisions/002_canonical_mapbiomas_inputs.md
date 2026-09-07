# Decision 002 — Canonical MapBiomas inputs

- **Status:** Accepted
- **Date recorded:** 2026-09-07
- **Scope:** Source data, classification, and mandatory reprocessing
- **Related method:** `docs/methods/data_sources_and_classification.md`
- **Related configuration:** `config/constants.js`

## Context

The exploratory analysis was developed before the official release of MapBiomas Brazil Collection 11. It used the working `classification-ft` asset with version `0-4-13-w3y-5`.

The final public Collection 11 coverage product is now available. Scientific outputs intended for peer review must be generated from the stable public source rather than from a pre-release working asset, even when substantive changes in the results are not expected.

The pasture-age asset, class-code lists, and native pixel grid used in the exploratory analysis have been confirmed as appropriate for the reconstructed workflow.

## Decision

The canonical annual land-cover source is:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_coverage_v3
```

The canonical pasture-age source is:

```text
projects/mapbiomas-public/assets/brazil/lulc/collection11/
mapbiomas_brazil_collection11_pasture_age_v1
```

The public coverage asset will be loaded directly as an `ee.Image`. Canonical scripts will not filter or mosaic the historical `classification-ft` collection.

All calculations previously based on `classification-ft` version `0-4-13-w3y-5` must be rerun with `mapbiomas_brazil_collection11_coverage_v3`.

## Confirmed conventions

- The coverage and pasture-age products use the same native pixel grid.
- Annual coverage bands use `classification_<year>`.
- The reference years are 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, and 2025.
- The primary inferential period ends in 2020.
- The 2020–2025 interval is retained for diagnosis but not for the main conclusions.
- Pasture-age value `100` identifies pasture present in 1985.
- Pasture-age values `2xx` represent `200 + age in years`.
- The canonical class-code lists are definitive for the current analysis.
- No valid Collection 11 class code is known to be absent from the remapping scheme.
- Canonical area reductions use the native CRS transform rather than only `scale: 30`.

## Rationale

This decision ensures that:

- the analysis is based on a public and citable data product;
- collaborators and reviewers can access the same source;
- the repository does not depend on a mutable or inaccessible working asset;
- the source image does not require unnecessary mosaicking;
- all scripts use a common classification and spatial alignment;
- manuscript values can be traced to a stable Collection 11 release.

Reprocessing is required as a matter of provenance and reproducibility, not because a particular direction or magnitude of change is expected.

## Consequences

### Required actions

The following products must be regenerated:

1. the fixed-domain verification if its endpoint calculations used the working asset;
2. five-year stock and flow accounting;
3. pasture-origin decomposition of `PAS→TMP`;
4. the fixed 1985 pasture-cohort trajectory;
5. annual within-interval trajectory measurements;
6. coverage–pasture-age agreement diagnostics;
7. spatial metrics, MAUP tests, and spatial autocorrelation;
8. manuscript tables, figures, maps, and reported values.

### Status of historical outputs

Historical outputs remain useful as regression references. They are not authoritative results and must not be combined with outputs from the canonical source in final summaries.

### Expected comparison

No major substantive change is expected. Nevertheless, differences will be quantified by interval and, where possible, by cell. Agreement must be demonstrated rather than assumed.

### Terminological consequence

Pasture-age code `100` will be described primarily as the **initial pasture stock present in 1985**. The establishment date of this cohort is left-censored; it will not be assigned a more precise age than the data support.

## Alternatives considered

### Retain the pre-release working asset

Rejected because it is not the stable public reference for Collection 11 and would weaken reproducibility and source traceability.

### Treat existing results as final because changes are expected to be small

Rejected. Expected similarity is not evidence of identity, and peer-reviewed results must derive from the official product.

### Mix historical and canonical outputs

Rejected because even small source differences could make tables, figures, and accounting identities internally inconsistent.

### Reprocess only headline results

Rejected because validation, spatial analysis, and secondary results depend on the same source and must remain internally coherent.

## Acceptance criteria

This decision is fully implemented when:

- no canonical script references the historical `classification-ft` asset;
- all canonical scripts import parameters from `config/constants.js` or an exact synchronized Earth Engine module;
- source-band and projection audits pass;
- the fixed analytical domain has been verified against the final coverage product;
- all analytical outputs have been regenerated;
- new and historical outputs have been compared quantitatively;
- every manuscript value can be traced to an output generated from `coverage_v3`;
- historical files are clearly labeled and separated from canonical outputs.

## Superseded configuration

The historical value:

```javascript
exports.VERSAO = '0-4-13-w3y-5';
```

and the use of:

```text
projects/mapbiomas-brazil/assets/LAND-COVER/COLLECTION-11/
INTEGRATION/classification-ft
```

are superseded for all future project processing.


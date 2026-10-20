> Historical status/instructions. On 2026-10-20 the targeted audit was accepted; no rerun is needed. Current: [acceptance record](../validation/pasture_v2_targeted_domain_audit_acceptance_v1.md).

# Pasture-age v2: rejected all-null return and real-geometry preflight v3

Date: 2026-10-20. Native v3 status: **PENDING**. No scientific closure.

## Observed evidence

The supplied `pasture_v2_coverage_recheck82_20261020143416_v2_1.csv` has the exact 82 expected identities and passing native synthetic fixtures. Each row has `reducer_missing_count=26`; all calculated output cells contain the explicit -9999 failure sentinel. This is 2,132 missing reductions. Raw dictionaries omit the numerical values while the property-name inventory contains their expected names. The constant `native_grid_support` output is also null. This establishes failed real-region reduction, not age-code absence and not a missing selector-name problem.

The unchanged input is archived under `outputs/native/pasture_v2_coverage_recheck82_v2_1/rejected_20261020143416/`. Its SHA-256 is `b4ed7b512d1dba36d3abf0c585d0dee3d463f93990a1ee1623af32890e1d0317`. The adjacent structured rejection record supplies the same count and status. The v1 rejection and v2 synthetic stop remain historical evidence.

## Interpretation and intervention

The pattern is consistent with a documented filtered-table/image-footprint intersection issue. This is an inference, not a reproduced backend diagnosis. Earth Engine developer Noel Gorelick has described `.limit()` materialization and finite image clipping as workarounds in first-hand reports:

- https://gis.stackexchange.com/questions/478174/reduceregion-works-but-reduceregions-returns-null-values-for-all-reducer
- https://gis.stackexchange.com/questions/407965/null-value-after-reduceregions-in-gee

Official guidance also documents mapping `reduceRegion` over features as an alternative to `reduceRegions`: https://developers.google.com/earth-engine/guides/best_practices . API: https://developers.google.com/earth-engine/apidocs/ee-featurecollection-limit .

V3 materializes only the 82 selected geometries using `limit(82).toList(82)`, rejects nonpositive geometry areas, and clips the image to a buffered bounding window containing all cells. The 1 km buffer avoids clipping cell-edge support. It compares direct and collection reductions on the lexicographically first selected audit ID (`000000000000000002b2`, IC-201, cell_id 5045) before defining the export task. All 26 outputs must be finite numbers and constant support must equal 1. A successful method must reproduce the parent unknown-coverage flag. Both complete methods must agree exactly; direct reduction is preferred. Failed methods are recorded, not converted to zeros. If neither works or they disagree, the script stops.

The selected production method, both diagnostic dictionaries, finite-window coordinates and per-cell geometry area are exported. The validator requires the checked cell to reproduce its preflight values and rejects missing reductions anywhere in the 82-cell export. A single successful preflight is not claimed to validate the other 81 cells; subsequent CSV validation is mandatory.

The temporal engine, annual bands, native transform, cell selection and 39-code coverage policy are unchanged. Only the real-geometry reduction path, verification and transport metadata change. No full-domain rerun or source migration is requested. Eight accepted input CSVs and their recorded hashes remain unchanged. Matrix v4.3, cumulative events-v5 and accounting results remain unchanged.

## Assurance

Software-only checks: 14 original scalar cases, 3 additional scalar cases, 5 method-selection scenarios, structural guards and 17 validator integration tests pass. Temporary synthetic CSVs are not delivered as native evidence. The v3 script has not been executed in GEE here. No operator execution-text hash is asserted.

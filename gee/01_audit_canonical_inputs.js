/**
 * 01_audit_canonical_inputs.js - version 3
 *
 * Structural audit of the canonical MapBiomas Collection 11 inputs and the
 * analytical grid used by pasture-crop-dynamic.
 *
 * This version uses the native Collection 11 coverage transform defined in
 * lib/constants.js. Heavy checks run only as batch exports.
 *
 * Batch outputs:
 *   1. canonical_input_audit_c11_v3_native_grid_domain.csv
 *   2. canonical_endpoint_rule_c11_v3_native_grid_by_cell.csv
 *   3. canonical_low_age_codes_c11_v3_native_grid.csv
 */

// ---------------------------------------------------------------------------
// 0. Import canonical constants
// ---------------------------------------------------------------------------

var K = require(
  'users/barroso2501/pasture-crop:lib/constants.js'
);

// ---------------------------------------------------------------------------
// 1. Audit parameters
// ---------------------------------------------------------------------------

var AUDIT_YEARS = K.MARK_YEARS;

// Conservative rectangle containing the complete retained hexagons.
// The domain mask limits all domain summaries to selected cells.
var PROCESSING_REGION = ee.Geometry.Rectangle([
  -75, -25, -40, 7
]);

var DRIVE_FOLDER = 'pasture_crop_dynamic_audits';

var SUMMARY_PREFIX =
  'canonical_input_audit_c11_v3_native_grid_domain';

var ENDPOINT_PREFIX =
  'canonical_endpoint_rule_c11_v3_native_grid_by_cell';

var LOW_AGE_PREFIX =
  'canonical_low_age_codes_c11_v3_native_grid';

var ENDPOINT_TOLERANCE_HA = 0.01;

var TRANSFORM_TEXT = K.CRS_TRANSFORM.join(',');

// ---------------------------------------------------------------------------
// 2. Canonical inputs
// ---------------------------------------------------------------------------

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);

var pixelAreaHa = ee.Image.pixelArea()
  .divide(K.SQUARE_METRES_PER_HECTARE);

// Raster representation of the complete retained-cell union.
var domainMask = ee.Image(0)
  .byte()
  .paint(grid, 1)
  .selfMask()
  .rename('analytical_domain');

var domainMaskZero = domainMask.unmask(0);

// ---------------------------------------------------------------------------
// 3. Helper functions
// ---------------------------------------------------------------------------

function inCodes(image, codes) {
  var result = image.eq(codes[0]);

  for (var i = 1; i < codes.length; i++) {
    result = result.or(image.eq(codes[i]));
  }

  return result;
}

function domainAreaBand(mask, name) {
  return pixelAreaHa
    .multiply(domainMaskZero)
    .multiply(ee.Image(mask).unmask(0))
    .rename(name);
}

function unrestrictedAreaBand(mask, name) {
  return pixelAreaHa
    .multiply(ee.Image(mask).unmask(0))
    .rename(name);
}

function reduceDomainAreaBands(image) {
  return image.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: PROCESSING_REGION,
    crs: K.CRS,
    crsTransform: K.CRS_TRANSFORM,
    maxPixels: 1e13,
    tileScale: 16
  });
}

// ---------------------------------------------------------------------------
// 4. Lightweight console audit: source and band structure
// ---------------------------------------------------------------------------

var expectedCoverageBands = ee.List.sequence(
  K.FIRST_YEAR,
  K.LAST_YEAR
).map(function(year) {
  var yearText = ee.Number(year).format('%d');

  return ee.String(K.COVERAGE_BAND_PREFIX).cat(yearText);
});

var coverageBands = coverage.bandNames();
var ageBands = pastureAge.bandNames();

print('AUDIT 1A - Coverage asset:', K.COVERAGE_ASSET);
print('AUDIT 1B - Coverage band count (expected 41):',
  coverageBands.size());
print('AUDIT 1C - Missing coverage bands (expected empty):',
  expectedCoverageBands.removeAll(coverageBands));
print('AUDIT 1D - Unexpected coverage bands (expected empty):',
  coverageBands.removeAll(expectedCoverageBands));
print('AUDIT 1E - Pasture-age asset:', K.PASTURE_AGE_ASSET);
print('AUDIT 1F - Pasture-age band count (expected 41):',
  ageBands.size());
print('AUDIT 1G - Pasture-age bands:', ageBands);

// ---------------------------------------------------------------------------
// 5. Lightweight console audit: spatial-reference metadata
//
// Earth Engine returns projection.transform() as WKT text for these assets.
// Therefore, this script prints the source metadata but does not attempt to
// convert the WKT to an ee.List.
//
// The preceding audit established that coverage and pasture age have equal
// pixel sizes and origins separated by exactly 76 columns and 2,205 rows.
// They therefore share the same native pixel lattice.
// ---------------------------------------------------------------------------

var coverageProjection = coverage
  .select(K.coverageBandName(K.FIRST_YEAR))
  .projection();

var ageProjection = pastureAge
  .select([0])
  .projection();

print('AUDIT 2A - Coverage CRS:', coverageProjection.crs());
print('AUDIT 2B - Pasture-age CRS:', ageProjection.crs());
print('AUDIT 2C - Coverage native projection:', coverageProjection);
print('AUDIT 2D - Pasture-age native projection:', ageProjection);
print('AUDIT 2E - Coverage nominal scale (m):',
  coverageProjection.nominalScale());
print('AUDIT 2F - Pasture-age nominal scale (m):',
  ageProjection.nominalScale());
print('AUDIT 2G - Canonical processing CRS:', K.CRS);
print('AUDIT 2H - Canonical processing transform:', K.CRS_TRANSFORM);
print('AUDIT 2I - Spatial alignment decision:',
  'PASS: same lattice; coverage native transform is canonical.');

// ---------------------------------------------------------------------------
// 6. Lightweight console audit: retained-grid integrity
// ---------------------------------------------------------------------------

var gridWithArea = grid.map(function(feature) {
  var geometryAreaHa = feature
    .geometry()
    .area(1)
    .divide(K.SQUARE_METRES_PER_HECTARE);

  return feature.set('geometry_area_ha', geometryAreaHa);
});

var gridSize = grid.size();
var uniqueIdCount = grid.aggregate_count_distinct(K.CELL_ID_FIELD);

print('AUDIT 3A - Grid asset:', K.ANALYTICAL_GRID);
print('AUDIT 3B - Cell count:', gridSize);
print('AUDIT 3C - Expected cell count:',
  K.EXPECTED_ANALYTICAL_CELL_COUNT);
print('AUDIT 3D - First-cell property names:',
  grid.first().propertyNames());
print('AUDIT 3E - Configured ID field:', K.CELL_ID_FIELD);
print('AUDIT 3F - Distinct cell ID count:', uniqueIdCount);
print('AUDIT 3G - Cell ID is unique (1 means yes):',
  gridSize.eq(uniqueIdCount));
print('AUDIT 3H - First geometry type:',
  grid.first().geometry().type());
print('AUDIT 3I - Cells intersecting processing region:',
  grid.filterBounds(PROCESSING_REGION).size());
print('AUDIT 3J - Geometry area statistics in hectares:',
  gridWithArea.aggregate_stats('geometry_area_ha'));

// ---------------------------------------------------------------------------
// 7. Batch export 1: coverage-age agreement in the retained domain
// ---------------------------------------------------------------------------

var expectedCodes = ee.List(K.expectedSourceCodes());
var expectedTargets = ee.List.repeat(1, expectedCodes.size());

function auditYear(year) {
  var coverageBandName = K.coverageBandName(year);
  var pastureAgeBandIndex = K.ageBandIndex(year);

  var cov = coverage.select(coverageBandName);
  var age = pastureAge
    .select([pastureAgeBandIndex])
    .rename('age');

  var covValid = cov.mask().gt(0);
  var ageValue = age.unmask(0);
  var ageValid = ageValue.gt(0);

  var isPasture = cov
    .eq(K.CLASS_CODES.PAS[0])
    .and(covValid);

  var isNoData = inCodes(cov, K.CLASS_CODES.NODATA)
    .and(covValid);

  var isExpectedCode = cov
    .remap(expectedCodes, expectedTargets, 0)
    .eq(1)
    .and(covValid);

  var isUnexpectedCode = covValid.and(isExpectedCode.not());

  var isInitialAge = ageValue.eq(
    K.PASTURE_AGE_INITIAL_STOCK_CODE
  );

  var isNewAge = ageValue.gt(K.PASTURE_AGE_OFFSET);

  var isAge1To99 = ageValue
    .gte(1)
    .and(ageValue.lte(99));

  var isAge101To200 = ageValue
    .gte(101)
    .and(ageValue.lte(200));

  var isOtherPositiveAge = ageValid
    .and(isInitialAge.not())
    .and(isNewAge.not());

  var expectedMaximumAgeCode = K.PASTURE_AGE_OFFSET +
    (year - K.FIRST_YEAR);

  var isAboveExpectedMaximum = ageValue.gt(
    expectedMaximumAgeCode
  );

  var bands = ee.Image.cat([
    domainAreaBand(ee.Image.constant(1), 'domain_pixel_area_ha'),
    domainAreaBand(covValid, 'coverage_valid_ha'),
    domainAreaBand(isNoData, 'coverage_nodata_ha'),
    domainAreaBand(isUnexpectedCode, 'coverage_unexpected_code_ha'),
    domainAreaBand(isPasture, 'coverage_pasture_ha'),
    domainAreaBand(isPasture.and(ageValid), 'pasture_with_age_ha'),
    domainAreaBand(isPasture.and(ageValid.not()), 'pasture_without_age_ha'),
    domainAreaBand(
      ageValid.and(covValid).and(isPasture.not()),
      'age_outside_pasture_ha'
    ),
    domainAreaBand(
      isPasture.and(isInitialAge),
      'pasture_age100_ha'
    ),
    domainAreaBand(
      isPasture.and(isNewAge),
      'pasture_age2xx_ha'
    ),
    domainAreaBand(
      isPasture.and(isOtherPositiveAge),
      'pasture_other_positive_age_ha'
    ),
    domainAreaBand(
      isPasture.and(isAge1To99),
      'pasture_age1_99_ha'
    ),
    domainAreaBand(
      isPasture.and(isAge101To200),
      'pasture_age101_200_ha'
    ),
    domainAreaBand(
      isPasture.and(isAboveExpectedMaximum),
      'age_above_expected_max_ha'
    )
  ]);

  var summary = ee.Dictionary(reduceDomainAreaBands(bands));

  return ee.Feature(null, summary)
    .set('year', year)
    .set('coverage_band', coverageBandName)
    .set('pasture_age_band_index', pastureAgeBandIndex)
    .set('expected_maximum_age_code', expectedMaximumAgeCode)
    .set('coverage_asset', K.COVERAGE_ASSET)
    .set('pasture_age_asset', K.PASTURE_AGE_ASSET)
    .set('grid_asset', K.ANALYTICAL_GRID)
    .set('processing_crs', K.CRS)
    .set('processing_transform', TRANSFORM_TEXT)
    .set('output_version', K.OUTPUT_VERSION);
}

var annualAudit = ee.FeatureCollection(
  AUDIT_YEARS.map(auditYear)
);

Export.table.toDrive({
  collection: annualAudit,
  description: SUMMARY_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: SUMMARY_PREFIX,
  fileFormat: 'CSV',
  selectors: [
    'year',
    'coverage_band',
    'pasture_age_band_index',
    'expected_maximum_age_code',
    'domain_pixel_area_ha',
    'coverage_valid_ha',
    'coverage_nodata_ha',
    'coverage_unexpected_code_ha',
    'coverage_pasture_ha',
    'pasture_with_age_ha',
    'pasture_without_age_ha',
    'age_outside_pasture_ha',
    'pasture_age100_ha',
    'pasture_age2xx_ha',
    'pasture_other_positive_age_ha',
    'pasture_age1_99_ha',
    'pasture_age101_200_ha',
    'age_above_expected_max_ha',
    'output_version',
    'processing_crs',
    'processing_transform',
    'coverage_asset',
    'pasture_age_asset',
    'grid_asset'
  ]
});

// ---------------------------------------------------------------------------
// 8. Batch export 2: endpoint rule for every retained cell
// ---------------------------------------------------------------------------

function anthropogenicMask(year) {
  var cov = coverage.select(K.coverageBandName(year));

  var nativeOrWater = inCodes(
    cov,
    K.CLASS_CODES.NAT.concat(K.CLASS_CODES.WATER)
  );

  var noData = inCodes(cov, K.CLASS_CODES.NODATA);

  return cov.mask()
    .gt(0)
    .and(noData.not())
    .and(nativeOrWater.not());
}

var endpointAnthropogenicArea = ee.Image.cat([
  unrestrictedAreaBand(
    anthropogenicMask(1985),
    'anthropogenic_1985_ha'
  ),
  unrestrictedAreaBand(
    anthropogenicMask(2025),
    'anthropogenic_2025_ha'
  )
]);

var endpointByCell = endpointAnthropogenicArea.reduceRegions({
  collection: grid,
  reducer: ee.Reducer.sum(),
  crs: K.CRS,
  crsTransform: K.CRS_TRANSFORM,
  tileScale: 16,
  maxPixelsPerRegion: 1000000
});

var endpointAudit = endpointByCell.map(function(feature) {
  var area1985 = ee.Number(feature.get('anthropogenic_1985_ha'));
  var area2025 = ee.Number(feature.get('anthropogenic_2025_ha'));

  var retainedByEndpointRule = area1985
    .gt(ENDPOINT_TOLERANCE_HA)
    .or(area2025.gt(ENDPOINT_TOLERANCE_HA));

  return feature
    .set(
      'endpoint_rule_pass',
      ee.Algorithms.If(retainedByEndpointRule, 1, 0)
    )
    .set(
      'possible_violation',
      ee.Algorithms.If(retainedByEndpointRule, 0, 1)
    )
    .set('endpoint_tolerance_ha', ENDPOINT_TOLERANCE_HA)
    .set('processing_crs', K.CRS)
    .set('processing_transform', TRANSFORM_TEXT)
    .set('output_version', K.OUTPUT_VERSION);
});

Export.table.toDrive({
  collection: endpointAudit,
  description: ENDPOINT_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: ENDPOINT_PREFIX,
  fileFormat: 'CSV',
  selectors: [
    'cell_id',
    'GRID_ID',
    'anthropogenic_1985_ha',
    'anthropogenic_2025_ha',
    'endpoint_rule_pass',
    'possible_violation',
    'endpoint_tolerance_ha',
    'output_version',
    'processing_crs',
    'processing_transform'
  ]
});

// ---------------------------------------------------------------------------
// 9. Batch export 3: targeted inventory of pasture-age codes 1 through 99
//
// The full source-code inventory was cancelled because it grouped all pixels
// for two variables and nine years. This replacement masks everything except
// the small area requiring clarification.
// ---------------------------------------------------------------------------

function lowAgeCodeAreas(year) {
  var cov = coverage.select(K.coverageBandName(year));
  var age = pastureAge
    .select([K.ageBandIndex(year)])
    .rename('age_code');

  var lowAgeMask = domainMask
    .and(cov.eq(K.CLASS_CODES.PAS[0]))
    .and(age.gte(1))
    .and(age.lte(99));

  var groupedInput = pixelAreaHa
    .rename('area_ha')
    .addBands(age.rename('code'))
    .updateMask(lowAgeMask);

  var groupedResult = groupedInput.reduceRegion({
    reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'code'
    }),
    geometry: PROCESSING_REGION,
    crs: K.CRS,
    crsTransform: K.CRS_TRANSFORM,
    maxPixels: 1e13,
    tileScale: 16
  });

  var groups = ee.List(
    ee.Algorithms.If(
      groupedResult.contains('groups'),
      groupedResult.get('groups'),
      ee.List([])
    )
  );

  return ee.FeatureCollection(groups.map(function(group) {
    group = ee.Dictionary(group);

    return ee.Feature(null, {
      year: year,
      code: group.get('code'),
      area_ha: group.get('sum'),
      output_version: K.OUTPUT_VERSION,
      processing_crs: K.CRS,
      processing_transform: TRANSFORM_TEXT
    });
  }));
}

var lowAgeCollections = AUDIT_YEARS.map(function(year) {
  return lowAgeCodeAreas(year);
});

var lowAgeAudit = ee.FeatureCollection(
  lowAgeCollections
).flatten();

Export.table.toDrive({
  collection: lowAgeAudit,
  description: LOW_AGE_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: LOW_AGE_PREFIX,
  fileFormat: 'CSV',
  selectors: [
    'year',
    'code',
    'area_ha',
    'output_version',
    'processing_crs',
    'processing_transform'
  ]
});

// ---------------------------------------------------------------------------
// 10. Lightweight map and execution guidance
// ---------------------------------------------------------------------------

Map.setCenter(-52, -9, 5);

Map.addLayer(
  grid,
  {color: '2b8cbe'},
  'Fixed analytical grid',
  false
);

print('AUDIT VERSION 3 SETUP COMPLETE.');
print('Run the three CSV exports sequentially from the Tasks tab.');
print('1 - Domain summary');
print('2 - Endpoint rule by cell');
print('3 - Targeted low-age code inventory');

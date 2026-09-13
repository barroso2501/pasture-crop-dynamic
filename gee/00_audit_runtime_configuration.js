/**
 * 00_audit_runtime_configuration.js - version 1
 *
 * Phase 0 provenance audit for the hosted Earth Engine constants module.
 *
 * The script compares the runtime module with the canonical repository
 * configuration and with the native projections reported directly by the
 * Collection 11 coverage and pasture-age assets. It performs metadata calls
 * only, creates one single-row CSV export, and does not modify any asset.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Repository values expected at the time of this audit
// ---------------------------------------------------------------------------

var AUDIT_VERSION = 'canonical-runtime-configuration-audit-v1';
var AUDIT_DATE = '2026-09-12';
var MODULE_PATH = 'users/barroso2501/pasture-crop:lib/constants';
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';
var OUTPUT_NAME = 'canonical_runtime_configuration_audit_v1';

var EXPECTED = {
  coverageAsset:
    'projects/mapbiomas-public/assets/brazil/lulc/collection11/' +
    'mapbiomas_brazil_collection11_coverage_v3',
  pastureAgeAsset:
    'projects/mapbiomas-public/assets/brazil/lulc/collection11/' +
    'mapbiomas_brazil_collection11_pasture_age_v1',
  analyticalGrid:
    'projects/ee-barroso2501/assets/' +
    'grade_hex_CeAmz_canonical_c11_v3',
  expectedCellCount: 24889,
  crs: 'EPSG:4326',
  transform: [
    0.00026949458523585647, 0, -74.02073025380652,
    0, -0.00026949458523585647, 5.405791885246045
  ],
  outputVersion: 'canonical-c11-coverage-v3-native-grid'
};

// ---------------------------------------------------------------------------
// Small client-side metadata helpers
// ---------------------------------------------------------------------------

function numbersEqual(a, b, tolerance) {
  return Math.abs(Number(a) - Number(b)) <= tolerance;
}

function arraysEqual(a, b, tolerance) {
  if (!a || !b || a.length !== b.length) {
    return false;
  }
  for (var i = 0; i < a.length; i++) {
    if (!numbersEqual(a[i], b[i], tolerance)) {
      return false;
    }
  }
  return true;
}

function boolInt(value) {
  return value ? 1 : 0;
}

function listText(values) {
  return values.map(function (value) {
    return String(value);
  }).join(',');
}

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);

// Projection.getInfo() is used only for six affine parameters from one band.
// No regional raster computation is evaluated in the Console.
var coverageProjectionInfo = coverage
  .select(K.coverageBandName(K.FIRST_YEAR))
  .projection()
  .getInfo();

var ageProjectionInfo = pastureAge
  .select([K.ageBandIndex(K.FIRST_YEAR)])
  .projection()
  .getInfo();

var coverageNativeTransform = coverageProjectionInfo.transform;
var ageNativeTransform = ageProjectionInfo.transform;

var repositoryModuleChecks = {
  coverageAsset: K.COVERAGE_ASSET === EXPECTED.coverageAsset,
  pastureAgeAsset: K.PASTURE_AGE_ASSET === EXPECTED.pastureAgeAsset,
  analyticalGrid: K.ANALYTICAL_GRID === EXPECTED.analyticalGrid,
  expectedCellCount:
    K.EXPECTED_ANALYTICAL_CELL_COUNT === EXPECTED.expectedCellCount,
  crs: K.CRS === EXPECTED.crs,
  transform: arraysEqual(K.CRS_TRANSFORM, EXPECTED.transform, 1e-15),
  outputVersion: K.OUTPUT_VERSION === EXPECTED.outputVersion
};

var repositoryModulePass = Object.keys(repositoryModuleChecks).every(
  function (key) {
    return repositoryModuleChecks[key];
  }
);

var moduleCoverageNativeTransformPass = arraysEqual(
  K.CRS_TRANSFORM,
  coverageNativeTransform,
  1e-15
);

var coverageNativeCrsPass = coverageProjectionInfo.crs === K.CRS;
var ageNativeCrsPass = ageProjectionInfo.crs === K.CRS;

var xPixelOffset = (
  ageNativeTransform[2] - coverageNativeTransform[2]
) / coverageNativeTransform[0];

var yPixelOffset = (
  ageNativeTransform[5] - coverageNativeTransform[5]
) / Math.abs(coverageNativeTransform[4]);

var integerOffsetTolerance = 1e-8;
var xOffsetIntegerPass = numbersEqual(
  xPixelOffset,
  Math.round(xPixelOffset),
  integerOffsetTolerance
);
var yOffsetIntegerPass = numbersEqual(
  yPixelOffset,
  Math.round(yPixelOffset),
  integerOffsetTolerance
);

var pixelScalePass =
  numbersEqual(
    coverageNativeTransform[0],
    ageNativeTransform[0],
    1e-15
  ) &&
  numbersEqual(
    coverageNativeTransform[4],
    ageNativeTransform[4],
    1e-15
  );

var sourceLatticePass =
  coverageNativeCrsPass &&
  ageNativeCrsPass &&
  pixelScalePass &&
  xOffsetIntegerPass &&
  yOffsetIntegerPass;

// ---------------------------------------------------------------------------
// Lightweight server-side asset checks
// ---------------------------------------------------------------------------

var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var gridCount = grid.size();
var distinctCellIds = grid.aggregate_count_distinct(K.CELL_ID_FIELD);
var coverageBandCount = coverage.bandNames().size();
var ageBandCount = pastureAge.bandNames().size();

var gridCountPass = gridCount.eq(EXPECTED.expectedCellCount);
var distinctCellIdPass = distinctCellIds.eq(EXPECTED.expectedCellCount);
var coverageBandCountPass = coverageBandCount.eq(41);
var ageBandCountPass = ageBandCount.eq(41);

function serverBoolInt(value) {
  return ee.Number(ee.Algorithms.If(value, 1, 0));
}

var staticConfigurationPass =
  repositoryModulePass &&
  moduleCoverageNativeTransformPass &&
  sourceLatticePass;

var completePass = ee.Number(boolInt(staticConfigurationPass))
  .multiply(serverBoolInt(gridCountPass))
  .multiply(serverBoolInt(distinctCellIdPass))
  .multiply(serverBoolInt(coverageBandCountPass))
  .multiply(serverBoolInt(ageBandCountPass));

var auditFeature = ee.Feature(null, {
  audit_version: AUDIT_VERSION,
  audit_date: AUDIT_DATE,
  module_path: MODULE_PATH,

  runtime_coverage_asset: K.COVERAGE_ASSET,
  expected_coverage_asset: EXPECTED.coverageAsset,
  coverage_asset_match: boolInt(repositoryModuleChecks.coverageAsset),

  runtime_pasture_age_asset: K.PASTURE_AGE_ASSET,
  expected_pasture_age_asset: EXPECTED.pastureAgeAsset,
  pasture_age_asset_match:
    boolInt(repositoryModuleChecks.pastureAgeAsset),

  runtime_analytical_grid: K.ANALYTICAL_GRID,
  expected_analytical_grid: EXPECTED.analyticalGrid,
  analytical_grid_match: boolInt(repositoryModuleChecks.analyticalGrid),

  runtime_expected_cell_count: K.EXPECTED_ANALYTICAL_CELL_COUNT,
  repository_expected_cell_count: EXPECTED.expectedCellCount,
  expected_cell_count_match:
    boolInt(repositoryModuleChecks.expectedCellCount),
  observed_grid_count: gridCount,
  observed_distinct_cell_ids: distinctCellIds,
  grid_count_pass: gridCountPass,
  distinct_cell_id_pass: distinctCellIdPass,

  runtime_crs: K.CRS,
  expected_crs: EXPECTED.crs,
  coverage_native_crs: coverageProjectionInfo.crs,
  pasture_age_native_crs: ageProjectionInfo.crs,
  runtime_crs_match: boolInt(repositoryModuleChecks.crs),
  coverage_native_crs_match: boolInt(coverageNativeCrsPass),
  pasture_age_native_crs_match: boolInt(ageNativeCrsPass),

  runtime_transform: listText(K.CRS_TRANSFORM),
  expected_transform: listText(EXPECTED.transform),
  coverage_native_transform: listText(coverageNativeTransform),
  pasture_age_native_transform: listText(ageNativeTransform),
  repository_runtime_transform_match:
    boolInt(repositoryModuleChecks.transform),
  runtime_coverage_native_transform_match:
    boolInt(moduleCoverageNativeTransformPass),

  coverage_age_x_offset_pixels: xPixelOffset,
  coverage_age_y_offset_pixels: yPixelOffset,
  coverage_age_pixel_scale_match: boolInt(pixelScalePass),
  coverage_age_integer_x_offset: boolInt(xOffsetIntegerPass),
  coverage_age_integer_y_offset: boolInt(yOffsetIntegerPass),
  coverage_age_same_lattice: boolInt(sourceLatticePass),

  runtime_output_version: K.OUTPUT_VERSION,
  expected_output_version: EXPECTED.outputVersion,
  output_version_match: boolInt(repositoryModuleChecks.outputVersion),

  coverage_band_count: coverageBandCount,
  pasture_age_band_count: ageBandCount,
  coverage_band_count_pass: coverageBandCountPass,
  pasture_age_band_count_pass: ageBandCountPass,

  static_configuration_pass: boolInt(staticConfigurationPass),
  complete_runtime_configuration_pass: completePass
});

// ---------------------------------------------------------------------------
// Console report and one-row export
// ---------------------------------------------------------------------------

print('PHASE 0 - RUNTIME CONFIGURATION AUDIT - VERSION 1');
print('Hosted module:', MODULE_PATH);
print('Runtime coverage asset:', K.COVERAGE_ASSET);
print('Runtime pasture-age asset:', K.PASTURE_AGE_ASSET);
print('Runtime analytical grid:', K.ANALYTICAL_GRID);
print('Runtime expected cell count:', K.EXPECTED_ANALYTICAL_CELL_COUNT);
print('Observed grid count:', gridCount);
print('Observed distinct cell_id count:', distinctCellIds);
print('Runtime CRS:', K.CRS);
print('Runtime transform:', K.CRS_TRANSFORM);
print('Coverage native projection info:', coverageProjectionInfo);
print('Pasture-age native projection info:', ageProjectionInfo);
print('Coverage-age X offset in pixels:', xPixelOffset);
print('Coverage-age Y offset in pixels:', yPixelOffset);
print('Repository-runtime static checks:', repositoryModuleChecks);
print('Static configuration pass (expected true):', staticConfigurationPass);
print('Source lattice pass (expected true):', sourceLatticePass);
print('Complete runtime configuration pass (expected 1):', completePass);

Export.table.toDrive({
  collection: ee.FeatureCollection([auditFeature]),
  description: OUTPUT_NAME,
  fileNamePrefix: OUTPUT_NAME,
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV'
});

print('ONE TASK CREATED:', OUTPUT_NAME);
print('Run it only if the displayed static checks are true and the expected');
print('and observed grid counts are 24,889. Return the CSV and Console output.');

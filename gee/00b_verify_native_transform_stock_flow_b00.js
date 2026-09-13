/**
 * 00b_verify_native_transform_stock_flow_b00.js - version 1
 *
 * Phase 0 controlled replication of the accepted 2005-2010 b00 stock-flow
 * pilot. The processing CRS and affine transform are explicit literals in
 * this script and do not depend on the hosted constants module.
 *
 * All other inputs, class definitions, calculations, selectors, and output
 * metadata reproduce gee/03a_reprocess_stock_flow_pilot_b00.js. The output is
 * intended only for cell-by-cell comparison with the accepted pilot CSV.
 * It creates one Drive CSV task and no Earth Engine asset.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Verification configuration
// ---------------------------------------------------------------------------

var T0 = 2005;
var T1 = 2010;
var PILOT_BATCH = 0;
var EXPECTED_PILOT_CELLS = 3168;
var MAX_PIXELS_PER_REGION = 30000000;
var TILE_SCALE = 8;
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';
var OUTPUT_NAME =
  'canonical_stock_flow_2005_2010_b00_native_transform_verification_v1';

// Intentionally explicit. Do not replace with K.CRS or K.CRS_TRANSFORM in
// this verification script.
var EXPLICIT_CRS = 'EPSG:4326';
var EXPLICIT_NATIVE_TRANSFORM = [
  0.00026949458523585647, 0, -74.02073025380652,
  0, -0.00026949458523585647, 5.405791885246045
];

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);

var grid = ee.FeatureCollection(K.ANALYTICAL_GRID)
  .filter(ee.Filter.eq('source_batch_id', PILOT_BATCH));

var cov0 = coverage.select(K.coverageBandName(T0));
var cov1 = coverage.select(K.coverageBandName(T1));
var age0 = pastureAge.select([K.ageBandIndex(T0)]);

var MASKED_VALUE = -9999;
var cov0Filled = cov0.toInt16().unmask(MASKED_VALUE);
var cov1Filled = cov1.toInt16().unmask(MASKED_VALUE);
var age0Filled = age0.toInt16().unmask(MASKED_VALUE);
var pixelAreaHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);

// ---------------------------------------------------------------------------
// Mutually exclusive state masks
// ---------------------------------------------------------------------------

function inCodes(image, codes) {
  var result = image.eq(codes[0]);
  for (var i = 1; i < codes.length; i++) {
    result = result.or(image.eq(codes[i]));
  }
  return result;
}

function stateMasks(filledCoverage) {
  var masks = {
    nat: inCodes(filledCoverage, K.CLASS_CODES.NAT),
    pas: inCodes(filledCoverage, K.CLASS_CODES.PAS),
    tmp: inCodes(filledCoverage, K.CLASS_CODES.TMP),
    oag: inCodes(filledCoverage, K.CLASS_CODES.OAG),
    out: inCodes(filledCoverage, K.CLASS_CODES.OUT),
    water: inCodes(filledCoverage, K.CLASS_CODES.WATER),
    nodata: inCodes(filledCoverage, K.CLASS_CODES.NODATA),
    masked: filledCoverage.eq(MASKED_VALUE)
  };

  var known = masks.nat
    .or(masks.pas)
    .or(masks.tmp)
    .or(masks.oag)
    .or(masks.out)
    .or(masks.water)
    .or(masks.nodata);

  masks.unexpected = masks.masked.not().and(known.not());
  return masks;
}

var states0 = stateMasks(cov0Filled);
var states1 = stateMasks(cov1Filled);

var STATE_NAMES = [
  'nat', 'pas', 'tmp', 'oag', 'out',
  'water', 'nodata', 'unexpected', 'masked'
];
var FOCAL_NAMES = ['nat', 'pas', 'tmp'];
var AUXILIARY_NAMES = [
  'oag', 'out', 'water', 'nodata', 'unexpected', 'masked'
];

function areaBand(mask, name) {
  return mask
    .multiply(pixelAreaHa)
    .rename(name)
    .unmask(0);
}

var bands = [];
var selectors = ['cell_id', 'GRID_ID', 'source_batch_id'];

STATE_NAMES.forEach(function (stateName) {
  var name0 = 'stock0_' + stateName;
  var name1 = 'stock1_' + stateName;
  bands.push(areaBand(states0[stateName], name0));
  bands.push(areaBand(states1[stateName], name1));
  selectors.push(name0);
  selectors.push(name1);
});

FOCAL_NAMES.forEach(function (originName) {
  STATE_NAMES.forEach(function (destinationName) {
    var flowName = 'flow_' + originName + '_' + destinationName;
    bands.push(areaBand(
      states0[originName].and(states1[destinationName]),
      flowName
    ));
    selectors.push(flowName);
  });
});

AUXILIARY_NAMES.forEach(function (originName) {
  FOCAL_NAMES.forEach(function (destinationName) {
    var flowName = 'flow_' + originName + '_' + destinationName;
    bands.push(areaBand(
      states0[originName].and(states1[destinationName]),
      flowName
    ));
    selectors.push(flowName);
  });
});

// ---------------------------------------------------------------------------
// Exhaustive PAS->TMP origin partition using age at t0
// ---------------------------------------------------------------------------

var pasTmp = states0.pas.and(states1.tmp);
var ageCensored = age0Filled.eq(K.PASTURE_AGE_INITIAL_STOCK_CODE);
var maximumValidAgeCode = K.PASTURE_AGE_OFFSET + (T0 - K.FIRST_YEAR);
var ageNew = age0Filled.gt(K.PASTURE_AGE_OFFSET)
  .and(age0Filled.lte(maximumValidAgeCode));
var ageUnresolved = inCodes(
  age0Filled,
  K.PASTURE_AGE_UNRESOLVED_CODES
);
var ageAttributed = ageCensored.or(ageNew).or(ageUnresolved);
var ageUnattributed = ageAttributed.not();

var AGE_PARTITION_NAMES = [
  'pas_tmp_censored',
  'pas_tmp_new',
  'pas_tmp_unresolved_age',
  'pas_tmp_unattributed_age'
];

bands.push(areaBand(
  pasTmp.and(ageCensored),
  AGE_PARTITION_NAMES[0]
));
bands.push(areaBand(
  pasTmp.and(ageNew),
  AGE_PARTITION_NAMES[1]
));
bands.push(areaBand(
  pasTmp.and(ageUnresolved),
  AGE_PARTITION_NAMES[2]
));
bands.push(areaBand(
  pasTmp.and(ageUnattributed),
  AGE_PARTITION_NAMES[3]
));

selectors = selectors.concat(AGE_PARTITION_NAMES);

bands.push(pixelAreaHa.rename('raster_area_ha'));
selectors.push('raster_area_ha');

var metricImage = ee.Image.cat(bands);

// ---------------------------------------------------------------------------
// Reduction and per-cell accounting checks
// ---------------------------------------------------------------------------

function propertySum(feature, names) {
  var total = ee.Number(0);
  names.forEach(function (name) {
    total = total.add(ee.Number(feature.get(name)));
  });
  return total;
}

function stockNames(endpoint) {
  return STATE_NAMES.map(function (name) {
    return 'stock' + endpoint + '_' + name;
  });
}

function originFlowNames(originName) {
  return STATE_NAMES.map(function (destinationName) {
    return 'flow_' + originName + '_' + destinationName;
  });
}

function destinationFlowNames(destinationName) {
  return STATE_NAMES.map(function (originName) {
    return 'flow_' + originName + '_' + destinationName;
  });
}

var reduced = metricImage.reduceRegions({
  collection: grid,
  reducer: ee.Reducer.sum(),
  crs: EXPLICIT_CRS,
  crsTransform: EXPLICIT_NATIVE_TRANSFORM,
  tileScale: TILE_SCALE,
  maxPixelsPerRegion: MAX_PIXELS_PER_REGION
});

var panel = reduced.map(function (feature) {
  feature = ee.Feature(feature);

  var stock0Total = propertySum(feature, stockNames(0));
  var stock1Total = propertySum(feature, stockNames(1));
  var rasterArea = ee.Number(feature.get('raster_area_ha'));

  var natOriginFlows = propertySum(feature, originFlowNames('nat'));
  var pasOriginFlows = propertySum(feature, originFlowNames('pas'));
  var tmpOriginFlows = propertySum(feature, originFlowNames('tmp'));

  var natDestinationFlows =
    propertySum(feature, destinationFlowNames('nat'));
  var pasDestinationFlows =
    propertySum(feature, destinationFlowNames('pas'));
  var tmpDestinationFlows =
    propertySum(feature, destinationFlowNames('tmp'));

  var pasTmpPartition = propertySum(feature, AGE_PARTITION_NAMES);
  var pasTmpTotal = ee.Number(feature.get('flow_pas_tmp'));

  return feature.set({
    t0: T0,
    t1: T1,
    interval: T0 + '_' + T1,
    output_version: 'canonical-stock-flow-v1',
    diagnostic_interval: 0,
    geometry_area_ha: feature.geometry().area(1)
      .divide(K.SQUARE_METRES_PER_HECTARE),
    valid0_area_ha: stock0Total
      .subtract(ee.Number(feature.get('stock0_masked'))),
    valid1_area_ha: stock1Total
      .subtract(ee.Number(feature.get('stock1_masked'))),
    stock0_total: stock0Total,
    stock1_total: stock1Total,
    residual_stock0_area: stock0Total.subtract(rasterArea),
    residual_stock1_area: stock1Total.subtract(rasterArea),
    residual_origin_nat: ee.Number(feature.get('stock0_nat'))
      .subtract(natOriginFlows),
    residual_origin_pas: ee.Number(feature.get('stock0_pas'))
      .subtract(pasOriginFlows),
    residual_origin_tmp: ee.Number(feature.get('stock0_tmp'))
      .subtract(tmpOriginFlows),
    residual_destination_nat: ee.Number(feature.get('stock1_nat'))
      .subtract(natDestinationFlows),
    residual_destination_pas: ee.Number(feature.get('stock1_pas'))
      .subtract(pasDestinationFlows),
    residual_destination_tmp: ee.Number(feature.get('stock1_tmp'))
      .subtract(tmpDestinationFlows),
    residual_pas_tmp_partition: pasTmpTotal.subtract(pasTmpPartition)
  });
});

var METADATA_SELECTORS = [
  'cell_id', 'GRID_ID', 'source_batch_id',
  't0', 't1', 'interval', 'output_version', 'diagnostic_interval',
  'geometry_area_ha', 'valid0_area_ha', 'valid1_area_ha'
];

var AUDIT_SELECTORS = [
  'stock0_total',
  'stock1_total',
  'residual_stock0_area',
  'residual_stock1_area',
  'residual_origin_nat',
  'residual_origin_pas',
  'residual_origin_tmp',
  'residual_destination_nat',
  'residual_destination_pas',
  'residual_destination_tmp',
  'residual_pas_tmp_partition'
];

var OUTPUT_SELECTORS = METADATA_SELECTORS
  .concat(selectors.slice(3))
  .concat(AUDIT_SELECTORS);

// ---------------------------------------------------------------------------
// Lightweight setup checks and one export task
// ---------------------------------------------------------------------------

print('PHASE 0 - EXPLICIT NATIVE-TRANSFORM B00 VERIFICATION - VERSION 1');
print('Coverage asset:', K.COVERAGE_ASSET);
print('Pasture-age asset:', K.PASTURE_AGE_ASSET);
print('Canonical grid asset:', K.ANALYTICAL_GRID);
print('Interval:', T0 + '-' + T1);
print('Pilot source_batch_id:', PILOT_BATCH);
print('Pilot cell count (expected 3,168):', grid.size());
print('Explicit processing CRS:', EXPLICIT_CRS);
print('Explicit native transform:', EXPLICIT_NATIVE_TRANSFORM);
print('Runtime module CRS for comparison:', K.CRS);
print('Runtime module transform for comparison:', K.CRS_TRANSFORM);
print('Metric band count:', metricImage.bandNames().size());
print('Output column count (expected 90):', OUTPUT_SELECTORS.length);
print('Heavy results are intentionally not evaluated in the Console.');

Export.table.toDrive({
  collection: panel,
  description: OUTPUT_NAME,
  fileNamePrefix: OUTPUT_NAME,
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV',
  selectors: OUTPUT_SELECTORS
});

print('ONE TASK CREATED:', OUTPUT_NAME);
print('Run the task and return the CSV plus task metadata for comparison.');

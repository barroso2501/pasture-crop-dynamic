/**
 * 03b_reprocess_stock_flow_2005_2010_full_domain.js - version 1
 *
 * Full-domain production test for the five-year stock-and-flow panel.
 *
 * Scope:
 *   - interval: 2005-2010;
 *   - complete canonical domain: 24,889 cells;
 *   - one balanced CSV row per cell, including structural zeros;
 *   - canonical Collection 11 coverage_v3 and pasture-age assets;
 *   - native coverage CRS and affine transform from config/constants.js.
 *
 * The script measures independent endpoint stocks, the transitions required
 * to close the three focal origins and destinations (NAT, PAS, TMP), and an
 * exhaustive origin partition of PAS->TMP by pasture-age status.
 *
 * This script is identical in analytical logic to the validated b00 pilot.
 * The only substantive change is removal of the source_batch_id filter.
 * It creates ONE Drive export task and no Earth Engine asset.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Full-domain configuration
// ---------------------------------------------------------------------------

var T0 = 2005;
var T1 = 2010;
var EXPECTED_DOMAIN_CELLS = K.EXPECTED_ANALYTICAL_CELL_COUNT;
var MAX_PIXELS_PER_REGION = 30000000;
var TILE_SCALE = 8;
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';
var OUTPUT_NAME = 'canonical_stock_flow_2005_2010_full_v1';

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);

var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);

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

// Independent stocks at both endpoints.
STATE_NAMES.forEach(function (stateName) {
  var name0 = 'stock0_' + stateName;
  var name1 = 'stock1_' + stateName;
  bands.push(areaBand(states0[stateName], name0));
  bands.push(areaBand(states1[stateName], name1));
  selectors.push(name0);
  selectors.push(name1);
});

// All destinations for focal origins: closes NAT, PAS, and TMP at t0.
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

// Auxiliary origins entering focal destinations: closes NAT, PAS, and TMP at t1.
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
// Exhaustive origin partition of PAS->TMP using age at t0
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

// Independent raster-area control on the canonical lattice.
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
  crs: K.CRS,
  crsTransform: K.CRS_TRANSFORM,
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

print('CANONICAL STOCK-FLOW FULL-DOMAIN TEST - VERSION 1');
print('Coverage asset:', K.COVERAGE_ASSET);
print('Pasture-age asset:', K.PASTURE_AGE_ASSET);
print('Canonical grid asset:', K.ANALYTICAL_GRID);
print('Interval:', T0 + '-' + T1);
print('Expected domain cell count:', EXPECTED_DOMAIN_CELLS);
print('Full-domain cell count (expected 24,889):', grid.size());
print('Metric band count:', metricImage.bandNames().size());
print('Output column count:', OUTPUT_SELECTORS.length);
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
print('Run the task and return the CSV plus task metadata for validation.');

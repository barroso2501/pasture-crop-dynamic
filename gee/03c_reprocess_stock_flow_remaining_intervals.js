/**
 * 03c_reprocess_stock_flow_remaining_intervals.js - version 1
 *
 * Production processing for the seven five-year intervals that remain after
 * validation of the canonical 2005-2010 full-domain result.
 *
 * Scope:
 *   - seven independent full-domain CSV exports;
 *   - complete canonical domain: 24,889 cells in every interval;
 *   - one balanced row per cell, including structural zeros;
 *   - canonical Collection 11 coverage_v3 and pasture-age assets;
 *   - native coverage CRS and affine transform from config/constants.js;
 *   - 2020-2025 explicitly flagged as a diagnostic interval.
 *
 * The script uses the analytical logic validated by:
 *   - gee/03a_reprocess_stock_flow_pilot_b00.js; and
 *   - gee/03b_reprocess_stock_flow_2005_2010_full_domain.js.
 *
 * It does NOT recreate 2005-2010. Loading the script creates seven Drive
 * tasks. Tasks are not started automatically. Because each full-domain export
 * is computationally expensive, run them individually and record the task ID,
 * runtime, attempt number, and EECU use after completion.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Production configuration
// ---------------------------------------------------------------------------

var INTERVALS = [
  [1985, 1990],
  [1990, 1995],
  [1995, 2000],
  [2000, 2005],
  [2010, 2015],
  [2015, 2020],
  [2020, 2025]
];

var EXPECTED_DOMAIN_CELLS = K.EXPECTED_ANALYTICAL_CELL_COUNT;
var MAX_PIXELS_PER_REGION = 30000000;
var TILE_SCALE = 8;
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';
var OUTPUT_VERSION = 'canonical-stock-flow-v1';

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);

var MASKED_VALUE = -9999;
var pixelAreaHa = ee.Image.pixelArea()
  .divide(K.SQUARE_METRES_PER_HECTARE);

var STATE_NAMES = [
  'nat', 'pas', 'tmp', 'oag', 'out',
  'water', 'nodata', 'unexpected', 'masked'
];

var FOCAL_NAMES = ['nat', 'pas', 'tmp'];

var AUXILIARY_NAMES = [
  'oag', 'out', 'water', 'nodata', 'unexpected', 'masked'
];

var AGE_PARTITION_NAMES = [
  'pas_tmp_censored',
  'pas_tmp_new',
  'pas_tmp_unresolved_age',
  'pas_tmp_unattributed_age'
];

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

// ---------------------------------------------------------------------------
// Shared helpers
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

function areaBand(mask, name) {
  return mask
    .multiply(pixelAreaHa)
    .rename(name)
    .unmask(0);
}

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

// ---------------------------------------------------------------------------
// Build one independent full-domain export
// ---------------------------------------------------------------------------

function createIntervalExport(t0, t1) {
  var intervalLabel = t0 + '_' + t1;
  var outputName = 'canonical_stock_flow_' + intervalLabel + '_full_v1';
  var diagnosticInterval =
    (t0 === K.DIAGNOSTIC_INTERVAL[0] &&
     t1 === K.DIAGNOSTIC_INTERVAL[1]) ? 1 : 0;

  var cov0 = coverage.select(K.coverageBandName(t0));
  var cov1 = coverage.select(K.coverageBandName(t1));
  var age0 = pastureAge.select([K.ageBandIndex(t0)]);

  var cov0Filled = cov0.toInt16().unmask(MASKED_VALUE);
  var cov1Filled = cov1.toInt16().unmask(MASKED_VALUE);
  var age0Filled = age0.toInt16().unmask(MASKED_VALUE);

  var states0 = stateMasks(cov0Filled);
  var states1 = stateMasks(cov1Filled);

  var bands = [];
  var selectors = ['cell_id', 'GRID_ID', 'source_batch_id'];

  // Independently measured stocks at both endpoints.
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

  // Auxiliary origins entering focal destinations: closes focal stocks at t1.
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

  // Exhaustive PAS->TMP origin partition using pasture age at t0.
  var pasTmp = states0.pas.and(states1.tmp);
  var ageCensored = age0Filled.eq(K.PASTURE_AGE_INITIAL_STOCK_CODE);
  var maximumValidAgeCode = K.PASTURE_AGE_OFFSET +
    (t0 - K.FIRST_YEAR);
  var ageNew = age0Filled.gt(K.PASTURE_AGE_OFFSET)
    .and(age0Filled.lte(maximumValidAgeCode));
  var ageUnresolved = inCodes(
    age0Filled,
    K.PASTURE_AGE_UNRESOLVED_CODES
  );
  var ageAttributed = ageCensored.or(ageNew).or(ageUnresolved);
  var ageUnattributed = ageAttributed.not();

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
      t0: t0,
      t1: t1,
      interval: intervalLabel,
      output_version: OUTPUT_VERSION,
      diagnostic_interval: diagnosticInterval,
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

  var outputSelectors = METADATA_SELECTORS
    .concat(selectors.slice(3))
    .concat(AUDIT_SELECTORS);

  Export.table.toDrive({
    collection: panel,
    description: outputName,
    fileNamePrefix: outputName,
    folder: DRIVE_FOLDER,
    fileFormat: 'CSV',
    selectors: outputSelectors
  });

  print(
    'TASK CREATED:',
    outputName,
    '| diagnostic_interval =',
    diagnosticInterval,
    '| metric bands =',
    metricImage.bandNames().size(),
    '| output columns =',
    outputSelectors.length
  );
}

// ---------------------------------------------------------------------------
// Lightweight setup checks and task creation
// ---------------------------------------------------------------------------

print('CANONICAL STOCK-FLOW REMAINING INTERVALS - VERSION 1');
print('Coverage asset:', K.COVERAGE_ASSET);
print('Pasture-age asset:', K.PASTURE_AGE_ASSET);
print('Canonical grid asset:', K.ANALYTICAL_GRID);
print('Expected domain cell count:', EXPECTED_DOMAIN_CELLS);
print('Full-domain cell count (expected 24,889):', grid.size());
print('Intervals to create:', INTERVALS);
print('2005-2010 is intentionally excluded: canonical result already exists.');
print('Heavy results are intentionally not evaluated in the Console.');

INTERVALS.forEach(function (interval) {
  createIntervalExport(interval[0], interval[1]);
});

print('SEVEN TASKS CREATED. Start them individually from the Tasks tab.');
print('Return each CSV plus its task metadata for validation.');


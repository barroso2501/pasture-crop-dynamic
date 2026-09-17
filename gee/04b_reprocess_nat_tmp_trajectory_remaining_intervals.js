/**
 * 04b_reprocess_nat_tmp_trajectory_remaining_intervals.js - version 1
 *
 * Production processing for the seven five-year NAT->TMP within-interval
 * trajectory analyses remaining after validation of the 2005-2010 pilot.
 *
 * Scope:
 *   - seven independent full-domain CSV exports;
 *   - complete canonical domain: 24,889 cells in every interval;
 *   - one balanced row per cell, including structural zeros;
 *   - canonical Collection 11 coverage_v3 and native coverage transform;
 *   - counts pasture observations in the four intermediate years;
 *   - measures any pasture, two-or-more pasture years, and two consecutive
 *     pasture years;
 *   - separates incomplete intermediate raster support; and
 *   - exports explicit accounting residuals.
 *
 * This script applies without methodological changes the design validated by:
 *   - gee/04a_reprocess_nat_tmp_trajectory_2005_2010_full_domain.js; and
 *   - docs/validation/nat_tmp_trajectory_2005_2010.md.
 *
 * It does NOT recreate 2005-2010. Loading the script creates seven Drive
 * tasks. Tasks are not started automatically. Run them individually and
 * record task ID, runtime, attempt number, and EECU use after completion.
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
var OUTPUT_VERSION = 'canonical-nat-tmp-trajectory-v1';
var MASKED_VALUE = -9999;

var coverage = ee.Image(K.COVERAGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelAreaHa = ee.Image.pixelArea()
  .divide(K.SQUARE_METRES_PER_HECTARE);

var METADATA_SELECTORS = [
  'cell_id',
  'GRID_ID',
  'source_batch_id',
  't0',
  't1',
  'interval',
  'output_version',
  'diagnostic_interval',
  'intermediate_years',
  'geometry_area_ha'
];

var AUDIT_SELECTORS = [
  'residual_endpoint_observation_partition',
  'residual_pas_count_partition',
  'residual_pas_any_partition',
  'residual_pas_2plus_partition',
  'residual_pas_consecutive_partition'
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

function filledCoverage(year) {
  return coverage
    .select(K.coverageBandName(year))
    .toInt16()
    .unmask(MASKED_VALUE);
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

// ---------------------------------------------------------------------------
// Build one independent full-domain export
// ---------------------------------------------------------------------------

function createIntervalExport(t0, t1) {
  var intervalLabel = t0 + '_' + t1;
  var midYears = [t0 + 1, t0 + 2, t0 + 3, t0 + 4];
  var outputName = 'canonical_nat_tmp_trajectory_' +
    intervalLabel + '_full_v1';
  var diagnosticInterval =
    (t0 === K.DIAGNOSTIC_INTERVAL[0] &&
     t1 === K.DIAGNOSTIC_INTERVAL[1]) ? 1 : 0;

  // Endpoint population.
  var cov0 = filledCoverage(t0);
  var cov1 = filledCoverage(t1);
  var nat0 = inCodes(cov0, K.CLASS_CODES.NAT);
  var tmp1 = inCodes(cov1, K.CLASS_CODES.TMP);
  var natTmpEndpoint = nat0.and(tmp1);

  // Four intermediate annual observations.
  var midCoverage = midYears.map(function (year) {
    return filledCoverage(year);
  });

  var midObserved = midCoverage.map(function (image) {
    return image.neq(MASKED_VALUE);
  });

  var midPasture = midCoverage.map(function (image) {
    return inCodes(image, K.CLASS_CODES.PAS);
  });

  var allMidObserved = midObserved[0]
    .and(midObserved[1])
    .and(midObserved[2])
    .and(midObserved[3]);

  var natTmpMidAllObserved = natTmpEndpoint.and(allMidObserved);
  var natTmpMidIncomplete = natTmpEndpoint.and(allMidObserved.not());

  var pastureYearCount = ee.Image.constant(0).toInt8();
  midPasture.forEach(function (pastureMask) {
    pastureYearCount = pastureYearCount.add(pastureMask.toInt8());
  });

  var pastureConsecutive2 = midPasture[0].and(midPasture[1])
    .or(midPasture[1].and(midPasture[2]))
    .or(midPasture[2].and(midPasture[3]));

  var natTmpPasAny = natTmpMidAllObserved.and(
    pastureYearCount.gte(1)
  );
  var natTmpPas2Plus = natTmpMidAllObserved.and(
    pastureYearCount.gte(2)
  );
  var natTmpPasConsecutive2 = natTmpMidAllObserved.and(
    pastureConsecutive2
  );
  var natTmpPasAnyNonconsecutive2 = natTmpPasAny.and(
    pastureConsecutive2.not()
  );

  // Raster metrics.
  var bands = [];
  var metricSelectors = [];

  function addMetric(mask, name) {
    bands.push(areaBand(mask, name));
    metricSelectors.push(name);
  }

  addMetric(natTmpEndpoint, 'nat_tmp_endpoint_ha');
  addMetric(
    natTmpMidAllObserved,
    'nat_tmp_mid_all_observed_ha'
  );
  addMetric(natTmpMidIncomplete, 'nat_tmp_mid_incomplete_ha');

  var countNames = [];
  for (var count = 0; count <= 4; count++) {
    var countName = 'nat_tmp_pas_years_' + count + '_ha';
    countNames.push(countName);
    addMetric(
      natTmpMidAllObserved.and(pastureYearCount.eq(count)),
      countName
    );
  }

  addMetric(natTmpPasAny, 'nat_tmp_pas_any_ha');
  addMetric(natTmpPas2Plus, 'nat_tmp_pas_2plus_ha');
  addMetric(
    natTmpPasConsecutive2,
    'nat_tmp_pas_consecutive2_ha'
  );
  addMetric(
    natTmpPasAnyNonconsecutive2,
    'nat_tmp_pas_any_nonconsecutive2_ha'
  );

  bands.push(pixelAreaHa.rename('raster_area_ha'));
  metricSelectors.push('raster_area_ha');

  var metricImage = ee.Image.cat(bands);

  // Reduction and accounting checks.
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

    var endpoint = ee.Number(feature.get('nat_tmp_endpoint_ha'));
    var allObserved = ee.Number(
      feature.get('nat_tmp_mid_all_observed_ha')
    );
    var incomplete = ee.Number(
      feature.get('nat_tmp_mid_incomplete_ha')
    );
    var noPasture = ee.Number(
      feature.get('nat_tmp_pas_years_0_ha')
    );
    var pastureAny = ee.Number(feature.get('nat_tmp_pas_any_ha'));
    var pasture2Plus = ee.Number(
      feature.get('nat_tmp_pas_2plus_ha')
    );
    var pastureConsecutive2 = ee.Number(
      feature.get('nat_tmp_pas_consecutive2_ha')
    );
    var pastureAnyNonconsecutive2 = ee.Number(
      feature.get('nat_tmp_pas_any_nonconsecutive2_ha')
    );

    var countTotal = propertySum(feature, countNames);
    var count2PlusTotal = propertySum(feature, [
      'nat_tmp_pas_years_2_ha',
      'nat_tmp_pas_years_3_ha',
      'nat_tmp_pas_years_4_ha'
    ]);

    return feature.set({
      t0: t0,
      t1: t1,
      interval: intervalLabel,
      output_version: OUTPUT_VERSION,
      diagnostic_interval: diagnosticInterval,
      intermediate_years: midYears.join(','),
      geometry_area_ha: feature.geometry().area(1)
        .divide(K.SQUARE_METRES_PER_HECTARE),
      residual_endpoint_observation_partition: endpoint
        .subtract(allObserved)
        .subtract(incomplete),
      residual_pas_count_partition: allObserved.subtract(countTotal),
      residual_pas_any_partition: allObserved
        .subtract(noPasture)
        .subtract(pastureAny),
      residual_pas_2plus_partition: pasture2Plus
        .subtract(count2PlusTotal),
      residual_pas_consecutive_partition: pastureAny
        .subtract(pastureConsecutive2)
        .subtract(pastureAnyNonconsecutive2)
    });
  });

  var outputSelectors = METADATA_SELECTORS
    .concat(metricSelectors)
    .concat(AUDIT_SELECTORS);

  print('Interval:', t0 + '-' + t1);
  print('Intermediate years:', midYears);
  print('Diagnostic interval:', diagnosticInterval);
  print('Metric band count (expected 13):', metricImage.bandNames().size());
  print('Output column count (expected 28):', outputSelectors.length);

  Export.table.toDrive({
    collection: panel,
    description: outputName,
    fileNamePrefix: outputName,
    folder: DRIVE_FOLDER,
    fileFormat: 'CSV',
    selectors: outputSelectors
  });

  print('TASK CREATED:', outputName);
}

// ---------------------------------------------------------------------------
// Lightweight setup checks and seven export tasks
// ---------------------------------------------------------------------------

print('CANONICAL NAT-TMP WITHIN-INTERVAL PRODUCTION - VERSION 1');
print('Coverage asset:', K.COVERAGE_ASSET);
print('Canonical grid asset:', K.ANALYTICAL_GRID);
print('Expected domain cell count:', EXPECTED_DOMAIN_CELLS);
print('Full-domain cell count (expected 24,889):', grid.size());
print('Output version:', OUTPUT_VERSION);
print('2005-2010 is omitted because the pilot is already validated.');
print('Heavy results are intentionally not evaluated in the Console.');

INTERVALS.forEach(function (interval) {
  createIntervalExport(interval[0], interval[1]);
});

print('SEVEN TASKS CREATED.');
print('Run each task and retain all CSV files plus task metadata.');

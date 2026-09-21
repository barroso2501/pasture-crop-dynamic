/**
 * 15b_export_fixed_1985_pasture_cohort_v1.js
 *
 * Phase 9 gap-resolution extraction for RQ1.
 *
 * The fixed cohort is defined once as pixels that are:
 *   1. planted pasture in the 1985 coverage map; and
 *   2. pasture-age code 100 in 1985.
 *
 * The same pixels are classified at the nine reference years into the same
 * nine exhaustive land-cover states used by the canonical stock-flow panel.
 * This is a new longitudinal extraction. It does not change the canonical
 * domain, recompute interval flows, or alter earlier products.
 *
 * Run pilot first. After pilot validation, change RUN_MODE to 'full'.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// User setting
// ---------------------------------------------------------------------------

var RUN_MODE = 'pilot';  // 'pilot' or 'full'

// ---------------------------------------------------------------------------
// Frozen configuration
// ---------------------------------------------------------------------------

var SCRIPT_VERSION = 'phase9-fixed-1985-pasture-cohort-export-v1';
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';
var PILOT_BATCH_ID = 0;
var EXPECTED_PILOT_CELLS = 3168;
var EXPECTED_FULL_CELLS = K.EXPECTED_ANALYTICAL_CELL_COUNT;
var MAX_PIXELS_PER_REGION = 30000000;
var TILE_SCALE = 8;
var MASKED_VALUE = -9999;

var YEARS = K.MARK_YEARS;
var STATE_NAMES = [
  'nat', 'pas', 'tmp', 'oag', 'out',
  'water', 'nodata', 'unexpected', 'masked'
];

if (RUN_MODE !== 'pilot' && RUN_MODE !== 'full') {
  throw new Error("RUN_MODE must be 'pilot' or 'full'");
}

var outputName = RUN_MODE === 'pilot'
  ? 'canonical_fixed_1985_pasture_cohort_states_b00_v1'
  : 'canonical_fixed_1985_pasture_cohort_states_full_v1';

var expectedCells = RUN_MODE === 'pilot'
  ? EXPECTED_PILOT_CELLS
  : EXPECTED_FULL_CELLS;

var fullGrid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var grid = RUN_MODE === 'pilot'
  ? fullGrid.filter(ee.Filter.eq('source_batch_id', PILOT_BATCH_ID))
  : fullGrid;

var coverage = ee.Image(K.COVERAGE_ASSET);
var pastureAge = ee.Image(K.PASTURE_AGE_ASSET);
var pixelAreaHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);

// ---------------------------------------------------------------------------
// Shared state logic — identical class groups to the stock-flow panel
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
  return mask.multiply(pixelAreaHa).rename(name).unmask(0);
}

function propertySum(feature, names) {
  var total = ee.Number(0);
  names.forEach(function(name) {
    total = total.add(ee.Number(feature.get(name)));
  });
  return total;
}

function stateBandName(year, state) {
  return 'cohort_' + year + '_' + state + '_ha';
}

// ---------------------------------------------------------------------------
// Fixed cohort and endpoint-state bands
// ---------------------------------------------------------------------------

var coverage1985 = coverage
  .select(K.coverageBandName(K.FIRST_YEAR))
  .toInt16()
  .unmask(MASKED_VALUE);
var age1985 = pastureAge
  .select([K.ageBandIndex(K.FIRST_YEAR)])
  .toInt16()
  .unmask(MASKED_VALUE);

var states1985 = stateMasks(coverage1985);
var fixedCohort = states1985.pas.and(
  age1985.eq(K.PASTURE_AGE_INITIAL_STOCK_CODE)
);

var bands = [areaBand(fixedCohort, 'cohort_total_ha')];
var selectors = [
  'cell_id', 'GRID_ID', 'source_batch_id',
  'cohort_extraction_version', 'cohort_definition', 'run_mode',
  'cohort_total_ha'
];

YEARS.forEach(function(year) {
  var filled = coverage
    .select(K.coverageBandName(year))
    .toInt16()
    .unmask(MASKED_VALUE);
  var states = stateMasks(filled);

  STATE_NAMES.forEach(function(state) {
    var name = stateBandName(year, state);
    bands.push(areaBand(fixedCohort.and(states[state]), name));
    selectors.push(name);
  });

  selectors.push('cohort_' + year + '_state_total_ha');
  selectors.push('cohort_' + year + '_closure_residual_ha');
});

var metrics = ee.Image.cat(bands);

var reduced = metrics.reduceRegions({
  collection: grid,
  reducer: ee.Reducer.sum(),
  crs: K.CRS,
  crsTransform: K.CRS_TRANSFORM,
  tileScale: TILE_SCALE,
  maxPixelsPerRegion: MAX_PIXELS_PER_REGION
});

var output = reduced.map(function(feature) {
  feature = ee.Feature(feature);
  var cohortTotal = ee.Number(feature.get('cohort_total_ha'));
  var additions = {
    cohort_extraction_version: SCRIPT_VERSION,
    cohort_definition:
      'coverage_1985_is_pas_and_pasture_age_1985_equals_100',
    run_mode: RUN_MODE
  };

  YEARS.forEach(function(year) {
    var names = STATE_NAMES.map(function(state) {
      return stateBandName(year, state);
    });
    var stateTotal = propertySum(feature, names);
    additions['cohort_' + year + '_state_total_ha'] = stateTotal;
    additions['cohort_' + year + '_closure_residual_ha'] =
      cohortTotal.subtract(stateTotal);
  });

  return feature.set(additions);
});

// ---------------------------------------------------------------------------
// Lightweight setup diagnostics
// ---------------------------------------------------------------------------

var observedCells = output.size();
var uniqueCellIds = output.aggregate_count_distinct('cell_id');
var baselinePasture = ee.Number(
  output.aggregate_sum('cohort_1985_pas_ha')
);
var baselineCohort = ee.Number(output.aggregate_sum('cohort_total_ha'));
var baselineDifference = baselineCohort.subtract(baselinePasture).abs();

print('PHASE 9 RQ1 FIXED 1985 PASTURE COHORT EXPORT — VERSION 1');
print('Run mode:', RUN_MODE);
print('Script version:', SCRIPT_VERSION);
print('Canonical grid:', K.ANALYTICAL_GRID);
print('Coverage asset:', K.COVERAGE_ASSET);
print('Pasture-age asset:', K.PASTURE_AGE_ASSET);
print('Expected cells:', expectedCells);
print('Observed cells:', observedCells);
print('Unique cell_id:', uniqueCellIds);
print('Initial fixed-cohort area (ha):', baselineCohort);
print('Baseline PAS area (ha):', baselinePasture);
print('Baseline cohort minus PAS absolute difference (ha):', baselineDifference);
print('First output feature:', output.first());

Export.table.toDrive({
  collection: output,
  description: outputName,
  fileNamePrefix: outputName,
  folder: DRIVE_FOLDER,
  fileFormat: 'CSV',
  selectors: selectors
});

print('ONE TASK CREATED:', outputName);
print('Start the task only when observed and unique cell counts equal expected.');

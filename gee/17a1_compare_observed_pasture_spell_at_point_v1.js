/**
 * Observed pasture-spell reconstruction at one known problematic pixel.
 * Paste this entire file into the Google Earth Engine Code Editor.
 * Creates one CSV task with 41 annual records; no assets are modified.
 * Requires the synchronized project constants module.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');
var SCRIPT_VERSION = 'observed-pasture-spell-point-diagnostic-v1';
var LON = -55.164051;
var LAT = -20.281475;
var POINT = ee.Geometry.Point([LON, LAT]); // Earth Engine uses [longitude, latitude].
var FOLDER = 'pasture_spell_remediation_pilot_v1';
var OUTPUT = 'observed_pasture_spell_point_history_v1';
var MISSING = -9999;
var SOURCE_CODES = K.expectedSourceCodes();

// Origin state: 0 observed non-PAS; 1 continuous since 1985;
// 2 observed entry after a valid non-PAS year;
// 3 unresolved current PAS episode; 4 uncertain annual coverage.
var S = {NONPAS:0, INITIAL:1, NEW:2, UNRESOLVED:3, UNCERTAIN:4};
var LABEL = {
  0:'not_pasture', 1:'initial_1985_continuous_stock',
  2:'post_1985_observed_entry', 3:'unresolved_episode_origin',
  4:'uncertain_coverage'
};

function observedKind(code) {
  if (code === 15) return 'pas';
  if (code === MISSING || code === 27 ||
      SOURCE_CODES.indexOf(code) === -1) return 'uncertain';
  return 'non_pas';
}

// Independent client-side reconstruction from the 41 annual coverage values
// sampled at precisely one native-grid pixel. Source age never enters this rule.
function nextState(previous, observed, firstYear, year) {
  var result = {state:S.UNCERTAIN, age:0, entryYear:0,
    terminationYear:0};
  if (observed === 'uncertain') return result;
  if (observed === 'non_pas') {
    result.state = S.NONPAS;
    if (!firstYear && [S.INITIAL,S.NEW,S.UNRESOLVED]
        .indexOf(previous.state) !== -1) result.terminationYear = year;
    return result;
  }
  if (firstYear || previous.state === S.INITIAL) {
    result.state = S.INITIAL;
    result.age = 100;
  } else if (previous.state === S.NONPAS) {
    result.state = S.NEW;
    result.age = 201;
    result.entryYear = year;
  } else if (previous.state === S.NEW) {
    result.state = S.NEW;
    result.age = previous.age + 1;
  } else {
    result.state = S.UNRESOLVED;
  }
  return result;
}

var coverage = ee.Image(K.COVERAGE_ASSET);
var sourceAge = ee.Image(K.PASTURE_AGE_ASSET);
var years = [];
var bands = [];
for (var y = 1985; y <= 2025; y++) {
  years.push(y);
  // Unmask makes source gaps explicit, separately for the two products.
  bands.push(coverage.select(K.coverageBandName(y))
    .unmask(MISSING).toInt16().rename('coverage_' + y));
  bands.push(sourceAge.select([K.ageBandIndex(y)])
    .unmask(MISSING).toInt16().rename('source_age_' + y));
}

print('PASTURE-SPELL KNOWN-PIXEL AUDIT');
print('Version:', SCRIPT_VERSION);
print('Coordinates longitude/latitude:', LON, LAT);
print('Coverage asset:', K.COVERAGE_ASSET);
print('Pasture-age asset (comparison only):', K.PASTURE_AGE_ASSET);
print('Expected sampled bands:', 82);

// One synchronous small read is deliberate: it permits a readable 41-row
// client-side audit and makes task creation conditional on a complete sample.
// crsTransform is the numeric six-element native coverage affine transform.
var sample = ee.Image.cat(bands).reduceRegion({
  reducer:ee.Reducer.first(),
  geometry:POINT,
  crs:K.CRS,
  crsTransform:K.CRS_TRANSFORM,
  maxPixels:1000
}).getInfo();
if (!sample) throw new Error('No sample returned at the selected coordinate');

var rows = [];
var previous = {state:S.UNCERTAIN, age:0};
var raw100AfterEntry = 0;
var rawCode1Pasture = 0;
years.forEach(function (year, i) {
  var coverageCode = sample['coverage_' + year];
  var ageCode = sample['source_age_' + year];
  if (coverageCode === undefined || ageCode === undefined ||
      coverageCode === null || ageCode === null) {
    throw new Error('Incomplete sample at year ' + year);
  }
  var kind = observedKind(coverageCode);
  var result = nextState(previous, kind, i === 0, year);
  var conflict100 = coverageCode === 15 && ageCode === 100 &&
    result.state === S.NEW ? 1 : 0;
  var code1 = coverageCode === 15 && ageCode === 1 ? 1 : 0;
  raw100AfterEntry += conflict100;
  rawCode1Pasture += code1;
  rows.push({
    year:year, longitude:LON, latitude:LAT,
    coverage_code:coverageCode,
    observed_kind:kind,
    source_pasture_age_code:ageCode,
    reconstructed_origin_code:result.state,
    reconstructed_origin:LABEL[result.state],
    reconstructed_aux_age:result.age || MISSING,
    observed_entry_year:result.entryYear || MISSING,
    observed_termination_year:result.terminationYear || MISSING,
    boundary_adjacent_event:(year >= 2024 &&
      (result.entryYear || result.terminationYear)) ? 1 : 0,
    source_100_after_observed_entry:conflict100,
    source_code_1_on_pasture:code1,
    script_version:SCRIPT_VERSION
  });
  previous = result;
});

print('41 annual rows:', rows.length);
print('Source 100 while reconstructed episode is post-1985:',
  raw100AfterEntry);
print('Source 1 while coverage is PAS:', rawCode1Pasture);
print('FULL ANNUAL AUDIT (expand each row):', rows);

var features = ee.FeatureCollection(rows.map(function (r) {
  return ee.Feature(null, r);
}));
print('One 41-row CSV task will be created:', OUTPUT);
Export.table.toDrive({
  collection:features,
  description:OUTPUT,
  folder:FOLDER,
  fileNamePrefix:OUTPUT,
  fileFormat:'CSV',
  selectors:[
    'year','longitude','latitude','coverage_code','observed_kind',
    'source_pasture_age_code','reconstructed_origin_code',
    'reconstructed_origin','reconstructed_aux_age','observed_entry_year',
    'observed_termination_year','boundary_adjacent_event',
    'source_100_after_observed_entry','source_code_1_on_pasture',
    'script_version'
  ]
});

Map.centerObject(POINT, 15);
Map.addLayer(POINT, {color:'red'}, 'Known problematic pixel');

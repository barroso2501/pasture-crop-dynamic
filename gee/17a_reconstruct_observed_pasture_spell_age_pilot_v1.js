/**
 * PHASE 9 PASTURE-SPELL RECONSTRUCTION — STEP 1 / SMALL-TILE PREFLIGHT v1
 *
 * Run in the Earth Engine Code Editor with the project's synchronized
 * users/barroso2501/pasture-crop:lib/constants module.
 *
 * This is NOT a canonical full-domain output. It verifies the chronological
 * state engine on synthetic histories and exports one small tile for runtime,
 * size, and raster inspection. Start the single Drive task after the console
 * reports SYNTHETIC ENGINE: PASS and the expected 86 image bands.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');
var VERSION = 'observed-pasture-spell-step1-pilot-v1';
var FOLDER = 'pasture_spell_remediation_pilot_v1';
var NAME = 'observed_pasture_spell_preflight_tile_v1';
var START = 1985;
var END = 2025;
var MISSING = -9999;

// The diagnostic point is a tile locator, not a training or scientific sample.
// Change the coordinate only if its small neighbourhood falls outside the
// canonical analytical domain. Do not use this tile to estimate study totals.
var POINT = ee.Geometry.Point([-58.25, -16.66]);
var TILE = POINT.buffer(1200).bounds();

// Both states and annual observation status are explicit:
// 0 = confident non-PAS; 1 = continuous 1985 PAS; 2 = observed post-1985
// entry PAS; 3 = unresolved-origin PAS; 4 = uncertain annual coverage.
var S = {NONPAS: 0, INITIAL: 1, NEW: 2, UNRESOLVED: 3, UNCERTAIN: 4};
var PAS = 15;
var NODATA = 27;
var SOURCE_CODES = K.expectedSourceCodes();

function observation(value) {
  if (value === PAS) return 'PAS';
  if (value === MISSING || value === NODATA ||
      SOURCE_CODES.indexOf(value) === -1) return 'UNCERTAIN';
  return 'NONPAS';
}

function advance(previous, currentObservation, firstYear, year) {
  var state;
  var age = 0;
  var entry = 0;
  var termination = 0;
  if (currentObservation === 'UNCERTAIN') {
    state = S.UNCERTAIN;
  } else if (currentObservation === 'NONPAS') {
    state = S.NONPAS;
    termination = !firstYear && [S.INITIAL, S.NEW, S.UNRESOLVED]
      .indexOf(previous.state) !== -1 ? year : 0;
  } else if (firstYear || previous.state === S.INITIAL) {
    state = S.INITIAL;
    age = 100;
  } else if (previous.state === S.NONPAS) {
    state = S.NEW;
    age = 201;
    entry = year;
  } else if (previous.state === S.NEW) {
    state = S.NEW;
    age = previous.age + 1;
  } else {
    state = S.UNRESOLVED;
  }
  return {state: state, age: age, entry: entry,
    termination: termination};
}

function runSynthetic(codes) {
  var p = {state: S.UNCERTAIN, age: 0};
  return codes.map(function (v, i) {
    p = advance(p, observation(v), i === 0, START + i);
    return p.state === S.UNCERTAIN ? 'uncertain' :
      p.state === S.UNRESOLVED ? 'unresolved' :
      p.state === S.NONPAS ? 'NA' : p.age;
  });
}

var cases = [
  [[15,15,15], [100,100,100]],
  [[15,15,39,15,15], [100,100,'NA',201,202]],
  [[3,15,15,3,15], ['NA',201,202,'NA',201]],
  [[15,3,15,3,15], [100,'NA',201,'NA',201]],
  [[15,27,15], [100,'uncertain','unresolved']],
  [[39,15,27,15], ['NA',201,'uncertain','unresolved']],
  [[27,15,15], ['uncertain','unresolved','unresolved']],
  [[MISSING,15,3,15], ['uncertain','unresolved','NA',201]],
  [[15,27,15,3,15], [100,'uncertain','unresolved','NA',201]],
  [[15,999,15], [100,'uncertain','unresolved']]
];
cases.forEach(function (c, i) {
  var found = runSynthetic(c[0]);
  if (JSON.stringify(found) !== JSON.stringify(c[1])) {
    throw new Error('Synthetic case ' + (i + 1) + ' failed: ' +
      JSON.stringify(found) + ' != ' + JSON.stringify(c[1]));
  }
});
var boundary = advance({state:S.NONPAS,age:0},'PAS',false,2024);
var exit = advance({state:S.NEW,age:201},'NONPAS',false,2025);
if (boundary.entry !== 2024 || exit.termination !== 2025) {
  throw new Error('Boundary-event year check failed');
}
print('PASTURE-SPELL RECONSTRUCTION — STEP 1 PILOT');
print('Script version:', VERSION);
print('SYNTHETIC ENGINE: PASS; cases:', cases.length);
print('2024 entry and 2025 termination event-year check: PASS');

var source = ee.Image(K.COVERAGE_ASSET);
var accepted = ee.FeatureCollection(K.ANALYTICAL_GRID);
var pilotCells = accepted.filterBounds(TILE);
var domain = ee.Image.constant(0).byte()
  .paint(pilotCells, 1).eq(1).unmask(0);

function validNonPasture(cov) {
  var valid = ee.Image.constant(0).eq(1);
  SOURCE_CODES.forEach(function (code) {
    if (code !== PAS && code !== NODATA) valid = valid.or(cov.eq(code));
  });
  return valid;
}

var previous = {state:ee.Image.constant(S.UNCERTAIN).byte(),
  age:ee.Image.constant(0).int16()};
var bands = [];
var years = [];
for (var y = START; y <= END; y++) years.push(y);

years.forEach(function (year) {
  var raw = source.select('classification_' + year);
  var cov = raw.unmask(MISSING).toInt16();
  var pas = cov.eq(PAS);
  var non = validNonPasture(cov);
  var initial = year === START ? pas :
    pas.and(previous.state.eq(S.INITIAL));
  var entry = year === START ? ee.Image.constant(0).eq(1) :
    pas.and(previous.state.eq(S.NONPAS));
  var continuation = year === START ? ee.Image.constant(0).eq(1) :
    pas.and(previous.state.eq(S.NEW));
  var unresolved = pas.and(initial.not()).and(entry.not())
    .and(continuation.not());
  var end = year === START ? ee.Image.constant(0).eq(1) :
    non.and(previous.state.eq(S.INITIAL)
      .or(previous.state.eq(S.NEW))
      .or(previous.state.eq(S.UNRESOLVED)));

  var state = ee.Image.constant(S.UNCERTAIN).byte()
    .where(non, S.NONPAS).where(initial, S.INITIAL)
    .where(entry.or(continuation), S.NEW)
    .where(unresolved, S.UNRESOLVED);
  var age = ee.Image.constant(0).int16()
    .where(initial, 100)
    .where(entry, 201)
    .where(continuation, previous.age.add(1));

  bands.push(state.rename('origin_' + year));
  bands.push(age.rename('age_' + year));
  if (year === 2024 || year === 2025) {
    bands.push(entry.byte().rename('entry_boundary_adjacent_' + year));
    bands.push(end.byte().rename('termination_boundary_adjacent_' + year));
  }
  previous = {state:state, age:age};
});

// GeoTIFF export requires a uniform band type; categorical and age bands all
// fit safely into signed 16-bit integers (maximum observed age code = 240).
var image = ee.Image.cat(bands).toInt16().updateMask(domain).clip(TILE);
print('Expected bands:', 86);
print('Actual band count (must be 86):', image.bandNames().size());
print('Canonical cells intersecting pilot tile (must be >0):',
  pilotCells.size());
print('First and last bands:', image.bandNames().slice(0, 4),
  image.bandNames().slice(-4));
print('Pilot bounds (not the full study domain):', TILE);

Map.centerObject(POINT, 12);
Map.addLayer(pilotCells, {}, 'Canonical cells intersecting tile');
Map.addLayer(image.select('origin_2020'),
  {min:0,max:4,palette:['444444','8050a0','f2b341','c4288a','c9d1d9']},
  'Reconstructed origin 2020 — pilot');

// One explicitly small export; inspect task runtime/size before choosing
// full-domain tiling. The .tif has 41 origin + 41 auxiliary age bands and
// four event-year bands. It is not an accepted study-wide analytical output.
Export.image.toDrive({
  image:image,
  description:NAME,
  folder:FOLDER,
  fileNamePrefix:NAME,
  region:TILE,
  crs:K.CRS,
  crsTransform:K.CRS_TRANSFORM,
  maxPixels:1e7,
  fileFormat:'GeoTIFF',
  formatOptions:{cloudOptimized:true}
});
print('ONE SMALL-TILE TASK CREATED:', NAME);
print('Run it after band-count and tile-domain checks; report runtime, size,');
print('task status, console output, and GeoTIFF for independent inspection.');

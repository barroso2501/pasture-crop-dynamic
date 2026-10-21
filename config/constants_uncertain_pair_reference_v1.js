/**
 * Canonical constants for pasture-crop-dynamic.
 *
 * This file is the single source of truth for MapBiomas assets, years,
 * projection parameters, class groups, and core project assets.
 *
 * Google Earth Engine scripts should import a synchronized copy of this file
 * as a GEE module. Do not maintain independent class lists inside analysis
 * scripts.
 */

// ---------------------------------------------------------------------------
// Canonical public MapBiomas Collection 11 assets
// ---------------------------------------------------------------------------

exports.COVERAGE_ASSET =
  'projects/mapbiomas-public/assets/brazil/lulc/collection11/' +
  'mapbiomas_brazil_collection11_coverage_v3';

exports.PASTURE_AGE_ASSET =
  'projects/mapbiomas-public/assets/brazil/lulc/collection11/' +
  'mapbiomas_brazil_collection11_pasture_age_v1';

exports.COVERAGE_BAND_PREFIX = 'classification_';

// Provenance only. Never use this source for canonical outputs.
exports.HISTORICAL_COVERAGE_ASSET =
  'projects/mapbiomas-brazil/assets/LAND-COVER/COLLECTION-11/' +
  'INTEGRATION/classification-ft';
exports.HISTORICAL_WORKING_VERSION = '0-4-13-w3y-5';

// ---------------------------------------------------------------------------
// Canonical project assets
// ---------------------------------------------------------------------------

// Canonical fixed analytical domain reconstructed and validated on 2026-09-11.
exports.ANALYTICAL_GRID =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3';

// Provenance only. Do not use for canonical reprocessing.
exports.HISTORICAL_ANALYTICAL_GRID =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao';

exports.PARENT_GRID =
  'projects/ee-barroso2501/assets/grade_20mil_ha';

exports.BIOMES_ASSET =
  'projects/ee-barroso2501/assets/biomas_IBGE';

exports.CANDIDATE_GRID =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_candidates_ibge2025';

exports.CANONICAL_DOMAIN_MEMBERSHIP =
  'projects/ee-barroso2501/assets/canonical_domain_membership_c11_v3';

exports.BIOME_CODE_FIELD = 'CD_BIOMA';
exports.TARGET_BIOME_CODES = ['1', '3'];
exports.TARGET_BIOME_NAMES = {
  '1': 'Amazonia',
  '3': 'Cerrado'
};

exports.EXPECTED_ANALYTICAL_CELL_COUNT = 24889;
exports.EXPECTED_CANDIDATE_CELL_COUNT = 32305;
exports.CELL_ID_FIELD = 'cell_id';
exports.REFERENCE_CELL_AREA_HA = 20000;
exports.ENDPOINT_TOLERANCE_HA = 0.01;

// ---------------------------------------------------------------------------
// Temporal framework
// ---------------------------------------------------------------------------

exports.FIRST_YEAR = 1985;
exports.LAST_YEAR = 2025;
exports.MAIN_INFERENCE_LAST_YEAR = 2020;

exports.MARK_YEARS = [
  1985, 1990, 1995, 2000, 2005,
  2010, 2015, 2020, 2025
];

exports.DIAGNOSTIC_INTERVAL = [2020, 2025];

exports.ageBandIndex = function (year) {
  if (year < exports.FIRST_YEAR || year > exports.LAST_YEAR) {
    throw new Error('Pasture-age year outside the 1985–2025 series: ' + year);
  }
  return year - exports.FIRST_YEAR;
};

exports.coverageBandName = function (year) {
  if (year < exports.FIRST_YEAR || year > exports.LAST_YEAR) {
    throw new Error('Coverage year outside the 1985–2025 series: ' + year);
  }
  return exports.COVERAGE_BAND_PREFIX + year;
};

// ---------------------------------------------------------------------------
// Canonical MapBiomas raster grid
// ---------------------------------------------------------------------------

exports.CRS = 'EPSG:4326';

// Native affine transform of the canonical Collection 11 coverage asset.
// The pasture-age asset has the same pixel size and pixel lattice: its stored
// origin differs by exactly 76 columns and 2,205 rows. Keeping the coverage
// transform as the project reference avoids subpixel resampling during area,
// stock, and flow calculations.
//
// Do not replace this transform with the former global-origin transform
// [-180, 90]. That origin is not aligned to the native Collection 11 lattice.
exports.CRS_TRANSFORM = [
  0.00026949458523585647, 0, -74.02073025380652,
  0, -0.00026949458523585647, 5.405791885246045
];

exports.SQUARE_METRES_PER_HECTARE = 10000;

// ---------------------------------------------------------------------------
// Canonical Collection 11 class groups
// ---------------------------------------------------------------------------

exports.CLASS_CODES = {
  NAT: [1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 29, 32, 49, 50, 84],
  PAS: [15],
  TMP: [19, 20, 39, 40, 41, 62],
  OAG: [9, 21, 35, 36, 46, 47, 48],
  OUT: [22, 23, 24, 25, 30, 75, 91],
  WATER: [26, 31, 33],
  NODATA: [27]
};

// Compact internal values used only when a reclassified raster is required.
exports.INTERNAL_CLASS = {
  NODATA: 0,
  NAT: 1,
  PAS: 2,
  TMP: 3,
  OAG: 4,
  OUT: 5,
  WATER: 6
};

exports.FOCAL_GROUPS = ['NAT', 'PAS', 'TMP'];
exports.AUXILIARY_GROUPS = ['OAG', 'OUT', 'WATER'];

// ---------------------------------------------------------------------------
// Pasture-age encoding
// ---------------------------------------------------------------------------

exports.PASTURE_AGE_INITIAL_STOCK_CODE = 100;
exports.PASTURE_AGE_OFFSET = 200;

// Observed in the public pasture-age asset but not defined by the documented
// 100/2xx encoding. MapBiomas confirmed that this value is unexpected and is
// investigating it. Do not reinterpret it as age 1 or code 201.
exports.PASTURE_AGE_UNRESOLVED_CODES = [1];

exports.isInitialPastureAgeCode = function (value) {
  return value === exports.PASTURE_AGE_INITIAL_STOCK_CODE;
};

exports.isUnresolvedPastureAgeCode = function (value) {
  return exports.PASTURE_AGE_UNRESOLVED_CODES.indexOf(value) !== -1;
};

exports.decodePastureAge = function (value) {
  // Unresolved and initial-stock codes deliberately return null. Only 2xx
  // values have an attributable consecutive age in the current workflow.
  if (value > exports.PASTURE_AGE_OFFSET) {
    return value - exports.PASTURE_AGE_OFFSET;
  }
  return null;
};

// ---------------------------------------------------------------------------
// Reclassification helpers
// ---------------------------------------------------------------------------

exports.remapVectors = function () {
  var from = [];
  var to = [];
  var groups = ['NAT', 'PAS', 'TMP', 'OAG', 'OUT', 'WATER'];

  for (var i = 0; i < groups.length; i++) {
    var groupName = groups[i];
    var codes = exports.CLASS_CODES[groupName];
    var target = exports.INTERNAL_CLASS[groupName];

    for (var j = 0; j < codes.length; j++) {
      from.push(codes[j]);
      to.push(target);
    }
  }

  return {from: from, to: to};
};

exports.expectedSourceCodes = function () {
  var groups = ['NAT', 'PAS', 'TMP', 'OAG', 'OUT', 'WATER', 'NODATA'];
  var values = [];

  for (var i = 0; i < groups.length; i++) {
    values = values.concat(exports.CLASS_CODES[groups[i]]);
  }

  values.sort(function (a, b) { return a - b; });
  return values;
};

// ---------------------------------------------------------------------------
// Output conventions
// ---------------------------------------------------------------------------

exports.OUTPUT_VERSION = 'canonical-c11-coverage-v3-native-grid';

exports.intervalLabel = function (year0, year1) {
  return year0 + '_' + year1;
};

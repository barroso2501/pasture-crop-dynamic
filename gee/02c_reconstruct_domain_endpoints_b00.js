/**
 * 02c_reconstruct_domain_endpoints_b00.js - version 1
 *
 * Pilot reconstruction of the canonical analytical domain for batch b00.
 *
 * The script reads the materialized Cerrado-Amazon candidate grid directly.
 * It does not repeat the biome spatial join and it does not use the historical
 * grid to determine membership.
 *
 * ONLY ONE TASK IS CREATED:
 *   canonical_domain_endpoints_c11_v3_b00_v1
 *
 * Do not create or run batches b01-b07 until this pilot output, runtime, and
 * compute use have been reviewed.
 */

// ---------------------------------------------------------------------------
// 0. Canonical configuration
// ---------------------------------------------------------------------------

var K = require(
  'users/barroso2501/pasture-crop:lib/constants.js'
);

var CANDIDATE_GRID_ASSET =
  'projects/ee-barroso2501/assets/' +
  'grade_hex_CeAmz_candidates_ibge2025';

var DRIVE_FOLDER = 'pasture_crop_dynamic_audits';
var OUTPUT_PREFIX =
  'canonical_domain_endpoints_c11_v3_b00_v1';

var PILOT_BATCH_ID = 0;
var EXPECTED_PILOT_CELL_COUNT = 4040;
var BATCH_COUNT = 8;
var SCRIPT_VERSION = 1;

var ENDPOINT_YEARS = [1985, 2025];
var ENDPOINT_TOLERANCE_HA = K.ENDPOINT_TOLERANCE_HA;
var TRANSFORM_TEXT = K.CRS_TRANSFORM.join(',');

// ---------------------------------------------------------------------------
// 1. Inputs
// ---------------------------------------------------------------------------

var coverage = ee.Image(K.COVERAGE_ASSET);
var candidateGrid = ee.FeatureCollection(
  CANDIDATE_GRID_ASSET
);

// batch_id was stored when the candidate asset was materialized. Filtering a
// stored property avoids rebuilding a spatial join inside the raster graph.
var pilotGrid = candidateGrid.filter(
  ee.Filter.eq('batch_id', PILOT_BATCH_ID)
);

var pixelAreaHa = ee.Image.pixelArea()
  .divide(K.SQUARE_METRES_PER_HECTARE);

// ---------------------------------------------------------------------------
// 2. Canonical code groups
// ---------------------------------------------------------------------------

var anthropogenicCodes = K.CLASS_CODES.PAS
  .concat(K.CLASS_CODES.TMP)
  .concat(K.CLASS_CODES.OAG)
  .concat(K.CLASS_CODES.OUT);

var naturalWaterCodes = K.CLASS_CODES.NAT
  .concat(K.CLASS_CODES.WATER);

var expectedCodes = anthropogenicCodes
  .concat(naturalWaterCodes)
  .concat(K.CLASS_CODES.NODATA);

function binaryTargets(codes) {
  return codes.map(function() {
    return 1;
  });
}

function inCodes(image, codes) {
  return image.remap(
    codes,
    binaryTargets(codes),
    0
  ).eq(1);
}

function areaBand(mask, name) {
  return pixelAreaHa
    .multiply(ee.Image(mask).unmask(0))
    .rename(name);
}

// ---------------------------------------------------------------------------
// 3. Endpoint audit bands
// ---------------------------------------------------------------------------

function endpointBands(year) {
  var cov = coverage.select(
    K.coverageBandName(year)
  );

  var valid = cov.mask().gt(0);

  var anthropogenic = valid.and(
    inCodes(cov, anthropogenicCodes)
  );

  var naturalWater = valid.and(
    inCodes(cov, naturalWaterCodes)
  );

  var noData = valid.and(
    inCodes(cov, K.CLASS_CODES.NODATA)
  );

  var expected = inCodes(cov, expectedCodes);

  var unexpected = valid.and(
    expected.not()
  );

  return ee.Image.cat([
    areaBand(
      anthropogenic,
      'anthropogenic_' + year + '_ha'
    ),
    areaBand(
      naturalWater,
      'natural_water_' + year + '_ha'
    ),
    areaBand(
      noData,
      'nodata_' + year + '_ha'
    ),
    areaBand(
      unexpected,
      'unexpected_' + year + '_ha'
    ),
    areaBand(
      valid,
      'coverage_valid_' + year + '_ha'
    )
  ]);
}

var endpointImage = ee.Image.cat([
  endpointBands(ENDPOINT_YEARS[0]),
  endpointBands(ENDPOINT_YEARS[1])
]);

// ---------------------------------------------------------------------------
// 4. Raster reduction over the materialized pilot batch
// ---------------------------------------------------------------------------

var reduced = endpointImage.reduceRegions({
  collection: pilotGrid,
  reducer: ee.Reducer.sum(),
  crs: K.CRS,
  crsTransform: K.CRS_TRANSFORM,
  tileScale: 16,
  maxPixelsPerRegion: 5000000
});

// ---------------------------------------------------------------------------
// 5. Canonical membership and diagnostics
// ---------------------------------------------------------------------------

var pilotResult = reduced.map(function(feature) {
  feature = ee.Feature(feature);

  var anth1985 = ee.Number(
    feature.get('anthropogenic_1985_ha')
  );

  var anth2025 = ee.Number(
    feature.get('anthropogenic_2025_ha')
  );

  var maxAnthropogenic = anth1985.max(
    anth2025
  );

  var endpointPass = maxAnthropogenic.gt(
    ENDPOINT_TOLERANCE_HA
  );

  var reconstructedMember = ee.Number(
    ee.Algorithms.If(
      endpointPass,
      1,
      0
    )
  );

  var unexpectedMaximum = ee.Number(
    feature.get('unexpected_1985_ha')
  ).max(
    ee.Number(
      feature.get('unexpected_2025_ha')
    )
  );

  var unexpectedFlag = ee.Number(
    ee.Algorithms.If(
      unexpectedMaximum.gt(
        ENDPOINT_TOLERANCE_HA
      ),
      1,
      0
    )
  );

  var geometryAreaHa = feature
    .geometry()
    .area(1)
    .divide(
      K.SQUARE_METRES_PER_HECTARE
    );

  return feature
    .set(
      'geometry_area_ha',
      geometryAreaHa
    )
    .set(
      'max_endpoint_anthropogenic_ha',
      maxAnthropogenic
    )
    .set(
      'endpoint_rule_pass',
      reconstructedMember
    )
    .set(
      'reconstructed_member',
      reconstructedMember
    )
    .set(
      'unexpected_code_flag',
      unexpectedFlag
    )
    .set(
      'endpoint_tolerance_ha',
      ENDPOINT_TOLERANCE_HA
    )
    .set(
      'pilot_batch',
      1
    )
    .set(
      'script_version',
      SCRIPT_VERSION
    )
    .set(
      'coverage_asset',
      K.COVERAGE_ASSET
    )
    .set(
      'candidate_grid_asset',
      CANDIDATE_GRID_ASSET
    )
    .set(
      'processing_crs',
      K.CRS
    )
    .set(
      'processing_transform',
      TRANSFORM_TEXT
    );
});

// ---------------------------------------------------------------------------
// 6. Single pilot export
// ---------------------------------------------------------------------------

var selectors = [
  'cell_id',
  'GRID_ID',
  'batch_id',
  'batch_count',
  'historical_member',
  'pilot_batch',
  'geometry_area_ha',
  'anthropogenic_1985_ha',
  'anthropogenic_2025_ha',
  'max_endpoint_anthropogenic_ha',
  'natural_water_1985_ha',
  'natural_water_2025_ha',
  'nodata_1985_ha',
  'nodata_2025_ha',
  'unexpected_1985_ha',
  'unexpected_2025_ha',
  'coverage_valid_1985_ha',
  'coverage_valid_2025_ha',
  'unexpected_code_flag',
  'endpoint_rule_pass',
  'reconstructed_member',
  'endpoint_tolerance_ha',
  'script_version',
  'processing_crs',
  'processing_transform',
  'coverage_asset',
  'candidate_grid_asset'
];

Export.table.toDrive({
  collection: pilotResult,
  description: OUTPUT_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: OUTPUT_PREFIX,
  fileFormat: 'CSV',
  selectors: selectors
});

// ---------------------------------------------------------------------------
// 7. Lightweight execution guidance
// ---------------------------------------------------------------------------

print(
  'CANONICAL DOMAIN ENDPOINT PILOT - VERSION 1'
);

print(
  'Coverage asset:',
  K.COVERAGE_ASSET
);

print(
  'Candidate-grid asset:',
  CANDIDATE_GRID_ASSET
);

print(
  'Pilot batch:',
  PILOT_BATCH_ID
);

print(
  'Pilot cell count:',
  pilotGrid.size()
);

print(
  'Expected pilot cell count:',
  EXPECTED_PILOT_CELL_COUNT
);

print(
  'Endpoint years:',
  ENDPOINT_YEARS
);

print(
  'Endpoint tolerance (ha):',
  ENDPOINT_TOLERANCE_HA
);

print(
  'Output bands:',
  endpointImage.bandNames()
);

print(
  'ONE TASK CREATED:',
  OUTPUT_PREFIX
);

print(
  'Run only this task. Do not run b01-b07 yet.'
);
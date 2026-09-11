/**
 * 02e_reconstruct_domain_endpoints_b02_b07.js - version 1
 *
 * Canonical analytical-domain reconstruction for batches b02-b07.
 *
 * This script uses the lean two-band configuration validated with batch b01.
 * It reads the materialized candidate grid directly and calculates recognized
 * anthropogenic area only for 1985 and 2025.
 *
 * SIX INDEPENDENT TASKS ARE CREATED:
 *   canonical_domain_endpoints_c11_v3_b02_v1
 *   canonical_domain_endpoints_c11_v3_b03_v1
 *   canonical_domain_endpoints_c11_v3_b04_v1
 *   canonical_domain_endpoints_c11_v3_b05_v1
 *   canonical_domain_endpoints_c11_v3_b06_v1
 *   canonical_domain_endpoints_c11_v3_b07_v1
 *
 * Batches b00 and b01 are not recreated by this script.
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

var DRIVE_FOLDER =
  'pasture_crop_dynamic_audits';

var OUTPUT_BASE =
  'canonical_domain_endpoints_c11_v3';

var BATCH_COUNT = 8;
var SCRIPT_VERSION = 1;

var PROCESSING_CONFIGURATION =
  'lean_two_band';

var ENDPOINT_YEARS = [1985, 2025];

var ENDPOINT_TOLERANCE_HA =
  K.ENDPOINT_TOLERANCE_HA;

var TRANSFORM_TEXT =
  K.CRS_TRANSFORM.join(',');

// Only these batches are created. Counts come from the validated
// materialized candidate-grid audit and must sum to 24,224 cells.
var BATCHES = [
  {id: 2, expectedCount: 4034},
  {id: 3, expectedCount: 4043},
  {id: 4, expectedCount: 4038},
  {id: 5, expectedCount: 4036},
  {id: 6, expectedCount: 4037},
  {id: 7, expectedCount: 4036}
];

// ---------------------------------------------------------------------------
// 1. Inputs
// ---------------------------------------------------------------------------

var coverage = ee.Image(
  K.COVERAGE_ASSET
);

var candidateGrid = ee.FeatureCollection(
  CANDIDATE_GRID_ASSET
);

var pixelAreaHa = ee.Image.pixelArea()
  .divide(
    K.SQUARE_METRES_PER_HECTARE
  );

// ---------------------------------------------------------------------------
// 2. Recognized anthropogenic classes
// ---------------------------------------------------------------------------

var anthropogenicCodes =
  K.CLASS_CODES.PAS
    .concat(K.CLASS_CODES.TMP)
    .concat(K.CLASS_CODES.OAG)
    .concat(K.CLASS_CODES.OUT);

var anthropogenicTargets =
  anthropogenicCodes.map(function() {
    return 1;
  });

function anthropogenicAreaBand(year) {
  var cov = coverage.select(
    K.coverageBandName(year)
  );

  var anthropogenic = cov.remap(
    anthropogenicCodes,
    anthropogenicTargets,
    0
  ).eq(1);

  return pixelAreaHa
    .multiply(
      anthropogenic.unmask(0)
    )
    .rename(
      'anthropogenic_' + year + '_ha'
    );
}

var endpointImage = ee.Image.cat([
  anthropogenicAreaBand(
    ENDPOINT_YEARS[0]
  ),
  anthropogenicAreaBand(
    ENDPOINT_YEARS[1]
  )
]);

// ---------------------------------------------------------------------------
// 3. Batch calculation
// ---------------------------------------------------------------------------

function reconstructBatch(batchId) {
  var batchGrid = candidateGrid.filter(
    ee.Filter.eq(
      'batch_id',
      batchId
    )
  );

  var reduced = endpointImage.reduceRegions({
    collection: batchGrid,
    reducer: ee.Reducer.sum(),
    crs: K.CRS,
    crsTransform: K.CRS_TRANSFORM,
    tileScale: 16,
    maxPixelsPerRegion: 5000000
  });

  return reduced.map(function(feature) {
    feature = ee.Feature(feature);

    var anth1985 = ee.Number(
      feature.get(
        'anthropogenic_1985_ha'
      )
    );

    var anth2025 = ee.Number(
      feature.get(
        'anthropogenic_2025_ha'
      )
    );

    var maxAnthropogenic =
      anth1985.max(anth2025);

    var reconstructedMember =
      ee.Number(
        ee.Algorithms.If(
          maxAnthropogenic.gt(
            ENDPOINT_TOLERANCE_HA
          ),
          1,
          0
        )
      );

    var geometryAreaHa =
      feature
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
        'endpoint_tolerance_ha',
        ENDPOINT_TOLERANCE_HA
      )
      .set(
        'script_version',
        SCRIPT_VERSION
      )
      .set(
        'processing_configuration',
        PROCESSING_CONFIGURATION
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
}

// ---------------------------------------------------------------------------
// 4. Output schema
// ---------------------------------------------------------------------------

var selectors = [
  'cell_id',
  'GRID_ID',
  'batch_id',
  'batch_count',
  'historical_member',
  'geometry_area_ha',
  'anthropogenic_1985_ha',
  'anthropogenic_2025_ha',
  'max_endpoint_anthropogenic_ha',
  'endpoint_rule_pass',
  'reconstructed_member',
  'endpoint_tolerance_ha',
  'script_version',
  'processing_configuration',
  'processing_crs',
  'processing_transform',
  'coverage_asset',
  'candidate_grid_asset'
];

// ---------------------------------------------------------------------------
// 5. Create the six independent exports
// ---------------------------------------------------------------------------

BATCHES.forEach(function(batch) {
  var batchLabel =
    ('0' + batch.id).slice(-2);

  var outputPrefix =
    OUTPUT_BASE +
    '_b' +
    batchLabel +
    '_v1';

  var batchGrid = candidateGrid.filter(
    ee.Filter.eq(
      'batch_id',
      batch.id
    )
  );

  Export.table.toDrive({
    collection: reconstructBatch(
      batch.id
    ),
    description: outputPrefix,
    folder: DRIVE_FOLDER,
    fileNamePrefix: outputPrefix,
    fileFormat: 'CSV',
    selectors: selectors
  });

  print(
    'Batch b' +
      batchLabel +
      ' cell count:',
    batchGrid.size()
  );

  print(
    'Batch b' +
      batchLabel +
      ' expected count:',
    batch.expectedCount
  );
});

// ---------------------------------------------------------------------------
// 6. Lightweight execution guidance
// ---------------------------------------------------------------------------

print(
  'CANONICAL DOMAIN ENDPOINTS B02-B07 - VERSION 1'
);

print(
  'Processing configuration:',
  PROCESSING_CONFIGURATION
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
  'SIX TASKS CREATED: b02, b03, b04, b05, b06, b07.'
);

print(
  'Batches b00 and b01 are not recreated.'
);
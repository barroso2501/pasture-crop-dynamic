/**
 * 02d_reconstruct_domain_endpoints_b01.js - version 1
 *
 * Lean production-configuration test for canonical domain batch b01.
 *
 * The b00 pilot validated the endpoint rule and the additional coverage
 * diagnostics. This script reduces only the two bands required to determine
 * canonical membership: recognized anthropogenic area in 1985 and 2025.
 *
 * ONLY ONE TASK IS CREATED:
 *   canonical_domain_endpoints_c11_v3_b01_v1
 *
 * Run only this task. Compare its runtime and EECU use with b00 before
 * creating or running batches b02-b07.
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

var OUTPUT_PREFIX =
  'canonical_domain_endpoints_c11_v3_b01_v1';

var BATCH_ID = 1;
var EXPECTED_BATCH_CELL_COUNT = 4041;
var BATCH_COUNT = 8;
var SCRIPT_VERSION = 1;

var PROCESSING_CONFIGURATION =
  'lean_two_band';

var ENDPOINT_YEARS = [1985, 2025];

var ENDPOINT_TOLERANCE_HA =
  K.ENDPOINT_TOLERANCE_HA;

var TRANSFORM_TEXT =
  K.CRS_TRANSFORM.join(',');

// ---------------------------------------------------------------------------
// 1. Inputs
// ---------------------------------------------------------------------------

var coverage = ee.Image(
  K.COVERAGE_ASSET
);

var candidateGrid = ee.FeatureCollection(
  CANDIDATE_GRID_ASSET
);

// batch_id is a stored property in the materialized candidate asset.
// No biome intersection or historical-grid join is evaluated here.
var batchGrid = candidateGrid.filter(
  ee.Filter.eq(
    'batch_id',
    BATCH_ID
  )
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
// 3. Raster reduction over materialized batch b01
// ---------------------------------------------------------------------------

// The spatial parameters are unchanged from b00.
// This allows the effect of reducing the image from ten bands
// to two bands to be evaluated directly.
var reduced = endpointImage.reduceRegions({
  collection: batchGrid,
  reducer: ee.Reducer.sum(),
  crs: K.CRS,
  crsTransform: K.CRS_TRANSFORM,
  tileScale: 16,
  maxPixelsPerRegion: 5000000
});

// ---------------------------------------------------------------------------
// 4. Canonical membership
// ---------------------------------------------------------------------------

var batchResult = reduced.map(
  function(feature) {
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
  }
);

// ---------------------------------------------------------------------------
// 5. Single b01 export
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

Export.table.toDrive({
  collection: batchResult,
  description: OUTPUT_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: OUTPUT_PREFIX,
  fileFormat: 'CSV',
  selectors: selectors
});

// ---------------------------------------------------------------------------
// 6. Lightweight execution guidance
// ---------------------------------------------------------------------------

print(
  'CANONICAL DOMAIN ENDPOINT B01 - VERSION 1'
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
  'Batch ID:',
  BATCH_ID
);

print(
  'Batch cell count:',
  batchGrid.size()
);

print(
  'Expected batch cell count:',
  EXPECTED_BATCH_CELL_COUNT
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
  'Run only this task. Do not run b02-b07 yet.'
);
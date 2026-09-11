/**
 * 02a_materialize_candidate_grid.js - version 1
 *
 * Materializes the complete parent-grid hexagons that intersect the Amazonia
 * or Cerrado features of the IBGE 2025 biome layer.
 *
 * This is a vector-only prerequisite for analytical-domain reconstruction.
 * It breaks the dynamic spatial-join graph before any MapBiomas raster
 * reduction is attempted.
 *
 * The script creates a NEW asset. It does not overwrite the historical grid:
 *
 * projects/ee-barroso2501/assets/
 * grade_hex_CeAmz_candidates_ibge2025
 */

var K = require(
  'users/barroso2501/pasture-crop:lib/constants.js'
);

var CANDIDATE_GRID_ASSET =
  'projects/ee-barroso2501/assets/' +
  'grade_hex_CeAmz_candidates_ibge2025';

var BATCH_COUNT = 8;

var parentGrid = ee.FeatureCollection(K.PARENT_GRID);
var historicalGrid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var biomes = ee.FeatureCollection(K.BIOMES_ASSET);

var targetBiomes = biomes.filter(
  ee.Filter.inList(
    K.BIOME_CODE_FIELD,
    K.TARGET_BIOME_CODES
  )
);

var biomeIntersection = ee.Filter.intersects({
  leftField: '.geo',
  rightField: '.geo',
  maxError: 1
});

// Default outer=false is intentional: only intersecting parent cells remain.
// saveFirst ensures that a cell intersecting both biomes appears only once.
var intersectingParentCells = ee.FeatureCollection(
  ee.Join.saveFirst('_biome_match').apply(
    parentGrid,
    targetBiomes,
    biomeIntersection
  )
);

var idMatch = ee.Filter.equals({
  leftField: K.CELL_ID_FIELD,
  rightField: K.CELL_ID_FIELD
});

var joinedToHistoricalGrid = ee.FeatureCollection(
  ee.Join.saveFirst({
    matchKey: '_historical_match',
    outer: true
  }).apply(
    intersectingParentCells,
    historicalGrid,
    idMatch
  )
);

var candidateGrid = joinedToHistoricalGrid.map(function(feature) {
  feature = ee.Feature(feature);

  var historicalMember = ee.Number(ee.Algorithms.If(
    ee.Algorithms.IsEqual(
      feature.get('_historical_match'),
      null
    ),
    0,
    1
  ));

  var cellId = ee.Number(feature.get(K.CELL_ID_FIELD));

  // The partition is stored now so later raster scripts only need a simple
  // property filter on a materialized FeatureCollection.
  var batchId = cellId.mod(BATCH_COUNT);

  return ee.Feature(feature.geometry(), {
    cell_id: feature.get(K.CELL_ID_FIELD),
    GRID_ID: feature.get('GRID_ID'),
    historical_member: historicalMember,
    batch_id: batchId,
    batch_count: BATCH_COUNT,
    biome_code_field: K.BIOME_CODE_FIELD,
    target_biome_codes: K.TARGET_BIOME_CODES.join(','),
    selection_relation: 'INTERSECTS',
    parent_grid_asset: K.PARENT_GRID,
    historical_grid_asset: K.ANALYTICAL_GRID,
    biomes_asset: K.BIOMES_ASSET,
    materialization_version: 1
  });
});

Export.table.toAsset({
  collection: candidateGrid,
  description: 'materialize_ceamz_candidates_v1',
  assetId: CANDIDATE_GRID_ASSET
});

print('CANDIDATE-GRID MATERIALIZATION VERSION 1');
print('Output asset:', CANDIDATE_GRID_ASSET);
print('Parent-grid cell count:', parentGrid.size());
print('Target-biome feature count:', targetBiomes.size());
print('Historical analytical-grid count:', historicalGrid.size());
print('Candidate count:', candidateGrid.size());
print('First candidate:', candidateGrid.first());
print('ONE VECTOR-ONLY TASK CREATED: materialize_ceamz_candidates_v1');
print('Do not rerun raster reconstruction until this asset succeeds.');

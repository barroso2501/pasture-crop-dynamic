/**
 * 02b_audit_candidate_grid.js - version 1
 *
 * Vector-only audit of the materialized Cerrado-Amazon candidate grid.
 * No MapBiomas raster is loaded or evaluated.
 *
 * Output task:
 *   candidate_grid_audit_v1
 */

var K = require(
  'users/barroso2501/pasture-crop:lib/constants.js'
);

var CANDIDATE_GRID_ASSET =
  'projects/ee-barroso2501/assets/' +
  'grade_hex_CeAmz_candidates_ibge2025';

var DRIVE_FOLDER = 'pasture_crop_dynamic_audits';
var OUTPUT_PREFIX = 'candidate_grid_audit_v1';
var BATCH_COUNT = 8;

var candidateGrid = ee.FeatureCollection(CANDIDATE_GRID_ASSET);
var historicalGrid = ee.FeatureCollection(K.ANALYTICAL_GRID);

var candidateWithGeometryAudit = candidateGrid.map(function(feature) {
  feature = ee.Feature(feature);

  return feature
    .set('geometry_type_audit', feature.geometry().type())
    .set(
      'geometry_area_ha_audit',
      feature.geometry().area(1)
        .divide(K.SQUARE_METRES_PER_HECTARE)
    );
});

var idMatch = ee.Filter.equals({
  leftField: K.CELL_ID_FIELD,
  rightField: K.CELL_ID_FIELD
});

// Check the opposite direction: every historical cell should match a feature
// in the newly materialized candidate grid.
var historyJoinedToCandidates = ee.FeatureCollection(
  ee.Join.saveFirst({
    matchKey: '_candidate_match',
    outer: true
  }).apply(
    historicalGrid,
    candidateGrid,
    idMatch
  )
);

var historicalCandidateCheck = historyJoinedToCandidates.map(
  function(feature) {
    feature = ee.Feature(feature);

    var outside = ee.Number(ee.Algorithms.If(
      ee.Algorithms.IsEqual(
        feature.get('_candidate_match'),
        null
      ),
      1,
      0
    ));

    return ee.Feature(null, {
      historical_outside_candidate: outside
    });
  }
);

var candidateCount = candidateGrid.size();
var distinctIdCount = candidateGrid.aggregate_count_distinct(
  K.CELL_ID_FIELD
);

var historicalCount = historicalGrid.size();
var historicalMarkedInCandidate = ee.Number(
  candidateGrid.aggregate_sum('historical_member')
);

var historicalOutsideCount = ee.Number(
  historicalCandidateCheck.aggregate_sum(
    'historical_outside_candidate'
  )
);

var nonPolygonCount = candidateWithGeometryAudit
  .filter(ee.Filter.neq('geometry_type_audit', 'Polygon'))
  .size();

var validHistoricalFlagCount = candidateGrid.filter(
  ee.Filter.inList('historical_member', [0, 1])
).size();

var invalidHistoricalFlagCount = candidateCount.subtract(
  validHistoricalFlagCount
);

var invalidBatchCount = candidateGrid.filter(
  ee.Filter.or(
    ee.Filter.lt('batch_id', 0),
    ee.Filter.gte('batch_id', BATCH_COUNT)
  )
).size();

var batchCounts = [];

for (var batchId = 0; batchId < BATCH_COUNT; batchId++) {
  batchCounts.push(
    candidateGrid.filter(
      ee.Filter.eq('batch_id', batchId)
    ).size()
  );
}

var auditPass = candidateCount.eq(distinctIdCount)
  .and(nonPolygonCount.eq(0))
  .and(invalidHistoricalFlagCount.eq(0))
  .and(invalidBatchCount.eq(0))
  .and(historicalMarkedInCandidate
    .add(historicalOutsideCount)
    .eq(historicalCount));

var summary = ee.Feature(null, {
  audit_pass: ee.Number(ee.Algorithms.If(auditPass, 1, 0)),
  candidate_asset: CANDIDATE_GRID_ASSET,
  candidate_count: candidateCount,
  distinct_cell_id_count: distinctIdCount,
  cell_id_unique: ee.Number(ee.Algorithms.If(
    candidateCount.eq(distinctIdCount),
    1,
    0
  )),
  historical_grid_asset: K.ANALYTICAL_GRID,
  historical_grid_count: historicalCount,
  historical_marked_in_candidates: historicalMarkedInCandidate,
  historical_outside_candidate_count: historicalOutsideCount,
  candidate_not_in_historical_count: candidateCount
    .subtract(historicalMarkedInCandidate),
  non_polygon_count: nonPolygonCount,
  invalid_historical_flag_count: invalidHistoricalFlagCount,
  invalid_batch_count: invalidBatchCount,
  geometry_area_min_ha: candidateWithGeometryAudit.aggregate_min(
    'geometry_area_ha_audit'
  ),
  geometry_area_mean_ha: candidateWithGeometryAudit.aggregate_mean(
    'geometry_area_ha_audit'
  ),
  geometry_area_max_ha: candidateWithGeometryAudit.aggregate_max(
    'geometry_area_ha_audit'
  ),
  batch_count: BATCH_COUNT,
  batch_00_cells: batchCounts[0],
  batch_01_cells: batchCounts[1],
  batch_02_cells: batchCounts[2],
  batch_03_cells: batchCounts[3],
  batch_04_cells: batchCounts[4],
  batch_05_cells: batchCounts[5],
  batch_06_cells: batchCounts[6],
  batch_07_cells: batchCounts[7],
  first_feature_properties: ee.Feature(candidateGrid.first())
    .propertyNames()
    .sort()
    .join(','),
  audit_script_version: 1
});

var summaryCollection = ee.FeatureCollection([summary]);

Export.table.toDrive({
  collection: summaryCollection,
  description: OUTPUT_PREFIX,
  folder: DRIVE_FOLDER,
  fileNamePrefix: OUTPUT_PREFIX,
  fileFormat: 'CSV'
});

print('CANDIDATE-GRID AUDIT VERSION 1');
print('Candidate asset:', CANDIDATE_GRID_ASSET);
print('Audit summary:', summary);
print('ONE VECTOR-ONLY TASK CREATED:', OUTPUT_PREFIX);
print('Return the CSV before any raster batch is attempted.');

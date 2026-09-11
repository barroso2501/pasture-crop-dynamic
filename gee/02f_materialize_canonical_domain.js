/**
 * 02f_materialize_canonical_domain.js - version 1
 *
 * Materializes the canonical Cerrado-Amazon analytical domain without
 * repeating the endpoint raster reductions.
 *
 * Required preparation in Earth Engine:
 *   1. Upload canonical_domain_membership_c11_v3.csv as a table asset:
 *      projects/ee-barroso2501/assets/canonical_domain_membership_c11_v3
 *   2. Confirm that cell_id and canonical_member were imported as numbers.
 *   3. Run this script and start the single export task.
 *
 * The CSV contains all 32,305 candidate cells. The script retains only the
 * 24,889 records with canonical_member = 1, joins them to the already
 * materialized candidate grid, and exports the complete parent-grid
 * geometries as the canonical analytical-grid asset.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Versioned inputs and output
// ---------------------------------------------------------------------------

var CANDIDATE_GRID_ASSET =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_candidates_ibge2025';

var MEMBERSHIP_TABLE_ASSET =
  'projects/ee-barroso2501/assets/canonical_domain_membership_c11_v3';

var OUTPUT_GRID_ASSET =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3';

var EXPECTED_CANDIDATE_COUNT = 32305;
var EXPECTED_CANONICAL_COUNT = 24889;
var CELL_ID_FIELD = K.CELL_ID_FIELD;

// ---------------------------------------------------------------------------
// Load the materialized candidate grid and uploaded membership table
// ---------------------------------------------------------------------------

var candidates = ee.FeatureCollection(CANDIDATE_GRID_ASSET);
var membership = ee.FeatureCollection(MEMBERSHIP_TABLE_ASSET);

var retainedMembership = membership
  .filter(ee.Filter.eq('canonical_member', 1));

// ---------------------------------------------------------------------------
// Join by the stable parent-grid cell identifier
// ---------------------------------------------------------------------------

var joined = ee.FeatureCollection(
  ee.Join.inner().apply({
    primary: candidates,
    secondary: retainedMembership,
    condition: ee.Filter.equals({
      leftField: CELL_ID_FIELD,
      rightField: CELL_ID_FIELD
    })
  })
);

var canonicalDomain = joined.map(function (pair) {
  pair = ee.Feature(pair);

  var cell = ee.Feature(pair.get('primary'));
  var record = ee.Feature(pair.get('secondary'));

  return cell.set({
    canonical_member: 1,
    historical_member: record.get('historical_member'),
    source_batch_id: record.get('batch_id'),
    anthropogenic_1985_ha: record.get('anthropogenic_1985_ha'),
    anthropogenic_2025_ha: record.get('anthropogenic_2025_ha'),
    max_endpoint_anthropogenic_ha:
      record.get('max_endpoint_anthropogenic_ha'),
    endpoint_tolerance_ha: record.get('endpoint_tolerance_ha'),
    domain_version: 'canonical-c11-coverage-v3-native-grid',
    membership_source: 'canonical_domain_membership_c11_v3'
  });
});

// ---------------------------------------------------------------------------
// Lightweight vector checks
// ---------------------------------------------------------------------------

print('CANONICAL DOMAIN MATERIALIZATION - VERSION 1');
print('Candidate grid asset:', CANDIDATE_GRID_ASSET);
print('Membership table asset:', MEMBERSHIP_TABLE_ASSET);
print('Output grid asset:', OUTPUT_GRID_ASSET);
print('Candidate count (expected 32,305):', candidates.size());
print('Membership row count (expected 32,305):', membership.size());
print('Retained membership rows (expected 24,889):',
  retainedMembership.size());
print('Joined canonical cells (expected 24,889):', canonicalDomain.size());
print('Distinct canonical cell_id count (expected 24,889):',
  canonicalDomain.aggregate_count_distinct(CELL_ID_FIELD));
print('First canonical feature:', canonicalDomain.first());

Map.addLayer(
  canonicalDomain.style({color: 'f6c945', fillColor: '00000000', width: 1}),
  {},
  'Canonical domain - 24,889 cells',
  false
);

// ---------------------------------------------------------------------------
// One task: materialize the canonical analytical grid
// ---------------------------------------------------------------------------

Export.table.toAsset({
  collection: canonicalDomain,
  description: 'materialize_canonical_domain_c11_v3',
  assetId: OUTPUT_GRID_ASSET
});

print('ONE TASK CREATED: materialize_canonical_domain_c11_v3');
print('Run the task only after all five printed counts match expectations.');

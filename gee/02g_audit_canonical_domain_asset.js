/**
 * 02g_audit_canonical_domain_asset.js - version 1
 *
 * Final vector-only audit of the materialized canonical analytical domain.
 *
 * This script does not repeat raster reductions and does not create an export
 * task. It compares the persisted domain asset with the validated membership
 * table and checks identifiers, properties, geometry type, and cell areas.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

var CANONICAL_GRID_ASSET =
  'projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3';

var MEMBERSHIP_TABLE_ASSET =
  'projects/ee-barroso2501/assets/canonical_domain_membership_c11_v3';

var EXPECTED_CANONICAL_COUNT = 24889;
var CELL_ID_FIELD = K.CELL_ID_FIELD;

var canonical = ee.FeatureCollection(CANONICAL_GRID_ASSET);
var membership = ee.FeatureCollection(MEMBERSHIP_TABLE_ASSET);
var retainedMembership = membership
  .filter(ee.Filter.eq('canonical_member', 1));

var canonicalCount = canonical.size();
var canonicalDistinctIds =
  canonical.aggregate_count_distinct(CELL_ID_FIELD);
var canonicalDistinctGridIds =
  canonical.aggregate_count_distinct('GRID_ID');
var retainedCount = retainedMembership.size();
var retainedDistinctIds =
  retainedMembership.aggregate_count_distinct(CELL_ID_FIELD);

var requiredProperties = [
  CELL_ID_FIELD,
  'GRID_ID',
  'canonical_member',
  'historical_member',
  'source_batch_id',
  'anthropogenic_1985_ha',
  'anthropogenic_2025_ha',
  'max_endpoint_anthropogenic_ha',
  'endpoint_tolerance_ha',
  'domain_version',
  'membership_source'
];

var completePropertyCount = canonical
  .filter(ee.Filter.notNull(requiredProperties))
  .size();

var nonCanonicalFlagCount = canonical
  .filter(ee.Filter.neq('canonical_member', 1))
  .size();

// Compare the output asset with the retained rows of the membership table.
var idMatch = ee.Filter.equals({
  leftField: CELL_ID_FIELD,
  rightField: CELL_ID_FIELD
});

var outputWithMembership = ee.FeatureCollection(
  ee.Join.saveFirst('membership_record').apply({
    primary: canonical,
    secondary: retainedMembership,
    condition: idMatch
  })
);

var outputMatchedCount = outputWithMembership
  .filter(ee.Filter.notNull(['membership_record']))
  .size();

var membershipWithOutput = ee.FeatureCollection(
  ee.Join.saveFirst('grid_record').apply({
    primary: retainedMembership,
    secondary: canonical,
    condition: idMatch
  })
);

var membershipMatchedCount = membershipWithOutput
  .filter(ee.Filter.notNull(['grid_record']))
  .size();

var outputWithoutMembershipCount =
  canonicalCount.subtract(outputMatchedCount);
var membershipWithoutOutputCount =
  retainedCount.subtract(membershipMatchedCount);

var geometryAudit = canonical.map(function (feature) {
  feature = ee.Feature(feature);
  return feature.set({
    audit_geometry_type: feature.geometry().type(),
    audit_geometry_area_ha: feature.geometry().area(1).divide(10000)
  });
});

print('CANONICAL DOMAIN ASSET AUDIT - VERSION 1');
print('Canonical grid asset:', CANONICAL_GRID_ASSET);
print('Membership table asset:', MEMBERSHIP_TABLE_ASSET);

print('AUDIT 1A - Canonical feature count (expected 24,889):',
  canonicalCount);
print('AUDIT 1B - Canonical count matches expectation (expected true):',
  canonicalCount.eq(EXPECTED_CANONICAL_COUNT));
print('AUDIT 1C - Distinct canonical cell_id count (expected 24,889):',
  canonicalDistinctIds);
print('AUDIT 1D - Duplicate canonical cell_id count (expected 0):',
  canonicalCount.subtract(canonicalDistinctIds));
print('AUDIT 1E - Distinct canonical GRID_ID count (expected 24,889):',
  canonicalDistinctGridIds);
print('AUDIT 1F - Duplicate canonical GRID_ID count (expected 0):',
  canonicalCount.subtract(canonicalDistinctGridIds));

print('AUDIT 2A - First-feature property names:',
  ee.Feature(canonical.first()).propertyNames());
print('AUDIT 2B - Features with all required properties (expected 24,889):',
  completePropertyCount);
print('AUDIT 2C - Features with canonical_member other than 1 (expected 0):',
  nonCanonicalFlagCount);
print('AUDIT 2D - canonical_member histogram:',
  canonical.aggregate_histogram('canonical_member'));
print('AUDIT 2E - source_batch_id histogram:',
  canonical.aggregate_histogram('source_batch_id'));
print('AUDIT 2F - domain_version histogram:',
  canonical.aggregate_histogram('domain_version'));

print('AUDIT 3A - Retained membership rows (expected 24,889):',
  retainedCount);
print('AUDIT 3B - Distinct retained membership cell_id (expected 24,889):',
  retainedDistinctIds);
print('AUDIT 3C - Output cells without retained membership (expected 0):',
  outputWithoutMembershipCount);
print('AUDIT 3D - Retained membership rows without output cell (expected 0):',
  membershipWithoutOutputCount);

print('AUDIT 4A - Geometry-type histogram (expected Polygon only):',
  geometryAudit.aggregate_histogram('audit_geometry_type'));
print('AUDIT 4B - Geometry area statistics in hectares:',
  geometryAudit.aggregate_stats('audit_geometry_area_ha'));

print('AUDIT COMPLETE - NO EXPORT TASK IS CREATED.');
print('Return the Console output before updating constants.js.');

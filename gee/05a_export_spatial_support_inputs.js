/**
 * 05a_export_spatial_support_inputs.js - version 1
 *
 * Phase 1A export of the vector inputs required to build the canonical
 * spatial-support table and fixed contiguity graph.
 *
 * The script creates two Drive exports:
 *   1. the 24,889 canonical complete hexagons as GeoJSON;
 *   2. the Amazon and Cerrado IBGE 2025 biome geometries as GeoJSON.
 *
 * No raster reduction, spatial join, biome assignment, or asset mutation is
 * performed here. Biome overlaps and neighborhood relationships will be
 * calculated and validated in Colab from these versioned vector inputs.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

var SCRIPT_VERSION = 'canonical-spatial-input-export-v1';
var EXPORT_DATE = '2026-09-13';
var DRIVE_FOLDER = 'pasture_crop_dynamic_canonical';

var BIOME_ASSET = 'projects/ee-barroso2501/assets/biomas_IBGE';
var BIOME_CODE_FIELD = 'CD_BIOMA';
var AMAZON_CODE = '1';
var CERRADO_CODE = '3';

var EXPECTED_GRID_COUNT = 24889;
var EXPECTED_BIOME_COUNT = 2;

var GRID_OUTPUT_NAME = 'canonical_spatial_grid_input_v1';
var BIOME_OUTPUT_NAME = 'canonical_biomes_input_ibge2025_v1';

// ---------------------------------------------------------------------------
// Canonical grid export
// ---------------------------------------------------------------------------

var sourceGrid = ee.FeatureCollection(K.ANALYTICAL_GRID);

var gridExport = sourceGrid.map(function(feature) {
  feature = ee.Feature(feature);

  var geometry = feature.geometry();
  var centroidCoordinates = geometry.centroid({maxError: 1}).coordinates();

  return ee.Feature(geometry, {
    cell_id: feature.get(K.CELL_ID_FIELD),
    GRID_ID: feature.get('GRID_ID'),
    source_batch_id: feature.get('source_batch_id'),
    canonical_member: feature.get('canonical_member'),
    domain_version: feature.get('domain_version'),
    geometry_type_gee: geometry.type(),
    geometry_area_geodesic_ha: geometry.area({maxError: 1}).divide(10000),
    centroid_lon_gee: centroidCoordinates.get(0),
    centroid_lat_gee: centroidCoordinates.get(1),
    spatial_input_version: SCRIPT_VERSION,
    spatial_input_export_date: EXPORT_DATE
  });
});

// ---------------------------------------------------------------------------
// Target-biome export
// ---------------------------------------------------------------------------

var sourceBiomes = ee.FeatureCollection(BIOME_ASSET)
  .filter(ee.Filter.inList(BIOME_CODE_FIELD, [AMAZON_CODE, CERRADO_CODE]));

var biomeNames = ee.Dictionary({
  '1': 'Amazon',
  '3': 'Cerrado'
});

var biomeExport = sourceBiomes.map(function(feature) {
  feature = ee.Feature(feature);

  var geometry = feature.geometry();
  var code = ee.String(feature.get(BIOME_CODE_FIELD));

  return ee.Feature(geometry, {
    biome_code: code,
    biome_name: biomeNames.get(code),
    source_code_field: BIOME_CODE_FIELD,
    source_asset: BIOME_ASSET,
    source_geometry_type_gee: geometry.type(),
    source_area_geodesic_ha: geometry.area({maxError: 1}).divide(10000),
    spatial_input_version: SCRIPT_VERSION,
    spatial_input_export_date: EXPORT_DATE
  });
});

// ---------------------------------------------------------------------------
// Lightweight acceptance checks
// ---------------------------------------------------------------------------

var gridCount = gridExport.size();
var distinctCellIds = gridExport.aggregate_count_distinct('cell_id');
var distinctGridIds = gridExport.aggregate_count_distinct('GRID_ID');
var gridGeometryTypes = gridExport.aggregate_histogram('geometry_type_gee');

var biomeCount = biomeExport.size();
var distinctBiomeCodes = biomeExport.aggregate_count_distinct('biome_code');
var biomeCodeHistogram = biomeExport.aggregate_histogram('biome_code');

var gridCountPass = gridCount.eq(EXPECTED_GRID_COUNT);
var cellIdPass = distinctCellIds.eq(EXPECTED_GRID_COUNT);
var gridIdPass = distinctGridIds.eq(EXPECTED_GRID_COUNT);
var biomeCountPass = biomeCount.eq(EXPECTED_BIOME_COUNT);
var biomeCodePass = distinctBiomeCodes.eq(EXPECTED_BIOME_COUNT);

var completeSetupPass = ee.Number(
  ee.Algorithms.If(gridCountPass, 1, 0)
).multiply(
  ee.Number(ee.Algorithms.If(cellIdPass, 1, 0))
).multiply(
  ee.Number(ee.Algorithms.If(gridIdPass, 1, 0))
).multiply(
  ee.Number(ee.Algorithms.If(biomeCountPass, 1, 0))
).multiply(
  ee.Number(ee.Algorithms.If(biomeCodePass, 1, 0))
);

print('PHASE 1A - SPATIAL SUPPORT INPUT EXPORT - VERSION 1');
print('Script version:', SCRIPT_VERSION);
print('Canonical grid asset:', K.ANALYTICAL_GRID);
print('Biome asset:', BIOME_ASSET);
print('Biome code field:', BIOME_CODE_FIELD);
print('Target biome codes:', [AMAZON_CODE, CERRADO_CODE]);
print('Canonical grid count (expected 24,889):', gridCount);
print('Distinct cell_id count (expected 24,889):', distinctCellIds);
print('Distinct GRID_ID count (expected 24,889):', distinctGridIds);
print('Grid geometry-type histogram:', gridGeometryTypes);
print('Target-biome feature count (expected 2):', biomeCount);
print('Distinct target-biome codes (expected 2):', distinctBiomeCodes);
print('Target-biome code histogram:', biomeCodeHistogram);
print('Complete setup pass (expected 1):', completeSetupPass);
print('First grid export feature:', gridExport.first());
print('Biome export features:', biomeExport);

// ---------------------------------------------------------------------------
// Two vector export tasks
// ---------------------------------------------------------------------------

Export.table.toDrive({
  collection: gridExport,
  description: GRID_OUTPUT_NAME,
  fileNamePrefix: GRID_OUTPUT_NAME,
  folder: DRIVE_FOLDER,
  fileFormat: 'GeoJSON'
});

Export.table.toDrive({
  collection: biomeExport,
  description: BIOME_OUTPUT_NAME,
  fileNamePrefix: BIOME_OUTPUT_NAME,
  folder: DRIVE_FOLDER,
  fileFormat: 'GeoJSON'
});

print('TWO TASKS CREATED:');
print('1.', GRID_OUTPUT_NAME);
print('2.', BIOME_OUTPUT_NAME);
print('Run them only if complete setup pass equals 1.');
print('Return both files, Console output, and task metadata.');

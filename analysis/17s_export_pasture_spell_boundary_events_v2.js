/**
 * Decision 024 criterion 10: observed pasture spell boundaries in 2024/2025.
 *
 * Paste into the Earth Engine Code Editor. The constants module must be the
 * project's synchronized users/barroso2501/pasture-crop:lib/constants.
 * Revision 2 fixes the outer-domain edge pixels omitted by the raster mask
 * in v1. MODE='edge' tests cell GRID_ID GU-181 (known v1 mismatch); next
 * MODE='asset' writes a NEW four-band asset with one-pixel mask padding;
 * MODE='full' creates eight cell-summary tasks FROM THE SAVED v2 ASSET.
 * Each run creates tasks; it does not start them automatically.
 *
 * The trigger is annual coverage in the preceding and current year:
 * valid non-PAS -> PAS = entry; PAS -> valid non-PAS = termination.
 * A no-data/masked/unexpected observation is uncertain and never implies a
 * boundary. This is the same event definition as 17a and Decision 024.
 */

var K = require('users/barroso2501/pasture-crop:lib/constants');
var MODE = 'edge';  // 'edge', 'asset', or 'full'
var VERSION = 'pasture-spell-boundary-events-v2';
var FOLDER = 'pasture_spell_boundary_events_raw_v2';
var ASSET_ID = 'projects/ee-barroso2501/assets/' +
  'canonical_pasture_spell_boundary_events_2024_2025_v2';
var PAS = 15;
var NODATA = 27;
var MISSING = -9999;
if (['edge','asset','full'].indexOf(MODE) === -1) {
  throw new Error('MODE must be edge, asset, or full');
}

var expected = K.expectedSourceCodes();
function classifyNumber(v) {
  if (v === PAS) return 'pas';
  if (v === MISSING || v === NODATA || expected.indexOf(v) < 0)
    return 'uncertain';
  return 'non';
}
function pairNumber(previous, current) {
  var a = classifyNumber(previous), b = classifyNumber(current);
  if (a === 'uncertain' || b === 'uncertain') return 'uncertain_pair';
  if (a === 'pas' && b === 'pas') return 'pas_pas';
  if (a === 'pas') return 'termination_boundary_adjacent';
  if (b === 'pas') return 'entry_boundary_adjacent';
  return 'non_non';
}
var cases = [
  [39,15,'entry_boundary_adjacent'], [15,39,'termination_boundary_adjacent'],
  [15,15,'pas_pas'], [39,39,'non_non'], [15,27,'uncertain_pair'],
  [27,15,'uncertain_pair'], [15,999,'uncertain_pair'],
  [MISSING,15,'uncertain_pair'], [15,MISSING,'uncertain_pair']
];
cases.forEach(function(c, i) {
  if (pairNumber(c[0],c[1]) !== c[2])
    throw new Error('Synthetic case ' + (i+1) + ' failed');
});
var synthetic = [{year:2024,prev:39,now:15},
  {year:2025,prev:15,now:39}];
if (synthetic[0].year !== 2024 ||
    pairNumber(synthetic[0].prev, synthetic[0].now) !==
      'entry_boundary_adjacent' ||
    synthetic[1].year !== 2025 ||
    pairNumber(synthetic[1].prev, synthetic[1].now) !==
      'termination_boundary_adjacent') {
  throw new Error('Year-specific boundary test failed');
}

var coverage = ee.Image(K.COVERAGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var names = [], bands = [], assetBands = [];
function add(mask, name) {
  var p = mask.unmask(0).toDouble();
  bands.push(p.rename(name+'_pixels'));
  bands.push(p.multiply(pixelHa).rename(name+'_ha'));
  names.push(name+'_pixels');
  names.push(name+'_ha');
}
function validNon(img) {
  var result = ee.Image.constant(0).eq(1);
  expected.forEach(function(c) {
    if (c !== PAS && c !== NODATA) result = result.or(img.eq(c));
  });
  return result;
}
var all = ee.Image.constant(1).eq(1);
add(all,'domain');
// Paint on the native lattice. A polygon may cover part of a pixel whose
// centre lies outside the union. Weighted reduceRegions includes that part,
// so expand the storage mask by one native pixel in each direction. This
// changes the STORAGE mask only, never the classification/event rule.
var painted = ee.Image.constant(0).byte()
  .setDefaultProjection(K.CRS,K.CRS_TRANSFORM).paint(grid,1);
var paddedDomain = painted.focalMax(1,'square','pixels').eq(1);
[2024,2025].forEach(function(year) {
  var prev = coverage.select(K.coverageBandName(year-1))
    .unmask(MISSING).toInt16();
  var curr = coverage.select(K.coverageBandName(year))
    .unmask(MISSING).toInt16();
  var pp=prev.eq(PAS), pn=validNon(prev), cp=curr.eq(PAS), cn=validNon(curr);
  assetBands.push(pn.and(cp).byte().rename('entry_boundary_adjacent_'+year));
  assetBands.push(pp.and(cn).byte().rename('termination_boundary_adjacent_'+year));
});
var raster=ee.Image.cat(assetBands).toByte().updateMask(paddedDomain);
var savedAsset=MODE==='full' ? ee.Image(ASSET_ID) : raster;
[2024,2025].forEach(function(year) {
  var prev = coverage.select(K.coverageBandName(year-1))
    .unmask(MISSING).toInt16();
  var curr = coverage.select(K.coverageBandName(year))
    .unmask(MISSING).toInt16();
  var pp=prev.eq(PAS), pn=validNon(prev), cp=curr.eq(PAS), cn=validNon(curr);
  var expectedEntry=pn.and(cp);
  var expectedTermination=pp.and(cn);
  var entryName='entry_boundary_adjacent_'+year;
  var termName='termination_boundary_adjacent_'+year;
  var entry = savedAsset.select(entryName).unmask(0).eq(1);
  var termination = savedAsset.select(termName).unmask(0).eq(1);
  var samePasture=pp.and(cp);
  var sameNon=pn.and(cn);
  var uncertain=expectedEntry.or(expectedTermination)
    .or(samePasture).or(sameNon).not();
  add(entry,entryName);
  add(termination,termName);
  add(samePasture,'pas_pas_'+year);
  add(sameNon,'non_non_'+year);
  add(uncertain,'uncertain_pair_'+year);
  add(entry.neq(expectedEntry),'entry_asset_mismatch_'+year);
  add(termination.neq(expectedTermination),'termination_asset_mismatch_'+year);
});
if (bands.length !== 30 || assetBands.length !== 4)
  throw new Error('Expected 30 table bands and 4 raster bands');
var image = ee.Image.cat(bands);
var selectors = ['cell_id','GRID_ID','source_batch_id',
  'diagnostic_interval','output_version'].concat(names);

function createTask(collection, name, batch) {
  var reduced = image.reduceRegions({
    collection:collection,
    reducer:ee.Reducer.sum(),
    crs:K.CRS,
    crsTransform:K.CRS_TRANSFORM,
    tileScale:16,
    maxPixelsPerRegion:100000000
  });
  var table = reduced.map(function(f) {
    return ee.Feature(null, f.toDictionary(names)).set({
      cell_id:f.get('cell_id'), GRID_ID:f.get('GRID_ID'),
      source_batch_id:f.get('source_batch_id'),
      diagnostic_interval:1, output_version:VERSION
    });
  });
  Export.table.toDrive({collection:table, description:name,
    folder:FOLDER, fileNamePrefix:name, fileFormat:'CSV',
    selectors:selectors});
  print('TASK CREATED:',name, 'batch:',batch);
}

print('CANONICAL PASTURE-SPELL BOUNDARY EVENTS — CRITERION 10 REVISION 2');
print('Mode:',MODE,'Synthetic checks: PASS');
print('Coverage asset:',K.COVERAGE_ASSET);
print('Grid asset:',K.ANALYTICAL_GRID);
print('Projection:',K.CRS,'transform:',K.CRS_TRANSFORM);
print('Expected numeric bands:',bands.length);
print('2024 uses 2023→2024; 2025 uses 2024→2025.');
print('A pair with either observation uncertain is not an event.');
if (MODE === 'edge') {
  var edgeCell=grid.filter(ee.Filter.eq('GRID_ID','GU-181'));
  createTask(edgeCell,'canonical_pasture_spell_boundary_events_edge_v2','edge');
  print('Start ONE edge-cell task; validate before exporting the asset.');
} else if (MODE === 'asset') {
  // The conservative rectangle sets bounds; the padded mask holds edge pixels.
  // v1 remains intact as an audited and rejected asset.
  Export.image.toAsset({image:raster,
    description:'canonical_pasture_spell_boundary_events_2024_2025_v2',
    assetId:ASSET_ID,
    region:ee.Geometry.Rectangle([-75,-26,-40,7],null,false),
    crs:K.CRS, crsTransform:K.CRS_TRANSFORM,
    pyramidingPolicy:{'.default':'sample'}, maxPixels:1e11});
  print('ONE PIXEL-LEVEL ASSET TASK CREATED:',ASSET_ID);
  print('Finish that task before creating full cell-summary tasks.');
} else {
  print('Full tables read four event bands from saved asset:',ASSET_ID);
  for (var b=0; b<8; b++) {
    var batchGrid = grid.filter(ee.Filter.eq('source_batch_id',b));
    var name='canonical_pasture_spell_boundary_events_b'+
      ('0'+b).slice(-2)+'_v2';
    createTask(batchGrid,name,b);
  }
  print('Start the EIGHT batch tasks gradually; validate all with 17t.');
}

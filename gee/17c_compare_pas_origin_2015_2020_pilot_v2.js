/** RQ2 origin impact pilot, 2015–2020. One full-domain Drive CSV task.
 * Requires the synchronized project constants module. Uses annual coverage
 * as authority for pasture-spell origin and age asset only for comparison.
 * This is a pilot, not an accepted replacement for canonical v1 outputs.
 */
var K = require('users/barroso2501/pasture-crop:lib/constants');
var START = 1985, T0 = 2015, T1 = 2020, MISSING = -9999;
var FOLDER = 'pasture_spell_remediation_pilot_v1';
var NAME = 'canonical_pas_origin_2015_2020_pilot_v2';
var coverage = ee.Image(K.COVERAGE_ASSET);
var ageAsset = ee.Image(K.PASTURE_AGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var codes = K.expectedSourceCodes();
var names = ['nat','pas','tmp','oag','out','water','nodata','unexpected','masked'];
var destinations = ['tmp','nat','oag','out','water','nodata','unexpected','masked'];
var oldNames = ['censored','new','unresolved','unattributed'];
var reconstructed = ['initial','new','unresolved'];
var pixelHa = ee.Image.pixelArea().divide(10000);

function inCodes(image, list) {
  var found = image.eq(list[0]);
  for (var i = 1; i < list.length; ++i) found = found.or(image.eq(list[i]));
  return found;
}
function states(image) {
  var s = {nat:inCodes(image,K.CLASS_CODES.NAT),pas:image.eq(15),
    tmp:inCodes(image,K.CLASS_CODES.TMP),
    oag:inCodes(image,K.CLASS_CODES.OAG),
    out:inCodes(image,K.CLASS_CODES.OUT),
    water:inCodes(image,K.CLASS_CODES.WATER),
    nodata:image.eq(27),masked:image.eq(MISSING)};
  var known = s.nat.or(s.pas).or(s.tmp).or(s.oag).or(s.out)
    .or(s.water).or(s.nodata);
  s.unexpected = s.masked.not().and(known.not());
  return s;
}
function add(mask, name) {
  bands.push(mask.multiply(pixelHa).rename(name).unmask(0));
  selectors.push(name);
}

// Chronological state: 0 observed non-PAS, 1 continuous from 1985,
// 2 entry following observed non-PAS, 3 unresolved PAS, 4 uncertain.
var previous = ee.Image.constant(4).byte();
var origin = null;
for (var year = START; year <= T0; ++year) {
  var c = coverage.select(K.coverageBandName(year)).unmask(MISSING).toInt16();
  var pas = c.eq(15);
  var non = ee.Image.constant(0).eq(1);
  codes.forEach(function (v) {
    if (v !== 15 && v !== 27) non = non.or(c.eq(v));
  });
  var initial = year === START ? pas : pas.and(previous.eq(1));
  var entered = year === START ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(0));
  var continued = year === START ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(2));
  origin = ee.Image.constant(4).byte().where(non,0).where(initial,1)
    .where(entered.or(continued),2)
    .where(pas.and(initial.not()).and(entered.not())
      .and(continued.not()),3);
  previous = origin;
}
var c0 = coverage.select(K.coverageBandName(T0)).unmask(MISSING).toInt16();
var c1 = coverage.select(K.coverageBandName(T1)).unmask(MISSING).toInt16();
var s0 = states(c0), s1 = states(c1);
var old = ageAsset.select([K.ageBandIndex(T0)]).unmask(MISSING).toInt16();
var oldC = old.eq(K.PASTURE_AGE_INITIAL_STOCK_CODE);
var oldN = old.gt(K.PASTURE_AGE_OFFSET)
  .and(old.lte(K.PASTURE_AGE_OFFSET + T0 - START));
var oldU = inCodes(old,K.PASTURE_AGE_UNRESOLVED_CODES);
var oldMasks = [oldC,oldN,oldU,oldC.or(oldN).or(oldU).not()];
var newMasks = [origin.eq(1),origin.eq(2),origin.eq(3)];

var bands = [], selectors = ['cell_id','GRID_ID','t0','t1',
  'diagnostic_interval','output_version'];
names.forEach(function (name) {
  add(s0[name],'stock0_'+name);
  add(s1[name],'stock1_'+name);
});
// Endpoint origin and destination totals are coverage-only control bands.
names.forEach(function (name) {
  add(s0.pas.and(s1[name]),'flow_pas_'+name);
});
add(s0.nat.and(s1.pas),'flow_nat_pas');
destinations.forEach(function (d) {
  var flow = s0.pas.and(s1[d]);
  oldNames.forEach(function (o,i) {
    add(flow.and(oldMasks[i]),'old_'+d+'_'+o);
  });
  reconstructed.forEach(function (o,i) {
    add(flow.and(newMasks[i]),'new_'+d+'_'+o);
  });
  // The 4x3 cross-tab gives the exact old-to-new transfer (not just marginals).
  oldNames.forEach(function (o,i) {
    reconstructed.forEach(function (n,j) {
      add(flow.and(oldMasks[i]).and(newMasks[j]),
        'move_'+d+'_'+o+'_to_'+n);
    });
  });
});
add(ee.Image.constant(1).eq(1),'raster_area_ha');

var reduced = ee.Image.cat(bands).reduceRegions({
  collection:grid, reducer:ee.Reducer.sum(), crs:K.CRS,
  // This ~180-band comparison image exceeds 30 million band-pixels even in
  // an ordinary full-size hexagon (observed 61,178,000). This upper bound
  // limits an individual cell; tileScale controls processing tile memory.
  crsTransform:K.CRS_TRANSFORM, tileScale:16, maxPixelsPerRegion:250000000
});
var exported = reduced.map(function (f) {
  return ee.Feature(null, f.toDictionary(selectors.slice(6))).set({
    cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),t0:T0,t1:T1,
    diagnostic_interval:0,
    output_version:'pas-origin-reconstruction-pilot-v2'
  });
});

print('RQ2 PASTURE-ORIGIN IMPACT PILOT — 2015–2020 REVISION 2');
print('REGION BAND-PIXEL LIMIT: 250000000; TILE SCALE: 16');
print('Coverage:', K.COVERAGE_ASSET);
print('Age asset (comparison only):', K.PASTURE_AGE_ASSET);
print('Expected cells:',K.EXPECTED_ANALYTICAL_CELL_COUNT);
print('Bands / CSV fields:',bands.length,selectors.length);
print('This task measures old-to-reconstructed transfers for PAS outflows.');
print('Do not infer a national percentage from a sampled cell or point.');
Export.table.toDrive({collection:exported, description:NAME,folder:FOLDER,
  fileNamePrefix:NAME,fileFormat:'CSV',selectors:selectors});
print('ONE FULL-DOMAIN TASK CREATED:', NAME);

/** Decision 024, criterion 7: one-batch PAS origin x endpoint destination pilot.
 * Set INTERVAL_INDEX and BATCH_ID only. Run one task, validate locally, then
 * repeat on the remaining batches/intervals after the pilot is accepted.
 * Requires the synchronized canonical constants module used by 17g.
 */
var K = require('users/barroso2501/pasture-crop:lib/constants');
var INTERVAL_INDEX = 6; // 2015-2020 pilot; 7 is flagged diagnostic.
var BATCH_ID = 0;
var INTERVALS = [[1985,1990],[1990,1995],[1995,2000],[2000,2005],
  [2005,2010],[2010,2015],[2015,2020],[2020,2025]];
if (INTERVAL_INDEX < 0 || INTERVAL_INDEX > 7 ||
    INTERVAL_INDEX !== Math.floor(INTERVAL_INDEX) ||
    BATCH_ID < 0 || BATCH_ID > 7 || BATCH_ID !== Math.floor(BATCH_ID)) {
  throw new Error('Invalid interval index or batch ID');
}
var T0 = INTERVALS[INTERVAL_INDEX][0];
var T1 = INTERVALS[INTERVAL_INDEX][1];
var MISSING = -9999;
var coverage = ee.Image(K.COVERAGE_ASSET);
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID)
  .filter(ee.Filter.eq('source_batch_id', BATCH_ID));
var pixelHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var sourceCodes = K.expectedSourceCodes();
function inCodes(img, codes) {
  var hit = img.eq(codes[0]);
  for (var i=1; i<codes.length; i++) hit = hit.or(img.eq(codes[i]));
  return hit;
}
// States 0 observed non-PAS, 1 continuous 1985 spell, 2 observed entry,
// 3 unresolved PAS after missing/unexpected observation, 4 uncertain.
var previous = ee.Image.constant(4).byte();
for (var year=1985; year<=T0; year++) {
  var cov = coverage.select(K.coverageBandName(year)).unmask(MISSING).toInt16();
  var pas = cov.eq(15);
  var non = ee.Image.constant(0).eq(1);
  sourceCodes.forEach(function(code) {
    if (code !== 15 && code !== 27) non = non.or(cov.eq(code));
  });
  var initial = year===1985 ? pas : pas.and(previous.eq(1));
  var entered = year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(0));
  var continued = year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(2));
  previous = ee.Image.constant(4).byte().where(non,0).where(initial,1)
    .where(entered.or(continued),2)
    .where(pas.and(initial.not()).and(entered.not())
      .and(continued.not()),3);
}
var c0 = coverage.select(K.coverageBandName(T0)).unmask(MISSING).toInt16();
var c1 = coverage.select(K.coverageBandName(T1)).unmask(MISSING).toInt16();
var origins = {initial:previous.eq(1), new:previous.eq(2),
  unresolved:previous.eq(3)};
var destinations = {
  pas:inCodes(c1,K.CLASS_CODES.PAS),
  tmp:inCodes(c1,K.CLASS_CODES.TMP),
  nat:inCodes(c1,K.CLASS_CODES.NAT),
  oag:inCodes(c1,K.CLASS_CODES.OAG),
  out:inCodes(c1,K.CLASS_CODES.OUT),
  water:inCodes(c1,K.CLASS_CODES.WATER),
  nodata:inCodes(c1,K.CLASS_CODES.NODATA),
  masked:c1.eq(MISSING)
};
var known = ee.Image.constant(0).eq(1);
['pas','tmp','nat','oag','out','water','nodata'].forEach(function(d) {
  known = known.or(destinations[d]);
});
destinations.unexpected = destinations.masked.not().and(known.not());
var bands=[], selectors=['cell_id','GRID_ID','source_batch_id','t0','t1',
  'diagnostic_interval','output_version'];
function add(mask,name) {
  bands.push(mask.multiply(pixelHa).rename(name).unmask(0));
  selectors.push(name);
}
var pas0 = c0.eq(15);
add(pas0,'stock0_pas');
['initial','new','unresolved'].forEach(function(o) {
  add(pas0.and(origins[o]),'origin_'+o);
});
['pas','tmp','nat','oag','out','water','nodata','unexpected','masked']
  .forEach(function(d) {
    add(pas0.and(destinations[d]),'flow_pas_'+d);
    ['initial','new','unresolved'].forEach(function(o) {
      add(pas0.and(origins[o]).and(destinations[d]),
        'pas_'+o+'_to_'+d);
    });
  });
// 40 independent area bands: 1 stock, 3 origins, 9 flows, 27 partitions.
print('DECISION 024 PAS ORIGIN x DESTINATION PILOT');
print('Interval:',T0,T1,'Batch:',BATCH_ID,'Area bands:',bands.length);
if (bands.length !== 40) throw new Error('Unexpected area-band count');
var reduced = ee.Image.cat(bands).reduceRegions({
  collection:grid, reducer:ee.Reducer.sum(), crs:K.CRS,
  crsTransform:K.CRS_TRANSFORM, tileScale:16,
  maxPixelsPerRegion:100000000
});
var table = reduced.map(function(f) {
  return ee.Feature(null,f.toDictionary(selectors.slice(7))).set({
    cell_id:f.get('cell_id'), GRID_ID:f.get('GRID_ID'),
    source_batch_id:f.get('source_batch_id'), t0:T0, t1:T1,
    diagnostic_interval:T0===2020 ? 1 : 0,
    output_version:'pas-origin-destination-closure-pilot-v1'
  });
});
var taskName='canonical_pas_origin_destination_'+T0+'_'+T1+'_b'+
  ('0'+BATCH_ID).slice(-2)+'_pilot_v1';
Export.table.toDrive({collection:table,description:taskName,
  fileNamePrefix:taskName,folder:'pasture_spell_closure_pilot_v1',
  fileFormat:'CSV',selectors:selectors});
print('ONE TASK CREATED:',taskName);

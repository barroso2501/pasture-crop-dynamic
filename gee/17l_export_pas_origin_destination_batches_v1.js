/** Decision 024 criterion 7: origin x endpoint destination for one interval.
 * Set INTERVAL_INDEX; create seven tasks for accepted 2015-2020 pilot interval,
 * eight tasks otherwise. Start tasks gradually in the GEE Tasks panel.
 */
var K = require('users/barroso2501/pasture-crop:lib/constants');
var INTERVAL_INDEX = 6;
var INTERVALS = [[1985,1990],[1990,1995],[1995,2000],[2000,2005],
  [2005,2010],[2010,2015],[2015,2020],[2020,2025]];
if (INTERVAL_INDEX < 0 || INTERVAL_INDEX > 7 ||
    INTERVAL_INDEX !== Math.floor(INTERVAL_INDEX)) {
  throw new Error('Choose one interval index from 0 to 7');
}
var T0=INTERVALS[INTERVAL_INDEX][0], T1=INTERVALS[INTERVAL_INDEX][1];
var batches=INTERVAL_INDEX===6 ? [1,2,3,4,5,6,7] : [0,1,2,3,4,5,6,7];
var coverage=ee.Image(K.COVERAGE_ASSET);
var grid=ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa=ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var codes=K.expectedSourceCodes();
function inCodes(img,values) {
  var hit=img.eq(values[0]);
  for(var i=1;i<values.length;i++) hit=hit.or(img.eq(values[i]));
  return hit;
}
var previous=ee.Image.constant(4).byte();
for(var year=1985;year<=T0;year++) {
  var cov=coverage.select(K.coverageBandName(year)).unmask(-9999).toInt16();
  var pas=cov.eq(15), non=ee.Image.constant(0).eq(1);
  codes.forEach(function(code) {
    if(code!==15 && code!==27) non=non.or(cov.eq(code));
  });
  var initial=year===1985 ? pas : pas.and(previous.eq(1));
  var entered=year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(0));
  var continued=year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(2));
  previous=ee.Image.constant(4).byte().where(non,0).where(initial,1)
    .where(entered.or(continued),2)
    .where(pas.and(initial.not()).and(entered.not())
      .and(continued.not()),3);
}
var c0=coverage.select(K.coverageBandName(T0)).unmask(-9999).toInt16();
var c1=coverage.select(K.coverageBandName(T1)).unmask(-9999).toInt16();
var origins={initial:previous.eq(1),new:previous.eq(2),
  unresolved:previous.eq(3)};
var destinations={
  pas:inCodes(c1,K.CLASS_CODES.PAS),tmp:inCodes(c1,K.CLASS_CODES.TMP),
  nat:inCodes(c1,K.CLASS_CODES.NAT),oag:inCodes(c1,K.CLASS_CODES.OAG),
  out:inCodes(c1,K.CLASS_CODES.OUT),water:inCodes(c1,K.CLASS_CODES.WATER),
  nodata:inCodes(c1,K.CLASS_CODES.NODATA),masked:c1.eq(-9999)
};
var known=ee.Image.constant(0).eq(1);
['pas','tmp','nat','oag','out','water','nodata'].forEach(function(d) {
  known=known.or(destinations[d]);
});
destinations.unexpected=destinations.masked.not().and(known.not());
var originNames=['initial','new','unresolved'];
var destNames=['pas','tmp','nat','oag','out','water','nodata',
  'unexpected','masked'];
var bands=[], selectors=['cell_id','GRID_ID','source_batch_id','t0','t1',
  'diagnostic_interval','output_version'];
function add(mask,name) {
  bands.push(mask.multiply(pixelHa).rename(name).unmask(0));
  selectors.push(name);
}
var pas0=c0.eq(15);
add(pas0,'stock0_pas');
originNames.forEach(function(o) {add(pas0.and(origins[o]),'origin_'+o);});
destNames.forEach(function(d) {
  add(pas0.and(destinations[d]),'flow_pas_'+d);
  originNames.forEach(function(o) {
    add(pas0.and(origins[o]).and(destinations[d]),'pas_'+o+'_to_'+d);
  });
});
if(bands.length!==40) throw new Error('Expected 40 area bands');
var metricImage=ee.Image.cat(bands);
print('PAS ORIGIN × DESTINATION — PRODUCTION EXPORT V1');
print('Interval:',T0,T1,'diagnostic:',T0===2020 ? 1 : 0);
print('Area bands:',bands.length,'batches:',batches);
print('No regional preview is evaluated in the Console.');
batches.forEach(function(batch) {
  var name='canonical_pas_origin_destination_'+T0+'_'+T1+'_b'+
    ('0'+batch).slice(-2)+'_v1';
  var reduced=metricImage.reduceRegions({
    collection:grid.filter(ee.Filter.eq('source_batch_id',batch)),
    reducer:ee.Reducer.sum(),crs:K.CRS,
    crsTransform:K.CRS_TRANSFORM,tileScale:16,
    maxPixelsPerRegion:100000000
  });
  var table=reduced.map(function(f) {
    return ee.Feature(null,f.toDictionary(selectors.slice(7))).set({
      cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),
      source_batch_id:f.get('source_batch_id'),t0:T0,t1:T1,
      diagnostic_interval:T0===2020 ? 1 : 0,
      output_version:'pas-origin-destination-closure-v1'
    });
  });
  Export.table.toDrive({collection:table,description:name,
    fileNamePrefix:name,folder:'pasture_spell_closure_full_v1',
    fileFormat:'CSV',selectors:selectors});
  print('TASK CREATED:',name);
});
print('Start tasks gradually and check completion.');

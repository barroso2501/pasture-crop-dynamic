/** Lightweight PAS→temporary-crop origin comparison, 2015–2020.
 * Seven independent tasks for canonical batches 01–07. Batch 00 is accepted
 * separately and must not be rerun here.
 * Use only the accepted canonical grid and aligned Collection 11 assets.
 * Old source age is retained solely for old-to-new cross-tabulation.
 */
var K = require('users/barroso2501/pasture-crop:lib/constants');
var BATCHES = [1,2,3,4,5,6,7];
var T0 = 2015, T1 = 2020, MISSING = -9999;
var canonicalGrid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var coverage = ee.Image(K.COVERAGE_ASSET);
var ageSource = ee.Image(K.PASTURE_AGE_ASSET);
var sourceCodes = K.expectedSourceCodes();
var pixelHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);

function inCodes(img,codes) {
  var hit=img.eq(codes[0]);
  for(var i=1;i<codes.length;i++) hit=hit.or(img.eq(codes[i]));
  return hit;
}

// States 0 observed non-PAS, 1 continuous since 1985, 2 observed later
// entry, 3 unresolved PAS, 4 uncertain observation.
var previous=ee.Image.constant(4).byte();
for(var year=1985;year<=T0;year++) {
  var cov=coverage.select(K.coverageBandName(year))
    .unmask(MISSING).toInt16();
  var pas=cov.eq(15);
  var non=ee.Image.constant(0).eq(1);
  sourceCodes.forEach(function(code) {
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

var c0=coverage.select(K.coverageBandName(T0)).unmask(MISSING);
var c1=coverage.select(K.coverageBandName(T1)).unmask(MISSING);
var pas0=c0.eq(15);
var pasTmp=pas0.and(inCodes(c1,K.CLASS_CODES.TMP));
var natPas=inCodes(c0,K.CLASS_CODES.NAT).and(c1.eq(15));
var oldAge=ageSource.select([K.ageBandIndex(T0)]).unmask(MISSING);
var oldC=oldAge.eq(100);
var oldN=oldAge.gt(K.PASTURE_AGE_OFFSET)
  .and(oldAge.lte(K.PASTURE_AGE_OFFSET+T0-K.FIRST_YEAR));
var oldU=inCodes(oldAge,K.PASTURE_AGE_UNRESOLVED_CODES);
var old=[oldC,oldN,oldU,oldC.or(oldN).or(oldU).not()];
var oldNames=['censored','new','unresolved','unattributed'];
var current=[previous.eq(1),previous.eq(2),previous.eq(3)];
var currentNames=['initial','new','unresolved'];
var bands=[], selectors=['cell_id','GRID_ID','source_batch_id',
  't0','t1','output_version'];
function add(mask,name) {
  bands.push(mask.multiply(pixelHa).rename(name).unmask(0));
  selectors.push(name);
}
add(pasTmp,'flow_pas_tmp');
add(natPas,'flow_nat_pas');
add(pas0,'stock0_pas');
for(var i=0;i<old.length;i++) add(pasTmp.and(old[i]),'old_'+oldNames[i]);
for(var j=0;j<current.length;j++)
  add(pasTmp.and(current[j]),'new_'+currentNames[j]);
for(var a=0;a<old.length;a++)
  for(var b=0;b<current.length;b++)
    add(pasTmp.and(old[a]).and(current[b]),
      'move_'+oldNames[a]+'_to_'+currentNames[b]);

// Exactly 22 area bands (three controls, four old, three reconstructed,
// twelve cross-tab cells). No full origin×destination cube is computed.
var metricImage=ee.Image.cat(bands);
print('RQ2 ORIGIN COMPARISON — SEVEN REMAINING BATCHES');
print('Image bands (must be 22):',bands.length);
print('Batches:',BATCHES);
print('No regional preview is evaluated in the Console.');
BATCHES.forEach(function(batch) {
  var name='canonical_pas_tmp_origin_2015_2020_b'+
    ('0'+batch).slice(-2)+'_v3';
  var reduced=metricImage.reduceRegions({
    collection:canonicalGrid.filter(ee.Filter.eq('source_batch_id',batch)),
    reducer:ee.Reducer.sum(),crs:K.CRS,
    crsTransform:K.CRS_TRANSFORM,tileScale:16,
    maxPixelsPerRegion:100000000
  });
  var table=reduced.map(function(f) {
    return ee.Feature(null,f.toDictionary(selectors.slice(6))).set({
      cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),
      source_batch_id:f.get('source_batch_id'),t0:T0,t1:T1,
      output_version:'pas-tmp-origin-light-batch-v3'
    });
  });
  Export.table.toDrive({collection:table,description:name,
    fileNamePrefix:name,folder:'pasture_spell_remediation_pilot_v1',
    fileFormat:'CSV',selectors:selectors});
  print('TASK CREATED:',name);
});
print('SEVEN TASKS CREATED. Start one at a time and check completion.');

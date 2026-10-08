/** Decision 024 criterion 11: native-grid, 41-year source-age audit.
 *
 * Paste in the GEE Code Editor with the synchronized constants module.
 * MODE='pilot' makes two tiny CSV tasks near known anomalies. After Colab
 * validation, MODE='batch' makes TWO tasks for one source_batch_id at a time.
 * There are eight batches (0..7); finish batch 0 before creating more.
 * No getInfo or nationwide reduceRegion preview is used.
 *
 * Source code 1 is tested directly on the public age asset. Reused 100 is
 * raw age==100 AND the independently reconstructed NEW episode state.
 * Unresolved-origin PAS with raw 100 is reported separately, never silently
 * called a known re-entry. Both anomalies can overlap at the PIXEL level
 * across different years; same-year overlap is impossible by definition.
 */
var K=require('users/barroso2501/pasture-crop:lib/constants');
var MODE='pilot';  // 'pilot' or 'batch'
var BATCH=0;       // 0..7 when MODE='batch'
var VERSION='pasture-age-source-audit-v1';
var FOLDER='pasture_age_source_audit_raw_v1';
var MISSING=-9999, PAS=15, NODATA=27;
if(['pilot','batch'].indexOf(MODE)<0 || BATCH<0 || BATCH>7 ||
   Math.floor(BATCH)!==BATCH) throw new Error('Invalid MODE or BATCH');
var C=K.expectedSourceCodes();
function classify(v) {
  if(v===PAS) return 1;
  if(v===MISSING || v===NODATA || C.indexOf(v)<0) return 4;
  return 0;
}
function step(prev,code,age) {
  var c=classify(code), state=c===4?4:c===0?0:
    age===1985 || prev===1?1:prev===0 || prev===2?2:3;
  return state;
}
var cases=[
  {codes:[15,15,39,15,15],ages:[100,100,-9999,100,100],states:[1,1,0,2,2]},
  {codes:[15,27,15],ages:[100,-9999,100],states:[1,4,3]},
  {codes:[39,15,39,15],ages:[-9999,1,-9999,100],states:[0,2,0,2]}
];
cases.forEach(function(c,j){var prev=4;
  c.codes.forEach(function(code,i){var s=step(prev,code,1985+i);
    if(s!==c.states[i]) throw new Error('State case '+j+'/'+i);
    prev=s;
  });
});
if(!(cases[0].ages[3]===100 && cases[0].states[3]===2 &&
     cases[1].states[2]===3 && cases[2].ages[1]===1 &&
     cases[2].ages[3]===100 && cases[2].states[3]===2))
  throw new Error('Anomaly synthetic check failed');

var grid=ee.FeatureCollection(K.ANALYTICAL_GRID);
var coverage=ee.Image(K.COVERAGE_ASSET), age=ee.Image(K.PASTURE_AGE_ASSET);
var pixelHa=ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE)
  .reproject({crs:K.CRS,crsTransform:K.CRS_TRANSFORM});
var zero=ee.Image.constant(0).byte().reproject({crs:K.CRS,
  crsTransform:K.CRS_TRANSFORM});
var falseImage=zero.eq(1);
function nonPas(img){var out=falseImage;
  C.forEach(function(c){if(c!==PAS && c!==NODATA)out=out.or(img.eq(c));});
  return out;
}
var annualBands=[], annualNames=[], cellBands=[], cellNames=[];
function addPair(bands,names,img,name){
  var v=ee.Image(img).unmask(0).toDouble();
  bands.push(v.rename(name+'_pixel_equiv'));
  bands.push(v.multiply(pixelHa).rename(name+'_ha'));
  names.push(name+'_pixel_equiv');names.push(name+'_ha');
}
var previous=ee.Image.constant(4).byte();
var everPas=falseImage, anyCode1=falseImage, anyReuse100=falseImage;
var rawCode1Years=zero.toInt16(),reuse100Years=zero.toInt16();
var code1PasYears=zero.toInt16(),code1NonYears=zero.toInt16();
var code1UncertainYears=zero.toInt16(),code100UnresolvedYears=zero.toInt16();
var code100NonYears=zero.toInt16();
var newEntries=zero.toInt16(), reentries=zero.toInt16();
var reentryActive=falseImage, reentryLength=zero.toInt16();
var maxReentryLength=zero.toInt16();
for(var year=1985;year<=2025;year++){
  var cov=coverage.select(K.coverageBandName(year))
    .unmask(MISSING).toInt16();
  var src=age.select([K.ageBandIndex(year)])
    .unmask(MISSING).toInt16();
  var pas=cov.eq(PAS), non=nonPas(cov);
  var initial=year===1985?pas:pas.and(previous.eq(1));
  var entry=year===1985?falseImage:pas.and(previous.eq(0));
  var continuation=year===1985?falseImage:pas.and(previous.eq(2));
  var unresolved=pas.and(initial.not()).and(entry.not())
    .and(continuation.not());
  var current=ee.Image.constant(4).byte().where(non,0)
    .where(initial,1).where(entry.or(continuation),2)
    .where(unresolved,3);
  var raw1=src.eq(1);
  var reuse=src.eq(100).and(current.eq(2));
  var code100Unresolved=src.eq(100).and(current.eq(3));
  addPair(annualBands,annualNames,raw1,'raw_code1_'+year);
  addPair(annualBands,annualNames,reuse,'reuse100_'+year);
  anyCode1=anyCode1.or(raw1);anyReuse100=anyReuse100.or(reuse);
  rawCode1Years=rawCode1Years.add(raw1.toInt16());
  reuse100Years=reuse100Years.add(reuse.toInt16());
  code1PasYears=code1PasYears.add(raw1.and(pas).toInt16());
  code1NonYears=code1NonYears.add(raw1.and(non).toInt16());
  code1UncertainYears=code1UncertainYears.add(
    raw1.and(pas.or(non).not()).toInt16());
  code100UnresolvedYears=code100UnresolvedYears.add(
    code100Unresolved.toInt16());
  code100NonYears=code100NonYears.add(src.eq(100).and(non).toInt16());
  var reentry=entry.and(everPas);
  newEntries=newEntries.add(entry.toInt16());
  reentries=reentries.add(reentry.toInt16());
  reentryActive=reentry.or(continuation.and(reentryActive));
  reentryLength=ee.Image.constant(0).int16()
    .where(reentry,1)
    .where(continuation.and(reentryActive),reentryLength.add(1));
  maxReentryLength=maxReentryLength.max(reentryLength);
  everPas=everPas.or(pas);previous=current;
}
if(annualBands.length!==164 || annualNames.length!==164)
  throw new Error('Expected 164 annual bands');
var cohort=everPas.or(anyCode1);
var joint={
  joint_none:cohort.and(anyCode1.not()).and(anyReuse100.not()),
  joint_code1_only:cohort.and(anyCode1).and(anyReuse100.not()),
  joint_reuse100_only:cohort.and(anyCode1.not()).and(anyReuse100),
  joint_both:cohort.and(anyCode1).and(anyReuse100)
};
var cellImages={
  domain:ee.Image.constant(1),ever_pas:everPas,audit_cohort:cohort,
  raw_code1_any:anyCode1,reuse100_any:anyReuse100,
  code1_outside_ever_pas:anyCode1.and(everPas.not()),
  raw_code1_years:rawCode1Years,reuse100_years:reuse100Years,
  code1_pas_years:code1PasYears,code1_nonpas_years:code1NonYears,
  code1_uncertain_years:code1UncertainYears,
  code100_unresolved_years:code100UnresolvedYears,
  code100_nonpas_years:code100NonYears,
  new_entry_events:newEntries,reentry_events:reentries,
  reentry_any:reentries.gt(0),reentry_two_plus:reentries.gte(2),
  max_reentry_duration_years:maxReentryLength,
  reentry_duration_ge2:maxReentryLength.gte(2),
  reentry_duration_ge5:maxReentryLength.gte(5)
};
Object.keys(cellImages).forEach(function(n){
  addPair(cellBands,cellNames,cellImages[n],n);
});
Object.keys(joint).forEach(function(n){
  addPair(cellBands,cellNames,joint[n],n);
});
if(cellBands.length!==48) throw new Error('Expected 48 cell bands');

var pilotPoints=[ee.Geometry.Point([-58.25,-16.66]),
  ee.Geometry.Point([-55.164051,-20.281475])];
var selected=MODE==='pilot' ?
  grid.filterBounds(pilotPoints[0]).merge(grid.filterBounds(pilotPoints[1]))
    .distinct(['cell_id']):
  grid.filter(ee.Filter.eq('source_batch_id',BATCH));
function createTask(kind,image,names){
  var reduced=image.reduceRegions({collection:selected,
    reducer:ee.Reducer.sum(),crs:K.CRS,crsTransform:K.CRS_TRANSFORM,
    tileScale:16,maxPixelsPerRegion:100000000});
  var table=reduced.map(function(f){return ee.Feature(null,f.toDictionary(names))
    .set({cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),
      source_batch_id:f.get('source_batch_id'),output_version:VERSION});});
  var suffix=MODE==='pilot'?'pilot':'b'+('0'+BATCH).slice(-2);
  var name='canonical_pasture_age_source_audit_'+kind+'_'+suffix+'_v1';
  Export.table.toDrive({collection:table,description:name,folder:FOLDER,
    fileNamePrefix:name,fileFormat:'CSV',
    selectors:['cell_id','GRID_ID','source_batch_id','output_version']
      .concat(names)});
  print('TASK CREATED:',name,'bands:',names.length);
}
print('PASTURE-AGE SOURCE-ANOMALY AUDIT — DECISION 024 CRITERION 11');
print('MODE:',MODE,'BATCH:',BATCH,'SYNTHETIC ENGINE: PASS');
print('Source:',K.PASTURE_AGE_ASSET);
print('Coverage:',K.COVERAGE_ASSET);
print('Overlap means BOTH anomalies in the same pixel in any year,');
print('within the ever-PAS OR raw-code1 cohort; not the same year.');
createTask('cell',ee.Image.cat(cellBands),cellNames);
createTask('annual',ee.Image.cat(annualBands),annualNames);
print('Start both pilot tasks first; validate in Colab before batch 0.');

/** Uncertain annual-pair cross-tab, 2023/2024 and 2024/2025.
 * Copy this full supplied file into the GEE Code Editor without parameter edits.
 * PAS/non-PAS/invalid quality only: no pasture-age product or age inference.
 */
var MODE='full';
var VERSION='uncertain-pair-crosstab-v1';
var RUN_TAG='up1_20261015';
var SOURCE_SCRIPT='19a_export_uncertain_pair_crosstab_full_v1.js';
var K=require('users/barroso2501/pasture-crop:lib/constants');
var SOURCE_CODES=K.expectedSourceCodes();
var MISSING=-9999;
var PAIRS=[[2023,2024],[2024,2025]];
var LABELS=['observed_PAS','observed_nonPAS','NODATA','masked','unexpected'];
var PILOT_GRID_IDS=['IK-77','GH-123'];
var PILOT_CELL_IDS=['32173','18081'];
var FIXTURES=[{"case_id":"pair_0_0","previous_value":15,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":0,"expected_current":0},{"case_id":"pair_0_1","previous_value":15,"previous_masked":false,"current_value":3,"current_masked":false,"expected_previous":0,"expected_current":1},{"case_id":"pair_0_2","previous_value":15,"previous_masked":false,"current_value":27,"current_masked":false,"expected_previous":0,"expected_current":2},{"case_id":"pair_0_3","previous_value":15,"previous_masked":false,"current_value":null,"current_masked":true,"expected_previous":0,"expected_current":3},{"case_id":"pair_0_4","previous_value":15,"previous_masked":false,"current_value":999,"current_masked":false,"expected_previous":0,"expected_current":4},{"case_id":"pair_1_0","previous_value":3,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"pair_1_1","previous_value":3,"previous_masked":false,"current_value":3,"current_masked":false,"expected_previous":1,"expected_current":1},{"case_id":"pair_1_2","previous_value":3,"previous_masked":false,"current_value":27,"current_masked":false,"expected_previous":1,"expected_current":2},{"case_id":"pair_1_3","previous_value":3,"previous_masked":false,"current_value":null,"current_masked":true,"expected_previous":1,"expected_current":3},{"case_id":"pair_1_4","previous_value":3,"previous_masked":false,"current_value":999,"current_masked":false,"expected_previous":1,"expected_current":4},{"case_id":"pair_2_0","previous_value":27,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":2,"expected_current":0},{"case_id":"pair_2_1","previous_value":27,"previous_masked":false,"current_value":3,"current_masked":false,"expected_previous":2,"expected_current":1},{"case_id":"pair_2_2","previous_value":27,"previous_masked":false,"current_value":27,"current_masked":false,"expected_previous":2,"expected_current":2},{"case_id":"pair_2_3","previous_value":27,"previous_masked":false,"current_value":null,"current_masked":true,"expected_previous":2,"expected_current":3},{"case_id":"pair_2_4","previous_value":27,"previous_masked":false,"current_value":999,"current_masked":false,"expected_previous":2,"expected_current":4},{"case_id":"pair_3_0","previous_value":null,"previous_masked":true,"current_value":15,"current_masked":false,"expected_previous":3,"expected_current":0},{"case_id":"pair_3_1","previous_value":null,"previous_masked":true,"current_value":3,"current_masked":false,"expected_previous":3,"expected_current":1},{"case_id":"pair_3_2","previous_value":null,"previous_masked":true,"current_value":27,"current_masked":false,"expected_previous":3,"expected_current":2},{"case_id":"pair_3_3","previous_value":null,"previous_masked":true,"current_value":null,"current_masked":true,"expected_previous":3,"expected_current":3},{"case_id":"pair_3_4","previous_value":null,"previous_masked":true,"current_value":999,"current_masked":false,"expected_previous":3,"expected_current":4},{"case_id":"pair_4_0","previous_value":999,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":4,"expected_current":0},{"case_id":"pair_4_1","previous_value":999,"previous_masked":false,"current_value":3,"current_masked":false,"expected_previous":4,"expected_current":1},{"case_id":"pair_4_2","previous_value":999,"previous_masked":false,"current_value":27,"current_masked":false,"expected_previous":4,"expected_current":2},{"case_id":"pair_4_3","previous_value":999,"previous_masked":false,"current_value":null,"current_masked":true,"expected_previous":4,"expected_current":3},{"case_id":"pair_4_4","previous_value":999,"previous_masked":false,"current_value":999,"current_masked":false,"expected_previous":4,"expected_current":4},{"case_id":"source_code_1","previous_value":1,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"source_code_39","previous_value":39,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"source_code_26","previous_value":26,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"source_code_84","previous_value":84,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"source_code_91","previous_value":91,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":1,"expected_current":0},{"case_id":"source_code_0","previous_value":0,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":4,"expected_current":0},{"case_id":"source_code_minus9999","previous_value":-9999,"previous_masked":false,"current_value":15,"current_masked":false,"expected_previous":4,"expected_current":0},{"case_id":"masked_PAS_value","previous_value":15,"previous_masked":true,"current_value":15,"current_masked":false,"expected_previous":3,"expected_current":0},{"case_id":"masked_unexpected_value","previous_value":999,"previous_masked":true,"current_value":27,"current_masked":false,"expected_previous":3,"expected_current":2}];
var coverage=ee.Image(K.COVERAGE_ASSET);
var grid=ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa=ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var nativeProjections={};
[2023,2024,2025].forEach(function(y) {
  // Small metadata only. Projection.transform() is WKT, not coefficients.
  var info=coverage.select(K.coverageBandName(y)).projection().getInfo();
  if(!info || info.crs!==K.CRS || !Array.isArray(info.transform) ||
     info.transform.length!==6 || !info.transform.every(function(v,i) {
       return typeof v==='number' && isFinite(v) && Math.abs(v-K.CRS_TRANSFORM[i])<=1e-13;
     })) throw new Error('Native coverage projection differs for year '+y);
  nativeProjections[y]={crs:info.crs,transform:info.transform};
});
var RUNTIME=JSON.stringify({version:VERSION,coverage_asset:K.COVERAGE_ASSET,
  grid_asset:K.ANALYTICAL_GRID,constants_module:'users/barroso2501/pasture-crop:lib/constants',
  valid_source_codes:SOURCE_CODES,class_groups:K.CLASS_CODES,crs:K.CRS,
  crs_transform:K.CRS_TRANSFORM,square_metres_per_hectare:K.SQUARE_METRES_PER_HECTARE,
  pairs:PAIRS,observation_classes:LABELS,
  footprint_convention:'endpoint_unmask_sameFootprint_true_pair_support_intersection'});

// BEGIN_PAIR_CLASSIFICATION_ENGINE
function knownNonPAS(cov) {
  var result=cov.multiply(0).eq(1);
  SOURCE_CODES.forEach(function(code) {
    if(code!==15 && code!==27) result=result.or(cov.eq(code));
  });
  return result;
}
function endpointState(raw) {
  // Keep the original image footprint. Fill only masked values within it.
  var cov=raw.unmask(MISSING,true).toInt16();
  var observed=raw.mask().gt(0).unmask(0,true);
  var pas=cov.eq(15),non=knownNonPAS(cov);
  var state=cov.multiply(0).add(3).byte();
  state=state.where(observed.and(cov.eq(27)),2)
    .where(observed.and(non),1).where(observed.and(pas),0)
    .where(observed.and(pas.not()).and(non.not()).and(cov.neq(27)),4);
  return state;
}
function classifyPair(previousRaw,currentRaw) {
  var previous=endpointState(previousRaw),current=endpointState(currentRaw);
  var one=previous.multiply(0).add(1).multiply(current.multiply(0).add(1));
  var cells=[],count=one.multiply(0);
  for(var i=0;i<5;i++) for(var j=0;j<5;j++) {
    var mask=previous.eq(i).and(current.eq(j));
    cells.push(mask);count=count.add(mask);
  }
  var valid=previous.lt(2).and(current.lt(2));
  var uncertain=valid.not();
  var a=previousRaw.unmask(MISSING,true).toInt16();
  var b=currentRaw.unmask(MISSING,true).toInt16();
  var legacyValid=a.eq(15).or(knownNonPAS(a)).and(b.eq(15).or(knownNonPAS(b)));
  var previousPAS=uncertain.and(previous.eq(0));
  var currentPAS=uncertain.and(current.eq(0));
  var noObservedPAS=uncertain.and(previous.neq(0)).and(current.neq(0));
  return {previous:previous,current:current,cells:cells,domain:one,
    valid:valid,uncertain:uncertain,
    uncertain_previous_PAS:previousPAS,uncertain_current_PAS:currentPAS,
    uncertain_no_observed_PAS:noObservedPAS,
    entry:previous.eq(1).and(current.eq(0)),
    termination:previous.eq(0).and(current.eq(1)),
    partition_error:count.neq(1),
    legacy_uncertain_error:uncertain.neq(legacyValid.not()),
    conditional_partition_error:previousPAS.add(currentPAS).add(noObservedPAS).neq(uncertain)};
}
// END_PAIR_CLASSIFICATION_ENGINE

var AREA=['domain_ha','valid_pair_ha','uncertain_pair_ha',
  'uncertain_previous_PAS_ha','uncertain_current_PAS_ha','uncertain_no_observed_PAS_ha',
  'entry_ha','termination_ha'];
var ERRORS=['partition_error_pixel_equivalents','legacy_uncertain_error_pixel_equivalents',
  'conditional_partition_error_pixel_equivalents'];
var PAIR_FIELDS=[];
for(var i=0;i<5;i++) for(var j=0;j<5;j++) PAIR_FIELDS.push('p'+i+j+'_ha');
var METRICS=PAIR_FIELDS.concat(AREA).concat(ERRORS);
var KEYS=['cell_id','GRID_ID','source_batch_id','previous_year','event_year',
  'diagnostic_interval','scope','output_version','run_id'];
var allBands=[];
PAIRS.forEach(function(pair) {
  var result=classifyPair(coverage.select(K.coverageBandName(pair[0])),
    coverage.select(K.coverageBandName(pair[1])));
  var prefix='y'+pair[1]+'_';
  function area(mask,name){allBands.push(mask.multiply(pixelHa).rename(prefix+name).unmask(0,true));}
  PAIR_FIELDS.forEach(function(name,k){area(result.cells[k],name);});
  var areaMasks=[result.domain,result.valid,result.uncertain,result.uncertain_previous_PAS,
    result.uncertain_current_PAS,result.uncertain_no_observed_PAS,result.entry,result.termination];
  AREA.forEach(function(name,k){area(areaMasks[k],name);});
  [result.partition_error,result.legacy_uncertain_error,result.conditional_partition_error].forEach(function(mask,k){
    allBands.push(mask.toDouble().rename(prefix+ERRORS[k]).unmask(0,true));
  });
});
var image=ee.Image.cat(allBands);
var batches=MODE==='pilot'?[-1]:[0,1,2,3,4,5,6,7];
batches.forEach(function(batch){
  var selected=MODE==='pilot'?grid.filter(ee.Filter.inList('GRID_ID',PILOT_GRID_IDS)):
    grid.filter(ee.Filter.eq('source_batch_id',batch));
  var reduced=image.reduceRegions({collection:selected,reducer:ee.Reducer.sum(),
    crs:K.CRS,crsTransform:K.CRS_TRANSFORM,tileScale:16,maxPixelsPerRegion:100000000});
  var tables=PAIRS.map(function(pair){return reduced.map(function(f){
    var data={cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),source_batch_id:f.get('source_batch_id'),
      previous_year:pair[0],event_year:pair[1],diagnostic_interval:1,scope:MODE,
      output_version:VERSION,run_id:RUN_TAG+'_'+MODE};
    METRICS.forEach(function(name){data[name]=f.get('y'+pair[1]+'_'+name);});
    return ee.Feature(null,data);
  });});
  var table=tables[0].merge(tables[1]);
  var name='canonical_uncertain_pairs_'+(MODE==='pilot'?'pilot':'b'+('0'+batch).slice(-2))+'_v1';
  Export.table.toDrive({collection:table,description:name,fileNamePrefix:name,
    folder:'uncertain_pair_crosstab_v1',fileFormat:'CSV',selectors:KEYS.concat(METRICS)});
  print('TASK:',name,'| two annual pairs per cell');
});
var manifestName='canonical_uncertain_pairs_manifest_'+MODE+'_v1';
Export.table.toDrive({collection:ee.FeatureCollection([ee.Feature(null,{
  scope:MODE,output_version:VERSION,run_id:RUN_TAG+'_'+MODE,source_script:SOURCE_SCRIPT,
  expected_cells:MODE==='pilot'?2:24889,expected_rows:MODE==='pilot'?4:49778,
  config_json:RUNTIME,pilot_cell_ids_json:JSON.stringify(PILOT_CELL_IDS),
  native_projections_json:JSON.stringify(nativeProjections),
  coverage_band_count:coverage.bandNames().size(),
  coverage_bands_csv:ee.List(coverage.bandNames()).join('|')})]),
  description:manifestName,fileNamePrefix:manifestName,folder:'uncertain_pair_crosstab_v1',fileFormat:'CSV',
  selectors:['scope','output_version','run_id','source_script','expected_cells','expected_rows',
    'config_json','pilot_cell_ids_json','native_projections_json','coverage_band_count','coverage_bands_csv']});

if(MODE==='pilot') {
  // All fixtures share ONE small native reduction, avoiding concurrent aggregations.
  var region=ee.Geometry.Rectangle([-47,-16,-46.999,-15.999],K.CRS,false);
  var nativeBands=[];
  FIXTURES.forEach(function(test,index){
    function fixture(value,masked){var im=ee.Image.constant(value===null?0:value);
      return masked?im.updateMask(ee.Image.constant(0)):im;}
    var result=classifyPair(fixture(test.previous_value,test.previous_masked),fixture(test.current_value,test.current_masked));
    var masks=[result.domain,result.previous.neq(test.expected_previous),result.current.neq(test.expected_current),
      result.cells[test.expected_previous*5+test.expected_current].neq(1),result.partition_error,
      result.legacy_uncertain_error,result.conditional_partition_error];
    masks.forEach(function(mask,k){nativeBands.push(mask.toDouble().rename('f'+index+'_'+k));});
  });
  var totals=ee.Image.cat(nativeBands).reduceRegion({reducer:ee.Reducer.sum(),geometry:region,
    crs:K.CRS,crsTransform:K.CRS_TRANSFORM,maxPixels:10000});
  var nativeFeatures=FIXTURES.map(function(test,index){
    return ee.Feature(null,{case_id:test.case_id,scope:'native_synthetic',output_version:VERSION,
      run_id:RUN_TAG+'_pilot_synthetic',expected_previous:test.expected_previous,expected_current:test.expected_current,
      test_pixel_equivalents:totals.get('f'+index+'_0'),previous_state_error:totals.get('f'+index+'_1'),
      current_state_error:totals.get('f'+index+'_2'),cross_classification_error:totals.get('f'+index+'_3'),
      partition_error:totals.get('f'+index+'_4'),legacy_uncertain_error:totals.get('f'+index+'_5'),
      conditional_partition_error:totals.get('f'+index+'_6')});
  });
  Export.table.toDrive({collection:ee.FeatureCollection(nativeFeatures),description:'canonical_uncertain_pairs_native_synthetic_v1',
    fileNamePrefix:'canonical_uncertain_pairs_native_synthetic_v1',folder:'uncertain_pair_crosstab_v1',fileFormat:'CSV',
    selectors:['case_id','scope','output_version','run_id','expected_previous','expected_current',
      'test_pixel_equivalents','previous_state_error','current_state_error','cross_classification_error',
      'partition_error','legacy_uncertain_error','conditional_partition_error']});
  print('PILOT: THREE tasks. Return all three CSVs after Drive finishes writing them.');
} else {print('FULL: NINE tasks. Preserve the accepted pilot native CSV for validation.');}
print('No global PAS-overlap conclusion until the FULL exports pass legacy-total checks.');

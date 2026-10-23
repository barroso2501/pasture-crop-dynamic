/** FULL entry/re-entry export: 64 interval/batch tables, 8 history audits, 1 manifest.
 * Run this full file unchanged. Native pilot is preserved and NOT rerun.
 * Metadata asynchronous; export creation yields to the UI between tasks.
 */
var VERSION='entry-reentry-full-v1',RUN_TAG='er1_full_20261021';
var SOURCE_SCRIPT='20c_export_entry_reentry_full_v1.js';
var K=require('users/barroso2501/pasture-crop:lib/constants');
var SOURCE_CODES=K.expectedSourceCodes(),MISSING=-9999,START=1985,END=2025;
var INTERVALS=[[1985, 1990], [1990, 1995], [1995, 2000], [2000, 2005], [2005, 2010], [2010, 2015], [2015, 2020], [2020, 2025]];
var BATCHES=[0,1,2,3,4,5,6,7],FOLDER='entry_reentry_full_v1';
var AREAS=["domain_ha","flow_pas_tmp_ha","stock0_pas_ha","initial_ha","entry_ha","unresolved_ha","first_observed_entry_ha","observed_reentry_ha","prior_history_uncertain_ha","initial_pas_stock_ha","entry_pas_stock_ha","unresolved_pas_stock_ha","first_observed_entry_pas_stock_ha","observed_reentry_pas_stock_ha","prior_history_uncertain_pas_stock_ha","control_initial_ha","control_entry_ha","control_unresolved_ha","control_initial_pas_stock_ha","control_entry_pas_stock_ha","control_unresolved_pas_stock_ha"];
var CELL_ERRORS=["accepted_origin_mismatch_pixel_equivalents"];
var KEYS=["cell_id","GRID_ID","source_batch_id","t0","t1","diagnostic_interval","scope","output_version","run_id"];
var ERRORS=["origin_partition_error_pixel_years","initial_continuity_error_pixel_years","auxiliary_partition_error_pixel_years","entry_label_error_pixel_years","frozen_label_error_pixel_years","entry_age201_error_pixel_years","reentry_age201_error_pixel_years","auxiliary_age_error_pixel_years","entry_count_error_pixel_years","entry_metadata_error_pixel_years"];
var AUDIT_COUNTS=["history_support_pixel_equivalents","confirmed_entry_pixel_years","confirmed_reentry_pixel_years","first_observed_entry_pixel_years","prior_history_uncertain_entry_pixel_years"];
var BOUNDARY_AREAS=["entry_2024_ha","termination_2024_ha","entry_2025_ha","termination_2025_ha"];
var AUDIT_KEYS=["cell_id","GRID_ID","source_batch_id","start_year","end_year","years_checked","scope","output_version","run_id"];
// BEGIN_ACCEPTED_REFERENCE_ENGINE
// Same categorical update as accepted 17g, with the base year parameterized.
// States: 0 observed non-PAS, 1 continuous since base, 2 observed entry,
// 3 unresolved PAS, 4 uncertain observation. Audits are pixel-year sums.
function reconstruct(base,t0,getCoverage,expectedStates) {
  var previous=ee.Image.constant(4).byte();
  var continuous=ee.Image.constant(1);
  var partitionErrors=ee.Image.constant(0);
  var initialErrors=ee.Image.constant(0);
  var entryErrors=ee.Image.constant(0);
  var expectedErrors=ee.Image.constant(0);
  for(var year=base;year<=t0;year++) {
    var cov=getCoverage(year).unmask(MISSING).toInt16();
    var pas=cov.eq(15);
    var non=ee.Image.constant(0).eq(1);
    SOURCE_CODES.forEach(function(code) {
      if(code!==15 && code!==27) non=non.or(cov.eq(code));
    });
    var initial=year===base ? pas : pas.and(previous.eq(1));
    var entered=year===base ? ee.Image.constant(0).eq(1) :
      pas.and(previous.eq(0));
    var continued=year===base ? ee.Image.constant(0).eq(1) :
      pas.and(previous.eq(2));
    var current=ee.Image.constant(4).byte().where(non,0).where(initial,1)
      .where(entered.or(continued),2)
      .where(pas.and(initial.not()).and(entered.not())
        .and(continued.not()),3);
    continuous=continuous.and(pas);
    var originCount=current.eq(1).add(current.eq(2)).add(current.eq(3));
    partitionErrors=partitionErrors.add(pas.and(originCount.neq(1))
      .or(pas.not().and(originCount.neq(0))).unmask(0));
    initialErrors=initialErrors.add(current.eq(1).neq(continuous).unmask(0));
    if(year!==base) {
      entryErrors=entryErrors.add(entered.and(current.neq(2)).unmask(0));
    }
    if(expectedStates) {
      expectedErrors=expectedErrors.add(current.neq(expectedStates[year-base]).unmask(0));
    }
    previous=current;
  }
  return {state:previous,partitionErrors:partitionErrors,
    initialErrors:initialErrors,entryErrors:entryErrors,
    expectedErrors:expectedErrors};
}
// END_ACCEPTED_REFERENCE_ENGINE
// BEGIN_ENTRY_REENTRY_ENGINE
function emptyEntryState() {
  var z=ee.Image.constant(0).toInt16();
  return {state:z.add(4).byte(),age:z,kind:z,entryYear:z,count:z,
    everPAS:z.eq(1),everGap:z.eq(1),continuous:z.eq(0)};
}
function advanceEntry(p,raw,year,first) {
  var cov=raw.unmask(MISSING,true).toInt16();
  var pas=cov.eq(15),non=ee.Image.constant(0).eq(1);
  SOURCE_CODES.forEach(function(code){if(code!==15 && code!==27) non=non.or(cov.eq(code));});
  var valid=pas.or(non),zero=ee.Image.constant(0).toInt16();
  var initial=first?pas:pas.and(p.state.eq(1));
  var entered=first?zero.eq(1):pas.and(p.state.eq(0));
  var continued=first?zero.eq(1):pas.and(p.state.eq(2));
  var unresolved=pas.and(initial.not()).and(entered.not()).and(continued.not());
  var state=zero.add(4).byte().where(non,0).where(initial,1)
    .where(entered.or(continued),2).where(unresolved,3);
  // p.everPAS and p.everGap are strictly prior to the current entry.
  // Freeze the entry label and year throughout its confirmed spell.
  var atEntry=zero.where(p.everPAS,2).where(p.everPAS.not().and(p.everGap.not()),1)
    .where(p.everPAS.not().and(p.everGap),3);
  var kind=zero.where(entered,atEntry).where(continued,p.kind);
  var age=zero.where(initial,100).where(entered,201).where(continued,p.age.add(1));
  var entryYear=zero.where(entered,year).where(continued,p.entryYear);
  var count=p.count.add(entered);
  var continuous=p.continuous.and(pas);
  var terminated=first?zero.eq(1):non.and(p.state.eq(1).or(p.state.eq(2)).or(p.state.eq(3)));
  var originCount=state.eq(1).add(state.eq(2)).add(state.eq(3));
  var kindCount=kind.eq(1).add(kind.eq(2)).add(kind.eq(3));
  var expectedAge=zero.where(state.eq(1),100).where(entered,201)
    .where(continued,p.age.add(1));
  var errors={
    origin_partition_error_pixel_years:originCount.neq(pas),
    initial_continuity_error_pixel_years:state.eq(1).neq(continuous),
    auxiliary_partition_error_pixel_years:kindCount.neq(state.eq(2)),
    entry_label_error_pixel_years:entered.and(kind.neq(atEntry)),
    frozen_label_error_pixel_years:continued.and(kind.neq(p.kind).or(entryYear.neq(p.entryYear))),
    entry_age201_error_pixel_years:entered.and(age.neq(201)),
    reentry_age201_error_pixel_years:entered.and(kind.eq(2)).and(age.neq(201)),
    auxiliary_age_error_pixel_years:age.neq(expectedAge),
    entry_count_error_pixel_years:count.neq(p.count.add(entered)),
    entry_metadata_error_pixel_years:state.eq(2).and(entryYear.lte(START).or(entryYear.gt(year)))
      .or(state.neq(2).and(entryYear.neq(0)))
  };
  return {state:state,age:age,kind:kind,entryYear:entryYear,count:count,
    everPAS:p.everPAS.or(pas),everGap:p.everGap.or(valid.not()),continuous:continuous,
    entered:entered,terminated:terminated,errors:errors};
}
// END_ENTRY_REENTRY_ENGINE
var coverage=ee.Image(K.COVERAGE_ASSET),grid=ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa=ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
function readCoverage(year){return coverage.select(K.coverageBandName(year));}
function inCodes(image,codes){var hit=image.eq(codes[0]);for(var i=1;i<codes.length;i++)hit=hit.or(image.eq(codes[i]));return hit;}
// BEGIN_ACCEPTED_R2_HISTORY_AUDIT
var STATE_FIELDS=['state','age','kind','entryYear','count','everPAS','everGap','continuous'];
var SNAPSHOT_FIELDS=['snapshot2015_state','snapshot2015_kind','snapshot2020_state','snapshot2020_kind'];
var EVENT_COUNTS=AUDIT_COUNTS.slice(1);
function packEntry(p){return ee.Image.cat(STATE_FIELDS.map(function(k){return p[k].rename(k);})).toInt16();}
function unpackEntry(image){var p={};STATE_FIELDS.forEach(function(k){p[k]=image.select(k);});return p;}
function serverCoverage(year){return coverage.select(ee.String('classification_').cat(ee.Number(year).format('%d')));}
function makeRealAccumulator(p){
  var parts=[packEntry(p)];
  ERRORS.forEach(function(k){parts.push(p.errors[k].toDouble().unmask(0,true).rename('audit_'+k));});
  var events=[p.entered,p.entered.and(p.kind.eq(2)),p.entered.and(p.kind.eq(1)),p.entered.and(p.kind.eq(3))];
  EVENT_COUNTS.forEach(function(k,j){parts.push(events[j].toDouble().unmask(0,true).rename('audit_'+k));});
  BOUNDARY_AREAS.concat(SNAPSHOT_FIELDS).forEach(function(k){parts.push(ee.Image.constant(0).toInt16().rename(k));});
  return ee.Image.cat(parts);
}
function realIteration(year,accumulator){
  year=ee.Number(year);var previous=ee.Image(accumulator),p=unpackEntry(previous);
  var next=advanceEntry(p,serverCoverage(year),year,false),parts=[packEntry(next)];
  ERRORS.forEach(function(k){parts.push(previous.select('audit_'+k).add(next.errors[k].unmask(0,true)).rename('audit_'+k));});
  var events=[next.entered,next.entered.and(next.kind.eq(2)),next.entered.and(next.kind.eq(1)),next.entered.and(next.kind.eq(3))];
  EVENT_COUNTS.forEach(function(k,j){parts.push(previous.select('audit_'+k).add(events[j].unmask(0,true)).rename('audit_'+k));});
  BOUNDARY_AREAS.forEach(function(k){
    var targetYear=k.indexOf('2024')>=0?2024:2025;
    var event=k.indexOf('termination_')===0?next.terminated:next.entered;
    parts.push(previous.select(k).where(ee.Image.constant(year).eq(targetYear),event).rename(k));
  });
  SNAPSHOT_FIELDS.forEach(function(k){
    var targetYear=k.indexOf('2015')>=0?2015:2020;
    var value=k.slice(-5)==='state'?next.state:next.kind;
    parts.push(previous.select(k).where(ee.Image.constant(year).eq(targetYear),value).rename(k));
  });
  return ee.Image.cat(parts);
}
function walkRealHistory(){
  var first=advanceEntry(emptyEntryState(),readCoverage(START),START,true);
  return ee.Image(ee.List.sequence(START+1,END).iterate(realIteration,makeRealAccumulator(first)));
}
// END_ACCEPTED_R2_HISTORY_AUDIT

// BEGIN_FULL_ENDPOINT_WALKER
// The accepted categorical formula, with its own carried state and no auxiliary inputs.
function acceptedOriginStep(previous,raw,first){
  var cov=raw.unmask(MISSING,true).toInt16(),pas=cov.eq(15),non=ee.Image.constant(0).eq(1);
  SOURCE_CODES.forEach(function(code){if(code!==15 && code!==27)non=non.or(cov.eq(code));});
  var initial=first?pas:pas.and(previous.eq(1));
  var entered=first?ee.Image.constant(0).eq(1):pas.and(previous.eq(0));
  var continued=first?ee.Image.constant(0).eq(1):pas.and(previous.eq(2));
  return ee.Image.constant(4).byte().where(non,0).where(initial,1).where(entered.or(continued),2)
    .where(pas.and(initial.not()).and(entered.not()).and(continued.not()),3);
}
function walkEndpoint(t0){
  var first=advanceEntry(emptyEntryState(),readCoverage(START),START,true);
  var ref=acceptedOriginStep(ee.Image.constant(4).byte(),readCoverage(START),true);
  var seed=ee.Image.cat([packEntry(first),ref.rename('accepted_state')]);
  if(t0===START)return seed; // Empty subsequent-year sequence: preserve the baseline construction.
  return ee.Image(ee.List.sequence(START+1,t0).iterate(function(year,accumulator){
    year=ee.Number(year);var previous=ee.Image(accumulator),raw=serverCoverage(year);
    var current=advanceEntry(unpackEntry(previous),raw,year,false);
    var accepted=acceptedOriginStep(previous.select('accepted_state'),raw,false);
    return ee.Image.cat([packEntry(current),accepted.rename('accepted_state')]);
  },seed));
}
// END_FULL_ENDPOINT_WALKER

var RUNTIME={version:VERSION,coverage_asset:K.COVERAGE_ASSET,grid_asset:K.ANALYTICAL_GRID,
  constants_module:'users/barroso2501/pasture-crop:lib/constants',valid_source_codes:SOURCE_CODES,
  class_groups:K.CLASS_CODES,crs:K.CRS,crs_transform:K.CRS_TRANSFORM,
  square_metres_per_hectare:K.SQUARE_METRES_PER_HECTARE,start_year:START,end_year:END,
  intervals:INTERVALS,footprint_convention:'accepted_coverage_unmask_sameFootprint_true_no_gap_bridging',
  auxiliary_labels:{none:0,first_observed_entry:1,observed_reentry:2,prior_history_uncertain:3},
  tile_scale:16,max_pixels_per_region:100000000,expected_cells:24889,batches:BATCHES,history_audit_years:41};
var EXPECTED_RUNTIME={"version":"entry-reentry-full-v1","coverage_asset":"projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3","grid_asset":"projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3","constants_module":"users/barroso2501/pasture-crop:lib/constants","valid_source_codes":[1,3,4,5,6,7,9,10,11,12,13,15,19,20,21,22,23,24,25,26,27,29,30,31,32,33,35,36,39,40,41,46,47,48,49,50,62,75,84,91],"class_groups":{"NAT":[1,3,4,5,6,7,10,11,12,13,29,32,49,50,84],"PAS":[15],"TMP":[19,20,39,40,41,62],"OAG":[9,21,35,36,46,47,48],"OUT":[22,23,24,25,30,75,91],"WATER":[26,31,33],"NODATA":[27]},"crs":"EPSG:4326","crs_transform":[0.00026949458523585647,0,-74.02073025380652,0,-0.00026949458523585647,5.405791885246045],"start_year":1985,"end_year":2025,"intervals":[[1985,1990],[1990,1995],[1995,2000],[2000,2005],[2005,2010],[2010,2015],[2015,2020],[2020,2025]],"footprint_convention":"accepted_coverage_unmask_sameFootprint_true_no_gap_bridging","square_metres_per_hectare":10000,"auxiliary_labels":{"none":0,"first_observed_entry":1,"observed_reentry":2,"prior_history_uncertain":3},"tile_scale":16,"max_pixels_per_region":100000000,"expected_cells":24889,"batches":[0,1,2,3,4,5,6,7],"history_audit_years":41};
var MANIFEST_FIELDS=["scope","output_version","run_id","source_script","expected_cells","expected_rows","expected_audit_rows","expected_cell_files","expected_audit_files","config_json","coverage_band_count","coverage_bands_csv","native_projections_json","audit_start_year","audit_end_year","audit_years_checked","runtime_grid_cells","runtime_b00_cells","runtime_b01_cells","runtime_b02_cells","runtime_b03_cells","runtime_b04_cells","runtime_b05_cells","runtime_b06_cells","runtime_b07_cells"];
function canonical(value){if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
  if(value && typeof value==='object')return '{'+Object.keys(value).sort().map(function(k){return JSON.stringify(k)+':'+canonical(value[k]);}).join(',')+'}';
  return JSON.stringify(value);}
if(canonical(RUNTIME)!==canonical(EXPECTED_RUNTIME))throw new Error('Installed constants differ from the supplied full configuration');
function batchName(batch){return 'b'+('0'+batch).slice(-2);}
function exportCSV(table,name,fields){Export.table.toDrive({collection:table,description:name,fileNamePrefix:name,
  folder:FOLDER,fileFormat:'CSV',selectors:fields});}
function identity(f){return {cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),source_batch_id:f.get('source_batch_id'),
  scope:'full',output_version:VERSION,run_id:RUN_TAG+'_full'};}
var endpointImages={},auditImage=null;
function intervalImage(t0,t1){
  if(endpointImages[t0])return endpointImages[t0];
  var endpoint=walkEndpoint(t0),state=endpoint.select('state'),kind=endpoint.select('kind'),control=endpoint.select('accepted_state');
  var pas=readCoverage(t0).unmask(MISSING,true).eq(15);
  var flow=pas.and(inCodes(readCoverage(t1).unmask(MISSING,true),K.CLASS_CODES.TMP)),bands=[];
  function area(mask,name){bands.push(mask.multiply(pixelHa).rename(name).unmask(0,true));}
  area(ee.Image.constant(1),'domain_ha');area(flow,'flow_pas_tmp_ha');area(pas,'stock0_pas_ha');
  ['initial','entry','unresolved'].forEach(function(k,j){
    area(flow.and(state.eq(j+1)),k+'_ha');area(pas.and(state.eq(j+1)),k+'_pas_stock_ha');
    area(flow.and(control.eq(j+1)),'control_'+k+'_ha');area(pas.and(control.eq(j+1)),'control_'+k+'_pas_stock_ha');
  });
  ['first_observed_entry','observed_reentry','prior_history_uncertain'].forEach(function(k,j){
    area(flow.and(state.eq(2)).and(kind.eq(j+1)),k+'_ha');area(pas.and(state.eq(2)).and(kind.eq(j+1)),k+'_pas_stock_ha');
  });
  bands.push(state.neq(control).toDouble().rename(CELL_ERRORS[0]).unmask(0,true));
  endpointImages[t0]=ee.Image.cat(bands);return endpointImages[t0];
}
function historyAuditImage(){
  if(auditImage)return auditImage;
  var history=walkRealHistory(),bands=[ee.Image.constant(1).toDouble().rename('history_support_pixel_equivalents')];
  EVENT_COUNTS.concat(ERRORS).forEach(function(k){bands.push(history.select('audit_'+k).toDouble().rename(k).unmask(0,true));});
  BOUNDARY_AREAS.forEach(function(k){bands.push(history.select(k).multiply(pixelHa).rename(k).unmask(0,true));});
  auditImage=ee.Image.cat(bands);return auditImage;
}
function selectedBatch(batch){return grid.filter(ee.Filter.eq('source_batch_id',batch));}
function reduceBatch(image,batch){return image.reduceRegions({collection:selectedBatch(batch),reducer:ee.Reducer.sum(),
  crs:K.CRS,crsTransform:K.CRS_TRANSFORM,tileScale:16,maxPixelsPerRegion:100000000});}
function createIntervalTask(job){
  var reduced=reduceBatch(intervalImage(job.t0,job.t1),job.batch);
  var table=reduced.map(function(f){var data=identity(f);data.t0=job.t0;data.t1=job.t1;data.diagnostic_interval=job.t0===2020?1:0;
    AREAS.concat(CELL_ERRORS).forEach(function(k){data[k]=f.get(k);});return ee.Feature(null,data);});
  exportCSV(table,job.name,KEYS.concat(AREAS).concat(CELL_ERRORS));
}
function createAuditTask(job){
  var table=reduceBatch(historyAuditImage(),job.batch).map(function(f){var data=identity(f);
    data.start_year=START;data.end_year=END;data.years_checked=41;
    AUDIT_COUNTS.concat(ERRORS).concat(BOUNDARY_AREAS).forEach(function(k){data[k]=f.get(k);});return ee.Feature(null,data);});
  exportCSV(table,job.name,AUDIT_KEYS.concat(AUDIT_COUNTS).concat(ERRORS).concat(BOUNDARY_AREAS));
}
function createAllTasks(nativeProjections,actualBands){
  var jobs=[];
  INTERVALS.forEach(function(pair){BATCHES.forEach(function(batch){jobs.push({kind:'cells',t0:pair[0],t1:pair[1],batch:batch,
    name:'canonical_entry_reentry_'+pair[0]+'_'+pair[1]+'_'+batchName(batch)+'_v1'});});});
  BATCHES.forEach(function(batch){jobs.push({kind:'audit',batch:batch,name:'canonical_entry_reentry_history_audit_'+batchName(batch)+'_v1'});});
  jobs.push({kind:'manifest',name:'canonical_entry_reentry_manifest_full_v1'});
  var completed=0;
  function dispatch(){
    var job=jobs[completed];
    try{
      if(job.kind==='cells')createIntervalTask(job);
      else if(job.kind==='audit')createAuditTask(job);
      else{
        var data={scope:'full',output_version:VERSION,run_id:RUN_TAG+'_full',source_script:SOURCE_SCRIPT,
          expected_cells:24889,expected_rows:199112,expected_audit_rows:24889,expected_cell_files:64,expected_audit_files:8,
          config_json:JSON.stringify(RUNTIME),coverage_band_count:actualBands.length,coverage_bands_csv:actualBands.join('|'),
          native_projections_json:JSON.stringify(nativeProjections),audit_start_year:START,audit_end_year:END,audit_years_checked:41,
          runtime_grid_cells:grid.size()};
        BATCHES.forEach(function(b){data['runtime_'+batchName(b)+'_cells']=selectedBatch(b).size();});
        exportCSV(ee.FeatureCollection([ee.Feature(null,data)]),job.name,MANIFEST_FIELDS);
      }
    }catch(error){print('ERRO ao preparar '+job.name+'. A criacao foi interrompida:',error);return;}
    completed++;
    if(completed%8===0 || completed===jobs.length)print('Tarefas criadas: '+completed+'/'+jobs.length+'; ultima: '+job.name);
    if(completed<jobs.length)ui.util.setTimeout(dispatch,75);
    else print('COMPLETO: 73 tarefas criadas. Inicie por grupos. Retorne 73 CSVs da pasta '+FOLDER+'. Nao repita o piloto.');
  }
  print('Metadados aprovados. Criando gradualmente 64 tabelas, 8 auditorias e 1 manifesto.');
  dispatch();
}
print('FULL: consultando os metadados de forma assincrona. Aguarde a mensagem de 73 tarefas criadas.');
coverage.evaluate(function(info,error){
  if(error){print('ERRO DE METADADOS; nenhuma tarefa criada:',error);return;}
  var bands=info && info.bands;
  if(!Array.isArray(bands) || bands.length!==41){print('ERRO: esperado inventario de 41 bandas; nenhuma tarefa criada.');return;}
  var names=[],projections={};
  for(var i=0;i<41;i++){
    var year=START+i,b=bands[i],transform=b.crs_transform;
    if(b.id!==K.coverageBandName(year) || b.crs!==K.CRS || !Array.isArray(transform) || transform.length!==6 ||
      !transform.every(function(v,k){return typeof v==='number' && isFinite(v) && Math.abs(v-K.CRS_TRANSFORM[k])<=1e-13;})){
      print('ERRO: metadados nativos diferentes em '+year+'; nenhuma tarefa criada.');return;
    }
    names.push(b.id);projections[year]={crs:b.crs,transform:transform};
  }
  createAllTasks(projections,names);
});

/* Eager local adapter for the complete production script. No network and no native GEE execution. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'gee/20c_export_entry_reentry_full_v1.js'),'utf8');
const C=JSON.parse(fs.readFileSync(path.join(root,'config/entry_reentry_full_v1.json')));
const S=JSON.parse(fs.readFileSync(path.join(root,'config/entry_reentry_full_schema_v1.json')));
const fixtures=JSON.parse(fs.readFileSync(path.join(root,'provenance/entry_reentry_pilot_r2/config/entry_reentry_native_cases_v1.json')));
const number=x=>x instanceof N?x.value:Number(x);
class N{constructor(x){this.value=number(x);} add(x){return new N(this.value+number(x));} format(){return new Str(String(this.value));} valueOf(){return this.value;}}
class Str{constructor(x){this.value=x instanceof Str?x.value:String(x);} cat(x){return new Str(this.value+String(x));} toString(){return this.value;}}
class L{constructor(x){this.value=x instanceof L?x.value:x;} get(i){i=number(i);return this.value.at(i);} iterate(fn,seed){return this.value.reduce((acc,x)=>fn(x,acc),seed);}}
class Img{
 constructor(bands){this.bands=bands;}
 static constant(v){const list=v instanceof L?v.value:Array.isArray(v)?v:[v];return new Img(Object.fromEntries(list.map((x,i)=>[i?'constant_'+i:'constant',{v:number(x),m:true}])));}
 select(names){names=Array.isArray(names)?names:[String(names)];return new Img(Object.fromEntries(names.map(n=>{assert.ok(n in this.bands,'missing image band '+n);return[n,this.bands[n]];})));}
 rename(names){names=Array.isArray(names)?names:[names];const values=Object.values(this.bands);assert.equal(names.length,values.length);return new Img(Object.fromEntries(names.map((n,i)=>[n,values[i]])));}
 op(other,fn){other=other instanceof Img?other:Img.constant(other);const a=Object.entries(this.bands),b=Object.entries(other.bands);
  assert.ok(a.length===b.length||a.length===1||b.length===1,'broadcast mismatch');const len=Math.max(a.length,b.length),result={};
  for(let i=0;i<len;i++){const [na,va]=a[a.length===1?0:i],[nb,vb]=b[b.length===1?0:i];result[a.length===1&&b.length>1?nb:na]={v:fn(va.v,vb.v),m:va.m&&vb.m};}return new Img(result);}
 add(v){return this.op(v,(a,b)=>a+b);} multiply(v){return this.op(v,(a,b)=>a*b);} divide(v){return this.op(v,(a,b)=>a/b);}
 eq(v){return this.op(v,(a,b)=>+(a===b));} neq(v){return this.op(v,(a,b)=>+(a!==b));}
 lt(v){return this.op(v,(a,b)=>+(a<b));} lte(v){return this.op(v,(a,b)=>+(a<=b));} gt(v){return this.op(v,(a,b)=>+(a>b));} gte(v){return this.op(v,(a,b)=>+(a>=b));}
 and(v){return this.op(v,(a,b)=>+(!!a&&!!b));} or(v){return this.op(v,(a,b)=>+(!!a||!!b));} not(){return this.op(0,a=>+!a);}
 where(test,value){value=value instanceof Img?value:Img.constant(value);const t=Object.values(test.bands),v=Object.values(value.bands),a=Object.entries(this.bands);
  return new Img(Object.fromEntries(a.map(([k,x],i)=>{const y=t[t.length===1?0:i],z=v[v.length===1?0:i];return[k,x.m&&y.m&&y.v&&z.m?{v:z.v,m:true}:x];})));}
 unmask(v,same=true){assert.equal(same,true);return new Img(Object.fromEntries(Object.entries(this.bands).map(([k,x])=>[k,x.m?x:{v:number(v),m:true}])));}
 updateMask(mask){const b=Object.values(mask.bands);return new Img(Object.fromEntries(Object.entries(this.bands).map(([k,x],i)=>[k,{v:x.v,m:x.m&&b[b.length===1?0:i].m&&!!b[b.length===1?0:i].v}])));}
 byte(){return this;} toDouble(){return this;} toInt16(){return this;}
 reduceRegion(){return {get:k=>{assert.ok(k in this.bands,'missing reduction band '+k);const x=this.bands[k];return x.m?x.v:0;}};}
 reduceRegions(args){assert.equal(args.maxPixelsPerRegion,1e8);assert.deepEqual(Array.from(args.crsTransform),C.crs_transform);return new FC(args.collection.features.map(f=>new Feature({...f.data,...Object.fromEntries(Object.entries(this.bands).map(([k,x])=>[k,x.m?x.v:0]))})));}
}
class Feature{constructor(data){this.data=data;}get(k){assert.ok(k in this.data,'missing feature field '+k);return this.data[k];}}
class FC{constructor(features){this.features=features;}filter(f){return new FC(this.features.filter(x=>f.eq?x.data[f.field]===f.value:f.values.includes(x.data[f.field])));}size(){return new N(this.features.length);}map(fn){return new FC(this.features.map(fn));}merge(other){return new FC(this.features.concat(other.features));}}
function run(history,mode='valid'){
 const exports=[],callbacks=[],timers=[],messages=[];
 const testCells=Array.from({length:8},(_,b)=>({cell_id:String(1000+b),GRID_ID:'test-'+b,source_batch_id:b}));
 testCells[1]={cell_id:'18081',GRID_ID:'GH-123',source_batch_id:1};testCells[5]={cell_id:'32173',GRID_ID:'IK-77',source_batch_id:5};
 const coverage={select:name=>{const y=Number(String(name).replace('classification_','')),i=y-1985;assert.ok(i>=0&&i<41);const j=Math.min(i,history.values.length-1);return Img.constant(history.values[j]).updateMask(Img.constant(history.masked[j]?0:1));},evaluate:fn=>callbacks.push(fn)};
 function Image(value){if(value instanceof Img)return value;if(value===C.coverage_asset)return coverage;throw Error('Unexpected Image constructor '+value);}
 Image.constant=Img.constant;Image.pixelArea=()=>Img.constant(10000);Image.cat=function(parts){return new Img(Object.assign({},...parts.map(x=>x.bands)));};
 function List(v){return v instanceof L?v:new L(v);}List.sequence=(start,end)=>{assert.ok(number(end)>=number(start),'empty sequence must be handled explicitly');return new L(Array.from({length:number(end)-number(start)+1},(_,i)=>number(start)+i));};
 const K={COVERAGE_ASSET:C.coverage_asset,ANALYTICAL_GRID:C.grid_asset,CRS:C.crs,CRS_TRANSFORM:C.crs_transform,CLASS_CODES:C.class_groups,SQUARE_METRES_PER_HECTARE:10000,expectedSourceCodes:()=>C.valid_source_codes,coverageBandName:y=>'classification_'+y};
 const ee={Image,List,Number:x=>new N(x),String:x=>new Str(x),Feature:(_,data)=>new Feature(data),FeatureCollection:x=>typeof x==='string'?new FC(testCells.map(x=>new Feature(x))):new FC(x),Filter:{inList:(field,values)=>({field,values}),eq:(field,value)=>({field,value,eq:true})},Reducer:{sum:()=>({})},Geometry:{Rectangle:()=>({})}};
 const ui={util:{setTimeout:(fn,delay)=>{assert.ok(delay>0);timers.push(fn);return timers.length;}}};
 const context=vm.createContext({ee,ui,require:()=>K,print:(...x)=>messages.push(x),Export:{table:{toDrive:x=>exports.push(x)}}});
 vm.runInContext(source,context,{timeout:10000});assert.equal(callbacks.length,1);assert.equal(exports.length,0);
 if(mode==='error'){callbacks[0](null,'test metadata failure');assert.equal(exports.length,0);assert.equal(timers.length,0);return;}
 const bands=Array.from({length:41},(_,i)=>({id:'classification_'+(1985+i),crs:C.crs,crs_transform:[...C.crs_transform]}));
 if(mode==='invalid')bands[10].crs_transform[0]=.1;
 callbacks[0]({bands},null);
 if(mode==='invalid'){assert.equal(exports.length,0);assert.equal(timers.length,0);return;}
 assert.equal(exports.length,1,'one task before yielding to the UI');assert.equal(timers.length,1);
 let dispatched=0;while(timers.length){timers.shift()();assert.ok(++dispatched<=72);}
 assert.equal(exports.length,73);assert.equal(dispatched,72);assert.equal(new Set(exports.map(x=>x.fileNamePrefix)).size,73);
 for(const e of exports){assert.equal(e.folder,'entry_reentry_full_v1');
  const kind=e.fileNamePrefix.includes('manifest')?'manifest':e.fileNamePrefix.includes('history_audit')?'audit':'cells';
  assert.deepEqual(Array.from(e.selectors),S[{cells:'cell_fields',audit:'audit_fields',manifest:'manifest_fields'}[kind]],'full selector contract');
  assert.equal(e.collection.features.length,1,'one mock cell per batch, one mock manifest');
  for(const f of e.collection.features){for(const k of e.selectors)assert.ok(k in f.data && f.data[k]!==undefined && f.data[k]!==null,'missing '+k);}
  const row=e.collection.features[0].data;
  if(kind==='cells'){
   assert.equal(row.accepted_origin_mismatch_pixel_equivalents,0);assert.equal(row.diagnostic_interval,+(row.t0===2020));
   assert.ok(Math.abs(row.entry_ha-row.first_observed_entry_ha-row.observed_reentry_ha-row.prior_history_uncertain_ha)<1e-12);
   if(row.t0===1985){assert.equal(row.entry_ha,0);assert.equal(row.unresolved_ha,0);assert.equal(row.initial_ha,row.flow_pas_tmp_ha);}
  }else if(kind==='audit'){for(const k of S.error_fields)assert.equal(row[k],0,k);assert.equal(row.years_checked,41);}
  else{assert.deepEqual(JSON.parse(row.config_json),S.runtime_config);assert.equal(Object.keys(JSON.parse(row.native_projections_json)).length,41);assert.equal(row.expected_rows,199112);assert.equal(row.runtime_grid_cells.value,8);}
 }
 const names=new Set(exports.map(x=>x.fileNamePrefix));
 for(const [a,b] of C.intervals)for(const batch of C.expected_batches)assert.ok(names.has(`canonical_entry_reentry_${a}_${b}_b${String(batch).padStart(2,'0')}_v1`));
 assert.ok(messages.some(x=>String(x[0]).includes('73 tarefas criadas')));
}
assert.ok(!source.includes('.getInfo('));assert.ok(!source.includes('K.PASTURE_AGE_ASSET'));
for(const name of ['first_entry_maximum_age_240','reentry_2025','entry_2024_exit_2025','prior_pas_gap_reset_reentry'])run(fixtures.find(x=>x.case_id===name));
run(fixtures[0],'error');run(fixtures[0],'invalid');
console.log(JSON.stringify({status:'PASS',assurance:'local_eager_adapter_only',successful_scenarios:4,metadata_rejections:2,asynchronous_metadata_calls_per_run:1,exports_before_metadata:0,exports_before_first_UI_yield:1,deferred_callbacks_per_success:72,unique_export_tasks:73,cell_files:64,history_files:8,manifest_files:1,native_execution_performed:false},null,2));

/* Local scalar tests only: these do not execute Earth Engine or reducers. */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const config=JSON.parse(fs.readFileSync(path.join(root,'config/entry_reentry_v1.json')));
const cases=JSON.parse(fs.readFileSync(path.join(root,'config/entry_reentry_native_cases_v1.json')));
const script=fs.readFileSync(path.join(root,'gee/20a_export_entry_reentry_pilot_v1.js'),'utf8');
const ref=script.split('// BEGIN_ACCEPTED_REFERENCE_ENGINE\n')[1].split('// END_ACCEPTED_REFERENCE_ENGINE')[0];
const historical=fs.readFileSync(path.join(root,'docs/history/entry_reentry_browser_freeze_r1/gee/18c_accepted_window_engine_reference_v1.js'),'utf8')
  .split('// BEGIN_RECONSTRUCTION_ENGINE\n')[1].split('// END_RECONSTRUCTION_ENGINE')[0];
assert.equal(ref,historical,'accepted categorical engine must remain byte-identical');
class Image {
  constructor(v,masked=false){this.v=v;this.masked=masked;}
  op(x,fn){x=x instanceof Image?x:new Image(x);return new Image(fn(this.v,x.v),this.masked||x.masked);}
  add(x){return this.op(x,(a,b)=>a+b);} multiply(x){return this.op(x,(a,b)=>a*b);}
  eq(x){return this.op(x,(a,b)=>+(a===b));} neq(x){return this.op(x,(a,b)=>+(a!==b));}
  lt(x){return this.op(x,(a,b)=>+(a<b));} lte(x){return this.op(x,(a,b)=>+(a<=b));}
  gt(x){return this.op(x,(a,b)=>+(a>b));} gte(x){return this.op(x,(a,b)=>+(a>=b));}
  and(x){return this.op(x,(a,b)=>+(!!a&&!!b));} or(x){return this.op(x,(a,b)=>+(!!a||!!b));}
  not(){return new Image(+!this.v,this.masked);}
  where(test,value){value=value instanceof Image?value:new Image(value);
    return !this.masked && !test.masked && test.v && !value.masked?new Image(value.v):new Image(this.v,this.masked);}
  unmask(value,same=true){assert.equal(same,true);return this.masked?new Image(value):this;}
  toInt16(){return this;} toDouble(){return this;} byte(){return this;}
}
const ctx=vm.createContext({ee:{Image:{constant:v=>new Image(v)}},SOURCE_CODES:config.valid_source_codes,MISSING:-9999,START:1985});
vm.runInContext(ref+'\n'+script.split('// BEGIN_ENTRY_REENTRY_ENGINE\n')[1].split('// END_ENTRY_REENTRY_ENGINE')[0],ctx);
function category(value,masked){return masked||value===27||!config.valid_source_codes.includes(value)?'U':value===15?'P':'N';}
// Independent whole-history oracle: scan backwards to the contiguous run, then inspect its strict prefix.
function oracle(history) {
 const obs=history.map(x=>category(x.value,x.masked)),last=obs.length-1;
 let state,age=0,kind=0,entry=0,count=0;
 for(let j=1;j<obs.length;j++) if(obs[j]==='P' && obs[j-1]==='N') count++;
 if(obs[last]==='N') state=0;
 else if(obs[last]==='U') state=4;
 else {
  let first=last;while(first>0 && obs[first-1]==='P') first--;
  if(first===0){state=1;age=100;}
  else if(obs[first-1]==='N'){
   state=2;age=200+obs.length-first;entry=1985+first;
   const prefix=obs.slice(0,first);
   kind=prefix.includes('P')?2:prefix.includes('U')?3:1;
  } else state=3;
 }
 return {state,age,kind,entryYear:entry,count};
}
let fixtureSteps=0;
for(const c of cases){
 let p=ctx.emptyEntryState(),history=[];
 c.values.forEach((value,j)=>{
  history.push({value,masked:c.masked[j]});p=ctx.advanceEntry(p,new Image(value,c.masked[j]),c.start_year+j,j===0);
  const expected={state:c.expected_state[j],age:c.expected_age[j],kind:c.expected_entry_kind[j],count:c.expected_confirmed_entry_count[j],entryYear:c.expected_entry_year[j]};
  assert.deepEqual(oracle(history),expected,c.case_id+'/manual oracle/'+j);
  for(const [k,v] of Object.entries(expected)) assert.equal(p[k].v,v,c.case_id+'/'+j+'/'+k);
  assert.equal(+(p.entryYear.v>=2024),c.expected_boundary_adjacent[j],c.case_id+'/boundary');
  for(const [k,v] of Object.entries(p.errors)) assert.equal(v.v,0,c.case_id+'/'+k);
  fixtureSteps++;
 });
 const final=ctx.reconstruct(1985,1985+c.values.length-1,y=>new Image(c.values[y-1985],c.masked[y-1985]),null);
 assert.equal(p.state.v,final.state.v,'accepted engine fixture/'+c.case_id);
}
const alphabet=[{value:15,masked:false},{value:3,masked:false},{value:27,masked:false},
 {value:999,masked:false},{value:15,masked:true},{value:1,masked:false}];
let histories=0,steps=0;
function enumerate(history,p,depth){
 if(depth===6){histories++;return;}
 for(const symbol of alphabet){
  const h=history.concat([symbol]);const q=ctx.advanceEntry(p,new Image(symbol.value,symbol.masked),1985+depth,depth===0);
  const expected=oracle(h);
  for(const [k,v] of Object.entries(expected)) assert.equal(q[k].v,v,JSON.stringify(h)+'/'+k);
  for(const [k,v] of Object.entries(q.errors)) assert.equal(v.v,0,k);
  if(depth===5){const control=ctx.reconstruct(1985,1990,y=>new Image(h[y-1985].value,h[y-1985].masked),null);assert.equal(q.state.v,control.state.v);}
  steps++;enumerate(h,q,depth+1);
 }
}
enumerate([],ctx.emptyEntryState(),0);
const embedded=JSON.parse(script.match(/var FIXTURES=(\[[\s\S]*?\]);\nvar FOLDER/)[1]);
assert.deepEqual(embedded,cases,'GEE must embed exact supplied native expectations');
console.log(JSON.stringify({status:'PASS',assurance:'local_scalar_only',manual_fixture_cases:cases.length,manual_fixture_steps:fixtureSteps,exhaustive_length6_histories:histories,exhaustive_prefix_steps:steps,accepted_engine_byte_identity:true,native_execution_performed:false},null,2));

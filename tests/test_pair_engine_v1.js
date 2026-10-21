/* Software-only scalar adapter of the exact supplied engine, not a GEE run. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const config=JSON.parse(fs.readFileSync(path.join(root,'config/uncertain_pair_crosstab_v1.json')));
function engine(scope){
  const text=fs.readFileSync(path.join(root,'gee',config.gee_scripts[scope].filename),'utf8');
  return text.split('// BEGIN_PAIR_CLASSIFICATION_ENGINE')[1].split('// END_PAIR_CLASSIFICATION_ENGINE')[0];
}
assert.equal(engine('pilot'),engine('full'));
class Scalar {
  constructor(value,masked=false){this.v=value;this.masked=masked;}
  op(other,fn){other=other instanceof Scalar?other:new Scalar(other);
    return new Scalar(fn(this.v,other.v),this.masked||other.masked);}
  multiply(x){return this.op(x,(a,b)=>a*b);} add(x){return this.op(x,(a,b)=>a+b);}
  eq(x){return this.op(x,(a,b)=>+(a===b));} neq(x){return this.op(x,(a,b)=>+(a!==b));}
  lt(x){return this.op(x,(a,b)=>+(a<b));} gt(x){return this.op(x,(a,b)=>+(a>b));}
  and(x){return this.op(x,(a,b)=>+(!!a&&!!b));} or(x){return this.op(x,(a,b)=>+(!!a||!!b));}
  not(){return new Scalar(+!this.v,this.masked);}
  mask(){return new Scalar(this.masked?0:1);}
  unmask(value,sameFootprint){assert.equal(sameFootprint,true);return this.masked?new Scalar(value):this;}
  toInt16(){return this;} byte(){return this;}
  where(test,value){return !this.masked&&!test.masked&&test.v?new Scalar(value):this;}
}
const context=vm.createContext({SOURCE_CODES:config.valid_source_codes,MISSING:-9999});
vm.runInContext(engine('pilot'),context);
function expected(value,masked){return masked?3:value===15?0:value===27?2:
  config.valid_source_codes.includes(value)?1:4;}
let pairs=0;
const values=[...config.valid_source_codes,0,-9999,999];
for(const a of values) for(const b of values) for(const ma of [false,true]) for(const mb of [false,true]) {
  const x=expected(a,ma),y=expected(b,mb),r=context.classifyPair(new Scalar(a,ma),new Scalar(b,mb));
  const uncertain=+(x>=2||y>=2);
  for(const field of ['previous','current','domain','valid','uncertain','entry','termination',
      'partition_error','legacy_uncertain_error','conditional_partition_error']) assert.equal(r[field].masked,false);
  assert.equal(r.previous.v,x);assert.equal(r.current.v,y);
  r.cells.forEach((cell,k)=>assert.equal(cell.v,+(k===x*5+y)));
  assert.equal(r.domain.v,1);assert.equal(r.valid.v,1-uncertain);assert.equal(r.uncertain.v,uncertain);
  assert.equal(r.entry.v,+(x===1&&y===0));assert.equal(r.termination.v,+(x===0&&y===1));
  assert.equal(r.uncertain_previous_PAS.v,+(uncertain&&x===0));
  assert.equal(r.uncertain_current_PAS.v,+(uncertain&&y===0));
  assert.equal(r.uncertain_no_observed_PAS.v,+(uncertain&&x!==0&&y!==0));
  for(const field of ['partition_error','legacy_uncertain_error','conditional_partition_error']) assert.equal(r[field].v,0);
  pairs++;
}
const fixtures=JSON.parse(fs.readFileSync(path.join(root,'config/uncertain_pair_native_cases_v1.json')));
fixtures.forEach(f=>{
  assert.equal(expected(f.previous_value,f.previous_masked),f.expected_previous);
  assert.equal(expected(f.current_value,f.current_masked),f.expected_current);
});
console.log(JSON.stringify({status:'PASS',assurance:'software_scalar_only',exhaustive_pairs:pairs,
  fixture_definitions:fixtures.length,native_execution:'PENDING'}));

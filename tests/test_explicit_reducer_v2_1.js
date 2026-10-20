/* Structural reducer-model check; not an Earth Engine execution. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'gee/recheck_pasture_v2_82cells_v2_1.js'),'utf8');
const temporal=require(path.join(root,'gee/recheck_pasture_v2_82cells_v2_1.js'));
console.log(temporal.runSelfTests());console.log(temporal.addedCoverageTests());
class ReducerModel {
  constructor(names){this.names=names;this.inputs=names.length;}
  setOutputs(names){assert.equal(names.length,this.inputs);assert.equal(new Set(names).size,names.length);return new ReducerModel([...names]);}
  combine({reducer2,sharedInputs}){assert.equal(sharedInputs,false);return new ReducerModel([...this.names,...reducer2.names]);}
  evaluate(pixels){return Object.fromEntries(this.names.map((k,i)=>[k,Math.max(...pixels.map(p=>p[i]))]));}
}
const code=source.slice(source.indexOf('  function namedMaxReducer('),source.indexOf('  var image=ee.Image.cat(bands);'));
const context=vm.createContext({ee:{Reducer:{max:()=>new ReducerModel(['max'])}}});
vm.runInContext(code,context);
const fields=Array.from({length:26},(_,i)=>'field_'+i);
const r=context.namedMaxReducer(fields);
assert.equal(r.inputs,26);assert.deepEqual(r.names,fields);
const pixels=[fields.map((_,i)=>i%2===0?i+1:0),fields.map((_,i)=>i%2===1?i+1:0)];
assert.deepEqual(r.evaluate(pixels),Object.fromEntries(fields.map((k,i)=>[k,i+1])));
assert.ok(source.includes("data=data.set(k,ee.Algorithms.If(ee.Algorithms.IsEqual(f.get(k),null),-9999,f.get(k)))"));
assert.ok(source.includes('ee.String.encodeJSON(f.toDictionary())'));
assert.ok(!source.includes('ee.Reducer.max(26)'));
console.log(JSON.stringify({status:'PASS',independent_inputs:26,outputs:26,assurance:'software_model_only',native:'PENDING'}));

assert.ok(!source.includes('pixelCoordinates('));
assert.ok(source.includes('left_min:0,left_max:1,right_min:0,right_max:1'));
assert.ok(source.includes('return ee.Feature(reducedFixture.first()).toDictionary().getInfo()'));

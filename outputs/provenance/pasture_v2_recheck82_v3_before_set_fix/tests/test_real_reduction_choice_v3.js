/* Software-only checks of observed-path selection; no native execution claim. */
const assert=require('node:assert/strict'),path=require('node:path'),fs=require('node:fs');
const source=fs.readFileSync(path.join(__dirname,'../gee/recheck_pasture_v2_82cells_v3.js'),'utf8');
const a=require(path.join(__dirname,'../gee/recheck_pasture_v2_82cells_v3.js'));
console.log(a.runSelfTests());console.log(a.addedCoverageTests());
const fields=['new_code1','legacy_coverage_unknown_present','native_grid_support'];
const good={new_code1:0,legacy_coverage_unknown_present:1,native_grid_support:1};
const nulls={new_code1:null,legacy_coverage_unknown_present:null,native_grid_support:null};
assert.equal(a.chooseRealReduction(good,good,fields).strategy,'mapped_direct_reduceRegion_finite_image');
assert.equal(a.chooseRealReduction(good,nulls,fields).strategy,'mapped_direct_reduceRegion_finite_image');
assert.equal(a.chooseRealReduction({},good,fields).strategy,'materialized_table_finite_image');
assert.throws(()=>a.chooseRealReduction(nulls,nulls,fields),/Nenhuma redução válida/);
assert.throws(()=>a.chooseRealReduction(good,{...good,new_code1:1},fields),/divergem/);
assert.ok(source.includes('cells.limit(82).toList(82)'));
assert.ok(source.includes('finiteWindow=cells.geometry(1).bounds(1).buffer(1000,1).bounds(1)'));
assert.ok(source.includes('var finiteImage=image.clip(finiteWindow)'));
assert.ok(source.includes('return f.setMulti(values)'));
assert.ok(!source.includes('toList(21869)'));
console.log(JSON.stringify({status:'PASS',selection_scenarios:5,assurance:'software_only',native:'PENDING'}));

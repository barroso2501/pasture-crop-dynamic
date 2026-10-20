/* Rechecagem v2.1: duas metades explícitas, teste nativo e controle de campos ausentes. uma tarefa CSV, 41 anos, somente idade nova.
 * Não execute novamente os oito lotes anteriores.
 */
var RECHECK = {"version":"pasture-v2-coverage-recheck-v2.1","parent_run":"20261016150312","cells":[{"audit_id":"00000000000000000661","cell_id":"6679","GRID_ID":"HS-189"},{"audit_id":"00000000000000000a0b","cell_id":"8111","GRID_ID":"IH-179"},{"audit_id":"00000000000000000c50","cell_id":"8975","GRID_ID":"IK-173"},{"audit_id":"00000000000000000d6d","cell_id":"9395","GRID_ID":"HS-170"},{"audit_id":"00000000000000000ded","cell_id":"9570","GRID_ID":"IR-169"},{"audit_id":"0000000000000000141e","cell_id":"11808","GRID_ID":"JE-155"},{"audit_id":"0000000000000000169c","cell_id":"12657","GRID_ID":"JE-150"},{"audit_id":"0000000000000000179c","cell_id":"12999","GRID_ID":"JE-148"},{"audit_id":"00000000000000001f60","cell_id":"15818","GRID_ID":"IN-133"},{"audit_id":"00000000000000002981","cell_id":"20182","GRID_ID":"CT-115"},{"audit_id":"00000000000000002c25","cell_id":"21217","GRID_ID":"HN-112"},{"audit_id":"00000000000000002e1f","cell_id":"22053","GRID_ID":"DH-109"},{"audit_id":"000000000000000046cd","cell_id":"34851","GRID_ID":"JR-67"},{"audit_id":"000000000000000003df","cell_id":"5670","GRID_ID":"GJ-196"},{"audit_id":"00000000000000000648","cell_id":"6654","GRID_ID":"GT-189"},{"audit_id":"00000000000000000bef","cell_id":"8833","GRID_ID":"IM-174"},{"audit_id":"00000000000000000c4f","cell_id":"8974","GRID_ID":"IJ-173"},{"audit_id":"00000000000000000cb3","cell_id":"9120","GRID_ID":"IK-172"},{"audit_id":"00000000000000000d06","cell_id":"9249","GRID_ID":"HT-171"},{"audit_id":"000000000000000013a0","cell_id":"11641","GRID_ID":"JF-156"},{"audit_id":"0000000000000000149c","cell_id":"11977","GRID_ID":"JF-154"},{"audit_id":"0000000000000000189f","cell_id":"13343","GRID_ID":"JG-146"},{"audit_id":"00000000000000001f61","cell_id":"15819","GRID_ID":"IO-133"},{"audit_id":"00000000000000002a38","cell_id":"20476","GRID_ID":"CS-114"},{"audit_id":"000000000000000003af","cell_id":"5582","GRID_ID":"ID-197"},{"audit_id":"0000000000000000067a","cell_id":"6704","GRID_ID":"IR-189"},{"audit_id":"00000000000000001197","cell_id":"10956","GRID_ID":"IP-160"},{"audit_id":"00000000000000002a39","cell_id":"20477","GRID_ID":"CT-114"},{"audit_id":"00000000000000002c26","cell_id":"21218","GRID_ID":"HO-112"},{"audit_id":"00000000000000004106","cell_id":"32214","GRID_ID":"JY-77"},{"audit_id":"000000000000000003f6","cell_id":"5716","GRID_ID":"ID-196"},{"audit_id":"0000000000000000043e","cell_id":"5852","GRID_ID":"ID-195"},{"audit_id":"0000000000000000053b","cell_id":"6264","GRID_ID":"IA-192"},{"audit_id":"0000000000000000099f","cell_id":"7953","GRID_ID":"HT-180"},{"audit_id":"00000000000000000c51","cell_id":"8976","GRID_ID":"IL-173"},{"audit_id":"00000000000000000d07","cell_id":"9250","GRID_ID":"HU-171"},{"audit_id":"00000000000000000d6c","cell_id":"9394","GRID_ID":"HR-170"},{"audit_id":"00000000000000001113","cell_id":"10780","GRID_ID":"ID-161"},{"audit_id":"0000000000000000139e","cell_id":"11628","GRID_ID":"IS-156"},{"audit_id":"0000000000000000179d","cell_id":"13000","GRID_ID":"JF-148"},{"audit_id":"0000000000000000275b","cell_id":"19204","GRID_ID":"IN-119"},{"audit_id":"00000000000000004622","cell_id":"34616","GRID_ID":"JX-68"},{"audit_id":"0000000000000000483a","cell_id":"35324","GRID_ID":"JQ-65"},{"audit_id":"000000000000000004e1","cell_id":"6128","GRID_ID":"ID-193"},{"audit_id":"0000000000000000051e","cell_id":"6233","GRID_ID":"GV-192"},{"audit_id":"000000000000000005f7","cell_id":"6538","GRID_ID":"HS-190"},{"audit_id":"00000000000000000679","cell_id":"6703","GRID_ID":"IQ-189"},{"audit_id":"00000000000000000b2b","cell_id":"8545","GRID_ID":"IL-176"},{"audit_id":"00000000000000000b8e","cell_id":"8689","GRID_ID":"IM-175"},{"audit_id":"00000000000000000d6f","cell_id":"9397","GRID_ID":"HU-170"},{"audit_id":"0000000000000000118b","cell_id":"10944","GRID_ID":"ID-160"},{"audit_id":"0000000000000000118c","cell_id":"10945","GRID_ID":"IE-160"},{"audit_id":"0000000000000000151c","cell_id":"12146","GRID_ID":"JF-153"},{"audit_id":"0000000000000000171c","cell_id":"12828","GRID_ID":"JE-149"},{"audit_id":"0000000000000000099e","cell_id":"7952","GRID_ID":"HS-180"},{"audit_id":"000000000000000009ad","cell_id":"7967","GRID_ID":"IH-180"},{"audit_id":"00000000000000000d04","cell_id":"9247","GRID_ID":"HR-171"},{"audit_id":"00000000000000000d0a","cell_id":"9253","GRID_ID":"HX-171"},{"audit_id":"0000000000000000159d","cell_id":"12316","GRID_ID":"JE-152"},{"audit_id":"0000000000000000159e","cell_id":"12317","GRID_ID":"JF-152"},{"audit_id":"0000000000000000161e","cell_id":"12489","GRID_ID":"JF-151"},{"audit_id":"0000000000000000169e","cell_id":"12659","GRID_ID":"JG-150"},{"audit_id":"0000000000000000171d","cell_id":"12829","GRID_ID":"JF-149"},{"audit_id":"00000000000000002801","cell_id":"19480","GRID_ID":"IO-118"},{"audit_id":"0000000000000000478a","cell_id":"35089","GRID_ID":"JQ-66"},{"audit_id":"000000000000000002b2","cell_id":"5045","GRID_ID":"IC-201"},{"audit_id":"00000000000000000894","cell_id":"7526","GRID_ID":"HV-183"},{"audit_id":"00000000000000000a0a","cell_id":"8110","GRID_ID":"IG-179"},{"audit_id":"00000000000000000b8c","cell_id":"8687","GRID_ID":"IK-175"},{"audit_id":"00000000000000000f1a","cell_id":"10029","GRID_ID":"IU-166"},{"audit_id":"0000000000000000151b","cell_id":"12145","GRID_ID":"JE-153"},{"audit_id":"0000000000000000161f","cell_id":"12490","GRID_ID":"JG-151"},{"audit_id":"0000000000000000181e","cell_id":"13172","GRID_ID":"JG-147"},{"audit_id":"00000000000000001cb5","cell_id":"14802","GRID_ID":"IV-138"},{"audit_id":"0000000000000000346d","cell_id":"25404","GRID_ID":"IQ-99"},{"audit_id":"00000000000000004789","cell_id":"35088","GRID_ID":"JP-66"},{"audit_id":"00000000000000000716","cell_id":"6941","GRID_ID":"HA-187"},{"audit_id":"0000000000000000141f","cell_id":"11809","GRID_ID":"JF-155"},{"audit_id":"0000000000000000169d","cell_id":"12658","GRID_ID":"JF-150"},{"audit_id":"00000000000000001cb4","cell_id":"14801","GRID_ID":"IU-138"},{"audit_id":"00000000000000002edc","cell_id":"22371","GRID_ID":"DI-108"},{"audit_id":"000000000000000033eb","cell_id":"25079","GRID_ID":"IQ-100"}],"expected_cells":82,"known_coverage_codes":[1,3,4,5,6,7,9,10,11,12,13,15,19,20,21,22,23,24,25,26,29,30,31,32,33,35,36,39,40,41,46,47,48,49,50,62,75,84,91],"previous_known_coverage_codes":[3,4,5,6,7,9,11,12,13,15,19,20,21,23,24,25,29,30,31,32,33,35,36,39,40,41,46,47,48,49,50,62],"newly_recognized_codes":[1,10,22,26,75,84,91],"coverage":"projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3","age":"projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_origin_age_v2","grid":"projects/ee-barroso2501/assets/grade_hex_CeAmz_selecao","crs":"EPSG:4326","crs_transform":[0.00026949458523585647,0,-74.02073025380652,0,-0.00026949458523585647,5.405791885246045],"parent_zip_sha256":"6f6cfe4b026879f72899d82787827249d1a33f652e1e16dea4f86e43f061efd9","parent_validation_sha256":"f874225b3dcda43959b154f4699bf49e9463a7f77c953bde825dc8022b5224df","required_transport_controls":["native_schema_test_status","native_schema_test_fields","native_schema_expected_json","image_band_names_json","reducer_missing_count","reducer_missing_fields","reducer_properties_json","reducer_property_names_json","native_fixture_method","native_constant_test_status","native_partition_test_json","native_fixture_region_json"],"native_grid_support_required":1};
var CFG={start:1985,end:2025};
// Classes conhecidas da cobertura; 0, 27 e máscara NÃO provam não-pastagem.
// Classes não listadas são explicitamente exportadas como desconhecidas.
var KNOWN = [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32, 33, 35, 36, 39, 40, 41, 46, 47, 48, 49, 50, 62, 75, 84, 91];
var FLAGS = [
  'code1', 'invalid100_after_nonpas', 'reused100_after_exit',
  'code100_without_confirmed_initial', 'code100_after_gap_only',
  'age100_outside_pas', 'age_positive_outside_pas',
  'pasture_age_masked', 'pasture_age_zero', 'unexpected_age_code',
  'coverage_unknown_code', 'has_pasture', 'has_code100', 'has_2xx',
  'has_valid_coverage'
];

// Lógica compartilhada pelo processamento raster e pelo autoteste local.
// Entradas: imagens de uma banda ou objetos escalares com a mesma álgebra.
function temporalAudit(coverRows, ageRows, zero) {
  var out = {};
  FLAGS.forEach(function(k) { out[k] = zero; });
  var seenNonPas = zero;
  var seen100 = zero;
  var brokenAfter100 = zero;
  var seenGap = zero;
  var continuousInitial = null;
  coverRows.forEach(function(c, i) {
    var a = ageRows[i];
    var pas = c.valid.and(c.value.eq(15));
    var nonpas = c.valid.and(c.value.neq(15));
    var gap = c.valid.not();
    var is100 = a.valid.and(a.value.eq(100));
    var is1 = a.valid.and(a.value.eq(1));
    var positive = a.valid.and(a.value.gt(0));
    var maxCode = 200 + i; // 1986 -> 201, ..., 2025 -> 240.
    var code2xx = a.value.gte(201).and(a.value.lte(maxCode));
    if (i === 0) { continuousInitial = pas; }
    else { continuousInitial = continuousInitial.and(pas); }
    function flag(k, condition) { out[k] = out[k].or(condition); }
    flag('code1', is1);
    // Testa qualquer não-PAS observado anteriormente, não só o ano t-1.
    flag('invalid100_after_nonpas', is100.and(pas).and(seenNonPas));
    // Subconjunto exato: já houve 100, depois não-PAS e agora voltou a 100.
    flag('reused100_after_exit', is100.and(pas).and(brokenAfter100));
    flag('code100_without_confirmed_initial', is100.and(pas).and(continuousInitial.not()));
    flag('code100_after_gap_only', is100.and(pas).and(seenGap).and(seenNonPas.not()));
    flag('age100_outside_pas', is100.and(nonpas));
    flag('age_positive_outside_pas', positive.and(nonpas));
    flag('pasture_age_masked', pas.and(a.valid.not()));
    flag('pasture_age_zero', pas.and(a.valid).and(a.value.eq(0)));
    flag('unexpected_age_code', a.valid.and(a.value.neq(0))
      .and(is100.or(code2xx).not()));
    flag('coverage_unknown_code', c.unknown);
    flag('has_pasture', pas);
    flag('has_code100', is100);
    flag('has_2xx', a.valid.and(code2xx));
    flag('has_valid_coverage', c.valid);
    // Atualizações ocorrem DEPOIS de avaliar o estado do ano corrente.
    brokenAfter100 = brokenAfter100.or(nonpas.and(seen100));
    seen100 = seen100.or(is100.and(pas));
    seenNonPas = seenNonPas.or(nonpas);
    seenGap = seenGap.or(gap);
  });
  return out;
}

// Autoteste da MESMA função temporalAudit, sem acesso a rasters.
function scalar(x) {
  return {
    v: Number(x),
    eq: function(y) { return scalar(this.v === Number(y)); },
    neq: function(y) { return scalar(this.v !== Number(y)); },
    gt: function(y) { return scalar(this.v > Number(y)); },
    gte: function(y) { return scalar(this.v >= Number(y)); },
    lte: function(y) { return scalar(this.v <= Number(y)); },
    and: function(y) { return scalar(Boolean(this.v && y.v)); },
    or: function(y) { return scalar(Boolean(this.v || y.v)); },
    not: function() { return scalar(!this.v); }
  };
}
function syntheticAudit(c, a) {
  return temporalAudit(c.map(function(v) {
    var valid = KNOWN.indexOf(v) !== -1;
    return {value: scalar(v === null ? -9999 : v), valid: scalar(valid),
      unknown: scalar(v !== null && v !== 0 && v !== 27 && !valid)};
  }), a.map(function(v) {
    return {value: scalar(v === null ? -9999 : v), valid: scalar(v !== null)};
  }), scalar(0));
}
function runSelfTests() {
  var cases = [
    [[15,15,15],[100,100,100],{code1:0,invalid100_after_nonpas:0,reused100_after_exit:0,code100_without_confirmed_initial:0}],
    [[15,3,15],[100,null,100],{invalid100_after_nonpas:1,reused100_after_exit:1}],
    [[15,3,15,15],[100,null,201,202],{invalid100_after_nonpas:0,reused100_after_exit:0,unexpected_age_code:0}],
    [[3,15],[null,100],{invalid100_after_nonpas:1,reused100_after_exit:0}],
    [[15,15,15],[1,1,1],{code1:1}],
    [[15,null,15],[100,null,100],{invalid100_after_nonpas:0,reused100_after_exit:0,code100_after_gap_only:1}],
    [[15,27,15],[100,null,100],{invalid100_after_nonpas:0,code100_after_gap_only:1}],
    [[null,15],[null,100],{invalid100_after_nonpas:0,code100_after_gap_only:1}],
    [[15,3,27,15],[100,null,null,100],{invalid100_after_nonpas:1,reused100_after_exit:1,code100_after_gap_only:0}],
    [[15],[null],{pasture_age_masked:1,has_pasture:1}],
    [[15],[0],{pasture_age_zero:1}],
    [[3],[100],{age100_outside_pas:1}],
    [[3,15],[null,240],{unexpected_age_code:1}],
    [[15,99,15],[100,null,100],{coverage_unknown_code:1,invalid100_after_nonpas:0,code100_after_gap_only:1}]
  ];
  cases.forEach(function(t, i) {
    var got = syntheticAudit(t[0], t[1]);
    Object.keys(t[2]).forEach(function(k) {
      if (got[k].v !== t[2][k]) { throw new Error('Autoteste ' + i + ': ' + k); }
    });
  });
  return cases.length + ' casos sintéticos: PASS';
}

function selectAnnual(info, prefix) {
  var names = info.bands.map(function(b) { return b.id; });
  var selected = [];
  for (var y = CFG.start; y <= CFG.end; y++) {
    var matches = names.filter(function(n) {
      return prefix ? n === prefix + y : new RegExp('(^|_)' + y + '$').test(n);
    });
    if (matches.length !== 1) {
      throw new Error('Ano ' + y + ': bandas candidatas ' + JSON.stringify(matches) +
        '. Ajuste o prefixo em CFG. Bandas: ' + names.join(', '));
    }
    selected.push(matches[0]);
  }
  return selected;
}
function assertGrid(info, bands, ref) {
  bands.forEach(function(name) {
    var b = info.bands.filter(function(x) { return x.id === name; })[0];
    var t = b.crs_transform;
    var r = ref.crs_transform;
    if (!t || !r || b.crs !== ref.crs || t[1] !== 0 || t[3] !== 0 ||
        r[1] !== 0 || r[3] !== 0 || Math.abs(t[0]-r[0]) > 1e-12 ||
        Math.abs(t[4]-r[4]) > 1e-12) {
      throw new Error('Grade incompatível: ' + name + '. Não reamostrar automaticamente.');
    }
    var col = (t[2]-r[2])/r[0];
    var row = (t[5]-r[5])/r[4];
    if (Math.abs(col-Math.round(col)) > 1e-5 || Math.abs(row-Math.round(row)) > 1e-5) {
      throw new Error('Origem fora da malha nativa: ' + name);
    }
  });
}

function addedCoverageTests() {
  var cases=[
    [[15,26,15],[100,null,100],{invalid100_after_nonpas:1,reused100_after_exit:1,coverage_unknown_code:0}],
    [[1],[100],{age100_outside_pas:1,coverage_unknown_code:0}],
    [[15,27,15],[100,null,100],{invalid100_after_nonpas:0,code100_after_gap_only:1}]
  ];
  cases.forEach(function(test){
    var got=syntheticAudit(test[0],test[1]);
    Object.keys(test[2]).forEach(function(k){
      if (got[k].v!==test[2][k]) throw new Error('Regressão de classes: '+k);
    });
  });
  return '3 casos adicionais: PASS';
}

function main() {
  print('AUTOTESTES LOCAIS',runSelfTests(),addedCoverageTests());
  var coverage=ee.Image(RECHECK.coverage),age=ee.Image(RECHECK.age);
  var ci=coverage.getInfo(),ai=age.getInfo();
  var cb=selectAnnual(ci,''),ab=selectAnnual(ai,'');
  var ref=ci.bands.filter(function(b){return b.id===cb[0];})[0];
  if (ref.crs!==RECHECK.crs || ref.crs_transform.length!==6 ||
      ref.crs_transform.some(function(v,i){return Math.abs(v-RECHECK.crs_transform[i])>1e-13;})) {
    throw new Error('Projeção da cobertura diverge da execução aceita.');
  }
  assertGrid(ci,cb,ref);assertGrid(ai,ab,ref);
  var proj=coverage.select(cb[0]).projection();
  var zero=ee.Image.constant(0).rename('b').setDefaultProjection(proj).toByte();
  var previousKnown=RECHECK.previous_known_coverage_codes;
  function unpack(image,name,isCoverage) {
    var raw=image.select(name).rename('b');
    var present=raw.mask().unmask(0,false).gt(0);
    var value=raw.toInt16().unmask(-9999,false);
    if (!isCoverage) return {value:value,valid:present};
    var known=value.remap(KNOWN,KNOWN.map(function(){return 1;}),0).eq(1);
    var previous=value.remap(previousKnown,previousKnown.map(function(){return 1;}),0).eq(1);
    return {value:value,present:present,valid:present.and(known),
      unknown:present.and(value.neq(0)).and(value.neq(27)).and(known.not()),
      previousUnknown:present.and(value.neq(0)).and(value.neq(27)).and(previous.not())};
  }
  var cs=cb.map(function(n){return unpack(coverage,n,true);});
  var ages=ab.map(function(n){return unpack(age,n,false);});
  var flags=temporalAudit(cs,ages,zero);
  var bands=FLAGS.map(function(k){return ee.Image(flags[k]).rename('new_'+k).toByte();});
  var legacy=zero;
  cs.forEach(function(c){legacy=legacy.or(c.previousUnknown);});
  bands.push(legacy.rename('legacy_coverage_unknown_present').toByte());
  var diagnostics=['legacy_coverage_unknown_present'];
  RECHECK.newly_recognized_codes.forEach(function(code){
    var found=zero;
    cs.forEach(function(c){found=found.or(c.present.and(c.value.eq(code)));});
    var name='coverage_code_'+code+'_present';
    bands.push(found.rename(name).toByte());diagnostics.push(name);
  });
  // Two extra extrema identify the range if any truly unknown code remains.
  // Sentinels are explicit: they are never interpreted as real source codes.
  var unknownMax=zero.toInt32().add(-1000000000);
  var unknownNegativeMin=unknownMax;
  cs.forEach(function(c){
    var empty=zero.toInt32().add(-1000000000);
    unknownMax=unknownMax.max(empty.where(c.unknown,c.value));
    unknownNegativeMin=unknownNegativeMin.max(empty.where(c.unknown,c.value.multiply(-1)));
  });
  bands.push(unknownMax.rename('remaining_unknown_max_code'));
  bands.push(unknownNegativeMin.rename('remaining_unknown_negative_min_code'));
  diagnostics=diagnostics.concat(['remaining_unknown_max_code','remaining_unknown_negative_min_code']);
  var ids=RECHECK.cells.map(function(c){return c.audit_id;});
  var cells=ee.FeatureCollection(RECHECK.grid).filter(ee.Filter.inList('system:index',ids));
  if (cells.size().getInfo()!==82) throw new Error('A seleção não contém exatamente 82 células.');
  cells=cells.map(function(f){return f.set('audit_id',ee.String(f.get('system:index')));});
  var today=new Date().toISOString(),stamp=today.replace(/[^0-9]/g,'').slice(0,14);
  var meta={script_version:RECHECK.version,parent_run:RECHECK.parent_run,
    parent_validation_sha256:RECHECK.parent_validation_sha256,run_id:stamp,
    generated_at_utc:today,expected_cells:82,year_start:1985,year_end:2025,
    coverage_asset:RECHECK.coverage,new_asset:RECHECK.age,grid_asset:RECHECK.grid,
    known_codes_json:JSON.stringify(KNOWN),prior_known_codes_json:JSON.stringify(previousKnown),
    crs:ref.crs,crs_transform:JSON.stringify(ref.crs_transform),tile_scale:16};
  // Explicit independent inputs/outputs; do not use max(26), which is argmax.
  var resultFields=FLAGS.map(function(k){return 'new_'+k;}).concat(diagnostics);
  resultFields.push('native_grid_support');
  bands.push(zero.add(1).rename('native_grid_support'));
  function namedMaxReducer(names) {
    var reducer=ee.Reducer.max().setOutputs([names[0]]);
    for (var k=1;k<names.length;k++) {
      reducer=reducer.combine({reducer2:ee.Reducer.max().setOutputs([names[k]]),sharedInputs:false});
    }
    return reducer.setOutputs(names);
  }
  var image=ee.Image.cat(bands);
  var actualBandNames=image.bandNames().getInfo();
  if (JSON.stringify(actualBandNames)!==JSON.stringify(resultFields)) {
    throw new Error('Bandas/ordem divergentes: '+JSON.stringify(actualBandNames));
  }
  // Native fixture: explicit halves of a 4x4 window on the exact affine grid.
  // This avoids assuming a coordinate parity pattern is sampled as intended.
  var transform=ref.crs_transform;
  var nativeProjection=ee.Projection(ref.crs,transform);
  var col=Math.floor((-47-transform[2])/transform[0]);
  var row=Math.floor((-16-transform[5])/transform[4]);
  var x0=transform[2]+col*transform[0],x2=x0+2*transform[0],x4=x0+4*transform[0];
  var y0=transform[5]+row*transform[4],y4=y0+4*transform[4];
  var testRegion=ee.Geometry.Rectangle([x0,y4,x4,y0],ref.crs,false);
  var leftRegion=ee.Geometry.Rectangle([x0,y4,x2,y0],ref.crs,false);
  var baseOne=ee.Image.constant(1).rename('fixture').setDefaultProjection(nativeProjection);
  // Zero outside each known synthetic half is part of the fixture definition;
  // no missing observations in the actual audit are imputed to zero.
  var left=baseOne.clip(leftRegion).unmask(0,false).rename('left');
  // Complement within the tested rectangle avoids ambiguous shared-edge pixels.
  var right=left.not().rename('right');
  var partitionTest=left.add(right).rename('covered').addBands(left).addBands(right)
    .reduceRegion({reducer:ee.Reducer.minMax(),geometry:testRegion,crs:ref.crs,
      crsTransform:transform,maxPixels:10000,tileScale:16}).getInfo();
  var expectedPartition={covered_min:1,covered_max:1,left_min:0,left_max:1,right_min:0,right_max:1};
  Object.keys(expectedPartition).forEach(function(k){
    if (!partitionTest || partitionTest[k]!==expectedPartition[k]) {
      throw new Error('A geometria do teste nativo não contém as duas metades: '+JSON.stringify(partitionTest));
    }
  });
  // Exercise EXACTLY reduceRegions, the same API as the 82-cell export.
  var testCollection=ee.FeatureCollection([ee.Feature(testRegion,{fixture_id:'native_4x4'})]);
  function fixtureValues(testBands) {
    var reducedFixture=ee.Image.cat(testBands).reduceRegions({collection:testCollection,
      reducer:namedMaxReducer(resultFields),crs:ref.crs,crsTransform:transform,
      tileScale:16,maxPixelsPerRegion:10000});
    return ee.Feature(reducedFixture.first()).toDictionary().getInfo();
  }
  var expectedSchema={};
  var constantBands=resultFields.map(function(k,i){
    expectedSchema[k]=i+1;return baseOne.multiply(i+1).rename(k);
  });
  var constantsResult=fixtureValues(constantBands);
  resultFields.forEach(function(k){
    if (!constantsResult || constantsResult[k]!==expectedSchema[k]) {
      throw new Error('Mapeamento de saídas constantes falhou: '+JSON.stringify(constantsResult));
    }
  });
  var spatialBands=resultFields.map(function(k,i){
    return (i%2===0?left:right).multiply(i+1).rename(k);
  });
  var testResults=fixtureValues(spatialBands);
  resultFields.forEach(function(k){
    if (!testResults || testResults[k]!==expectedSchema[k]) {
      throw new Error('Máximos independentes falharam em '+k+': '+JSON.stringify(testResults));
    }
  });
  // Keep only the exact 26 tested numeric outputs, not the fixture feature ID.
  var schemaResults={};
  resultFields.forEach(function(k){schemaResults[k]=testResults[k];});
  meta.native_fixture_method='two_explicit_halves_native_4x4_reduceRegions_v1';
  meta.native_constant_test_status='PASS';
  meta.native_partition_test_json=JSON.stringify(partitionTest);
  meta.native_fixture_region_json=JSON.stringify([x0,y4,x4,y0]);
  meta.native_schema_test_status='PASS';
  meta.native_schema_test_fields=resultFields.length;
  meta.native_schema_expected_json=JSON.stringify(schemaResults);
  meta.image_band_names_json=JSON.stringify(actualBandNames);
  var reduced=image.reduceRegions({collection:cells,reducer:namedMaxReducer(resultFields),
    crs:ref.crs,crsTransform:ref.crs_transform,tileScale:16,maxPixelsPerRegion:1000000000});
  var rows=reduced.map(function(f){
    var data=f.toDictionary();
    var missing=ee.List(resultFields).map(function(k){
      return ee.Algorithms.If(ee.Algorithms.IsEqual(f.get(ee.String(k)),null),k,'');
    }).removeAll(['']);
    resultFields.forEach(function(k){
      // Explicit failure sentinel, NEVER a zero imputation for missing values.
      data=data.set(k,ee.Algorithms.If(ee.Algorithms.IsEqual(f.get(k),null),-9999,f.get(k)));
    });
    return ee.Feature(null,data).set(meta)
      .set('reducer_missing_count',missing.size())
      .set('reducer_missing_fields',missing.join('|'))
      .set('reducer_properties_json',ee.String.encodeJSON(f.toDictionary()))
      .set('reducer_property_names_json',ee.String.encodeJSON(f.propertyNames()));
  });
  var name='pasture_v2_coverage_recheck82_'+stamp+'_v2_1';
  Export.table.toDrive({collection:rows,description:name,fileNamePrefix:name,
    folder:'auditoria_pasture_v2_recheck82_v2_1',fileFormat:'CSV',
    selectors:['audit_id','cell_id','GRID_ID'].concat(Object.keys(meta)).concat(resultFields)
      .concat(['reducer_missing_count','reducer_missing_fields','reducer_properties_json','reducer_property_names_json'])});
  print('Teste nativo de 26 saídas: PASS. UMA tarefa nas mesmas 82 células. Devolva o CSV v2_1.');
}

if (typeof module!=='undefined' && module.exports) {
  module.exports={temporalAudit:temporalAudit,syntheticAudit:syntheticAudit,
    runSelfTests:runSelfTests,addedCoverageTests:addedCoverageTests,FLAGS:FLAGS,KNOWN:KNOWN};
} else {main();}


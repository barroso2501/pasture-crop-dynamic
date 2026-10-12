/** Observation-window sensitivity: baseline years 1985, 1995, 2000.
 * Copy this complete file unchanged into the GEE Code Editor.
 * No public pasture-age product is read. Native pixel area/alignment retained.
 * Full implementation computes only 1995-2000 through 2020-2025; the accepted
 * earlier 1985 baseline rows are reused by the Python validator.
 */
var MODE = 'full';
var INTERVAL_INDICES = [2, 3, 4, 5, 6, 7];
var RUN_TAG = 'ws1_20261009';
var SCRIPT_VERSION = 'window-origin-sensitivity-v1';
var SOURCE_SCRIPT = '18c_export_window_origin_sensitivity_full_v1.js';
var K = require('users/barroso2501/pasture-crop:lib/constants');
var BASELINES = [1985,1995,2000];
var INTERVALS = [[1985,1990],[1990,1995],[1995,2000],[2000,2005],
  [2005,2010],[2010,2015],[2015,2020],[2020,2025]];
var PILOT_CELL_IDS = ['32173','18081'];
var PILOT_GRID_IDS = ['IK-77','GH-123'];
var BATCHES = [0,1,2,3,4,5,6,7];
var MISSING = -9999;
var SOURCE_CODES = K.expectedSourceCodes();
var SYNTHETIC_CASES = [{"case_id":"continuous","values":[15,15,15],"expected":[1,1,1]},{"case_id":"exit_reentry","values":[15,39,39,15,15],"expected":[1,0,0,2,2]},{"case_id":"first_and_reentry","values":[3,15,15,3,15],"expected":[0,2,2,0,2]},{"case_id":"repeated_reentry","values":[15,3,15,3,15],"expected":[1,0,2,0,2]},{"case_id":"gap_after_initial","values":[15,27,15],"expected":[1,4,3]},{"case_id":"gap_after_entry","values":[39,15,27,15],"expected":[0,2,4,3]},{"case_id":"baseline_nodata","values":[27,15,15],"expected":[4,3,3]},{"case_id":"baseline_masked","values":[null,15,15],"expected":[4,3,3]},{"case_id":"reset_after_gap","values":[15,27,3,15],"expected":[1,4,0,2]},{"case_id":"unexpected_gap","values":[15,999,15],"expected":[1,4,3]}];
var coverage = ee.Image(K.COVERAGE_ASSET);
// BEGIN_NATIVE_PROJECTION_METADATA
// A single small metadata request, before any export task is created.
// Projection.transform() is a WKT string, not the six affine coefficients.
var nativeProjectionInfo = coverage.select(K.coverageBandName(1985))
  .projection().getInfo();
if (!nativeProjectionInfo || typeof nativeProjectionInfo.crs !== 'string' ||
    !nativeProjectionInfo.crs.length ||
    !Array.isArray(nativeProjectionInfo.transform) ||
    nativeProjectionInfo.transform.length !== 6 ||
    !nativeProjectionInfo.transform.every(function(value) {
      return typeof value === 'number' && isFinite(value);
    })) {
  throw new Error('Coverage projection metadata must contain a CRS and six finite affine coefficients.');
}
var nativeTransformCsv = nativeProjectionInfo.transform.join('|');
// END_NATIVE_PROJECTION_METADATA
var grid = ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa = ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var folder = 'window_origin_sensitivity_v1';
var RUNTIME_CONFIG = JSON.stringify({version:SCRIPT_VERSION,
  coverage_asset:K.COVERAGE_ASSET,grid_asset:K.ANALYTICAL_GRID,
  crs:K.CRS,crs_transform:K.CRS_TRANSFORM,classes:K.CLASS_CODES,
  valid_source_codes:SOURCE_CODES,baselines:BASELINES,
  square_metres_per_hectare:K.SQUARE_METRES_PER_HECTARE,
  constants_module:'users/barroso2501/pasture-crop:lib/constants'});
function readCoverage(year) {
  return coverage.select(K.coverageBandName(year));
}
function inCodes(image,codes) {
  var out=image.eq(codes[0]);
  for(var i=1;i<codes.length;i++) out=out.or(image.eq(codes[i]));
  return out;
}
// BEGIN_RECONSTRUCTION_ENGINE
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
// END_RECONSTRUCTION_ENGINE

var METRICS=['flow_pas_tmp_ha','stock0_pas_ha','baseline_pas_stock_ha',
  'initial_ha','entry_ha','unresolved_ha','initial_pas_stock_ha',
  'entry_pas_stock_ha','unresolved_pas_stock_ha',
  'origin_partition_error_pixel_years','initial_continuity_error_pixel_years',
  'confirmed_entry_error_pixel_years'];
var SELECTORS=['cell_id','GRID_ID','source_batch_id','baseline_year','t0','t1',
  'elapsed_intervals','diagnostic_interval','baseline_interval_by_construction',
  'scope','output_version','run_id'].concat(METRICS);
var manifestFeatures=[];
INTERVAL_INDICES.forEach(function(index) {
  if(index<2 || index>7 || index!==Math.floor(index))
    throw new Error('Fresh sensitivity intervals must have indices 2..7');
  var t0=INTERVALS[index][0],t1=INTERVALS[index][1];
  var active=BASELINES.filter(function(b) {return b<=t0;});
  var runId=RUN_TAG+'_'+MODE+'_i'+index;
  var c0=readCoverage(t0).unmask(MISSING);
  var c1=readCoverage(t1).unmask(MISSING);
  var pas0=c0.eq(15),pasTmp=pas0.and(inCodes(c1,K.CLASS_CODES.TMP));
  var bands=[];
  function add(mask,name,isPixelYears) {
    bands.push((isPixelYears ? mask.toDouble() : mask.multiply(pixelHa))
      .rename(name).unmask(0));
  }
  add(pasTmp,'flow_pas_tmp_ha',false);
  add(pas0,'stock0_pas_ha',false);
  active.forEach(function(base) {
    var built=reconstruct(base,t0,readCoverage,null),state=built.state;
    var prefix='b'+base+'_';
    add(readCoverage(base).unmask(MISSING).eq(15),prefix+'baseline_pas_stock_ha',false);
    ['initial','entry','unresolved'].forEach(function(label,n) {
      add(pasTmp.and(state.eq(n+1)),prefix+label+'_ha',false);
      add(pas0.and(state.eq(n+1)),prefix+label+'_pas_stock_ha',false);
    });
    add(built.partitionErrors,prefix+'origin_partition_error_pixel_years',true);
    add(built.initialErrors,prefix+'initial_continuity_error_pixel_years',true);
    add(built.entryErrors,prefix+'confirmed_entry_error_pixel_years',true);
  });
  // One native reduction for all active baselines, then reshape its rows.
  var image=ee.Image.cat(bands);
  var groups=MODE==='pilot' ? [-1] : BATCHES;
  groups.forEach(function(batch) {
    var cells=MODE==='pilot' ? grid.filter(ee.Filter.inList('GRID_ID',PILOT_GRID_IDS)) :
      grid.filter(ee.Filter.eq('source_batch_id',batch));
    var reduced=image.reduceRegions({collection:cells,reducer:ee.Reducer.sum(),
      crs:K.CRS,crsTransform:K.CRS_TRANSFORM,tileScale:16,
      maxPixelsPerRegion:100000000});
    var tables=active.map(function(base) {
      return reduced.map(function(f) {
        var data={cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),
          source_batch_id:f.get('source_batch_id'),baseline_year:base,t0:t0,t1:t1,
          elapsed_intervals:(t0-base)/5,diagnostic_interval:t0===2020?1:0,
          baseline_interval_by_construction:t0===base?1:0,scope:MODE,
          output_version:SCRIPT_VERSION,run_id:runId,
          flow_pas_tmp_ha:f.get('flow_pas_tmp_ha'),stock0_pas_ha:f.get('stock0_pas_ha')};
        METRICS.slice(2).forEach(function(name) {data[name]=f.get('b'+base+'_'+name);});
        return ee.Feature(null,data);
      });
    });
    var table=tables[0];
    for(var n=1;n<tables.length;n++) table=table.merge(tables[n]);
    var name='canonical_window_origin_'+t0+'_'+t1+'_'+
      (MODE==='pilot'?'pilot':'b'+('0'+batch).slice(-2))+'_v1';
    Export.table.toDrive({collection:table,description:name,fileNamePrefix:name,
      folder:folder,fileFormat:'CSV',selectors:SELECTORS});
    print('TASK:',name,'| active baselines:',active);
  });
  manifestFeatures.push(ee.Feature(null,{run_id:runId,scope:MODE,
    interval_index:index,t0:t0,t1:t1,baselines_json:JSON.stringify(active),
    expected_cells:MODE==='pilot'?2:24889,source_script:SOURCE_SCRIPT,
    output_version:SCRIPT_VERSION,config_json:RUNTIME_CONFIG,
    coverage_band_count:coverage.bandNames().size(),
    coverage_bands_csv:ee.List(coverage.bandNames()).join('|'),
    native_crs:nativeProjectionInfo.crs,
    native_transform_csv:nativeTransformCsv,
    pilot_cells_json:JSON.stringify(PILOT_CELL_IDS)}));
});
var manifestName='canonical_window_origin_run_manifest_'+MODE+'_v1';
Export.table.toDrive({collection:ee.FeatureCollection(manifestFeatures),
  description:manifestName,fileNamePrefix:manifestName,folder:folder,fileFormat:'CSV',
  selectors:['run_id','scope','interval_index','t0','t1','baselines_json',
    'expected_cells','source_script','output_version','config_json','pilot_cells_json',
    'coverage_band_count','coverage_bands_csv','native_crs','native_transform_csv']});

if(MODE==='pilot') {
  // Tests execute the actual reconstruction function as native ee.Image graphs.
  var region=ee.Geometry.Rectangle([-47,-16,-46.999,-15.999],K.CRS,false);
  var nativeTests=[];
  BASELINES.forEach(function(base) {
    SYNTHETIC_CASES.forEach(function(test) {
      function fixtureCoverage(year) {
        var value=test.values[year-base];
        return value===null ? ee.Image.constant(0).updateMask(ee.Image.constant(0)) :
          ee.Image.constant(value);
      }
      var built=reconstruct(base,base+test.values.length-1,fixtureCoverage,test.expected);
      var errors=ee.Image.cat([
        ee.Image.constant(1).rename('test_pixel_equivalents'),
        built.expectedErrors.rename('state_mismatch_pixel_steps'),
        built.partitionErrors.rename('partition_mismatch_pixel_steps'),
        built.initialErrors.rename('initial_mismatch_pixel_steps'),
        built.entryErrors.rename('entry_mismatch_pixel_steps')]);
      var totals=errors.reduceRegion({reducer:ee.Reducer.sum(),geometry:region,
        crs:K.CRS,crsTransform:K.CRS_TRANSFORM,maxPixels:10000});
      nativeTests.push(ee.Feature(null,totals).set({baseline_year:base,
        case_id:test.case_id,steps:test.values.length,scope:'native_synthetic',
        output_version:SCRIPT_VERSION,run_id:RUN_TAG+'_pilot_native_synthetic'}));
    });
  });
  Export.table.toDrive({collection:ee.FeatureCollection(nativeTests),
    description:'canonical_window_origin_native_synthetic_v1',
    fileNamePrefix:'canonical_window_origin_native_synthetic_v1',folder:folder,fileFormat:'CSV',
    selectors:['baseline_year','case_id','steps','scope','output_version','run_id',
      'test_pixel_equivalents','state_mismatch_pixel_steps','partition_mismatch_pixel_steps',
      'initial_mismatch_pixel_steps','entry_mismatch_pixel_steps']});
  print('PILOT: 3 tasks: two-cell table, run manifest, native synthetic tests.');
} else {
  print('FULL: 48 cell-table tasks plus one run-manifest task.');
}
print('Use the Python validator before interpreting any exported percentages.');
print('1985 is a control; sensitivity does not identify a fraction of window artifact.');

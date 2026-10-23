/** Entry/re-entry auxiliary decomposition: pilot only, four CSV tasks.
 * Copy this entire file to the GEE Code Editor without editing parameters.
 * Coverage-only reconstruction; historical data, origins and matrix unchanged.
 */
var VERSION='entry-reentry-pilot-v1', RUN_TAG='er1_20261021';
var SOURCE_SCRIPT='20a_export_entry_reentry_pilot_v1.js';
var K=require('users/barroso2501/pasture-crop:lib/constants');
var SOURCE_CODES=K.expectedSourceCodes(), MISSING=-9999;
var START=1985, END=2025, INTERVALS=[[2015,2020],[2020,2025]];
var CELLS=[{"cell_id":"18081","GRID_ID":"GH-123","source_batch_id":1},{"cell_id":"32173","GRID_ID":"IK-77","source_batch_id":5}];
var FIXTURES=[{"case_id":"continuous_initial","start_year":1985,"values":[15,15,15],"masked":[false,false,false],"expected_state":[1,1,1],"expected_age":[100,100,100],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"first_entry_continues","start_year":1985,"values":[3,15,15,15],"masked":[false,false,false,false],"expected_state":[0,2,2,2],"expected_age":[0,201,202,203],"expected_entry_kind":[0,1,1,1],"expected_confirmed_entry_count":[0,1,1,1],"expected_entry_year":[0,1986,1986,1986],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"baseline_exit_reentry","start_year":1985,"values":[15,39,15,15],"masked":[false,false,false,false],"expected_state":[1,0,2,2],"expected_age":[100,0,201,202],"expected_entry_kind":[0,0,2,2],"expected_confirmed_entry_count":[0,0,1,1],"expected_entry_year":[0,0,1987,1987],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"repeated_reentry","start_year":1985,"values":[3,15,3,15,3,15],"masked":[false,false,false,false,false,false],"expected_state":[0,2,0,2,0,2],"expected_age":[0,201,0,201,0,201],"expected_entry_kind":[0,1,0,2,0,2],"expected_confirmed_entry_count":[0,1,1,2,2,3],"expected_entry_year":[0,1986,0,1988,0,1990],"expected_boundary_adjacent":[0,0,0,0,0,0]},{"case_id":"gap_after_initial","start_year":1985,"values":[15,27,15,15],"masked":[false,false,false,false],"expected_state":[1,4,3,3],"expected_age":[100,0,0,0],"expected_entry_kind":[0,0,0,0],"expected_confirmed_entry_count":[0,0,0,0],"expected_entry_year":[0,0,0,0],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"gap_after_entry","start_year":1985,"values":[3,15,27,15,15],"masked":[false,false,false,false,false],"expected_state":[0,2,4,3,3],"expected_age":[0,201,0,0,0],"expected_entry_kind":[0,1,0,0,0],"expected_confirmed_entry_count":[0,1,1,1,1],"expected_entry_year":[0,1986,0,0,0],"expected_boundary_adjacent":[0,0,0,0,0]},{"case_id":"baseline_nodata","start_year":1985,"values":[27,15,15],"masked":[false,false,false],"expected_state":[4,3,3],"expected_age":[0,0,0],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"baseline_masked","start_year":1985,"values":[15,15,15],"masked":[true,false,false],"expected_state":[4,3,3],"expected_age":[0,0,0],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"gap_then_reset_first_uncertain","start_year":1985,"values":[27,3,15,15],"masked":[false,false,false,false],"expected_state":[4,0,2,2],"expected_age":[0,0,201,202],"expected_entry_kind":[0,0,3,3],"expected_confirmed_entry_count":[0,0,1,1],"expected_entry_year":[0,0,1987,1987],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"gap_before_nonpas_reset","start_year":1985,"values":[3,27,3,15],"masked":[false,false,false,false],"expected_state":[0,4,0,2],"expected_age":[0,0,0,201],"expected_entry_kind":[0,0,0,3],"expected_confirmed_entry_count":[0,0,0,1],"expected_entry_year":[0,0,0,1988],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"prior_pas_gap_reset_reentry","start_year":1985,"values":[15,27,3,15,15],"masked":[false,false,false,false,false],"expected_state":[1,4,0,2,2],"expected_age":[100,0,0,201,202],"expected_entry_kind":[0,0,0,2,2],"expected_confirmed_entry_count":[0,0,0,1,1],"expected_entry_year":[0,0,0,1988,1988],"expected_boundary_adjacent":[0,0,0,0,0]},{"case_id":"unresolved_pas_then_reentry","start_year":1985,"values":[27,15,3,15,15],"masked":[false,false,false,false,false],"expected_state":[4,3,0,2,2],"expected_age":[0,0,0,201,202],"expected_entry_kind":[0,0,0,2,2],"expected_confirmed_entry_count":[0,0,0,1,1],"expected_entry_year":[0,0,0,1988,1988],"expected_boundary_adjacent":[0,0,0,0,0]},{"case_id":"prior_uncertain_first_then_reentry","start_year":1985,"values":[27,3,15,3,15],"masked":[false,false,false,false,false],"expected_state":[4,0,2,0,2],"expected_age":[0,0,201,0,201],"expected_entry_kind":[0,0,3,0,2],"expected_confirmed_entry_count":[0,0,1,1,2],"expected_entry_year":[0,0,1987,0,1989],"expected_boundary_adjacent":[0,0,0,0,0]},{"case_id":"unexpected_zero","start_year":1985,"values":[0,3,15,15],"masked":[false,false,false,false],"expected_state":[4,0,2,2],"expected_age":[0,0,201,202],"expected_entry_kind":[0,0,3,3],"expected_confirmed_entry_count":[0,0,1,1],"expected_entry_year":[0,0,1987,1987],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"unexpected_minus9999","start_year":1985,"values":[-9999,3,15,15],"masked":[false,false,false,false],"expected_state":[4,0,2,2],"expected_age":[0,0,201,202],"expected_entry_kind":[0,0,3,3],"expected_confirmed_entry_count":[0,0,1,1],"expected_entry_year":[0,0,1987,1987],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"unexpected_999","start_year":1985,"values":[999,3,15,15],"masked":[false,false,false,false],"expected_state":[4,0,2,2],"expected_age":[0,0,201,202],"expected_entry_kind":[0,0,3,3],"expected_confirmed_entry_count":[0,0,1,1],"expected_entry_year":[0,0,1987,1987],"expected_boundary_adjacent":[0,0,0,0]},{"case_id":"masked_pas_does_not_create_prior_pas","start_year":1985,"values":[15,3,15],"masked":[true,false,false],"expected_state":[4,0,2],"expected_age":[0,0,201],"expected_entry_kind":[0,0,3],"expected_confirmed_entry_count":[0,0,1],"expected_entry_year":[0,0,1987],"expected_boundary_adjacent":[0,0,0]},{"case_id":"masked_valid_nonpas_is_gap","start_year":1985,"values":[3,3,15],"masked":[false,true,false],"expected_state":[0,4,3],"expected_age":[0,0,0],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_1","start_year":1985,"values":[1,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_39","start_year":1985,"values":[39,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_26","start_year":1985,"values":[26,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_84","start_year":1985,"values":[84,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_75","start_year":1985,"values":[75,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"valid_source_91","start_year":1985,"values":[91,15,15],"masked":[false,false,false],"expected_state":[0,2,2],"expected_age":[0,201,202],"expected_entry_kind":[0,1,1],"expected_confirmed_entry_count":[0,1,1],"expected_entry_year":[0,1986,1986],"expected_boundary_adjacent":[0,0,0]},{"case_id":"all_nonpas","start_year":1985,"values":[3,39,26],"masked":[false,false,false],"expected_state":[0,0,0],"expected_age":[0,0,0],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"all_uncertain","start_year":1985,"values":[27,999,15],"masked":[false,false,true],"expected_state":[4,4,4],"expected_age":[0,0,0],"expected_entry_kind":[0,0,0],"expected_confirmed_entry_count":[0,0,0],"expected_entry_year":[0,0,0],"expected_boundary_adjacent":[0,0,0]},{"case_id":"entry_2024_continues_2025","start_year":1985,"values":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,15,15],"masked":[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"expected_state":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],"expected_age":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,201,202],"expected_entry_kind":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],"expected_confirmed_entry_count":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],"expected_entry_year":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024,2024],"expected_boundary_adjacent":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]},{"case_id":"reentry_2025","start_year":1985,"values":[15,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,15],"masked":[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"expected_state":[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],"expected_age":[100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,201],"expected_entry_kind":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],"expected_confirmed_entry_count":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],"expected_entry_year":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2025],"expected_boundary_adjacent":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]},{"case_id":"first_entry_maximum_age_240","start_year":1985,"values":[3,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],"masked":[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"expected_state":[0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],"expected_age":[0,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240],"expected_entry_kind":[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"expected_confirmed_entry_count":[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"expected_entry_year":[0,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986,1986],"expected_boundary_adjacent":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},{"case_id":"initial_continuity_41years","start_year":1985,"values":[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],"masked":[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"expected_state":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],"expected_age":[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100],"expected_entry_kind":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"expected_confirmed_entry_count":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"expected_entry_year":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"expected_boundary_adjacent":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]},{"case_id":"entry_2024_exit_2025","start_year":1985,"values":[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,15,3],"masked":[false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false],"expected_state":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],"expected_age":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,201,0],"expected_entry_kind":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],"expected_confirmed_entry_count":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],"expected_entry_year":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2024,0],"expected_boundary_adjacent":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]}];
var FOLDER='entry_reentry_pilot_v1';
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

var AREAS=['domain_ha','flow_pas_tmp_ha','stock0_pas_ha','initial_ha','entry_ha','unresolved_ha',
  'first_observed_entry_ha','observed_reentry_ha','prior_history_uncertain_ha',
  'initial_pas_stock_ha','entry_pas_stock_ha','unresolved_pas_stock_ha',
  'first_observed_entry_pas_stock_ha','observed_reentry_pas_stock_ha','prior_history_uncertain_pas_stock_ha',
  'control_initial_ha','control_entry_ha','control_unresolved_ha',
  'control_initial_pas_stock_ha','control_entry_pas_stock_ha','control_unresolved_pas_stock_ha'];
var CELL_ERRORS=['accepted_origin_mismatch_pixel_equivalents'];
var KEYS=['cell_id','GRID_ID','source_batch_id','t0','t1','diagnostic_interval','scope','output_version','run_id'];
var ERRORS=['origin_partition_error_pixel_years','initial_continuity_error_pixel_years',
  'auxiliary_partition_error_pixel_years','entry_label_error_pixel_years','frozen_label_error_pixel_years',
  'entry_age201_error_pixel_years','reentry_age201_error_pixel_years','auxiliary_age_error_pixel_years',
  'entry_count_error_pixel_years','entry_metadata_error_pixel_years'];
var AUDIT_COUNTS=['history_support_pixel_equivalents','confirmed_entry_pixel_years',
  'confirmed_reentry_pixel_years','first_observed_entry_pixel_years','prior_history_uncertain_entry_pixel_years'];
var BOUNDARY_AREAS=['entry_2024_ha','termination_2024_ha','entry_2025_ha','termination_2025_ha'];
var AUDIT_KEYS=['cell_id','GRID_ID','source_batch_id','start_year','end_year','years_checked','scope','output_version','run_id'];
var NATIVE_ERRORS=['expected_state_error_pixel_steps','expected_age_error_pixel_steps',
  'expected_kind_error_pixel_steps','expected_count_error_pixel_steps',
  'expected_entry_year_error_pixel_steps','expected_boundary_error_pixel_steps'].concat(ERRORS);
var NATIVE_KEYS=['case_id','start_year','end_year','steps','scope','output_version','run_id',
  'expected_final_state','expected_final_age','expected_final_kind','expected_final_count',
  'expected_final_entry_year','test_pixel_equivalents'];
var coverage=ee.Image(K.COVERAGE_ASSET),grid=ee.FeatureCollection(K.ANALYTICAL_GRID);
var pixelHa=ee.Image.pixelArea().divide(K.SQUARE_METRES_PER_HECTARE);
var RUNTIME={version:VERSION,coverage_asset:K.COVERAGE_ASSET,grid_asset:K.ANALYTICAL_GRID,
  constants_module:'users/barroso2501/pasture-crop:lib/constants',valid_source_codes:SOURCE_CODES,
  class_groups:K.CLASS_CODES,crs:K.CRS,crs_transform:K.CRS_TRANSFORM,
  square_metres_per_hectare:K.SQUARE_METRES_PER_HECTARE,start_year:START,end_year:END,
  intervals:INTERVALS,pilot_cells:CELLS,
  footprint_convention:'accepted_coverage_unmask_sameFootprint_true_no_gap_bridging',
  auxiliary_labels:{none:0,first_observed_entry:1,observed_reentry:2,prior_history_uncertain:3},
  tile_scale:16,max_pixels_per_region:100000000};
var EXPECTED_RUNTIME={"version":"entry-reentry-pilot-v1","coverage_asset":"projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3","grid_asset":"projects/ee-barroso2501/assets/grade_hex_CeAmz_canonical_c11_v3","constants_module":"users/barroso2501/pasture-crop:lib/constants","valid_source_codes":[1,3,4,5,6,7,9,10,11,12,13,15,19,20,21,22,23,24,25,26,27,29,30,31,32,33,35,36,39,40,41,46,47,48,49,50,62,75,84,91],"class_groups":{"NAT":[1,3,4,5,6,7,10,11,12,13,29,32,49,50,84],"PAS":[15],"TMP":[19,20,39,40,41,62],"OAG":[9,21,35,36,46,47,48],"OUT":[22,23,24,25,30,75,91],"WATER":[26,31,33],"NODATA":[27]},"crs":"EPSG:4326","crs_transform":[0.00026949458523585647,0,-74.02073025380652,0,-0.00026949458523585647,5.405791885246045],"start_year":1985,"end_year":2025,"intervals":[[2015,2020],[2020,2025]],"pilot_cells":[{"cell_id":"18081","GRID_ID":"GH-123","source_batch_id":1},{"cell_id":"32173","GRID_ID":"IK-77","source_batch_id":5}],"footprint_convention":"accepted_coverage_unmask_sameFootprint_true_no_gap_bridging","square_metres_per_hectare":10000,"auxiliary_labels":{"none":0,"first_observed_entry":1,"observed_reentry":2,"prior_history_uncertain":3},"tile_scale":16,"max_pixels_per_region":100000000};
function canonical(value){if(Array.isArray(value)) return '['+value.map(canonical).join(',')+']';
  if(value && typeof value==='object') return '{'+Object.keys(value).sort().map(function(k){return JSON.stringify(k)+':'+canonical(value[k]);}).join(',')+'}';
  return JSON.stringify(value);}
if(canonical(RUNTIME)!==canonical(EXPECTED_RUNTIME)) throw new Error('Installed constants differ from the supplied pilot configuration');
function readCoverage(y){return coverage.select(K.coverageBandName(y));}
function inCodes(img,codes){var hit=img.eq(codes[0]);for(var j=1;j<codes.length;j++) hit=hit.or(img.eq(codes[j]));return hit;}
// Metadata only; no raster preview or domain-wide Console aggregation.
var nativeProjections={};
for(var yr=START;yr<=END;yr++) {
  var info=readCoverage(yr).projection().getInfo();
  if(!info || info.crs!==K.CRS || !Array.isArray(info.transform) || info.transform.length!==6 ||
      !info.transform.every(function(v,k){return typeof v==='number' && isFinite(v) && Math.abs(v-K.CRS_TRANSFORM[k])<=1e-13;}))
    throw new Error('Native projection differs at '+yr);
  nativeProjections[yr]={crs:info.crs,transform:info.transform};
}
var expectedBands=[];for(var by=START;by<=END;by++) expectedBands.push(K.coverageBandName(by));
var actualBands=coverage.bandNames().getInfo();
if(JSON.stringify(actualBands)!==JSON.stringify(expectedBands)) throw new Error('Expected exactly 41 ordered annual coverage bands');

var p=emptyEntryState(),snapshots={},totals={},counts={},boundary={};
ERRORS.forEach(function(k){totals[k]=ee.Image.constant(0).toDouble();});
AUDIT_COUNTS.forEach(function(k){counts[k]=ee.Image.constant(0).toDouble();});
counts.history_support_pixel_equivalents=ee.Image.constant(1).toDouble();
for(var year=START;year<=END;year++) {
  p=advanceEntry(p,readCoverage(year),year,year===START);
  ERRORS.forEach(function(k){totals[k]=totals[k].add(p.errors[k].unmask(0,true));});
  counts.confirmed_entry_pixel_years=counts.confirmed_entry_pixel_years.add(p.entered.unmask(0,true));
  counts.confirmed_reentry_pixel_years=counts.confirmed_reentry_pixel_years.add(p.entered.and(p.kind.eq(2)).unmask(0,true));
  counts.first_observed_entry_pixel_years=counts.first_observed_entry_pixel_years.add(p.entered.and(p.kind.eq(1)).unmask(0,true));
  counts.prior_history_uncertain_entry_pixel_years=counts.prior_history_uncertain_entry_pixel_years.add(p.entered.and(p.kind.eq(3)).unmask(0,true));
  if(year===2015 || year===2020) snapshots[year]=p;
  if(year===2024 || year===2025) {
    boundary['entry_'+year+'_ha']=p.entered;
    boundary['termination_'+year+'_ha']=p.terminated;
  }
}
var bands=[];
function area(mask,name){bands.push(mask.multiply(pixelHa).rename(name).unmask(0,true));}
function count(mask,name){bands.push(mask.toDouble().rename(name).unmask(0,true));}
INTERVALS.forEach(function(pair){
  var t0=pair[0],t1=pair[1],s=snapshots[t0];
  var control=reconstruct(START,t0,readCoverage,null).state;
  var pas=readCoverage(t0).unmask(MISSING,true).eq(15);
  var flow=pas.and(inCodes(readCoverage(t1).unmask(MISSING,true),K.CLASS_CODES.TMP));
  var prefix='t'+t0+'_';
  area(ee.Image.constant(1),prefix+'domain_ha');area(flow,prefix+'flow_pas_tmp_ha');area(pas,prefix+'stock0_pas_ha');
  ['initial','entry','unresolved'].forEach(function(k,j){
    area(flow.and(s.state.eq(j+1)),prefix+k+'_ha');
    area(pas.and(s.state.eq(j+1)),prefix+k+'_pas_stock_ha');
    area(flow.and(control.eq(j+1)),prefix+'control_'+k+'_ha');
    area(pas.and(control.eq(j+1)),prefix+'control_'+k+'_pas_stock_ha');
  });
  ['first_observed_entry','observed_reentry','prior_history_uncertain'].forEach(function(k,j){
    area(flow.and(s.state.eq(2)).and(s.kind.eq(j+1)),prefix+k+'_ha');
    area(pas.and(s.state.eq(2)).and(s.kind.eq(j+1)),prefix+k+'_pas_stock_ha');
  });
  count(s.state.neq(control),prefix+CELL_ERRORS[0]);
});
AUDIT_COUNTS.forEach(function(k){count(counts[k],'audit_'+k);});
ERRORS.forEach(function(k){count(totals[k],'audit_'+k);});
BOUNDARY_AREAS.forEach(function(k){area(boundary[k],'audit_'+k);});
// Select the same known cells by GRID_ID, retaining their canonical cell/batch identities.
var selected=grid.filter(ee.Filter.inList('GRID_ID',CELLS.map(function(c){return c.GRID_ID;})));
var reduced=ee.Image.cat(bands).reduceRegions({collection:selected,reducer:ee.Reducer.sum(),
  crs:K.CRS,crsTransform:K.CRS_TRANSFORM,tileScale:16,maxPixelsPerRegion:100000000});
function identity(f){return {cell_id:f.get('cell_id'),GRID_ID:f.get('GRID_ID'),source_batch_id:f.get('source_batch_id'),
  scope:'pilot',output_version:VERSION,run_id:RUN_TAG+'_pilot'};}
var tables=INTERVALS.map(function(pair){return reduced.map(function(f){
  var data=identity(f);data.t0=pair[0];data.t1=pair[1];data.diagnostic_interval=pair[0]===2020?1:0;
  AREAS.concat(CELL_ERRORS).forEach(function(k){data[k]=f.get('t'+pair[0]+'_'+k);});return ee.Feature(null,data);
});});
var cellTable=tables[0].merge(tables[1]);
var auditTable=reduced.map(function(f){var data=identity(f);data.start_year=START;data.end_year=END;data.years_checked=41;
  AUDIT_COUNTS.concat(ERRORS).concat(BOUNDARY_AREAS).forEach(function(k){data[k]=f.get('audit_'+k);});
  return ee.Feature(null,data);});
function exportCSV(table,name,selectors){Export.table.toDrive({collection:table,description:name,fileNamePrefix:name,
  folder:FOLDER,fileFormat:'CSV',selectors:selectors});print('TASK:',name);}
exportCSV(cellTable,'canonical_entry_reentry_pilot_v1',KEYS.concat(AREAS).concat(CELL_ERRORS));
exportCSV(auditTable,'canonical_entry_reentry_history_audit_pilot_v1',AUDIT_KEYS.concat(AUDIT_COUNTS).concat(ERRORS).concat(BOUNDARY_AREAS));

// All synthetic histories enter ONE small native reduction, without parallel reduceRegion calls.
var nativeBands=[];
FIXTURES.forEach(function(test,index){
  var s=emptyEntryState(),errs={};
  NATIVE_ERRORS.forEach(function(k){errs[k]=ee.Image.constant(0).toDouble();});
  test.values.forEach(function(value,j){
    var raw=ee.Image.constant(value);if(test.masked[j]) raw=raw.updateMask(ee.Image.constant(0));
    s=advanceEntry(s,raw,test.start_year+j,j===0);
    var expected=[s.state.neq(test.expected_state[j]),s.age.neq(test.expected_age[j]),s.kind.neq(test.expected_entry_kind[j]),
      s.count.neq(test.expected_confirmed_entry_count[j]),s.entryYear.neq(test.expected_entry_year[j]),
      s.entryYear.gte(2024).neq(test.expected_boundary_adjacent[j])];
    expected.forEach(function(e,k){errs[NATIVE_ERRORS[k]]=errs[NATIVE_ERRORS[k]].add(e);});
    ERRORS.forEach(function(k){errs[k]=errs[k].add(s.errors[k]);});
  });
  countNative(ee.Image.constant(1),'n'+index+'_support');
  NATIVE_ERRORS.forEach(function(k,j){countNative(errs[k],'n'+index+'_e'+j);});
});
function countNative(image,name){nativeBands.push(image.toDouble().rename(name));}
var testRegion=ee.Geometry.Rectangle([-47,-16,-46.999,-15.999],K.CRS,false);
var nativeTotals=ee.Image.cat(nativeBands).reduceRegion({reducer:ee.Reducer.sum(),geometry:testRegion,
  crs:K.CRS,crsTransform:K.CRS_TRANSFORM,maxPixels:10000,tileScale:4});
var nativeFeatures=FIXTURES.map(function(test,index){
  var last=test.values.length-1;
  var data={case_id:test.case_id,start_year:test.start_year,end_year:test.start_year+last,steps:last+1,
    scope:'native_synthetic',output_version:VERSION,run_id:RUN_TAG+'_pilot_native_synthetic',
    expected_final_state:test.expected_state[last],expected_final_age:test.expected_age[last],
    expected_final_kind:test.expected_entry_kind[last],expected_final_count:test.expected_confirmed_entry_count[last],
    expected_final_entry_year:test.expected_entry_year[last],test_pixel_equivalents:nativeTotals.get('n'+index+'_support')};
  NATIVE_ERRORS.forEach(function(k,j){data[k]=nativeTotals.get('n'+index+'_e'+j);});
  return ee.Feature(null,data);
});
exportCSV(ee.FeatureCollection(nativeFeatures),'canonical_entry_reentry_native_synthetic_v1',NATIVE_KEYS.concat(NATIVE_ERRORS));
var manifest=ee.FeatureCollection([ee.Feature(null,{scope:'pilot',output_version:VERSION,run_id:RUN_TAG+'_pilot',
  source_script:SOURCE_SCRIPT,expected_cells:2,expected_rows:4,expected_audit_rows:2,
  expected_native_cases:FIXTURES.length,expected_native_steps:302,config_json:JSON.stringify(RUNTIME),
  coverage_band_count:actualBands.length,coverage_bands_csv:actualBands.join('|'),
  native_projections_json:JSON.stringify(nativeProjections),
  audit_start_year:START,audit_end_year:END,audit_years_checked:41})]);
exportCSV(manifest,'canonical_entry_reentry_manifest_pilot_v1',['scope','output_version','run_id','source_script',
  'expected_cells','expected_rows','expected_audit_rows','expected_native_cases','expected_native_steps','config_json',
  'coverage_band_count','coverage_bands_csv','native_projections_json','audit_start_year','audit_end_year','audit_years_checked']);
print('PILOT: FOUR CSV TASKS. Wait for all four files to appear in Drive, then return them together.');
print('Native acceptance and scientific decomposition remain PENDING until those CSVs pass the validator.');

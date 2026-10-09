var VERSION="observed-pasture-spell-step1-pilot-v1";
var K={expectedSourceCodes:function(){return [3,15,27,39];}};var START=1985;var MISSING=-9999;function print(){ }
var S = {NONPAS: 0, INITIAL: 1, NEW: 2, UNRESOLVED: 3, UNCERTAIN: 4};
var PAS = 15;
var NODATA = 27;
var SOURCE_CODES = K.expectedSourceCodes();

function observation(value) {
  if (value === PAS) return 'PAS';
  if (value === MISSING || value === NODATA ||
      SOURCE_CODES.indexOf(value) === -1) return 'UNCERTAIN';
  return 'NONPAS';
}

function advance(previous, currentObservation, firstYear, year) {
  var state;
  var age = 0;
  var entry = 0;
  var termination = 0;
  if (currentObservation === 'UNCERTAIN') {
    state = S.UNCERTAIN;
  } else if (currentObservation === 'NONPAS') {
    state = S.NONPAS;
    termination = !firstYear && [S.INITIAL, S.NEW, S.UNRESOLVED]
      .indexOf(previous.state) !== -1 ? year : 0;
  } else if (firstYear || previous.state === S.INITIAL) {
    state = S.INITIAL;
    age = 100;
  } else if (previous.state === S.NONPAS) {
    state = S.NEW;
    age = 201;
    entry = year;
  } else if (previous.state === S.NEW) {
    state = S.NEW;
    age = previous.age + 1;
  } else {
    state = S.UNRESOLVED;
  }
  return {state: state, age: age, entry: entry,
    termination: termination};
}

function runSynthetic(codes) {
  var p = {state: S.UNCERTAIN, age: 0};
  return codes.map(function (v, i) {
    p = advance(p, observation(v), i === 0, START + i);
    return p.state === S.UNCERTAIN ? 'uncertain' :
      p.state === S.UNRESOLVED ? 'unresolved' :
      p.state === S.NONPAS ? 'NA' : p.age;
  });
}

var cases = [
  [[15,15,15], [100,100,100]],
  [[15,15,39,15,15], [100,100,'NA',201,202]],
  [[3,15,15,3,15], ['NA',201,202,'NA',201]],
  [[15,3,15,3,15], [100,'NA',201,'NA',201]],
  [[15,27,15], [100,'uncertain','unresolved']],
  [[39,15,27,15], ['NA',201,'uncertain','unresolved']],
  [[27,15,15], ['uncertain','unresolved','unresolved']],
  [[MISSING,15,3,15], ['uncertain','unresolved','NA',201]],
  [[15,27,15,3,15], [100,'uncertain','unresolved','NA',201]],
  [[15,999,15], [100,'uncertain','unresolved']]
];
cases.forEach(function (c, i) {
  var found = runSynthetic(c[0]);
  if (JSON.stringify(found) !== JSON.stringify(c[1])) {
    throw new Error('Synthetic case ' + (i + 1) + ' failed: ' +
      JSON.stringify(found) + ' != ' + JSON.stringify(c[1]));
  }
});
var boundary = advance({state:S.NONPAS,age:0},'PAS',false,2024);
var exit = advance({state:S.NEW,age:201},'NONPAS',false,2025);
if (boundary.entry !== 2024 || exit.termination !== 2025) {
  throw new Error('Boundary-event year check failed');
}
print('PASTURE-SPELL RECONSTRUCTION — STEP 1 PILOT');
print('Script version:', VERSION);
print('SYNTHETIC ENGINE: PASS; cases:', cases.length);
print('2024 entry and 2025 termination event-year check: PASS');


console.log(JSON.stringify({status:'PASS',cases:cases.length,boundary_event_year_check:boundary.entry===2024&&exit.termination===2025}));

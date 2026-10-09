class Img {constructor(v){this.v=v;} byte(){return this;} toInt16(){return this;} unmask(v){return new Img(this.v==null?v:this.v);} eq(v){return new Img(Number(this.v===(v instanceof Img?v.v:v)));} and(o){return new Img(Number(Boolean(this.v)&&Boolean(o.v)));} or(o){return new Img(Number(Boolean(this.v)||Boolean(o.v)));} not(){return new Img(Number(!this.v));} where(cond,v){return cond.v?new Img(v instanceof Img?v.v:v):this;}}
const ee={Image:{constant:v=>new Img(v)}};const K={coverageBandName:y=>y};const sourceCodes=[3,15,27,39];const MISSING=-9999;
function observed(codes){const T0=1985+codes.length-1;const coverage={select:y=>new Img(codes[y-1985])};
var previous=ee.Image.constant(4).byte();
for(var year=1985;year<=T0;year++) {
  var cov=coverage.select(K.coverageBandName(year))
    .unmask(MISSING).toInt16();
  var pas=cov.eq(15);
  var non=ee.Image.constant(0).eq(1);
  sourceCodes.forEach(function(code) {
    if(code!==15 && code!==27) non=non.or(cov.eq(code));
  });
  var initial=year===1985 ? pas : pas.and(previous.eq(1));
  var entered=year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(0));
  var continued=year===1985 ? ee.Image.constant(0).eq(1) :
    pas.and(previous.eq(2));
  previous=ee.Image.constant(4).byte().where(non,0).where(initial,1)
    .where(entered.or(continued),2)
    .where(pas.and(initial.not()).and(entered.not())
      .and(continued.not()),3);
}
return previous.v;}
function expected(codes){let state=4;for(let i=0;i<codes.length;i++){const c=codes[i];if(c===15)state=i===0||state===1?1:state===0||state===2?2:3;else state=c===3||c===39?0:4;}return state;}
const values=[15,3,39,27,-9999,999];let count=0;function visit(a){if(a.length){if(observed(a)!==expected(a))throw Error('Production state mismatch '+JSON.stringify(a));count++;}if(a.length<5)for(const v of values)visit([...a,v]);}visit([]);
let maxYear=0;for(let y=1985;y<=2025;y++){const a=Array(y-1985+1).fill(15);if(observed(a)!==1)throw Error('continuous');maxYear=y;}
console.log(JSON.stringify({status:'PASS',production_histories_checked:count,continuous_history_through:maxYear,classes_checked:values,all_states_single_valued:true}));

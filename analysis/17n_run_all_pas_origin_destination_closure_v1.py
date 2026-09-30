"""Run 17m v3 over all eight intervals from _pilot_v1 GEE exports.

The script skips incomplete intervals, displays every validator error, and
never marks an interval accepted unless its own validator reports PASS.
"""
import subprocess
import sys
from pathlib import Path

ROOT=Path('/content/drive/MyDrive')
PROJECT=ROOT/'Trabalho/Contabilidade'
SCRIPT=Path('/content/17m_validate_pas_origin_destination_full_v3.py')
CLOSURE_DIR=PROJECT/'spatial/phase9/pasture_spell_closure_pilot_v1'
RQ2_PILOT_DIR=ROOT/'pasture_spell_remediation_pilot_v1'
RQ2_REMAINING_DIR=ROOT/'pasture_spell_remediation_remaining_v1'
RQ2_VALIDATIONS=PROJECT/'spatial/phase9/pasture_spell_series_v1'
OUTPUT_DIR=PROJECT/'spatial/phase9/pasture_spell_closure_full_v1'
INTERVALS=((1985,1990),(1990,1995),(1995,2000),(2000,2005),
           (2005,2010),(2010,2015),(2015,2020),(2020,2025))


def main():
    if not SCRIPT.is_file():
        raise FileNotFoundError(f'Upload the 17m v3 script to {SCRIPT}')
    results=[]
    for t0,t1 in INTERVALS:
        interval=f'{t0}_{t1}'
        is_2015=t0==2015
        baseline=PROJECT/'csv'/f'canonical_stock_flow_{interval}_full_v1.csv'
        validation=(RQ2_VALIDATIONS/
                    f'canonical_pas_tmp_origin_impact_{interval}_validation_v1.json')
        rq2dir=RQ2_PILOT_DIR if is_2015 else RQ2_REMAINING_DIR
        suffix='v3' if is_2015 else 'v4'
        closure=[CLOSURE_DIR/
                 f'canonical_pas_origin_destination_{interval}_b{b:02d}_pilot_v1.csv'
                 for b in range(8)]
        rq2=[rq2dir/f'canonical_pas_tmp_origin_{interval}_b{b:02d}_{suffix}.csv'
             for b in range(8)]
        required=[baseline,validation,*closure,*rq2]
        if is_2015:
            pilot_validation=(CLOSURE_DIR/
                              'canonical_pas_origin_destination_2015_2020_b00_validation_v1.json')
            required.append(pilot_validation)
        missing=[str(path) for path in required if not path.is_file()]
        print(f'\n=== {t0}–{t1} ===',flush=True)
        if missing:
            print('PENDING: missing input files:',*missing,sep='\n  ',flush=True)
            results.append((interval,'PENDING'))
            continue
        command=[sys.executable,str(SCRIPT),'--t0',str(t0),
                 '--closure-export-style','pilot',
                 '--baseline',str(baseline),
                 '--closure-dir',str(CLOSURE_DIR),
                 '--rq2-dir',str(rq2dir),
                 '--rq2-validation',str(validation),
                 '--output-dir',str(OUTPUT_DIR)]
        if is_2015:
            command+=['--pilot-b00',str(closure[0]),
                      '--pilot-validation',str(pilot_validation)]
        run=subprocess.run(command,text=True,capture_output=True)
        if run.stdout: print(run.stdout,flush=True)
        if run.stderr: print('VALIDATOR STDERR:\n'+run.stderr,flush=True)
        status='PASS' if run.returncode==0 else f'ERROR {run.returncode}'
        print('Result:',status,flush=True)
        results.append((interval,status))
    print('\n=== SUMMARY ===',flush=True)
    for interval,status in results:
        print(interval,status,flush=True)
    if any(status.startswith('ERROR') for _,status in results):
        sys.exit(1)


if __name__=='__main__':
    main()

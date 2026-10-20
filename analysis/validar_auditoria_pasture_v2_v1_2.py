#!/usr/bin/env python3
"""Valida somente a execução v1.2. Python >=3.10, sem dependências adicionais.
Uso: python3 validar_auditoria_pasture_v2_v1_2.py PASTA --mode smoke --product new
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re

FLAGS = ['code1', 'invalid100_after_nonpas', 'reused100_after_exit',
         'code100_without_confirmed_initial', 'code100_after_gap_only',
         'age100_outside_pas', 'age_positive_outside_pas', 'pasture_age_masked',
         'pasture_age_zero', 'unexpected_age_code', 'coverage_unknown_code',
         'has_pasture', 'has_code100', 'has_2xx', 'has_valid_coverage']
ASSETS = {
    'coverage_asset': 'projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3',
    'new_asset': 'projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_origin_age_v2',
    'old_asset': 'projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_pasture_age_v1'}
KNOWN = [3,4,5,6,7,9,11,12,13,15,19,20,21,23,24,25,29,30,31,32,33,
         35,36,39,40,41,46,47,48,49,50,62]
COMMON = ['script_version','mode','product','run_id','generated_at_utc',
          'coverage_asset','new_asset','old_asset','compared_age_asset','grid_asset',
          'year_start','year_end','crs','crs_transform','tile_scale',
          'max_pixels_per_region','partition_seed','partition_rule','known_coverage_codes_json']
DOMAIN = ['expected_grid_features','expected_full_grid_features','expected_batches',
          'expected_batch_counts_json']


def require(value, message):
    if not value:
        raise ValueError(message)


def integer(value, minimum=0):
    x = float(value)
    require(math.isfinite(x) and x.is_integer() and x >= minimum, f'Inteiro inválido: {value}')
    return int(x)


def read(path):
    with path.open(encoding='utf-8-sig',newline='') as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames and len(reader.fieldnames)==len(set(reader.fieldnames)), 'Colunas duplicadas/ausentes')
        rows = list(reader)
        require(rows and all(None not in r and None not in r.values() for r in rows), 'CSV vazio ou malformado')
        return rows


def validate(folder, mode='smoke', product='new', run=None):
    folder = Path(folder)
    pattern = re.compile(r'pasture_v2_mem12_(smoke|domain|points)_(new|old)_(\d{14})(?:_b(\d+))?\.csv')
    inventory = {}
    for path in folder.glob('*.csv'):
        match = pattern.fullmatch(path.name)
        # Retry files with (1) are not silently accepted as another valid export.
        if path.name.startswith(f'pasture_v2_mem12_{mode}_{product}_'):
            require(match is not None, f'Nome não reconhecido/duplicata: {path.name}')
        if match and match[1]==mode and match[2]==product:
            inventory.setdefault(match[3],[]).append((match[4],path))
    require(inventory, 'Nenhuma execução v1.2 correspondente; não usar CSVs v1/v1.1')
    run = run or max(inventory)
    require(run in inventory, 'Execução solicitada não encontrada')
    parts = sorted(inventory[run],key=lambda pair: pair[1].name)
    rows, hashes = [], {}
    for batch,path in parts:
        chunk = read(path)
        require((batch is None)==(mode=='points'), 'Nome de lote incompatível com o modo')
        if batch is not None:
            require(all(integer(r['audit_batch'])==int(batch) for r in chunk), 'Atribuição de lote divergente')
        rows.extend(chunk)
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    metadata = COMMON + (['expected_sample_points'] if mode=='points' else DOMAIN)
    for k in metadata:
        require(all(k in r and r[k]!='' for r in rows), 'Metadado ausente: '+k)
        require(len({r[k] for r in rows})==1, 'Execução/metadados misturados: '+k)
    first = rows[0]
    require(first['script_version']=='pasture-v2-targeted-audit-v1.2', 'Versão incorreta')
    require(first['mode']==mode and first['product']==product and first['run_id']==run, 'Identidade incorreta')
    require(re.sub(r'[^0-9]','',first['generated_at_utc'])[:14]==run, 'Horário/ID divergentes')
    require(all(first[k]==v for k,v in ASSETS.items()), 'Asset não corresponde à auditoria')
    require(first['compared_age_asset']==ASSETS[product+'_asset'], 'Produto incompatível')
    require(integer(first['year_start'])==1985 and integer(first['year_end'])==2025, 'Série incompleta')
    require(integer(first['tile_scale'])==16 and integer(first['max_pixels_per_region'])==1000000000, 'Parâmetros divergentes')
    require(integer(first['partition_seed'])==20261015 and
            first['partition_rule']=='seeded_system_index_uniform_floor_v1', 'Particionamento divergente')
    require(json.loads(first['known_coverage_codes_json'])==KNOWN, 'Lista de classes alterada')
    transform = json.loads(first['crs_transform'])
    require(len(transform)==6 and all(math.isfinite(x) for x in transform) and
            transform[0]>0 and transform[4]<0 and transform[1]==transform[3]==0, 'Transformação inválida')
    totals = None
    if mode=='points':
        require(len(parts)==1 and integer(first['expected_sample_points'])==100 and len(rows)==100, 'Amostra incompleta')
        require({r['sample_id'] for r in rows}=={f'MB1_{i:03}' for i in range(1,101)}, 'Pontos ausentes/duplicados')
        for r in rows:
            for stem in ['coverage',product+'_age']:
                for y in range(1985,2026):
                    x = float(r[f'{stem}_{y}'])
                    require(math.isfinite(x) and x.is_integer(), 'Histórico nulo/não inteiro')
    else:
        n = integer(first['expected_grid_features'],1)
        full = integer(first['expected_full_grid_features'],1)
        batches = integer(first['expected_batches'],1)
        counts = {int(k):integer(v,1) for k,v in json.loads(first['expected_batch_counts_json']).items()}
        require((mode=='smoke' and n==1 and batches==1) or
                (mode=='domain' and n==full and batches==8), 'Escopo/população divergente')
        require(set(counts).issubset(range(batches)) and sum(counts.values())==n, 'Contagem declarada inconsistente')
        require({int(b) for b,_ in parts}==set(counts) and len(parts)==len(counts), 'Lotes ausentes/duplicados')
        ids = [r['audit_id'] for r in rows]
        require(len(rows)==n and all(ids) and len(set(ids))==n, 'Células incompletas/duplicadas')
        for batch,count in counts.items():
            require(sum(integer(r['audit_batch'])==batch for r in rows)==count, 'Contagem de lote divergente')
        totals = {k:0 for k in FLAGS}
        for r in rows:
            flags = {k:integer(r[product+'_'+k]) for k in FLAGS}
            require(all(x in [0,1] for x in flags.values()), 'Indicador não binário')
            require(flags['reused100_after_exit']<=flags['invalid100_after_nonpas']<=flags['code100_without_confirmed_initial'],
                    'Subconjuntos temporais inconsistentes')
            require(flags['code100_after_gap_only']<=flags['code100_without_confirmed_initial'], 'Lacuna inconsistente')
            for k in FLAGS:
                totals[k] += flags[k]
    controls = []
    if totals is not None:
        controls = [k for k in ['pasture_age_masked','pasture_age_zero','unexpected_age_code',
                    'coverage_unknown_code','age100_outside_pas','age_positive_outside_pas',
                    'code100_without_confirmed_initial','code100_after_gap_only'] if totals[k]>0]
        if totals['has_valid_coverage']!=len(rows):
            controls.append('celulas_sem_cobertura_valida')
        if totals['has_pasture']==0:
            controls.append('nenhuma_pastagem_no_escopo')
    def verdict(key):
        if totals[key]>0:
            return 'PRESENTE_NO_ESCOPO'
        if mode=='smoke':
            return 'NAO_DETECTADO_NA_UNICA_CELULA_TESTE'
        return 'NAO_DETECTADO_COM_PENDENCIAS' if controls else 'NAO_DETECTADO_NO_DOMINIO_COMPLETO'
    report = {'status':'PASS','run':run,'mode':mode,'product':product,'rows_validated':len(rows),
              'grid_asset':first['grid_asset'],'input_sha256':hashes,'pending_controls':controls,
              'affected_cells':totals,'unit':'células com ocorrência, não pixels ou hectares',
              'full_domain_complete_for_this_product':mode=='domain',
              'executed_script_sha256':None,'native_execution_independently_observed':False,
              'limitation':'Um smoke PASS confirma apenas exportação e integridade de uma célula; não ausência no domínio.'}
    if totals is not None:
        report['verdicts'] = {k:verdict(k) for k in ['code1','invalid100_after_nonpas','reused100_after_exit']}
    output = folder/f'pasture_v2_mem12_{mode}_{product}_{run}_validation.json'
    data = (json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    require(not output.exists() or output.read_bytes()==data, 'Recusa de sobrescrever validação diferente')
    if not output.exists():
        output.write_bytes(data)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder')
    p.add_argument('--mode',choices=['smoke','domain','points'],default='smoke')
    p.add_argument('--product',choices=['new','old'],default='new')
    p.add_argument('--run')
    args=p.parse_args()
    try:
        print(json.dumps(validate(args.folder,args.mode,args.product,args.run),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as error:
        p.exit(1,f'AUDITORIA INCONCLUSIVA: {error}\n')

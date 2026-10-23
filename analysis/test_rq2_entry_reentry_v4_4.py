"""Focused denominator, evidence-preservation and event-history regressions."""
from pathlib import Path
import copy,importlib.util,unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rq2_audit',ROOT/'analysis/20i_validate_rq2_entry_reentry_v4_4.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class Tests(unittest.TestCase):
 def test_ratio_of_summed_areas_not_mean_cell_ratios(self):
  # Cells with 1/1 and 0/99: aggregate is 1%, unweighted mean is 50%.
  v.check_ratio('.01',1,100)
  with self.assertRaises(ValueError):v.check_ratio('.5',1,100)
 def test_undefined_baseline_is_blank(self):
  v.check_ratio('',0,0)
  with self.assertRaises(ValueError):v.check_ratio('0',0,0)
 def test_positive_denominator_with_no_reentry_is_zero(self):
  v.check_ratio('0',0,10)
  with self.assertRaises(ValueError):v.check_ratio('',0,10)
 def matrix(self):
  fields,old=v.read(ROOT/'outputs/summary/rq2_relative_conversion_v1/canonical_integrated_evidence_matrix_v4_3.csv')
  _,new=v.read(ROOT/'outputs/summary/rq2_entry_reentry_v4_4/canonical_integrated_evidence_matrix_v4_4.csv');return fields,old,new
 def test_only_two_supplemented_findings(self):
  f,o,n=self.matrix();self.assertEqual(v.check_matrix_rows(f,o,n),['P9A035','P9A036'])
 def test_other_finding_cannot_change(self):
  f,o,n=self.matrix();n[0]['main_result']+=' altered'
  with self.assertRaises(ValueError):v.check_matrix_rows(f,o,n)
 def test_canonical_anchor_cannot_change(self):
  f,o,n=self.matrix();next(x for x in n if x['finding_id']=='P9A035')['source_sha256']='0'*64
  with self.assertRaises(ValueError):v.check_matrix_rows(f,o,n)
 def test_qualified_status_cannot_be_promoted(self):
  f,o,n=self.matrix();next(x for x in n if x['finding_id']=='P9A036')['evidence_status']='supported'
  with self.assertRaises(ValueError):v.check_matrix_rows(f,o,n)
 def test_causal_flag_cannot_be_promoted(self):
  f,o,n=self.matrix();next(x for x in n if x['finding_id']=='P9A036')['causal_claim_flag']='1'
  with self.assertRaises(ValueError):v.check_matrix_rows(f,o,n)
 def test_historical_events_exact_prefix(self):
  a=(ROOT/'outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv').read_bytes();b=(ROOT/'outputs/validation/rq2_entry_reentry_v4_4/canonical_evidence_status_events_v6.csv').read_bytes();v.check_event_bytes(a,b)
  with self.assertRaises(ValueError):v.check_event_bytes(a,b.replace(b'suspended',b'cleared',1))
 def test_no_duplicate_new_event_ids(self):
  a=(ROOT/'outputs/validation/rq2_relative_conversion_v1/canonical_evidence_status_events_v5.csv').read_bytes();b=(ROOT/'outputs/validation/rq2_entry_reentry_v4_4/canonical_evidence_status_events_v6.csv').read_bytes()
  b=b.replace(b'P9A036-ENTRY-REENTRY-20261023',b'P9A035-ENTRY-REENTRY-20261023')
  with self.assertRaises(ValueError):v.check_event_bytes(a,b)

if __name__=='__main__':unittest.main()

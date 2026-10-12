# Operator execution-text addendum

Status: tool prepared; **no operator attestation supplied or recorded by this update**. Accepted full validation and its null executed-script field remain byte-identical.

Save the exact script text used in the completed Code Editor run, preserving its bytes. A current copied template alone is not evidence of the historical text. If the operator can attest that this was the text used, create a separate addendum:

```bash
python analysis/18j_record_operator_execution_addendum_v1.py   --executed-script /PATH/actual_executed_text.js   --accepted-validation outputs/validation/window_origin_sensitivity_v1/full/canonical_window_origin_sensitivity_validation_v1.json   --operator-name 'Mario Barroso Ramos Neto'   --gee-script-path 'ACTUAL_GEE_REPOSITORY_PATH'   --operator-attests-exact-text-used   --addendum-id window_full_operator_attestation_001   --output-dir execution_addenda
```

Execution date and repository commit may be supplied if known; they are operator statements. The tool records the text hash, a content-addressed snapshot, the original validation hash and whether the text bytes match the supplied snapshot. It never edits the old validation. If hashes differ, the addendum records the difference and requires review/revalidation; it does not silently validate a changed script. A recorded operator attestation is still not independent service verification.

If the actual historical text cannot be established, keep the provenance gap explicit. For future executions, capture the exact source/constant snapshots before the run and retain them with task/export records.

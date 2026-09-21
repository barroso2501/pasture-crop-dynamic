# Phase 9A preflight

- **Script version:** `phase9a-integrated-evidence-matrix-v1`
- **Expected claims:** 30
- **Expected authenticated sources:** 16
- **Expected research questions:** 5
- **Expected explicit evidence gaps:** 2, for RQ1 and RQ2

## Static checks

- Python syntax and imports pass.
- The 16 packaged source hashes match the frozen source manifest.
- The claim schema has 19 required fields and unique `P9A###` identifiers.
- Every claim points to one authenticated source.
- Every controlled field contains only declared values.
- No row is marked as causal.

## Expected execution message

```text
CANONICAL INTEGRATED EVIDENCE MATRIX — PHASE 9A VERSION 1
CURATED CLAIMS; AUTHENTICATED SOURCES; NO NEW INFERENCE
...
PHASE 9A EVIDENCE MATRIX COMPLETE — VALIDATION PASS
Evidence statements: 30
Authenticated sources: 16
Explicit evidence gaps: 2 (RQ1 and RQ2)
```

Successful execution means that the accepted evidence registry is internally
consistent and traceable. It does not close the two evidence gaps and does not
complete Phase 9B or 9C.

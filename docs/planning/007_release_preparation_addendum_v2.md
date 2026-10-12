# Plan 007 — partial known-product release preparation v2

Date: 2026-10-12. **Status: partial inventory and verification tool prepared; complete Stage 0 and DOI deposit remain pending.** This adds the accepted window sensitivity and new endpoint-fraction derivative to the known Decision 024 dependencies. It does not replace the full Phase1–9 product audit or its release/claim-allocation criteria.

The portable `config/public_release_known_products_v2.csv` contains 86 known objects: the original eight full-v3 cell CSVs and three corrected v2 Parquets, 61 window-sensitivity data/provenance objects, and 14 current fraction/interpretation/code support objects. Each object has a source root, relative input path, proposed public path, exact expected hash, optional row count and explicit hash basis. The 83 objects available locally were checked against exact bytes and expected rows. Three Parquets remain unavailable in this workspace; their expected hashes are inherited from accepted validation, not newly verified. Two searches of the connected Drive, exact and broader names, returned no matching Parquet objects; this is not evidence that they do not exist elsewhere.

Missing exact bytes:

| Product | Expected SHA-256 |
| --- | --- |
| `canonical_stock_flow_panel_1985_2025_v2.parquet` | `ef3589be99e3a2cdc1c2245a15cedd090c8255775b34f14d4f2f27d3f9f8faa7` |
| `canonical_stock_flow_derived_metrics_1985_2025_v2.parquet` | `e4a17ba21640704e2f7db7a9885417a403b842910624f36f7f9da34bfd67a9c2` |
| `canonical_integrated_stock_flow_trajectory_1985_2025_v2.parquet` | `06127aac2f67a34ed79118f666a9c00063e28f32f16a046901370c0336b98499` |

Expected rows are 199,112 each. The verifier checks exact bytes first and Parquet metadata rows when files and pyarrow are available. A mismatch is not replaced by a hash of whichever current file happens to be present. Missing/failed objects remain explicit; the report never declares a complete DOI release ready.

## Portable verification

Place data under the existing project-relative `panel/`, `analysis/` and `spatial/` paths, or supply an equivalent portable staging root. Repository objects are resolved against `--repo-root`. The earlier external window-data ZIP supplies the sensitivity `spatial/` tree; the eight closure CSVs and three Parquets are separate dependencies.

```bash
python analysis/18l_verify_known_release_files_v2.py \
  --data-root /PATH/Contabilidade \
  --output-json release_checks_after_parquet_delivery.json
```

Install `analysis/requirements_release_verification_v2.txt` for Parquet metadata checks. Exit code 2 means missing/failed checks, with the detailed JSON preserved. Exit code 0 means only the known listed bytes/rows pass, not that full release scope or DOI is complete. Repeated runs require new report names.

Current report: `outputs/validation/release_preparation_v2/known_release_file_byte_checks_v1.json`: 83 verified, three missing, `release_ready=false`, `doi_assigned=false`.

## Remaining release work

Obtain the exact three Parquets and finish the full Stage 0 product/claim/figure inventory for all accepted phases; confirm release tiers and exact v1.0.0 scope. Complete dictionaries, licenses, creator/credit metadata and portable reuse examples; reconcile all manuscript claims to the deposited version. Then assemble the release candidate, verify it in a fresh environment and deposit with a persistent DOI. Optional unexecuted GEE extensions should be included only if their results are used in that manuscript/release. No author list, license, DOI or successful public deposition was invented by this preparation.

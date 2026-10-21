# Uncertain-pair cross-tab: native pilot acceptance v1

**2026-10-15: pilot PASS. Full-domain execution PENDING.** This is technical acceptance of the supplied native pilot exports on two canonical cells, not closure of the domain-wide uncertain-pair question. Matrix v4.3 and cumulative events-v5 remain unchanged.

## Material and checks

Received `drive-download-20261015T195023Z-1-001.zip` with exactly the three expected CSVs. Original CSV bytes are preserved under `outputs/native/uncertain_pair_crosstab_v1/pilot/`. The unchanged supplied `analysis/19b_validate_uncertain_pair_crosstab_v1.py` produced the accepted machine report and five derived CSVs under `outputs/validation/uncertain_pair_crosstab_v1/pilot/`.

| Check | Observed result |
|---|---|
| Canonical cells | GH-123 / 18081 / batch 1; IK-77 / 32173 / batch 5 |
| Annual pairs | 2023→2024 and 2024→2025; both diagnostic |
| Actual cell/pair inventory | 4 rows; complete, unique and correctly assigned |
| Runtime configuration | Assets, classes, constants and 41 coverage bands match |
| Native projections | All three years match the canonical CRS and six transform coefficients |
| Native synthetic cases | 34 complete cases, each with positive reduction support and all six error fields zero |
| Actual raster audit counters | 12 values checked; all zero |
| Area identities | All per-cell and aggregate identities pass preregistered tolerances |
| Observed uncertain area | 0 ha in each of the four actual cell/pair rows |

The native synthetic cases include all 25 observation-state combinations, valid coverage code 1, unexpected codes, and masking precedence. Thus the invalid categories were exercised natively even though neither actual pilot cell contains uncertain pairs. Pixel support of the synthetic rectangle is reduction-weighted and need not be an integer.

## Interpretation and continuation

Zero uncertainty in these two cells does not estimate its prevalence in the 24,889-cell domain, or demonstrate that the historical ~4.69 Mha rarely overlaps PAS. No new scientific claim about its composition is accepted. Full execution must supply the complete cell inventory, zero raster audit counters and national totals reproducing the accepted boundary summary within 0.001 ha. No full-domain boundary comparison has been made at this pilot stage.

Proceed with the **unchanged** `gee/19a_export_uncertain_pair_crosstab_full_v1.js`. Its classification engine is identical to the accepted pilot. Expected exports are eight cell batches and one full manifest. Preserve and reuse the exact accepted pilot native CSV and validation JSON. See `RUN_UNCERTAIN_PAIRS_FULL_PT.md`.

The acceptance report records the supplied code snapshot hash, input/output hashes and runtime metadata. The executed-text hash remains null because no operator attestation was supplied. Validation is of operator-provided exports and does not independently authenticate remote execution. Entry/re-entry chronology, auxiliary numerical-age 201, an independent boundary-raster comparison and public DOI deposition retain their previous scope/status.

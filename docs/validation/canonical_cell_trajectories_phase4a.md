# Canonical cell trajectories Phase 4A validation

- **Status:** Accepted computational production and reviewed supplementary GIS consistency checks.
- **Date accepted:** 2026-09-15.
- **Run:** `run_20260915T091255_865443Z`.
- **Completed UTC:** `2026-09-15T09:14:52.362638+00:00`.
- **Script version:** `phase4a-cell-trajectories-v2`.
- **Executed script:** `09a_build_cell_state_trajectories_v2.py`.
- **Script SHA-256:** `8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec`.
- **Design:** Decisions 009 and 010.

## Acceptance and scope

Phase 4A's temporal products are accepted following review of the actual Colab
execution record, inventory, frozen specifications, adjacent transition tables,
pattern counts and four cell-level GIS summaries. This acceptance closes the
computational construction of temporal sequences and episodes. Interpretation,
figure selection and analysis of spatial relocation remain separate work; no
Moran/LISA or spatial-relocation result is asserted.

All 12 metrics received descriptive sequences, episodes, stage occupancy and
transitions in both temporal windows. Decision 010's substantive typology was
applied only to the C–R balance and NAT–TMP endpoint magnitude axes. The other
ten metrics retain `not_classified` and `typology_applied = False`.

The full observed window includes 2020–2025, visibly and structurally flagged
as diagnostic. It neither contributes to fitted class thresholds nor overwrites
the primary 1985–2020 reconstruction.

## Provenance

Output directory in the user's project:

```text
/content/drive/MyDrive/Trabalho/Contabilidade/spatial/phase4/trajectories_v1/run_20260915T091255_865443Z
```

The uploaded `latest_successful_run_v1.json` identifies this same run. Its
validation hash exactly matches the JSON received in the compact output ZIP:

```text
54e3ab5600abaa268c642b67ed50d99fa9e81546fff875cef3266801e1a33b7e
```

The executed script hash matches the delivered revision 2. Required upstream
identities in the production record match the accepted pins. The classified
panel is authenticated against the Phase 3B output record by the script.

| Input | SHA-256 |
|---|---|
| `canonical_spatial_metrics_panel_v1.parquet` | `8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c` |
| `canonical_spatial_metrics_validation_v1.json` | `9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8` |
| `canonical_map_classes_validation_v2.json` | `cb909c77372c34947d670342db233a51e07f31996a4bb8085947f973937f7343` |
| `canonical_comparable_map_class_counts_v2.csv` | `1740b1fa90d47a2031202426efb0973a02ea93a8e94f20a00323e382fe54a908` |
| `canonical_spatial_map_classes_v1.parquet` | `f0860bd2aff2c5bf6f6020bcd5022c86180311229191f58a1ed9600809d12bc3` |
| `canonical_comparable_maps_validation_v1.json` | `c7e8a3d4df68615d058b1e1935fe1bd57a8a22884920b61853bf1acca9d769cc` |


## Production structure

| Product | Actual count |
|---|---:|
| Canonical cells | 24,889 |
| Descriptive metrics | 12 |
| Typology axes | 2 |
| Windows per metric | 2 |
| Combined interval-stage records | 4,480,020 |
| Combined cell-window-metric summaries | 597,336 |
| Episode records | 1,515,075 |
| Cell-window-stage occupancy records | 1,135,618 |
| Primary adjacent transition events | 1,792,008 |
| Full observed adjacent transition events | 2,090,676 |
| Inventory records | 117 |
| Transition CSV records, including zero-count pairs | 3,796 |
| Core pattern-count records | 22 |
| GIS CSVs | 4 |
| Rows per GIS CSV | 24,889 |
| Columns per GIS CSV | 42 |

Episode and occupancy counts depend on the observed sequences, not fixed
population expectations. The transition table's 3,796 rows are aggregated
stage pairs; their event sums reconcile with the larger totals above.

## Execution checks and independent review

All 13 checks in the actual production validation JSON are true. They cover
input authentication, upstream acceptance, balanced keys, reproduction of all
504 frozen class counts, complete support on the two core axes, episode
expansion, duration and occupancy partitions, boundary/reentry consistency,
primary restriction, diagnostic comparison, transition marginals, GIS join
cardinality and output authentication.

The following were independently checked from the received files:

- Both uploaded ZIP archives passed CRC integrity checking.
- Hashes of the received compact outputs, the four GIS CSVs and `schema.ini`
  match the production JSON. The pointer matches the validation JSON hash.
- All 117 inventory entries have unique relative paths and reconcile with
  the dimensions and hashes recorded in the JSON. Summed inventory row counts
  reproduce the reported interval, trajectory, episode and occupancy totals.
- Every metric/window/adjacent-period transition sum is 24,889. Source
  counts and normalized fractions reconcile; target and source marginals
  match accepted Phase 3A class populations in every interval.
- The six overlapping transition pairs are identical between primary and
  full observed outputs. Only the added pair reaches diagnostic 2020–2025.
- All 12 numeric class specifications match the authenticated full-precision
  Phase 3A JSON exactly. No rounded display threshold was used to refit them.
- Core pattern counts sum to 24,889 for each axis and temporal window.
- The four GIS summaries have unique cell IDs, complete core support and the
  expected metric/window identities.

Full episode Parquets were not independently reread in this review. Their
cell-level partition/expansion checks were performed by the accepted script;
their dimensions and recorded identities were reconciled through the inventory.
This distinguishes actual file inspection from checks reported by execution.

## Supplementary constancy equivalence check

The two redundant constancy outputs were independently compared cell by cell
on both complete-support core axes and both windows:

```text
trajectory_pattern_code == 'constant'
    ⇔ trajectory_constant_flag == 1
    ⇔ episode_count == 1
```

Across 99,556 GIS records there were zero mismatches. This equivalence is scoped
to `typology_applied = True` with complete substantive support. A descriptive
metric can have a constant flag while its pattern remains `not_classified`;
that is expected, not inconsistency.

| GIS CSV | Rows | Constant cells | Equivalence mismatches | no_change with activity-change pattern |
|---|---:|---:|---:|---:|
| `nat_tmp_endpoint_magnitude_primary_v1.csv` | 24,889 | 11,581 | 0 | 0 |
| `cr_balance_primary_v1.csv` | 24,889 | 12,596 | 0 | 2,531 |
| `nat_tmp_endpoint_magnitude_full_observed_v1.csv` | 24,889 | 10,823 | 0 | 0 |
| `cr_balance_full_observed_v1.csv` | 24,889 | 11,587 | 0 | 2,661 |


## Reachability of no_change

`ordinal_direction = no_change` is reachable in the activity-change pattern,
not merely in constant or returning trajectories. Repeated observations within
one active episode supply two or more eligible equal ranks without creating
stage reentry. For example, the primary sequence `I,I,C,C,C,C,C` has two
episodes, no reentry and an unchanged active rank; its pattern is
`activity_change_without_ordinal_change`.

This combination was observed in 2,531 primary and 2,661 full C–R records.
The same pattern additionally contains 427 primary and 617 full records with
`insufficient_ordinal_support`. In returning or recurrent trajectories, the
reentry rules take precedence over ordinal direction, as designed.

These are supplementary validation findings, not changes to Decision 010 or
its decision order. Future implementation revisions should preserve and
explicitly verify constancy equivalence and these precedence/reachability cases.

## Pattern counts as validated descriptive outputs

| Pattern | C–R primary | C–R full | NAT–TMP primary | NAT–TMP full |
|---|---:|---:|---:|---:|
| constant | 12596 | 11587 | 11581 | 10823 |
| monotonic_without_return | 3851 | 1978 | 3763 | 3022 |
| nonmonotonic_without_return | 318 | 368 | 684 | 670 |
| returning | 3074 | 4529 | 4613 | 4803 |
| recurrent | 2092 | 3149 | 4248 | 5571 |
| activity_change_without_ordinal_change | 2958 | 3278 | 0 | 0 |


Each column totals 24,889. Constant activity magnitude can include constant
zero; constant balance can include inactivity. These are not automatically
persistent agricultural expansion. Differences between the two windows reflect
the appended diagnostic observation and must be interpreted with its flag.

## Script correction and verification history

Revision 1 failed while reproducing relative-intensity classes because its
Parquet column projection omitted three rate-support fields. Revision 2 derives
those fields from the authenticated frozen specifications. This correction did
not change stages, thresholds, typology or upstream accounting and did not
require reprocessing previous phases.

Local revision-2 verification covered 2,048 sequences, meaningful boundary,
interruption, precision and recurrence cases, synthetic output round-trips and
the complete input-loader path. The production JSON's nested
`sequence_engine_verification.canonical_input_execution = false` describes the
synthetic engine self-check only. It does not negate the actual canonical run,
which is evidenced separately by its production structure, authenticated inputs
and outputs. Likewise, the production engine check does not repeat the local
integration-output test, hence its nested round-trip flag is false.

## Compact evidence identities

| Compact evidence | SHA-256 |
|---|---|
| `canonical_phase4_frozen_class_specifications_v1.csv` | `675b9047bf04f248da4e6014724fdaf0ae2e047a266c9f6a55c31cff1315e7ad` |
| `canonical_cell_trajectories_validation_v1.json` | `54e3ab5600abaa268c642b67ed50d99fa9e81546fff875cef3266801e1a33b7e` |
| `canonical_core_trajectory_pattern_counts_v1.csv` | `50e6580c2b85dcc7ef2a6a364d582d352d99a49d2fb3e06dc583fcf21acaec87` |
| `canonical_cell_trajectories_inventory_v1.csv` | `8a9344334d431eb6dfbfed2777e732e75e9c85521de0766d6221587234886908` |
| `canonical_cell_state_transition_matrices_v1.csv` | `984946e0d5f25160a3ea87b34db2a4da8ec7e47e016db375d7ead66390656871` |


The four GIS CSV and schema identities remain in the production JSON and
inventory. The JSON is preserved unchanged; this supplementary Markdown review
does not edit the original execution record or add fictional runtime checks.

## Repository implementation reconciliation

The accepted production run used revision 2 with SHA-256
`8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec`.
That revision contains `required_metric_columns()` and explicitly loads
`consolidation_rate_defined`, `replenishment_rate_defined` and
`nat_tmp_intensity_defined`. The production output provenance is therefore
unambiguous and no rate-metric rerun is required.

Revision 3 has SHA-256
`ed2ded69036cb460fb659e16aaeb9fda3456b557e91b6cd7cb6c53a5944fa58e`.
Relative to revision 2, it changes only the version/banner and removes
`CharacterSet=65001` from future `schema.ini` generation. It is the current
canonical repository implementation but is not retroactively claimed as the
executed production script.

## Diagnostic-extension pattern sensitivity

For the C–R axis, `returning + recurrent` increases from 5,166 cells (20.76%)
in the seven-interval primary window to 7,678 (30.85%) in the eight-interval
full window. The increase consists of 2,512 cells newly entering the union:

| Primary pattern | Full pattern | Cells |
|---|---|---:|
| `monotonic_without_return` | `returning` | 2,052 |
| `activity_change_without_ordinal_change` | `returning` | 233 |
| `nonmonotonic_without_return` | `returning` | 227 |

All 2,512 change state in 2020–2025. Across the full population, 4,460 cells
gain exactly one stage reentry: 1,057 move from `returning` to `recurrent`, 891
remain `recurrent` with an additional reentry, and the 2,512 above cross from
no reentry to `returning`. Of the newly returning cells, 1,859 (74.0%) end the
diagnostic interval in replenishment dominance.

This is a window-extension sensitivity result, not evidence that historical
recurrence nearly doubled. Appending a diagnostic state creates one additional
opportunity for reentry, and the 2020–2025 balance frequently reintroduces
replenishment after the terminal primary state.

## Software and subsequent work

- Python: 3.13.15.
- pandas: 2.2.3.
- NumPy: 2.1.3.
- PyArrow: 23.0.1.

No canonical rerun is required for this acceptance. Phase 4 exploration and
synthesis were subsequently completed, followed by accepted Global Moran and
Local Moran/LISA analyses in Phases 5 and 6. GitHub synchronization itself is
not asserted by this record.

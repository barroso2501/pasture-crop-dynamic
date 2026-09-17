# GitHub audit reconciliation — 2026-09-17

## Scope

This record reconciles the repository with the accepted analytical history
through Phase 6 and the start of Phase 7. It corrects missing files, stale
documentation and an ambiguous canonical script path. It does not change any
accepted numerical result or claim a new analytical execution.

## Phase 4A script provenance

The initial revision of `09a_build_cell_state_trajectories.py` omitted three
support fields from its projected Parquet read and failed with a `KeyError`.
Revision 2 corrected the loader by deriving required columns from the
authenticated class specifications.

The accepted production record is unambiguous:

| Item | Value |
|---|---|
| Run | `run_20260915T091255_865443Z` |
| Executed file | `09a_build_cell_state_trajectories_v2.py` |
| Version | `phase4a-cell-trajectories-v2` |
| Script SHA-256 | `8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec` |
| Validation status | PASS |

Revision 3 retains the complete revision-2 analytical code and changes only:

- the internal version string;
- the Console revision banner;
- removal of the invalid `CharacterSet=65001` schema option.

Revision 3 SHA-256 is
`ed2ded69036cb460fb659e16aaeb9fda3456b557e91b6cd7cb6c53a5944fa58e`.
It is installed by this package at the unsuffixed canonical repository path.
No Phase 4A rerun is required.

## Missing artifacts restored

- `gee/04b_reprocess_nat_tmp_trajectory_remaining_intervals.js`, SHA-256
  `b5a1ced8823ae857025ba52a86ccf79712beb632e3fae2d535cace95ccee793c`;
- `docs/analysis/high_nat_tmp_spatial_exploration_v1.md`, the initial report
  underlying the high-magnitude cohort exploration.

## Documentation corrections

- the investigation plan now records Phases 4–6 as complete and Phase 7 as in
  production;
- the Phase 4 closure report links to the restored exploration report;
- the Phase 4A method distinguishes executed revision 2 from current revision
  3;
- the Phase 4A validation records the diagnostic-window explanation for the
  increase in `returning + recurrent` trajectories;
- the temporal-synthesis method identifies its implementation script;
- the two legacy output references now include the physical `docs/` prefix;
- the purpose and validation of `analysis/05_temporal_characterization.py` are
  now documented.

## Diagnostic extension finding

The C–R `returning + recurrent` count increases from 5,166 in the primary
window to 7,678 in the full window. The 2,512 newly included cells all change
state in 2020–2025. The increase is interpreted as sensitivity to appending a
diagnostic observation and its additional opportunity for reentry, not as a
doubling of historical recurrence.

## Acceptance statement

This reconciliation is documentary and repository-facing. It requires no GEE,
Colab, Phase 4 rerun, class refit, Moran recomputation or change to accepted
output hashes.


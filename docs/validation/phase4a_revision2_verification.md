# Phase 4A script revision 2 verification

- **Date:** 2026-09-15.
- **Script:** `09a_build_cell_state_trajectories_v2.py`.
- **Version:** `phase4a-cell-trajectories-v2`.
- **SHA-256:** `8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec`.
- **Status:** Local regression verification PASS, followed by canonical production PASS in run `run_20260915T091255_865443Z`.

## Correction

Revision 1 projected the Phase 2 Parquet onto a subset of columns that omitted
`consolidation_rate_defined`, `replenishment_rate_defined` and
`nat_tmp_intensity_defined`. Reproducing the relative-intensity classes then
raised a KeyError. This was a script input-projection defect, not an upstream
accounting failure.

Revision 2 derives required support columns from the authenticated frozen class
specifications. Trajectory-share support expressions use their explicitly
declared fields. No stage, tolerance, class limit, typology or output population
is changed. Output product paths remain under `trajectories_v1`; execution
records identify script revision 2.

## Verification

- All 2,048 sequence-engine checks and the synthetic output round-trip passed.
- The three relative-intensity support fields were verified in the projected
  Parquet read and their undefined/zero/positive classes reproduced.
- The complete input-loader path passed on a six-cell, eight-interval synthetic
  fixture using all 12 frozen specifications and 504 count records. Synthetic
  hashes and population expectations were set only in that isolated test;
  the delivered script retains its canonical production pins.

These checks preceded the canonical run. Production subsequently completed
with the same revision-2 bytes and recorded script SHA-256
`8500ad7e08bf21d972a660449e9a635ee1c3c92947fc9a3ce1fd3d42a2d386ec`.
The production validation and inventory were independently reviewed. No
upstream phase requires reprocessing for this correction.

```python
%run /content/09a_build_cell_state_trajectories_v2.py
```

Revision 3 later removed the invalid `CharacterSet=65001` line from future GIS
schema generation. It did not change stages, metrics, sequences or numerical
outputs. The canonical repository path may therefore contain revision 3 while
this record and the production JSON continue to identify the executed
revision-2 bytes exactly.

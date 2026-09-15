# Cell state trajectories and multiquinquennial episodes

- **Design:** Decision 010, accepted 2026-09-15, extending Decision 009.
- **Implementation:** `analysis/09a_build_cell_state_trajectories.py` (accepted revision 2; executed in Colab as `09a_build_cell_state_trajectories_v2.py`).
- **Script version:** `phase4a-cell-trajectories-v2`.
- **Production status:** Canonical temporal production accepted on 2026-09-15; interpretation pending.

## Purpose and scope

The script reconstructs temporal sequences and maximal equal-stage episodes for
all 12 accepted Phase 3 metrics. It applies the Decision 010 trajectory typology
only to the two defined axes: C–R balance and NAT–TMP endpoint magnitude.
The other ten metrics receive descriptive sequences, episodes, occupancy and
transitions; `trajectory_pattern_code = not_classified` and
`typology_applied = False` prevent an undocumented substantive classification.
Occurrence and ordinal descriptors on these ten metrics are not configured and
remain null or `not_configured`.

This is Phase 4A temporal processing. It does not run GEE, Moran/LISA or geometry
operations, establish causality, or by itself demonstrate spatial relocation.

## Inputs and provenance

Required files relative to the project directory:

| Path | Role |
|---|---|
| `spatial/phase2/canonical_spatial_metrics_panel_v1.parquet` | Continuous metrics and context |
| `spatial/phase2/canonical_spatial_metrics_validation_v1.json` | Accepted Phase 2 validation |
| `spatial/phase3/canonical_spatial_map_classes_v1.parquet` | Frozen cell-interval stages |
| `spatial/phase3/canonical_comparable_maps_validation_v1.json` | Phase 3B provenance and classified-panel output hash |
| `spatial/phase3/canonical_map_classes_validation_v2.json` | Authenticated full-precision limits |
| `spatial/phase3/canonical_comparable_map_class_counts_v2.csv` | All 504 accepted class counts |

Known upstream hashes are pinned to those used in accepted 08b/08c scripts.
The classified-panel hash is verified against the Phase 3B output record, whose
relevant input hashes must also agree with the pinned upstream identities.
Each prior validation must have nonempty checks containing only `True` and
status `PASS`. All 12 class fields are reproduced with the frozen rules and
compared cell by cell; the 504 accepted counts must match exactly. No empirical
limit is recalculated. The rounded limit CSV is not a numeric input.

`cell_id`, `t0`, `t1` must form unique, equal, balanced keys in both panels.
All 24,889 cells must have the eight expected intervals. Missing or invalid
values in the complete-support core axes fail acceptance; they are not
inactivity or zero. Legitimate undefined/support classes of other metrics are
retained verbatim in sequences, episodes and labeled transitions.

## Axes, windows and stage rules

The C–R axis preserves `inactive`, `replenishment_dominant`, `mixed` and
`consolidation_dominant`. Inactivity uses gross flow no greater than `1e-9` ha.
Active index values exactly at −1/3 or +1/3 belong to `mixed`.

The magnitude axis preserves the actual upstream vocabulary: `zero`,
`positive_low`, `positive_moderate`, `positive_high`. These are the low,
moderate and high classes referenced in Decision 010. Magnitude zero uses the
frozen upstream `1e-9`-ha tolerance. Class-boundary ties use full-precision
limits. Share-support thresholds do not exclude small absolute endpoint flows.

Both axes and all descriptive metrics are reconstructed for `primary` (seven
intervals, 1985–2020) and `full_observed` (eight, 1985–2025). The latter includes
2020–2025 with its diagnostic flag. Both patterns and all duration/transition
results are kept rather than overwritten.

## Episodes and temporal coverage

One episode is a maximal run of consecutive identical interval stages. The
script verifies that expansion recovers the source sequence. Episode durations
partition every window and equal the sum of interval spans; in the present
panel this is five times the interval count. Duration describes coverage of
quinquennial assignments, not proof of uninterrupted annual activity or pixel
use. Boundary flags identify unknown continuation beyond each observed window;
window-edge occupancy is not an observed process entry or exit.

A persistent episode spans at least two intervals. Whole-window constancy is a
separate trajectory flag. A sole episode touches both boundaries. Independent
isolation flags distinguish a one-interval interior excursion, isolated
activity and isolated inactivity. Examples such as `R→I→R` have an isolated
inactivity episode when I lasts one interval.

## Trajectory descriptors and patterns

`stage_reentry_count` counts each episode whose stage has appeared before,
once per episode. It is also independently verified as episode count minus
number of distinct stages and reconciled with stage-specific counts in local
engine verification.

C–R ranks are −1, 0, +1 for the active states; inactivity has no rank.
`ordinal_direction` and `direction_change_count` describe the ordered eligible
path after zero differences are removed. Off-axis counts and a bridging flag
identify interruptions. `direct_direction_change_count` considers only
contiguous eligible blocks. Endpoint magnitude ranks include zero.

Adjacent 0→1 and 1→0 occurrence changes count observed activity entries and
exits. Interior inactive runs bracketed by activity count interruptions and
their resumptions. Unknown support is not zero and is not bridged into a
fabricated event. Direct and mediated dominance reversals compare successive
C–R dominant episodes, distinguishing adjacency from intervening mixed or
inactive episodes.

The Decision 010 ordered pattern rules yield `constant`, `returning`,
`recurrent`, `nonmonotonic_without_return`, `monotonic_without_return`, or
`activity_change_without_ordinal_change` on the two complete-support axes.
`repeated_two_state_alternation_flag` requires exactly two distinct episode
stages and at least four episodes. Recurrence does not automatically imply
strict alternation. Descriptive metrics do not acquire this substantive
pattern classification.

The primary/full comparison retains both sequences and patterns, their changes,
terminal-episode continuation and deltas in episode count, maximum duration,
reentries and occurrence descriptors. An appended diagnostic interval either
extends the terminal episode by one or creates exactly one new episode.

## Output organization

Outputs are staged locally and copied to an isolated run directory:

```text
spatial/phase4/trajectories_v1/run_<UTC timestamp>/
```

A successful copy is verified by hash. A failed copy produces `FAIL`, and a
copy in progress carries `COPYING`, preventing a partial folder from appearing
as an accepted run. `latest_successful_run_v1.json`, in the parent folder,
points to the most recent successfully written run. A computational `PASS`
still requires review before the scientific production stage is accepted.

Each metric has the following products in `tables/<metric>/<window>/`:

| File | Content |
|---|---|
| `interval_stages.parquet` | One row per cell/interval with continuous values and context |
| `cell_trajectories.parquet` | One row per cell with original sequence, episodes and descriptors |
| `episodes.parquet` | One row per maximal consecutive-stage run |
| `stage_occupancy.parquet` | One row per observed cell/stage with recurrence and duration |

`tables/<metric>/primary_full_comparison.parquet` preserves both window
summaries. Root-level products are:

- `canonical_cell_state_transition_matrices_v1.csv`: counts and source-normalized fractions by adjacent interval pair; support classes are labeled.
- `canonical_cell_primary_full_comparison_v1.parquet`: compact comparisons for all metrics.
- `canonical_core_trajectory_pattern_counts_v1.csv`: pattern counts for the two core axes and both windows.
- `canonical_phase4_frozen_class_specifications_v1.csv`: full-precision upstream specifications, retained as provenance.
- `canonical_cell_trajectories_inventory_v1.csv`: relative paths, dimensions and hashes.
- `canonical_cell_trajectories_validation_v1.json`: actual execution checks, provenance, software versions and output hashes.
- A copy of the executed script.

The `gis/` folder contains four one-to-one CSV summaries, one per core axis and
window, plus `schema.ini`. IDs remain text; booleans are exported as 0/1; counts
are integers; numeric metrics retain double precision. These CSVs can join to
the canonical grid by `cell_id`. Their keys, width and type conventions are
independent of the earlier 08c interval tables.

## Principal field meanings

| Field | Meaning |
|---|---|
| `metric`, `stage_axis`, `analysis_window` | Measurement, declared axis and temporal window |
| `sequence_json`, `episode_sequence_json` | Original interval-stage list and compressed episode-stage list |
| `start_interval_index`, `end_interval_index` | Zero-based inclusive positions within the window |
| `episode_interval_count`, `episode_duration_observed_years` | Consecutive interval count and observation coverage |
| `left_boundary_flag`, `right_boundary_flag` | Touching each window edge; both can be true |
| `persistent_episode_flag`, `trajectory_constant_flag` | Multiquinquennial run versus whole-window constancy |
| `stage_reentry_count`, `stage_reentry_flag` | Number of returns and whether one episode is a reentry |
| `stage_first_observed_year`, `stage_last_observed_end_year` | First and last observed occurrence, not inferred process onset/end |
| `isolated_episode_flag`, `isolated_activity_flag`, `isolated_inactivity_flag` | Independent excursion and process-occurrence properties |
| `ordinal_direction`, `direction_change_count` | Direction and changes in the eligible ordinal path |
| `direct_direction_change_count` | Direction changes restricted to contiguous eligible blocks |
| `off_axis_interval_count`, `ordinal_path_crosses_off_axis_flag` | Intervals without rank and gaps inside the eligible path |
| `activity_entry_count`, `activity_exit_count` | Adjacent observed activation/deactivation events |
| `activity_interruption_count`, `activity_resumption_count` | Interior inactive runs bracketed by activity and corresponding resumptions |
| `direct_dominance_reversal_count`, `mediated_dominance_reversal_count` | Dominance switches with or without intervening nondominant stages |
| `continuous_defined_interval_count`, `continuous_mean/min/max/first/last` | Valid continuous observations and unweighted window summaries |
| `contains_diagnostic_interval`, `diagnostic_interval` | Episode/window membership and interval identity |
| `pattern_changed_with_diagnostic` | Difference between the two pattern codes |
| `terminal_primary_episode_continues_in_diagnostic` | Equality of seventh/eighth stages |
| `*_delta` | Full-series value minus primary value |
| `typology_applied` | Whether Decision 010's substantive classification is configured |

Continuous values use their original metric units. The original interval tables
retain gross activity, net balance, endpoint area, denominators, biome fractions
and pasture-composition context for interpretation; these are not substituted
by a single categorical code. Window means are not annual trends or duration-
weighted estimates of pixel persistence.

## Expected canonical populations

| Product | Expected count |
|---|---:|
| Input cell-interval records | 199,112 |
| Primary cell-metric trajectories | 298,668 |
| Full cell-metric trajectories | 298,668 |
| Combined cell-window-metric summaries | 597,336 |
| Primary interval-stage rows across 12 metrics | 2,090,676 |
| Full interval-stage rows across 12 metrics | 2,389,344 |
| Combined interval-stage rows | 4,480,020 |
| Primary adjacent transition events across 12 metrics | 1,792,008 |
| Full adjacent transition events across 12 metrics | 2,090,676 |
| Core typology rows across both axes and windows | 99,556 |
| Records per core GIS CSV | 24,889 |

Episode and occupancy row counts depend on the observed sequences. Transition
CSV row counts depend on the stage vocabulary and include zero-count pairs;
the event sums, not its number of rows, reconcile with the totals above.

## Accepted production and supplementary review

Canonical temporal production is accepted for run
`run_20260915T091255_865443Z`. The actual validation and supplementary GIS
consistency findings are documented in
`docs/validation/canonical_cell_trajectories_phase4a.md`. Interpretation and
spatial-relocation inference remain separate from computational acceptance.

Revision 2 loads required rate-support fields from the authenticated class
specifications, correcting revision 1's Parquet column projection. This
changes input loading only, preserving stages and frozen thresholds.

The code/flag constancy equivalence was verified on all 99,556 complete-support
core GIS records. Repeated intervals inside a single active episode can produce
`no_change` without stage reentry, reaching the activity-change pattern. This
reachability and the priority of returning/recurrent patterns are validation
cases of the existing design, not a typology change.

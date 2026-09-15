# Decision 010 — Stage definition and trajectory typology for Phase 4

- **Status:** Accepted analytical design; implementation and data validation pending.
- **Date accepted:** 2026-09-15.
- **Scope:** Interval stages, episode reconstruction and computable trajectory descriptors.
- **Dependencies:** Decisions 008 and 009; the spatiotemporal investigation plan.
- **Authorization:** The user requested the corrections identified in the review and documentation for GitHub.

## 1. Purpose and relationship to Decision 009

This decision supplies operational stage and pattern rules for the multiquinquennial analysis established by Decision 009. It preserves the fixed domain, the inclusion of 2020–2025, parallel primary/full-series outputs and temporal-boundary qualifications.

It explicitly refines the proposed flat six-pattern reading: trajectory patterns and episode properties are separate outputs. Persistence is measured at episode level; complete-window constancy is a separate trajectory property. Recurrence, direction changes, inactivity and isolated episodes are not forced into a single label. These rules supersede the corresponding proposed rules in the Decision 010 draft, not accepted upstream accounting or Phase 3 classifications.

No empirical result, execution success or Phase 4 completion is asserted here. Existing Decision 009 text must remain in the repository; its exact filename should be retained rather than renamed on the basis of the alternative names in conversation and the draft.

## 2. Independent stage axes

Reconstruct episodes independently for each declared axis. Use `stage_axis` in every table; never fuse axes into an undocumented composite stage. A cross-axis comparison can join interval records on `cell_id`, `t0`, `t1` and analysis window. Episode boundaries need not coincide across axes.

### 2.1 C–R balance

Reuse the accepted Phase 3 C–R class and verify it against these definitions:

| Stage | Rule |
|---|---|
| `inactive` | `gross_cr_activity_ha <= 1e-9` |
| `replenishment_dominant` | active and `cr_balance_index < -1/3` |
| `mixed` | active and `-1/3 <= cr_balance_index <= 1/3` |
| `consolidation_dominant` | active and `cr_balance_index > 1/3` |

For active records, the index must be finite and within its accepted range; an unexpected missing index is a validation failure, not inactivity. Missing gross activity is likewise not inactivity. The two boundaries belong to `mixed`. Activity uses the existing numerical tolerance, not a substantive minimum area.

These are aggregate cell balance states. The order of the three active states follows the index; it does not establish a necessary agricultural-development sequence. Interpret balance persistence alongside continuous gross activity and net balance: small and large flows can have the same balance class.

### 2.2 NAT–TMP endpoint magnitude

Adopt `nat_tmp_endpoint_ha__class` as the independent magnitude axis. Preserve the accepted labels `zero`, `low`, `moderate`, `high` and any upstream support labels verbatim; confirm the actual schema and class vocabulary before execution.

Reuse the authenticated full-precision Phase 3 limits, estimated from positive values in the seven primary intervals. Do not estimate new thresholds from 2020–2025, individual biomes or mapped subsets. `zero` denotes observed absence under the upstream rule; do not rename it to a value whose tolerance differs from that rule.

The ordinal magnitude order is `zero < low < moderate < high`. Zero is a valid magnitude state. For activity occurrence descriptors, zero is inactive and the three positive classes are active.

This axis measures endpoint conversion magnitude. Detected intermediate pasture and its trajectory shares remain separate complementary measurements, with their own support rules. The approximately 20-ha share-support requirement is not a new minimum for absolute endpoint magnitude. Composition can later be reconstructed as a separately declared axis without changing either axis defined here.

The two axes are required Phase 4 products. Implementation may deliver C–R first, but completion requires the endpoint-magnitude pass too. The other Phase 3 metrics may receive descriptive sequences and episodes; extending the named typology to them requires an explicit ordinal/support configuration rather than assuming all 12 have the same semantics.

## 3. Windows and inclusion of 2020–2025

Produce all sequences, episodes, transition matrices, descriptors and trajectory patterns separately for:

| `analysis_window` | Intervals | Observation range |
|---|---:|---|
| `primary` | 7 | 1985–2020 |
| `full_observed` | 8 | 1985–2025 |

The interval 2020–2025 has `diagnostic_interval = 1`; all earlier intervals have 0. It participates in the full sequence, the final transition, observed episode duration and full-series classification. It must not be excluded or overwrite primary results.

For each cell and axis, expose primary and full patterns, `pattern_changed_with_diagnostic`, and changes in episode count, maximum duration, reentry count and activity interruptions. Distinguish continuation of the terminal primary episode from a new episode in 2020–2025. Membership in a diagnostic interval and a change caused by appending that interval are different flags.

## 4. Episode reconstruction and duration

Order intervals by time and run-length encode consecutive identical stages separately within each window. One maximal run is one episode; adjacent episodes must have different stages. Retain the uncompressed stage sequence.

`episode_interval_count` is the number of contiguous intervals in the run. `episode_duration_observed_years` is the sum of their `t1 - t0` values; for the present panel it equals `5 * episode_interval_count`. This is observation coverage assigned to a quinquennial state, not proof that its balance or pixel condition persisted continuously in every year.

`persistent_episode_flag = 1` when the run spans at least two intervals. A changing trajectory can contain multiple persistent episodes. `trajectory_constant_flag = 1` only when the whole window has one episode.

Expose `previous_stage`, `next_stage`, stage-specific episode counts, total time in each stage, maximum consecutive duration, entry/exit events and reentries. First observation of a stage at the left boundary is observed occupancy, not a demonstrated onset. Ending at the right boundary is not a demonstrated exit.

### 4.1 Episode boundary and isolation properties

Use independent booleans:

- `left_boundary_flag`: the episode starts at the first interval of its window.
- `right_boundary_flag`: it ends at the last interval of its window.
- `isolated_episode_flag`: it is interior, lasts one interval and its immediate preceding and following episodes have the same stage.
- `isolated_activity_flag`: isolated episode with known active process occurrence.
- `isolated_inactivity_flag`: isolated episode with known inactive process occurrence.
- `contains_diagnostic_interval`: at least one constituent interval is diagnostic.

A sole episode has both boundary flags. If a display category is needed, `episode_position` is exactly one of `both_boundaries`, `left_boundary`, `right_boundary`, `interior`. Isolation remains independent of position.

Preserve the temporal censoring/boundary language adopted in Decision 009. Report boundary episodes as observed duration with unknown continuation beyond the relevant window; do not infer their true process onset, end or uncensored lifetime from the class panel.

## 5. Independent trajectory descriptors

### 5.1 Stage reentries

Let `E = (e1, ..., ek)` be the full ordered episode-stage list for a window. Count one reentry for each episode whose stage occurred in any earlier episode. Adjacent stages differ by construction, so any repeat is nonadjacent. Each episode contributes at most one reentry regardless of the number of earlier matching episodes.

Expose `stage_reentry_count` and stage-specific reentry counts. A return requires at least one intervening different episode; it does not require two intervening stages. This descriptor includes returns through inactivity. It denotes class recurrence, not return of the same pixels or parcels to an earlier use.

### 5.2 Direction on the declared ordinal axis

For C–R, assign ranks only to replenishment (−1), mixed (0) and consolidation (+1). Inactivity remains off-axis. For endpoint magnitude, assign ranks zero (0), low (1), moderate (2), high (3).

Extract the ordered eligible ranks from interval records, retain their original positions and collapse consecutive duplicate ranks in this extracted sequence. Compute nonzero successive rank differences and their signs. `direction_change_count` counts switches between successive signs. Set `ordinal_direction` to `increasing`, `decreasing`, `nonmonotonic`, or `no_change`; use `insufficient_ordinal_support` if fewer than two eligible interval observations exist.

For C–R, this describes the path among observed active states even when inactivity intervenes. Expose `off_axis_interval_count` and `ordinal_path_crosses_off_axis_flag` (an off-axis interval between the first and last eligible observations). Never describe such a comparison as uninterrupted activity or an adjacent observed transition. Also expose a direct direction-change count calculated within contiguous eligible blocks, without bridging off-axis episodes.

### 5.3 Activity interruptions and resumptions

Retain the ordered binary occurrence sequence, independently of ordinal direction. Count observed 0→1 entries and 1→0 exits between adjacent intervals. Count interior inactive runs bracketed by activity as `activity_interruption_count`; count the corresponding resumptions separately. Expose left/right activity occupancy flags rather than treating window boundaries as observed entries/exits.

An inactive interval remains a substantive state. Unexpected missing or support-restricted observations are unknown occurrence, not 0; do not bridge them or fabricate activity events.

### 5.4 Strict two-state alternation

Expose `repeated_two_state_alternation_flag = 1` only when the full episode list contains exactly two distinct stages, at least four episodes and alternates between them throughout. Thus `A→B→A` is one return, while `A→B→A→B` is repeated two-state alternation. Recurrence involving more stages remains visible through reentry counts and does not receive this strict flag automatically.

## 6. Trajectory pattern code

Evaluate these rules in order, separately for each window and axis:

| Code | Computable rule |
|---|---|
| `constant` | `k == 1` |
| `returning` | `stage_reentry_count == 1` |
| `recurrent` | `stage_reentry_count >= 2` |
| `nonmonotonic_without_return` | no reentries and `ordinal_direction == nonmonotonic` |
| `monotonic_without_return` | no reentries and `ordinal_direction` is increasing or decreasing |
| `activity_change_without_ordinal_change` | remaining complete supported sequence; no ordinal change or insufficient ordinal observations |

The last code accommodates, for example, inactivity followed by a single active balance state. A monotonic active path with an interruption retains the monotonic code and its interruption descriptors; the code alone is not a claim of uninterrupted progression.

`recurrent` means repeated reentries, not necessarily regular alternation. Strict alternation is an independent flag. `constant` can describe constant inactivity as well as a constant active class. Never interpret any of these codes as a pixel-level NAT→PAS→TMP trajectory.

Any unexpected missing observation blocks acceptance of the two canonical complete-support axes. If an optional axis legitimately contains `undefined`, `not_applicable` or `low_support`, preserve these states in its sequence and episode tables; do not rank them. Its substantive pattern must be `support_limited` until a separately documented support rule authorizes a comparable classification. Boundary and unknown-support events must not be counted as ordinary process transitions without labeling.

## 7. Examples defining expected behavior

Here `R`, `M`, `C` and `I` denote the three C–R balance stages and inactivity. Examples are compressed episode lists; runs can have different lengths.

| Episode list | Pattern | Additional interpretation |
|---|---|---|
| R | constant | both boundaries; episode persistence depends on run length |
| R→M→C | monotonic_without_return | increasing active balance |
| M→C→R | nonmonotonic_without_return | one direction change, no reentry |
| R→C→R | returning | one reentry, not strict repeated alternation |
| R→C→R→C | recurrent | two reentries; strict two-state alternation |
| R→I→R | returning | interruption; isolated inactivity if I spans one interval |
| R→I→C | monotonic_without_return | increasing active path with an interruption |
| I→C | activity_change_without_ordinal_change | observed activation, no active-rank change |
| I→C→I | returning | isolated activity if C spans one interval |

## 8. Outputs and acceptance criteria

Required tables are the interval-stage table, uncompressed cell sequences, episode table, cell-window trajectory summary, primary/full comparison and adjacent-interval transition matrices. Keys include `cell_id`, `stage_axis`, `analysis_window`, and interval or episode identifiers as appropriate. Record input hashes, class-source identity, schema version, decision version and the diagnostic interval rule.

Acceptance requires:

1. Exactly 24,889 cells per axis and window, with seven primary and eight full observations; no lost or duplicate keys.
2. Exact reuse of accepted upstream stages and full-precision class definitions.
3. Episode intervals partition each cell-window sequence without gaps or overlaps; recompression and expansion recover the original sequence exactly.
4. Episode counts, durations, reentries, boundaries, isolation flags and pattern codes satisfy the rules above, including the single-episode and inactive examples.
5. All primary outputs can be reproduced by restricting input to the first seven intervals; all full outputs retain the eighth.
6. Transition counts reconcile with 24,889 × 6 primary and 24,889 × 7 full transitions per axis, including inactive/zero states.
7. Every complete-support cell-window-axis has exactly one pattern. Additional flags can coexist; missing support is never silently recoded.
8. Primary/full comparisons retain both classifications and identify diagnostic-dependent changes.
9. Implementation verification covers meaningful edge cases, including direction changes without repeats, interruptions, both boundaries and an appended diagnostic state that changes the pattern.
10. Continuous magnitudes and support diagnostics accompany interpretation; computational validation does not establish agricultural succession, annual persistence or causality.

The future validation record must report actual results. This decision authorizes implementation; it is not that validation record.

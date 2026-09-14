# Decision 009 — Multiquinquennial episodes and flagged inclusion of 2020–2025

- **Status:** Accepted
- **Date recorded:** 2026-09-14
- **Scope:** Phase 4 temporal trajectories, episode duration, stage alternation, and treatment of the final interval
- **Related plan:** `docs/planning/006_spatiotemporal_investigation_plan.md`
- **Related outputs:** canonical integrated panel, spatial metrics panel, comparable map classes, and GIS interval tables

## Context

The canonical accounting system is organized into eight five-year intervals:

```text
1985–1990
1990–1995
1995–2000
2000–2005
2005–2010
2010–2015
2015–2020
2020–2025
```

These intervals are standardized accounting windows. They are not assumed to represent the complete duration of a land-use process.

A cell may remain in the same analytical stage for more than one five-year interval. It may also change stage, return to a previously occupied stage, or alternate repeatedly between expansion, consolidation, mixed activity, and low or absent focal activity.

Treating every interval as an independent episode would therefore fragment processes that persist across multiple quinquennia and conceal temporal alternation. Conversely, joining intervals without explicit rules could create episodes that are artifacts of cell-level aggregation rather than evidence of continuous pixel-level land-use trajectories.

The interval 2020–2025 also requires explicit treatment. It is a valid part of the canonical panel and must not be discarded. However, because it reaches the final year of the source series, trajectories that remain active in 2025 cannot be observed to completion. Results involving this interval therefore have a temporal-boundary limitation.

## Decision

### 1. Five-year intervals remain the accounting units

All canonical stock, flow, balance, mapping, and validation products will continue to use the eight fixed five-year intervals.

The existing interval-level accounting will not be replaced by an episode-based accounting system. Episodes are a derived analytical representation constructed during Phase 4 from the validated interval panel.

### 2. Phase 4 will explicitly identify multiquinquennial episodes

Cell trajectories will be evaluated across the complete ordered sequence of intervals.

An episode is defined as one or more consecutive five-year intervals assigned to the same preregistered analytical stage.

For each cell and episode, the Phase 4 output should retain at least:

- `cell_id`;
- `episode_id`;
- `episode_start_year`;
- `episode_end_year`;
- `episode_interval_count`;
- `episode_observed_duration_years`;
- `episode_stage`;
- `previous_stage`;
- `next_stage`;
- `stage_change_count`;
- `alternation_flag`;
- `left_boundary_flag`;
- `right_boundary_flag`;
- `includes_2020_2025`;
- the complete ordered interval-stage sequence required to reconstruct the episode.

A stage persisting for two or more consecutive intervals will be recorded as a multiquinquennial episode.

The observed episode duration is:

\[
D_e = 5n_e,
\]

where \(n_e\) is the number of consecutive five-year intervals belonging to episode \(e\).

This is an observed duration within the analytical series. It is not necessarily the complete duration of the underlying land-use process.

### 3. Stage alternation will be retained as information

The Phase 4 trajectory classification must distinguish:

- persistence in the same stage;
- one-directional progression between stages;
- return to a previously occupied stage;
- repeated alternation between two or more stages;
- isolated activity surrounded by intervals assigned to another stage;
- entry into or exit from focal activity at a temporal boundary.

Alternation will not automatically be interpreted as land-use reversal at the pixel level. The primary unit is the approximately 20,000 ha analytical cell, within which different component processes may occur simultaneously or sequentially.

The term **cell-level stage alternation** will therefore be preferred unless pixel-level annual trajectories directly support a stronger interpretation.

### 4. Stage definitions must be fixed before trajectory interpretation

The rules used to assign interval-level stages must be documented before inspecting the resulting spatial trajectories.

The same rules and thresholds must be applied to every interval, including 2020–2025.

Thresholds must not be recalculated separately for each interval because interval-specific quantiles would make apparent stage changes partly dependent on changing class boundaries.

If empirical thresholds are used, they must be estimated once from a declared reference population and then held fixed. The preferred reference population is the primary 1985–2020 period. The resulting fixed thresholds will subsequently be applied unchanged to 2020–2025.

The stage-definition record must specify:

- variables used;
- analytical denominator;
- treatment of structural zeros;
- treatment of undefined ratios;
- numerical thresholds;
- reference population used to derive any empirical threshold;
- rules for ties and boundary values;
- minimum material-flow tolerance.

### 5. The interval 2020–2025 will be included and flagged

The interval 2020–2025 will remain in:

- interval tables;
- maps;
- cell trajectories;
- episode reconstruction;
- descriptive summaries;
- spatial comparisons;
- supplementary outputs.

It will be identified explicitly as:

```text
diagnostic temporal-boundary interval
```

Its inclusion must be visible in tables, figure captions, legends, validation records, and analytical metadata whenever its boundary status is relevant.

It will not be silently pooled with earlier intervals in a way that hides this limitation.

### 6. Episodes reaching 2025 are right-boundary episodes

Any episode containing 2020–2025 and still present at the end of the observed series will receive:

```text
right_boundary_flag = 1
```

Such an episode may be described as having persisted for at least its observed duration. It must not be described as having ended in 2025 unless an observed stage transition supports that conclusion.

For example, an episode observed in 2015–2020 and 2020–2025 has an observed duration of at least ten years. Its complete duration remains unknown if the stage is still present in 2025.

### 7. Primary and full-period summaries will be distinguished

The primary temporal interpretation will be supported by the seven intervals ending in 2020.

The 2020–2025 interval will nevertheless be included in the analysis and presented as an explicitly flagged extension.

For conclusions sensitive to the last interval, two summaries will be compared:

1. **primary-period summary:** 1985–2020;
2. **full observed-series summary:** 1985–2025, including the flagged final interval.

The comparison is a temporal-boundary sensitivity analysis, not a basis for removing an inconvenient observation.

A conclusion will be described as temporally robust when its direction and substantive interpretation remain consistent in both summaries. Material differences must be reported and investigated.

### 8. Interval accounting and episode interpretation remain distinct

The creation of multiquinquennial episodes must not alter or redistribute the validated areas assigned to individual five-year intervals.

Episode reconstruction is a temporal classification layer over the canonical interval panel. It does not change:

- stock and flow identities;
- pasture-origin partitions;
- interval totals;
- cell-level accounting closure;
- the distinction between endpoint transitions and annual intermediate trajectories.

## Rationale

This decision:

- recognizes that land-use stages can persist for longer than one quinquennium;
- prevents a persistent process from being represented as a series of unrelated events;
- retains alternation and recurrence rather than forcing all trajectories into a monotonic sequence;
- preserves the validated five-year accounting structure;
- avoids interpreting cell-level alternation as demonstrated pixel-level reversal;
- preserves 2020–2025 as useful evidence;
- makes the temporal-boundary limitation of the final interval explicit;
- permits direct sensitivity analysis of conclusions with and without the boundary interval.

## Consequences

### Positive consequences

- Phase 4 can represent duration, persistence, progression, recurrence, and alternation.
- Episodes spanning more than one quinquennium become explicit analytical objects.
- The complete 1985–2025 information is preserved.
- Right-boundary censoring is distinguished from an observed episode ending.
- Conclusions can be assessed for sensitivity to the inclusion of 2020–2025.
- Interval-level accounting remains reproducible and unchanged.

### Constraints and interpretation limits

- Episode duration is resolved in five-year units.
- Processes beginning before 1985 may be left-boundary censored.
- Processes continuing after 2025 are right-boundary censored.
- A stable cell-level stage does not imply that every pixel remained in the same state.
- Cell-level alternation may arise from different processes occurring in different portions of the same cell.
- Pixel-level continuity must not be inferred from interval-level cell aggregates alone.
- Threshold-dependent episodes require the threshold specification to be preserved with the output.

## Alternatives considered

### Treat every five-year interval as an independent episode

Rejected because it would fragment stages that persist across multiple intervals and prevent direct measurement of observed persistence.

### Replace the five-year accounting with variable-duration episodes

Rejected because it would abandon the standardized accounting windows and make stock and flow comparisons less transparent.

### Force trajectories into monotonic sequences

Rejected because cells may return to earlier stages or alternate between processes. Such behavior is analytically relevant and should not be erased.

### Exclude 2020–2025 from Phase 4

Rejected because the interval is valid observed information and may reveal continuation or change in trajectories. Its limitation can be handled through explicit flagging and sensitivity analysis.

### Treat 2020–2025 identically to all earlier intervals without qualification

Rejected because episodes reaching the end of the source series cannot be observed beyond 2025. Their completion and full duration are unknown.

### Define stage thresholds separately for every interval

Rejected because changes in relative class boundaries could be mistaken for changes in the underlying process.

## Implementation requirements

Phase 4 must produce:

1. an interval-stage table with one row per `cell_id × interval`;
2. an ordered stage sequence for every cell;
3. an episode table with one row per reconstructed episode;
4. explicit duration and temporal-boundary fields;
5. indicators of persistence, progression, return, and alternation;
6. primary-period and full-series summaries;
7. validation showing that every interval-stage row belongs to exactly one episode;
8. documentation of the fixed stage definitions and thresholds.

The 2020–2025 flag must also be propagated to relevant maps, tables, captions, and validation metadata.

## Acceptance criteria

This decision is implemented when:

- all 24,889 cells have an ordered record for all eight intervals;
- interval-stage keys are unique;
- stage definitions are fixed before substantive trajectory interpretation;
- thresholds are identical across intervals;
- consecutive intervals with the same stage are combined reproducibly;
- every interval-stage observation belongs to exactly one episode;
- episode duration equals five times the number of included intervals;
- alternation and return patterns can be distinguished from monotonic progression;
- episodes touching 1985 or 2025 carry the appropriate boundary flag;
- all outputs containing 2020–2025 identify it as the diagnostic temporal-boundary interval;
- primary-period and full-series results can be compared directly;
- episode construction leaves the validated interval-level accounting unchanged.

## Terminology

Preferred terms:

- **five-year accounting interval**;
- **interval-level analytical stage**;
- **multiquinquennial episode**;
- **cell-level stage persistence**;
- **cell-level stage alternation**;
- **observed episode duration**;
- **left-boundary episode**;
- **right-boundary episode**;
- **diagnostic temporal-boundary interval**;
- **primary-period summary, 1985–2020**;
- **full observed-series summary, 1985–2025**.

Terms to avoid without additional evidence:

- complete episode duration;
- episode ended in 2025;
- pixel-level reversal;
- continuous pixel trajectory across quinquennia;
- independent event, when referring only to one interval within a longer episode.

"""Phase 4A: canonical cell trajectories, episodes and temporal transitions.

Colab: %run /content/09a_build_cell_state_trajectories.py
Local verification: python 09a_build_cell_state_trajectories.py --self-test
No GEE or geometry processing. Frozen Phase 3 classes are verified, not refitted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
import pandas as pd

VERSION = "phase4a-cell-trajectories-v3"
INTERVALS = [(y, y + 5) for y in range(1985, 2025, 5)]
KEYS = ["cell_id", "t0", "t1"]
EXPECTED_CELLS = 24889
EXPECTED_ROWS = 199112
METRICS = [
    "consolidation_ha", "consolidation_rate_initial_pasture",
    "replenishment_ha", "replenishment_rate_initial_native",
    "nat_tmp_endpoint_ha", "nat_tmp_intensity_initial_native",
    "nat_tmp_pas_any_ha", "nat_tmp_pas_any_share_endpoint",
    "nat_tmp_pas_consecutive2_ha", "nat_tmp_pas_consecutive2_share_endpoint",
    "net_cr_balance_ha", "cr_balance_index",
]
CR = "cr_balance_index"
NAT = "nat_tmp_endpoint_ha"
CORE = {CR, NAT}
UNKNOWN = {"undefined", "not_applicable", "low_support"}
RANKS = {
    CR: {"replenishment_dominant": -1, "mixed": 0, "consolidation_dominant": 1},
    NAT: {"zero": 0, "positive_low": 1, "positive_moderate": 2, "positive_high": 3},
}
HASHES = {
    "canonical_spatial_metrics_panel_v1.parquet": "8c99e77fc85a55e753f95e0e51b7be954ba9c4229a741e9e7b576c6f61637e4c",
    "canonical_spatial_metrics_validation_v1.json": "9b9278112bbddfb4b8b01c21d15727ae277f28b77cfbf2702b040eff8f3784b8",
    "canonical_map_classes_validation_v2.json": "cb909c77372c34947d670342db233a51e07f31996a4bb8085947f973937f7343",
    "canonical_comparable_map_class_counts_v2.csv": "1740b1fa90d47a2031202426efb0973a02ea93a8e94f20a00323e382fe54a908",
}
STAGE_AXIS = {CR: "cr_balance", NAT: "nat_tmp_endpoint_magnitude"}
CONTEXT = [
    "GRID_ID", "gross_cr_activity_ha", "net_cr_balance_ha", "consolidation_ha",
    "replenishment_ha", "nat_tmp_endpoint_ha", "stock0_nat", "stock0_pas",
    "geometry_area_aea_ha", "nat_tmp_endpoint_share_defined",
    "nat_tmp_pas_any_share_endpoint", "nat_tmp_pas_consecutive2_share_endpoint",
    "primary_biome", "amazon_fraction_cell", "cerrado_fraction_cell",
]


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False,
                                    allow_nan=False) + "\n", encoding="utf-8")


def identifier(value):
    require(not pd.isna(value), "Missing cell_id")
    if isinstance(value, (int, np.integer)):
        result = str(int(value))
    elif isinstance(value, (float, np.floating)):
        require(np.isfinite(value) and value.is_integer(), "Non-integral numeric cell_id")
        result = str(int(value))
    else:
        result = str(value).strip()
    require(bool(result), "Empty cell_id")
    return result


def activity(stage, metric):
    if stage in UNKNOWN:
        return None
    if metric == CR:
        return int(stage != "inactive")
    if metric == NAT:
        return int(stage != "zero")
    return None  # No undocumented process-occurrence semantics for optional axes.


def direction(sequence, metric):
    ranks = RANKS.get(metric, {})
    eligible = [(i, ranks[s]) for i, s in enumerate(sequence) if s in ranks]
    off = len(sequence) - len(eligible)
    if len(eligible) < 2:
        return "insufficient_ordinal_support", 0, 0, off, False
    values = [v for _, v in eligible]
    diffs = np.diff(values)
    signs = np.sign(diffs[diffs != 0]).astype(int).tolist()
    changes = sum(a != b for a, b in zip(signs, signs[1:]))
    label = ("no_change" if not signs else "nonmonotonic" if changes else
             "increasing" if signs[0] > 0 else "decreasing")
    direct_changes = 0
    block = []
    for stage in list(sequence) + ["__end__"]:
        if stage in ranks:
            block.append(ranks[stage])
        else:
            d = np.diff(block)
            ss = np.sign(d[d != 0]).astype(int).tolist()
            direct_changes += sum(a != b for a, b in zip(ss, ss[1:]))
            block = []
    lo, hi = eligible[0][0], eligible[-1][0]
    crosses = any(s not in ranks for s in sequence[lo:hi + 1])
    return label, changes, direct_changes, off, crosses


def reconstruct(sequence, metric, window):
    """Pure sequence engine; no I/O and no dependence on the canonical population."""
    sequence = list(sequence)
    require(0 < len(sequence) <= len(INTERVALS), "Invalid sequence length")
    require(all(isinstance(s, str) and bool(s) for s in sequence), "Missing stage")
    starts = [0] + [i for i in range(1, len(sequence)) if sequence[i] != sequence[i - 1]]
    ends = starts[1:] + [len(sequence)]
    stages = [sequence[i] for i in starts]
    seen = set()
    reentries = []
    for s in stages:
        reentries.append(s in seen)
        seen.add(s)
    reentry_count = sum(reentries)
    k = len(stages)
    ordinal, changes, direct_changes, off, crosses = direction(sequence, metric)
    typology = metric in CORE
    support_limited = any(s in UNKNOWN for s in sequence)
    if not typology:
        pattern = "not_classified"
    elif support_limited:
        pattern = "support_limited"
    elif k == 1:
        pattern = "constant"
    elif reentry_count == 1:
        pattern = "returning"
    elif reentry_count >= 2:
        pattern = "recurrent"
    elif ordinal == "nonmonotonic":
        pattern = "nonmonotonic_without_return"
    elif ordinal in {"increasing", "decreasing"}:
        pattern = "monotonic_without_return"
    else:
        pattern = "activity_change_without_ordinal_change"
    acts = [activity(s, metric) for s in sequence]
    entries = sum(a == 0 and b == 1 for a, b in zip(acts, acts[1:]))
    exits = sum(a == 1 and b == 0 for a, b in zip(acts, acts[1:]))
    episodes = []
    interruptions = 0
    for j, (start, stop) in enumerate(zip(starts, ends)):
        s = stages[j]
        left, right = j == 0, j == k - 1
        interior = not left and not right
        previous = stages[j - 1] if j else None
        following = stages[j + 1] if j < k - 1 else None
        isolated = interior and stop - start == 1 and previous == following
        interrupted = (interior and activity(s, metric) == 0
                       and activity(previous, metric) == 1 and activity(following, metric) == 1)
        interruptions += int(interrupted)
        episodes.append({
            "episode_id": j + 1, "episode_stage": s,
            "start_interval_index": start, "end_interval_index": stop - 1,
            "start_year": INTERVALS[start][0], "end_year": INTERVALS[stop - 1][1],
            "episode_interval_count": stop - start,
            "episode_duration_observed_years": sum(b - a for a, b in INTERVALS[start:stop]),
            "persistent_episode_flag": stop - start >= 2,
            "previous_stage": previous, "next_stage": following,
            "stage_reentry_flag": reentries[j],
            "left_boundary_flag": left, "right_boundary_flag": right,
            "episode_position": ("both_boundaries" if left and right else "left_boundary"
                                 if left else "right_boundary" if right else "interior"),
            "isolated_episode_flag": isolated,
            "isolated_activity_flag": isolated and activity(s, metric) == 1,
            "isolated_inactivity_flag": isolated and activity(s, metric) == 0,
            "activity_interruption_flag": interrupted,
            "contains_diagnostic_interval": stop == 8,
        })
    require([e["episode_stage"] for e in episodes for _ in range(e["episode_interval_count"])]
            == sequence, "Episode expansion does not recover the source sequence")
    require(sum(e["episode_interval_count"] for e in episodes) == len(sequence),
            "Episode duration does not partition the window")
    require(all(a != b for a, b in zip(stages, stages[1:])), "Nonmaximal episodes")
    # Direct and mediated dominance reversals, separate from general rank changes.
    direct_reversals = mediated_reversals = 0
    if metric == CR:
        dominant = [(j, s) for j, s in enumerate(stages)
                    if s in {"replenishment_dominant", "consolidation_dominant"}]
        for (a, sa), (b, sb) in zip(dominant, dominant[1:]):
            if sa != sb:
                direct_reversals += int(b == a + 1)
                mediated_reversals += int(b > a + 1)
    summary = {
        "sequence_json": json.dumps(sequence, separators=(",", ":")),
        "episode_sequence_json": json.dumps(stages, separators=(",", ":")),
        "interval_count": len(sequence), "episode_count": k,
        "stage_change_count": k - 1, "distinct_stage_count": len(seen),
        "trajectory_constant_flag": k == 1,
        "stage_reentry_count": reentry_count,
        "max_episode_interval_count": max(e["episode_interval_count"] for e in episodes),
        "max_episode_duration_observed_years": max(e["episode_duration_observed_years"] for e in episodes),
        "persistent_episode_count": sum(e["persistent_episode_flag"] for e in episodes),
        "isolated_episode_count": sum(e["isolated_episode_flag"] for e in episodes),
        "isolated_activity_count": sum(e["isolated_activity_flag"] for e in episodes),
        "isolated_inactivity_count": sum(e["isolated_inactivity_flag"] for e in episodes),
        "trajectory_pattern_code": pattern,
        "typology_applied": typology,
        "support_limited_flag": support_limited,
        "ordinal_direction": ordinal if typology else "not_configured",
        "direction_change_count": changes if typology else None,
        "direct_direction_change_count": direct_changes if typology else None,
        "off_axis_interval_count": off if typology else None,
        "ordinal_path_crosses_off_axis_flag": crosses if typology else None,
        "activity_entry_count": entries if typology else None,
        "activity_exit_count": exits if typology else None,
        "activity_interruption_count": interruptions if typology else None,
        "activity_resumption_count": interruptions if typology else None,
        "left_activity_occupancy": acts[0], "right_activity_occupancy": acts[-1],
        "repeated_two_state_alternation_flag": len(seen) == 2 and k >= 4,
        "direct_dominance_reversal_count": direct_reversals if metric == CR else None,
        "mediated_dominance_reversal_count": mediated_reversals if metric == CR else None,
        "contains_diagnostic_interval": len(sequence) == 8,
    }
    state_rows = []
    for s in sorted(seen):
        rows = [e for e in episodes if e["episode_stage"] == s]
        state_rows.append({
            "stage": s, "stage_episode_count": len(rows),
            "stage_reentry_count": sum(e["stage_reentry_flag"] for e in rows),
            "stage_interval_count": sum(e["episode_interval_count"] for e in rows),
            "stage_duration_observed_years": sum(e["episode_duration_observed_years"] for e in rows),
            "stage_max_episode_interval_count": max(e["episode_interval_count"] for e in rows),
            "stage_first_observed_year": rows[0]["start_year"],
            "stage_last_observed_end_year": rows[-1]["end_year"],
            "stage_first_observed_at_left_boundary": rows[0]["left_boundary_flag"],
            "stage_last_observed_at_right_boundary": rows[-1]["right_boundary_flag"],
        })
    require(sum(r["stage_reentry_count"] for r in state_rows) == reentry_count,
            "Stage-specific reentry counts do not reconcile")
    return summary, episodes, state_rows


def reproduce_classes(panel, limit):
    """Same fixed rules as accepted 08b v3; no quantiles are estimated."""
    metric, kind = limit["metric"], limit["measure_type"]
    a, b, tol = float(limit["break_1"]), float(limit["break_2"]), float(limit["zero_tolerance"])
    v = pd.to_numeric(panel[metric], errors="raise")
    require(not np.isinf(v.to_numpy()).any(), f"Infinite values: {metric}")
    if kind == "bounded_balance_index":
        gross = pd.to_numeric(panel["gross_cr_activity_ha"], errors="raise")
        require(gross.notna().all() and np.isfinite(gross).all() and gross.ge(0).all(),
                "Invalid gross C–R activity")
        active = gross.gt(1e-9)
        require(v[active].notna().all() and v[active].between(-1, 1).all(), "Invalid active balance")
        require(v[~active].isna().all(), "Inactive index must remain undefined")
        require(panel["cr_balance_defined"].eq(active.astype(int)).all(), "Balance support mismatch")
        out = pd.Series("inactive", index=panel.index)
        out.loc[active & v.lt(-1 / 3)] = "replenishment_dominant"
        out.loc[active & v.between(-1 / 3, 1 / 3, inclusive="both")] = "mixed"
        out.loc[active & v.gt(1 / 3)] = "consolidation_dominant"
        require(out.eq(panel["cr_balance_state"]).all(), "Accepted balance state differs from formula")
    elif kind == "trajectory_share":
        defined = panel["nat_tmp_endpoint_share_defined"].eq(1)
        eligible = defined & panel[NAT].gt(panel["geometry_area_aea_ha"] * 0.001)
        require(v[eligible].notna().all(), f"Missing eligible share: {metric}")
        out = pd.Series("not_applicable", index=panel.index)
        out.loc[defined & ~eligible] = "low_support"
        out.loc[eligible & v.le(tol)] = "zero"
        out.loc[eligible & v.gt(tol) & v.le(a)] = "positive_low"
        out.loc[eligible & v.gt(a) & v.le(b)] = "positive_moderate"
        out.loc[eligible & v.gt(b)] = "positive_high"
    elif kind == "signed_area_ha":
        require(v.notna().all(), f"Missing signed area: {metric}")
        out = pd.Series("zero", index=panel.index)
        for mask, label in [
            (v.lt(-b), "replenishment_high"), (v.ge(-b) & v.lt(-a), "replenishment_moderate"),
            (v.ge(-a) & v.lt(-tol), "replenishment_low"),
            (v.gt(tol) & v.le(a), "consolidation_low"),
            (v.gt(a) & v.le(b), "consolidation_moderate"), (v.gt(b), "consolidation_high"),
        ]:
            out.loc[mask] = label
    else:
        field = limit["support_field"]
        supported = v.notna() if field == "all_rows" else panel[field].eq(1)
        require(v[supported].notna().all(), f"Missing supported values: {metric}")
        out = pd.Series("undefined", index=panel.index)
        out.loc[supported & v.le(tol)] = "zero"
        out.loc[supported & v.gt(tol) & v.le(a)] = "positive_low"
        out.loc[supported & v.gt(a) & v.le(b)] = "positive_moderate"
        out.loc[supported & v.gt(b)] = "positive_high"
    return out


def required_metric_columns(limits):
    # Share support is an expression with explicitly declared input fields.
    # Other frozen records name a single support field, which must be loaded.
    fields = KEYS + METRICS + CONTEXT + ["cr_balance_defined", "cr_balance_state"]
    for limit in limits:
        if limit["measure_type"] == "trajectory_share":
            fields += ["nat_tmp_endpoint_share_defined", NAT, "geometry_area_aea_ha"]
        elif limit["measure_type"] not in {"signed_area_ha", "bounded_balance_index"}:
            support = limit["support_field"]
            if support != "all_rows":
                require(isinstance(support, str) and support.isidentifier(),
                        f"Unsupported support-field expression: {support}")
                fields.append(support)
    return list(dict.fromkeys(fields))


def load_inputs(project):
    p2, p3 = project / "spatial/phase2", project / "spatial/phase3"
    paths = [p2 / "canonical_spatial_metrics_panel_v1.parquet",
             p2 / "canonical_spatial_metrics_validation_v1.json",
             p3 / "canonical_map_classes_validation_v2.json",
             p3 / "canonical_comparable_map_class_counts_v2.csv",
             p3 / "canonical_spatial_map_classes_v1.parquet",
             p3 / "canonical_comparable_maps_validation_v1.json"]
    records = {}
    for p in paths:
        require(p.is_file(), f"Missing required input: {p}")
        digest = sha256(p)
        if p.name in HASHES:
            require(digest == HASHES[p.name], f"SHA-256 mismatch: {p.name}")
        records[p.name] = {"path": str(p), "sha256": digest}
    v2 = json.loads(paths[1].read_text())
    va = json.loads(paths[2].read_text())
    vb = json.loads(paths[5].read_text())
    for v, label in [(v2, "Phase 2"), (va, "Phase 3A"), (vb, "Phase 3B")]:
        require(v.get("validation_status") == "PASS", f"{label} is not PASS")
        checks = v.get("checks", {})
        require(bool(checks) and all(value is True for value in checks.values()), f"{label} has invalid checks")
    require(va.get("map_class_version") == vb.get("map_class_version")
            == "canonical-comparable-map-classes-v2", "Wrong map-class version")
    require(vb.get("map_product_version") == "canonical-comparable-interval-maps-v1", "Wrong map-product version")
    require(va["scope"]["diagnostic_used_to_fit_limits"] is False, "Diagnostic fitted class limits")
    for name in [paths[0].name, paths[2].name, paths[3].name]:
        require(vb.get("inputs", {}).get(name, {}).get("sha256") == records[name]["sha256"],
                f"Phase 3B input provenance mismatch: {name}")
    require(vb.get("outputs", {}).get(paths[4].name, {}).get("sha256") == records[paths[4].name]["sha256"],
            "Classified panel does not match Phase 3B output hash")
    columns = required_metric_columns(va["limits"])
    panel = pd.read_parquet(paths[0], columns=columns)
    classes = pd.read_parquet(paths[4], columns=KEYS + [f"{m}__class" for m in METRICS])
    for frame in [panel, classes]:
        frame["cell_id"] = frame["cell_id"].map(identifier)
        for field in ["t0", "t1"]:
            numeric = pd.to_numeric(frame[field], errors="raise")
            require(numeric.notna().all() and numeric.mod(1).eq(0).all(), f"Invalid {field}")
            frame[field] = numeric.astype(int)
        require(len(frame) == EXPECTED_ROWS and frame["cell_id"].nunique() == EXPECTED_CELLS,
                "Unexpected canonical population")
        require(not frame.duplicated(KEYS).any(), "Duplicate cell-interval keys")
        require(set(map(tuple, frame[["t0", "t1"]].to_numpy())) == set(INTERVALS), "Unexpected intervals")
        require(frame.groupby("cell_id").size().eq(8).all(), "Unbalanced cell series")
        frame.sort_values(["cell_id", "t0", "t1"], inplace=True)
        frame.reset_index(drop=True, inplace=True)
    require(panel[KEYS].equals(classes[KEYS]), "Metric/class keys differ")
    require(set(METRICS) == {l["metric"] for l in va["limits"]} and len(va["limits"]) == 12,
            "Class-limit specification differs")
    accepted = pd.read_csv(paths[3])
    require(len(accepted) == 504, "Unexpected accepted class-count table size")
    count_rows = []
    for limit in va["limits"]:
        metric = limit["metric"]
        predicted = reproduce_classes(panel, limit)
        observed = classes[f"{metric}__class"]
        require(observed.notna().all() and predicted.eq(observed).all(), f"Frozen class mismatch: {metric}")
        labels = json.loads(limit["class_labels"])
        require(set(observed).issubset(labels), f"Unexpected stage: {metric}")
        if metric in CORE:
            require(not observed.isin(UNKNOWN).any(), f"Canonical core axis lacks complete support: {metric}")
        for t0, t1 in INTERVALS:
            counts = observed[panel["t0"].eq(t0)].value_counts()
            for label in labels:
                count_rows.append({"metric": metric, "t0": t0, "t1": t1,
                                   "class_label": label, "cell_count": int(counts.get(label, 0))})
    keys = ["metric", "t0", "t1", "class_label"]
    reproduced = pd.DataFrame(count_rows)
    joined = reproduced.merge(accepted[keys + ["cell_count"]], on=keys, how="outer",
                              validate="one_to_one", indicator=True, suffixes=("_new", "_accepted"))
    require(joined["_merge"].eq("both").all()
            and joined.cell_count_new.eq(joined.cell_count_accepted).all(), "Accepted 504 class counts differ")
    panel = pd.concat([panel, classes.drop(columns=KEYS)], axis=1)
    return panel, va["limits"], records


def save_table(frame, path, inventory):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        # Categoricals reduce file and runtime-memory size; double precision is retained.
        frame = frame.copy()
        for col in ["stage_axis", "analysis_window", "metric", "stage", "episode_stage",
                    "previous_stage", "next_stage", "episode_position", "trajectory_pattern_code",
                    "ordinal_direction", "class_label", "from_stage", "to_stage"]:
            if col in frame:
                frame[col] = frame[col].astype("category")
        frame.to_parquet(path, index=False, compression="snappy")
    else:
        frame.to_csv(path, index=False, encoding="utf-8-sig", float_format="%.17g")
    inventory.append({"path": str(path), "filename": path.name, "rows": len(frame),
                      "columns": len(frame.columns), "sha256": sha256(path)})


def transition_counts(wide, metric, window):
    result = []
    labels = sorted(set(wide.ravel()))
    for i in range(wide.shape[1] - 1):
        counts = Counter(zip(wide[:, i], wide[:, i + 1]))
        source_counts = Counter(wide[:, i])
        require(sum(counts.values()) == len(wide), "Transition population does not close")
        require(all(sum(n for (a, _), n in counts.items() if a == s) == source_counts[s]
                    for s in labels), "Transition source marginal differs")
        target_counts = Counter(wide[:, i + 1])
        require(all(sum(n for (_, b), n in counts.items() if b == s) == target_counts[s]
                    for s in labels), "Transition target marginal differs")
        for a in labels:
            for b in labels:
                n = counts[(a, b)]
                result.append({"metric": metric, "stage_axis": STAGE_AXIS.get(metric, metric),
                               "analysis_window": window, "from_t0": INTERVALS[i][0],
                               "from_t1": INTERVALS[i][1], "to_t0": INTERVALS[i + 1][0],
                               "to_t1": INTERVALS[i + 1][1], "from_stage": a, "to_stage": b,
                               "cell_count": n, "source_cell_count": source_counts[a],
                               "source_transition_fraction": n / source_counts[a] if source_counts[a] else None,
                               "contains_diagnostic_interval": i + 1 == 7,
                               "from_support_limited": a in UNKNOWN, "to_support_limited": b in UNKNOWN})
    return pd.DataFrame(result)


def build_products(panel, limits, output):
    """Write one metric/window at a time. Population derives from validated input."""
    n = panel.cell_id.nunique()
    panel = panel.sort_values(["cell_id", "t0", "t1"]).reset_index(drop=True)
    ids = panel.cell_id.drop_duplicates().tolist()
    require(len(panel) == n * 8, "Unexpected product-input shape")
    inventory, matrix_parts, comparisons, pattern_parts = [], [], [], []
    totals = {"interval_stage_rows": 0, "cell_window_summary_rows": 0,
              "episode_rows": 0, "state_summary_rows": 0,
              "primary_transition_events": 0, "full_transition_events": 0}
    for metric in METRICS:
        started = time.monotonic()
        print(f"Processing {metric} ({'Decision 010 typology' if metric in CORE else 'descriptive episodes'})", flush=True)
        wide = panel[f"{metric}__class"].to_numpy().reshape(n, 8)
        measures = panel[metric].to_numpy(dtype=float).reshape(n, 8)
        summaries = {}
        for window, length in [("primary", 7), ("full_observed", 8)]:
            base = output / "tables" / metric / window
            summary_rows, episode_rows, state_rows = [], [], []
            positions = np.tile(np.arange(8), n) < length
            selected = list(dict.fromkeys(KEYS + [metric] + CONTEXT))
            interval_frame = panel.loc[positions, selected].copy()
            interval_frame["metric"] = metric
            interval_frame["stage_axis"] = STAGE_AXIS.get(metric, metric)
            interval_frame["analysis_window"] = window
            interval_frame["interval_index"] = np.tile(np.arange(length), n)
            interval_frame["episode_stage"] = wide[:, :length].ravel()
            interval_frame["diagnostic_interval"] = interval_frame["t0"].eq(2020).astype("int8")
            interval_frame["support_limited_flag"] = interval_frame.episode_stage.isin(UNKNOWN)
            save_table(interval_frame, base / "interval_stages.parquet", inventory)
            totals["interval_stage_rows"] += len(interval_frame)
            for row, cell_id in enumerate(ids):
                summary, episodes, states = reconstruct(wide[row, :length], metric, window)
                common = {"cell_id": cell_id, "metric": metric,
                          "stage_axis": STAGE_AXIS.get(metric, metric), "analysis_window": window}
                vals = measures[row, :length]
                finite = vals[np.isfinite(vals)]
                summary.update(common)
                summary.update({"continuous_defined_interval_count": len(finite),
                                "continuous_mean": float(finite.mean()) if len(finite) else None,
                                "continuous_min": float(finite.min()) if len(finite) else None,
                                "continuous_max": float(finite.max()) if len(finite) else None,
                                "continuous_first": float(vals[0]) if np.isfinite(vals[0]) else None,
                                "continuous_last": float(vals[-1]) if np.isfinite(vals[-1]) else None})
                summary_rows.append(summary)
                for e in episodes:
                    e.update(common)
                    ev = vals[e["start_interval_index"]:e["end_interval_index"] + 1]
                    fv = ev[np.isfinite(ev)]
                    e["continuous_defined_interval_count"] = len(fv)
                    e["continuous_mean"] = float(fv.mean()) if len(fv) else None
                    episode_rows.append(e)
                for s in states:
                    s.update(common)
                    state_rows.append(s)
            sdf, edf, stf = map(pd.DataFrame, [summary_rows, episode_rows, state_rows])
            require(len(sdf) == n and not sdf.cell_id.duplicated().any(), "Missing or duplicate summary cells")
            require(not edf.duplicated(["cell_id", "episode_id"]).any(), "Duplicate episode key")
            require(edf.groupby("cell_id").episode_interval_count.sum().eq(length).all(), "Episode partition differs")
            require(edf.groupby("cell_id").episode_duration_observed_years.sum().eq(length * 5).all(), "Year-duration partition differs")
            require(edf.groupby("cell_id").left_boundary_flag.sum().eq(1).all()
                    and edf.groupby("cell_id").right_boundary_flag.sum().eq(1).all(), "Episode boundary count differs")
            require(stf.groupby("cell_id").stage_interval_count.sum().eq(length).all(), "State duration differs")
            save_table(sdf, base / "cell_trajectories.parquet", inventory)
            save_table(edf, base / "episodes.parquet", inventory)
            save_table(stf, base / "stage_occupancy.parquet", inventory)
            summaries[window] = sdf
            totals["cell_window_summary_rows"] += len(sdf)
            totals["episode_rows"] += len(edf)
            totals["state_summary_rows"] += len(stf)
            matrix = transition_counts(wide[:, :length], metric, window)
            require(matrix.cell_count.sum() == n * (length - 1), "Window transition sum differs")
            matrix_parts.append(matrix)
            totals["primary_transition_events" if length == 7 else "full_transition_events"] += n * (length - 1)
            if metric in CORE:
                gis_frame = sdf.copy()
                for col in gis_frame.select_dtypes(include="bool"):
                    gis_frame[col] = gis_frame[col].astype("int8")
                save_table(gis_frame, output / "gis" / f"{STAGE_AXIS[metric]}_{window}_v1.csv", inventory)
                patterns = sdf.groupby("trajectory_pattern_code", observed=True).size().reset_index(name="cell_count")
                patterns["metric"], patterns["analysis_window"] = metric, window
                pattern_parts.append(patterns)
            del interval_frame, summary_rows, episode_rows, state_rows, edf, stf
        primary = summaries["primary"].drop(columns=["analysis_window", "metric", "stage_axis"])
        full = summaries["full_observed"].drop(columns=["analysis_window", "metric", "stage_axis"])
        comparison = primary.merge(full, on="cell_id", validate="one_to_one", suffixes=("_primary", "_full"))
        comparison["metric"] = metric
        comparison["stage_axis"] = STAGE_AXIS.get(metric, metric)
        comparison["typology_applied"] = metric in CORE
        comparison["pattern_changed_with_diagnostic"] = (
            comparison.trajectory_pattern_code_primary.ne(comparison.trajectory_pattern_code_full))
        comparison["terminal_primary_episode_continues_in_diagnostic"] = wide[:, 6] == wide[:, 7]
        comparison["diagnostic_creates_new_episode"] = wide[:, 6] != wide[:, 7]
        comparison["terminal_primary_episode_interval_count"] = [
            len(list(next(itertools.groupby(reversed(seq[:7])))[1])) for seq in wide]
        comparison["terminal_full_episode_interval_count"] = np.where(
            comparison.terminal_primary_episode_continues_in_diagnostic,
            comparison.terminal_primary_episode_interval_count + 1, 1)
        for field in ["episode_count", "max_episode_interval_count", "max_episode_duration_observed_years",
                      "stage_reentry_count", "activity_interruption_count", "activity_entry_count", "activity_exit_count"]:
            comparison[f"{field}_delta"] = (pd.to_numeric(comparison[f"{field}_full"])
                                                   - pd.to_numeric(comparison[f"{field}_primary"]))
        require(comparison.episode_count_delta.eq((wide[:, 6] != wide[:, 7]).astype(int)).all(),
                "Diagnostic episode count differs")
        require(comparison.stage_reentry_count_delta.isin([0, 1]).all(), "Diagnostic reentry count differs")
        # Independently restrict the source sequence and check the recorded primary sequence.
        require(all(json.loads(s) == list(seq[:7]) for s, seq in zip(comparison.sequence_json_primary, wide)),
                "Primary sequence is not an exact restriction")
        save_table(comparison, output / "tables" / metric / "primary_full_comparison.parquet", inventory)
        keep = ["cell_id", "metric", "stage_axis", "typology_applied", "trajectory_pattern_code_primary",
                "trajectory_pattern_code_full", "pattern_changed_with_diagnostic",
                "terminal_primary_episode_continues_in_diagnostic", "diagnostic_creates_new_episode",
                "terminal_primary_episode_interval_count", "terminal_full_episode_interval_count"]
        keep += [c for c in comparison if c.endswith("_delta")]
        comparisons.append(comparison[keep])
        print(f"  Completed both windows in {time.monotonic() - started:.1f}s", flush=True)
    matrix = pd.concat(matrix_parts, ignore_index=True)
    comparison = pd.concat(comparisons, ignore_index=True)
    save_table(matrix, output / "canonical_cell_state_transition_matrices_v1.csv", inventory)
    save_table(comparison, output / "canonical_cell_primary_full_comparison_v1.parquet", inventory)
    save_table(pd.concat(pattern_parts, ignore_index=True), output / "canonical_core_trajectory_pattern_counts_v1.csv", inventory)
    save_table(pd.DataFrame(limits), output / "canonical_phase4_frozen_class_specifications_v1.csv", inventory)
    require(totals["cell_window_summary_rows"] == n * 12 * 2, "Trajectory total differs")
    require(totals["interval_stage_rows"] == n * 12 * 15, "Interval-stage total differs")
    require(totals["primary_transition_events"] == n * 12 * 6, "Primary transition total differs")
    require(totals["full_transition_events"] == n * 12 * 7, "Full transition total differs")
    # ArcGIS text configuration for the four one-to-one core summaries.
    lines = []
    for item in inventory:
        path = Path(item["path"])
        if path.parent.name != "gis":
            continue
        frame = pd.read_csv(path, dtype={"cell_id": str})
        require(frame.cell_id.nunique() == n and len(frame) == n, "GIS join cardinality differs")
        lines += [f"[{path.name}]", "Format=CSVDelimited", "ColNameHeader=True",
                  "MaxScanRows=0"]
        for i, col in enumerate(frame.columns, 1):
            numeric = pd.api.types.is_numeric_dtype(frame[col])
            boolean = pd.api.types.is_bool_dtype(frame[col])
            integer = pd.api.types.is_integer_dtype(frame[col])
            kind = "Long" if boolean or integer else "Double" if numeric else "Text Width 1024"
            lines.append(f"Col{i}={col} {kind}")
        lines.append("")
    schema = output / "gis/schema.ini"
    schema.write_text("\n".join(lines), encoding="utf-8")
    inventory.append({"path": str(schema), "filename": schema.name, "rows": None,
                      "columns": None, "sha256": sha256(schema)})
    manifest = pd.DataFrame(inventory)
    manifest["relative_path"] = manifest.path.map(lambda s: str(Path(s).relative_to(output)))
    manifest.drop(columns="path").to_csv(output / "canonical_cell_trajectories_inventory_v1.csv", index=False,
                                        encoding="utf-8-sig")
    return totals, inventory


def self_test(integration=True):
    R, M, C, I = "replenishment_dominant", "mixed", "consolidation_dominant", "inactive"
    cases = [([R] * 7, "constant"), ([R, M, C], "monotonic_without_return"),
             ([M, C, R], "nonmonotonic_without_return"), ([R, C, R], "returning"),
             ([R, C, R, C], "recurrent"), ([R, I, R], "returning"),
             ([R, I, C], "monotonic_without_return"), ([I, C], "activity_change_without_ordinal_change"),
             ([I, C, I], "returning")]
    for seq, expected in cases:
        summary, episodes, _ = reconstruct(seq, CR, "primary")
        require(summary["trajectory_pattern_code"] == expected, f"Example failed: {seq}")
    s, e, _ = reconstruct([R] * 7, CR, "primary")
    require(e[0]["episode_position"] == "both_boundaries" and e[0]["persistent_episode_flag"], "Sole episode flags")
    s, e, _ = reconstruct([R, I, C], CR, "primary")
    require(s["activity_interruption_count"] == 1 and s["ordinal_path_crosses_off_axis_flag"]
            and s["direct_direction_change_count"] == 0, "Inactive interruption semantics")
    _, e, _ = reconstruct([R, I, R], CR, "primary")
    require(e[1]["isolated_inactivity_flag"] and not e[1]["isolated_activity_flag"], "Isolated inactivity semantics")
    _, e, _ = reconstruct([I, C, I], CR, "primary")
    require(e[1]["isolated_activity_flag"], "Isolated activity semantics")
    s, _, _ = reconstruct([R, M, C, I, R], CR, "primary")
    require(s["mediated_dominance_reversal_count"] == 2 and s["direct_dominance_reversal_count"] == 0,
            "Mediated dominance reversals")
    s, _, _ = reconstruct(["zero", "positive_low", "positive_high"], NAT, "primary")
    require(s["ordinal_direction"] == "increasing" and s["activity_entry_count"] == 1, "Magnitude zero rank")
    s, _, _ = reconstruct(["zero", "low_support", "positive_high"], NAT, "primary")
    require(s["trajectory_pattern_code"] == "support_limited" and s["activity_entry_count"] == 0,
            "Unknown support must not create a process event")
    s, _, _ = reconstruct(["zero", "low_support", "zero"], "nat_tmp_pas_any_share_endpoint", "primary")
    require(s["trajectory_pattern_code"] == "not_classified" and s["activity_entry_count"] is None,
            "Optional axis semantics must not be invented")
    exhaustive = 0
    for metric, labels in [(CR, [I, R, M, C]), (NAT, list(RANKS[NAT]))]:
        for seq in itertools.product(labels, repeat=5):
            summary, episodes, states = reconstruct(seq, metric, "primary")
            require(sum(s["stage_interval_count"] for s in states) == 5, "Exhaustive occupancy partition")
            require(summary["stage_reentry_count"] == len(episodes) - len(set(seq)), "Independent reentry identity")
            require(sum(e["left_boundary_flag"] for e in episodes) == 1
                    and sum(e["right_boundary_flag"] for e in episodes) == 1, "Exhaustive boundaries")
            exhaustive += 1
    primary, _, _ = reconstruct([R] * 7, CR, "primary")
    full, _, _ = reconstruct([R] * 7 + [C], CR, "full_observed")
    require(primary["trajectory_pattern_code"] == "constant" and full["trajectory_pattern_code"]
            == "monotonic_without_return", "Diagnostic-dependent classification")
    # Check exact ties and the difference between full-precision and rounded limits.
    fixture = pd.DataFrame({NAT: [0, 1e-9, 13.353057218357627, 357.7931682403865,
                                 np.nextafter(357.7931682403865, np.inf)]})
    limit = {"metric": NAT, "measure_type": "endpoint_area_ha", "support_field": "all_rows",
             "break_1": 13.353057218357627, "break_2": 357.7931682403865, "zero_tolerance": 1e-9}
    require(reproduce_classes(fixture, limit).tolist() == ["zero", "zero", "positive_low", "positive_moderate", "positive_high"],
            "Full-precision magnitude ties")
    fixture = pd.DataFrame({CR: [np.nan, -1 / 3, 1 / 3, -1, 1],
                            "gross_cr_activity_ha": [0, 1, 1, 1, 1], "cr_balance_defined": [0, 1, 1, 1, 1],
                            "cr_balance_state": [I, M, M, R, C]})
    require(reproduce_classes(fixture, {"metric": CR, "measure_type": "bounded_balance_index",
                                       "break_1": -1 / 3, "break_2": 1 / 3, "zero_tolerance": 1e-12}).tolist()
            == [I, M, M, R, C], "Balance boundary ties")
    rate_limits = []
    for metric, support in [
        ("consolidation_rate_initial_pasture", "consolidation_rate_defined"),
        ("replenishment_rate_initial_native", "replenishment_rate_defined"),
        ("nat_tmp_intensity_initial_native", "nat_tmp_intensity_defined"),
    ]:
        record = {"metric": metric, "measure_type": "relative_intensity", "support_field": support,
                  "break_1": 0.1, "break_2": 0.5, "zero_tolerance": 1e-12}
        rate_limits.append(record)
        frame = pd.DataFrame({metric: [np.nan, 0, 0.1, 0.5, 0.8], support: [0, 1, 1, 1, 1]})
        require(support in required_metric_columns([record]), "Rate support field omitted by column projection")
        require(reproduce_classes(frame, record).tolist() ==
                ["undefined", "zero", "positive_low", "positive_moderate", "positive_high"],
                "Rate classification/support regression")
    if integration:
        require(importlib.util.find_spec("pyarrow") is not None, "Self-test integration needs pyarrow")
        with tempfile.TemporaryDirectory(prefix="phase4_support_regression_") as td:
            fixture = pd.DataFrame({col: [1.0] for col in required_metric_columns(rate_limits)})
            path = Path(td) / "rates.parquet"
            fixture.to_parquet(path, index=False)
            projected = pd.read_parquet(path, columns=required_metric_columns(rate_limits))
            for record in rate_limits:
                reproduce_classes(projected, record)

        seqs = [[R] * 8, [R, R, M, C, C, I, C, R], [I, C, I, R, I, C, I, I]]
        rows = []
        for i, seq in enumerate(seqs):
            for j, (t0, t1) in enumerate(INTERVALS):
                row = {"cell_id": f"00{i}", "t0": t0, "t1": t1, "GRID_ID": str(i)}
                for metric in METRICS:
                    row[metric] = np.nan if metric == CR and seq[j] == I else float(j)
                    row[f"{metric}__class"] = seq[j] if metric == CR else (
                        ["zero", "positive_low", "positive_moderate", "positive_high"][j % 4])
                for col in CONTEXT:
                    row.setdefault(col, "synthetic" if col == "primary_biome" else 1.0)
                rows.append(row)
        with tempfile.TemporaryDirectory(prefix="phase4_selftest_") as td:
            totals, inventory = build_products(pd.DataFrame(rows), [], Path(td))
            require(totals["cell_window_summary_rows"] == 72, "Synthetic summary totals")
            for item in inventory:
                if item["filename"].endswith(".parquet"):
                    frame = pd.read_parquet(item["path"])
                    require(len(frame) == item["rows"], "Output round-trip row count")
                    if "cell_id" in frame:
                        require(set(frame.cell_id).issubset({"000", "001", "002"}), "Text IDs lost on round trip")
            comparison = pd.read_parquet(Path(td) / "tables" / CR / "primary_full_comparison.parquet")
            require(comparison.terminal_primary_episode_continues_in_diagnostic.tolist() == [True, False, True],
                    "Synthetic terminal episode linking")
    return {"status": "PASS", "exhaustive_sequences_checked": exhaustive,
            "integration_output_roundtrip": integration,
            "canonical_input_execution": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=Path, default=Path(os.environ.get(
        "CANONICAL_SPATIAL_PROJECT_DIR", "/content/drive/MyDrive/Trabalho/Contabilidade")))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if importlib.util.find_spec("pyarrow") is None:
        print("Installing missing dependency: pyarrow>=14", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyarrow>=14"])
    if args.self_test:
        print(json.dumps(self_test(), indent=2), flush=True)
        return
    try:
        from google.colab import drive
    except ImportError:
        drive = None
    if drive is not None and str(args.project_dir).startswith("/content/drive/"):
        drive.mount("/content/drive")
    print("CANONICAL CELL TRAJECTORIES — PHASE 4A SCRIPT REVISION 3", flush=True)
    print("FROZEN CLASS SUPPORT FIELDS: LOADED", flush=True)
    print("PRIMARY AND FULL SERIES: ENABLED; DIAGNOSTIC 2020–2025: INCLUDED", flush=True)
    print(f"Script version: {VERSION}\nProject directory: {args.project_dir}", flush=True)
    verification = self_test(integration=False)
    print("Sequence-engine verification: PASS", flush=True)
    panel, limits, inputs = load_inputs(args.project_dir)
    print("Canonical input hashes, keys and all 504 frozen class counts: PASS", flush=True)
    run_id = datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%S_%fZ")
    destination = args.project_dir / "spatial/phase4/trajectories_v1" / run_id
    require(not destination.exists(), "Run directory already exists")
    try:
        with tempfile.TemporaryDirectory(prefix="phase4a_") as td:
            stage = Path(td)
            totals, inventory = build_products(panel, limits, stage)
            # The script itself accompanies the products and is authenticated.
            script = Path(__file__).resolve()
            shutil.copy2(script, stage / script.name)
            script_hash = sha256(script)
            validation = {
                "validation_status": "PASS", "script_version": VERSION,
                "decision": "010_stage_definition_and_trajectory_typology.md",
                "run_id": run_id, "completed_utc": datetime.now(timezone.utc).isoformat(),
                "script_sha256": script_hash, "inputs": inputs,
                "scope": {"cells": EXPECTED_CELLS, "descriptive_metrics": METRICS,
                          "typology_metrics": sorted(CORE), "primary_intervals": 7, "full_intervals": 8,
                          "diagnostic_interval": [2020, 2025], "diagnostic_included": True,
                          "class_limits_refitted": False, "gee_used": False,
                          "duration_interpretation": "coverage of consecutive quinquennial stage assignments",
                          "spatial_relocation_inference": False},
                "structure": totals, "sequence_engine_verification": verification,
                "checks": {"input_authentication": True, "upstream_validations_pass": True,
                           "canonical_balanced_keys": True, "frozen_classes_and_504_counts_match": True,
                           "complete_support_core_axes": True, "episode_expansion_matches_source": True,
                           "duration_and_state_partitions_close": True, "boundaries_and_reentries_close": True,
                           "primary_is_exact_restriction": True, "diagnostic_comparison_closes": True,
                           "transition_counts_and_marginals_close": True, "four_gis_tables_one_to_one": True,
                           "all_written_outputs_authenticated": True},
                "software": {"python": sys.version, **{p: importlib.metadata.version(p)
                             for p in ["pandas", "numpy", "pyarrow"]}},
                "outputs": {item["path"].removeprefix(str(stage) + "/"): {
                    "sha256": item["sha256"], "rows": item["rows"], "columns": item["columns"]}
                    for item in inventory},
            }
            validation["outputs"]["canonical_cell_trajectories_inventory_v1.csv"] = {
                "sha256": sha256(stage / "canonical_cell_trajectories_inventory_v1.csv")}
            validation["outputs"][script.name] = {"sha256": script_hash}
            dump_json(stage / "canonical_cell_trajectories_validation_v1.json", validation)
            # Isolated run directories prevent a failed rerun mixing products with a prior PASS.
            destination.mkdir(parents=True)
            pending = dict(validation, validation_status="COPYING")
            dump_json(destination / "canonical_cell_trajectories_validation_v1.json", pending)
            print(f"Copying authenticated outputs to: {destination}", flush=True)
            for p in sorted(stage.rglob("*")):
                if not p.is_file() or p.name == "canonical_cell_trajectories_validation_v1.json":
                    continue
                target = destination / p.relative_to(stage)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, target)
                require(sha256(target) == sha256(p), f"Copied output hash mismatch: {target}")
            shutil.copy2(stage / "canonical_cell_trajectories_validation_v1.json",
                         destination / "canonical_cell_trajectories_validation_v1.json")
            dump_json(destination.parent / "latest_successful_run_v1.json", {
                "run_id": run_id, "output_directory": str(destination), "validation_status": "PASS",
                "validation_sha256": sha256(destination / "canonical_cell_trajectories_validation_v1.json")})
        print("PHASE 4A CELL TRAJECTORY BUILD COMPLETE\nValidation status: PASS", flush=True)
        print(f"Cells: {EXPECTED_CELLS:,}\nDescriptive metrics: 12\nTypology axes: 2\nWindows per metric: 2", flush=True)
        print(f"Output directory: {destination}\nValidation: {destination / 'canonical_cell_trajectories_validation_v1.json'}", flush=True)
        print(f"Inventory: {destination / 'canonical_cell_trajectories_inventory_v1.csv'}", flush=True)
        print("No GEE processing. Canonical run requires review of the validation record before acceptance.", flush=True)
    except Exception as exc:
        if destination.exists():
            dump_json(destination / "canonical_cell_trajectories_validation_v1.json", {
                "validation_status": "FAIL", "script_version": VERSION, "run_id": run_id,
                "error": str(exc)})
        raise


if __name__ == "__main__":
    main()

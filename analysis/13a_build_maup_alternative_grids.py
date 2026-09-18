"""Build and validate the Phase 8A alternative MAUP grids, script revision 2.

Colab
------
%pip install -q pyarrow geopandas shapely scipy pyogrio
%run /content/13a_build_maup_alternative_grids_v2.py

The script reads the accepted canonical spatial support, infers the equal-area
hexagonal lattice, and creates three alternative grids over the fixed union of
the 24,889 canonical cells:

* approximately 10,000 ha, original origin;
* approximately 40,000 ha, original origin; and
* approximately 20,000 ha, translated by half of each lattice basis vector.

No land-cover or process value is read or calculated in Phase 8A.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from scipy.spatial import cKDTree
from shapely.geometry import Polygon


VERSION = "phase8a-maup-alternative-grids-script-v2"
EXPECTED_SOURCE_SHA256 = (
    "22425834aee2826f5261fdbda959719a4e46d7c6589a91417cc0328c3112cecc"
)
EXPECTED_SOURCE_CELLS = 24_889
WGS84_CRS = "EPSG:4326"
AEA_CRS = (
    "+proj=aea +lat_0=-32 +lon_0=-60 +lat_1=-5 +lat_2=-42 "
    "+x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs"
)

BASE_AREA_HA = 20_000.0
AREA_SCALE_TOLERANCE = 0.01
NEIGHBOR_DISTANCE_TOLERANCE = 0.08
LATTICE_P99_RESIDUAL_FRACTION = 0.01
LATTICE_MAX_RESIDUAL_FRACTION = 0.03
SUPPORT_CLOSURE_RELATIVE_TOLERANCE = 2e-7
SUPPORT_AREA_TOLERANCE_M2 = 1e-3
BATCH_COUNT = 8

GRID_SPECS = (
    {
        "grid_code": "hex10k_base",
        "area_multiplier": 0.5,
        "shift_q": 0.0,
        "shift_r": 0.0,
        "description": "Half-area scale grid with canonical origin and orientation.",
    },
    {
        "grid_code": "hex20k_shift",
        "area_multiplier": 1.0,
        "shift_q": 0.5,
        "shift_r": 0.5,
        "description": "Canonical-area grid shifted by half of both lattice basis vectors.",
    },
    {
        "grid_code": "hex40k_base",
        "area_multiplier": 2.0,
        "shift_q": 0.0,
        "shift_r": 0.0,
        "description": "Double-area scale grid with canonical origin and orientation.",
    },
)


def require(condition: bool, message: str) -> None:
    if not bool(condition):
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def angle_modulo_mean(angles: np.ndarray, period: float) -> float:
    z = np.exp(1j * (2.0 * np.pi / period) * angles).mean()
    require(abs(z) > 0.5, "Hex-lattice orientation is not sufficiently concentrated")
    angle = np.angle(z) * period / (2.0 * np.pi)
    return float(angle % period)


def regular_hexagons(
    centers_x: np.ndarray,
    centers_y: np.ndarray,
    side_m: float,
    vertex_angle_rad: float,
):
    angles = vertex_angle_rad + np.arange(6, dtype=float) * np.pi / 3.0
    vertices = np.empty((len(centers_x), 6, 2), dtype=float)
    vertices[:, :, 0] = centers_x[:, None] + side_m * np.cos(angles)[None, :]
    vertices[:, :, 1] = centers_y[:, None] + side_m * np.sin(angles)[None, :]
    return shapely.polygons(vertices)


def infer_canonical_lattice(source_aea: gpd.GeoDataFrame) -> dict:
    centroids = source_aea.geometry.centroid
    coordinates = np.column_stack((centroids.x.to_numpy(), centroids.y.to_numpy()))
    require(len(coordinates) >= 100, "Too few source cells for lattice inference")

    tree = cKDTree(coordinates)
    distances, indices = tree.query(coordinates, k=7)
    nearest = distances[:, 1]
    neighbor_distance = float(np.median(nearest))
    require(np.isfinite(neighbor_distance) and neighbor_distance > 0, "Invalid nearest-neighbor distance")

    lower = neighbor_distance * (1.0 - NEIGHBOR_DISTANCE_TOLERANCE)
    upper = neighbor_distance * (1.0 + NEIGHBOR_DISTANCE_TOLERANCE)
    vectors = []
    for row in range(len(coordinates)):
        for distance, column in zip(distances[row, 1:], indices[row, 1:]):
            if lower <= distance <= upper:
                vectors.append(coordinates[column] - coordinates[row])
    require(len(vectors) >= len(coordinates), "Insufficient nearest-neighbor vectors")
    vectors = np.asarray(vectors)
    neighbor_angles = np.arctan2(vectors[:, 1], vectors[:, 0])
    neighbor_angle = angle_modulo_mean(neighbor_angles, np.pi / 3.0)
    vertex_angle = neighbor_angle - np.pi / 6.0

    polygon_area_m2 = source_aea.geometry.area.to_numpy(float)
    median_source_area = float(np.median(polygon_area_m2))
    source_side_from_area = math.sqrt(2.0 * median_source_area / (3.0 * math.sqrt(3.0)))
    source_side_from_centers = neighbor_distance / math.sqrt(3.0)
    side_relative_difference = abs(source_side_from_centers - source_side_from_area) / source_side_from_area
    require(
        side_relative_difference <= AREA_SCALE_TOLERANCE,
        "Canonical center spacing and polygon area do not describe one regular hex lattice",
    )

    # Center spacing governs tessellation; the implied area is retained as the
    # exact Phase 8A reference area.
    side_m = source_side_from_centers
    implied_area_m2 = 3.0 * math.sqrt(3.0) * side_m * side_m / 2.0
    implied_area_ha = implied_area_m2 / 10_000.0
    require(
        abs(implied_area_ha - BASE_AREA_HA) / BASE_AREA_HA <= AREA_SCALE_TOLERANCE,
        "Inferred canonical area is not consistent with the 20,000-ha reference",
    )

    central = np.array([np.median(coordinates[:, 0]), np.median(coordinates[:, 1])])
    anchor_index = int(np.argmin(np.linalg.norm(coordinates - central, axis=1)))
    anchor = coordinates[anchor_index]

    basis_q = neighbor_distance * np.array([math.cos(neighbor_angle), math.sin(neighbor_angle)])
    basis_r = neighbor_distance * np.array(
        [math.cos(neighbor_angle + np.pi / 3.0), math.sin(neighbor_angle + np.pi / 3.0)]
    )
    basis = np.column_stack((basis_q, basis_r))
    coefficients = np.linalg.solve(basis, (coordinates - anchor).T).T
    rounded = np.rint(coefficients)
    reconstructed = anchor + rounded @ basis.T
    residuals = np.linalg.norm(coordinates - reconstructed, axis=1)
    residual_p99 = float(np.quantile(residuals, 0.99))
    residual_max = float(residuals.max())
    require(
        residual_p99 <= neighbor_distance * LATTICE_P99_RESIDUAL_FRACTION,
        "Canonical-centroid p99 residual exceeds the lattice tolerance",
    )
    require(
        residual_max <= neighbor_distance * LATTICE_MAX_RESIDUAL_FRACTION,
        "Canonical-centroid maximum residual exceeds the lattice tolerance",
    )

    return {
        "anchor_x_aea": float(anchor[0]),
        "anchor_y_aea": float(anchor[1]),
        "anchor_source_index": anchor_index,
        "neighbor_angle_rad": float(neighbor_angle),
        "vertex_angle_rad": float(vertex_angle),
        "neighbor_distance_m": neighbor_distance,
        "side_length_m": side_m,
        "implied_reference_area_ha": implied_area_ha,
        "source_median_area_ha": median_source_area / 10_000.0,
        "side_length_relative_difference": side_relative_difference,
        "lattice_residual_p99_m": residual_p99,
        "lattice_residual_max_m": residual_max,
        "basis_q": basis_q,
        "basis_r": basis_r,
    }


def candidate_axial_bounds(
    source_bounds: np.ndarray,
    anchor: np.ndarray,
    basis: np.ndarray,
    side_m: float,
) -> tuple[int, int, int, int]:
    minx, miny, maxx, maxy = map(float, source_bounds)
    margin = 2.5 * side_m
    corners = np.array(
        [
            [minx - margin, miny - margin],
            [minx - margin, maxy + margin],
            [maxx + margin, miny - margin],
            [maxx + margin, maxy + margin],
        ]
    )
    coefficients = np.linalg.solve(basis, (corners - anchor).T).T
    q_min = math.floor(float(coefficients[:, 0].min())) - 2
    q_max = math.ceil(float(coefficients[:, 0].max())) + 2
    r_min = math.floor(float(coefficients[:, 1].min())) - 2
    r_max = math.ceil(float(coefficients[:, 1].max())) + 2
    return q_min, q_max, r_min, r_max


def calculate_domain_support(
    candidates: gpd.GeoDataFrame,
    source_aea: gpd.GeoDataFrame,
) -> pd.Series:
    joined = gpd.sjoin(
        candidates[["candidate_index", "geometry"]],
        source_aea[["geometry"]],
        how="inner",
        predicate="intersects",
    )
    require(len(joined) > 0, "Alternative grid does not intersect the canonical domain")
    right_geometry = source_aea.geometry.iloc[joined["index_right"].to_numpy(int)].array
    intersections = shapely.intersection(joined.geometry.array, right_geometry)
    areas = shapely.area(intersections)
    table = pd.DataFrame(
        {
            "candidate_index": joined["candidate_index"].to_numpy(int),
            "intersection_area_m2": areas,
        }
    )
    table = table[table.intersection_area_m2.gt(SUPPORT_AREA_TOLERANCE_M2)]
    return table.groupby("candidate_index", sort=False).intersection_area_m2.sum()


def build_alternative_grid(
    source_aea: gpd.GeoDataFrame,
    lattice: dict,
    spec: dict,
) -> tuple[gpd.GeoDataFrame, dict]:
    scale = math.sqrt(float(spec["area_multiplier"]))
    side_m = float(lattice["side_length_m"]) * scale
    neighbor_distance = math.sqrt(3.0) * side_m
    angle = float(lattice["neighbor_angle_rad"])
    basis_q = neighbor_distance * np.array([math.cos(angle), math.sin(angle)])
    basis_r = neighbor_distance * np.array(
        [math.cos(angle + np.pi / 3.0), math.sin(angle + np.pi / 3.0)]
    )
    basis = np.column_stack((basis_q, basis_r))

    canonical_basis_q = np.asarray(lattice["basis_q"], dtype=float)
    canonical_basis_r = np.asarray(lattice["basis_r"], dtype=float)
    anchor = np.array([lattice["anchor_x_aea"], lattice["anchor_y_aea"]], dtype=float)
    anchor = anchor + float(spec["shift_q"]) * canonical_basis_q
    anchor = anchor + float(spec["shift_r"]) * canonical_basis_r

    q_min, q_max, r_min, r_max = candidate_axial_bounds(
        source_aea.total_bounds, anchor, basis, side_m
    )
    q_values = np.arange(q_min, q_max + 1, dtype=np.int32)
    r_values = np.arange(r_min, r_max + 1, dtype=np.int32)
    q_grid, r_grid = np.meshgrid(q_values, r_values, indexing="ij")
    q = q_grid.ravel()
    r = r_grid.ravel()
    centers = anchor + q[:, None] * basis_q + r[:, None] * basis_r
    geometries = regular_hexagons(
        centers[:, 0], centers[:, 1], side_m, float(lattice["vertex_angle_rad"])
    )
    candidates = gpd.GeoDataFrame(
        {
            "candidate_index": np.arange(len(q), dtype=np.int64),
            "axial_q": q,
            "axial_r": r,
            "centroid_x_aea": centers[:, 0],
            "centroid_y_aea": centers[:, 1],
        },
        geometry=geometries,
        crs=AEA_CRS,
    )

    support = calculate_domain_support(candidates, source_aea)
    selected = candidates[candidates.candidate_index.isin(support.index)].copy()
    selected["vector_domain_support_ha"] = (
        selected.candidate_index.map(support).astype(float) / 10_000.0
    )
    nominal_area_m2 = 3.0 * math.sqrt(3.0) * side_m * side_m / 2.0
    nominal_area_ha = nominal_area_m2 / 10_000.0
    selected["nominal_area_ha"] = nominal_area_ha
    selected["domain_support_fraction"] = (
        selected.vector_domain_support_ha / nominal_area_ha
    ).clip(lower=0.0)
    require(
        selected.domain_support_fraction.max() <= 1.0 + 2e-7,
        "A generated cell has domain support greater than its nominal area",
    )

    selected.sort_values(["axial_q", "axial_r"], inplace=True, ignore_index=True)
    selected.insert(0, "maup_cell_id", np.arange(1, len(selected) + 1, dtype=np.int64))
    selected.insert(
        1,
        "maup_uid",
        [f"{spec['grid_code']}__q{a:+d}__r{b:+d}" for a, b in zip(selected.axial_q, selected.axial_r)],
    )
    selected.insert(2, "grid_code", spec["grid_code"])
    selected["batch_id"] = selected.maup_cell_id.mod(BATCH_COUNT).astype(np.int8)
    selected["grid_version"] = VERSION
    selected["geometry_valid"] = selected.geometry.is_valid.astype(np.int8)
    require(selected.geometry_valid.eq(1).all(), "Invalid generated geometry")
    require(selected.maup_cell_id.is_unique and selected.maup_uid.is_unique, "Duplicate grid identifiers")

    source_area_m2 = float(source_aea.geometry.area.sum())
    support_area_m2 = float(selected.vector_domain_support_ha.sum() * 10_000.0)
    closure_relative_difference = abs(support_area_m2 - source_area_m2) / source_area_m2
    require(
        closure_relative_difference <= SUPPORT_CLOSURE_RELATIVE_TOLERANCE,
        "Alternative-grid support does not close to the fixed canonical domain",
    )

    summary = {
        "grid_code": spec["grid_code"],
        "description": spec["description"],
        "cell_count": int(len(selected)),
        "candidate_cell_count": int(len(candidates)),
        "nominal_area_ha": nominal_area_ha,
        "side_length_m": side_m,
        "neighbor_distance_m": neighbor_distance,
        "shift_q_canonical_basis": float(spec["shift_q"]),
        "shift_r_canonical_basis": float(spec["shift_r"]),
        "vector_domain_support_total_ha": float(selected.vector_domain_support_ha.sum()),
        "fixed_domain_area_ha": source_area_m2 / 10_000.0,
        "support_closure_relative_difference": closure_relative_difference,
        "minimum_support_fraction": float(selected.domain_support_fraction.min()),
        "median_support_fraction": float(selected.domain_support_fraction.median()),
        "maximum_support_fraction": float(selected.domain_support_fraction.max()),
        "cells_support_ge_10pct": int(selected.domain_support_fraction.ge(0.10).sum()),
        "cells_support_ge_25pct": int(selected.domain_support_fraction.ge(0.25).sum()),
        "cells_support_ge_50pct": int(selected.domain_support_fraction.ge(0.50).sum()),
        "cells_support_ge_75pct": int(selected.domain_support_fraction.ge(0.75).sum()),
        "cells_support_ge_90pct": int(selected.domain_support_fraction.ge(0.90).sum()),
    }
    return selected, summary


def support_distribution(grid: gpd.GeoDataFrame, grid_code: str) -> list[dict]:
    bins = [0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 0.999999, np.inf]
    labels = [
        "gt0_lt10pct",
        "10_lt25pct",
        "25_lt50pct",
        "50_lt75pct",
        "75_lt90pct",
        "90_lt100pct",
        "approximately_full",
    ]
    category = pd.cut(
        grid.domain_support_fraction,
        bins=bins,
        labels=labels,
        include_lowest=False,
        right=False,
    )
    counts = category.value_counts(sort=False)
    return [
        {
            "grid_code": grid_code,
            "support_fraction_class": label,
            "cells": int(counts.get(label, 0)),
            "cell_fraction": float(counts.get(label, 0) / len(grid)),
        }
        for label in labels
    ]


def public_columns() -> list[str]:
    return [
        "maup_cell_id",
        "maup_uid",
        "grid_code",
        "batch_id",
        "axial_q",
        "axial_r",
        "nominal_area_ha",
        "vector_domain_support_ha",
        "domain_support_fraction",
        "centroid_x_aea",
        "centroid_y_aea",
        "geometry_valid",
        "grid_version",
        "geometry",
    ]


def export_grid(grid_aea: gpd.GeoDataFrame, output: Path, grid_code: str) -> list[Path]:
    wgs84 = grid_aea[public_columns()].to_crs(WGS84_CRS)
    paths = [
        output / f"maup_grid_{grid_code}_v1.parquet",
        output / f"maup_grid_{grid_code}_v1.gpkg",
        output / f"maup_grid_{grid_code}_v1.geojson",
    ]
    wgs84.to_parquet(paths[0], index=False, compression="zstd")
    wgs84.to_file(paths[1], layer=grid_code, driver="GPKG", index=False)
    wgs84.to_file(paths[2], driver="GeoJSON", index=False)
    return paths


def verify_geometry_engine() -> None:
    side = math.sqrt(2.0 * BASE_AREA_HA * 10_000.0 / (3.0 * math.sqrt(3.0)))
    neighbor = math.sqrt(3.0) * side
    neighbor_angle = 0.19
    vertex_angle = neighbor_angle - math.pi / 6.0
    basis_q = neighbor * np.array([math.cos(neighbor_angle), math.sin(neighbor_angle)])
    basis_r = neighbor * np.array(
        [math.cos(neighbor_angle + math.pi / 3.0), math.sin(neighbor_angle + math.pi / 3.0)]
    )
    # The production inference deliberately requires at least 100 source
    # cells. Revision 1 created only 25 synthetic cells here and therefore
    # stopped before testing the engine or reading the canonical input.
    q, r = np.meshgrid(np.arange(-6, 7), np.arange(-6, 7), indexing="ij")
    centers = q.ravel()[:, None] * basis_q + r.ravel()[:, None] * basis_r
    polygons = regular_hexagons(centers[:, 0], centers[:, 1], side, vertex_angle)
    source = gpd.GeoDataFrame(
        {"cell_id": np.arange(len(polygons))}, geometry=polygons, crs=AEA_CRS
    )
    inferred = infer_canonical_lattice(source)
    require(
        abs(inferred["implied_reference_area_ha"] - BASE_AREA_HA) / BASE_AREA_HA < 1e-10,
        "Synthetic reference area failed",
    )
    test_spec = {
        "grid_code": "synthetic_shift",
        "area_multiplier": 1.0,
        "shift_q": 0.5,
        "shift_r": 0.5,
        "description": "Synthetic test",
    }
    test_grid, summary = build_alternative_grid(source, inferred, test_spec)
    require(len(test_grid) > 0, "Synthetic shifted grid is empty")
    require(
        summary["support_closure_relative_difference"] <= SUPPORT_CLOSURE_RELATIVE_TOLERANCE,
        "Synthetic fixed-domain closure failed",
    )
    print("Geometry-engine verification: PASS", flush=True)


def default_project_dir() -> Path:
    return Path("/content/drive/MyDrive/Trabalho/Contabilidade")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", type=Path, default=default_project_dir())
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--self-test-only", action="store_true")
    return parser.parse_args()


def mount_drive_if_needed(project_dir: Path) -> None:
    if str(project_dir).startswith("/content/drive/") and not project_dir.exists():
        try:
            from google.colab import drive

            drive.mount("/content/drive")
        except ImportError:
            pass


def main() -> None:
    args = parse_args()
    print("CANONICAL MAUP ALTERNATIVE GRIDS — PHASE 8A SCRIPT REVISION 2", flush=True)
    print("SYNTHETIC TEST POPULATION FIX: ENABLED", flush=True)
    print("FIXED CANONICAL DOMAIN; PROCESS METRICS NOT COMPUTED", flush=True)
    print("Script version:", VERSION, flush=True)
    verify_geometry_engine()
    if args.self_test_only:
        print("SELF-TEST ONLY COMPLETE", flush=True)
        return

    mount_drive_if_needed(args.project_dir)
    source_path = args.project_dir / "spatial/phase1/canonical_spatial_support_v1.parquet"
    output = args.output_dir or args.project_dir / "spatial/phase8/maup_grids_v1"
    output.mkdir(parents=True, exist_ok=True)

    require(source_path.is_file(), f"Missing source: {source_path}")
    source_hash = sha256(source_path)
    require(source_hash == EXPECTED_SOURCE_SHA256, "Canonical spatial-support hash differs")

    source = gpd.read_parquet(source_path)
    require(len(source) == EXPECTED_SOURCE_CELLS, "Canonical source cell count differs")
    require(source.cell_id.nunique() == EXPECTED_SOURCE_CELLS, "Canonical cell_id is not unique")
    require(source.crs is not None, "Canonical spatial support has no CRS")
    require(source.geometry.notna().all() and source.geometry.is_valid.all(), "Invalid source geometry")
    source_aea = source[["cell_id", "geometry"]].to_crs(AEA_CRS).reset_index(drop=True)
    require(not source_aea.geometry.is_empty.any(), "Empty projected source geometry")

    lattice = infer_canonical_lattice(source_aea)
    lattice_json = {
        key: (
            value.tolist() if isinstance(value, np.ndarray) else value
        )
        for key, value in lattice.items()
    }

    all_paths: list[Path] = []
    summaries: list[dict] = []
    support_rows: list[dict] = []
    for spec in GRID_SPECS:
        print("Building:", spec["grid_code"], flush=True)
        grid, summary = build_alternative_grid(source_aea, lattice, spec)
        summaries.append(summary)
        support_rows.extend(support_distribution(grid, spec["grid_code"]))
        all_paths.extend(export_grid(grid, output, spec["grid_code"]))
        print(
            "  cells:", f"{len(grid):,}",
            "| nominal ha:", f"{summary['nominal_area_ha']:,.3f}",
            "| closure:", f"{summary['support_closure_relative_difference']:.3e}",
            flush=True,
        )

    summary_path = output / "canonical_maup_grid_summary_v1.csv"
    support_path = output / "canonical_maup_grid_support_distribution_v1.csv"
    pd.DataFrame(summaries).to_csv(summary_path, index=False, encoding="utf-8-sig", float_format="%.17g")
    pd.DataFrame(support_rows).to_csv(support_path, index=False, encoding="utf-8-sig", float_format="%.17g")
    all_paths.extend([summary_path, support_path])

    design = {
        "script_version": VERSION,
        "fixed_domain": "union of the 24,889 canonical Phase 1 cells",
        "fixed_domain_area_source": "projected canonical geometries in the project AEA CRS",
        "source_sha256": source_hash,
        "source_cells": EXPECTED_SOURCE_CELLS,
        "crs_aea": AEA_CRS,
        "crs_public_geometry": WGS84_CRS,
        "grid_specs": list(GRID_SPECS),
        "lattice": lattice_json,
        "support_threshold_decision": "deferred; Phase 8A reports the geometric distribution only",
        "process_metrics_computed": False,
    }
    design_path = output / "canonical_maup_grid_design_v1.json"
    write_json(design_path, design)
    all_paths.append(design_path)

    validation = {
        "validation_status": "PASS",
        "script_version": VERSION,
        "execution_utc": datetime.now(timezone.utc).isoformat(),
        "script_sha256": sha256(Path(__file__)),
        "input": {
            "path": str(source_path),
            "sha256": source_hash,
            "cells": EXPECTED_SOURCE_CELLS,
        },
        "lattice": lattice_json,
        "grids": summaries,
        "checks": {
            "geometry_engine_verification": True,
            "authenticated_canonical_source": True,
            "canonical_population": True,
            "aea_lattice_inferred": True,
            "reference_area_consistent_with_20000_ha": True,
            "unique_grid_identifiers": True,
            "valid_generated_geometries": True,
            "fixed_domain_support_closure": True,
            "support_threshold_not_selected": True,
            "no_process_metrics_computed": True,
        },
        "outputs": {
            path.name: {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
            for path in all_paths
        },
    }
    validation_path = output / "canonical_maup_grid_validation_v1.json"
    write_json(validation_path, validation)

    inventory_rows = []
    for path in all_paths + [validation_path]:
        rows = None
        if path.suffix.lower() == ".csv":
            rows = len(pd.read_csv(path))
        elif path.suffix.lower() in {".parquet", ".gpkg", ".geojson"}:
            rows = int(next(x["cell_count"] for x in summaries if x["grid_code"] in path.name))
        inventory_rows.append(
            {
                "relative_path": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "rows": rows,
            }
        )
    inventory_path = output / "canonical_maup_grid_inventory_v1.csv"
    pd.DataFrame(inventory_rows).to_csv(inventory_path, index=False, encoding="utf-8-sig")

    portable_paths = all_paths + [validation_path, inventory_path]
    zip_path = output / "canonical_maup_alternative_grids_v1.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in portable_paths:
            archive.write(path, arcname=path.name)

    print("PHASE 8A ALTERNATIVE GRIDS COMPLETE — VALIDATION PASS", flush=True)
    print("Output:", output, flush=True)
    for summary in summaries:
        print(
            summary["grid_code"],
            "| cells:", f"{summary['cell_count']:,}",
            "| support >=50%:", f"{summary['cells_support_ge_50pct']:,}",
            flush=True,
        )
    print("Validation:", validation_path, flush=True)
    print("Inventory:", inventory_path, flush=True)
    print("Portable ZIP:", zip_path, flush=True)


if __name__ == "__main__":
    main()

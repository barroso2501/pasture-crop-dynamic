# High NAT–TMP continuous cohort comparison validation

- **Date:** 2026-09-15.
- **Status:** Executed comparison; numerical checks PASS and figure layout inspected.
- **Version:** `phase4a-high-nat-tmp-continuous-v1`.
- **Executed UTC:** `2026-09-15T15:27:06.667947+00:00`.
- **Script SHA-256:** `b779ae002c31db979e1a29b92025c8079a64e1f67ffea75e55c241a009a2541a`.
- **Scope:** Descriptive extension of the accepted Phase 4A run; not a new state design or spatial inference.

## Received and authenticated inputs

The source is `drive-download-20260915T151612Z-1-001.zip`, containing eight GIS
08c cell-interval tables, the original validation JSON, manifest and dictionary.
The transport ZIP was repacked by Drive; authenticate component hashes rather
than expecting its bytes to match the original 08c portable ZIP.

Every received table has 24,889 rows and 78 columns. Its hash matches the
export JSON and manifest. The manifest and dictionary hashes match as well.
The received export JSON records PASS for all 14 source checks. Underlying
metric/class hashes match the previously accepted Phase 4A inputs. Missing
schema bytes in this transport package were not required for numerical reading;
new GIS tables have their own corrected schema.

| File | SHA-256 |
|---|---|
| `canonical_gis_interval_tables_manifest_v1.csv` | `0a9a8d11cb3a19e0a499d35b9a046411c3c95ab8f34bae89559ebb70ccea90e3` |
| `canonical_gis_interval_fields_v1.csv` | `3fa71bfe3a712fae598e305dd7f40b5583aa49c9e05d0190a5c1da8a59c2a16e` |
| `canonical_gis_metrics_classes_1985_1990_v1.csv` | `a117bd01012ea6d5c6296634606c8b6efd2b1e244c8319d55c5120d5a48c22d1` |
| `canonical_gis_metrics_classes_1990_1995_v1.csv` | `94c458fdde49e0d63836716fe4e780a4ee4c10e9ff2937938efc7a4967bad7cb` |
| `canonical_gis_metrics_classes_1995_2000_v1.csv` | `206a94d5bbf25c758dbd213993209cdcf4a32258354fe51f00574dca64168fc3` |
| `canonical_gis_metrics_classes_2000_2005_v1.csv` | `567184977e98a35a1dd3ec7eb8babdf3724ae1dc8f97d0a038a43b0af41dc275` |
| `canonical_gis_metrics_classes_2005_2010_v1.csv` | `da715dddb7514a671fb6161490d1c52010db660a374e508fdd642a38b3611f87` |
| `canonical_gis_metrics_classes_2010_2015_v1.csv` | `7665a4b6f0f8231712340f8538ec710e0669fd81f30a546bd5b54d5d27232b3d` |
| `canonical_gis_metrics_classes_2015_2020_v1.csv` | `255464f72f5145ef09c6d1dc22c38089e0c562a6f17e67e807559471a8fced96` |
| `canonical_gis_metrics_classes_2020_2025_v1.csv` | `104b05e0aac41de7c701ec1912f27ea02cf02e4b77c1083db94067b368e88852` |
| `canonical_gis_interval_tables_validation_v1.json` | `130a9d8652f51f232c0d4f0a09e6ceb1d6caac8b0b7fb6a705e2b455dbbd12f3` |


## Executed numerical checks

All 16 comparison checks in
`high_nat_tmp_continuous_validation_v1.json` passed. They establish:

- transport CRC integrity, no duplicate archive basenames and component hashes;
- upstream identity and accepted export version;
- 199,112 unique balanced cell-interval records with eight fixed populations;
- stable coordinates, biome labels, cell area and biome fractions;
- finite, nonnegative absolute process and stock areas;
- gross/net C–R identities and nested pasture-trajectory area identities;
- exactly 2,598 primary-cohort cells and 20,784 selected records;
- diagnostic flag preservation without retrospective cohort expansion;
- endpoint areas partition exactly by primary-biome label and C–R state;
- finite projected weighted centers;
- primary endpoint sum 8,010,398.701347958 ha reproduces prior exploration
  within declared CSV serialization tolerance;
- all products written and eight one-to-one GIS tables defined without the
  unsupported CharacterSet schema option.

Identity comparisons allow 1e-10 relative and 1e-6 ha absolute tolerance for
15-significant-digit CSV serialization. Class labels are reused without
reclassification at rounded boundaries.

## Independent output review

Selected output CSVs were reread, their cell IDs and eight-record-per-cell
partition verified, and period endpoint sums independently reproduced. The
eight GIS files each have 2,598 unique text IDs. All schema column positions
and field names match their CSV headers; `cell_id` remains text and no
CharacterSet line is present. No live ArcGIS opening retest is asserted.

All three figure layouts were inspected. A preliminary overlap between the
spatial panel's colorbar label and explanatory note was corrected and the
figure regenerated. The executed source hash and output record identify the
final figure generation.

## Interpretation boundaries

No statistical trend, cluster or causal claim is validated here. Cell-center
weighted locations approximate the spatial distribution of endpoint hectares,
not exact converted-pixel centroids. Primary-biome grouping does not allocate
conversion to the inside of each biome in mixed cells. Pooled trajectory shares
are ratios of sums, and absence of detected pasture is not direct-conversion
proof. Summed interval areas are not deduplicated unique-pixel areas.

The numerical comparison confirms a 2000–2005 endpoint peak, changes in relative
cohort contribution and aggregate C–R balance, and the diagnostic results. The
substantive analysis is in `docs/analysis/high_nat_tmp_continuous_comparison_v1.md`.
Original accepted validation JSONs are preserved, not edited to insert these
new checks. New output hashes are in the separate comparison JSON.

## Output storage and software

Results are in the delivered `results/` folder. Compact tables and validation
can be tracked in GitHub; the selected full panel and per-period GIS exports
can remain external, identified by the comparison JSON.

- pandas: 2.2.3.
- NumPy: 2.3.5.
- matplotlib: 3.10.8.
- pyproj: 3.8.0.

No upstream reprocessing was performed or required.

# Legacy hash fields — meaning and migration

Date: 2026-10-12. This dictionary clarifies the unchanged v3 closure records. It does not rewrite accepted JSONs or invent missing dependency paths.

| Legacy field | Object identified | What it does not identify | Future explicit name |
| --- | --- | --- | --- |
| `rq2_validation_sha256` | Accepted RQ2 validation JSON dependency used by the closure validator, as described in the accepted full-closure record | Evidence matrix, cell CSV, GEE source text or complete execution identity | `rq2_dependency_validation_json_sha256` |
| `output_sha256` | Exact final closure CSV bytes named in `output_csv` | Validation JSON or matrix | Keep the object filename and hash together |
| `inventory[].rq2_sha256` | Exact RQ2 batch CSV bytes named in `rq2_file` | The RQ2 validation JSON | Keep batch filename and hash together |
| `baseline_sha256` | Baseline dependency recorded by the original closure run | Executed GEE source text | Store an explicit dependency type/path/filename in any new schema |

The original top-level `rq2_validation_sha256` lacks the dependency filename, which is part of the ambiguity. Resolve the exact dependency object from the original run arguments or by matching byte hashes; do not infer its identity from a similar filename. Interpretation here follows `docs/validation/canonical_pas_origin_destination_full_closure_v3.md`; the original producer's complete run arguments are not present in this compact update.

For a future v4 closure schema, use a typed dependency record containing `role`, `object_type`, `filename`, `relative_path`, `sha256` and `hash_basis=exact_file_bytes`. Add a schema/migration note. Leave all v3 bytes unchanged. Hashes identify serialized bytes, not merely semantically equivalent JSON objects; key order, encoding and line endings can change a JSON hash.

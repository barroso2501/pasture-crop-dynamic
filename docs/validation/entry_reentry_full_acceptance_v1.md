# Entry/re-entry full native acceptance

**2026-10-23 — PASS.** The unchanged distributed `20d_validate_entry_reentry_full_v1.py --scope full` accepted the 73 supplied native CSVs. The archived implementation ZIP was authenticated by its original SHA256 before recovering two incomplete local scratch reference copies; all critical source pins then passed, without changing the validator or scientific logic.

| Check | Result |
|---|---:|
| Native files | 64 interval/batch CSVs + 8 audits + 1 manifest |
| Cells | 24,889, complete in each interval |
| Cell/interval rows | 199,112 |
| History audit | 24,889 rows, all 41 years 1985–2025 |
| Native actual-history error counters | 248,890 values, all zero |
| Accepted-origin pixel mismatch counters | 199,112 values, all zero |
| Historical per-cell field comparisons | 1,592,896 |
| Maximum historical per-cell difference | 3.79979610443e-07 ha |
| Historical aggregate controls | 64 |
| Maximum historical aggregate difference | 3.59117984772e-06 ha |
| Preserved-pilot controls | 126, all pass |
| Maximum pilot area difference | 3.63797880709e-12 ha |
| Maximum auxiliary cell partition residual | 1.09139364213e-11 ha |

Exact batch membership, unique keys, runtime parameters, all 41 annual bands and CRS/affine transforms, positive support, all origin/auxiliary stock and flow partitions, baseline construction, flow bounds, event partitions, frozen labels and auxiliary age-201 reset invariants passed. Tolerances are 0.01 ha per cell, 0.001 ha for aggregates and 1e-6 for pixel-equivalent count comparisons.

The original accepted pilot is preserved byte-for-byte and revalidated by its unchanged validator: 31 native fixtures / 302 steps. The full validation sets both `full_domain_decomposition_complete` and `native_full_domain_auxiliary_age201_complete` to true. This closes the specified coverage-derived auxiliary entry/re-entry assurance, including numerical age 201. It does not validate every numeric value of a public pasture-age asset or migrate analytical origin to that asset.

Historical reference provenance remains explicit: 49,778 reused rows and 149,334 fresh native sensitivity rows. No historical native counters were invented. The new counters are supplied in the actual full exports. Operator-supplied tables were validated; remote execution was not independently witnessed, and executed-script hash / operator attestation remain null. No fresh event-raster asset comparison was performed.

The machine PASS JSON and its output hashes are unchanged. `received_full_review_v1.json` records receipt, source hashes, scope, zero-counter counts and additional review. All received CSV bytes match the input ZIP and the machine report. Matrix v4.3/events-v5 and canonical accounting are unchanged.

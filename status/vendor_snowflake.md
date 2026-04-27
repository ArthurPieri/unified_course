# Vendor Snowflake Branch — Build Status

Last updated: 2026-04-10
Target certifications: **SOL-C01** → **COF-C02** → **DEA-C02**

## Modules
- [x] 00_exam_profile — drafted 2026-04-10 (all 3 exams side-by-side; code/duration/Q count/pass/fees; Pearson VUE)
- [x] 01_architecture — drafted 2026-04-10 (3-layer, micro-partitions, caches, object hierarchy)
- [x] 02_loading — drafted 2026-04-10 (stages, COPY INTO, file formats, Snowpipe vs Streaming vs Kafka, INFER_SCHEMA)
- [x] 03_access — drafted 2026-04-10 (system roles, hierarchy, primary/secondary, SCIM)
- [x] 04_protection — drafted 2026-04-10 (Time Travel, Fail-safe, zero-copy clone, replication, Tri-Secret Secure)
- [x] 05_performance — drafted 2026-04-10 (scale up/out, caches, QAS, clustering keys, SOS, Query Profile)
- [x] 06_dea_advanced — drafted 2026-04-10 (streams, tasks, Dynamic Tables, Snowpark, UDFs, Iceberg tables)

## Artifacts
- [x] vendors/snowflake/README.md (tri-cert hub, three learning paths)
- [x] vendors/snowflake/references.md
- [x] vendors/snowflake/mock_exam_sources.md (first-party links only; explicit no-fabricated-questions notice)

## Decisions recorded
- Primary source: Snowflake official documentation and certification study guides
- Tri-cert structure: Platform → Core → DEA Advanced (overlap Platform→Core ~85%, Core→DEA ~50-75%)
- SOL-C01: 65 Q / 85 min / 750/1000 / weights 35-15-40-10 verified from *Platform Guide p. 4*
- COF-C02 and DEA-C02 duration/Q count flagged "verify on cert page" where not in the PDF
- All exam facts cited with PDF page numbers
- No labs/ content created — labs are out of scope per task

## Blockers
none

## Next action
Stage 10: appendices + master references merge

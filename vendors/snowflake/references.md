# Vendor Snowflake — Branch References

## Official Snowflake study guides (PDFs in sibling repo)
- *SnowPro Associate: Platform (SOL-C01) Exam Study Guide*, last updated June 9 2025 — `../../../snowflake_eng/SnowProPlatformStudyGuide.pdf`
- *SnowPro Core (COF-C02) Exam Study Guide*, last updated August 22 2025 — `../../../snowflake_eng/SnowProCoreStudyGuide.pdf`
- *SnowPro Advanced: Data Engineer (DEA-C02) Exam Study Guide*, last updated March 6 2026 — `../../../snowflake_eng/SnowProDataEngineerStudyGuide.pdf`

## Snowflake certification pages
- [Snowflake Certifications hub](https://www.snowflake.com/en/learn/certifications/)
- [SnowPro Associate: Platform](https://www.snowflake.com/en/learn/certifications/snowpro-associate-platform/)
- [SnowPro Core](https://www.snowflake.com/en/learn/certifications/snowpro-core/)
- [SnowPro Advanced: Data Engineer](https://www.snowflake.com/en/learn/certifications/snowpro-advanced-data-engineer/)
- [Snowflake University](https://learn.snowflake.com/)

## Snowflake documentation (canonical per `docs/REUSE_POLICY.md`)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Key concepts & architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts)
- [Loading data overview](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [Access control](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Continuous Data Protection (CDP)](https://docs.snowflake.com/en/user-guide/data-cdp)
- [Virtual warehouses](https://docs.snowflake.com/en/user-guide/warehouses)
- [Streams and tasks](https://docs.snowflake.com/en/user-guide/streams-intro)
- [Dynamic tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [Snowpark for Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)

## Sibling repo — primary reuse source
- `../../../snowflake_eng/STUDY_PLAN.md` — tri-cert study plan
- `../../../snowflake_eng/phase1_platform/README.md`
- `../../../snowflake_eng/phase1_platform/study_notes/domain_1_0_architecture.md`
- `../../../snowflake_eng/phase1_platform/study_notes/domain_2_0_identity.md`
- `../../../snowflake_eng/phase1_platform/study_notes/domain_3_0_data_loading.md`
- `../../../snowflake_eng/phase1_platform/study_notes/domain_4_0_data_protection.md`
- `../../../snowflake_eng/phase1_platform/labs/lab_01_architecture_and_ui.sql`
- `../../../snowflake_eng/phase1_platform/labs/lab_02_data_loading.sql`
- `../../../snowflake_eng/phase1_platform/labs/lab_03_warehouses.sql`
- `../../../snowflake_eng/phase1_platform/labs/lab_04_identity_and_access.sql`
- `../../../snowflake_eng/phase1_platform/labs/lab_05_data_protection.sql`

## Sibling gap notice
`../../../snowflake_eng/` contains only `phase1_platform/`. No sibling content exists for Core (COF-C02) or DEA-C02 topics beyond what overlaps with Platform. Modules `05_performance` and `06_dea_advanced` therefore cite the three PDF study guides and docs.snowflake.com directly rather than sibling notes. See `../../references/sibling_sources.md:L158-L178`.

## Policy
All citations conform to `../../docs/REUSE_POLICY.md`. No blogs. No LLM summaries. Sibling citations use `path:Lstart-Lend`; PDF citations use `*Guide title, page N*`.

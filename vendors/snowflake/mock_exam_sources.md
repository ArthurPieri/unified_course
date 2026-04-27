# Snowflake Tri-Cert — Practice / Mock Exam Sources

**No fabricated questions.** This file contains only links to first-party Snowflake practice material and pointers to sibling quiz sources. Per `../../docs/REUSE_POLICY.md`, writing mock MCQs from scratch without a cited primary source is prohibited.

## Primary practice sources (Snowflake first-party)

| Source | Cert(s) | Format | Cost | Link |
|---|---|---|---|---|
| Snowflake University — SnowPro Platform Certification Preparation | SOL-C01 | On-demand course + quizzes | Free with Snowflake Community login | https://learn.snowflake.com/ (search "SnowPro Platform") |
| Snowflake University — SnowPro Core On-Demand Preparation Course | COF-C02 | On-demand course + quizzes | Free | https://learn.snowflake.com/ (search "SnowPro Core On-Demand") |
| Snowflake University — Data Engineer I / Data Engineer II ILT | DEA-C02 | Instructor-led | Paid | https://learn.snowflake.com/ |
| Official SnowPro Core Practice Exam | COF-C02 | Full-length simulation | ~$50 | Linked from the SnowPro Core cert page at https://www.snowflake.com/en/learn/certifications/snowpro-core/ |
| Official SnowPro Advanced: Data Engineer Practice Exam | DEA-C02 | Full-length simulation | ~$50 | Linked from https://www.snowflake.com/en/learn/certifications/snowpro-advanced-data-engineer/ |
| Exam Study Guide Sample Questions | all | 5 MCQ per cert | Free (in PDF) | Embedded in each PDF study guide below |

## PDF study guides (with sample questions)

Each of the three official PDFs ends with a **"Sample Questions"** section (5 questions + answers). These are authoritative and should be worked first.

- *SnowPro Associate: Platform (SOL-C01) Study Guide* — sample questions section, p. 9. Download from [Snowflake certification study guides](https://www.snowflake.com/certifications/).
- *SnowPro Core (COF-C02) Study Guide* — sample questions section, p. 13. Download from [Snowflake certification study guides](https://www.snowflake.com/certifications/).
- *SnowPro Advanced: Data Engineer (DEA-C02) Study Guide* — sample questions section, p. 12. Download from [Snowflake certification study guides](https://www.snowflake.com/certifications/).

## Sibling repo quick-check questions

The Phase 1 Platform study notes include "Quick Check" questions at the end of each objective. These are written by the sibling curriculum author and map 1:1 to SOL-C01 and partially to COF-C02 topics.

- Architecture Quick Checks — see [Snowflake Architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) and module `01_architecture/quiz.md`
- Identity Quick Checks — see [Snowflake Access Control](https://docs.snowflake.com/en/user-guide/security-access-control-overview) and module `03_access/quiz.md`
- Data Loading Quick Checks — see [Snowflake Data Loading](https://docs.snowflake.com/en/user-guide/data-load-overview) and module `02_loading/quiz.md`
- Data Protection Quick Checks — see [Snowflake Data Protection](https://docs.snowflake.com/en/user-guide/data-time-travel) and module `04_protection/quiz.md`

## Module quizzes in this branch

Each module in this branch ships an 8-12 question `quiz.md` with an answer key and primary-source citations:

- `01_architecture/quiz.md`
- `02_loading/quiz.md`
- `03_access/quiz.md`
- `04_protection/quiz.md`
- `05_performance/quiz.md`
- `06_dea_advanced/quiz.md`

Every question cites either (a) an official Snowflake PDF study guide section, (b) docs.snowflake.com, or (c) a specific line range in the sibling study notes. Do not add new questions without such a citation.

## Readiness gates

Recommended readiness gates per the [Snowflake certification guide](https://www.snowflake.com/certifications/):

| Phase | Gate |
|---|---|
| SOL-C01 | 80%+ on Snowflake University practice and module quizzes across all 4 domains |
| COF-C02 | 80%+ on official practice exam AND sibling quick-checks |
| DEA-C02 | 85%+ on official practice exam |

## What not to do

- Do not purchase "brain dump" sites. They violate the Snowflake Certification NDA and are frequently stale.
- Do not reuse questions lifted from third-party training vendors without verifying the underlying claim against docs.snowflake.com.
- Do not generate MCQs with an LLM and present them as practice — per `../../docs/REUSE_POLICY.md` factual-only rule.

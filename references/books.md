# Canonical Books

Books cited throughout the course, with chapter references for the modules that use them. No copyrighted prose is reproduced — modules cite the chapter and paraphrase.

## Data engineering fundamentals

- ***Fundamentals of Data Engineering***, Joe Reis & Matt Housley, O'Reilly 2022
  - Overall lifecycle framing used in phase intros and appendices
  - Ch. 2 Data engineering lifecycle — Phase 5 CI/CD
  - Ch. 4 Choosing technologies across the lifecycle, managed-services trade-off — Phase 5 Cloud Concepts
  - Ch. 4 Cost and the data engineering lifecycle; TCO vs TVO — Phase 5 FinOps
  - Ch. 5 Data generation — Phase 6 Capstone
  - Ch. 6 Ingestion → serving as a controlled release path — Phase 5 CI/CD
  - Ch. 6 Storage — Phase 6 Capstone
  - Ch. 8 Queries, modeling, transformation — Phase 6 Capstone
  - Ch. 8 Orchestration — DAG-of-tasks vs asset-oriented — Phase 5 Airflow Bridge
  - Ch. 9 Serving stage; reverse ETL as operational activation — Phase 5 Data Serving
  - Ch. 10 Security and access control foundations — Phase 5 IAM Primer
  - Lakehouse architecture chapter — Phase 2 lakehouse bridge

- ***Designing Data-Intensive Applications***, Martin Kleppmann, O'Reilly 2017
  - Ch. 3 Storage and retrieval — Phase 2 storage, Phase 3 stack, Phase 4 semi-structured, Phase 4 performance tuning, Appendix B engines
  - Ch. 4 Encoding and schema evolution — Phase 4 semi-structured, Appendix A architecture
  - Ch. 5 Replication — Phase 2 distributed systems, Phase 5 Kubernetes, Phase 6 Capstone
  - Ch. 6 Partitioning — Phase 2 distributed systems, Phase 6 Capstone, Appendix B engines
  - Ch. 7 Transactions — Phase 2 ETL patterns, Appendix B engines
  - Ch. 9 Consistency and consensus — Phase 2 CAP/consistency, Phase 6 Capstone, Appendix B engines
  - Ch. 10 Batch processing — Phase 3 PySpark, Phase 4 security/governance (retention), Appendix A architecture
  - Ch. 11 Stream processing — Phase 2 streaming concepts, Phase 4 Kafka, Phase 4 CDC, Phase 5 Data Serving, Appendix A architecture

## Data warehouse modeling

- ***The Data Warehouse Toolkit*** (3rd ed.), Ralph Kimball & Margy Ross, Wiley 2013
  - Ch. 1 Dimensional modeling primer, four-step design process — Phase 2 modeling, Appendix A architecture
  - Ch. 2 Dimensional modeling techniques (reference) — Phase 2 modeling, Appendix A architecture
  - Ch. 3 Retail sales case study, conformed dimensions, bus matrix — Phase 2 star schema lab, Appendix A architecture
  - Ch. 5 Slowly Changing Dimensions (Types 0/1/2/3/6) — Phase 2 SCD lab, Appendix A architecture
  - Ch. 1–3 dimensional modeling for Gold layer — Phase 6 Capstone
  - Ch. 1–5 star schema modeling for warehouse design — Vendors/Azure compute

- ***Building the Data Warehouse*** (4th ed.), W. H. Inmon, Wiley 2005
  - Ch. 1 Evolution of decision-support; subject-oriented, integrated, time-variant, non-volatile — Phase 2 modeling, Appendix A
  - Ch. 2 Corporate Information Factory — Phase 2 modeling, Appendix A
  - Ch. 3 3NF enterprise layer — Phase 2 modeling, Appendix A

- ***Building a Scalable Data Warehouse with Data Vault 2.0***, Dan Linstedt & Michael Olschimke, Morgan Kaufmann 2015
  - Ch. 1 Introduction to Data Vault 2.0 — Phase 2 modeling
  - Ch. 2 Scalable DW architecture; hub/link/satellite — Phase 2 modeling, Appendix A

## Version control

- ***Pro Git*** (2nd ed.), Scott Chacon & Ben Straub, Apress — free online at [git-scm.com/book](https://git-scm.com/book/en/v2)
  - Ch. 3 Git Branching — branch mechanics, workflows, rebasing — Phase 1 Git
  - Ch. 3 Rebasing section — merge vs rebase, golden rule of rebasing — Phase 1 Git
  - Ch. 7 Rewriting History — `--amend`, interactive rebase, filter-branch warnings — Phase 1 Git

## Operations and production

- ***Site Reliability Engineering***, Beyer, Jones, Petoff & Murphy (eds.), O'Reilly 2016 — free at [sre.google/sre-book/table-of-contents/](https://sre.google/sre-book/table-of-contents/)
  - Ch. 6 Monitoring Distributed Systems — golden signals, SLI/SLO framing — Phase 4 observability

## Foundational research papers

- Diego Ongaro & John Ousterhout, *In Search of an Understandable Consensus Algorithm* (Raft paper), USENIX ATC 2014 — Phase 2 distributed systems
- Leslie Lamport, *The Part-Time Parliament* (1998) and *Paxos Made Simple* (2001) — Phase 2 distributed systems
- Sergey Melnik et al., *Dremel: Interactive Analysis of Web-Scale Datasets*, VLDB 2010 — [research.google/pubs/pub36632/](https://research.google/pubs/pub36632/) — origin of Parquet's repetition/definition levels — Phase 4 semi-structured

## Exam study guides (vendor, PDF distributed with course)

- **AWS Certified Data Engineer – Associate (DEA-C01) Exam Guide** — exam domains, tasks, skills — Vendors/AWS exam profile
- **SnowPro Associate: Platform (SOL-C01) Study Guide** (2025-06-09) — Vendors/Snowflake modules 00–05
- **SnowPro Core (COF-C02) Study Guide** (2025-08-22) — Vendors/Snowflake modules 00–06
- **SnowPro Advanced: Data Engineer (DEA-C02) Study Guide** (2026-03-06) — Vendors/Snowflake modules 00, 02–06

## Citation format

Inline: `*Title, Author, Ch. N*` — e.g., `*Designing Data-Intensive Applications, Kleppmann, Ch. 5*`.

No page numbers (they differ between editions). No copyrighted excerpts.

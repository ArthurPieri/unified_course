> **Historical document.** This file preserves the original course brief used
> during initial planning. The authoritative plan is
> [`UNIFIED_COURSE_PLAN.md`](UNIFIED_COURSE_PLAN.md), which incorporates
> revisions from two rounds of adversarial analysis. Do not rely on CONTEXT.md
> for current scope, hour estimates, or outcome claims.

# Context: Unified Data Engineering Course Plan — Enhancement Project

This file consolidates all source material needed to execute the `IMPLEMENTATION_PLAN.md`. It contains:

1. **The current UNIFIED_COURSE_PLAN.md** — the document being enhanced
2. **The adversarial analysis** — the 8 findings driving all changes
3. **The 5 categorized source documents** — reference material that informed the original plan

---

# Part 1: Current UNIFIED_COURSE_PLAN.md

> This is the document to be modified. All line references in the implementation plan refer to this version.

---

# Unified Data Engineering Course Plan

---

## I. Course Goal

By the end of this course, the learner will design, build, deploy, monitor, and troubleshoot production-grade data pipelines spanning ingestion, transformation, storage, orchestration, governance, and serving — first using vendor-agnostic open-source tools, then implementing equivalent solutions on one or more cloud platforms (AWS, Azure, or Snowflake). The learner will be prepared to pass at least one industry-recognized data engineering certification and operate as a mid-level data engineer in a professional environment.

---

## II. Learner Profile

**Assumed starting level:**
- Intermediate SQL (JOINs, aggregations, subqueries, window functions, CTEs)
- Basic-intermediate Python (data structures, file I/O, generators, virtual environments)
- Basic Linux/CLI (navigation, file manipulation, piping)
- Basic Git (clone, commit, push, branch, merge, open a PR)
- Conceptual awareness of what a database is and what a data pipeline does

**Who this course is for:**
- Software developers transitioning to data engineering
- Data analysts seeking to move upstream into pipeline development
- Junior data engineers building systematic depth
- Career changers with programming fundamentals who want a structured path to DE employment
- Self-taught practitioners who have tool knowledge but lack architectural foundations

**Who this course is NOT for:**
- Complete beginners with no programming or SQL experience (complete prerequisites first)
- Experienced senior data engineers seeking only certification prep (skip to vendor branches)
- Data scientists focused exclusively on ML modeling without pipeline interest
- Anyone expecting a surface-level survey — this course demands hands-on mastery

---

## III. Curriculum Design Principles

1. **Foundations before tools.** Durable principles (data modeling, distributed systems, SQL, security) are taught before any specific product. These transfer across every vendor and every job.
2. **Concepts before implementation.** Each concept is introduced abstractly (what, why, when) before the learner touches a specific tool (how). This prevents cargo-culting.
3. **Open-source before proprietary.** The learner builds a complete lakehouse with open tools (PostgreSQL, MinIO, Iceberg, Trino, dbt, dlt, Dagster) before encountering any vendor platform. This ensures the learner understands what managed services abstract away.
4. **Shared core, then branching.** All vendor-specific content is deferred until after a unified conceptual and practical foundation. A learner who completes only the shared core is employable. Vendor branches add specialization and certification readiness.
5. **Spiral reinforcement.** Key concepts (partitioning, schema evolution, incremental loading, data quality) appear at increasing depth across multiple phases rather than being taught once and forgotten.
6. **Prerequisite-gated progression.** Each phase has explicit exit criteria. No phase is entered without demonstrated competence in prior phases.
7. **Practical-first assessment.** Competence is proven through labs, projects, and capstones — not by reading comprehension. Every phase produces a tangible deliverable.

---

## IV–V. Full Learning Roadmap

### Phase 0: Orientation and Mental Models

**Why now:** Before learning any tool or technique, the learner needs a map of the territory. Without this, they accumulate disconnected facts instead of building a coherent mental model.

**Prerequisites:** None beyond the stated learner profile.

**Learning objectives:**
- Define data engineering, its responsibilities, and where it sits relative to data science, analytics, and platform engineering
- Understand the data lifecycle: sources -> ingestion -> storage -> transformation -> serving -> consumption
- Map the Hadoop -> Spark -> Lakehouse evolution and why it matters for job interviews
- Distinguish batch, micro-batch, and streaming paradigms at a conceptual level
- Survey the certification landscape and choose an initial target

**Key topics:**
- What data engineers build and why businesses need them
- The data lifecycle and pipeline anatomy
- Historical evolution: Hadoop era (2006-2015) -> Spark era (2015-2020) -> Lakehouse era (2020+)
- Batch vs. streaming: when each matters, 90%+ of real work is batch
- Career landscape: job titles, salary ranges, common interview patterns
- Certification overview: LFCA, AWS DEA-C01, Azure DP-700, Snowflake SnowPro (Platform -> Core -> DE)
- How this course is structured and how to use it

**Practical exercises:**
- Self-assessment quiz (45 min): SQL window functions, Python generators, Git branching, networking basics (ports, HTTP)
- Map 5 real job postings to specific skills taught in this course
- Choose a target certification path and write a 1-paragraph learning goal

**Deliverables:** Completed self-assessment with gap identification. Written learning goal and target certification.

**Estimated duration:** 5-8 hours

**Exit criteria:** Self-assessment score >= 70%. Learners below threshold directed to prerequisite resources before Phase 1.

---

### Phase 1: Foundational General Knowledge

**Why now:** Everything that follows depends on fluency with Linux, networking, containers, scripting, and SQL. These are the load-bearing skills that every vendor platform, every tool, and every architecture assumes.

**Prerequisites:** Phase 0 completed. Self-assessment passed.

**Learning objectives:**
- Navigate Linux systems confidently (filesystem, processes, permissions, package management)
- Write bash scripts for automation (loops, conditionals, jq, piping)
- Understand networking fundamentals (IP, DNS, ports, HTTP/HTTPS, TCP vs. UDP)
- Structure Python projects professionally (pyproject.toml, uv/venv, project layout)
- Use Docker and Docker Compose to run multi-service local environments
- Write intermediate SQL (window functions, CTEs, self-joins, EXPLAIN ANALYZE)
- Use Git workflows (branching, PRs, merge conflict resolution, pre-commit hooks)

**Key topics:**

*Linux & CLI (16h):*
- Filesystem hierarchy, permissions (chmod, chown), process management (ps, top, kill)
- Package management, environment variables, shell configuration
- Bash scripting: variables, loops, conditionals, exit codes, jq for JSON, piping/redirection
- Health-check scripts, cron scheduling concepts, xargs for batch operations

*Networking (6h):*
- IP addresses, subnets, ports, DNS resolution
- HTTP/HTTPS, TCP vs. UDP, curl for API interaction
- How Docker containers communicate via hostnames and exposed ports
- VPN, firewall, and proxy concepts at a level sufficient for troubleshooting

*Python Engineering (12h):*
- Project structure: pyproject.toml, src layout, dependency management (uv recommended, pip/Poetry alternatives)
- Virtual environments, .python-version, lockfiles for reproducibility
- Code quality: ruff (lint + format), mypy (type checking), pre-commit hooks
- Testing with pytest: fixtures, parametrize, assertions, test organization

*Docker & Containers (12h):*
- Containers, images, volumes, networks — mental model
- Dockerfile basics, multi-stage builds
- Docker Compose: services, profiles, health checks, resource limits (mem_limit), .env for secrets
- Version pinning rationale (postgres:16-alpine vs. postgres:latest)
- Secret management: .env files, .gitignore patterns, never hardcode credentials

*SQL Depth (10h):*
- Window functions: ROW_NUMBER, RANK, LEAD/LAG, SUM OVER (PARTITION BY)
- CTEs, recursive CTEs, subqueries vs. joins performance
- EXPLAIN ANALYZE: reading query plans, identifying sequential scans, index usage
- PostgreSQL specifics: pg_dump/restore, VACUUM/ANALYZE, indexing (B-tree, GIN), pg_stat_activity

*Git Workflows (4h):*
- Branching strategies for data teams (feature, hotfix, main)
- PR review checklists, merge conflict resolution
- Pre-commit hooks for code quality enforcement

**Practical exercises:**
- Stand up PostgreSQL + pgAdmin via Docker Compose with .env-based credentials
- Write a bash health-check script for all services
- Load NYC Taxi sample data, write analytical queries with window functions
- Run EXPLAIN ANALYZE, create indexes, measure performance difference
- Structure a Python project with pyproject.toml, add dependencies with uv

**Deliverables:**
- Working Docker Compose environment with PostgreSQL + pgAdmin
- Health-check script that validates all services
- SQL analysis report on NYC Taxi data (5 analytical queries with EXPLAIN output)
- Python project skeleton with linting, testing, and pre-commit hooks configured

**Estimated duration:** 55-65 hours (5-6 weeks at 10-12h/week)

**Exit criteria:** 30-minute quiz (Docker, SQL, bash, Python) + mini-project: fix 3 intentional issues in a provided Docker Compose file (hardcoded credentials, missing health check, latest image tag). Pass threshold: 70%.

---

### Phase 2: Core Domain Concepts and Vocabulary

**Why now:** With foundational tools in hand, the learner needs the conceptual framework that makes data engineering a discipline, not just a collection of tools. Every topic in this phase is vendor-agnostic and will remain relevant regardless of which platform the learner ultimately works on.

**Prerequisites:** Phase 1 exit criteria met.

**Learning objectives:**
- Design data models for both transactional and analytical workloads
- Distinguish ETL, ELT, batch, micro-batch, and streaming patterns and choose correctly
- Understand distributed systems fundamentals (CAP theorem, partitioning, replication, consistency)
- Evaluate data quality using the six dimensions framework
- Describe data governance, classification, lineage, and compliance requirements
- Compare data architectures (Medallion, Data Mesh, Data Fabric, Data Hub, Serverless)
- Survey the database and processing engine landscape

**Key topics:**

*Data Modeling (14h):*
- Conceptual -> Logical -> Physical modeling progression
- Normalization (1NF-3NF) for OLTP vs. denormalization for OLAP
- Row-store vs. columnar storage: why analytics prefers columns
- Dimensional modeling (Kimball): star schema, snowflake schema, fact vs. dimension tables
- Slowly Changing Dimensions: Type 1 (overwrite), Type 2 (versioned rows), Type 3 (columns), Type 6 (hybrid)
- Hands-on: implement SCD Type 2 in PostgreSQL

*Pipeline Paradigms (10h):*
- ETL vs. ELT: when each applies, why modern stacks prefer ELT
- Batch (minutes-hours) vs. micro-batch (seconds-minutes) vs. streaming (milliseconds)
- Idempotency patterns: UPSERT/MERGE, delete-and-replace, checkpointing
- Incremental loading: cursor-based (watermark), append-only (immutable events), merge (mutable entities)
- Pipeline resilience: retry with exponential backoff, dead-letter queues, circuit breakers, poison-pill handling

*Distributed Systems Fundamentals (8h):*
- CAP theorem: Consistency, Availability, Partition tolerance — the tradeoff
- Partitioning/sharding: splitting data across nodes
- Replication: copying data for fault tolerance
- Consistency models: strong (PostgreSQL), eventual (Cassandra, S3), read-your-writes
- Horizontal scaling (add nodes) vs. vertical scaling (bigger machine)
- Why the lakehouse architecture is designed for horizontal scaling at every layer

*Data Quality & Governance (8h):*
- Six data quality dimensions: accuracy, completeness, consistency, timeliness, validity, uniqueness
- Data contracts: schema enforcement at pipeline boundaries
- Data classification: PII, Sensitive, Internal, Public
- Data governance: roles, lineage, governance-as-code, retention policies
- Compliance awareness: GDPR right-to-erasure, data residency, audit trails

*File Formats & Storage Patterns (6h):*
- CSV, JSON, Avro, Parquet, ORC: trade-offs (schema support, compression, columnar access, splittability)
- Hive-style partitioning: year=2024/month=01/file.parquet
- Target file sizes (256MB-1GB compressed), small files anti-pattern
- Open table formats overview: Iceberg, Delta Lake, Hudi — ACID on object storage

*Architecture Landscape (8h):*
- Data lakehouse: open table formats + decoupled compute + object storage
- Medallion architecture: Bronze (raw) -> Silver (cleansed) -> Gold (business-ready)
- Data Mesh: domain-oriented decentralized ownership (for large orgs)
- Data Fabric: metadata-driven integration
- Hadoop ecosystem legacy and why it matters for interviews
- Modern architecture decision framework: when to use what

*Database & Engine Landscape (6h):*
- Relational: PostgreSQL, MySQL, Oracle, SQL Server, Aurora — dialect differences, DE interaction
- NoSQL families: Document (MongoDB), Column-family (Cassandra), Graph (Neo4j), Key-Value (Redis)
- Polyglot persistence: modern apps use multiple databases, DEs ingest from all
- Processing engines: Trino (interactive SQL), Spark (large-scale ETL/ML), Flink (real-time streaming)
- Managed warehouses: Snowflake, BigQuery, Redshift — zero-ops alternatives to open stack

*Streaming Concepts (6h):*
- Event streaming fundamentals: events vs. messages, delivery semantics (at-least-once, at-most-once, exactly-once)
- Apache Kafka architecture (conceptual): topics, partitions, consumer groups, offsets
- Windowing: tumbling, hopping, sliding, session windows
- Watermarks, checkpoints, output modes (append, complete, update)
- When streaming vs. batch: decision framework with real-world examples

**Practical exercises:**
- Design a star schema for an e-commerce dataset; implement in PostgreSQL
- Implement SCD Type 2 with effective dates
- Classify columns in a sample dataset by PII/Sensitive/Internal/Public
- Write a data contract (YAML) for a staging model
- Compare query performance on row-store vs. columnar formats (PostgreSQL vs. Parquet via DuckDB)

**Deliverables:**
- Star schema ERD + PostgreSQL implementation with SCD Type 2
- Written data quality assessment of a provided messy dataset
- Architecture decision document: choose and justify an architecture for a given scenario

**Estimated duration:** 55-70 hours (5-6 weeks at 10-12h/week)

**Exit criteria:** 15-question quiz (data modeling, pipeline paradigms, distributed systems, data quality, architectures). Pass threshold: 70%. Plus: star schema implementation reviewed and accepted.

---

### Phase 3: Core Tools, Workflows, and Applied Practice

**Why now:** Concepts without hands-on practice create false confidence. This phase builds the full open-source lakehouse stack piece by piece, giving the learner concrete experience with every layer of a modern data platform before encountering vendor abstractions.

**Prerequisites:** Phase 2 exit criteria met.

**Learning objectives:**
- Deploy and operate a local lakehouse: MinIO (object storage) + Iceberg (table format) + Hive Metastore (catalog) + Trino (query engine) + dlt (ingestion) + dbt (transformation) + Dagster (orchestration)
- Build complete ELT pipelines from ingestion through serving
- Write and test dbt models with contracts, tests, and documentation
- Orchestrate multi-step pipelines with Dagster
- Use DuckDB for local exploration and CI testing

**Key topics:**

*Object Storage — MinIO (8h):*
- S3-compatible object storage: buckets, objects, mc CLI, web console
- Credential management via .env
- Docker Compose profile: `storage`
- Connection patterns: path-style access, endpoint configuration
- Lab: create lakehouse bucket, upload sample Parquet, verify access

*Table Format — Apache Iceberg (10h):*
- Three-layer architecture: data (Parquet files), metadata (manifests), catalog (pointer to current metadata)
- Snapshot isolation, schema evolution, hidden partitioning, time travel
- File sizing best practices: 256-512MB per Parquet file, partition tables > 1TB
- Comparison: Iceberg vs. Delta Lake vs. Hudi
- Lab: create Iceberg tables with PyIceberg, demonstrate schema evolution and time travel

*Metadata Catalog — Hive Metastore + Landscape (8h):*
- HMS: standalone Thrift service, PostgreSQL backend, metadata_location pointer for Iceberg
- Catalog landscape: HMS (mature), Apache Polaris (REST, modern), Nessie (Git-like versioning)
- Data sharing via open formats: Iceberg as lingua franca for multi-engine access
- Docker Compose profile: `metadata`
- Lab: deploy HMS, create database/table, inspect backend tables (TBLS, DBS, SDS)

*Query Engine — Trino (14h):*
- Distributed SQL engine: coordinator + workers, 50+ connectors, federated queries
- Connecting Trino to Iceberg on MinIO via HMS (catalog configuration)
- JVM configuration and memory management
- Query performance tuning: EXPLAIN vs. EXPLAIN ANALYZE, predicate pushdown, partition pruning, dynamic filtering
- Performance benchmarking methodology: establish baselines, change one variable, document before/after
- DuckDB as lightweight complement for local exploration and CI testing
- Docker Compose profile: `query`
- Lab: deploy Trino, create schemas (bronze/silver/gold), run analytical queries, EXPLAIN ANALYZE

*Data Ingestion — dlt (12h):*
- Pure Python E+L: @dlt.source, @dlt.resource, dlt.pipeline()
- Schema inference, JSON normalization, incremental loading
- Schema contracts: evolve, disallow_additions, disallow_all
- Schema evolution workflows: compatibility checking, dead-letter routing for violations
- Using pandas within dlt transforms for row-level enrichment
- Lab: ingest NYC Taxi data into MinIO/Iceberg Bronze layer, implement incremental loading

*Data Transformation — dbt (14h):*
- The T in ELT: models as SELECT statements, ref() for dependency DAG
- Materializations: view, table, incremental, snapshot
- Medallion mapping: staging/ (stg_) -> Silver, intermediate/ (int_) -> Silver, marts/ (fct_, dim_) -> Gold
- Data contracts (dbt 1.8+): enforced schema with column types and constraints
- Unit tests (dbt 1.8+): given/expect pattern for logic validation
- Testing: unique + not_null on PKs, dbt-expectations for advanced tests, dbt docs generate
- Git workflows: branching for dbt, PR review checklist, pre-commit hooks (dbt-checkpoint)
- Lab: build staging/intermediate/mart models for NYC Taxi data, add contracts and tests

*Orchestration — Dagster (12h):*
- Software-Defined Assets: declare what data should exist
- Architecture: webserver + daemon + code locations + PostgreSQL
- Schedules, sensors, partitions, asset checks, freshness policies
- dagster-dbt integration: @dbt_assets mapping each model to an asset
- dagster-dlt integration: @dlt_assets for ingestion assets
- Testing: materialize_to_memory with DagsterInstance.ephemeral()
- Orchestrator landscape comparison: Dagster vs. Airflow vs. Prefect
- Lab: orchestrate full pipeline (dlt ingest -> dbt transform -> quality checks)

*BI & Visualization — Metabase (4h):*
- Connecting Metabase to Trino (native support)
- Dashboard design: KPIs, charts, filters
- Lab: build a dashboard on Gold-layer data

**Practical exercises (cumulative):**
- Each sub-topic builds on the previous; by end, full stack is running
- Progressive Docker Compose activation: storage -> metadata -> query -> orchestration -> visualization

**Deliverables:**
- Running local lakehouse stack with all services healthy
- Complete ELT pipeline: NYC Taxi data -> dlt (Bronze) -> dbt (Silver/Gold) -> Trino queries -> Metabase dashboard
- Dagster orchestration with schedule and quality checks
- dbt documentation site generated
- All code in a Git repo with branching, pre-commit hooks, and CI tests (DuckDB-based)

**Estimated duration:** 80-100 hours (7-9 weeks at 10-12h/week)

**Exit criteria:** 2-hour integration exercise: from a fresh Docker Compose stack, complete end-to-end flow (start services -> create Iceberg table -> dbt transform -> Trino query -> verify results). All dbt tests pass. Can explain the data flow at every step.

---

### Phase 4: Intermediate Domain Specializations

**Why now:** With a working lakehouse and practical pipeline experience, the learner is ready to go deeper into the dimensions that separate junior from mid-level: streaming, CDC, security, governance, and performance.

**Prerequisites:** Phase 3 exit criteria met.

**Learning objectives:**
- Implement change data capture pipelines
- Handle semi-structured data (JSON shredding, FLATTEN, schema drift)
- Apply security and governance patterns to pipelines (masking, RLS, audit trails)
- Diagnose and resolve performance issues (data skew, spill, small files)
- Implement data quality monitoring and observability

**Key topics:**

*Change Data Capture (10h):*
- CDC concepts: WAL-based replication, binlog capture, change tables
- Debezium: PostgreSQL WAL -> Debezium -> Kafka -> dlt -> Iceberg MERGE INTO
- Incremental load refinement: watermark pattern, append-only, merge with primary key
- Lab: real CDC pipeline from PostgreSQL through to Iceberg Silver layer

*Semi-Structured Data Handling (8h):*
- JSON shredding in SQL: explode() in Spark, FLATTEN in Snowflake-SQL, OPENJSON in T-SQL
- Schema drift handling: rescue columns, merge schema, schema evolution workflows
- Encoding/serialization: UTF-8/UTF-16, Avro/Parquet/JSON format considerations
- Spark read modes: PERMISSIVE, DROPMALFORMED, FAILFAST
- Lab: ingest nested JSON API data, flatten to relational tables, handle schema evolution

*Security & Governance in Practice (12h):*
- Data classification implementation: PII tags in dbt meta, enforcement via masking views
- Column masking in Trino: regexp_replace for email masking, role-based masked views
- Row-level security: policy-based transparent filtering
- Access audit trails: querying system.runtime.queries
- Secret management: .env patterns, never-committed credentials, rotation concepts
- PII masking pipeline: detection -> masking -> access control -> right-to-erasure -> audit
- Multi-tenant data isolation: row-level filtering, schema-per-tenant, catalog-per-tenant
- Encryption concepts: at-rest (AES-256), in-transit (TLS), envelope encryption, CMK
- Lab: implement end-to-end PII masking pipeline with audit dashboard

*Performance Tuning & Troubleshooting (12h):*
- Data skew: symptom (one task 10-100x slower), solutions (AQE, salting, broadcast join)
- Small file compaction: OPTIMIZE, ZORDER (max 3-4 columns), auto-optimize
- Data spill: memory vs. disk, executor OOM vs. driver OOM diagnosis
- Spark troubleshooting: check order (error -> executors -> stages -> driver logs)
- Query optimization: predicate pushdown, partition pruning, dynamic filtering, caching
- Benchmarking: baseline (3 runs, discard cold), one variable at a time, document results
- Lab: diagnose and fix a slow query (provided broken pipeline with skew, small files, missing partitioning)

*Observability & Monitoring (8h):*
- Pipeline monitoring: Dagster freshness policies, data quality metric functions
- Infrastructure monitoring: Prometheus + Grafana basics
- Data catalog/discovery: OpenLineage standard, DataHub/OpenMetadata landscape
- Alerting: Alertmanager configuration, severity framework, runbook templates
- Lab: set up monitoring for the lakehouse pipeline with alerting on failures

**Deliverables:**
- CDC pipeline from PostgreSQL to Iceberg with MERGE INTO
- PII masking pipeline with role-based access and audit trail
- Performance optimization report: before/after benchmarks on provided slow queries
- Monitoring dashboard with alerting for pipeline health

**Estimated duration:** 45-55 hours (4-5 weeks at 10-12h/week)

**Exit criteria:** Can diagnose a failing pipeline (provided broken scenario), identify root cause (skew, schema drift, permission error), and fix it. Written performance report with before/after metrics.

---

### Phase 5: Advanced Architecture, Operations, and Strategy

**Why now:** The learner has individual pipeline competence. This phase elevates to system-level thinking: designing architectures, managing costs, deploying to production, and making strategic technology choices.

**Prerequisites:** Phase 4 exit criteria met.

**Learning objectives:**
- Design end-to-end data architectures for different organizational contexts
- Implement CI/CD for data projects
- Estimate and optimize data platform costs (FinOps)
- Deploy data infrastructure on Kubernetes
- Serve data to applications via APIs
- Prepare data for ML/AI consumption

**Key topics:**

*CI/CD for Data (8h):*
- GitHub Actions pipeline: lint -> test (DuckDB) -> deploy dbt -> verify
- CI/CD landscape: GitHub Actions, GitLab CI, CircleCI, ArgoCD
- dbt deployment: production runs, environment management, artifact promotion
- Lab: set up GitHub Actions for the lakehouse project

*Kubernetes Fundamentals (8h):*
- Container orchestration: pods, services, deployments, Helm charts
- kind/Minikube: local Kubernetes for learning
- Deploying Trino on Kubernetes via Helm
- When to use K8s vs. Docker Compose vs. managed services
- Lab: deploy Trino to a local Kubernetes cluster

*Cloud Computing Fundamentals (6h):*
- Cloud models: IaaS, PaaS, SaaS — where each tool in the stack fits
- Multi-cloud service mapping: AWS, Azure, GCP equivalents for each open-source component
- Storage tier lifecycle: hot -> cool -> archive -> delete
- Serverless vs. provisioned compute: decision framework
- Managed vs. self-hosted: trade-off analysis (Snowflake/Databricks vs. open stack)

*FinOps & Cost Optimization (6h):*
- TCO comparison: self-hosted lakehouse vs. managed platforms
- Cloud cost optimization patterns: right-sizing, spot instances, auto-scaling, auto-termination
- Query cost monitoring: tracking compute consumption per query
- Lab: estimate monthly cost for the lakehouse at 3 different data volumes

*Data Serving & ML Patterns (6h):*
- API-first data serving: FastAPI + Trino for Gold-layer data to applications
- API vs. SQL access: decision guide
- Feature stores: Gold-layer feeding ML training
- Vector databases as lakehouse extension (conceptual)
- Lab: build a FastAPI endpoint serving Gold-layer analytics

*Architecture Design (6h):*
- Architecture decision records (ADRs): documenting why, not just what
- Trade-off analysis: latency vs. cost vs. complexity vs. operational burden
- When to choose: Medallion vs. Data Mesh vs. Data Fabric
- Scaling the lakehouse: adding workers, adding storage, adding catalogs
- Lab: write an ADR for a technology decision in the capstone project

**Deliverables:**
- CI/CD pipeline for the lakehouse project (GitHub Actions)
- Trino deployed on local Kubernetes
- Cost estimation spreadsheet for 3 scale scenarios
- FastAPI data-serving endpoint
- Architecture decision record

**Estimated duration:** 35-45 hours (3-4 weeks at 10-12h/week)

**Exit criteria:** CI/CD pipeline runs green. Kubernetes deployment healthy. Can present a cost estimate and architectural rationale for the full stack.

---

### Phase 6: Vendor-Agnostic Capstone

**Why now:** Before branching into vendor specializations, the learner consolidates all skills into a single production-grade project that demonstrates employability.

**Prerequisites:** Phase 5 exit criteria met.

**Learning objectives:**
- Design, build, deploy, and document a complete data platform from scratch
- Demonstrate end-to-end data engineering competence in a portfolio-worthy project

**Project specification:**

Build an end-to-end data lakehouse processing a realistic dataset:

1. **Source**: Simulated streaming data (Python producer) + batch API source + relational database (PostgreSQL)
2. **Ingestion**: dlt pipelines — batch (API -> Bronze), CDC (PostgreSQL -> Bronze via Debezium), append (streaming -> Bronze)
3. **Storage**: MinIO (S3-compatible) with Iceberg tables across Bronze/Silver/Gold zones
4. **Catalog**: Hive Metastore with proper schema registration
5. **Transformation**: dbt models (staging -> intermediate -> marts) with contracts, tests, unit tests, documentation
6. **Query**: Trino for analytical queries on Gold layer
7. **Orchestration**: Dagster managing the full pipeline DAG with schedules, sensors, and quality checks
8. **Security**: PII masking, role-based access, secret management, audit trail
9. **Monitoring**: Pipeline health dashboard, alerting on failures, data quality metrics
10. **Serving**: Metabase dashboard + FastAPI endpoint for programmatic access
11. **CI/CD**: GitHub Actions running lint, test, deploy
12. **Documentation**: dbt docs, architecture diagram, ADR for key decisions, README

**Assessment criteria:**
- Pipeline runs end-to-end without manual intervention
- All dbt tests pass
- Monitoring detects injected failure within 5 minutes
- PII masking prevents unauthorized data access
- Documentation sufficient for another engineer to onboard
- Code quality: pre-commit hooks, type hints, test coverage

**Estimated duration:** 30-40 hours (3-4 weeks)

**Exit criteria:** Completed project reviewed against rubric. Deployed, documented, and pushed to a public Git repository as a portfolio piece.

---

## VI. Vendor-Specific Branches

> **When to start:** Only after Phase 6 capstone is complete (or Phase 4 for experienced learners who can demonstrate equivalent competence).

---

### Branch A: AWS Data Engineering

**Assumes common core:** Phases 0-6 (data modeling, ETL/ELT patterns, Spark fundamentals, streaming concepts, Medallion architecture, security principles, orchestration, monitoring).

**Vendor-specific topics:**

*Ingestion Services (20h):*
- Amazon S3: landing zone, multipart upload, Transfer Acceleration, lifecycle policies, storage classes
- AWS DMS: CDC, full load, ongoing replication
- DataSync, Snow Family: bulk/offline transfer
- AppFlow: SaaS-to-S3 managed ingestion
- Kinesis Data Streams: shards, partition keys, consumers (KCL, enhanced fan-out)
- Kinesis Data Firehose: delivery streams, format conversion (JSON -> Parquet), Lambda transforms
- Amazon MSK: managed Kafka, MSK Connect, MSK Serverless
- Decision matrix: KDS vs. KDF vs. MSK

*Transformation Services (18h):*
- AWS Glue: ETL jobs (Spark/Python), crawlers, DynamicFrames, bookmarks
- Glue DataBrew: visual data preparation
- Glue Data Catalog: databases, tables, schema registry
- Amazon EMR: managed Spark/Hive clusters, EMR Serverless, EMR on EKS
- Managed Apache Flink: real-time stream processing
- Decision matrix: Glue vs. EMR vs. Flink

*Orchestration Services (10h):*
- AWS Step Functions: state machines, error handling, parallel/map states
- Amazon MWAA: managed Airflow — DAGs, operators, sensors
- Amazon EventBridge: event-driven rules and schedules
- Decision matrix: Step Functions vs. MWAA

*Data Store Selection (14h):*
- DynamoDB: partition/sort keys, GSI/LSI, capacity modes, Streams
- Redshift: Spectrum, materialized views, RA3 nodes, Serverless, data sharing
- Athena: serverless SQL on S3, Iceberg tables, federated query, cost control
- RDS/Aurora, OpenSearch, DocumentDB, Neptune, Keyspaces, MemoryDB — when to choose each
- Lake Formation: governed tables, TBAC, column/row/cell-level security

*Operations & Monitoring (10h):*
- Lambda: event-driven processing, triggers, concurrency
- CloudWatch: metrics, alarms, Logs, Log Insights
- CloudTrail: API/data event logging
- Glue Data Quality: rule-based quality checks

*Security & Governance (10h):*
- IAM: identity vs. resource policies, SCPs, cross-account, federation, least privilege
- KMS: envelope encryption, SSE-S3/SSE-KMS/SSE-C, key policies
- VPC endpoints, PrivateLink
- Macie: PII discovery in S3
- Secrets Manager: credential rotation

**Implementation labs:**
- Build end-to-end pipeline: S3 -> Glue ETL -> Athena queries -> QuickSight dashboard
- Streaming pipeline: Kinesis -> Firehose -> S3 (Parquet) -> Glue Catalog -> Athena
- Step Functions orchestration with error handling and SNS notifications
- IAM least-privilege policies for a Glue job accessing S3 and DynamoDB
- Lake Formation permissions: database/table/column-level access control

**Real-world project:** Capstone equivalent on AWS — recreate the Phase 6 architecture using AWS services (S3, Glue, Athena, Step Functions, CloudWatch, IAM/KMS).

**Recommended certification sequence:**
1. AWS Certified Data Engineer Associate (DEA-C01) — primary target

**When to choose this branch:**
- Your target employer uses AWS
- You want the broadest cloud market share (AWS leads in enterprise adoption)
- You prefer a wide service catalog with fine-grained control

**Trade-offs vs. other branches:**
- More services to learn than Snowflake (higher complexity, more flexibility)
- Less unified than Azure Fabric (more architectural decisions, more operational control)
- Open-source friendly (Glue = Spark, MSK = Kafka, MWAA = Airflow)

**Estimated duration:** 80-100 hours (7-9 weeks at 10-12h/week)

---

### Branch B: Azure / Microsoft Fabric Data Engineering

**Assumes common core:** Phases 0-6.

**Vendor-specific topics:**

*Storage Layer (8h):*
- ADLS Gen2: hierarchical namespace, abfss:// protocol, HNS upgrade (irreversible)
- Storage account hierarchy: account -> container -> directory -> file
- Delta Lake on Azure: transaction log, MERGE, OPTIMIZE, ZORDER, VACUUM, time travel

*Synapse Analytics (18h):*
- Pool types: dedicated SQL (DWUs), serverless SQL (per-TB), Spark pools (per-node-hour)
- Distributions: hash, round-robin, replicated — choosing based on table size and join patterns
- T-SQL in Synapse: OPENROWSET, CETAS, external tables, filepath() partition pruning
- PolyBase / COPY INTO for dedicated pool loading
- CCI row group health, ordered CCI, heaps for staging
- DMVs: exec_requests, request_steps (ShuffleMove, BroadcastMove), partition_stats
- Synapse Link: Cosmos DB HTAP

*ADF / Synapse Pipelines (14h):*
- Copy Activity: 90+ connectors, NOT transformation
- Mapping Data Flows: visual Spark transforms (Derived Column, Aggregate, Join, Pivot, Flatten)
- Expression language: @pipeline().parameters, @activity().output
- Integration Runtime types: Azure IR, Self-hosted IR, Azure-SSIS IR
- Trigger types: Schedule, Tumbling Window, Event-based, Custom Event
- Incremental loads: watermark pattern, tumbling window backfill

*Stream Processing (10h):*
- Event Hubs: partitioned log, TUs, Consumer Groups, Capture to ADLS (Avro)
- Stream Analytics: SQL temporal query language, windowing, TIMESTAMP BY, embarrassingly parallel
- Spark Structured Streaming on Azure: readStream/writeStream, cloudFiles (Auto Loader)
- Checkpoints, watermarks, foreachBatch for upserts

*Databricks on Azure (8h):*
- Unity Catalog: catalog.schema.table namespace, GRANT/REVOKE
- Job clusters vs. all-purpose clusters, autoscaling, spot instances
- Auto Loader: cloudFiles format, schema evolution
- Delta Change Data Feed

*Monitoring & Optimization (10h):*
- Azure Monitor, Log Analytics (KQL), diagnostic settings
- Metric alerts vs. log alerts, dynamic thresholds
- Query performance: DMVs, data skew detection, statistics management
- Small file compaction, OPTIMIZE, auto-optimize
- Copy Activity tuning: DIUs, parallel copies, throughput metrics

*Security (10h):*
- RBAC vs. POSIX ACLs on ADLS Gen2 (RBAC checked first)
- Encryption: TDE, CMK via Key Vault, TLS 1.2
- RLS, CLS, Dynamic Data Masking
- Private endpoints vs. service endpoints, Managed VNet, data exfiltration protection
- Managed Identity: preferred over keys/SAS everywhere
- Microsoft Purview: lineage, catalog, PII scanning, business glossary

*Microsoft Fabric (DP-700 path) (14h):*
- OneLake replacing ADLS Gen2
- Fabric Data Warehouse vs. Synapse dedicated pools
- Dataflows Gen2 / Power Query M language
- KQL and Eventhouse (Real-Time Intelligence)
- Shortcuts and mirroring (data virtualization)
- Fabric deployment pipelines, capacities, licensing

**Implementation labs:**
- ADF pipeline: Copy Activity + Data Flow + parameterization
- Spark transforms in Synapse/Databricks with Delta Lake MERGE
- Event Hubs + Stream Analytics with windowed aggregation
- Synapse dedicated pool: distributions, loading, DMV analysis
- End-to-end Medallion on Azure: ADLS -> ADF -> Databricks/Spark -> Synapse -> Power BI
- RBAC + ACL configuration on ADLS Gen2
- Purview catalog scan and lineage visualization

**Real-world project:** Rebuild the Phase 6 capstone on Azure (ADLS, ADF, Databricks/Synapse Spark, Synapse SQL, Azure Monitor, Key Vault).

**Recommended certification sequence:**
1. DP-700: Fabric Data Engineer Associate — primary target (current exam)
2. (Optional) DP-203 knowledge as deep Azure foundation — exam retired, use for learning only

**When to choose this branch:**
- Your target employer uses Azure / Microsoft ecosystem
- You want to learn Microsoft Fabric (newer, rapidly growing)
- You work in enterprises with existing Microsoft licensing

**Trade-offs vs. other branches:**
- Platform in transition (Synapse -> Fabric); more concepts to track
- Stronger enterprise integration (Power BI, Purview, Entra ID)
- DP-700 is a newer exam with less community material available

**Estimated duration:** 90-110 hours (8-10 weeks at 10-12h/week)

---

### Branch C: Snowflake Data Engineering

**Assumes common core:** Phases 0-6.

**Vendor-specific topics:**

*Architecture & Platform (16h):*
- Three-layer architecture: storage, compute (virtual warehouses), cloud services
- Editions: Standard, Enterprise, Business Critical, VPS — feature gates
- Snowsight UI, Snowflake Notebooks (SQL/Python cells, Streamlit visualization)
- SnowSQL CLI, connectors, drivers
- Micro-partitions and data clustering (automatic), cluster keys, SYSTEM$CLUSTERING_INFORMATION
- Object hierarchy: databases, schemas, tables, views, stages, pipes, streams, tasks

*Data Loading & Movement (14h):*
- Stages: internal vs. external, storage integrations (S3/GCS/Azure)
- COPY INTO: loading with file format options, unloading with compression
- Snowpipe: auto-ingest (event-driven) vs. REST API
- Snowpipe Streaming vs. Kafka connector
- INFER_SCHEMA: auto-detect file structure
- File formats: CSV, JSON, Parquet, Avro, ORC — Snowflake-specific handling

*Virtual Warehouses & Performance (14h):*
- Sizing (XS-6XL), multi-cluster warehouses (scale out), auto-suspend/auto-resume
- Credit consumption model and cost optimization
- Caching types: metadata cache, result cache (24h), warehouse cache (SSD) — invalidation rules
- Query Profile: explain plans, data spilling, pruning, query history
- Materialized views, search optimization, query acceleration service
- Resource monitors, budgets, ACCOUNT_USAGE schema, cost center tagging
- Snowpark-optimized warehouses

*Data Transformation (14h):*
- Semi-structured data: VARIANT column, FLATTEN, LATERAL FLATTEN, ARRAY/OBJECT functions
- UDFs: SQL, Python, Java, Scala — including secure UDFs and UDTFs
- Stored procedures: SQL Scripting, JavaScript, Snowpark — transaction management
- Streams + Tasks: CDC pipeline building, DAG creation
- Dynamic Tables: declarative pipeline (source -> staging -> curated)
- Snowpark: Python/Java/Scala DataFrame API on Snowflake compute
- dbt with Snowflake: project setup, deployment, testing

*Data Protection & Sharing (10h):*
- Time Travel: AT/BEFORE queries, DATA_RETENTION_TIME_IN_DAYS (0-90)
- Fail-safe: 7-day non-queryable recovery period
- Cloning: zero-copy, permission inheritance, dev environment creation
- Replication: cross-region, cross-cloud failover/failback
- Secure Data Sharing: direct shares, listings, DDL (CREATE SHARE, GRANT)
- Snowflake Marketplace, Data Exchange
- Iceberg tables and Horizon Catalog for federated access

*Security & Governance (10h):*
- Role hierarchy: ACCOUNTADMIN > SECURITYADMIN > SYSADMIN > custom roles
- Network policies (IP whitelisting), MFA, SSO, key pair auth
- Row access policies, Dynamic Data Masking, aggregation/projection policies
- Object tagging, data classification (PII detection), access history tracking
- Data Clean Rooms: privacy-preserving collaboration

*DevOps & AI (8h):*
- Git integration in Snowflake
- Code deployment pipelines, testing/validation frameworks
- Environment management with cloning and role isolation
- Cortex LLM functions: PARSE_DOCUMENT, TRANSLATE, CLASSIFY_TEXT, COMPLETE
- Cortex AI cost management

**Implementation labs:**
- Set up Snowflake trial (Enterprise edition), navigate Snowsight
- COPY INTO: CSV and JSON loading from internal/external stages
- Build stream + task CDC pipeline
- Dynamic Table pipeline: source -> staging -> curated
- FLATTEN nested JSON, create analytical views
- Snowpark Python UDF with dependencies
- Query Profile deep-dive: diagnose and fix a slow query
- Zero-copy clone for dev environment, Time Travel recovery
- Data share with row-level filtering
- dbt project targeting Snowflake

**Real-world project:** Rebuild Phase 6 capstone on Snowflake (stages, COPY INTO/Snowpipe, streams+tasks/Dynamic Tables, Snowpark, UDFs, role-based security, Snowsight dashboards).

**Recommended certification sequence:**
1. SnowPro Associate Platform (SOL-C01) — entry point ($175)
2. SnowPro Core (COF-C02) — foundational certification ($175)
3. SnowPro Advanced Data Engineer (DEA-C02) — requires active Core ($375)

**When to choose this branch:**
- Your target employer uses Snowflake
- You want the most integrated, lowest-operational-overhead platform
- You prefer SQL-first data engineering over heavy Python/Spark
- You want a clear three-tier certification path

**Trade-offs vs. other branches:**
- Vendor lock-in: Snowflake is proprietary (mitigated by Iceberg table support)
- Less control over infrastructure (no self-hosted option)
- Strongest SQL developer experience of the three platforms
- Three certifications required for full DE credential (vs. one for AWS/Azure)
- Highest exam cost total ($725 minimum for all three)

**Estimated duration:** 80-100 hours for Platform + Core, additional 60-80 hours for DE Advanced (total 140-180 hours over 14-20 weeks)

---

## VII. Certification Roadmap

| # | Certification | Provider | Level | Timing | Knowledge Prerequisites | Practical Prerequisites | Classification |
|---|---|---|---|---|---|---|---|
| 1 | LFCA (Linux Foundation Certified IT Associate) | Linux Foundation | Entry | After Phase 1 | Linux, networking, cloud concepts, security basics, DevOps, containers | CLI proficiency, basic troubleshooting | Optional — validates IT foundations |
| 2 | SnowPro Associate Platform (SOL-C01) | Snowflake | Entry | After Snowflake Branch Week 4 | Snowflake architecture, Snowsight, loading, warehouses, RBAC, data protection | Snowflake trial experience | Recommended if pursuing Snowflake path |
| 3 | AWS DEA-C01 (Data Engineer Associate) | AWS | Associate | After AWS Branch completion | All 4 AWS domains: ingestion, storage, operations, security | LocalStack + AWS Free Tier hands-on | Recommended if pursuing AWS path |
| 4 | DP-700 (Fabric Data Engineer Associate) | Microsoft | Associate | After Azure Branch completion | Fabric architecture, pipelines, Spark, SQL, security | Fabric Trial + Azure Free Tier labs | Recommended if pursuing Azure path |
| 5 | SnowPro Core (COF-C02) | Snowflake | Core | After Platform + 6 weeks | Deeper architecture, security, performance, loading, transformations, protection | Extensive Snowflake hands-on | Required for Snowflake DE path |
| 6 | SnowPro Advanced DE (DEA-C02) | Snowflake | Advanced | After Core + 10 weeks | Data movement, transformation, performance, storage, governance | 2+ years DE experience with Snowflake | Strategic — highest Snowflake credential |

**Certification sequencing guidance:**
- Take at most one entry-level cert to build confidence, then skip to associate-level
- Never schedule an exam before scoring 80%+ on practice tests (85% for advanced)
- Use the certification-tutor-prompt.xml tool for practice: /quiz for domains, /exam for full simulation
- Budget the 14-day mandatory retake wait period into planning

---

## VIII. Skills Matrix

| Skill / Domain | After Phase 1 | After Phase 3 | After Phase 6 | After Vendor Branch |
|---|---|---|---|---|
| **SQL** | Intermediate (window functions, CTEs, EXPLAIN) | Advanced (optimization, complex joins, DDL) | Expert (cross-engine, performance tuning) | Expert + vendor dialect |
| **Python** | Intermediate (project structure, testing) | Advanced (pipelines, transforms, testing) | Advanced (API serving, CI integration) | + vendor SDK proficiency |
| **Linux / CLI** | Proficient (navigation, scripting, processes) | Proficient | Proficient | Proficient |
| **Docker / Containers** | Working (Compose, profiles, health checks) | Fluent (multi-service stacks) | Fluent + Kubernetes basics | + managed container services |
| **Data Modeling** | None | Intermediate (star schema, SCD) | Advanced (multi-domain, governance-aware) | + vendor-specific optimization |
| **ETL / ELT Pipelines** | None | Working (dlt + dbt + Dagster) | Production-grade (CDC, monitoring, CI/CD) | + vendor service implementation |
| **Streaming** | Conceptual | Conceptual + Kafka literacy | Applied (CDC, windowing concepts) | + vendor streaming services |
| **Data Governance** | None | Awareness | Applied (masking, RLS, audit, contracts) | + vendor governance tools |
| **Security** | Secret management basics | + encryption, RBAC concepts | + PII masking, multi-tenant | + vendor IAM, CMK, endpoints |
| **Performance Tuning** | SQL EXPLAIN | + partitioning, file sizing | + skew, spill, compaction, benchmarking | + vendor-specific optimization |
| **Cloud Architecture** | None | Conceptual | Design-level (ADRs, cost, scaling) | Implemented on target platform |
| **Observability** | None | Basic (Dagster UI) | Applied (Prometheus, alerting, runbooks) | + vendor monitoring stack |
| **Certification Readiness** | LFCA eligible | None | None | Target cert exam-ready |

---

## IX. Milestones and Assessments

### Checkpoint Quizzes (30 min each, 70% pass threshold)

| Checkpoint | After | Topics |
|---|---|---|
| Q0 | Phase 0 | Self-assessment: SQL, Python, Git, networking |
| Q1 | Phase 1 | Docker Compose, bash scripting, SQL window functions, Python project structure |
| Q2 | Phase 2 | Data modeling, ETL/ELT, distributed systems, data quality, architectures |
| Q3 | Phase 3 | Iceberg, Trino, dlt, dbt, Dagster — tool mechanics and integration |
| Q4 | Phase 4 | CDC, security patterns, performance diagnosis, observability |
| Q5 | Phase 5 | CI/CD, Kubernetes, cloud concepts, FinOps, architecture design |

### Hands-On Labs (graded by rubric)

| Lab | Phase | Deliverable |
|---|---|---|
| L1 | 1 | Docker Compose + PostgreSQL + health-check script |
| L2 | 2 | Star schema + SCD Type 2 in PostgreSQL |
| L3a | 3 | MinIO + Iceberg + HMS + Trino stack running |
| L3b | 3 | dlt ingestion pipeline (incremental) |
| L3c | 3 | dbt models with contracts + tests + docs |
| L3d | 3 | Dagster orchestration of full pipeline |
| L4a | 4 | CDC pipeline (Debezium -> Kafka -> Iceberg) |
| L4b | 4 | PII masking pipeline with audit trail |
| L4c | 4 | Performance diagnosis and optimization report |
| L5 | 5 | CI/CD pipeline + Kubernetes deployment |

### Portfolio Projects

| Project | Phase | Scope |
|---|---|---|
| P1 | Phase 6 | Vendor-agnostic capstone: full lakehouse from scratch |
| P2 | Vendor branch | Platform-specific capstone: rebuild on target vendor |

### Mock Certification Checkpoints

| Mock | When | Format | Pass Threshold |
|---|---|---|---|
| LFCA mock | End of Phase 1 | 30 MCQ, 45 min | 80% |
| Vendor mock 1 | Mid vendor branch | 30 questions, domain-weighted | 75% |
| Vendor mock 2 | End vendor branch | Full-length simulation | 80% (85% for advanced) |

---

## X. Final Recommended Sequence

1. **Phase 0** — Orientation and self-assessment (1 week)
2. **Phase 1** — Linux, networking, Python, Docker, SQL, Git (5-6 weeks)
3. *(Optional)* LFCA certification attempt
4. **Phase 2** — Data modeling, ETL/ELT, distributed systems, data quality, architectures (5-6 weeks)
5. **Phase 3** — Build the lakehouse: MinIO, Iceberg, HMS, Trino, dlt, dbt, Dagster, Metabase (7-9 weeks)
6. **Phase 4** — CDC, semi-structured data, security, performance, observability (4-5 weeks)
7. **Phase 5** — CI/CD, Kubernetes, cloud concepts, FinOps, data serving (3-4 weeks)
8. **Phase 6** — Vendor-agnostic capstone project (3-4 weeks)
9. **Choose vendor branch:**
   - **9a. AWS** — S3, Glue, Kinesis, Athena, Redshift, Step Functions, IAM/KMS (7-9 weeks) -> DEA-C01 cert
   - **9b. Azure** — ADLS, ADF, Synapse, Databricks, Event Hubs, Purview, Fabric (8-10 weeks) -> DP-700 cert
   - **9c. Snowflake** — Architecture, warehouses, Snowpipe, Snowpark, governance (14-20 weeks) -> SOL-C01 -> COF-C02 -> DEA-C02 certs
10. **Certification preparation** — Practice exams, weak-area remediation, exam scheduling (2-4 weeks)

**Total timeline (one vendor path):** 38-50 weeks at 10-12 hours/week (~400-550 hours)

---

## XI. Assumptions

- The learner has access to a machine with 16GB RAM (minimum) for the Docker-based lakehouse stack.
- The learner can dedicate 10-12 hours per week consistently. Faster paces are possible with more hours; the sequencing does not change.
- Cloud vendor accounts (AWS Free Tier, Azure $200 credit, Snowflake 30-day trial) will be used for vendor branches. Lab costs are estimated at $0-100 per branch.
- The LFCA certification is included as an optional early milestone based on its domain coverage (Linux, networking, cloud, security, DevOps), not because the source documents contain a full LFCA curriculum. The learner will need supplementary exam-specific study.
- DP-203 content is treated as learning material only (exam retired March 2025). The certification target for Azure is DP-700 (Fabric).
- Snowflake's three-certification path (Platform -> Core -> DE) is presented as a single branch because the certifications are sequential prerequisites; the learner may stop after any level.
- Where source documents reference different tools for the same function (e.g., Dagster vs. Airflow for orchestration), the curriculum teaches the primary tool hands-on and the alternatives conceptually, with enough transferable knowledge to switch.

---

## XII. Outcome

A learner who completes the shared core and one vendor branch will operate as a capable mid-level data engineer: designing data models, building and orchestrating production pipelines, implementing security and governance, diagnosing performance issues, and deploying on their chosen cloud platform — with at least one industry certification proving it.

---
---

# Part 2: Adversarial Analysis (8 Findings)

> These findings drive every change in the implementation plan.

---

# Adversarial Analysis [V1] — Unified Data Engineering Course Plan

> 2026-04-09 | Deep Analysis | Lens: Round 1 — "Is this the right thing?"

---

## Scope and Prior Rounds

**Subject:** `UNIFIED_COURSE_PLAN.md` (914 lines) — a unified data engineering curriculum synthesizing five source documents into a single progressive path from foundations through vendor certification.

**Source documents analyzed for context (now fully integrated into this course):**
- Open-source lakehouse curriculum
- AWS DEA-C01 study plan
- Azure DP-203/DP-700 implementation plan
- Snowflake SnowPro triple cert study plan
- LFCA tutor implementation plan

**What this analysis examines:** Whether the plan's structure, scope, sequencing, and hour budgets will produce the claimed outcome — a learner who can "operate as a mid-level data engineer in a professional environment."

**Prior rounds:** None. This is the first adversarial pass.

---

## What This Analysis Does NOT Challenge

- **The foundational-before-vendor principle.** This is sound curriculum design. Teaching open-source concepts before vendor abstractions produces engineers who understand *why*, not just *how*.
- **The Medallion architecture as a unifying pattern.** It is genuinely the most common layered data architecture in industry and serves as a good pedagogical scaffold.
- **The tool selection for the open-source stack.** MinIO, Iceberg, Trino, dbt, dlt, Dagster are defensible modern choices. They are not the only choices, but they form a coherent stack.
- **The three-vendor-branch structure.** AWS, Azure, and Snowflake cover the vast majority of the employer market. Offering branches rather than forcing a single vendor is correct.
- **The progressive Docker Compose profiles approach.** Starting with `storage` and layering services is a practical way to manage complexity and machine resources.

---

## 1. The Total Hour Budget Is Likely 30-50% Underestimated [SERIOUS]

### The problem

The plan claims 400-550 hours for one vendor path (38-50 weeks at 10-12h/week). Let's audit the individual phases:

| Phase | Claimed Hours | Likely Hours | Delta |
|-------|--------------|-------------|-------|
| Phase 0 | 5-8h | 5-8h | — |
| Phase 1 | 55-65h | 65-80h | +10-15h |
| Phase 2 | 55-70h | 55-70h | — |
| Phase 3 | 80-100h | 110-140h | +30-40h |
| Phase 4 | 45-55h | 60-75h | +15-20h |
| Phase 5 | 35-45h | 40-55h | +5-10h |
| Phase 6 | 30-40h | 50-70h | +20-30h |
| Vendor branch | 80-180h | 100-200h | +20h |
| **Total** | **400-550h** | **530-720h** | **+130-170h** |

**Phase 3 is the most underestimated.** The plan asks the learner to deploy 7 interconnected services (MinIO, Iceberg, HMS, Trino, dlt, dbt, Dagster, Metabase), learn each one's configuration, build a complete ELT pipeline, and set up CI tests — in 80-100h. Each tool has its own configuration surface, failure modes, and debugging patterns. HMS alone regularly produces cryptic Thrift errors that can consume hours. Trino catalog configuration and JVM tuning are not trivial. The plan pins specific versions (Trino 470, HMS 4.0.1), which is good for reproducibility but means learners hit version-specific bugs without community guidance for that exact combination.

**Phase 6 capstone requires 12 components** (listed at lines 496-512): streaming producer, batch API source, CDC via Debezium, MinIO+Iceberg storage, HMS catalog, dbt transformations with contracts/tests/unit tests/docs, Trino queries, Dagster orchestration with schedules/sensors/quality checks, PII masking + RLS + audit, Prometheus + alerting, Metabase + FastAPI serving, GitHub Actions CI/CD, documentation. Building this from scratch in 30-40 hours assumes the learner makes zero wrong turns. For a learner who has *never built a production system*, 50-70h is more realistic — and even that is aggressive.

### Why this matters

If a learner budgets 10 months and the course actually takes 13-16 months, they burn out, question the curriculum, or rush through advanced phases where deep understanding matters most. Underestimated hour budgets are the #1 cause of self-paced course abandonment.

### What this means

Either increase the hour estimates to honest ranges, or reduce scope per phase. The plan already has an escape hatch at Phase 4 for experienced learners entering vendor branches — formalize similar off-ramps for Phase 3 (e.g., a "core track" that skips Metabase and Dagster-dlt integration, and a "full track" that includes everything).

---

## 2. Apache Spark Has No Hands-On Coverage in the Core Phases [SERIOUS]

### The problem

Spark is mentioned in Phase 2 under "Processing engines" (line 221) and appears heavily in both the AWS branch (Glue = Spark, EMR) and Azure branch (Synapse Spark, Databricks). The Snowflake branch has Snowpark, which has a DataFrame API modeled on Spark. Yet the learner never writes a single line of PySpark code before entering a vendor branch.

The plan teaches Trino as the query engine (distributed SQL), which is the right choice for the open-source lakehouse. But Trino and Spark solve different problems:

- **Trino:** Interactive analytics, federated queries, SQL-first.
- **Spark:** Large-scale batch ETL, ML preprocessing, DataFrame transformations.

A learner who finishes Phase 6 can write Trino SQL and dbt models but cannot write a Spark job. When they enter the AWS branch and encounter Glue or EMR, they must simultaneously learn (a) the AWS service, (b) Spark fundamentals (lazy evaluation, partitions, shuffles, broadcast joins, the entire executor model), and (c) how they interact. This is a triple learning burden where only (a) should be new.

### Why this matters

The AWS DEA-C01 exam's largest domain is "Ingestion & Transformation" at 34% — and Glue (Spark-based) is the primary transformation service. The Azure DP-700 and Databricks paths assume Spark fluency. The plan's own Phase 4 references "data skew" (line 385), "AQE skew join, salting, broadcast join" (line 385), and "executor OOM vs. driver OOM" (line 387) — all Spark-specific concepts. But these concepts are taught in Phase 4 without the learner ever having run a Spark job.

### What this means

Add a PySpark module to Phase 3 (8-12h) or Phase 4 (before performance tuning). The learner should at minimum: read Parquet from MinIO, apply transformations (filter, groupBy, join), understand lazy evaluation and actions vs. transformations, write back to Iceberg, and encounter a shuffle. This can be done with a local PySpark session against MinIO — no new infrastructure needed. Alternatively, introduce DuckDB's Python API earlier as a stepping stone, since DuckDB's DataFrame-like interface teaches similar concepts without Spark's operational overhead.

---

## 3. Streaming Is Taught Conceptually for 30+ Weeks Before Any Hands-On [MODERATE]

### The problem

The Skills Matrix (line 824) is transparent about this: streaming is "Conceptual" after Phase 3 and only reaches "Applied (CDC, windowing concepts)" after Phase 6. Kafka architecture is taught in Phase 2 (line 226) purely conceptually. CDC with Debezium appears in Phase 4 (line 362), which is the first real streaming-adjacent hands-on — but Debezium-to-Kafka is micro-batch CDC, not true stream processing.

The learner completes 30+ weeks of study before writing their first streaming consumer. The only hands-on streaming happens in vendor branches (Kinesis for AWS, Event Hubs + Stream Analytics for Azure, Snowpipe Streaming for Snowflake).

### Why this matters

The plan correctly notes "90%+ of real work is batch" (line 66), so deferring streaming is defensible. However, streaming questions appear on every certification exam:
- AWS DEA-C01: Kinesis is a major exam topic within the 34% Ingestion & Transformation domain
- Azure DP-700: Event Hubs, Stream Analytics, Structured Streaming are tested
- Snowflake DEA-C02: Snowpipe Streaming, Kafka connector, Streams are tested

A learner who reaches a vendor branch with zero streaming hands-on experience must learn both the streaming paradigm *and* the vendor's implementation simultaneously.

### What this means

The CDC lab in Phase 4 (Debezium -> Kafka -> dlt -> Iceberg) already introduces Kafka infrastructure. Extend this lab by 4-6h to include: (a) producing messages to a Kafka topic with a Python producer, (b) consuming messages with a basic consumer, (c) observing partition behavior, (d) a simple windowed aggregation (even with DuckDB reading from the Kafka-written files). This gives the learner tactile streaming experience without adding a new major tool.

---

## 4. Phase 2 Theory Block Risks Motivation Collapse [MODERATE]

### The problem

Phase 2 is 55-70 hours of nearly pure conceptual content: data modeling, pipeline paradigms, distributed systems, data quality, file formats, architecture landscape, database landscape, streaming concepts. The practical exercises (lines 231-236) are limited to PostgreSQL and DuckDB work — the learner is still using the same tools from Phase 1.

After Phase 1 (which is mostly practical — Docker, bash scripting, SQL, Python), the learner enters 5-6 weeks where the primary activity is reading, diagramming, and answering concept questions. The plan claims "practical-first assessment" (Principle 7, line 43), but Phase 2 is theory-first by design.

### Why this matters

Self-paced learners report the highest dropout rates during extended theory-only phases. The learner has *just* built Docker skills in Phase 1 and is eager to use them. Instead, they spend 5-6 weeks before touching MinIO. The gap between learning Docker Compose and actually deploying the lakehouse stack is ~10-12 weeks (Phase 1 + Phase 2), during which Docker skills atrophy.

### What this means

Two resolution paths:

**Option A: Interleave theory and practice.** Merge the first 2-3 weeks of Phase 3 (MinIO, Iceberg basics, Trino basics) into the end of Phase 2. The learner deploys the storage + query layers *while* learning about file formats, table formats, and distributed systems. This gives the concepts immediate grounding.

**Option B: Reduce Phase 2 duration.** Move "Database & Engine Landscape" (6h) and "Architecture Landscape" (8h) to a reference appendix. These are survey topics that don't require deep study before Phase 3 — the learner will understand them better *after* using the tools. This cuts Phase 2 to ~40-50h.

---

## 5. The Capstone (Phase 6) Scope Creates a Bottleneck Before Vendor Branches [MODERATE]

### The problem

Phase 6 requires 12 integrated components (lines 496-512). This is simultaneously the most ambitious deliverable in the curriculum and the gate to vendor specialization. Every learner must complete this regardless of their target certification.

For a learner whose goal is AWS DEA-C01 certification in ~9 months, the critical path is:

```
Phase 0 (1w) + Phase 1 (6w) + Phase 2 (6w) + Phase 3 (9w) + Phase 4 (5w) + Phase 5 (4w) + Phase 6 (4w) = 35 weeks
+ AWS Branch (9w) + Cert Prep (4w) = 48 weeks total
```

Phase 6 adds 3-4 weeks (realistically 4-6 weeks) to the timeline for every learner. A mid-career professional re-skilling to DE may need to show a certification within 6-8 months to be competitive in the job market.

### Why this matters

The capstone is valuable for portfolio building and skill consolidation. But if a learner has been building incrementally through Phases 3-5 (each producing its own deliverables and labs), the capstone largely re-integrates what they've already built. The incremental deliverables from Phases 3-5 (L3a through L5 in the assessment table) *already demonstrate* the same skills.

### What this means

Make Phase 6 **optional but recommended.** Provide a "fast track" gate: if the learner's Phase 3-5 deliverables collectively meet a rubric (covering all 12 capstone dimensions across their individual labs), they can proceed to vendor branches with Phase 6 as a stretch goal to complete in parallel. This preserves the capstone for portfolio-oriented learners without blocking certification-oriented learners.

---

## 6. The "Mid-Level Data Engineer" Outcome Claim Is Undefined and Risky [MODERATE]

### The problem

The plan's outcome statement (line 913) claims the learner will "operate as a capable mid-level data engineer." The Skills Matrix (Section VIII) shows "Expert" SQL and "Advanced" Python after Phase 6 — but these ratings are self-referential (defined by the curriculum itself, not by external benchmarks).

Industry expectations for a mid-level DE typically include:
- 2-3 years of production experience (not lab experience)
- Ownership of at least one production pipeline end-to-end
- On-call experience with production incidents
- Cross-functional collaboration (working with analysts, scientists, PMs)
- Working within existing codebases (not greenfield)
- Operating under cost constraints with real data volumes

The curriculum produces a learner who has built everything from scratch in a controlled local environment. They have never:
- Debugged a production incident at 2 AM
- Dealt with a 500GB daily data volume
- Worked within an existing team's codebase with technical debt
- Managed cloud costs with real money
- Handled stakeholder requests and priority conflicts

### Why this matters

Overclaiming outcomes creates a mismatch between learner expectations and employer expectations. A hiring manager reading "mid-level" expects production battle scars. The learner is *entry-level with exceptionally strong theoretical foundations and broad tool exposure* — which is genuinely valuable, but should be marketed accurately.

### What this means

Reframe the outcome statement: "A learner who completes the shared core and one vendor branch will enter the job market as a **strong junior / early mid-level data engineer** with unusually broad architectural knowledge, hands-on tool proficiency across the modern data stack, and at least one industry certification. The breadth of the open-source core gives them a faster path to mid-level than typical bootcamp graduates, who often know only one vendor's tools."

This is honest, still compelling, and sets correct expectations.

---

## 7. 16GB RAM Assumption Excludes a Significant Learner Segment [MODERATE]

### The problem

Line 901: "The learner has access to a machine with 16GB RAM (minimum)." The original lakehouse source document specifies the full stack needs ~11-12GB, and Trino alone needs 4GB JVM heap.

The plan targets career changers and junior engineers. In many markets (Latin America, Southeast Asia, Eastern Europe), 8GB machines are common. Apple's base MacBook Air ships with 8GB. Corporate-issued machines may be locked down.

### Why this matters

This is a hard gate. Unlike hour estimates (which flex), RAM is binary: the stack either runs or it doesn't. A learner who completes Phases 0-2 (26 weeks of study) and then discovers their machine can't run Phase 3 faces a devastating interruption.

### What this means

Three mitigations (implement all):

1. **Surface the requirement in Phase 0**, not in an assumptions section at line 901 that many learners won't read. The self-assessment should include "verify your machine has 16GB+ RAM."
2. **Provide a cloud fallback**: GitHub Codespaces (free tier: 60h/month, 4-core/8GB) or Gitpod can run the Docker stack. Document the setup.
3. **Design a "light" Phase 3 profile** that runs MinIO + Trino + PostgreSQL without HMS (using Iceberg's JDBC catalog instead of Thrift HMS). This fits in 8GB and covers 80% of the learning objectives, with HMS added when resources allow.

---

## 8. No Airflow Coverage Despite 70% Job Market Share [STRUCTURAL]

### The problem

The plan teaches Dagster as the primary orchestrator and mentions Airflow only in comparison (line 320: "Orchestrator landscape comparison: Dagster vs. Airflow vs. Prefect"). The original lakehouse source document notes Airflow has ~70% of job postings.

The plan's defense is Principle 3 ("open-source before proprietary") and Principle 7 ("transferable knowledge"). These are valid — Dagster's asset-centric model is arguably better pedagogy than Airflow's task-centric model. However:

- AWS MWAA is Managed Airflow. The AWS branch teaches it (line 554).
- Many employers list "Airflow experience" as a hard requirement.
- The learner completes 35+ weeks without writing a DAG, then encounters MWAA cold.

### Why this matters

This is a structural tension between "teach the best tool for learning" and "teach the most employable tool." The plan makes a defensible pedagogical choice but doesn't adequately bridge the gap.

### What this means

Add a 4-6h "Airflow bridge" module in Phase 5 (alongside the CI/CD and Kubernetes content, both of which are operations-oriented). Content: (a) install Airflow via Docker Compose, (b) write one DAG that replicates a Dagster pipeline from Phase 3, (c) compare the two paradigms concretely. This is not about mastering Airflow — it's about giving the learner enough context to say "I've used both Dagster and Airflow" in an interview, and enough familiarity that MWAA in the AWS branch isn't cold.

---

## Risk Matrix

| # | Risk | Severity | Requires |
|---|------|----------|----------|
| 1 | Hour budget 30-50% underestimated — learner burnout and dropout | SERIOUS | Revised hour estimates or reduced scope |
| 2 | No Spark hands-on before vendor branches — triple learning burden | SERIOUS | PySpark module in Phase 3 or 4 (8-12h) |
| 3 | Streaming remains conceptual for 30+ weeks | MODERATE | Extended CDC lab with Kafka producer/consumer |
| 4 | Phase 2 theory block risks motivation collapse | MODERATE | Interleave early Phase 3 tools or reduce Phase 2 |
| 5 | Phase 6 capstone bottlenecks all paths to vendor branches | MODERATE | Optional capstone with fast-track rubric gate |
| 6 | "Mid-level" outcome claim sets incorrect expectations | MODERATE | Reframe to "strong junior / early mid-level" |
| 7 | 16GB RAM hard gate discovered too late | MODERATE | Phase 0 check + cloud fallback + light profile |
| 8 | No Airflow despite 70% job market share | STRUCTURAL | 4-6h Airflow bridge module in Phase 5 |

---

## Suggested Priority for Resolution

**Immediate (before any learner starts):**
1. **#7 — RAM requirement:** Move to Phase 0 and provide cloud fallback. Zero-cost fix, high-impact gate removal.
2. **#1 — Hour estimates:** Revise to honest ranges. This is transparency, not scope change.
3. **#6 — Outcome claim:** Single sentence edit. Prevents expectation mismatch.

**Before Phase 3 content is finalized:**
4. **#2 — Spark hands-on:** Design and place the PySpark module. This affects Phase 3-4 structure.
5. **#4 — Phase 2 theory block:** Decide on interleaving vs. trimming. Affects Phase 2-3 boundary.

**Before Phase 5 content is finalized:**
6. **#8 — Airflow bridge:** Design 4-6h module. Slot into Phase 5.
7. **#3 — Streaming hands-on:** Extend Phase 4 CDC lab with Kafka basics.

**Before launch:**
8. **#5 — Capstone gate:** Design fast-track rubric. This is a policy decision, not content creation.

---
---

# Part 3: Source Document Categorizations

> These categorizations show the full knowledge domain inventory from each source document. Use them to verify that content additions (PySpark, Kafka, Airflow) align with the source material and that no critical topics are dropped during edits.

---

## 3A. Open-source lakehouse curriculum

### Software Engineering / Programming

* **Python project structure:** `pyproject.toml` as single source of truth, project layout conventions (pipelines/, orchestration/, tests/, notebooks/), `.python-version` file
* **Dependency management tools:** uv (Rust-based, 10-100x faster than pip), pip + venv (built-in), Poetry (lockfile + publishing), conda (cross-language) — choosing based on project needs
* **Bash scripting fundamentals:** Variables, loops, conditionals, exit codes, `jq` for JSON manipulation, piping/redirection (`|`, `>`, `2>&1`, `tee`), `xargs` for batch operations
* **Health-check scripts:** Writing shell scripts to verify service availability using `nc -z` port checks
* **Pre-commit hooks:** `dbt-checkpoint` for model quality (minimum tests, descriptions, naming contracts), `ruff` for Python linting/formatting — enforcing standards before code enters repo
* **Git workflows for data teams:** Branching strategy for dbt projects (feature branches, hotfix branches), PR review checklists, merge conflict resolution for generated files
* **pytest patterns:** `materialize_to_memory` for Dagster assets, DuckDB for SQL logic testing in CI, `dlt` pipeline testing with schema contracts
* **Code quality tooling:** ruff (linter + formatter), mypy (type checking), pre-commit (git hooks) — configured via `pyproject.toml`
* **Project layout conventions:** Separating dlt pipelines, dbt projects, Dagster orchestration, and tests into distinct directories with clear boundaries
* **Quick start automation:** `setup.sh` scripts that validate prerequisites (Docker version, available RAM, required ports), create `.env` from template, and start appropriate services

### Data Engineering (Basic Knowledge)

* **Data modeling fundamentals:** Conceptual -> Logical -> Physical modeling, normalization (1NF-3NF) vs. denormalization, OLTP vs. OLAP, row vs. columnar storage
* **Dimensional modeling (Kimball):** Star schema, snowflake schema — fact and dimension table design for analytical workloads
* **Slowly Changing Dimensions:** Type 1 (overwrite), Type 2 (versioned rows with effective dates), Type 3 (columns), Type 6 (hybrid) — SCD Type 2 most commonly tested
* **ETL vs. ELT:** ETL transforms before loading; ELT loads raw then transforms in-place — this curriculum is ELT (dlt = E+L, dbt = T, Trino = compute)
* **Batch vs. streaming processing:** Batch (minutes-hours, analytics/reporting), micro-batch (seconds-minutes, near-real-time dashboards), true streaming (milliseconds, fraud detection/IoT)
* **Idempotency patterns:** UPSERT/MERGE, delete-and-replace, checkpointing — operations that produce the same result when repeated
* **Data quality dimensions:** Accuracy, completeness, consistency, timeliness, validity, uniqueness — framework for evaluating data health
* **Data governance fundamentals:** Roles, classification (PII/Sensitive/Internal/Public), lineage, governance-as-code, data retention policies
* **Data lakehouse architecture:** Open table formats (Iceberg, Delta Lake, Hudi) + decoupled compute + object storage, Medallion pattern (Bronze/Silver/Gold)
* **Data contracts:** Schema enforcement at transformation boundaries — what they are, why they matter, how they fit Bronze->Silver->Gold boundaries
* **Apache Kafka architecture (conceptual):** Topics, partitions, consumer groups, offsets, retention policies, at-least-once/at-most-once/exactly-once delivery semantics
* **Data processing engines landscape:** Trino (distributed SQL, interactive analytics), Spark (large-scale ETL, ML), Flink (real-time event processing) — overlapping but distinct problem spaces
* **NoSQL database families:** Document (MongoDB), Column-family (Cassandra), Graph (Neo4j), Key-Value (Redis) — use cases, data models, and how DEs ingest from each
* **Polyglot persistence:** Modern applications using multiple database types simultaneously; DE role is ingesting from all into a unified analytical layer
* **Distributed systems fundamentals:** CAP theorem (Consistency, Availability, Partition tolerance), partitioning/sharding, replication, consistency models (strong, eventual, read-your-writes)
* **Horizontal vs. vertical scaling:** Adding nodes (scale out) vs. bigger machines (scale up) — lakehouse architecture designed for horizontal scaling at each layer
* **Modern data architectures:** Medallion (layered refinement), Data Mesh (domain-oriented ownership), Data Fabric (metadata-driven integration), Data Hub (centralized metadata), serverless data (pay-per-query)
* **Hadoop ecosystem legacy:** HDFS -> MinIO, MapReduce -> Trino/dbt, YARN -> Dagster/Kubernetes, Hive -> Trino — understanding the evolution from Hadoop era (2006-2015) to Spark era (2015-2020) to Lakehouse era (2020+)
* **Orchestrator landscape:** Dagster (asset-centric), Airflow (DAG-centric, ~70% of job postings), Prefect (flow-centric), Luigi (task-centric, legacy), Mage (block-centric) — transferable concepts across tools
* **Incremental loading patterns:** Cursor-based (timestamp/ID), append (immutable events), merge (mutable entities with primary key)
* **Schema registries:** Confluent, AWS Glue, Apicurio — storing versioned schemas, validating incoming data, enforcing compatibility rules (backward, forward, full)
* **Schema evolution workflow:** Propose change -> check compatibility -> auto-register or reject -> downstream validation at transformation boundary
* **Data sources taxonomy:** Relational databases, APIs, files, logs, mobile apps, IoT devices, CDC — understanding ingestion patterns for each source type
* **Relational database landscape:** PostgreSQL, MySQL/MariaDB, Oracle, MS SQL Server, Aurora, Cloud SQL, Azure SQL — dialect differences and DE interaction patterns
* **PostgreSQL DBA essentials:** `pg_dump`/`pg_restore`, indexing strategies (B-tree, GIN), `EXPLAIN ANALYZE`, `VACUUM`/`ANALYZE` (MVCC dead tuples), connection pooling (PgBouncer), monitoring (`pg_stat_activity`)
* **Apache Iceberg architecture:** Three-layer design (data/Parquet, metadata/manifests, catalog/pointer) — snapshot isolation, schema evolution, hidden partitioning, time travel
* **Open table format comparison:** Iceberg vs. Delta Lake vs. Hudi — ACID on object storage, each with different strengths
* **Query performance tuning:** `EXPLAIN` vs. `EXPLAIN ANALYZE`, predicate pushdown, partition pruning, dynamic filtering, caching strategies, sorted data for better pushdown
* **Performance benchmarking methodology:** Establish baselines (3 runs, discard cold cache), change one variable at a time, document before/after — "never optimize without a benchmark"
* **Dead-letter queue pattern:** Routing failed records to a separate destination for investigation instead of failing the entire pipeline
* **Pipeline resilience patterns:** Retry with exponential backoff and jitter, dead-letter queues, circuit breakers, poison-pill handling
* **Data documentation strategy:** Documentation-as-code pyramid, business glossaries, ADRs, auto-generated docs
* **CDC with Debezium:** PostgreSQL WAL -> Debezium -> Kafka -> ingestion -> MERGE INTO for real-time change data capture
* **Multi-tenant data isolation:** Row-level filtering, schema-per-tenant, catalog-per-tenant strategies
* **API-first data serving:** Serving Gold-layer data to applications via REST APIs — API vs. SQL decision guide
* **Feature stores and ML data patterns:** Gold-layer feeding ML training, feature engineering, ML/AI data pipeline design

### Course/Tool Specific Content

* **dlt (data load tool):** Pure Python E+L library — `@dlt.source`, `@dlt.resource`, `dlt.pipeline()`, schema inference, JSON normalization, 60+ verified sources, `schema_contract` options (evolve, disallow_additions, disallow_all)
* **dlt with pandas transforms:** Using pandas within dlt transformers for row-level math/science (haversine distance, IQR outlier removal) before loading to Bronze
* **dlt filesystem + Iceberg destination:** SQLite per-table catalogs; for full catalog functionality, use external catalog (HMS, Polaris)
* **Dagster orchestration:** Software-Defined Assets, webserver + daemon + code locations architecture, schedules, sensors, partitions, asset checks, retry policies
* **dagster-dbt integration:** Mapping each dbt model to a Dagster asset via `@dbt_assets` decorator with manifest.json
* **dagster-dlt integration:** `@dlt_assets` decorator with known limitation (multi-table resources create single Dagster asset), workaround with `@multi_asset`
* **Dagster testing:** `materialize_to_memory` with `DagsterInstance.ephemeral()` for isolated asset testing
* **Dagster retry policies:** `RetryPolicy` with `Backoff.EXPONENTIAL` and `Jitter.PLUS_MINUS` to prevent thundering herd
* **dbt-trino adapter:** Configuration for Trino backend (`type: trino`, `database: iceberg`, `schema: analytics`)
* **dbt data contracts (1.8+):** `contract: enforced: true` for preflight schema enforcement with column types and constraints
* **dbt unit tests (1.8+):** `unit_tests` block with given/expect pattern for testing transformation logic without running against real data
* **dbt project structure for Medallion:** `models/staging/` (stg_) -> Silver, `models/intermediate/` (int_) -> Silver, `models/marts/` (fct_, dim_) -> Gold
* **Trino configuration:** `trinodb/trino:470` pinned, coordinator + workers, 50+ connectors, `iceberg.properties` catalog config, JVM tuning (`-Xmx4g`)
* **Trino-specific optimization:** Data cache (Parquet footers/column chunks), metadata caching (`hive.metastore-cache-ttl`), dynamic filtering (bloom filters from build side), `EXECUTE optimize` for compaction
* **Hive Metastore (HMS):** `apache/hive:4.0.1`, standalone Thrift service on 9083, PostgreSQL backend (never Derby), stores only `metadata_location` pointer for Iceberg
* **Apache Polaris:** REST API catalog (graduated to Apache TLP Feb 2026) — modern alternative to HMS for greenfield deployments
* **Nessie catalog:** REST + Git-like versioning for data experimentation and atomic multi-table commits
* **MinIO:** S3-compatible object storage — `RELEASE.2025-01-20T14-49-07Z` pinned, buckets, `mc` CLI, web console, `path-style-access=true` requirement
* **Metabase:** `v0.51.0` with native Trino support (no external Starburst driver needed) — dashboards and BI visualization
* **DuckDB:** Embedded analytical database for local Parquet/Iceberg exploration, CI/CD testing, prototyping SQL — complement to Trino (SQLite is to PostgreSQL as DuckDB is to Trino)
* **Docker Compose profiles:** `storage`, `metadata`, `query`, `orchestration`, `visualization`, `full` — progressive service activation matching curriculum weeks
* **Pinned tool versions:** Trino 470, Hive 4.0.1, MinIO RELEASE.2025-01-20, PostgreSQL 16-alpine, Metabase v0.51.0, dbt-core 1.11.6, dbt-trino 1.10.1, dlt 1.6+, Dagster 1.9+
* **Memory requirements by profile:** storage (~2GB) -> +metadata (~3.5GB) -> +query (~8.5GB) -> full (~11-12GB), 16GB minimum recommended

### Security & Compliance

* **Data classification scheme:** PII (names, emails, phones), Sensitive (salary, health), Internal (operational metrics), Public (aggregated stats) — with dbt meta tags for enforcement
* **Column masking in Trino:** `regexp_replace` for email masking, creating masked views per role
* **Access audit trails:** Querying `system.runtime.queries` in Trino for who-queried-what-when
* **GDPR compliance awareness:** Right-to-erasure implications for Bronze (immutable) vs. Silver/Gold (rebuildable), data retention policies
* **PII masking pipeline:** End-to-end PII detection -> masking -> access control -> right-to-erasure -> audit dashboard
* **Multi-tenant data isolation strategies:** Row-level filtering, schema-per-tenant, catalog-per-tenant — each with different security/complexity trade-offs
* **Secret management fundamentals:** `.env` files (never committed), `.gitignore` patterns, why hardcoded credentials are dangerous

### DevOps & Infrastructure

* **Docker deep-dive:** Containers, images, volumes, networks, Docker Compose — modern syntax (no `version` field), `mem_limit` for resource management
* **Docker Compose profiles:** Service subsets activated per curriculum week — learners only start services needed for current phase
* **Health checks in Docker:** `pg_isready`, `curl -f`, service discovery by hostname, named volumes for persistence
* **Version pinning rationale:** Why `postgres:16-alpine` over `postgres:latest` — real-world Trino `:latest` breaking change as example
* **Resource limits:** `mem_limit` and JVM heap flags for all services — preventing OOM on developer machines
* **Docker Desktop configuration:** macOS memory allocation (12GB minimum), Windows WSL `.wslconfig`, Linux RAM requirements
* **Prometheus + Grafana:** Infrastructure monitoring for pipeline observability — metrics collection and dashboard visualization
* **Kubernetes hands-on:** kind/Minikube lab deploying Trino via Helm chart — container orchestration fundamentals
* **CI/CD tool landscape:** GitHub Actions, GitLab CI, CircleCI, ArgoCD — pipeline automation for data project deployment
* **Alerting and incident response:** Alertmanager configuration, alert rules, notification channels, runbook templates, severity framework
* **OpenLineage standard:** Data lineage protocol for tracking data flow across tools — DataHub/OpenMetadata as catalog/discovery tools

### Cloud Computing Fundamentals

* **Multi-cloud service mappings:** AWS, Azure, GCP equivalent service comparison — understanding that concepts transfer across providers
* **Cost estimation and FinOps:** TCO comparison (self-hosted lakehouse vs. managed platforms like Snowflake/Databricks), cloud cost optimization patterns, query cost monitoring
* **Managed vs. self-hosted trade-offs:** Snowflake/BigQuery/Redshift as zero-ops commercial alternatives vs. open-source stack teaching the concepts underneath

### Networking Fundamentals

* **Prerequisites:** IP addresses, ports, DNS, HTTP/HTTPS, TCP vs. UDP — needed to understand Docker service communication via hostnames and ports
* **Service communication in Docker:** Why containers communicate via hostnames (service discovery) and exposed ports

### Pedagogy & Study Methodology

* **Target audience framing:** "From zero data engineering experience to building a production-grade open data lakehouse" — with non-negotiable prerequisites (intermediate SQL, basic Python, Linux/CLI, Git)
* **Week 0 self-assessment:** 45-minute quiz covering SQL (window functions, CTEs), Python (generators, context managers), networking (ports, HTTP), Git (branching) — 70% threshold
* **Suggested weekly rhythm:** 10-12h/week across Mon-Sat — concept study, hands-on labs, AI tutor quizzes, spaced repetition
* **Phase checkpoints:** Self-assessments after Phases 1, 2, and 3 with quizzes (70% passing) and hands-on exercises
* **Phase 1 checkpoint:** 30-minute quiz + 1-hour mini-project (fix 3 intentional Docker Compose issues)
* **Phase 2 checkpoint:** 2-hour integration exercise (fresh Docker stack -> Iceberg table -> dbt model -> Trino query -> DuckDB export)
* **Content density management:** Week 3 split into Core track (~14h, complete in week) and Reference track (~16h, revisit throughout curriculum)
* **Buffer weeks:** 1.5 weeks of buffer distributed across phases for catch-up and review
* **Priority labels for certification alignment:** Topics tagged with Snowflake SnowPro, IBM DE, Duke Python/Bash/SQL, DASCA ABDE certification relevance
* **Career context annotations:** Interview preparation advice tied to specific technical concepts (e.g., "Hadoop experience" in job postings means distributed data processing literacy)

---

## 3B. AWS DEA-C01 study plan

### Software Engineering / Programming

* **Idempotency patterns:** Designing operations that produce the same result when repeated — critical for reliable data pipelines regardless of platform
* **Error handling with retry and backoff:** Implementing retry policies with exponential backoff and dead-letter queues for failed processing
* **State machine design:** Defining task states, error handling, retry/catch logic, and parallel/map execution patterns in workflow orchestration

### Data Engineering (Basic Knowledge)

* **Batch vs. streaming ingestion patterns:** Choosing between bulk loading, CDC replication, and real-time streaming based on latency and volume requirements
* **ETL pipeline orchestration concepts:** DAG-based workflow design, parent-child pipeline patterns, event-driven vs. scheduled triggers
* **Data lake architecture:** Raw/curated/refined zone patterns, landing zone design, lifecycle policies for data progression through quality tiers
* **Star schema and dimensional modeling:** Fact tables, dimension tables, and their application in analytical workloads
* **Data quality validation:** Row counts, null checks, freshness checks, schema validation as pipeline health indicators
* **Incremental load patterns:** Watermark-based extraction (track last-processed timestamp), CDC for change tracking, append-only for immutable events
* **File format selection:** JSON, Parquet, Avro, ORC — trade-offs in compression, schema support, columnar vs. row access
* **Stream processing fundamentals:** Windowing concepts (tumbling, hopping, sliding, session), watermarks for late data, checkpoint-based fault tolerance, output modes (append, complete, update)

### Course/Tool Specific Content

* **DEA-C01 exam profile:** AWS Certified Data Engineer Associate — 170 minutes, 65 questions, passing score 720/1000, 4 domains
* **DEA-C01 domain structure:** Ingestion & Transformation (34%), Data Store Management (26%), Data Operations & Support (22%), Security & Governance (18%)
* **Amazon S3:** Universal landing zone — upload methods, multipart upload, S3 Transfer Acceleration, lifecycle policies, storage classes (Standard -> IA -> Glacier -> Deep Archive), intelligent tiering
* **AWS DMS:** Database Migration Service — CDC, full load, ongoing replication for database-to-S3 ingestion
* **AWS DataSync and Snow Family:** Bulk/offline data transfer mechanisms for large-scale or air-gapped migrations
* **Amazon AppFlow:** SaaS-to-S3 managed ingestion for sources like Salesforce, ServiceNow
* **Amazon Kinesis Data Streams (KDS):** Shards, partition keys, retention, consumers (KCL, enhanced fan-out)
* **Amazon Kinesis Data Firehose (KDF):** Delivery destinations, buffering, format conversion (JSON -> Parquet via Glue Catalog), Lambda transforms
* **Amazon MSK:** Managed Kafka — topics, partitions, consumer groups, MSK Connect, MSK Serverless
* **KDS vs. KDF vs. MSK decision matrix:** Choosing streaming service based on latency, management overhead, and consumer patterns
* **AWS Glue:** ETL jobs (Spark/Python), crawlers, DynamicFrames, bookmarks, job types (Spark, Python Shell, Ray)
* **AWS Glue DataBrew:** Visual data preparation, recipes, profiling — no-code transformation tool
* **AWS Glue Data Quality:** Rule-based data quality checks — completeness, uniqueness, freshness
* **AWS Glue Data Catalog:** Databases, tables, partitions, schema registry, crawlers for metadata discovery
* **Amazon EMR:** Managed Spark/Hive/Presto clusters, EMR Serverless, EMR on EKS
* **Amazon Managed Service for Apache Flink:** Real-time stream processing with SQL and Java/Scala applications
* **Glue vs. EMR vs. Flink decision matrix:** Choosing transformation service based on scale, latency, and operational complexity
* **AWS Step Functions:** State machines for pipeline orchestration — task states, error handling, retry/catch, parallel/map states
* **Amazon MWAA:** Managed Apache Airflow — DAGs, operators, sensors, connections
* **Amazon EventBridge:** Event-driven orchestration — rules, schedules, event buses for triggering workflows
* **Step Functions vs. MWAA decision matrix:** Choosing orchestration service based on workflow complexity and operational model
* **Amazon DynamoDB:** Key-value/document store — partition keys, sort keys, GSI/LSI, capacity modes, DynamoDB Streams
* **Amazon Redshift:** Columnar OLAP — Redshift Spectrum, materialized views, RA3 nodes, Redshift Serverless, data sharing
* **Amazon Athena:** Serverless SQL on S3 — partitioning, Iceberg tables, federated query, CTAS, workgroups, cost control
* **Amazon OpenSearch Service:** Search and log analytics
* **Amazon RDS / Aurora:** Managed relational databases — read replicas, Multi-AZ deployments
* **Amazon DocumentDB, Keyspaces, Neptune, MemoryDB:** Purpose-specific managed databases — when to choose each
* **AWS Lake Formation:** Data lake setup — governed tables, tag-based access control (TBAC), blueprints, column/row/cell-level security, data filters
* **AWS Lambda:** Event-driven processing — triggers (S3, Kinesis, SQS, EventBridge), concurrency, layers
* **AWS Batch:** Large-scale batch workloads — job definitions, compute environments
* **Amazon SageMaker AI:** Data preparation and Feature Store (in-scope portions for DE exam)
* **Amazon QuickSight:** Dashboards, SPICE engine, datasets, embedded analytics
* **Amazon CloudWatch:** Metrics, alarms, dashboards, Logs, Log Insights for pipeline monitoring
* **AWS CloudTrail:** API logging — data events, management events, trail configuration for audit
* **Amazon Managed Grafana:** Dashboards for pipeline monitoring
* **S3 Glacier:** Vault lock, retention policies for long-term archival

### Security & Compliance

* **Encryption concepts:** Envelope encryption, server-side encryption variants (SSE-S3, SSE-KMS, SSE-C), customer-managed keys, key policies
* **Identity and access management:** Identity vs. resource vs. SCP policies, cross-account access, federation, least-privilege principles
* **Network isolation:** VPC endpoints, PrivateLink for data isolation — preventing data traversal over public internet
* **Data masking:** Dynamic data masking in analytical warehouses, PII masking in ETL pipelines
* **Audit logging:** API logging, access logging, and audit trails for compliance and incident investigation
* **Sensitive data discovery:** Automated PII/sensitive data classification in storage systems
* **Data privacy patterns:** Tokenization, pseudonymization, data residency requirements
* **Credentials management:** Secrets rotation for pipeline connections — separating credentials from code

### Cloud Computing Fundamentals

* **Cloud storage tiers:** Hot/warm/cold/archive storage patterns with cost vs. access-time trade-offs — applicable across AWS, Azure, GCP
* **Serverless computing:** On-demand compute that scales to zero — Lambda, Athena, serverless Spark as examples of the pattern
* **Managed vs. self-managed services:** Trade-offs between operational overhead, cost, and control when choosing between managed Kafka (MSK) vs. self-hosted

### Pedagogy & Study Methodology

* **12-week phased study plan:** Foundation (Weeks 1-4, D1), Data Stores (Weeks 5-7, D2), Operations/Security (Weeks 8-10, D3/D4), Integration/Readiness (Weeks 11-12)
* **Weekly routine template:** Mon-Tue concepts (3-6h), Wed-Thu hands-on (3.5-7h), Fri-Sat exam practice (2.5-5h), Sun spaced repetition (1-2h)
* **Three-part learning flow:** Concepts (40%) -> Hands-on with LocalStack (35%) -> Exam practice questions (25%)
* **Session Pulse tracking:** Generated every 5 interactions to track domain accuracy, weak spots, and recommended focus
* **Mini mock exams:** 5-question domain assessments after each phase, full 65-question mock in Week 12
* **Capstone lab:** End-to-end pipeline (streaming -> ingestion -> catalog -> transform -> query -> orchestration -> security -> monitoring) in Week 11
* **Target threshold:** 80%+ on mock exams before scheduling the real exam
* **Lab environment strategy:** LocalStack for core services (free), AWS Free Tier for services needing real AWS

---

## 3C. Azure DP-700 implementation plan

### Software Engineering / Programming

* **Git integration for data pipelines:** Feature branches, collaboration branches, publish branches (`adf_publish`), ARM template deployment via Azure DevOps or GitHub Actions
* **Pipeline testing patterns:** Debug mode for interactive testing, data preview, breakpoints, unit testing Spark with small DataFrames, smoke test pipelines for post-deployment validation
* **Error handling in pipelines:** Activity retry policies (count 0-9, interval, backoff multiplier), dependency conditions (Success/Failure/Completion/Skipped), rerun from failure point
* **Parameterization patterns:** Pipeline, dataset, linked service, and global parameters with dynamic content expressions
* **Notebook integration:** Passing parameters to notebooks, returning values, `%run` (shared scope) vs. pipeline activity (separate execution)

### Data Engineering (Basic Knowledge)

* **Delta Lake fundamentals:** Parquet + transaction log, ACID transactions, schema enforcement/evolution, time travel, MERGE for upserts — open format applicable across platforms
* **Partition strategy for files:** Hive-style partitioning, target file sizes (256MB-1GB compressed Parquet), anti-pattern of over-partitioning on high-cardinality columns causing small files problem
* **Apache Spark fundamentals:** `select()`, `filter()`, `groupBy().agg()`, `join()`, lazy evaluation, `repartition()` vs. `coalesce()`, broadcast joins, never `collect()` on large datasets
* **Medallion architecture:** Bronze (raw, append-only) -> Silver (cleansed, deduped, schema-enforced) -> Gold (business aggregations, star schemas) — data flows one direction, each layer adds trust
* **Incremental load patterns:** Watermark pattern (lookup -> copy -> update), CDC via change tables/feeds, Auto Loader for file-based incremental ingestion
* **Data cleansing and deduplication:** `dropDuplicates()`, `ROW_NUMBER()` window function for dedup, `df.na.fill()`/`df.na.drop()` for missing data, quarantine pattern for bad records
* **JSON shredding:** Flattening nested JSON — `explode()` for arrays in Spark, `OPENJSON`/`JSON_VALUE`/`CROSS APPLY` in T-SQL
* **SCD Type 2:** Adding rows with effective dates for slowly changing dimensions — most commonly tested pattern
* **Normalization vs. denormalization:** 3NF for OLTP integrity vs. star schema for analytical query performance
* **Streaming fundamentals:** Output modes (append/complete/update), triggers, checkpoint-based fault tolerance, watermarks for late data handling
* **Windowing functions:** Tumbling (fixed, non-overlapping), Hopping (fixed, overlapping), Sliding (event-driven), Session (variable, gap-based), Snapshot (same timestamp)
* **Stream processing patterns:** foreachBatch for micro-batch upserts, replay from archived data, handling interruptions with checkpoints, at-least-once + idempotent writes
* **Schema drift handling:** Allowing additive schema changes, rescue columns for unexpected fields, merge schema options
* **Data skew identification and resolution:** Symptom (one task 10-100x slower), solutions (AQE skew join, salting, broadcast join)
* **Small file compaction:** OPTIMIZE for bin-packing, ZORDER for data co-location (max 3-4 columns effective), auto-optimize settings
* **Data spill diagnosis:** Memory vs. disk spill in Spark, increasing executor memory, increasing shuffle partitions, OOM on driver vs. executor
* **Encoding and serialization:** UTF-8/UTF-16 handling, Base64 encode/decode, Avro/Parquet/JSON format-specific serialization considerations
* **Spark read modes:** PERMISSIVE (corrupt_record column), DROPMALFORMED, FAILFAST — choosing based on data quality requirements

### Course/Tool Specific Content

* **DP-203 exam profile:** Azure Data Engineer Associate (retired March 31, 2025) — 100 minutes, mixed format (MCQ, multi-select, case studies, drag-and-drop), passing 700/1000, 3 domains
* **DP-203 domain structure:** Design & implement data storage (15-20%), Develop data processing (40-45%), Secure, monitor, optimize (30-35%)
* **DP-700 transition:** Microsoft Fabric replacing Synapse/ADF/Databricks — OneLake, Dataflows Gen2, KQL, Eventstreams, Fabric Data Warehouse; ~40-50% content transfer from DP-203
* **ADLS Gen2:** Hierarchical namespace (HNS), `abfss://` protocol, storage account -> container -> directory -> file hierarchy, HNS upgrade is irreversible
* **Synapse pool types:** Dedicated SQL pools (provisioned DWUs), serverless SQL pools (per-TB scanned), Spark pools (per-node-hour) — billing models and use cases
* **Synapse distributions:** Hash (large fact tables, co-located joins), round-robin (staging/temp, default), replicated (small dimensions <2GB) — need 1M+ rows per partition per distribution
* **ADF / Synapse Pipelines:** Copy Activity (data movement, 90+ connectors), Mapping Data Flows (visual Spark-based transforms), expression language (`@pipeline().parameters`)
* **Azure Stream Analytics:** SQL-like temporal query language, `TIMESTAMP BY` for event-time, embarrassingly parallel processing, Streaming Units (SU) for compute
* **Event Hubs:** Partitioned message log, Throughput Units, Consumer Groups, Event Hubs Capture (auto-archive to ADLS in Avro)
* **PolyBase / COPY INTO:** External Data Source -> External File Format -> External Table -> CTAS pipeline for dedicated pool loading; COPY INTO as simpler alternative
* **Spark Structured Streaming on Azure:** readStream/writeStream with Event Hubs and Kafka formats, cloudFiles (Auto Loader), Delta as streaming sink
* **Synapse Link:** Cosmos DB HTAP — near-real-time analytics without ETL, auto-synced column-store, analytical store TTL
* **Microsoft Purview:** Data lineage from ADF/Synapse (automatic), column-level lineage for mapping data flows, data catalog with PII scanning, business glossary, collections
* **Azure Monitor / Log Analytics:** Diagnostic settings per resource, KQL queries, metric alerts vs. log alerts, dynamic thresholds (ML-based)
* **DMVs for Synapse:** `sys.dm_pdw_exec_requests`, `sys.dm_pdw_request_steps` (ShuffleMove, BroadcastMove), `sys.dm_pdw_nodes_db_partition_stats` for distribution skew
* **Synapse Managed VNet:** Managed private endpoints, data exfiltration protection (connect only to approved targets)
* **Integration Runtime types:** Azure IR (cloud-to-cloud), Self-hosted IR (on-premises/private network), Azure-SSIS IR (lift-and-shift SSIS packages)
* **Trigger types in ADF:** Schedule (many-to-many), Tumbling Window (state tracking, backfill), Event-based (Storage + Event Grid), Custom Event, Manual
* **Databricks on Azure:** PATs vs. Managed Identity vs. OAuth authentication, Unity Catalog (catalog.schema.table namespace), job clusters vs. all-purpose clusters, Auto Loader with cloudFiles
* **CCI (Clustered Columnstore Index):** Default for Synapse analytics, target 1M rows per rowgroup, ordered CCI for segment elimination, heap for staging
* **Synapse result set caching:** `ALTER DATABASE db SET RESULT_SET_CACHING ON`, auto-invalidated on data change or 48 hours
* **Synapse database templates:** Industry-specific pre-built data models, lake databases pointing to ADLS Gen2 files
* **Azure free tier lab strategy:** $200 credit for 30 days, phased spending plan ($35-60 total), cost safety rules, Azurite for local Blob Storage emulation (no HNS/ACL support)
* **Cross-platform service mappings:** S3->ADLS, Glue->ADF, Redshift->Synapse, Kinesis->Event Hubs, EMR->Databricks (for AWS engineers); GCS->ADLS, Dataflow->ADF, BigQuery->Synapse, Pub/Sub->Event Hubs (for GCP engineers)

### Security & Compliance

* **Encryption at rest and in transit:** TDE (AES-256, service-managed or CMK), SSE always-on for storage, TLS 1.2 enforced, Key Vault for CMK management (Get, Wrap Key, Unwrap Key permissions)
* **RBAC vs. POSIX ACLs:** Storage Blob Data Reader/Contributor/Owner for data plane; Contributor role is management-plane only (common exam trap); RBAC checked first, if sufficient ACLs not evaluated
* **POSIX ACL mechanics:** Access ACLs + Default ACLs (inherited by new children, NOT retroactive), Read/Write/Execute permissions, Execute on directories = traverse, max 32 entries per object
* **Row-level and column-level security:** RLS via security predicate functions + security policies (transparent filtering), CLS via column-level GRANT SELECT — both work on dedicated and serverless pools
* **Dynamic Data Masking:** Default/Email/Random/Partial functions, GRANT UNMASK per column, NOT encryption (purely query-result mask, bypassed by db_owner)
* **Private endpoints vs. service endpoints:** Service endpoints (free, Azure backbone, public IP) vs. private endpoints (private IP in VNet, data exfiltration protection, per-endpoint cost)
* **Managed Identity authentication:** Preferred over keys/SAS tokens across all services — ADF to ADLS, Synapse to Key Vault, Databricks to storage
* **Sensitive data in DataFrames:** Column encryption via UDFs (Fernet/Key Vault), hashing (SHA-256), shuffle/cache encryption (`spark.io.encryption.enabled`), encrypt at earliest pipeline point
* **Data retention and immutable storage:** ADLS lifecycle management (Hot->Cool->Archive->Delete), WORM for regulatory compliance, archive tier rehydration (standard: 15h, high priority: <1h)

### Cloud Computing Fundamentals

* **Storage tier lifecycle:** Hot (frequent access) -> Cool (30+ days) -> Archive (180+ days) — cost vs. access-time trade-off pattern applicable across cloud providers
* **Resource scaling patterns:** DWU scaling (scale up before ETL, down/pause after), autoscaling clusters (min/max workers), spot instances (70-90% cheaper), auto-termination
* **Serverless vs. provisioned compute:** Serverless (pennies per query, ad-hoc) vs. dedicated (dollars per hour, consistent workloads) — prefer serverless for infrequent workloads

### Pedagogy & Study Methodology

* **Three study tracks:** Beginner (0-6 points, 150h, 12 weeks), Intermediate (7-12 points, 80-100h, 8 weeks), Advanced (13-18 points, 40-60h, 4 weeks) — based on self-assessment scoring
* **Cross-platform bridging:** AWS->Azure and GCP->Azure service mapping tables for experienced cloud engineers (budget 50-70h)
* **Spaced review schedule:** Weekly review protocol (close notes, self-check questions, flashcard pass, identify gaps), cumulative review at Weeks 2/4/6/8
* **Three depth levels:** Essential (42h, must-know only), Standard (80h, exam-ready), Comprehensive (120h, deep mastery with edge cases)
* **Daily rhythm:** 40% concept study, 40% hands-on labs, 20% practice questions and spaced review
* **Dependency graph:** Visual prerequisite tree showing which topics must be studied before others (e.g., ADLS Gen2 before Delta Lake before MERGE)
* **Top 33 exam-critical topics:** Ranked by question frequency with DP-700 transfer annotations — usable as spaced review flashcard deck
* **Exam strategy tips:** "Least privilege" almost always correct for security, "Managed Identity" almost always best auth choice, "Serverless" usually cheaper for ad-hoc
* **Common exam traps:** Contributor != data access, default ACLs not retroactive, VACUUM breaks time travel, Copy Activity doesn't transform, collect() crashes driver
* **Lab environment phased approach:** Local PySpark (free) -> MS Learn sandboxes (free) -> Databricks Free (free) -> Fabric Trial (60 days) -> Azure Free ($200 credit) — realistic cost $0-75

---

## 3D. Snowflake tri-cert study plan

### Software Engineering / Programming

* **Git integration and version control:** Configuring Git integration within a data platform for source control of SQL, procedures, and pipeline definitions
* **dbt project management:** Using dbt as a software engineering framework for data transformations — project structure, testing, deployment
* **Code deployment pipelines:** CI/CD for database objects — promoting code from dev to production environments
* **Testing and validation frameworks:** Unit testing UDFs, stored procedures, and transformation logic before deployment
* **Stored procedures with error handling:** Writing procedures with transaction management, try/catch, and multi-language support (SQL Scripting, JavaScript, Python via Snowpark)
* **UDF development:** Creating user-defined functions in SQL, Python, Java, and Scala — including secure UDFs and UDTFs that return multiple rows
* **Environment management strategies:** Managing dev/staging/production environments with cloning and role-based isolation

### Data Engineering (Basic Knowledge)

* **Semi-structured data handling:** Loading JSON into VARIANT columns, querying with dot notation, FLATTEN/LATERAL FLATTEN for unnesting nested arrays — applicable across platforms
* **Change Data Capture (CDC):** Using streams to track inserts, updates, and deletes on tables for incremental pipeline processing
* **Schema evolution:** Handling additive schema changes (new columns, type widening) in ingestion and transformation pipelines
* **Data sharing concepts:** Direct shares, data listings, row-level filtering for shares, marketplace/exchange models for data distribution
* **Batch vs. continuous ingestion patterns:** Bulk loading (COPY INTO) vs. continuous pipelines (auto-ingest, streaming) — choosing based on latency requirements
* **Data quality monitoring:** Implementing data quality metric functions on key columns, monitoring freshness and completeness
* **Data lineage and object dependencies:** Tracking read/write operations via access history, understanding upstream/downstream dependencies
* **File format considerations:** Choosing between CSV, JSON, Parquet, Avro, ORC based on compression, schema support, and query patterns
* **Data lifecycle management:** Storage tiering, retention policies, and cost implications of keeping historical data

### Course/Tool Specific Content

* **Snowflake three-layer architecture:** Storage layer, compute layer (virtual warehouses), cloud services layer — separation of storage and compute
* **Snowflake editions:** Standard, Enterprise, Business Critical, Virtual Private Snowflake — feature availability by edition (e.g., search optimization, multi-cluster auto-scaling, masking policies require Enterprise+)
* **Snowsight and Snowflake Notebooks:** Web UI for query execution, data loading, object browsing; Notebooks with SQL/Python cells and Streamlit visualization
* **Virtual warehouse sizing and scaling:** XS through 6XL sizing, multi-cluster warehouses (scale out), auto-suspend/auto-resume, credit consumption model
* **Micro-partitions and clustering:** Automatic micro-partitioning, cluster keys, SYSTEM$CLUSTERING_INFORMATION, automatic vs. manual re-clustering
* **Caching types:** Metadata cache (DDL, row counts), result cache (24hr, invalidated on DML), warehouse cache (SSD on compute nodes) — each with different invalidation rules
* **Snowpipe and Snowpipe Streaming:** Auto-ingest from stages (event-driven) vs. REST API, Snowpipe Streaming vs. Kafka connector comparison
* **Dynamic Tables:** Declarative pipeline definitions — source -> staging -> curated with automatic refresh management
* **Iceberg tables in Snowflake:** External and hybrid table types, Horizon Catalog for federated data access
* **Cortex LLM functions:** PARSE_DOCUMENT, TRANSLATE, CLASSIFY_TEXT, COMPLETE — SQL-callable AI functions with cost management
* **Snowpark:** Python/Java/Scala API for DataFrame-based transformations running on Snowflake compute, including Snowpark-optimized warehouses
* **SnowSQL CLI:** Command-line interface for Snowflake, connection configuration, Apple Silicon compatibility (Rosetta)
* **Snowflake roles:** ACCOUNTADMIN > SECURITYADMIN > SYSADMIN > custom roles hierarchy, privilege inheritance, RBAC model
* **Time Travel and Fail-safe:** DATA_RETENTION_TIME_IN_DAYS (0-90), UNDROP, AT/BEFORE queries, fail-safe period (7 days, non-queryable)
* **Cloning:** Zero-copy cloning of databases, schemas, tables — permission inheritance behavior, use for dev environments
* **Replication and failover:** Cross-region and cross-cloud database replication, failover/failback configuration
* **Snowflake Marketplace:** Browsing and installing third-party data listings, Data Exchange for private sharing
* **Data Clean Rooms:** UI and developer APIs for privacy-preserving data collaboration between organizations
* **Query Profile:** Explain plans, identifying data spilling, cache usage, micro-partition pruning, query history analysis
* **Resource monitors and budgets:** Credit quotas, ACCOUNT_USAGE schema, cost center tagging, Snowsight cost management
* **Materialized views and search optimization:** Precomputed views, search optimization service, query acceleration service
* **COPY INTO (load/unload):** Loading from stages with file format options, unloading to stages with compression — same command, different syntax direction
* **INFER_SCHEMA:** Auto-detecting file structure for staged data before loading
* **Storage integrations:** Connecting to external cloud storage (S3/GCS/Azure) with encryption options (pre-scoped URLs, server-side, client-side)
* **Kafka and Spark connectors:** External integration connectors for streaming and batch data movement
* **Aggregation and projection policies:** Column-level governance policies controlling what aggregate/detail levels different roles can see
* **Object tagging and data classification:** Metadata tags on database objects for governance, automated PII classification
* **SOL-C01 exam:** SnowPro Associate Platform — 65 questions, 85 min, 750/1000 passing, $175, 4 domains (Architecture 35%, Loading/Warehouses 40%, Access 15%, Protection 10%)
* **COF-C02 exam:** SnowPro Core — 100 questions, 115 min, 750/1000 passing, $175, 6 domains (Architecture 24%, Security 18%, Transformations 18%, Performance 16%, Loading 12%, Protection 12%)
* **DEA-C02 exam:** SnowPro Advanced Data Engineer — 115 min, 750/1000 passing, $375, requires active Core cert, 5 domains (Data Movement 28%, Transformation 25%, Performance 19%, Storage 14%, Governance 14%)
* **Snowflake trial account:** Enterprise edition recommended, $400 credit for 30 days, credit conservation tips
* **Cross-certification topic overlap:** Detailed reuse percentages — Platform->Core ~85%, Core->DEA 50-75% varying by domain

### Security & Compliance

* **Network security policies:** IP whitelisting, network policy configuration for access control at the account level
* **Authentication methods:** MFA enforcement, federated authentication (SSO), key pair authentication — defense-in-depth for identity
* **Row-level and column-level security:** Row access policies for transparent row filtering, column masking with Dynamic Data Masking
* **Data governance framework:** Object tagging, data classification (PII detection), access history tracking, secure views/functions
* **Data encryption:** End-to-end encryption for data at rest and in transit within the platform

### Pedagogy & Study Methodology

* **Three-phase progressive study path:** Platform (45-60h) -> Core (70-90h) -> Data Engineer (100-130h), totaling 215-280 hours over 22-29 weeks
* **Suggested weekly rhythm:** 10-12h/week across 6 days — concept study, hands-on labs, AI tutor quizzes, review, longer lab sessions
* **Readiness gates:** 80% on practice exams for Platform/Core, 85% for DEA — with specific self-assessment checklists per phase
* **Spaced repetition schedule:** End-of-domain quizzes, weekly review of all prior domains, cross-phase bridge reviews, 30 min/week prior-phase review
* **Exam-taking strategies:** Time management per question (78-120 sec), two-pass approach (confident first, flagged second), never leave blanks
* **Multi-select question tactics:** No partial credit — count selections carefully, eliminate weakest when uncertain
* **Snowflake distractor patterns:** Edition confusion, COPY INTO direction, cache type confusion, role confusion, plausible-but-incomplete answers
* **Scenario-based question strategy:** Read twice, identify constraint (cost/latency/compliance), eliminate violations, prefer simplest solution
* **Fast-track guidance:** Skip percentages for experienced users transitioning between phases, net-new topic identification
* **Retake strategy:** 14-day mandatory wait, re-study weak domains, score 85%+ before rescheduling
* **AI tutor integration:** Using certification-tutor-prompt.xml for `/quiz`, `/exam`, `/progress`, session state export/import across study sessions
* **Priority labels:** HIGH-YIELD (frequently tested) and DEEP-DIVE (conceptually difficult) tags for time-constrained study
* **Cost planning:** Total realistic cost $825-$1,360 including exams, practice tests, potential Snowflake credits, and retakes

---

## 3E. LFCA tutor implementation plan

### Software Engineering / Programming

* **XML prompt architecture:** Core + on-demand section design pattern for managing complexity and token budgets in structured documents
* **Token budget management:** Systematic allocation of computational resources across components with hard limits and measurement gates
* **Natural language command parsing:** Designing command interfaces that accept both structured commands and free-form natural language equivalents via alias mapping
* **Statelessness strategy:** Designing applications that operate within stateless runtime constraints, using explicit export/import protocols for cross-session continuity
* **Cooperative contract pattern:** Designing systems that guide user behavior through social contracts rather than enforcement mechanisms
* **MVP-first phased delivery:** Structuring a project into MVP, Enhancement, and Polish phases with validation gates between each

### Data Engineering (Basic Knowledge)

* **Exam profile data extraction and structuring:** Parsing unstructured text into structured data (cert name, vendor, format, domains with weights, topics)
* **Format-adaptive content generation:** Distributing output proportionally to weighted domain data (e.g., 30% weight domain receives ~30% of questions)

### Course/Tool Specific Content

* **LFCA exam profile:** Linux Foundation Certified IT Associate — online proctored, MCQ-only, 90 minutes, no prerequisites, beginner level, $250, 2-year validity
* **LFCA domain structure:** 6 domains — Linux Fundamentals (16%), System Administration (30%), Cloud Computing (18%), Security (14%), DevOps (12%), IT Project Management (10%)
* **LFCA sub-topics:** Linux OS, command line, networking, troubleshooting, disaster recovery, cloud best practices, containers, Git, OSS licensing, software architecture
* **LFCA free resources:** Introduction to Linux, DevOps/SRE, Cloud Infrastructure Technologies, Beginner's Guide to OSS Development (all free courses from Linux Foundation)
* **Certification tutor prompt design:** XML-based prompt file (`certification-tutor-prompt.xml`) that turns an LLM into a certification study tutor with auto-configuration from exam guides
* **Bootstrap paste-first design:** Exam guide intake prioritizing paste over URL fetch, with hard-gate confirmation before proceeding
* **Question engine format adaptation:** Suppressing question types the actual exam does not use (e.g., no labs for MCQ-only exams like LFCA)
* **Tutor command set:** `/quiz`, `/explain`, `/exam`, `/progress`, `/plan`, `/help` — reduced from 11 to 6 commands

### Pedagogy & Study Methodology

* **Two-phase teaching protocol:** Phase A (direct instruction for new concepts) and Phase B (Socratic deepening for review), with an escape valve for stuck learners after 2 wrong answers
* **Three-tier difficulty tracking:** Foundation (recall) -> Application (scenarios) -> Analysis (trade-offs), tracked per domain with 4/5 escalation and 2/5 de-escalation thresholds on rolling 5-question windows
* **Frustration detection:** 3+ consecutive wrong answers triggers difficulty drop, mode switch to direct instruction, and offer to change topics
* **Cross-experience bridging:** Optional technique activated only if learner reports prior experience (e.g., Windows background studying Linux)
* **Prerequisite check for beginners:** 3 quick foundational questions during onboarding; if all wrong, tutor includes foundational explanations throughout
* **Level-adaptive output formats:** Beginner (short, plain-language), Standard (structured with key points and gotchas), Advanced (trade-offs and exam traps)
* **Review queue (lightweight spaced repetition):** Incorrectly answered concepts queued for re-testing in different formats every 10-15 questions; capped at 10 items; honest about not being true SRS
* **Interleaving:** Cross-domain questions after covering 2+ domains to strengthen transfer learning
* **Session state block:** Compact JSON exported at session end for cross-session continuity (<400 tokens), including per-domain scores, weak topics, and review queue
* **Exam simulation mode:** Cooperative contract framing with honor-system timing, withheld explanations during exam, comprehensive review phase after
* **Study plan generation:** Time allocation proportional to domain weights, +25% for weak areas, final 20% reserved for review, hands-on practice adapted to exam type
* **Onboarding flow:** Welcome -> exam input -> bootstrap -> learner profile -> prerequisite check -> begin with highest-weight domain
* **Adversarial analysis resolution:** Systematic identification and resolution of 24 design flaws across pedagogy, architecture, and testing dimensions

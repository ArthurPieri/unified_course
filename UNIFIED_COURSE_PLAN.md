# Unified Data Engineering Course Plan

---

## I. Course Goal

By the end of this course, the learner will design, build, deploy, monitor, and troubleshoot production-grade data pipelines spanning ingestion, transformation, storage, orchestration, governance, and serving — first using vendor-agnostic open-source tools, then implementing equivalent solutions on one or more cloud platforms (AWS, Azure, or Snowflake). The learner will be prepared to pass at least one industry-recognized data engineering certification and enter the job market as a strong junior to early mid-level data engineer.

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
8. **Theory grounded by practice.** Extended theory-only phases are avoided. Conceptual content is interleaved with hands-on tool usage to maintain motivation and reinforce learning through doing.

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
- Hardware and environment verification: 16GB+ RAM requirement for Phase 3+, cloud fallback options (GitHub Codespaces, Gitpod), light profile for 8GB machines

**Practical exercises:**
- Self-assessment quiz (45 min): SQL window functions, Python generators, Git branching, networking basics (ports, HTTP)
- Map 5 real job postings to specific skills taught in this course
- Choose a target certification path and write a 1-paragraph learning goal
- Hardware readiness check: verify available RAM, Docker Desktop allocation (12GB+ recommended), verify Docker and Docker Compose installed

**Deliverables:** Completed self-assessment with gap identification. Written learning goal and target certification.

**Estimated duration:** 5-8 hours

**Exit criteria:** Self-assessment score >= 70%. Hardware verified (16GB+ RAM confirmed OR cloud development environment configured). Learners below threshold directed to prerequisite resources before Phase 1.

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

**Estimated duration:** 60-75 hours (6-7 weeks at 10-12h/week)

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
- Deploy and query an object storage layer as first lakehouse contact

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

*Streaming Concepts (6h):*
- Event streaming fundamentals: events vs. messages, delivery semantics (at-least-once, at-most-once, exactly-once)
- Apache Kafka architecture (conceptual): topics, partitions, consumer groups, offsets
- Windowing: tumbling, hopping, sliding, session windows
- Watermarks, checkpoints, output modes (append, complete, update)
- When streaming vs. batch: decision framework with real-world examples

*Hands-On Bridge: First Contact with the Lakehouse (6h):*
- Deploy MinIO via Docker Compose (storage profile)
- Upload sample Parquet files, explore via mc CLI
- Install DuckDB, query Parquet files locally and from MinIO
- Compare row-store (PostgreSQL) vs. columnar (Parquet/DuckDB) query performance with real data
- Lab: this directly bridges into Phase 3 — the MinIO instance persists

**Practical exercises:**
- Design a star schema for an e-commerce dataset; implement in PostgreSQL
- Implement SCD Type 2 with effective dates
- Classify columns in a sample dataset by PII/Sensitive/Internal/Public
- Write a data contract (YAML) for a staging model
- Compare query performance on row-store vs. columnar formats (PostgreSQL vs. Parquet via DuckDB)
- Deploy MinIO and load Parquet; query with DuckDB to compare columnar vs. row-store performance

**Deliverables:**
- Star schema ERD + PostgreSQL implementation with SCD Type 2
- Written data quality assessment of a provided messy dataset
- Data modeling decision document: for a given scenario, choose between normalized (3NF) and dimensional (star) modeling and justify the trade-offs
- MinIO stack running with sample Parquet queryable via DuckDB (stack persists into Phase 3)

**Estimated duration:** 50-65 hours (5-6 weeks at 10-12h/week)

**Exit criteria:** 15-question quiz (data modeling, pipeline paradigms, distributed systems, data quality, file formats). Pass threshold: 70%. Plus: star schema implementation reviewed and accepted. MinIO + DuckDB lab produces a row-store-vs-columnar benchmark with documented numbers.

---

### Phase 3: Core Tools, Workflows, and Applied Practice

**Why now:** Concepts without hands-on practice create false confidence. This phase builds the full open-source lakehouse stack piece by piece, giving the learner concrete experience with every layer of a modern data platform before encountering vendor abstractions.

**Prerequisites:** Phase 2 exit criteria met.

**Learning objectives:**
- Deploy and operate a local lakehouse: MinIO (object storage) + Iceberg (table format) + Hive Metastore (catalog) + Trino (query engine) + dlt (ingestion) + dbt (transformation) + Dagster (orchestration)
- Build complete ELT pipelines from ingestion through serving
- Write and test dbt models with contracts, tests, and documentation
- Orchestrate multi-step pipelines with Dagster
- Write PySpark transformations and understand the Spark execution model (lazy evaluation, shuffles, partitions)
- Use DuckDB for local exploration and CI testing

**Key topics:**

*Object Storage — MinIO (8h):*
- S3-compatible object storage: buckets, objects, mc CLI, web console
- Credential management via .env
- Docker Compose profile: `storage`
- Connection patterns: path-style access, endpoint configuration
- Lab: create lakehouse bucket, upload sample Parquet, verify access
- Note: *For machines with 8GB RAM, a light Docker Compose profile is available that runs MinIO + Trino + PostgreSQL using Iceberg's JDBC catalog (no HMS). This covers ~80% of Phase 3 objectives. HMS can be added when upgrading hardware or using a cloud development environment.*

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

*Batch Processing — PySpark (12h):*
- Why Spark matters: large-scale batch ETL, DataFrame transformations, the dominant processing engine in AWS/Azure vendor branches
- **Deployment (provided, not invented):** use the course-provided Spark Docker image with pinned, version-matched jars — Spark 3.5.x + iceberg-spark-runtime-3.5_2.12:1.5.x + hadoop-aws-3.3.4 + aws-java-sdk-bundle-1.12.x. Configured as a Docker Compose profile extending the Phase 2 MinIO stack. Learners do NOT assemble their own jar set.
- **Known gotchas (documented upfront, not rediscovered):** Scala version mismatch (2.12 vs 2.13) silently breaks Iceberg writes · Hadoop-AWS version drift causes `NoClassDefFoundError` at runtime · path-style access required for MinIO (`fs.s3a.path.style.access=true`) · driver/executor memory defaults too low for NYC Taxi — adjust in `spark-defaults.conf`. A troubleshooting playbook lists symptoms and fixes.
- PySpark fundamentals: SparkSession, DataFrame API (select, filter, groupBy, agg, join), lazy evaluation (transformations vs. actions)
- Reading from MinIO: Parquet and Iceberg via Spark-Iceberg connector
- Shuffles: what triggers them (groupBy, join, repartition), why they're expensive
- repartition() vs. coalesce(), broadcast joins for small tables
- Writing results back to Iceberg tables
- Comparing approaches: same analytical query in Trino SQL vs. PySpark vs. DuckDB — when each shines
- Lab: process NYC Taxi data with PySpark — read from MinIO, transform, write to Iceberg, observe Spark UI (stages, tasks, shuffles)

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
- PySpark notebook demonstrating DataFrame transforms on NYC Taxi data with Spark UI analysis
- All code in a Git repo with branching, pre-commit hooks, and CI tests (DuckDB-based)

**Estimated duration:** 100-140 hours (9-13 weeks at 10-12h/week). Upper bound reflects that learners running on 16GB RAM often hit Spark OOM on the NYC Taxi lab and spend real time on memory tuning.

**Exit criteria:** 2-hour integration exercise: from a fresh Docker Compose stack, complete end-to-end flow (start services -> create Iceberg table -> dbt transform -> Trino query -> verify results). All dbt tests pass. PySpark notebook demonstrates DataFrame transforms with Spark UI analysis. Can explain the data flow at every step.

---

### Phase 4: Intermediate Domain Specializations

**Why now:** With a working lakehouse and practical pipeline experience, the learner is ready to go deeper into the dimensions that separate junior from mid-level: streaming, CDC, security, governance, and performance.

**Prerequisites:** Phase 3 exit criteria met.

**Learning objectives:**
- Implement change data capture pipelines
- Produce and consume Kafka messages; implement basic windowed aggregations
- Handle semi-structured data (JSON shredding, FLATTEN, schema drift)
- Apply security and governance patterns to pipelines (masking, RLS, audit trails)
- Diagnose and resolve performance issues (data skew, spill, small files)
- Implement data quality monitoring and observability

**Key topics:**

*Change Data Capture & Streaming Fundamentals (16h):*
- CDC concepts: WAL-based replication, binlog capture, change tables
- Debezium: PostgreSQL WAL -> Debezium -> Kafka -> dlt -> Iceberg MERGE INTO
- Incremental load refinement: watermark pattern, append-only, merge with primary key
- Lab: real CDC pipeline from PostgreSQL through to Iceberg Silver layer
- Kafka hands-on: produce messages to a Kafka topic with a Python producer (kafka-python)
- Consume messages with a basic Python consumer, observe partition assignment and offset management
- Partition behavior: produce keyed messages, observe partition distribution
- Simple windowed aggregation: consume Kafka messages, compute tumbling-window counts using DuckDB on captured events
- Delivery semantics in practice: demonstrate at-least-once behavior with consumer restart
- Lab: extend CDC pipeline — add a Python Kafka producer simulating events, consume and aggregate with windowed counts, compare with the Debezium CDC flow

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
- Spark troubleshooting (building on Phase 3 PySpark experience): check order (error -> executors -> stages -> driver logs)
- Query optimization: predicate pushdown, partition pruning, dynamic filtering, caching
- Benchmarking: baseline (3 runs, discard cold), one variable at a time, document results
- Lab: diagnose and fix a slow query (provided broken pipeline with skew, small files, missing partitioning)
- **Data scale note:** skew, spill, and AQE are only observable on genuinely large inputs. A 16GB laptop running NYC Taxi will not reproduce these symptoms. For this lab, learners use one of: (a) the course-provided synthetic data generator that inflates the taxi dataset to 50–100GB with configurable skew, or (b) GitHub Codespaces with a larger machine type (or any cloud VM ≥ 32GB) for the duration of the performance lab only.
- **Deliverable reality check:** the performance report must include at least one Spark UI screenshot showing an actual skewed stage or spill event — not just the pre-built skew example from course materials.

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
- Kafka producer/consumer pipeline with windowed aggregation
- Monitoring dashboard with alerting for pipeline health

**Estimated duration:** 60-75 hours (5-7 weeks at 10-12h/week)

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
- Write an Airflow DAG and compare asset-centric (Dagster) vs. task-centric (Airflow) orchestration
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

*Cloud Identity and Access Primer (5h):*
- Why this module exists: every vendor branch (AWS, Azure, Snowflake) requires fluency with policy documents, role assumption, and least-privilege reasoning. Treating IAM as "learn it when you get there" repeatedly blocks learners in week 1 of vendor branches. This primer front-loads the cross-vendor mental model.
- IAM core model: principals, actions, resources, conditions — the four quadrants every cloud policy shares
- Policy document anatomy: JSON structure, Effect/Action/Resource/Condition, explicit deny vs. absence of allow
- Role assumption and trust policies: why a role has two policies (trust + permission), STS and temporary credentials
- Least-privilege reasoning: starting from deny-all and adding minimum permissions, common overly-broad patterns to avoid
- Hands-on with LocalStack: run LocalStack in Docker, create an S3 bucket, write a restrictive bucket policy, create an IAM role with an inline policy, assume the role via awslocal CLI, verify that denied actions actually fail
- Lab: given a scenario ("a Lambda should read from bucket-A and write to bucket-B but not delete"), write the minimum IAM policy, test with LocalStack, then intentionally break it (add a wildcard) and explain the security impact
- Mapping across vendors: how the same mental model translates to Azure RBAC (role assignments, scope inheritance) and Snowflake RBAC (role hierarchy, GRANT/REVOKE) — one-page comparison sheet

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

*Airflow Bridge (6h):*
- Why Airflow matters: ~70% of job postings list Airflow; AWS MWAA is managed Airflow; understanding both paradigms is essential for employability
- Deploy Airflow via Docker Compose (webserver + scheduler + PostgreSQL backend)
- Core concepts: DAGs, operators (PythonOperator, BashOperator), sensors, connections, XComs
- Write one DAG: replicate the dbt transformation pipeline from Phase 3 (BashOperator running dbt commands)
- Side-by-side comparison: Dagster asset-centric vs. Airflow task-centric — same pipeline, different paradigms
- When to choose which: Dagster for greenfield, Airflow for team familiarity and managed services
- Lab: deploy Airflow, write and trigger a DAG, compare with equivalent Dagster pipeline

**Deliverables:**
- CI/CD pipeline for the lakehouse project (GitHub Actions)
- Trino deployed on local Kubernetes
- Cost estimation spreadsheet for 3 scale scenarios
- FastAPI data-serving endpoint
- Airflow DAG replicating the dbt pipeline, with written comparison to Dagster approach
- Architecture decision record

**Estimated duration:** 50-65 hours (5-6 weeks at 10-12h/week)

**Exit criteria:** CI/CD pipeline runs green. Kubernetes deployment healthy. Can present a cost estimate and architectural rationale for the full stack.

---

### Phase 6: Vendor-Agnostic Capstone

**Why now:** Before branching into vendor specializations, the learner consolidates all skills into a single production-grade project that demonstrates employability. **This phase is strongly recommended for portfolio-building and skill integration, but certification-track learners who meet the fast-track criteria may proceed directly to vendor branches.**

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

**Estimated duration:** 50-70 hours (4-6 weeks)

> **Fast-track alternative:** Learners may skip the capstone and proceed to vendor branches only if they can produce the following self-diagnostic deliverables from their existing Phase 3–5 work. Each item is intentionally concrete so it cannot be ticked off cosmetically:
>
> 1. **Architecture walkthrough video (15–20 min):** screen-recorded walkthrough of the learner's Phase 3 lakehouse running end-to-end (ingestion → Silver → Gold → dashboard), explaining each component's role, why it was chosen, and one failure mode observed during development.
> 2. **CDC runbook (1–2 pages):** written runbook for the Phase 4 CDC pipeline including: topology diagram, known failure modes, recovery procedure for consumer lag, and how to verify Silver-layer consistency after a Debezium connector restart.
> 3. **Security decision log:** a markdown document listing every PII column in the pipeline, the masking/RLS decision made for each, the RBAC role that can see unmasked data, and the audit-log query that proves access was recorded.
> 4. **Performance report:** the Phase 4 performance lab writeup must include *quantified* before/after numbers (wall-clock, shuffle bytes, Spark UI screenshots) — not qualitative claims.
> 5. **CI/CD evidence:** link to a green CI run on the learner's repo showing lint + dbt test + integration test stages, plus the deployment manifest.
> 6. **Observability evidence:** screenshot of the Phase 4 monitoring dashboard showing at least one alert rule that fired in testing, with the runbook link the alert points to.
>
> A mentor (or self-review with a rubric checklist) verifies each item exists and is non-trivial. If all six are produced, the learner may proceed to vendor branches and complete the capstone in parallel or after. Learners who cannot produce these artifacts from existing Phase 3–5 work should complete Phase 6 — the gap is the signal that integration competence is missing.

**Exit criteria:** Completed project reviewed against rubric. Deployed, documented, and pushed to a public Git repository as a portfolio piece.

---

## VI. Vendor-Specific Branches

> **When to start:** After Phase 5 completion with Phase 6 capstone complete OR fast-track rubric met. Experienced learners with equivalent Phase 4+ competence may enter earlier with instructor approval.

---

### Branch A: AWS Data Engineering

**Assumes common core:** Phases 0-5 complete with Phase 6 capstone **OR** fast-track rubric met (data modeling, ETL/ELT patterns, Spark fundamentals, streaming concepts, Medallion architecture, security principles, orchestration, monitoring).

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

**Estimated duration:** 100-130 hours (9-12 weeks at 10-12h/week)

---

### Branch B: Azure / Microsoft Fabric Data Engineering

**Assumes common core:** Phases 0-5 complete with Phase 6 capstone **OR** fast-track rubric met.

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

**Estimated duration:** 110-140 hours (10-13 weeks at 10-12h/week)

---

### Branch C: Snowflake Data Engineering

**Assumes common core:** Phases 0-5 complete with Phase 6 capstone **OR** fast-track rubric met.

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

**Estimated duration:** 85-110 hours for Platform + Core, additional 65-90 hours for DE Advanced (total 150-200 hours over 15-22 weeks)

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

> **Proficiency legend (self-paced course calibration):** *Awareness* = can explain concept · *Working* = can use the tool on routine tasks with docs · *Working+* = can use the tool on non-routine tasks, diagnose common failures, and make design choices. The course does not claim to produce *Advanced* or *Expert* practitioners — those labels reflect years of production experience, not curriculum completion.

| Skill / Domain | After Phase 1 | After Phase 3 | After Phase 6 | After Vendor Branch |
|---|---|---|---|---|
| **SQL** | Working (window functions, CTEs, EXPLAIN) | Working+ (optimization, complex joins, DDL) | Working+ (cross-engine, basic performance tuning) | Working+ / vendor dialect |
| **Python** | Working (project structure, testing) | Working+ (pipelines, transforms, testing) | Working+ (API serving, CI integration) | + vendor SDK familiarity |
| **Linux / CLI** | Working (navigation, scripting, processes) | Working | Working | Working |
| **Docker / Containers** | Working (Compose, profiles, health checks) | Working+ (multi-service stacks) | Working+ with Kubernetes basics | + managed container services |
| **Data Modeling** | None | Working (star schema, SCD) | Working+ (multi-domain, governance-aware) | + vendor-specific optimization |
| **ETL / ELT Pipelines** | None | Working (dlt + dbt + Dagster + PySpark) | Working+ (CDC, monitoring, CI/CD) | + vendor service implementation |
| **Spark/PySpark** | None | Working (DataFrames, shuffles, Iceberg I/O) | Applied (performance tuning, Spark UI) | + Glue/EMR (AWS), Synapse Spark/Databricks (Azure), Snowpark (Snowflake) |
| **Streaming** | Conceptual | Conceptual + Kafka literacy | Applied (CDC, Kafka producer/consumer, windowed aggregation) | + vendor streaming services |
| **Data Governance** | None | Awareness | Working (masking, RLS, audit, contracts) | + vendor governance tools |
| **Security** | Secret management basics | + encryption, RBAC concepts | Working (PII masking, multi-tenant, IAM primer) | + vendor IAM, CMK, endpoints |
| **Performance Tuning** | SQL EXPLAIN | + partitioning, file sizing | Working (skew, spill, compaction, benchmarking) | + vendor-specific optimization |
| **Cloud Architecture** | None | Conceptual | Working (ADRs, cost, scaling at design level) | Implemented on target platform |
| **Orchestration** | None | Working (Dagster) | Working (Dagster + Airflow basics) | + MWAA (AWS) or ADF (Azure) or Tasks (Snowflake) |
| **Observability** | None | Basic (Dagster UI) | Working (Prometheus, alerting, runbooks) | + vendor monitoring stack |
| **Certification Readiness** | LFCA eligible | None | None | Target cert exam-ready |

---

## IX. Milestones and Assessments

### Checkpoint Quizzes (30 min each, 70% pass threshold)

| Checkpoint | After | Topics |
|---|---|---|
| Q0 | Phase 0 | Self-assessment: SQL, Python, Git, networking |
| Q1 | Phase 1 | Docker Compose, bash scripting, SQL window functions, Python project structure |
| Q2 | Phase 2 | Data modeling, ETL/ELT, distributed systems, data quality, file formats |
| Q3 | Phase 3 | Iceberg, Trino, dlt, dbt, Dagster, PySpark basics — tool mechanics and integration |
| Q4 | Phase 4 | CDC, Kafka producer/consumer, security patterns, performance diagnosis, observability |
| Q5 | Phase 5 | CI/CD, Kubernetes, Airflow DAG basics, cloud concepts, FinOps, architecture design |

### Hands-On Labs (graded by rubric)

| Lab | Phase | Deliverable |
|---|---|---|
| L1 | 1 | Docker Compose + PostgreSQL + health-check script |
| L2 | 2 | Star schema + SCD Type 2 in PostgreSQL |
| L3a | 3 | MinIO + Iceberg + HMS + Trino stack running |
| L3b | 3 | dlt ingestion pipeline (incremental) |
| L3c | 3 | dbt models with contracts + tests + docs |
| L3d | 3 | Dagster orchestration of full pipeline |
| L3e | 3 | PySpark notebook: NYC Taxi transforms with Spark UI analysis |
| L4a | 4 | CDC pipeline (Debezium -> Kafka -> Iceberg) |
| L4b | 4 | PII masking pipeline with audit trail |
| L4c | 4 | Performance diagnosis and optimization report |
| L4d | 4 | Kafka producer/consumer with windowed aggregation |
| L5a | 5 | CI/CD pipeline + Kubernetes deployment |
| L5b | 5 | Airflow DAG + Dagster comparison writeup |

### Portfolio Projects

| Project | Phase | Scope |
|---|---|---|
| P1 | Phase 6 | Vendor-agnostic capstone: full lakehouse from scratch **(recommended, see fast-track alternative)** |
| P2 | Vendor branch | Platform-specific capstone: rebuild on target vendor |

### Mock Certification Checkpoints

| Mock | When | Format | Pass Threshold |
|---|---|---|---|
| LFCA mock | End of Phase 1 | 30 MCQ, 45 min | 80% |
| Vendor mock 1 | Mid vendor branch | 30 questions, domain-weighted | 75% |
| Vendor mock 2 | End vendor branch | Full-length simulation | 80% (85% for advanced) |

---

## X. Final Recommended Sequence

**Standard track (recommended):**

1. **Phase 0** — Orientation, self-assessment, hardware check (1 week)
2. **Phase 1** — Linux, networking, Python, Docker, SQL, Git (6-7 weeks)
3. *(Optional)* LFCA certification attempt
4. **Phase 2** — Data modeling, ETL/ELT, distributed systems, data quality, first lakehouse contact (5-6 weeks)
5. **Phase 3** — Build the lakehouse: MinIO, Iceberg, HMS, Trino, PySpark, dlt, dbt, Dagster, Metabase (9-13 weeks)
6. **Phase 4** — CDC, Kafka fundamentals, semi-structured data, security, performance, observability (5-7 weeks)
7. **Phase 5** — CI/CD, Kubernetes, Airflow bridge, cloud concepts, FinOps, data serving, IAM primer (5-6 weeks)
8. **Phase 6** — Vendor-agnostic capstone project (4-6 weeks, recommended)
9. **Choose vendor branch:**
   - **9a. AWS** — S3, Glue, Kinesis, Athena, Redshift, Step Functions, IAM/KMS (9-12 weeks) -> DEA-C01 cert
   - **9b. Azure** — ADLS, ADF, Synapse, Databricks, Event Hubs, Purview, Fabric (10-13 weeks) -> DP-700 cert
   - **9c. Snowflake** — Architecture, warehouses, Snowpipe, Snowpark, governance (15-22 weeks) -> SOL-C01 -> COF-C02 -> DEA-C02 certs
10. **Certification preparation** — Practice exams, weak-area remediation, exam scheduling (2-4 weeks)

**Standard timeline (one vendor path, with capstone):** ~42-64 weeks at 10-12h/week (~475-628 hours total, plus 2-4 weeks certification prep)

**Fast-track timeline (skip capstone):** ~36-56 weeks at 10-12h/week (~425-558 hours total, plus 2-4 weeks certification prep)

---

## XI. Assumptions

- The learner has access to a machine with 16GB RAM (recommended) or 8GB RAM with the light Docker Compose profile. Learners with constrained hardware can use GitHub Codespaces (free tier: 60h/month) or Gitpod as a cloud development environment. Hardware requirements are verified in Phase 0 before any commitment.
- The learner can dedicate 10-12 hours per week consistently. Faster paces are possible with more hours; the sequencing does not change.
- Cloud vendor accounts (AWS Free Tier, Azure $200 credit, Snowflake 30-day trial) will be used for vendor branches. Lab costs are estimated at $0-100 per branch.
- The LFCA certification is included as an optional early milestone based on its domain coverage (Linux, networking, cloud, security, DevOps), not because the source documents contain a full LFCA curriculum. The learner will need supplementary exam-specific study.
- DP-203 content is treated as learning material only (exam retired March 2025). The certification target for Azure is DP-700 (Fabric).
- Snowflake's three-certification path (Platform -> Core -> DE) is presented as a single branch because the certifications are sequential prerequisites; the learner may stop after any level.
- Where source documents reference different tools for the same function (e.g., Dagster vs. Airflow for orchestration), the curriculum teaches the primary tool hands-on and the alternatives conceptually, with enough transferable knowledge to switch.
- Hour estimates include realistic buffer for debugging, configuration issues, and tool integration challenges. The ranges reflect variance between learners with stronger vs. weaker prerequisites. A learner consistently at the top of the range should revisit prerequisite gaps rather than pushing through.

---

## XII. Outcome

A learner who completes the shared core and one vendor branch will enter the job market as a **strong junior to early mid-level data engineer** with unusually broad architectural knowledge, hands-on tool proficiency across the modern data stack, and at least one industry certification. They can design data models, build and orchestrate production pipelines, implement security and governance, diagnose performance issues, and deploy on their chosen cloud platform. The breadth of the open-source core — covering storage, compute, orchestration, transformation, and monitoring — gives them a faster path to mid-level than typical bootcamp graduates who know only one vendor's tools.

---

## Appendix A: Reference Material

> *The following topics are important context for a data engineer's career but are not gated prerequisites for Phase 3. Study them as reference material throughout the course, revisiting after hands-on tool experience for deeper understanding.*

### Architecture Landscape (8h reference)

- Data lakehouse: open table formats + decoupled compute + object storage
- Medallion architecture: Bronze (raw) -> Silver (cleansed) -> Gold (business-ready)
- Data Mesh: domain-oriented decentralized ownership (for large orgs)
- Data Fabric: metadata-driven integration
- Hadoop ecosystem legacy and why it matters for interviews
- Modern architecture decision framework: when to use what

### Database & Engine Landscape (6h reference)

- Relational: PostgreSQL, MySQL, Oracle, SQL Server, Aurora — dialect differences, DE interaction
- NoSQL families: Document (MongoDB), Column-family (Cassandra), Graph (Neo4j), Key-Value (Redis)
- Polyglot persistence: modern apps use multiple databases, DEs ingest from all
- Processing engines: Trino (interactive SQL), Spark (large-scale ETL/ML), Flink (real-time streaming)
- Managed warehouses: Snowflake, BigQuery, Redshift — zero-ops alternatives to open stack

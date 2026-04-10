# Official Documentation Index

Canonical URLs for every tool, spec, and certification program used in the course. Deduplicated; modules link into this file instead of repeating URLs. Every entry is a primary source (vendor docs, spec, or official cert page) — no blog posts, no tutorials, no third-party commentary.

Format: `- [Name](url) — one-line why it matters`.

---

## Programming languages and runtimes

- [Python 3 documentation](https://docs.python.org/3/) — language reference, stdlib
- [Python venv](https://docs.python.org/3/library/venv.html) — stdlib virtual environments
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) — stdlib value objects
- [PEP 518 — pyproject.toml](https://peps.python.org/pep-0518/) — build system requirements
- [PEP 621 — project metadata](https://peps.python.org/pep-0621/) — `[project]` table schema
- [Python Packaging User Guide — src vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [uv documentation](https://docs.astral.sh/uv/) — fast Python package manager used in course examples
- [uv — projects](https://docs.astral.sh/uv/concepts/projects/)
- [uv — locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv — Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [pip documentation](https://pip.pypa.io/en/stable/) — alternative installer
- [Poetry documentation](https://python-poetry.org/docs/) — alternative project tool

## Code quality and testing

- [Ruff configuration](https://docs.astral.sh/ruff/configuration/) — linter/formatter
- [Ruff rules](https://docs.astral.sh/ruff/rules/)
- [Ruff formatter](https://docs.astral.sh/ruff/formatter/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/) — static type checker
- [mypy configuration file](https://mypy.readthedocs.io/en/stable/config_file.html)
- [pre-commit](https://pre-commit.com/) — git hook framework
- [pre-commit quick start](https://pre-commit.com/#quick-start)
- [pytest documentation](https://docs.pytest.org/en/stable/) — Python testing framework
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html)

## Linux and shell

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — authoritative bash language reference
- [Bash pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html) — pipefail and redirection
- [GNU coreutils manual](https://www.gnu.org/software/coreutils/manual/) — ls, cp, chmod, cut, sort
- [GNU grep manual](https://www.gnu.org/software/grep/manual/grep.html)
- [GNU sed manual](https://www.gnu.org/software/sed/manual/sed.html)
- [GNU awk (gawk) manual](https://www.gnu.org/software/gawk/manual/gawk.html)
- [Linux man-pages project](https://man7.org/linux/man-pages/) — canonical man pages
- [jq manual](https://jqlang.github.io/jq/manual/) — JSON query/transform language

## Networking specs and references

- [IANA Service Name and Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) — authoritative port list
- [RFC 1918 — Private IPv4 address allocation](https://datatracker.ietf.org/doc/html/rfc1918)
- [RFC 1034 — DNS concepts](https://datatracker.ietf.org/doc/html/rfc1034)
- [RFC 1035 — DNS implementation](https://datatracker.ietf.org/doc/html/rfc1035)
- [RFC 6335 — IANA procedures for port numbers](https://datatracker.ietf.org/doc/html/rfc6335)
- [RFC 768 — UDP](https://datatracker.ietf.org/doc/html/rfc768)
- [RFC 9293 — TCP (current spec)](https://datatracker.ietf.org/doc/html/rfc9293)
- [RFC 9110 — HTTP semantics](https://datatracker.ietf.org/doc/html/rfc9110)
- [RFC 9112 — HTTP/1.1](https://datatracker.ietf.org/doc/html/rfc9112)
- [RFC 8446 — TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)

## Containers, Compose, Kubernetes

- [Docker documentation](https://docs.docker.com/) — Dockerfile, build, run
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — all instructions, CMD vs ENTRYPOINT
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker storage — volumes](https://docs.docker.com/storage/volumes/)
- [Docker networking overview](https://docs.docker.com/network/)
- [Docker Compose](https://docs.docker.com/compose/) — multi-container applications
- [Compose file — services](https://docs.docker.com/reference/compose-file/services/)
- [Compose healthcheck + depends_on](https://docs.docker.com/reference/compose-file/services/#healthcheck)
- [Compose profiles](https://docs.docker.com/compose/how-tos/profiles/)
- [Compose environment variables](https://docs.docker.com/compose/how-tos/environment-variables/)
- [Kubernetes documentation](https://kubernetes.io/docs/home/) — pods, deployments, services
- [Kubernetes concepts overview](https://kubernetes.io/docs/concepts/overview/)
- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes resource management (requests, limits, QoS)](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Encrypting etcd at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [Helm — charts](https://helm.sh/docs/topics/charts/)
- [Helm — using Helm](https://helm.sh/docs/intro/using_helm/)
- [kind — quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [kind — configuration](https://kind.sigs.k8s.io/docs/user/configuration/)
- [containers.dev — dev container spec](https://containers.dev/)
- [Dev container features](https://containers.dev/features)

## Version control and collaboration

- [Git reference manual](https://git-scm.com/doc) — canonical Git docs
- [git-branch](https://git-scm.com/docs/git-branch)
- [git-rebase](https://git-scm.com/docs/git-rebase)
- [git-merge](https://git-scm.com/docs/git-merge)
- [git-fetch](https://git-scm.com/docs/git-fetch)
- [git-pull](https://git-scm.com/docs/git-pull)
- [git-push](https://git-scm.com/docs/git-push) — includes `--force-with-lease` semantics
- [git-commit](https://git-scm.com/docs/git-commit)
- [gitignore pattern syntax](https://git-scm.com/docs/gitignore)
- [GitHub pull requests](https://docs.github.com/en/pull-requests)
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions documentation](https://docs.github.com/en/actions) — CI/CD
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [GitHub Actions encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Actions OIDC hardening](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub Actions OIDC in AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [GitHub Actions environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-python](https://github.com/actions/setup-python)
- [GitHub Codespaces overview](https://docs.github.com/en/codespaces/overview)
- [Gitpod introduction](https://www.gitpod.io/docs/introduction)

## Databases (OLTP, OLAP, embedded)

- [PostgreSQL documentation](https://www.postgresql.org/docs/current/) — reference database for Phases 1–2
- [PostgreSQL tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [PostgreSQL window functions tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL window functions reference](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL WITH queries (CTEs)](https://www.postgresql.org/docs/current/queries-with.html)
- [PostgreSQL EXPLAIN usage](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL routine vacuuming + MVCC](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- [PostgreSQL index types](https://www.postgresql.org/docs/current/indexes-types.html)
- [PostgreSQL multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL partial indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
- [PostgreSQL index-only scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
- [PostgreSQL pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [PostgreSQL pg_dump / pg_restore](https://www.postgresql.org/docs/current/app-pgdump.html)
- [PostgreSQL COPY](https://www.postgresql.org/docs/current/sql-copy.html)
- [PostgreSQL streaming replication](https://www.postgresql.org/docs/current/warm-standby.html)
- [PostgreSQL logical replication](https://www.postgresql.org/docs/current/logical-replication.html) — used by CDC
- [PostgreSQL `wal_level` config](https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-LEVEL)
- [MySQL reference manual](https://dev.mysql.com/doc/)
- [DuckDB documentation](https://duckdb.org/docs/) — embedded OLAP engine
- [DuckDB — httpfs / S3 extension](https://duckdb.org/docs/extensions/httpfs/s3api)
- [DuckDB COPY](https://duckdb.org/docs/sql/statements/copy)
- [DuckDB Parquet files](https://duckdb.org/docs/data/parquet/overview)
- [ClickHouse documentation](https://clickhouse.com/docs)
- [MongoDB documentation](https://www.mongodb.com/docs/)
- [Apache Cassandra documentation](https://cassandra.apache.org/doc/latest/)
- [Redis documentation](https://redis.io/docs/latest/)
- [Redis persistence (RDB vs AOF)](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- [Elastic documentation](https://www.elastic.co/docs)

## Lakehouse, file formats, catalogs

- [Apache Iceberg documentation](https://iceberg.apache.org/docs/latest/) — table format docs
- [Apache Iceberg spec](https://iceberg.apache.org/spec/) — authoritative snapshot/commit format
- [Iceberg Spark configuration](https://iceberg.apache.org/docs/latest/spark-configuration/)
- [Iceberg Spark DDL](https://iceberg.apache.org/docs/1.5.2/spark-ddl/)
- [Iceberg Spark writes](https://iceberg.apache.org/docs/latest/spark-writes/)
- [Iceberg Spark queries (time travel)](https://iceberg.apache.org/docs/1.5.2/spark-queries/)
- [Iceberg Hive catalog](https://iceberg.apache.org/docs/latest/hive/)
- [Iceberg catalog concepts](https://iceberg.apache.org/concepts/catalog/)
- [Iceberg maintenance](https://iceberg.apache.org/docs/latest/maintenance/) — expire snapshots, compaction, orphan cleanup
- [Iceberg schema evolution](https://iceberg.apache.org/docs/latest/evolution/)
- [Iceberg partitioning and hidden partitioning](https://iceberg.apache.org/docs/latest/partitioning/)
- [Iceberg Spark procedures](https://iceberg.apache.org/docs/latest/spark-procedures/)
- [Iceberg configuration reference](https://iceberg.apache.org/docs/latest/configuration/)
- [Delta Lake protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md) — table format commit protocol
- [Delta Lake documentation](https://docs.delta.io/)
- [Apache Parquet file format](https://parquet.apache.org/docs/file-format/) — columnar layout, row groups, statistics
- [Parquet nested encoding](https://parquet.apache.org/docs/file-format/nested-encoding/) — definition/repetition levels
- [Parquet metadata and statistics](https://parquet.apache.org/docs/file-format/metadata/)
- [Apache Avro specification](https://avro.apache.org/docs/) — row-oriented format spec
- [Avro 1.11.1 schema resolution](https://avro.apache.org/docs/1.11.1/specification/#schema-resolution)
- [Apache ORC specification](https://orc.apache.org/specification/) — columnar spec
- [MinIO documentation](https://min.io/docs/minio/linux/index.html) — S3-compatible object storage
- [MinIO S3 compatibility](https://min.io/docs/minio/linux/developers/s3-compatible-cloud-storage.html)
- [MinIO mc client reference](https://min.io/docs/minio/linux/reference/minio-mc.html)
- [MinIO Python SDK (minio-py)](https://min.io/docs/minio/linux/developers/python/minio-py.html)
- [Apache Hive Metastore admin](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+Administration)
- [Hive Metastore 3.0 admin](https://cwiki.apache.org/confluence/display/Hive/AdminManual+Metastore+3.0+Administration)
- [Hadoop S3A (3.3.4)](https://hadoop.apache.org/docs/r3.3.4/hadoop-aws/tools/hadoop-aws/index.html) — endpoint, path-style, credentials
- [Dremel paper (origin of Parquet rep/def levels)](https://research.google/pubs/pub36632/)

## Query engines (Trino, Spark)

- [Trino documentation](https://trino.io/docs/current/) — distributed SQL engine
- [Trino overview and use cases](https://trino.io/docs/current/overview/use-cases.html)
- [Trino cluster concepts](https://trino.io/docs/current/overview/concepts.html) — coordinator, worker, connector, catalog
- [Trino deployment](https://trino.io/docs/current/installation/deployment.html)
- [Trino general admin properties](https://trino.io/docs/current/admin/properties-general.html)
- [Trino connector catalog](https://trino.io/docs/current/connector.html)
- [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) — JDBC catalog, time travel, optimize, metadata tables
- [Trino Hive connector](https://trino.io/docs/current/connector/hive.html)
- [Trino PostgreSQL connector](https://trino.io/docs/current/connector/postgresql.html)
- [Trino SQL reference](https://trino.io/docs/current/sql.html)
- [Trino functions and operators](https://trino.io/docs/current/functions.html)
- [Trino EXPLAIN](https://trino.io/docs/current/sql/explain.html)
- [Trino EXPLAIN ANALYZE](https://trino.io/docs/current/sql/explain-analyze.html)
- [Trino web UI](https://trino.io/docs/current/admin/web-interface.html)
- [Trino resource groups](https://trino.io/docs/current/admin/resource-groups.html)
- [Trino file-based system access control](https://trino.io/docs/current/security/file-system-access-control.html) — column masks, row filters
- [Trino Kubernetes deployment](https://trino.io/docs/current/installation/kubernetes.html)
- [trinodb/charts — official Helm chart](https://github.com/trinodb/charts)
- [Apache Spark documentation](https://spark.apache.org/docs/latest/) — unified processing engine
- [Spark SQL programming guide (3.5.3)](https://spark.apache.org/docs/3.5.3/sql-programming-guide.html)
- [PySpark DataFrame quickstart](https://spark.apache.org/docs/3.5.3/api/python/getting_started/quickstart_df.html)
- [PySpark DataFrame API reference](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/dataframe.html)
- [Spark configuration reference](https://spark.apache.org/docs/3.5.3/configuration.html)
- [Spark submitting applications](https://spark.apache.org/docs/3.5.3/submitting-applications.html)
- [Spark memory tuning](https://spark.apache.org/docs/3.5.3/tuning.html#memory-tuning)
- [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html) — AQE, broadcast, shuffle partitions
- [Spark tuning guide](https://spark.apache.org/docs/latest/tuning.html)
- [Spark Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)

## Ingestion and CDC

- [dlt documentation](https://dlthub.com/docs/intro) — Python declarative EL
- [dlt how it works](https://dlthub.com/docs/reference/explainers/how-dlt-works)
- [dlt sources](https://dlthub.com/docs/general-usage/source)
- [dlt resources](https://dlthub.com/docs/general-usage/resource)
- [dlt incremental loading](https://dlthub.com/docs/general-usage/incremental-loading)
- [dlt state and resumability](https://dlthub.com/docs/general-usage/state)
- [dlt schema contracts](https://dlthub.com/docs/general-usage/schema-contracts)
- [dlt filesystem destination](https://dlthub.com/docs/dlt-ecosystem/destinations/filesystem)
- [dlt Iceberg destination](https://dlthub.com/docs/dlt-ecosystem/destinations/iceberg)
- [dlt credentials and config](https://dlthub.com/docs/general-usage/credentials)
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — event streaming
- [Kafka introduction](https://kafka.apache.org/documentation/#introduction)
- [Kafka replication design](https://kafka.apache.org/documentation/#replication)
- [Kafka delivery semantics](https://kafka.apache.org/documentation/#semantics)
- [Kafka log compaction](https://kafka.apache.org/documentation/#compaction)
- [Kafka KRaft mode](https://kafka.apache.org/documentation/#kraft)
- [Kafka producer configs](https://kafka.apache.org/documentation/#producerconfigs)
- [Kafka consumer configs](https://kafka.apache.org/documentation/#consumerconfigs)
- [Kafka topic configs](https://kafka.apache.org/documentation/#topicconfigs)
- [Kafka Connect](https://kafka.apache.org/documentation/#connect) — source/sink connector framework
- [Kafka Connect transforms (SMTs)](https://kafka.apache.org/documentation/#connect_transforms)
- [Kafka Connect REST API](https://kafka.apache.org/documentation/#connect_rest)
- [Kafka quickstart](https://kafka.apache.org/quickstart)
- [kafka-python documentation](https://kafka-python.readthedocs.io/) — Python Kafka client
- [Debezium documentation](https://debezium.io/documentation/reference/stable/) — CDC platform
- [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html)
- [Debezium PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html)
- [Debezium outbox event router SMT](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)
- [Debezium new record state extraction (unwrap) SMT](https://debezium.io/documentation/reference/stable/transformations/event-flattening.html)

## Transformation (dbt)

- [dbt documentation](https://docs.getdbt.com/docs/introduction) — SQL transformations, tests, docs
- [dbt projects](https://docs.getdbt.com/docs/build/projects)
- [dbt_project.yml reference](https://docs.getdbt.com/reference/dbt_project.yml)
- [dbt profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml)
- [dbt models](https://docs.getdbt.com/docs/build/models)
- [dbt materializations](https://docs.getdbt.com/docs/build/materializations)
- [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)
- [dbt sources](https://docs.getdbt.com/docs/build/sources)
- [dbt source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness)
- [dbt ref function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)
- [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)
- [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests) — mocked fixtures, dbt 1.8+
- [dbt seeds](https://docs.getdbt.com/docs/build/seeds)
- [dbt snapshots](https://docs.getdbt.com/docs/build/snapshots) — SCD Type 2
- [dbt packages](https://docs.getdbt.com/docs/build/packages)
- [dbt test severity configs](https://docs.getdbt.com/reference/resource-configs/severity)
- [dbt how-we-structure guide](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) — staging / intermediate / marts
- [dbt model contracts](https://docs.getdbt.com/docs/collaborate/govern/model-contracts)
- [dbt model versions](https://docs.getdbt.com/docs/collaborate/govern/model-versions)
- [dbt documentation and lineage](https://docs.getdbt.com/docs/collaborate/documentation)
- [dbt continuous integration jobs](https://docs.getdbt.com/docs/deploy/continuous-integration) — Slim CI, deferral, state comparisons
- [dbt-trino adapter](https://docs.getdbt.com/docs/core/connect-data-platform/trino-setup)

## Orchestration (Dagster, Airflow)

- [Dagster documentation](https://docs.dagster.io/) — asset-based orchestrator
- [Dagster software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets)
- [Dagster asset definitions](https://docs.dagster.io/concepts/assets/asset-definitions)
- [Dagster resources](https://docs.dagster.io/concepts/resources)
- [Dagster IO managers](https://docs.dagster.io/concepts/io-management/io-managers)
- [Dagster jobs](https://docs.dagster.io/concepts/assets/asset-jobs)
- [Dagster schedules](https://docs.dagster.io/concepts/automation/schedules)
- [Dagster sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors)
- [Dagster partitions](https://docs.dagster.io/concepts/partitions-schedules-sensors/partitions)
- [Dagster asset checks](https://docs.dagster.io/concepts/assets/asset-checks)
- [Dagster freshness checks](https://docs.dagster.io/concepts/assets/asset-checks/checking-for-data-freshness)
- [Dagster declarative automation](https://docs.dagster.io/concepts/automation/declarative-automation)
- [dagster-dlt integration](https://docs.dagster.io/integrations/dlt)
- [dagster-dbt integration](https://docs.dagster.io/integrations/dbt)
- [Dagster workspace files](https://docs.dagster.io/concepts/code-locations/workspace-files)
- [Dagster CLI reference](https://docs.dagster.io/_apidocs/cli)
- [Apache Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/) — task-based orchestrator
- [Airflow architecture overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- [Airflow core concepts — DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Airflow operators](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html)
- [Airflow TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
- [Airflow XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)
- [Airflow connections and secrets backends](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html)
- [Airflow datasets and data-aware scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html)
- [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow templates reference](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)
- [Airflow providers index](https://airflow.apache.org/docs/apache-airflow-providers/)

## Data quality and validation

- [Great Expectations core concepts](https://docs.greatexpectations.io/docs/core/introduction/)
- [Great Expectations gallery](https://greatexpectations.io/expectations/)

## BI / serving layer

- [Metabase documentation](https://www.metabase.com/docs/latest/) — open-source BI
- [Metabase connecting to databases](https://www.metabase.com/docs/latest/databases/connecting)
- [Metabase Starburst / Trino driver](https://www.metabase.com/data_sources/starburst)
- [Metabase dashboards](https://www.metabase.com/docs/latest/dashboards/introduction)
- [Metabase permissions](https://www.metabase.com/docs/latest/permissions/introduction)
- [Metabase embedding](https://www.metabase.com/docs/latest/embedding/introduction)
- [FastAPI documentation](https://fastapi.tiangolo.com/) — typed Python API framework
- [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/) — OAuth2, API key, HTTP Basic
- [gRPC introduction](https://grpc.io/docs/what-is-grpc/introduction/) — RPC framework, HTTP/2, protobuf
- [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [Feast feature store](https://docs.feast.dev/)
- [Feast point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

## Observability (OTel, Prometheus, Grafana)

- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — tracing/metrics/logs standard
- [OTel signals primer](https://opentelemetry.io/docs/concepts/signals/)
- [OTel metrics signal](https://opentelemetry.io/docs/concepts/signals/metrics/)
- [OTel logs signal](https://opentelemetry.io/docs/concepts/signals/logs/)
- [OTel traces signal](https://opentelemetry.io/docs/concepts/signals/traces/)
- [Prometheus documentation](https://prometheus.io/docs/introduction/overview/) — metrics/time-series
- [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- [PromQL basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Grafana documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana data sources](https://grafana.com/docs/grafana/latest/datasources/)
- [Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Grafana dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [OpenLineage object model](https://openlineage.io/docs/spec/object-model) — run/job/dataset lineage events

## FinOps

- [FinOps Framework](https://www.finops.org/framework/) — canonical FinOps principles and capabilities
- [FinOps phases (Inform / Optimize / Operate)](https://www.finops.org/framework/phases/)
- [FinOps capability — allocation](https://www.finops.org/framework/capabilities/allocation/)
- [FinOps capability — chargeback and finance integration](https://www.finops.org/framework/capabilities/chargeback-finance-integration/)
- [FinOps capability — unit economics](https://www.finops.org/framework/capabilities/unit-economics/)
- [FinOps capability — rate optimization](https://www.finops.org/framework/capabilities/rate-optimization/)
- [FinOps capability — workload optimization](https://www.finops.org/framework/capabilities/workload-optimization/)
- [FinOps capability — anomaly management](https://www.finops.org/framework/capabilities/anomaly-management/)

## Canonical articles and third-party primary sources

- [Data Mesh Principles — Zhamak Dehghani](https://martinfowler.com/articles/data-mesh-principles.html) — original principles post
- [Databricks medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) — Bronze/Silver/Gold pattern

---

# Cloud provider branches

## AWS

### Storage and catalog
- [Amazon S3 user guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
- [S3 lifecycle management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
- [S3 Access Points](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)
- [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)
- [S3 event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)
- [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html#data-catalog-intro)
- [Glue crawlers](https://docs.aws.amazon.com/glue/latest/dg/add-crawler.html)
- [AWS Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [Lake Formation permissions reference](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-reference.html)
- [Lake Formation tag-based access control](https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html)
- [Athena Iceberg tables](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html)
- [Athena OPTIMIZE statement](https://docs.aws.amazon.com/athena/latest/ug/optimize-statement.html)

### Ingestion and streaming
- [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [KDS shards and partition keys](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html)
- [KDS enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html)
- [Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
- [Firehose delivery stream settings](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html)
- [Amazon MSK](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html)
- [MSK IAM authentication](https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html)
- [AWS DMS](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
- [DMS S3 target](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html)
- [DMS change data capture](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html)
- [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS Snow Family](https://docs.aws.amazon.com/snowball/latest/ug/whatisdevice.html)
- [Amazon AppFlow](https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html)

### Compute (Glue, EMR, Athena, Redshift)
- [AWS Glue developer guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [Glue DynamicFrames](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
- [Glue job bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html)
- [Glue DataBrew](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html)
- [Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html)
- [Glue workflows](https://docs.aws.amazon.com/glue/latest/dg/orchestrate-using-workflows.html)
- [Amazon EMR management guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [Amazon EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [Amazon EMR on EKS](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/emr-eks.html)
- [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html)
- [EMR instance fleets with Spot](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html)
- [Amazon Athena user guide](https://docs.aws.amazon.com/athena/latest/ug/what-is.html)
- [Athena partition projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html)
- [Athena federated query](https://docs.aws.amazon.com/athena/latest/ug/connect-to-a-data-source.html)
- [Athena performance tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html)
- [Athena query results reuse (cache)](https://docs.aws.amazon.com/athena/latest/ug/reusing-query-results.html)
- [Athena workgroups](https://docs.aws.amazon.com/athena/latest/ug/workgroups.html)
- [Amazon Redshift developer guide](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
- [Redshift distribution styles](https://docs.aws.amazon.com/redshift/latest/dg/c_choosing_dist_sort.html)
- [Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html)
- [Redshift materialized views](https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html)
- [Redshift data sharing](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)
- [Amazon Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html)
- [AWS Managed Service for Apache Flink](https://docs.aws.amazon.com/managed-flink/latest/java/what-is.html)
- [Amazon QuickSight](https://docs.aws.amazon.com/quicksight/latest/user/welcome.html)

### Orchestration and messaging
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Step Functions Standard vs Express](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html)
- [Step Functions service integrations](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html)
- [Step Functions distributed map](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-asl-use-map-state-distributed.html)
- [Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [Amazon MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) — managed Airflow
- [MWAA environment classes](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-env-class.html)
- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html)
- [Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)

### IAM, security, governance
- [AWS IAM user guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [IAM identity management overview](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_identity-management.html)
- [IAM policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — explicit deny > allow > implicit deny
- [IAM identity-based vs resource-based policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html)
- [IAM roles terms and concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html)
- [IAM condition keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html)
- [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [IAM attribute-based access control (ABAC)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
- [IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS STS — requesting temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html)
- [AWS KMS developer guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [KMS cross-account access](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [Secrets Manager secret rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
- [Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [VPC endpoints and PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)
- [Gateway VPC endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)
- [Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
- [CloudTrail data events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html)
- [CloudTrail Lake](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html)
- [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)

### Networking and platform
- [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [AWS global infrastructure (regions and AZs)](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)
- [Amazon VPC user guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [VPC subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
- [VPC NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Amazon RDS user guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [Amazon DynamoDB developer guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [DynamoDB TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [DynamoDB capacity modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
- [Amazon DocumentDB](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [Amazon Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html)
- [Amazon Keyspaces](https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html)
- [Amazon MemoryDB](https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb-for-redis.html)
- [Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [AWS Transfer Family](https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html)

### Monitoring and FinOps (AWS)
- [Amazon CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)
- [AWS Cost Explorer](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/ce-what-is.html)
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [S3 pricing](https://aws.amazon.com/s3/pricing/)
- [Athena pricing](https://aws.amazon.com/athena/pricing/)
- [AWS Glue pricing](https://aws.amazon.com/glue/pricing/)
- [Amazon EMR pricing](https://aws.amazon.com/emr/pricing/)
- [Amazon Redshift pricing](https://aws.amazon.com/redshift/pricing/)
- [Kinesis Data Streams pricing](https://aws.amazon.com/kinesis/data-streams/pricing/)
- [Firehose pricing](https://aws.amazon.com/firehose/pricing/)
- [Amazon MSK pricing](https://aws.amazon.com/msk/pricing/)
- [DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/)
- [Lambda pricing](https://aws.amazon.com/lambda/pricing/)
- [EC2 on-demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/)

### LocalStack (AWS emulator)
- [LocalStack documentation](https://docs.localstack.cloud/overview/)
- [LocalStack getting started](https://docs.localstack.cloud/getting-started/)
- [LocalStack IAM coverage](https://docs.localstack.cloud/user-guide/aws/iam/)
- [LocalStack S3](https://docs.localstack.cloud/user-guide/aws/s3/)
- [LocalStack STS](https://docs.localstack.cloud/user-guide/aws/sts/)

## Azure

### Storage and lakehouse (ADLS, OneLake, Fabric)
- [Azure Data Lake Storage Gen2 introduction](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [ADLS Gen2 access control (RBAC + POSIX ACLs)](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-access-control-model)
- [Set ACLs on ADLS Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-acl-azure-portal)
- [OneLake overview](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview)
- [OneLake security](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security)
- [OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcuts)
- [Create a OneLake shortcut](https://learn.microsoft.com/en-us/fabric/onelake/create-onelake-shortcut)
- [Fabric mirroring overview](https://learn.microsoft.com/en-us/fabric/database/mirrored-database/overview)
- [Fabric Lakehouse overview](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-overview)
- [Create a Fabric Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse)
- [Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing)
- [Fabric Warehouse T-SQL surface area](https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area)
- [Fabric Lakehouse SQL analytics endpoint](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint)
- [COPY statement in Fabric Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/ingest-data-copy)
- [Delta optimization and V-Order in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)
- [Delta Lake table maintenance in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance)

### Ingestion (ADF, Fabric Data Factory, Dataflows)
- [Azure Data Factory introduction](https://learn.microsoft.com/en-us/azure/data-factory/introduction)
- [ADF copy activity overview](https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-overview)
- [ADF mapping data flows](https://learn.microsoft.com/en-us/azure/data-factory/concepts-data-flow-overview)
- [ADF pipeline triggers](https://learn.microsoft.com/en-us/azure/data-factory/concepts-pipeline-execution-triggers)
- [ADF integration runtime](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime)
- [ADF expressions and functions](https://learn.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions)
- [ADF SQL Server CDC connector](https://learn.microsoft.com/en-us/azure/data-factory/connector-sql-server-change-data-capture)
- [Fabric Data Factory overview](https://learn.microsoft.com/en-us/fabric/data-factory/)
- [Fabric pipeline activities](https://learn.microsoft.com/en-us/fabric/data-factory/activity-overview)
- [Fabric copy data activity](https://learn.microsoft.com/en-us/fabric/data-factory/copy-data-activity)
- [Dataflow Gen2 overview](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-overview)
- [Create your first Dataflow Gen2](https://learn.microsoft.com/en-us/fabric/data-factory/create-first-dataflow-gen2)
- [Power Query M function reference](https://learn.microsoft.com/en-us/powerquery-m/power-query-m-function-reference)
- [On-premises data gateway](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem)
- [Delta Change Data Feed (Databricks on Azure)](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed)

### Compute (Synapse, Databricks, Fabric)
- [Fabric Spark compute](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Fabric notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
- [Fabric Spark SQL reference](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-sql-reference)
- [Fabric KQL database](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/create-database)
- [Kusto Query Language reference](https://learn.microsoft.com/en-us/kusto/query/)
- [Azure Synapse Analytics overview](https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is)
- [Synapse dedicated SQL pool distributions](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-distribute)
- [Synapse DMVs](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-manage-monitor)
- [Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/)
- [Databricks Delta Lake on Azure](https://learn.microsoft.com/en-us/azure/databricks/delta/)
- [Delta Lake MERGE](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Databricks Adaptive Query Execution](https://learn.microsoft.com/en-us/azure/databricks/optimizations/aqe)
- [T-SQL language reference](https://learn.microsoft.com/en-us/sql/t-sql/language-reference)

### Streaming and real-time (Event Hubs, Stream Analytics, Fabric RTI)
- [Azure Event Hubs overview](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about)
- [Event Hubs features](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-features)
- [Event Hubs Capture](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview)
- [Azure Stream Analytics](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-introduction)
- [Stream Analytics windowing](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-window-functions)
- [Stream Analytics parallelization](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-parallelization)
- [Databricks Structured Streaming on Azure](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/)
- [Fabric Real-Time Intelligence overview](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/overview)
- [Fabric Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/overview)
- [Create a Fabric Eventstream](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/create)
- [Fabric Activator](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/data-activator/data-activator-introduction)

### Security, identity, governance
- [Microsoft Entra ID fundamentals](https://learn.microsoft.com/en-us/entra/fundamentals/whatis)
- [Azure RBAC overview](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview)
- [Storage built-in roles](https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access)
- [Managed identities for Azure resources](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
- [Fabric workspace identity](https://learn.microsoft.com/en-us/fabric/security/workspace-identity)
- [Fabric workspace roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)
- [Row-level security (T-SQL)](https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security)
- [Column-level security](https://learn.microsoft.com/en-us/sql/relational-databases/security/column-level-security)
- [Dynamic data masking](https://learn.microsoft.com/en-us/sql/relational-databases/security/dynamic-data-masking)
- [Storage service encryption](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption)
- [Customer-managed keys with Key Vault](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-overview)
- [Azure private endpoints](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [Azure service endpoints](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview)
- [Microsoft Purview overview](https://learn.microsoft.com/en-us/purview/purview)
- [Purview Data Map](https://learn.microsoft.com/en-us/purview/concept-data-map)
- [Purview lineage](https://learn.microsoft.com/en-us/purview/concept-data-lineage)

### Networking and platform (Azure)
- [Azure shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
- [Azure regions and availability zones](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview)
- [Azure Virtual Network overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Azure NAT gateway](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview)
- [Azure SQL Database (PaaS) overview](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview)
- [Azure bandwidth pricing](https://azure.microsoft.com/en-us/pricing/details/bandwidth/)

### Monitoring and optimization (Azure)
- [Azure Monitor overview](https://learn.microsoft.com/en-us/azure/azure-monitor/overview)
- [Log Analytics overview](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview)
- [KQL tutorial](https://learn.microsoft.com/en-us/kusto/query/tutorial)
- [Azure diagnostic settings](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/diagnostic-settings)
- [Monitor ADF visually](https://learn.microsoft.com/en-us/azure/data-factory/monitor-visually)
- [Azure alerts overview](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview)
- [Create metric alert](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-metric)
- [Fabric monitoring hub](https://learn.microsoft.com/en-us/fabric/admin/monitoring-hub)
- [Fabric capacity metrics app](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)
- [Fabric Warehouse query insights](https://learn.microsoft.com/en-us/fabric/data-warehouse/query-insights)

## Snowflake

### Architecture and platform
- [Snowflake documentation](https://docs.snowflake.com/)
- [Snowflake key concepts and architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) — three-layer storage/compute/services model
- [Micro-partitions and data clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)
- [Virtual warehouses overview](https://docs.snowflake.com/en/user-guide/warehouses)
- [Persisted query results (result cache)](https://docs.snowflake.com/en/user-guide/querying-persisted-results)
- [Snowflake credits (services layer)](https://docs.snowflake.com/en/user-guide/credits)

### Loading
- [Loading data overview](https://docs.snowflake.com/en/user-guide/data-load-overview)
- [COPY INTO \<table\>](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [CREATE STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage)
- [CREATE FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)
- [CREATE STORAGE INTEGRATION](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration)
- [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro)
- [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview)
- [Snowflake Kafka connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview)
- [INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema)
- [Semi-structured data (VARIANT)](https://docs.snowflake.com/en/user-guide/semistructured-concepts)
- [SYSTEM$PIPE_STATUS](https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status)
- [VALIDATE_PIPE_LOAD](https://docs.snowflake.com/en/sql-reference/functions/validate_pipe_load)

### Access control and identity
- [Access control overview](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Access control considerations](https://docs.snowflake.com/en/user-guide/security-access-control-considerations)
- [GRANT privileges](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege)
- [USE ROLE](https://docs.snowflake.com/en/sql-reference/sql/use-role)
- [USE SECONDARY ROLES](https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles)
- [SCIM overview](https://docs.snowflake.com/en/user-guide/scim-intro)
- [SCIM for Okta / Azure AD](https://docs.snowflake.com/en/user-guide/scim-okta)

### Data protection
- [Continuous Data Protection (CDP)](https://docs.snowflake.com/en/user-guide/data-cdp)
- [Time Travel](https://docs.snowflake.com/en/user-guide/data-time-travel)
- [Fail-safe](https://docs.snowflake.com/en/user-guide/data-failsafe)
- [Object cloning (zero-copy)](https://docs.snowflake.com/en/user-guide/object-clone)
- [UNDROP TABLE](https://docs.snowflake.com/en/sql-reference/sql/undrop-table)
- [Database replication and failover](https://docs.snowflake.com/en/user-guide/account-replication-intro)
- [Encryption management and Tri-Secret Secure](https://docs.snowflake.com/en/user-guide/security-encryption-manage)
- [TABLE_STORAGE_METRICS](https://docs.snowflake.com/en/sql-reference/account-usage/table_storage_metrics)

### Performance and cost
- [Multi-cluster warehouses](https://docs.snowflake.com/en/user-guide/warehouses-multicluster)
- [ALTER WAREHOUSE](https://docs.snowflake.com/en/sql-reference/sql/alter-warehouse)
- [Query Profile](https://docs.snowflake.com/en/user-guide/ui-query-profile)
- [Clustering keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [SYSTEM$CLUSTERING_INFORMATION](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_information)
- [SYSTEM$CLUSTERING_DEPTH](https://docs.snowflake.com/en/sql-reference/functions/system_clustering_depth)
- [Search Optimization Service](https://docs.snowflake.com/en/user-guide/search-optimization-service)
- [Query Acceleration Service](https://docs.snowflake.com/en/user-guide/query-acceleration-service)
- [Materialized views](https://docs.snowflake.com/en/user-guide/views-materialized)
- [Resource monitors](https://docs.snowflake.com/en/user-guide/resource-monitors)
- [WAREHOUSE_METERING_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history)

### Advanced (streams, tasks, dynamic tables, Snowpark)
- [Streams intro](https://docs.snowflake.com/en/user-guide/streams-intro) — CDC primitive
- [Tasks intro](https://docs.snowflake.com/en/user-guide/tasks-intro)
- [CREATE STREAM](https://docs.snowflake.com/en/sql-reference/sql/create-stream)
- [CREATE TASK](https://docs.snowflake.com/en/sql-reference/sql/create-task)
- [Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [CREATE DYNAMIC TABLE](https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table)
- [User-defined functions overview](https://docs.snowflake.com/en/developer-guide/udf/udf-overview)
- [Secure UDFs](https://docs.snowflake.com/en/developer-guide/udf/udf-secure)
- [Python UDTFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-tabular-functions)
- [External functions](https://docs.snowflake.com/en/sql-reference/external-functions)
- [API integration](https://docs.snowflake.com/en/sql-reference/sql/create-api-integration)
- [Snowpark for Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Snowpark-optimized warehouses](https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized)
- [Iceberg tables in Snowflake](https://docs.snowflake.com/en/user-guide/tables-iceberg)
- [External tables](https://docs.snowflake.com/en/user-guide/tables-external-intro)
- [SYSTEM$STREAM_HAS_DATA](https://docs.snowflake.com/en/sql-reference/functions/system_stream_has_data)
- [TASK_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/task_history)

## Google Cloud (reference only — not a vendor branch)

- [Google Cloud shared responsibility](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)
- [Google Cloud geography and regions](https://cloud.google.com/docs/geography-and-regions)
- [Google Cloud VPC overview](https://cloud.google.com/vpc/docs/overview)
- [Google Cloud NAT](https://cloud.google.com/nat/docs/overview)
- [Google Cloud Storage overview](https://cloud.google.com/storage/docs/introduction)
- [Google Cloud SQL overview](https://cloud.google.com/sql/docs/introduction)
- [Google Cloud VPC network pricing](https://cloud.google.com/vpc/network-pricing)
- [GCP service accounts](https://cloud.google.com/iam/docs/service-account-overview)
- [GCP Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Cloud Composer (managed Airflow on GCP)](https://cloud.google.com/composer/docs/concepts/overview)
- [Google Cloud BigQuery documentation](https://cloud.google.com/bigquery/docs)

---

# Certification programs

- [Linux Foundation Certified IT Associate (LFCA)](https://training.linuxfoundation.org/certification/certified-it-associate/) — optional Phase 1 cert
- [AWS Certified Data Engineer – Associate (DEA-C01)](https://aws.amazon.com/certification/certified-data-engineer-associate/)
- [AWS certification portal](https://www.aws.training/certification) — scheduling and score history
- [AWS certification testing policies](https://aws.amazon.com/certification/policies/before-testing/)
- [Microsoft Certified: Fabric Data Engineer Associate (DP-700)](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/)
- [Exam DP-700 page](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/)
- [DP-700 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-700)
- [DP-700 practice assessment](https://learn.microsoft.com/en-us/credentials/certifications/exams/dp-700/practice/assessment)
- [DP-700 training path](https://learn.microsoft.com/en-us/training/courses/dp-700t00)
- [Microsoft Fabric trial](https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial)
- [Microsoft certification renewal](https://learn.microsoft.com/en-us/credentials/certifications/renew-your-microsoft-certification)
- [What is Microsoft Fabric?](https://learn.microsoft.com/en-us/fabric/get-started/microsoft-fabric-overview)
- [Snowflake certifications hub](https://www.snowflake.com/en/learn/certifications/)
- [SnowPro Associate: Platform (SOL-C01)](https://www.snowflake.com/en/learn/certifications/snowpro-associate-platform/)
- [SnowPro Core (COF-C02)](https://www.snowflake.com/en/learn/certifications/snowpro-core/)
- [SnowPro Advanced: Data Engineer (DEA-C02)](https://www.snowflake.com/en/learn/certifications/snowpro-advanced-data-engineer/)
- [Snowflake University](https://learn.snowflake.com/)

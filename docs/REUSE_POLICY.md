# Reuse and Citation Policy

Enforced across every module and lab. Agents building content MUST follow these rules.

## Accepted sources (priority order)

1. **Official tool documentation** at canonical domains — `iceberg.apache.org`, `trino.io`, `spark.apache.org`, `kafka.apache.org`, `airflow.apache.org`, `kubernetes.io`, `docs.getdbt.com`, `docs.dagster.io`, `dlthub.com`, `duckdb.org`, `postgresql.org`, `docs.docker.com`, `git-scm.com`, `python.org`, `debezium.io`, `min.io`, `metabase.com`, `prometheus.io`, `grafana.com`, `localstack.cloud`
2. **Official specifications** — Apache Iceberg spec, Parquet spec, Avro spec, RFCs
3. **Canonical books** — *Designing Data-Intensive Applications* (Kleppmann), *The Data Warehouse Toolkit* (Kimball), *Building the Data Warehouse* (Inmon), *Fundamentals of Data Engineering* (Reis/Housley). Cite as `*Title, Author, Ch. N*`. No URL unless a publisher page is verified. No copyrighted prose quoted.
4. **Existing sibling-dir files** — `../dataeng/`, `../linux_fundamentals/`, `../aws_certified/`, `../azure_certified/`, `../snowflake_eng/`. Cite as `../<sibling>/<path>:L<start>-L<end>`.
5. **Vendor certification pages** — AWS Certification, Microsoft Learn, Snowflake University (exam outlines, skill domains).

## Rejected sources

- Unverified blog posts
- Medium articles unless from the official tool account
- Stack Overflow answers (except alongside the canonical doc they reference)
- LLM-generated summaries from unknown origin
- Anything the writer cannot anchor to an accepted source → **omit the claim**, do not tag it `[UNVERIFIED]`

## Citation format

Inline in prose:
- Link: `[Iceberg table spec](https://iceberg.apache.org/spec/)`
- Book: `*Designing Data-Intensive Applications*, Kleppmann, Ch. 5`
- Sibling file: `../dataeng/notes/iceberg_catalog.md:L42-L67`

At the bottom of each module, a `references.md` lists all sources with one-line context.

## Reuse-first rule

Before writing any new module content, the agent must:
1. Search the sibling dirs for existing content on the same topic (Grep the topic keywords)
2. If found, lift it verbatim or lightly adapt — do not rewrite
3. If not found, write new content from primary docs
4. Either way, cite the source

## Factual-only rule

- If you cannot verify a number, version, or claim against a cited source → **omit it**
- Approximations ("roughly 70%") are only allowed if the source itself states the approximation
- Tool versions must be checked against the latest stable release page before being pinned in a compose file
- Do not invent example commands that have not been run

## Compactness rule

- Module README: 600–2000 words of prose (not counting code/tables)
- Lab README: 200–600 words
- Concepts: 2–5 sentences per concept
- No motivational preambles. No recaps. No "in this module you will learn" followed by the same list again.

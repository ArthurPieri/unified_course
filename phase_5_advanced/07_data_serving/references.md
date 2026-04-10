# References — Module 07: Data Serving

## Primary docs
- [FastAPI — main docs](https://fastapi.tiangolo.com/) — framework description, type-hint-driven schema, automatic interactive docs.
- [FastAPI — first steps](https://fastapi.tiangolo.com/tutorial/first-steps/) — automatic `/docs` and `/redoc` generation from path operations.
- [FastAPI — metadata and docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/) — OpenAPI metadata, custom docs paths.
- [FastAPI — request body](https://fastapi.tiangolo.com/tutorial/body/) — Pydantic models as request/response schemas.
- [FastAPI — async and await](https://fastapi.tiangolo.com/async/) — when to use `async def` vs `def`, threadpool behavior.
- [FastAPI — security intro](https://fastapi.tiangolo.com/tutorial/security/) — OAuth2, API key, HTTP Basic via dependency injection.
- [gRPC — what is gRPC](https://grpc.io/docs/what-is-grpc/introduction/) — RPC framework, HTTP/2, protobuf IDL.
- [gRPC — core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/) — service definition, unary and streaming RPCs.
- [Feast — introduction](https://docs.feast.dev/) — feature store definition, storage and serving responsibilities.
- [Feast — point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) — training data correctness, feature leakage prevention.
- [Trino — overview and use cases](https://trino.io/docs/current/overview/use-cases.html) — interactive analytic query engine positioning.
- [Trino — resource groups](https://trino.io/docs/current/admin/resource-groups.html) — isolating workload classes in a shared cluster.
- [DuckDB — why DuckDB](https://duckdb.org/why_duckdb) — in-process OLAP DBMS description, serving implications.
- [DuckDB — docs root](https://duckdb.org/docs/) — embedded engine, Parquet, httpfs for direct object-storage serving.

## Books
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 9 — serving stage of the data engineering lifecycle; reverse ETL as operational activation of warehouse data.
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 11 — derived data, materialized views, and the read-path trade-offs that motivate serving layers.

# Module 07: Data Serving — APIs, Feature Stores, Reverse ETL (6h)

> The warehouse holds the truth, but applications, ML models, and SaaS tools need that truth shaped, cached, and delivered on their own terms. This module covers the four dominant serving patterns, when a warehouse query is enough versus when you need a dedicated serving layer, and the primary-source mental models for each pattern. No blogs; every non-obvious claim cites the canonical docs.

## Learning goals
- Name the four data-serving patterns (BI dashboards, low-latency APIs, feature stores, reverse ETL) and give one concrete use case for each.
- Decide between "query the warehouse directly" and "push into a serving store" using a latency budget.
- Sketch a read-only FastAPI endpoint with a Pydantic response model and explain how OpenAPI is generated.
- Describe the online/offline split of a feature store and why point-in-time correctness is the hard problem.
- Explain the reverse-ETL mental model and what distinguishes it from a classical ETL/ELT load.
- Identify where caching belongs (in-process, Redis, CDN) relative to the query engine.

## Prerequisites
- `phase_3_core_tools/` — Trino / lakehouse query layer fluency.
- `phase_5_advanced/04_cloud_concepts/` — IaaS/PaaS framing for managed caches and API gateways.
- `phase_5_advanced/05_iam_primer/` — auth vocabulary used by API endpoints.

## Reading order
1. This README
2. `quiz.md`

## Concepts

### The four serving patterns
Warehouse data is consumed in four distinct shapes, and the right stack for each is different. (1) **BI dashboards** pull aggregates on a slow cadence; the warehouse itself is usually the serving layer. (2) **Low-latency data APIs** return small, filtered slices to application code on a request/response loop; they need predictable p99 latency. (3) **Feature stores** serve ML models — the same feature has to be queryable both in large historical batches (training) and at single-row per-request speed (inference). (4) **Reverse ETL** does not serve queries at all; it pushes warehouse rows back into operational SaaS systems (CRMs, ad platforms, support tools) on a schedule. Patterns 1 and 4 are pull-from-warehouse; patterns 2 and 3 usually need a dedicated serving store because the warehouse cannot meet the latency SLO.

### When the warehouse is enough
A modern OLAP engine serving dashboard queries in the low-seconds range is operationally simpler than any caching layer. The rough heuristic most practitioners apply: if the latency SLO is above ~100 ms and concurrency is moderate, query the warehouse or lakehouse directly and skip a serving store. Trino's documentation frames Trino precisely as a tool for "interactive analytic queries" running over large datasets, which matches the BI-dashboard serving pattern.
Ref: [Trino overview](https://trino.io/docs/current/overview/use-cases.html)

Once the SLO drops below ~100 ms — typical for user-facing APIs and for online ML inference — the warehouse stops being appropriate: each query pays planner, scheduler, and scan overhead, and concurrency scales by adding expensive workers. That is the moment to introduce either a cache or a purpose-built serving database. The split is not a hard rule; it is a budget question tied to tail latency, concurrency, and cost.

### Low-latency APIs with FastAPI
For read-only data APIs over a warehouse or cache, FastAPI is a common Python choice because it is async by default and generates its schema from Python type hints. The FastAPI docs describe it as "a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints", with automatic interactive API docs derived from the same type hints. Request and response shapes are declared as Pydantic models, which become both runtime validators and the schema FastAPI serializes into OpenAPI.
Ref: [FastAPI — main docs](https://fastapi.tiangolo.com/)

A minimal serving endpoint looks like a function that accepts a validated query model, executes a parameterized SQL query against the warehouse or cache, and returns a Pydantic response model. Async endpoints free the event loop during I/O so a single worker can handle many concurrent warehouse calls. For CPU-bound serialization FastAPI recommends using plain `def` handlers, which it runs in a threadpool.
Ref: [FastAPI — async and await](https://fastapi.tiangolo.com/async/)

### OpenAPI and contracts
FastAPI auto-generates an OpenAPI 3 schema from the declared path operations and Pydantic models, and exposes interactive Swagger UI and ReDoc browsers at `/docs` and `/redoc` without additional code. This is why "contract-first" and "code-first" collapse into the same workflow for FastAPI: the code *is* the contract, because the generated OpenAPI document reflects whatever the type hints say.
Ref: [FastAPI — first steps (automatic docs)](https://fastapi.tiangolo.com/tutorial/first-steps/) · [FastAPI — metadata and docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/)

### gRPC as the alternative shape
When the consumers are internal services rather than browsers, gRPC is the common alternative: a contract-first RPC framework where `.proto` files define services and messages, and code is generated for clients and servers across languages. The gRPC docs describe it as "a modern open source high performance Remote Procedure Call (RPC) framework" built on HTTP/2 with protocol buffers as the interface definition language. For data serving the trade-off is that gRPC clients are heavier than a JSON-over-HTTP `fetch`, but the binary wire format and streaming support matter when latency and payload size dominate.
Ref: [gRPC — what is gRPC](https://grpc.io/docs/what-is-grpc/introduction/) · [gRPC — core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)

### Caching strategies
Three layers show up in practice, listed by proximity to the consumer: (1) **CDN** caching for responses that are identical across many callers — rare for authenticated data APIs, common for public aggregates; (2) **Redis** or a similar in-memory store, where the app writes results keyed by the query parameters and reads them back across processes; (3) **in-process** caches inside the API worker, the fastest but lost on restart and not shared between workers. The mental model is that each layer trades freshness and shareability for latency; pick the layer where the cost of a stale response is still acceptable.

### Query-serving engines — Trino, DuckDB
Two engines straddle the "is the warehouse enough" line in different ways. **Trino** is the interactive-analytics engine from Phase 3; it serves dashboards and ad-hoc analytics directly over the lakehouse without an extra store. **DuckDB** is an in-process OLAP engine that can be embedded directly in the API worker, which eliminates the network hop between app and query engine. DuckDB's docs describe it as an "in-process SQL OLAP database management system" that runs inside the calling process, which makes it a practical serving choice when the dataset fits the worker and the API can load Parquet directly.
Ref: [Trino overview — use cases](https://trino.io/docs/current/overview/use-cases.html) · [DuckDB — why DuckDB](https://duckdb.org/why_duckdb)

### Feature stores: online/offline split
A feature store is the ML-specific serving pattern: it manages features — transformations of raw data used as model inputs — so that training and inference see the *same* feature values. The Feast docs describe a feature store as a system that "manages the storage and serving of feature data" and split that storage into an **offline store** (for historical point-in-time retrieval during training) and an **online store** (for low-latency single-row reads during inference).
Ref: [Feast — introduction](https://docs.feast.dev/)

The hard problem is **point-in-time correctness**: when building a training set, each label row must join features using the values those features held *at the label's event timestamp*, not their current values — otherwise the model sees data from the future during training and collapses in production. Feast's docs make this explicit, describing point-in-time joins as the mechanism that "prevents feature leakage" by joining feature values only from before the event timestamp of each label row.
Ref: [Feast — concepts: point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

### Reverse ETL (mental model only)
Reverse ETL flips the pipeline direction: instead of pulling data from source systems into the warehouse, it pushes rows from the warehouse out into operational SaaS tools (CRM, marketing automation, support, ad platforms). The warehouse remains the source of truth; the SaaS tools become downstream sinks that are refreshed on a schedule. Functionally this is just another scheduled ELT job whose destination happens to be a vendor API rather than a table — the significance is organizational, not architectural: the analytics team's models become directly usable by the sales and marketing teams without a separate integration codebase. This module covers the mental model only; no hands-on.

### Rate limiting and auth basics
A read-only data API needs two controls the warehouse does not provide by default: **authentication** (who is calling) and **rate limiting** (how often any one caller may call). FastAPI does not ship a rate limiter in core; auth is handled through its security utilities, which cover OAuth2, API keys, and HTTP Basic through dependency-injected schemes that also appear in the generated OpenAPI.
Ref: [FastAPI — security intro](https://fastapi.tiangolo.com/tutorial/security/)

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| API p99 spikes when dashboard users run ad-hoc queries | App and BI share the same warehouse workers | Split into separate virtual warehouses / Trino resource groups or put a cache in front of the API | [Trino — resource groups](https://trino.io/docs/current/admin/resource-groups.html) |
| Training accuracy great, production accuracy poor | Training set built with current feature values instead of point-in-time joins | Rebuild training set through the feature store's point-in-time join API | [Feast — point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins) |
| `/docs` shows endpoints but request bodies are `{}` | Handler parameters typed as plain `dict` instead of Pydantic models | Declare Pydantic request/response models so FastAPI can emit schema | [FastAPI — request body](https://fastapi.tiangolo.com/tutorial/body/) |
| Reverse-ETL job updates 5M rows every run | Full-refresh push instead of change-only | Filter to rows changed since last run watermark before calling the SaaS API | *Fundamentals of Data Engineering*, Reis & Housley, Ch. 9 |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] List the four serving patterns and pick the right one for a given use case.
- [ ] State the rough latency cutoff where a dedicated serving store becomes worth its cost.
- [ ] Write a minimal FastAPI endpoint with a Pydantic response model and explain where its OpenAPI schema comes from.
- [ ] Explain online vs. offline feature stores and why point-in-time correctness matters.
- [ ] Describe reverse ETL in one sentence and name one tool category it replaces.

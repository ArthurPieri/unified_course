# Quiz — Module 07: Data Serving

10 multiple-choice questions. Answer key at the bottom.

---

**Q1.** Which of the following is *not* one of the four data-serving patterns covered in this module?

A. BI dashboards
B. Low-latency data APIs
C. Feature stores for ML
D. Change data capture from OLTP sources

---

**Q2.** A product team needs a user-facing search endpoint with a p99 latency budget of 50 ms. Which approach best matches the module's heuristic?

A. Query the lakehouse warehouse directly on each request.
B. Put a dedicated serving store (cache or serving DB) in front of the warehouse.
C. Run Trino with more workers until p99 drops below 50 ms.
D. Serve from the offline feature store.

---

**Q3.** In FastAPI, the OpenAPI schema visible at `/docs` is produced by:

A. A separate hand-written YAML file kept in sync with the code.
B. A CLI command the developer runs after each release.
C. Automatic generation from path operations and Pydantic type hints.
D. Parsing runtime request logs.

---

**Q4.** Pydantic models in a FastAPI endpoint serve two roles simultaneously. Which pair is correct?

A. Runtime validation and OpenAPI schema source.
B. Database migration and dependency injection.
C. Rate limiting and authentication.
D. Connection pooling and logging.

---

**Q5.** According to the Feast docs, a feature store is split into an offline store and an online store because:

A. The offline store is for backups and the online store is for production data.
B. Training needs historical point-in-time retrieval while inference needs low-latency single-row reads.
C. Compliance requires two copies of every feature.
D. Online stores cannot hold numeric features.

---

**Q6.** Point-in-time correctness matters in feature stores because without it:

A. Features cannot be joined to labels at all.
B. Training queries become too slow to run.
C. Training data leaks future feature values into the training set, which collapses in production.
D. Feature names collide across projects.

---

**Q7.** Reverse ETL is best described as:

A. A rollback mechanism for broken ELT pipelines.
B. Pushing warehouse rows into operational SaaS tools on a schedule.
C. A feature store that runs inference backward through a model.
D. Streaming CDC from the warehouse back into the OLTP source.

---

**Q8.** Which caching layer is *closest* to the API worker and loses its state on process restart?

A. CDN
B. Redis
C. In-process cache
D. Warehouse result cache

---

**Q9.** gRPC is positioned in the module as the right shape when:

A. The consumers are browsers loading a public dashboard.
B. The consumers are internal services and payload size / latency dominate.
C. Only when the data is smaller than 1 KB per call.
D. When no schema exists for the data.

---

**Q10.** The Trino documentation positions Trino primarily as a tool for:

A. Transactional OLTP workloads with millisecond writes.
B. Interactive analytic queries over large datasets.
C. Model training on GPUs.
D. Reverse-ETL delivery to SaaS tools.

---

## Answer key

1. **D** — CDC is a capture pattern, not a serving pattern. Serving patterns are dashboards, APIs, feature stores, reverse ETL. See module §"The four serving patterns".
2. **B** — Below the ~100 ms heuristic a dedicated serving store is appropriate; the warehouse direct-query path targets looser SLOs. See module §"When the warehouse is enough".
3. **C** — FastAPI auto-generates OpenAPI from path operations and type hints. Ref: [FastAPI — first steps](https://fastapi.tiangolo.com/tutorial/first-steps/).
4. **A** — Pydantic models validate at runtime and supply the schema FastAPI serializes into OpenAPI. Ref: [FastAPI — request body](https://fastapi.tiangolo.com/tutorial/body/).
5. **B** — Offline store = historical / training, online store = low-latency inference reads. Ref: [Feast — introduction](https://docs.feast.dev/).
6. **C** — Point-in-time joins prevent feature leakage from future values into training. Ref: [Feast — point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins).
7. **B** — Reverse ETL = scheduled pushes from warehouse into operational SaaS systems. Ref: *Fundamentals of Data Engineering*, Reis & Housley, Ch. 9.
8. **C** — In-process caches live inside the worker and are lost on restart; Redis and CDN are out-of-process. See module §"Caching strategies".
9. **B** — gRPC fits internal service-to-service calls where payload and latency matter. Ref: [gRPC — what is gRPC](https://grpc.io/docs/what-is-grpc/introduction/).
10. **B** — Trino is described as an engine for interactive analytic queries over large datasets. Ref: [Trino — overview / use cases](https://trino.io/docs/current/overview/use-cases.html).

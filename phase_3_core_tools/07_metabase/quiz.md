# Quiz — 07_metabase

8 multiple-choice questions. One correct answer each. Answers and citations at the bottom.

---

**1. In the Phase 3 stack, Metabase connects to Trino using which four connection fields (at minimum)?**

A. Host, port, database name, password
B. Host, port, catalog, schema
C. JDBC URL, API key, warehouse, role
D. Endpoint, access key, secret key, region

---

**2. You build a metric that requires a window function and a CTE. Which Metabase question type is the right choice?**

A. Simple question
B. Custom (GUI) question
C. Native SQL question
D. Dashboard card only

---

**3. A Metabase **model** is best described as:**

A. A machine-learning model trained on your data
B. A saved question (usually native SQL) exposed with typed columns so other questions can build on it as if it were a table
C. A dbt model imported into Metabase
D. A synonym for "dashboard"

---

**4. A dashboard filter applies to a card when:**

A. The card was created by the same user as the dashboard
B. The filter is mapped to a field (or native SQL template variable) on that card
C. The dashboard is marked "public"
D. The card and the filter live in the same collection

---

**5. After a successful nightly dbt build, a Metabase dashboard still shows yesterday's numbers. The most likely cause is:**

A. Trino query queue is full
B. A cached result is being served until its TTL expires — Metabase does not invalidate on upstream writes
C. The Iceberg snapshot is not visible to Trino yet
D. Metabase's application database is out of disk

---

**6. You want an analyst group to browse the data warehouse with the GUI builder but NOT write raw SQL. Which permission do you adjust?**

A. The collection permission on the "Analytics" collection
B. The **native query** permission on the `iceberg` database for that group
C. The dashboard-level view permission
D. The embedding permission

---

**7. Metabase drill-through on a chart does which of the following when a user clicks a bar?**

A. Opens the raw Trino Web UI for the underlying query
B. Opens the underlying question with the clicked dimension value added as a filter
C. Exports the row to CSV
D. Refreshes the cache

---

**8. One-line rule: use Trino (via Metabase) over Spark for a given workload when:**

A. The workload is a long, wide-shuffle batch rewrite of a large Iceberg partition
B. The workload needs Python UDFs
C. The workload is interactive SQL over already-shaped gold tables driving a dashboard
D. The workload is a machine-learning training job

---

## Answer key

1. **B** — Trino identifiers are `catalog.schema.table`; the Metabase Trino connection form asks for host, port, catalog, and schema (plus an optional user). Ref: [Metabase — Connecting databases](https://www.metabase.com/docs/latest/databases/connecting), [Metabase — Starburst / Trino driver](https://www.metabase.com/data_sources/starburst).

2. **C** — The GUI builder does not expose window functions and CTEs; drop into the native SQL editor. Ref: [Metabase — Native SQL editor](https://www.metabase.com/docs/latest/questions/native-editor/writing-sql).

3. **B** — A model is a saved question exposed as a reusable, typed "table" for downstream questions. Ref: [Metabase — Models](https://www.metabase.com/docs/latest/data-modeling/models).

4. **B** — Dashboard filters are wired by mapping the filter to a field or to a native SQL template variable on each card. Ref: [Metabase — Dashboard filters](https://www.metabase.com/docs/latest/dashboards/filters).

5. **B** — Metabase caches results by rendered SQL + parameters with a TTL; upstream changes do not invalidate the cache. Ref: [Metabase — Caching query results](https://www.metabase.com/docs/latest/configuring-metabase/caching).

6. **B** — The native query permission is a separate toggle from the "view data" permission and is the standard tightening point for analyst groups. Ref: [Metabase — Data permissions](https://www.metabase.com/docs/latest/permissions/data).

7. **B** — Drill-through opens the underlying question with the clicked dimension value added as a filter; the user can then inspect the rows. Ref: [Metabase — Dashboards](https://www.metabase.com/docs/latest/dashboards/introduction).

8. **C** — Trino is the interactive SQL engine; Metabase-driven dashboards over gold tables are exactly its sweet spot. Ref: [Trino use cases](https://trino.io/docs/current/overview/use-cases.html), `../02_trino/README.md` (three-line rule).

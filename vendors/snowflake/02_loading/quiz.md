# Module 02 — Quiz: Data Loading

10 questions. Key + citations at the bottom.

---

**1.** Which stage is created automatically for every Snowflake user and cannot be altered or dropped?
A. `@my_stage`
B. `@%my_table`
C. `@~`
D. An external stage

**2.** You run `COPY INTO sales FROM @stg/file.csv` twice. The second run loads zero rows. Why?
A. The warehouse cache blocks the second load.
B. COPY INTO's load metadata remembers already-loaded files for 64 days.
C. CSV files cannot be reloaded.
D. The result cache served the second COPY INTO.

**3.** Which file formats does `INFER_SCHEMA` support? (Select THREE)
A. CSV
B. Parquet
C. Avro
D. XML
E. ORC

**4.** You need sub-second row-level ingestion from a custom application you control. Which option is the idiomatic Snowflake choice?
A. Snowpipe with auto-ingest over S3
B. Snowpipe Streaming via the SDK
C. `INSERT ... VALUES` in a loop from a stored procedure
D. External table auto-refresh

**5.** Which object is the canonical way to grant Snowflake access to an external cloud bucket without embedding credentials?
A. External stage
B. Storage integration
C. Network policy
D. Secret

**6.** `COPY INTO sales FROM @stg FILE_FORMAT = (FORMAT_NAME = ff_csv) PURGE = TRUE;` What does `PURGE = TRUE` do?
A. Deletes source files after a successful load.
B. Deletes the target table before loading.
C. Drops load history.
D. Removes rows whose checksums mismatch.

**7.** A JSON file is a single top-level array of 1,000 objects. You `COPY INTO` a VARIANT column and get one row. What fixes it?
A. Add `STRIP_OUTER_ARRAY = TRUE` to the file format.
B. Use `INFER_SCHEMA`.
C. Switch to CSV.
D. Increase warehouse size.

**8.** Which function reports the current load state and last error for a pipe?
A. `SYSTEM$CLUSTERING_INFORMATION`
B. `SYSTEM$PIPE_STATUS`
C. `QUERY_HISTORY`
D. `LOAD_HISTORY`

**9.** True or False: Snowpipe auto-ingest requires you to size a dedicated warehouse.

**10.** Which of the following correctly describes the Kafka connector in "Snowpipe Streaming" mode?
A. It writes files to a stage that a Snowpipe then ingests.
B. It calls the Snowpipe Streaming SDK to insert rows with low latency.
C. It uses `COPY INTO` from a Kafka topic URL.
D. It requires a Dynamic Table as the target.

---

## Answer key

1. **C** — User stage `@~` is per-user, auto-created, not alterable. `domain_3_0_data_loading.md:L34, L41`.
2. **B** — Load metadata deduplication with a 64-day window. `domain_3_0_data_loading.md:L46`; [COPY INTO](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table).
3. **B, C, E** — INFER_SCHEMA supports Parquet, Avro, ORC. [INFER_SCHEMA](https://docs.snowflake.com/en/sql-reference/functions/infer_schema).
4. **B** — Snowpipe Streaming is the low-latency SDK path. *DEA Study Guide §1.4, p. 5*; [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview).
5. **B** — Storage integration holds the trust relationship. [CREATE STORAGE INTEGRATION](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration).
6. **A** — Deletes source files on success only. [COPY INTO](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table); `lab_02_data_loading.sql` PURGE example.
7. **A** — Classic STRIP_OUTER_ARRAY case. `domain_3_0_data_loading.md:L49`.
8. **B** — `SYSTEM$PIPE_STATUS`. [System pipe status](https://docs.snowflake.com/en/sql-reference/functions/system_pipe_status); *DEA Study Guide §1.3, p. 5*.
9. **False** — Snowpipe is serverless; billed in credits, no warehouse sizing. [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro).
10. **B** — Kafka connector can delegate to the Streaming SDK for row-level latency. [Kafka connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview); *DEA Study Guide §1.4, p. 5*.

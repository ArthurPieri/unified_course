# Module 02 Quiz — Ingestion

10 questions. Answer key below.

---

**Q1.** A workload requires sub-second end-to-end latency, three independent consumer applications each reading the full stream, and 7-day replay. Which service fits best?

- A) Amazon Data Firehose to S3
- B) Amazon Kinesis Data Streams with enhanced fan-out
- C) Amazon SQS standard queue
- D) AWS Glue streaming job

**Q2.** Which statement about Amazon Data Firehose is correct?

- A) It guarantees sub-100 ms delivery latency.
- B) It can convert incoming JSON to Apache Parquet using a referenced Glue table schema.
- C) It natively writes to DynamoDB.
- D) It requires you to manage shards.

**Q3.** A Kinesis Data Streams producer calls `PutRecords` and receives a 200 response. What must the producer still check?

- A) Nothing — 200 means all records are durable.
- B) `FailedRecordCount`, and retry the records flagged with error codes.
- C) The CloudWatch alarm named `FailedRecords`.
- D) The shard iterator age.

**Q4.** You must migrate 800 TB of on-prem NAS files to S3 with the least wall-clock time across a 1 Gbps link that is often saturated. Which service?

- A) DataSync on a schedule
- B) AWS Snowball Edge Storage Optimized
- C) S3 Transfer Acceleration multipart uploads from a script
- D) AppFlow

**Q5.** Which AWS service is the canonical answer for ongoing CDC replication from an on-prem Oracle database to Amazon Redshift?

- A) Glue Crawlers
- B) AppFlow
- C) AWS DMS
- D) S3 Batch Replication

**Q6.** What is the minimum buffer interval for Firehose delivery to S3 (per the service defaults)?

- A) 0 seconds
- B) 60 seconds
- C) 5 minutes
- D) 15 minutes

**Q7.** A Glue ETL job on a JSON source has a field `discount` that appears sometimes as a float and sometimes as a string. Which Glue primitive resolves this?

- A) Spark DataFrame `cast`
- B) Glue DynamicFrame `ResolveChoice`
- C) Glue Crawler classifier
- D) Lake Formation column filter

**Q8.** MSK Serverless supports which authentication mechanism?

- A) SASL/SCRAM only
- B) mTLS only
- C) IAM access control only
- D) Open (no auth)

**Q9.** Which Glue feature enables incremental processing by tracking data already processed across job runs?

- A) Job bookmarks
- B) Continuations API
- C) Glue Workflows
- D) Glue Triggers

**Q10.** A KDS stream is throttling on one shard while nine other shards are idle. The most likely root cause is:

- A) Insufficient total shard capacity
- B) Hot partition key causing skew
- C) Enhanced fan-out disabled
- D) Consumer lag

---

## Answer key

1. **B** — KDS with enhanced fan-out gives per-consumer 2 MiB/s and sub-second latency with configurable retention up to 365 days. [KDS enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html).
2. **B** — Firehose supports record format conversion from JSON to Parquet/ORC via a Glue table reference. [Firehose record format conversion](https://docs.aws.amazon.com/firehose/latest/dev/record-format-conversion.html).
3. **B** — `PutRecords` can partially fail; always inspect `FailedRecordCount` and retry. [PutRecords API](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html).
4. **B** — Offline Snowball Edge for 800 TB over a saturated 1 Gbps link. [Snow Family](https://docs.aws.amazon.com/snowball/latest/ug/whatisdevice.html).
5. **C** — DMS full load + CDC. [DMS CDC](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html).
6. **B** — 60 seconds (minimum buffer interval; minimum buffer size 1 MiB). [Firehose buffering](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html).
7. **B** — DynamicFrame `ResolveChoice`. [DynamicFrame ResolveChoice](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html).
8. **C** — MSK Serverless supports IAM access control only. [MSK Serverless](https://docs.aws.amazon.com/msk/latest/developerguide/serverless.html).
9. **A** — Job bookmarks. [Glue job bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html).
10. **B** — Hot partition key. [KDS partition keys](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html).

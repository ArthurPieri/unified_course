# Module 02: Ingestion — Glue, DMS, DataSync, AppFlow, Kinesis, MSK (28h)

> Part of Domain 1 (**34%** of scored content — the largest on the exam). *AWS DEA-C01 Exam Guide, Content outline*.

## Learning goals

- Pick between KDS, Kinesis Data Firehose, and MSK for a given latency, throughput, retention, and processing requirement. *Skill 1.1.1*.
- Use DMS full-load + CDC to move a relational source to S3, Redshift, or another database. *Skill 1.1.1 + 1.1.2*.
- Use DataSync or Snow Family for bulk/offline migrations and decide between them. *Skill 2.1.4*.
- Configure AppFlow for SaaS-to-S3 ingestion with schedule and filter. *Skill 1.1.2*.
- Throttle and handle rate limits for DynamoDB, RDS, Kinesis. *Skill 1.1.9*.
- Explain replayability, fan-in/fan-out, stateful vs. stateless transactions. *Skill 1.1.10-1.1.12*.

## Exam weight

Task 1.1 (Perform data ingestion) and Task 1.2 (Transform and process data) together dominate the 34% Domain 1 weighting. *Exam Guide, Content Domain 1*.

## Key services and primary docs

| Service | What to know | AWS doc |
|---|---|---|
| Amazon S3 (as sink) | Multipart upload, event notifications, Transfer Acceleration | [S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html) |
| AWS DMS | Full load + CDC; sources (Oracle, SQL Server, MySQL, PostgreSQL, Mongo); targets (S3, Redshift, Kinesis, Kafka) | [DMS User Guide](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html) |
| AWS DataSync | Online bulk transfer, NFS/SMB/S3/HDFS | [DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html) |
| AWS Snow Family | Offline bulk transfer (TBs-PBs); Snowcone, Snowball Edge, Snowmobile | [Snow Family](https://docs.aws.amazon.com/snowball/latest/ug/whatisdevice.html) |
| Amazon AppFlow | SaaS-to-AWS managed ingestion (Salesforce, Google Analytics, ServiceNow, Slack...) | [AppFlow User Guide](https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html) |
| Amazon Kinesis Data Streams (KDS) | Shards, partition keys, sub-second reads, retention 1-365 days, KCL/enhanced fan-out | [KDS Developer Guide](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) |
| Amazon Data Firehose | Near-real-time delivery to S3/Redshift/OpenSearch/Splunk; buffering, Parquet conversion, Lambda transforms | [Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html) |
| Amazon MSK | Managed Kafka; Provisioned and Serverless; MSK Connect | [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html) |
| AWS Glue ETL | Spark/Python jobs, crawlers, DynamicFrames, job bookmarks | [AWS Glue Dev Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) |
| AWS Glue DataBrew | Visual data prep, ~250 built-in transforms, DQ rules | [Glue DataBrew](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html) |

## Concepts (compact)

### KDS vs. Firehose vs. MSK — the decision you must get right
- **KDS**: you manage shards (or use on-demand), pay per shard-hour + PUT payload units, get sub-second latency, 1-365 day retention, and write custom consumers (KCL, Lambda, enhanced fan-out). Use when you need replay or multiple independent consumers at low latency.
- **Firehose**: fully managed, near-real-time (60s+ buffering), buffers to S3/Redshift/OpenSearch/Splunk, can convert JSON->Parquet using a Glue table, and supports Lambda record transforms. Use when your destination is one of those four and you do not need sub-second latency.
- **MSK**: managed Apache Kafka. Choose over KDS when you need Kafka APIs, long-lived consumer groups across partitions, exactly-once via Kafka transactions, or ecosystem integrations (Kafka Connect, Debezium, ksqlDB).
Primary: [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/latest/dev/), [Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html), [Amazon MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/).

### Shards, partition keys, throttling
KDS shards cap at 1 MiB/s or 1000 records/s writes and 2 MiB/s reads (shared) or per-consumer with Enhanced Fan-Out. Hot-key skew = one shard throttles while others idle; fix with a higher-cardinality partition key. DynamoDB hot partitions throttle similarly — use adaptive capacity + better partition key design. Primary: [KDS key concepts](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html), [KDS enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html).

### DMS full load + CDC
DMS runs a full load then switches to CDC reading the source WAL/binlog. To S3 target, DMS lands CDC as a "cdc" file stream that you post-process (Glue/EMR) into a Bronze table. DMS Schema Conversion / SCT is the exam answer for heterogeneous migrations. *Skill 2.4.3*. Primary: [AWS DMS User Guide](https://docs.aws.amazon.com/dms/latest/userguide/), [DMS CDC](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html).

### DataSync vs. Snow Family
DataSync is online (network-bound), one-time or scheduled, handles NFS/SMB/HDFS/S3/EFS/FSx. Snow Family is offline (ship a device) — use it when you have petabytes or no link. Primary: [AWS DataSync User Guide](https://docs.aws.amazon.com/datasync/latest/userguide/), [AWS Snow Family](https://docs.aws.amazon.com/snowball/latest/ug/whatisdevice.html).

### AppFlow
Bidirectional managed connectors between SaaS apps and AWS (S3, Redshift). Supports schedule-based and event-based triggers, field-level filtering and masking. Primary: [Amazon AppFlow User Guide](https://docs.aws.amazon.com/appflow/latest/userguide/what-is-appflow.html).

### Glue ETL job primitives
DynamicFrame handles schema inconsistencies that break DataFrames. Job bookmarks provide incremental processing by tracking processed paths. Worker types (G.1X, G.2X, G.025X, Flex) trade cost vs. runtime. Primary: [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/), [Glue DynamicFrames](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html), [Glue job bookmarks](https://docs.aws.amazon.com/glue/latest/dg/monitor-continuations.html).

### Replayability and stateful/stateless
Replayability = the ability to re-read historical events (KDS retention window, Firehose destination backup, MSK log retention). Stateful transactions require windowing and checkpointing (Flink, Spark Structured Streaming). Stateless = map/filter only. *Skill 1.1.11-1.1.12*.

## Labs

See the hands-on labs in this module's labs/ directory. Key exercises:

| Lab | Goal | AWS reference |
|---|---|---|
| Ingestion fundamentals | Buckets, DMS-style workflow on LocalStack | [AWS DMS User Guide](https://docs.aws.amazon.com/dms/latest/userguide/), [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/) |
| Streaming | KDS produce/consume, Firehose to S3, PutRecords partial failure handling | [Amazon Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/latest/dev/), [Amazon Data Firehose](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html) |
| Glue ETL | JSON->Parquet, DynamicFrame, ResolveChoice, job bookmarks | [AWS Glue ETL](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl.html), [Glue DynamicFrames](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html) |

## Common exam gotchas

| Gotcha | Why it trips people | Reference |
|---|---|---|
| Firehose "real-time" | Minimum buffer is 60s (S3) / 0s special cases — not sub-second | [Firehose delivery stream settings](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html) |
| `PutRecords` partial failure | API returns 200 even when some records fail; always check `FailedRecordCount` and retry | [PutRecords API](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecords.html) |
| KDS hot shard | Partition key skew, not total throughput, is usually the culprit | [KDS partition keys](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html) |
| DMS CDC on S3 target | Produces change-event files; not a query-ready Iceberg table by itself | [DMS S3 target](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html) |
| MSK vs. MSK Serverless IAM | Serverless only supports IAM auth; Provisioned supports IAM, SASL/SCRAM, mTLS | [MSK authentication](https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html) |
| Enhanced fan-out | Per-consumer 2 MiB/s dedicated throughput; extra cost | [KDS enhanced fan-out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] You can draw the KDS vs. Firehose vs. MSK decision tree from memory.
- [ ] You can explain when DMS to S3 target needs post-processing and why.
- [ ] You can configure a Glue job with bookmarks and understand when bookmarks fail (schema drift).

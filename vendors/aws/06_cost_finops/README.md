# Module 06: AWS Cost / FinOps (8h)

> Cross-cutting. Directly maps to *Exam Guide, Skill 1.2.4* "Optimize costs while processing data" and recurs in every store-selection and compute-sizing question.

## Learning goals

- Identify the dominant cost lever for each major service (S3, Athena, Glue, EMR, Redshift, Kinesis, MSK, DynamoDB). *Skill 1.2.4, 3.2.5*.
- Choose storage class, query engine, and compute model to meet a cost target without missing an SLA.
- Apply partitioning, columnar formats, and compression to cut scan-based billing. *Skill 2.4.5*.
- Use Spot, Savings Plans, Reserved capacity, and auto-scaling appropriately.
- Monitor cost with Cost Explorer, AWS Budgets, and service-specific workgroups/limits.

## Exam weight

Domain 1 explicitly calls out cost optimization (Skill 1.2.4). Domain 3 covers provisioned vs. serverless trade-offs (Skill 3.2.5). Cost appears as a decision driver in nearly every scenario question. *AWS DEA-C01 Exam Guide*.

## Cost levers by service (the table to memorize)

| Service | Primary billing dimension | Biggest lever | Primary doc |
|---|---|---|---|
| S3 | Storage class x GB-month + request counts + data transfer | Lifecycle to IA/Glacier; Intelligent-Tiering for unknown patterns | [S3 pricing](https://aws.amazon.com/s3/pricing/) |
| Athena | Bytes scanned (per TB) | Partitioning, columnar formats, column pruning, query result reuse, workgroup data-scanned limits | [Athena pricing](https://aws.amazon.com/athena/pricing/) · [Workgroups](https://docs.aws.amazon.com/athena/latest/ug/workgroups.html) |
| Glue ETL | DPU-hours | Right-size worker type; use Flex execution class; shorten runtime | [Glue pricing](https://aws.amazon.com/glue/pricing/) |
| EMR | EC2 instance-hours + EMR markup | Spot for task nodes, managed scaling, EMR Serverless for bursty, EMR on EKS to share | [EMR pricing](https://aws.amazon.com/emr/pricing/) |
| Redshift Provisioned | Node-hours + managed storage (RA3) | RA3 + Pause/Resume, Concurrency Scaling credits, Reserved Instances | [Redshift pricing](https://aws.amazon.com/redshift/pricing/) |
| Redshift Serverless | RPU-seconds | Set base RPU floor, max RPU ceiling, query monitoring rules | [Redshift Serverless pricing](https://aws.amazon.com/redshift/pricing/#Amazon_Redshift_Serverless) |
| Kinesis Data Streams | Shard-hours + PUT payload units + retention extension | On-demand mode for spiky workloads; right-size shards in provisioned | [KDS pricing](https://aws.amazon.com/kinesis/data-streams/pricing/) |
| Data Firehose | GB ingested + optional format conversion + delivery | Use Parquet conversion at ingest to cut downstream Athena scans | [Firehose pricing](https://aws.amazon.com/firehose/pricing/) |
| MSK | Broker-hour + storage | Serverless for variable workloads; tiered storage for long retention | [MSK pricing](https://aws.amazon.com/msk/pricing/) |
| DynamoDB | On-demand (per-request) or Provisioned (RCU/WCU) + storage | Right-size capacity; use Infrequent Access table class; TTL expiration | [DynamoDB pricing](https://aws.amazon.com/dynamodb/pricing/) |
| Lambda | Per-request + GB-seconds | Memory tuning, ARM Graviton, provisioned concurrency only where needed | [Lambda pricing](https://aws.amazon.com/lambda/pricing/) |

## Concepts (compact)

### Partition, project, compress — the Athena trinity
Athena charges per TB scanned. Partitioning prunes unread objects; Parquet/ORC column pruning reads only required columns; Snappy/ZSTD compression cuts remaining bytes. The combined effect is often 10-100x cost reduction vs. raw JSON. Primary: [Athena performance tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html). See also [Athena partitions](https://docs.aws.amazon.com/athena/latest/ug/partitions.html).

### Storage class strategy
Use S3 Intelligent-Tiering when access patterns are unknown or unpredictable; use explicit Lifecycle transitions when the pattern is known (e.g., compliance logs). Deep Archive is cheapest but has retrieval latency. Primary: [Using Amazon S3 storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html), [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).

### Serverless vs. provisioned trade-off
Serverless (Redshift Serverless, Glue, Athena, EMR Serverless, Firehose) wins on bursty / intermittent / unpredictable workloads and on team agility. Provisioned (Redshift RA3, EMR, MSK Provisioned) wins on steady high-utilization workloads with Reserved Instances or Savings Plans. *Exam Guide, Skill 3.2.5*.

### Spot for EMR task nodes
Task nodes tolerate interruption; use Spot with instance fleets and allocation strategy = `lowestPrice` or `capacityOptimized`. Core nodes run HDFS/local shuffle — keep them On-Demand unless Spot interruption is acceptable. Primary: [EMR instance fleets](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html), [EMR managed scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-managed-scaling.html).

### Cost control guardrails
- Athena workgroups enforce per-query and per-workgroup data-scanned limits.
- AWS Budgets sends alerts at thresholds (80%, 100%, forecasted).
- Cost Explorer groups spend by tag, service, or linked account.
- Glue DataBrew / Glue Studio show DPU estimates before running.

### FinOps cross-service patterns
- Land raw data in S3 Standard; transform to Parquet + partition into curated; apply Lifecycle on raw.
- Prefer Firehose Parquet conversion at ingest over downstream Glue conversion.
- For one-shot analytics, Athena beats loading into Redshift.
- For high-QPS BI dashboards, load hot subset into Redshift; keep cold data in S3 and query via Spectrum.

Primary: [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) — the cross-domain architecture patterns are the single best read for FinOps thinking.

## Labs

See the hands-on labs in this module's labs/ directory. Key exercises:

| Lab | Goal | AWS reference |
|---|---|---|
| Lifecycle | Lifecycle rules that move cold data to IA/Glacier | [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) |
| Capstone -- cost-aware pipeline | End-to-end with Firehose Parquet conversion and partitioned S3 | [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) |

## Common exam gotchas

| Gotcha | Why it trips people | Reference |
|---|---|---|
| CSV + Athena | Full-row read, no column pruning — 10-100x more cost than Parquet | [Athena tuning](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html) |
| Missing partitions | `MSCK REPAIR` or partition projection required; full-table scan otherwise | [Athena partitions](https://docs.aws.amazon.com/athena/latest/ug/partitions.html) |
| Always-on EMR for weekly jobs | Use EMR Serverless or Glue Flex instead | [EMR Serverless](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html) |
| Redshift provisioned for sporadic workloads | Pause/Resume or move to Serverless | [Redshift Serverless](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html) |
| KDS provisioned for spiky streams | On-demand mode scales automatically | [KDS on-demand mode](https://docs.aws.amazon.com/streams/latest/dev/how-do-i-size-a-stream.html) |
| DynamoDB over-provisioning | Switch to on-demand or tune capacity with auto-scaling | [DynamoDB capacity modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] Given a workload (size, frequency, SLA), you can name the dominant cost lever and the first optimization to try.
- [ ] You can estimate Athena cost from a query's `Data scanned` metric.
- [ ] You can decide between Glue Flex, EMR Serverless, and EMR on EC2 for a bursty weekly job.

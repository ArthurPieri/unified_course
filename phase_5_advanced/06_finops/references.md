# References — 06 FinOps

## Primary framework
- [FinOps Framework — Overview](https://www.finops.org/framework/) — definition, principles, capabilities map.
- [FinOps Framework — Phases](https://www.finops.org/framework/phases/) — Inform, Optimize, Operate lifecycle.
- [FinOps Framework — Capability: Allocation](https://www.finops.org/framework/capabilities/allocation/) — tagging, account/project structure, hierarchies.
- [FinOps Framework — Capability: Chargeback & Finance Integration](https://www.finops.org/framework/capabilities/chargeback-finance-integration/) — showback vs. chargeback.
- [FinOps Framework — Capability: Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/) — cost per business unit.
- [FinOps Framework — Capability: Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/) — commitments, discounts, egress considerations.
- [FinOps Framework — Capability: Workload Optimization](https://www.finops.org/framework/capabilities/workload-optimization/) — rightsizing, auto-suspend, idle detection.
- [FinOps Framework — Capability: Anomaly Management](https://www.finops.org/framework/capabilities/anomaly-management/) — anomaly detection vs. static thresholds.

## AWS cost and optimization docs
- [AWS EMR — Instance purchasing options](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-purchasing-options.html) — EMR vs. Glue cost model, spot savings up to ~90%.
- [AWS Kinesis Data Streams — Pricing](https://aws.amazon.com/kinesis/data-streams/pricing/) — Kinesis/Firehose/MSK retention and per-shard cost lines.
- [AWS — EBS pricing](https://aws.amazon.com/ebs/pricing/) — S3 vs. EBS vs. EFS per-GB storage cost comparison.
- [AWS Glue — Pricing](https://aws.amazon.com/glue/pricing/) — compute engine cost models (Lambda, Glue, Batch, ECS).
- [AWS — Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html) — cost-effective reservation strategies.
- [AWS Glue — Reading input files in larger groups](https://docs.aws.amazon.com/glue/latest/dg/grouping-input-files.html) — `groupFiles=inPartition` fix for the small-files problem.

## Canonical book
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 4 — cost and the data engineering lifecycle; TCO vs. TVO framing.

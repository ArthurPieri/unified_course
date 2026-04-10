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

## Sibling sources
- `../aws_certified/docs/week-11-cross-domain.md:L489-L497` — EMR vs. Glue cost model, spot savings up to ~90%, cost-optimize signals.
- `../aws_certified/docs/week-11-cross-domain.md:L510-L542` — Kinesis/Firehose/MSK retention and per-query Athena/Redshift cost lines.
- `../aws_certified/docs/week-11-cross-domain.md:L574-L580` — S3 vs. EBS vs. EFS per-GB storage cost comparison.
- `../aws_certified/docs/week-11-cross-domain.md:L661-L680` — compute engine cost models (Lambda, Glue, Batch, ECS) and Athena vs. CloudWatch Logs Insights cost signals.
- `../aws_certified/docs/week-11-cross-domain.md:L717-L754` — exam-signal phrasing for cost-effective / small-files / query-cost optimisation.
- `../aws_certified/docs/week-11-cross-domain.md:L919-L933` — worked example: 500 GB / 500,000 files Glue job fixed with `groupFiles=inPartition`.

## Canonical book
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 4 — cost and the data engineering lifecycle; TCO vs. TVO framing.

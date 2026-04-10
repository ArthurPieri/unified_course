# Module 06: FinOps for Data Platforms (6h)

> FinOps is the discipline of managing cloud cost as a cross-functional practice shared between engineering, finance, and product. This module covers the framework, the levers that matter for data workloads, and how to monitor cost as an engineering signal.

## Learning goals
- Define FinOps and name its three phases.
- Build a cost allocation strategy using tags and account structure; distinguish chargeback from showback.
- Compute unit economics for a data workload (cost per query, per GB ingested, per dbt model run).
- Identify the top cost levers for storage, compute, and network in a modern data stack.
- Decide when reserved capacity beats on-demand, and when it does not.
- Set up cost monitoring that alerts on anomalies instead of static thresholds.

## Prerequisites
- `../04_cloud_concepts/` (on-demand pricing, service models)
- `../05_iam_primer/` (tag-based policies underpin tag-based cost allocation)

## Reading order
1. This README
2. `quiz.md`

## Concepts

### What FinOps is
FinOps is defined by the FinOps Foundation as "an operational framework and cultural practice which maximizes the business value of cloud... through collaboration between engineering, finance, and business teams." It is **not** cost-cutting; it is making cost a first-class engineering signal that teams optimise alongside latency and reliability. The outputs are decisions — "we will migrate this table to a colder storage class" — not spreadsheets. Ref: [FinOps Framework — Overview](https://www.finops.org/framework/).

### The three phases: Inform → Optimize → Operate
The FinOps Framework describes a lifecycle every workload moves through continuously. **Inform** means making cost visible to the teams who create it: tagging, dashboards, forecasts, shared reports. **Optimize** means acting on that visibility: rightsizing, tiering, committing to reservations, killing idle resources. **Operate** means embedding FinOps into the day-to-day: targets, policies, automation, anomaly detection. Teams revisit all three phases constantly — a new workload starts at Inform, a mature one spends most of its time in Operate but returns to Optimize whenever patterns change. Ref: [FinOps Framework — Phases](https://www.finops.org/framework/phases/).

### Cost allocation: tagging and account structure
You cannot optimise what you cannot attribute. Two mechanisms work together: **tags** (key-value pairs on resources — `env=prod`, `team=analytics`, `cost_center=1234`, `workload=etl`) and **account or project structure** (separate AWS accounts, Azure subscriptions, or GCP projects per team or environment). Account boundaries are the only guarantee that a runaway workload cannot appear on someone else's bill; tags are the flexible layer on top. The hard part is **enforcement** — untagged resources must be blocked at creation time (SCPs, Azure Policy, GCP Organization Policy), not detected after the fact. Ref: [FinOps Framework — Capability: Allocation](https://www.finops.org/framework/capabilities/allocation/).

### Chargeback vs. showback
**Showback** sends each team a report of what they spent but does not move money. **Chargeback** actually bills the team's P&L. Showback is faster to implement and creates awareness without finance friction; chargeback creates accountability but requires accurate allocation (otherwise teams dispute the bill). Most organisations start with showback, gain confidence in the numbers, and graduate to chargeback once allocation is trusted. Ref: [FinOps Framework — Capability: Chargeback & Finance Integration](https://www.finops.org/framework/capabilities/chargeback-finance-integration/).

### Unit economics
Raw dollar spend is noise; the signal is **cost per unit of business value**. For data platforms the useful units are:
- Cost per query (warehouse bill ÷ query count)
- Cost per GB ingested (pipeline bill ÷ bytes landed)
- Cost per dbt model run (compute bill ÷ model executions)
- Cost per active dashboard user (BI bill ÷ DAU)
Unit economics make cost comparable across time as volume grows. A warehouse bill that doubled while queries tripled is getting cheaper, not more expensive. Ref: [FinOps Framework — Capability: Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/).

### Top cost levers for data workloads
Five levers cover most of the savings on a typical data platform:

1. **Storage class tiering.** S3 Standard → Standard-IA → Glacier Instant → Glacier Deep Archive. Cold data that is read rarely belongs in a colder tier; the break-even is usually weeks, not months. Use lifecycle rules, not manual moves.
2. **Spot / preemptible compute for stateless jobs.** Batch Spark, Glue on G.1X, EMR task nodes, Kubernetes batch workers — all can run on spot with up to ~90% savings. `../aws_certified/docs/week-11-cross-domain.md:L489-L497` notes EMR spot can save "up to 90%" and flags "cost-optimize with spot" as an exam signal for EMR over Glue.
3. **Auto-suspend warehouses.** Snowflake, BigQuery BI Engine, Redshift Serverless, Databricks SQL warehouses all support automatic suspension after N seconds of idle. For interactive workloads this single setting routinely cuts bills 40–60%.
4. **Query result caching.** Repeated identical queries should hit a cache, not recompute. Most warehouses cache automatically; the engineering work is making sure your BI tool reuses them (consistent filters, parameter binding, no `now()` in WHERE clauses).
5. **File sizing — the small-files problem.** Thousands of tiny files destroy performance and cost because each one costs an S3 GET/HEAD API call and serialisation overhead. Target 128 MB–1 GB Parquet files. `../aws_certified/docs/week-11-cross-domain.md:L739` lists "small files problem" with fixes: Glue file grouping, Firehose buffering, Athena CTAS. Worked example: a 500,000-file / 500 GB Glue job resolved by `groupFiles=inPartition` at `../aws_certified/docs/week-11-cross-domain.md:L919-L933`.

### Reserved capacity vs. on-demand
Reservations (AWS Reserved Instances / Savings Plans, Azure Reserved VM Instances, GCP Committed Use Discounts, Snowflake pre-purchased capacity) trade flexibility for discount — typically 30–70% off on-demand in exchange for a 1- or 3-year commitment. The rule of thumb: **commit only to the baseline you are certain to consume.** Use on-demand or spot for the bursty layer on top. Reservations should cover the bottom of your daily usage curve; never buy to cover the peak. `../aws_certified/docs/week-11-cross-domain.md:L717` frames "most cost-effective" exam prompts around pay-per-use and on-demand for variable load, reservations for stable load.

### Egress is the silent killer
Inbound data transfer is usually free. **Outbound** transfer — cross-region, cross-AZ, cross-cloud, and especially out to the internet — is one of the most consistently underestimated line items on a cloud bill. Design data flows to keep compute, storage, and consumers in the same region whenever possible. A single cross-region replication job moving 100 TB/month can cost more than the warehouse it feeds. If you must move data between clouds, batch it, compress it, and consider direct-connect services rather than public egress. Ref: [FinOps Framework — Capability: Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/).

### Monitoring cost like any other SLI
Treat monthly cost as a time series and alert on **anomalies**, not absolute thresholds. A fixed "alert at $10k" threshold either fires constantly (if the baseline is close to it) or hides a runaway job (if the baseline is far below). Anomaly detection — deviation from the 7-day or 28-day trend for the same tag scope — catches the runaway Spark job that leaked overnight without paging on expected month-end batch spikes. AWS Cost Anomaly Detection, Azure Cost Management anomaly alerts, and GCP recommender all provide this; the engineering work is wiring the alerts to the team that owns the tag, not a central FinOps inbox. Ref: [FinOps Framework — Capability: Anomaly Management](https://www.finops.org/framework/capabilities/anomaly-management/).

## Labs
_No lab for this module — the assignment is to apply the levers to an existing workload you own. A guided audit worksheet may be added later._

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Bill up 30% month-over-month, nobody knows why | No unit economics; absolute dollars hide the real story | Divide by queries / GB / DAU and re-examine | [FinOps Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/) |
| Cost allocation report has a large "untagged" bucket | No tag enforcement at resource creation | Require tags via SCP / Azure Policy / Org Policy | [FinOps Allocation](https://www.finops.org/framework/capabilities/allocation/) |
| Glue/Spark job blows up memory and runtime on small files | Thousands of <10 MB input files | Enable `groupFiles=inPartition`, compact upstream, Firehose buffering | `../aws_certified/docs/week-11-cross-domain.md:L919-L933` |
| Warehouse bill flat despite low usage | Auto-suspend not configured or set too high | Set idle timeout to 60 s for dev, 5–10 min for prod BI | [FinOps Workload Optimization](https://www.finops.org/framework/capabilities/workload-optimization/) |
| Reservation utilisation below 70% | Over-committed; covered burst instead of baseline | Reduce commitment scope at renewal; keep baseline only | `../aws_certified/docs/week-11-cross-domain.md:L717` |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Explain FinOps to a product manager in three sentences.
- [ ] Describe what each of Inform, Optimize, and Operate produces as an output.
- [ ] Propose a tag schema for a data platform with three teams and two environments.
- [ ] Compute at least one unit-economic metric for a workload you own.
- [ ] List the five top cost levers for data workloads and one example for each.
- [ ] Decide whether a given workload should run on reserved, on-demand, or spot.
- [ ] Configure an anomaly-based cost alert scoped to a tag.

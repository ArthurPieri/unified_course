# Quiz — 06 FinOps

8 multiple-choice questions. Answer key at the bottom.

---

**1.** How does the FinOps Foundation define FinOps?
- A) A cost-cutting initiative run by finance
- B) An operational framework and cultural practice that maximises the business value of cloud through collaboration between engineering, finance, and business teams
- C) A set of AWS-specific billing tools
- D) A procurement process for cloud contracts

**2.** What are the three phases of the FinOps Framework?
- A) Plan, Build, Run
- B) Inform, Optimize, Operate
- C) Measure, Commit, Renew
- D) Tag, Alert, Report

**3.** A team wants accountability without moving money between P&Ls. Which approach fits?
- A) Chargeback
- B) Showback
- C) Reservation pooling
- D) Egress waivers

**4.** Why are unit economics more useful than absolute monthly spend?
- A) They are required by GAAP
- B) They normalise cost by business volume so trends are comparable as usage grows
- C) They eliminate the need for tagging
- D) They always decrease over time

**5.** Which combination is the most reliable cost lever for an interactive BI warehouse?
- A) Buy a 3-year reservation covering peak usage
- B) Aggressive auto-suspend plus query result caching
- C) Move all storage to Glacier Deep Archive
- D) Disable all caching to reduce stale-data risk

**6.** A Glue job reads 500,000 JSON files averaging 1 MB each from S3 and runs for hours. What is the most direct fix?
- A) Increase worker count
- B) Enable `groupFiles=inPartition` to merge small files on read
- C) Convert the sink to CSV
- D) Move the bucket to another region

**7.** When does a reserved / committed-use purchase make sense?
- A) For workloads whose usage is highly variable day-to-day
- B) For the stable baseline portion of a workload you are confident you will consume for the full term
- C) For dev/test environments used sporadically
- D) Never — on-demand is always cheaper

**8.** Which cost alerting strategy scales best across dozens of teams?
- A) A single fixed dollar threshold at the account level
- B) Anomaly detection scoped per tag, routed to the owning team
- C) Monthly email review by a central FinOps inbox
- D) No alerts; rely on end-of-month invoices

---

## Answer key

1. **B** — FinOps Foundation definition. Ref: [FinOps Framework Overview](https://www.finops.org/framework/).
2. **B** — Inform → Optimize → Operate. Ref: [FinOps Framework Phases](https://www.finops.org/framework/phases/).
3. **B** — Showback creates visibility without billing the P&L. Ref: [FinOps Chargeback & Finance Integration](https://www.finops.org/framework/capabilities/chargeback-finance-integration/).
4. **B** — Unit economics normalise for volume. Ref: [FinOps Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/).
5. **B** — Auto-suspend plus caching target the dominant costs of an interactive warehouse. Ref: [FinOps Workload Optimization](https://www.finops.org/framework/capabilities/workload-optimization/).
6. **B** — `groupFiles=inPartition` is the documented fix for the small-files problem. Ref: [AWS Glue — Reading input files in larger groups](https://docs.aws.amazon.com/glue/latest/dg/grouping-input-files.html).
7. **B** — Commit only to the certain baseline. Ref: [FinOps Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/); [AWS — Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html).
8. **B** — Anomaly detection per tag routed to owners. Ref: [FinOps Anomaly Management](https://www.finops.org/framework/capabilities/anomaly-management/).

# Checkpoint Q5 — Phase 5 Exit Quiz (20 questions)

Pass = 16/20. Roughly even coverage of the seven Phase 5 modules (01 CI/CD, 02 Kubernetes, 03 Airflow, 04 Cloud concepts, 05 IAM primer, 06 FinOps, 07 Data serving). Every answer cites a primary source.

---

**Q1.** (01 CI/CD) In GitHub Actions, the unit that executes a set of steps on a single runner is called:

A. A pipeline
B. A job
C. A workflow
D. A stage

---

**Q2.** (01 CI/CD) A dbt CI pipeline for a pull request typically runs which command to build only changed models and their downstream dependents?

A. `dbt run --full-refresh`
B. `dbt build --select state:modified+ --defer --state <artifacts>`
C. `dbt test --all`
D. `dbt seed`

---

**Q3.** (01 CI/CD) In a GitHub Actions workflow file, the top-level `on:` key defines:

A. The runner operating system
B. The events that trigger the workflow
C. The environment variables
D. The concurrency group

---

**Q4.** (02 Kubernetes) The smallest deployable unit in Kubernetes is:

A. A container
B. A pod
C. A node
D. A deployment

---

**Q5.** (02 Kubernetes) A Kubernetes Service of type `ClusterIP`:

A. Exposes the service on each node's IP at a static port.
B. Exposes the service on an internal cluster IP, reachable only from within the cluster.
C. Provisions an external load balancer from the cloud provider.
D. Routes traffic through an Ingress controller.

---

**Q6.** (02 Kubernetes) Helm is best described as:

A. A container runtime competing with containerd.
B. A package manager for Kubernetes that templates and versions manifests as charts.
C. A replacement for `kubectl` with a GUI.
D. A service mesh.

---

**Q7.** (03 Airflow) In Airflow, a DAG is:

A. A single task run on a schedule.
B. A collection of tasks with declared dependencies and a schedule.
C. A database table backing the scheduler.
D. The web UI component.

---

**Q8.** (03 Airflow) XComs are the Airflow mechanism for:

A. Cross-cluster replication of the metadata DB.
B. Passing small values between tasks in a DAG run.
C. Remote execution on Celery workers.
D. Extending the UI.

---

**Q9.** (03 Airflow) Compared to Airflow's task-centric model, Dagster's primary abstraction is:

A. Operators
B. Assets (the data objects produced and consumed)
C. Sensors
D. Plugins

---

**Q10.** (04 Cloud concepts) In the standard cloud service models, a managed Kubernetes service like Amazon EKS is classified as:

A. IaaS
B. PaaS
C. SaaS
D. FaaS only

---

**Q11.** (04 Cloud concepts) The purpose of storage tier lifecycle rules (hot → cool → archive → delete) is to:

A. Increase durability of recent data.
B. Reduce storage cost by moving rarely accessed objects to cheaper tiers.
C. Replace backups.
D. Enforce IAM policies.

---

**Q12.** (04 Cloud concepts) Serverless compute is usually the wrong choice when:

A. Workloads are spiky and short-lived.
B. Workloads are long-running, continuously busy, and latency-sensitive at high throughput.
C. Traffic is unpredictable.
D. Cold-start latency is tolerable.

---

**Q13.** (05 IAM primer) An AWS IAM policy statement has four core components:

A. User, Group, Role, Policy
B. Effect, Action, Resource, Condition
C. Subject, Verb, Object, Time
D. Principal, Endpoint, Method, Header

---

**Q14.** (05 IAM primer) An IAM role has two policies attached — a trust policy and a permissions policy. The trust policy answers:

A. What API actions the role may perform.
B. Which principals are allowed to assume the role.
C. Which region the role operates in.
D. What the role is billed against.

---

**Q15.** (05 IAM primer) In AWS IAM evaluation, the effect of an explicit `Deny` anywhere in the policy set is:

A. Ignored if an `Allow` exists for the same action.
B. Overridden by the resource's owner.
C. Final — it always wins over any `Allow`.
D. Only applied to the root user.

---

**Q16.** (06 FinOps) The FinOps "Crawl, Walk, Run" maturity model, as defined by the FinOps Foundation, describes:

A. A deployment rollout strategy.
B. Progressive maturity of a FinOps capability within an organization.
C. A container orchestration pattern.
D. A pricing tier from a cloud vendor.

---

**Q17.** (06 FinOps) Reserved or committed-use discounts on cloud compute are appropriate primarily when:

A. Workloads are unpredictable and short-lived.
B. Baseline usage is steady and predictable over 1–3 years.
C. You want to pay on-demand rates only.
D. You run only spot instances.

---

**Q18.** (06 FinOps) "Right-sizing" in FinOps refers to:

A. Purchasing the largest instance available for headroom.
B. Matching provisioned resources to actual utilization, typically by observing CPU/memory metrics and downsizing.
C. Splitting workloads across regions.
D. Reducing the number of availability zones.

---

**Q19.** (07 Data serving) A data API with a p99 latency budget below ~100 ms usually needs:

A. Only a bigger warehouse.
B. A dedicated serving store (cache or serving DB) in front of the warehouse.
C. Reverse ETL.
D. More BI dashboards.

---

**Q20.** (07 Data serving) In a feature store, point-in-time joins exist to:

A. Speed up online inference.
B. Prevent training labels from being joined against feature values from the future, which would leak into the model.
C. Compress feature tables.
D. Enable GDPR deletion.

---

## Answer key

1. **B** — A job runs on a single runner; a workflow is the whole file; steps are inside jobs. Ref: [GitHub Actions — workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).
2. **B** — `dbt build` with `state:modified+` and `--defer` builds changed models and descendants against a prior state. Ref: [dbt — defer](https://docs.getdbt.com/reference/node-selection/defer) · [dbt — state method](https://docs.getdbt.com/reference/node-selection/methods#the-state-method).
3. **B** — `on:` declares trigger events (push, pull_request, schedule, etc.). Ref: [GitHub Actions — events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).
4. **B** — A pod is the smallest deployable unit; it wraps one or more containers. Ref: [Kubernetes — Pods](https://kubernetes.io/docs/concepts/workloads/pods/).
5. **B** — `ClusterIP` exposes a service on an internal cluster IP. Ref: [Kubernetes — Service types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types).
6. **B** — Helm is the package manager for Kubernetes; charts template and version manifests. Ref: [Helm — docs](https://helm.sh/docs/).
7. **B** — A DAG is a collection of tasks with dependencies and a schedule. Ref: [Airflow — DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html).
8. **B** — XComs ("cross-communications") pass small values between tasks. Ref: [Airflow — XComs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html).
9. **B** — Dagster centers on software-defined assets, the data objects produced. Ref: [Dagster — assets](https://docs.dagster.io/concepts/assets/software-defined-assets).
10. **B** — Managed Kubernetes is PaaS: the provider manages the control plane. Ref: [AWS — EKS docs](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html).
11. **B** — Lifecycle rules move objects to cheaper tiers as access patterns cool. Ref: [AWS — S3 lifecycle management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html).
12. **B** — Serverless favors spiky, short workloads; steady, long, high-throughput jobs are cheaper on provisioned compute. Ref: [AWS Lambda — when to use](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).
13. **B** — Effect, Action, Resource, Condition are the statement fields. Ref: [AWS IAM — policy elements reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html).
14. **B** — Trust policy defines who may assume the role. Ref: [AWS IAM — roles terms and concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html).
15. **C** — An explicit Deny always wins in IAM evaluation. Ref: [AWS IAM — policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).
16. **B** — Crawl/Walk/Run is the FinOps Foundation's capability-maturity model. Ref: [FinOps Foundation — Crawl, Walk, Run](https://www.finops.org/framework/maturity-model/).
17. **B** — Commitments pay off for steady baseline usage over 1–3 years. Ref: [AWS — Savings Plans](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html).
18. **B** — Right-sizing matches provisioned capacity to observed utilization. Ref: [AWS Well-Architected — Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html).
19. **B** — Below ~100 ms SLO, a dedicated serving store is typically required. See `07_data_serving/README.md` §"When the warehouse is enough", citing [Trino — overview](https://trino.io/docs/current/overview/use-cases.html).
20. **B** — Point-in-time joins prevent feature leakage from future values into training. Ref: [Feast — point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins).

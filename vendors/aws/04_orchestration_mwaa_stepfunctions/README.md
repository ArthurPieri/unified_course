# Module 04: Orchestration — MWAA, Step Functions, EventBridge (12h)

> Domain 1 Task 1.3 and Domain 3 Task 3.1. Small surface, high exam value. *AWS DEA-C01 Exam Guide*.

## Learning goals

- Pick Step Functions vs. MWAA vs. EventBridge vs. Glue workflows for a given orchestration scenario. *Skill 1.3.1, 3.1.1*.
- Build a Step Functions state machine with Retry, Catch, Parallel, and Map states. *Skill 1.3.1*.
- Author an Airflow DAG in MWAA with sensors and hooks. *Skill 1.3.1*.
- Use EventBridge rules and schedules to trigger pipelines. *Skill 1.1.6, 3.1.9*.
- Send pipeline alerts via SNS and queue retries via SQS. *Skill 1.3.4*.
- Build resilient, fault-tolerant pipelines (idempotency, DLQs, retries). *Skill 1.3.2*.

## Exam weight

Orchestration is small by word count in the guide but appears frequently because every Domain 1 / Domain 3 scenario has a "how is this triggered" angle.

## Key services and primary docs

| Service | What to know | AWS doc |
|---|---|---|
| AWS Step Functions | Standard vs. Express, ASL, Retry/Catch, Parallel/Map, service integrations, `.sync` | [Step Functions Dev Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) |
| Amazon MWAA | Managed Airflow, DAGs, operators, sensors, environment sizing | [MWAA User Guide](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) |
| Amazon EventBridge | Event buses, rules, schedules (EventBridge Scheduler), schema registry, archive/replay | [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html) |
| AWS Glue workflows | Visual DAGs for chains of Glue crawlers and jobs | [Glue workflows](https://docs.aws.amazon.com/glue/latest/dg/orchestrate-using-workflows.html) |
| Amazon SNS | Fan-out pub/sub for pipeline notifications | [SNS Dev Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) |
| Amazon SQS | Buffer + DLQ for failed events; FIFO vs. Standard | [SQS Dev Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html) |

## Concepts (compact)

### Step Functions vs. MWAA vs. EventBridge
- **Step Functions** — serverless state machine. Standard workflows: up to 1 year, exactly-once, per-state-transition billing; good for long-running data pipelines. Express workflows: up to 5 min, at-least-once, higher throughput; good for stream processing. Native `.sync` integration waits for Glue/EMR/Athena/SageMaker jobs to finish.
- **MWAA** — managed Apache Airflow. Right answer when you need Python DAG authoring, sensor-heavy workflows, or you are porting existing Airflow. Environment sizing (Small/Medium/Large) determines scheduler/worker capacity.
- **EventBridge** — event routing and scheduling. Rules match events from AWS services or custom sources to targets (Lambda, Step Functions, SQS, Kinesis, API destinations). EventBridge Scheduler replaces CloudWatch Events scheduled rules for cron workloads at scale.
- **Glue workflows** — lightweight Glue-only DAG (crawlers + jobs). Use inside Glue-only pipelines; prefer Step Functions when multiple services are involved.

Primary: [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/), [MWAA User Guide](https://docs.aws.amazon.com/mwaa/latest/userguide/), [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/).

### Step Functions Retry and Catch
`Retry` re-runs the same state with `IntervalSeconds`, `MaxAttempts`, `BackoffRate`. `Catch` routes specific errors to a fallback state. Together they give you fine-grained error handling without custom code. Primary: [Step Functions error handling (Retry/Catch)](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html). See the hands-on labs in this module's labs/ directory.

### Parallel and Map (including distributed Map)
`Parallel` runs branches concurrently. `Map` iterates over an array. Distributed Map handles up to 10,000 child executions from an S3 inventory — the exam answer for "fan out Lambda over millions of S3 objects". Primary: [Distributed Map](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-asl-use-map-state-distributed.html), [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/).

### EventBridge rule patterns and Scheduler
Rules use a JSON event pattern to match. Schedules use cron or rate expressions. EventBridge Scheduler adds one-time schedules, flexible time windows, and higher scale than legacy scheduled rules. Primary: [Amazon EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html), [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/).

### MWAA basics
Configure via S3 (`dags/`, `plugins.zip`, `requirements.txt`). Sensors wait on external conditions (S3 prefix, Glue job state). Connections and variables live in the Airflow metastore; prefer Secrets Manager for credentials. Primary: [MWAA User Guide](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html), [MWAA environment classes](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-env-class.html).

### SNS + SQS patterns
Fan-out = SNS topic with multiple SQS subscribers. DLQ = SQS queue attached as a redrive target; SFN, Lambda, and EventBridge all support DLQs. Primary: [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/), [SQS dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html).

## Labs

See the hands-on labs in this module's labs/ directory. Key exercises:

| Lab | Goal | AWS reference |
|---|---|---|
| SFN + EventBridge + SQS DLQ | State machine with Retry/Catch and SNS notifications | [Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/) |
| Capstone | MWAA DAG driving an end-to-end pipeline | [AWS Well-Architected Data Analytics Lens](https://docs.aws.amazon.com/wellarchitected/latest/analytics-lens/) |
| CloudWatch alarms | Pipeline monitoring + SNS alert | [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/) |

## Common exam gotchas

| Gotcha | Why it trips people | Reference |
|---|---|---|
| Step Functions Express vs. Standard | Express = at-least-once, 5 min max, higher TPS | [SFN workflow types](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html) |
| `.sync` integration waiting | Saves you from custom polling loops | [SFN service integrations](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html) |
| MWAA environment size | Small has few workers — long DAGs can starve | [MWAA sizing](https://docs.aws.amazon.com/mwaa/latest/userguide/best-practices-env-class.html) |
| EventBridge Scheduler vs. rules | Scheduler is the modern, scalable cron; legacy scheduled rules still work but are capped | [EB Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html) |
| SFN vs. MWAA pricing | SFN Standard bills per state transition; MWAA bills per environment-hour | [SFN pricing](https://aws.amazon.com/step-functions/pricing/) / [MWAA pricing](https://aws.amazon.com/managed-workflows-for-apache-airflow/pricing/) |
| SQS FIFO throughput | 300 TPS (3000 with batching) — Standard has unlimited TPS but no ordering | [SQS quotas](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html) |

## References

See [references.md](./references.md).

## Checkpoint

- [ ] You can sketch a Step Functions state machine with Retry, Catch, and a distributed Map.
- [ ] You can write an Airflow DAG that waits on an S3 prefix and triggers a Glue job.
- [ ] You can build an EventBridge rule that triggers a pipeline on a CloudWatch alarm state change.

# Module 04 Quiz — Orchestration

8 questions. Answer key with cites.

---

**Q1.** A pipeline must process millions of S3 objects listed in an S3 inventory and invoke a Lambda per object, with retries. Which Step Functions primitive fits best?

- A) Parallel state with 10 branches
- B) Map state in inline mode
- C) Distributed Map state
- D) Choice state

**Q2.** A workload needs at-least-once semantics, sub-5-minute total duration, and very high TPS. Which Step Functions workflow type?

- A) Standard
- B) Express
- C) Synchronous Express (with API Gateway)
- D) Both A and B are equivalent

**Q3.** A pipeline calls a Glue job from Step Functions and must pause until the job completes. Which integration pattern?

- A) `.waitForTaskToken`
- B) Request/Response
- C) `.sync` (run-a-job)
- D) Poll via EventBridge

**Q4.** Which service is the modern, scalable solution for running one-time or recurring cron-style triggers with flexible time windows?

- A) CloudWatch Events scheduled rule (legacy)
- B) EventBridge Scheduler
- C) Step Functions Wait state
- D) Lambda cron

**Q5.** A team is porting an existing Airflow DAG repository with sensors and custom operators. Best AWS target?

- A) Step Functions
- B) MWAA
- C) Glue workflows
- D) Data Pipeline

**Q6.** Which combination delivers fan-out from one producer to four independent downstream processors?

- A) SNS topic with four SQS queue subscribers
- B) Single SQS queue with four consumers
- C) Step Functions Parallel state only
- D) EventBridge with one rule and one target

**Q7.** A Step Functions state calls a transient external API that sometimes returns 429. Which configuration handles this without custom code?

- A) A Catch with `States.ALL`
- B) A Retry with `IntervalSeconds`, `MaxAttempts`, and `BackoffRate`
- C) A Wait state of 60 seconds
- D) A Pass state

**Q8.** Which is true about SQS FIFO queues?

- A) Unlimited throughput by default.
- B) 300 messages/sec per API (3000/sec with batching) and ordered delivery.
- C) They cannot be used as DLQs.
- D) They guarantee exactly-once end-to-end across consumers.

---

## Answer key

1. **C** — Distributed Map handles large-scale iteration across S3 inventories (up to 10,000 child executions). [SFN Distributed Map](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-asl-use-map-state-distributed.html).
2. **B** — Express: at-least-once, up to 5 min, higher TPS. [SFN workflow types](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html).
3. **C** — `.sync` (run-a-job) makes Step Functions wait for supported services like Glue/EMR/Athena. [SFN service integrations](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html).
4. **B** — EventBridge Scheduler. [EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html).
5. **B** — MWAA (managed Airflow). [MWAA](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html).
6. **A** — SNS topic with SQS fan-out. [SNS fan-out to SQS](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html).
7. **B** — Retry with backoff handles transient errors declaratively. [SFN error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html).
8. **B** — SQS FIFO default limits: 300/sec per API without batching, 3000/sec with batching; ordered, exactly-once in-queue. [SQS quotas](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html).

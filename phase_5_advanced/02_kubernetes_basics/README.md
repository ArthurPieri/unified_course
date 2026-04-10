# Module 02: Kubernetes Basics for Data Engineers (8h)

> Phase 5 · Advanced. Enough Kubernetes to deploy, inspect, and debug a stateful data tool like Trino on a local cluster.

## Learning goals
- Explain the declarative / reconciliation-loop mental model in one paragraph.
- Name and describe six core Kubernetes objects: Pod, Deployment, Service, ConfigMap, Secret, Namespace.
- Use `kubectl get`, `describe`, `logs`, `exec`, and `apply` to inspect and modify a running cluster.
- Create a local cluster with `kind` and install a Helm chart into it.
- Map Docker Compose concepts to their Kubernetes equivalents (cite `../dataeng/k8s/README.md:L29-L38`).
- Decide when running a data tool on Kubernetes is worth the complexity and when a managed service is better.

## Prerequisites
- `phase_1_foundations/04_docker_compose`
- `phase_5_advanced/01_cicd` (Helm install runs inside a workflow)

## Reading order
1. This README
2. `../01_cicd/labs/lab_L5a_cicd_k8s/README.md` — the Helm install in step 3 exercises everything here
3. `quiz.md`

## Concepts

### Mental model: declarative desired state
Kubernetes is not a job runner. You do not tell it "start a container"; you tell it "I want three replicas of this container always running," and a **control loop** continuously compares actual state to desired state and takes action to close the gap. If a node dies, the loop notices the pod is missing and schedules a new one. If you change the image tag in the manifest, the loop rolls out the new version. Every object in the API is just a document describing desired state; every controller is just a loop watching for changes. This is the single most important idea in Kubernetes — it explains almost every behaviour.

Ref: [Kubernetes — What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/) · [Kubernetes — Object management](https://kubernetes.io/docs/concepts/overview/working-with-objects/)

### Pod
A **Pod** is the smallest deployable unit. It wraps one or more containers that share a network namespace (same `localhost`) and optionally storage volumes. In practice, single-container pods are the norm; multi-container pods exist for sidecar patterns (a log shipper next to the main app). Pods are ephemeral — they have no stable identity or IP; if one dies, its replacement is a new pod with a new name.

Ref: [Kubernetes — Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

### Deployment
A **Deployment** declares: "I want N pods matching this template, and here is how to roll out updates." It manages a ReplicaSet, which manages the actual pods. Deployments give you rolling updates (new pods come up before old ones go down), rollbacks (`kubectl rollout undo`), and scaling (`kubectl scale`). For any stateless or quasi-stateless workload — Trino coordinators, dbt runners, an API — a Deployment is the right choice. For workloads with stable identity (Kafka, ZooKeeper, databases) use a **StatefulSet** instead.

Ref: [Kubernetes — Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

### Service
A Pod's IP changes every time it is rescheduled. A **Service** gives you a stable virtual IP and DNS name that load-balances across the pods matching a label selector. `ClusterIP` (default) is reachable only inside the cluster; `NodePort` opens a port on every node; `LoadBalancer` asks the cloud provider for an external LB. The `trino-values.yaml` in the dataeng repo picks `NodePort` with port `30080` so the coordinator is reachable from the host via the kind port mapping (`../dataeng/k8s/trino-values.yaml:L47-L50`, `../dataeng/k8s/kind-config.yaml:L8-L12`).

Ref: [Kubernetes — Services](https://kubernetes.io/docs/concepts/services-networking/service/)

### ConfigMap and Secret
**ConfigMaps** hold non-sensitive configuration (env vars, config files). **Secrets** hold sensitive data (passwords, tokens, TLS keys) and are base64-encoded in etcd — by default *not* encrypted at rest unless you enable encryption providers. Both are mounted into pods either as environment variables or as files in a volume. Trino's catalog properties files are a natural fit for ConfigMaps; the S3 access key in `trino-values.yaml:L43-L44` would in production live in a Secret, not values.yaml.

Ref: [Kubernetes — ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) · [Kubernetes — Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

### Namespace
A **Namespace** is a virtual cluster inside a cluster. It scopes object names (two pods can be called `trino` if they're in different namespaces) and is the unit for RBAC policies and resource quotas. The dataeng example deploys Trino into `-n trino` to keep it isolated from anything else on the cluster — see `../dataeng/k8s/README.md:L18-L19`.

Ref: [Kubernetes — Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

### kubectl basics
Five verbs cover 90% of daily use:
- `kubectl get <kind>` — list objects (add `-o wide` for more columns, `-A` for all namespaces)
- `kubectl describe <kind>/<name>` — verbose detail including recent events (always check events when a pod is stuck)
- `kubectl logs <pod>` — container stdout/stderr; `-f` to follow, `--previous` for crashed container
- `kubectl exec -it <pod> -- <cmd>` — shell into a running container
- `kubectl apply -f <file>` — declaratively create or update from a manifest

Ref: [Kubernetes — kubectl overview](https://kubernetes.io/docs/reference/kubectl/) · [kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)

### Local cluster with kind
**kind** ("Kubernetes IN Docker") runs a full cluster as Docker containers — one per node. It is the standard way to develop locally and to spin up throwaway clusters inside CI runners. The cluster config is YAML: `apiVersion: kind.x-k8s.io/v1alpha4`, `kind: Cluster`, a list of nodes, and optional `extraPortMappings` to expose node ports on the host. The dataeng example (`../dataeng/k8s/kind-config.yaml:L1-L12`) creates a single-node cluster named `lakehouse-dev` and forwards host port `8180` to container port `30080` — exactly where the Trino NodePort service lives.

Ref: [kind — Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/) · [kind — Configuration](https://kind.sigs.k8s.io/docs/user/configuration/)

### Helm: why it exists
Writing raw YAML for a real app means dozens of files and copy-paste between environments. **Helm** is a package manager: a **chart** is a directory of Go templates plus a `values.yaml` with defaults. `helm install myrelease ./chart -f my-values.yaml` renders the templates with merged values and applies the result to the cluster. `helm upgrade` diffs and rolls forward; `helm rollback` reverts. The Trino chart lives at [github.com/trinodb/charts](https://github.com/trinodb/charts) and is consumed in the dataeng repo via a minimal values override that sets `server.workers: 1`, resource requests, and the Iceberg catalog (`../dataeng/k8s/trino-values.yaml:L1-L50`).

Ref: [Helm — Charts](https://helm.sh/docs/topics/charts/) · [Helm — Using Helm](https://helm.sh/docs/intro/using_helm/) · [Trino Helm charts](https://github.com/trinodb/charts)

### When to run data tools on K8s vs managed
Running **Trino on Kubernetes** is mature: the official chart is actively maintained, Trino is stateless between queries, and elastic worker scaling is a natural fit for K8s. Running **Spark on Kubernetes** is increasingly common — the Spark operator is production-grade. Running **Kafka on Kubernetes** is possible with Strimzi but operationally heavier than a managed service for most teams. Running **Postgres or other OLTP databases on Kubernetes** is still contentious: the community is split, and most teams should prefer a managed RDS/Cloud SQL unless they have a platform team dedicated to operating stateful workloads. The heuristic: **stateless or restart-tolerant → K8s is fine; stateful with strict durability → lean managed** unless you have strong operational reasons.

Ref: [Trino — Deploying on Kubernetes](https://trino.io/docs/current/installation/kubernetes.html) · *Designing Data-Intensive Applications*, Kleppmann, Ch. 5 (replication) for why stateful-on-K8s is hard.

## Labs
| Lab | Goal | Est. time | Link |
|---|---|---|---|
| `lab_L5a_cicd_k8s` (shared with 01_cicd) | Install Trino on a kind cluster via Helm inside a GitHub Actions workflow | 90m | [../01_cicd/labs/lab_L5a_cicd_k8s/](../01_cicd/labs/lab_L5a_cicd_k8s/) |

## Common failures
| Symptom | Cause | Fix | Source |
|---|---|---|---|
| Pod stuck in `Pending` | No node has enough CPU/memory | `kubectl describe pod` → check events; lower resource requests | [Kubernetes — Resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) |
| `ImagePullBackOff` on a local image | Image not loaded into kind | `kind load docker-image <tag> --name <cluster>` | [kind — Loading an image](https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster) |
| Service reachable inside cluster, not from host | ClusterIP service; no NodePort / port-forward | Use `NodePort` + `extraPortMappings` or `kubectl port-forward` | `../dataeng/k8s/kind-config.yaml:L8-L12` |
| Secret values visible in `kubectl get secret -o yaml` | base64 is not encryption | Enable etcd encryption-at-rest or use an external secret manager | [Kubernetes — Encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) |
| `helm upgrade` hangs forever | Pod never becomes ready; `--wait` blocks | Drop `--wait` for debugging; run `kubectl describe` to find the real cause | [Helm — Helm install](https://helm.sh/docs/helm/helm_install/) |

## References
See [references.md](./references.md).

## Checkpoint
Before moving on, you can:
- [ ] Draw the reconciliation-loop model on a whiteboard.
- [ ] Given a running cluster, find a crashing pod's last log line with `kubectl logs --previous`.
- [ ] Write a kind config that exposes a NodePort on a chosen host port.
- [ ] Install a Helm chart with a custom values file and roll it back.
- [ ] Justify (or reject) running Postgres on Kubernetes for your team's use case.

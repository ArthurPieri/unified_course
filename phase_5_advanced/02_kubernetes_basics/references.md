# References — 02_kubernetes_basics

## Kubernetes (official docs)
- [What is Kubernetes?](https://kubernetes.io/docs/concepts/overview/) — high-level overview and the declarative model.
- [Working with Kubernetes objects](https://kubernetes.io/docs/concepts/overview/working-with-objects/) — object metadata, spec, status.
- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) — smallest deployable unit.
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) — declarative rollouts and rollbacks.
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/) — ClusterIP, NodePort, LoadBalancer.
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) — non-sensitive config.
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) — sensitive config and their limits.
- [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) — virtual clusters and RBAC scope.
- [kubectl overview](https://kubernetes.io/docs/reference/kubectl/) — CLI reference.
- [kubectl cheat sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/) — common commands.
- [Resource management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) — requests, limits, QoS.
- [Encrypting confidential data at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) — etcd encryption.

## kind (Kubernetes IN Docker)
- [kind — Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/) — create a cluster, load images, delete.
- [kind — Configuration](https://kind.sigs.k8s.io/docs/user/configuration/) — `extraPortMappings`, multi-node, networking.

## Helm
- [Helm — Charts](https://helm.sh/docs/topics/charts/) — chart directory layout and templating.
- [Helm — Using Helm](https://helm.sh/docs/intro/using_helm/) — install, upgrade, rollback, values.
- [Helm — helm install](https://helm.sh/docs/helm/helm_install/) — command reference including `--wait`.

## Trino on Kubernetes
- [Trino — Deploying on Kubernetes](https://trino.io/docs/current/installation/kubernetes.html) — official deployment guide.
- [trinodb/charts](https://github.com/trinodb/charts) — official Trino Helm chart repository (`https://trinodb.github.io/charts`).

## Sibling repo (primary reuse source)
- `../dataeng/k8s/kind-config.yaml:L1-L12` — kind cluster config with NodePort mapping for Trino.
- `../dataeng/k8s/trino-values.yaml:L1-L50` — Helm values: image pin, workers, resources, Iceberg catalog, NodePort.
- `../dataeng/k8s/README.md:L1-L38` — Docker-Compose-to-Kubernetes concept mapping.

## Books
- *Designing Data-Intensive Applications*, Kleppmann, Ch. 5 — why stateful replication on dynamic infrastructure is hard.

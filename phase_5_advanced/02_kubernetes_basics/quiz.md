# Quiz — 02_kubernetes_basics

Ten multiple-choice questions. Answer key at the bottom.

---

**1.** The core mental model of Kubernetes is:
- A. A job scheduler that runs one container at a time.
- B. A declarative desired-state system with control loops reconciling actual state toward that desired state.
- C. A replacement for Docker Compose with the same semantics.
- D. A VM hypervisor.

**2.** What is a Pod?
- A. A physical machine in the cluster.
- B. The smallest deployable unit — one or more containers sharing a network namespace and optional volumes.
- C. A YAML file describing a Service.
- D. A type of storage volume.

**3.** Which object is the correct choice for a stateless workload that needs rolling updates and rollbacks?
- A. Pod
- B. StatefulSet
- C. Deployment
- D. Job

**4.** Which Service type exposes a port on every node in the cluster?
- A. ClusterIP
- B. NodePort
- C. Headless
- D. Ingress

**5.** Why is a base64-encoded Secret not the same as an encrypted Secret?
- A. base64 is case-insensitive.
- B. base64 is an encoding, not encryption — anyone with read access to the Secret can decode it trivially. Encryption at rest must be enabled separately.
- C. Secrets are always encrypted by default.
- D. base64 cannot represent binary data.

**6.** Which kubectl command is the first one to run when a pod is stuck in `Pending`?
- A. `kubectl logs <pod>`
- B. `kubectl describe pod <pod>` (to read the events section)
- C. `kubectl delete pod <pod>`
- D. `kubectl apply -f <file>`

**7.** What does `kind load docker-image` do?
- A. Pushes the image to Docker Hub.
- B. Makes a locally built image available to nodes in a kind cluster without a registry.
- C. Pulls an image from a private registry.
- D. Builds a new image from a Dockerfile.

**8.** In the dataeng repo, `kind-config.yaml` maps host port `8180` to container port `30080`. Why `30080`?
- A. It's the default Kubernetes API port.
- B. It matches the NodePort configured in `trino-values.yaml` for the Trino coordinator Service.
- C. It's a random choice with no meaning.
- D. It's the Docker daemon port.

**9.** What is a Helm chart?
- A. A monitoring dashboard.
- B. A package — a directory of templated Kubernetes manifests plus a default `values.yaml` — that Helm renders and applies.
- C. A Kubernetes object kind.
- D. A CI/CD tool.

**10.** Which of these is the *weakest* candidate for running on Kubernetes without a dedicated platform team?
- A. Trino coordinator and workers
- B. A stateless Python API
- C. A primary Postgres database holding production state
- D. A dbt runner job

---

## Answer key
1. **B** — declarative desired state + reconciliation loops.
2. **B** — smallest deployable unit; shared network namespace.
3. **C** — Deployments manage ReplicaSets and support rolling updates / rollbacks.
4. **B** — NodePort opens the same port on every node.
5. **B** — base64 is encoding, not encryption; etcd encryption must be enabled explicitly.
6. **B** — `describe` surfaces the scheduler events explaining why the pod is Pending.
7. **B** — loads a local Docker image into the kind node(s) without a registry.
8. **B** — Trino's NodePort is `30080` (see `trino-values.yaml:L50`), and kind forwards host `8180` → container `30080`.
9. **B** — a templated package rendered and applied by Helm.
10. **C** — stateful primary databases on Kubernetes remain operationally expensive; managed services are usually the better default.

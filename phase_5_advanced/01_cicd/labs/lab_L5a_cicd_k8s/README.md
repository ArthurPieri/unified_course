# Lab L5a: CI/CD to Kubernetes — GitHub Actions + kind + Trino

## Goal
Build a GitHub Actions workflow that lints and tests a Python package on every pull request, then, on merge to `main`, spins up a local kind cluster, loads a Docker image into it, and installs Trino via Helm.

## Prerequisites
- Docker Desktop running
- `kind`, `kubectl`, `helm` installed locally (see `../dataeng/k8s/README.md:L5-L11`)
- A GitHub repo you can push to
- Completed module `README.md`

## Setup
```bash
mkdir lab_l5a && cd lab_l5a
git init -b main
uv init --package .
mkdir -p .github/workflows k8s tests
cp ../../../../../dataeng/k8s/kind-config.yaml k8s/kind-config.yaml
cp ../../../../../dataeng/k8s/trino-values.yaml k8s/trino-values.yaml
```

Add a trivial module and test:
```bash
cat > src/lab_l5a/__init__.py <<'EOF'
def add(a: int, b: int) -> int:
    return a + b
EOF

cat > tests/test_add.py <<'EOF'
from lab_l5a import add
def test_add():
    assert add(2, 3) == 5
EOF
```

## Steps

1. **Write the CI workflow** at `.github/workflows/ci.yml`. Use `actions/checkout@v4` and `astral-sh/setup-uv@v3`, then run `uv sync`, `uv run ruff check .`, and `uv run pytest`. Workflow syntax reference: [GitHub Actions — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions). Trigger on `pull_request` and `push` to `main`.

2. **Add a deploy job** that only runs `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`. Steps:
   ```yaml
   - uses: helm/kind-action@v1
     with:
       config: k8s/kind-config.yaml
   - name: Build image
     run: docker build -t lab-l5a:${{ github.sha }} .
   - name: Load image into kind
     run: kind load docker-image lab-l5a:${{ github.sha }} --name lakehouse-dev
   ```
   The kind cluster name `lakehouse-dev` comes from `../dataeng/k8s/kind-config.yaml:L5`. `kind load docker-image` is the canonical way to make a locally built image available to the cluster without pushing to a registry — see [kind — Loading an image](https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster).

3. **Install Trino via Helm** in a following step:
   ```bash
   helm repo add trino https://trinodb.github.io/charts
   helm repo update
   helm upgrade --install trino trino/trino \
     --namespace trino --create-namespace \
     --values k8s/trino-values.yaml \
     --wait --timeout 10m
   ```
   The chart repo URL is the canonical one published by the Trino project at [github.com/trinodb/charts](https://github.com/trinodb/charts). The values file pins `image.tag: "470"` and sets a single worker — see `../dataeng/k8s/trino-values.yaml:L5-L32`.

4. **Verify Trino is healthy** in a final step:
   ```bash
   kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=trino -n trino --timeout=300s
   kubectl get pods -n trino
   COORD=$(kubectl get pod -n trino -l app.kubernetes.io/component=coordinator -o name | head -1)
   kubectl exec -n trino "$COORD" -- trino --execute "SELECT 1"
   ```

## Verify
- [ ] PR workflow run is green (lint + tests).
- [ ] Merge-to-main workflow reaches the Helm step without error.
- [ ] `kubectl get pods -n trino` shows `trino-coordinator-*` and `trino-worker-*` in `Running`.
- [ ] `SELECT 1` via `kubectl exec` returns `1`.

## Cleanup
```bash
helm uninstall trino -n trino
kind delete cluster --name lakehouse-dev
```

## Troubleshooting
| Symptom | Fix |
|---|---|
| `kind load docker-image` says image not found | Make sure `docker build` ran in the same job — kind load only sees the local Docker daemon. |
| Trino pod stuck in `Pending` | Runner memory too small; drop `coordinator.resources.limits.memory` in values or use a bigger runner. |
| `helm repo add` fails with TLS error | Re-run `helm repo update`; check outbound network on the runner. |
| Workflow deploys on PRs too | Add the `if:` guard in step 2 — check `github.ref` AND `github.event_name`. |

## Stretch goals
- Add a rollback step: on Helm failure, run `helm rollback trino 0` and fail the job.
- Add an environment protection rule (`environment: production`) requiring manual approval before the Helm step.
- Replace the pinned image with a build pushed to GitHub Container Registry via OIDC.

## References
See `../../references.md` (module-level).

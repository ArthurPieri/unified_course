# Module 04: Cloud Fallback (1h)

## Learning goals
- Choose between GitHub Codespaces and Gitpod for running the course
- Configure a Codespaces environment that fits the Phase 3 full-profile working set
- Understand the cost envelope before you commit

## Prerequisites
- [03_hardware_check](../03_hardware_check/) — only needed if `check.sh` said `CLOUD_FALLBACK`

## Reading order
1. This README
2. Check the pricing / free-tier pages linked below — they change; re-verify before starting Phase 3
3. Create your account and test a small container

## Concepts

### When to use this module
Your local machine has <8GB RAM, no Docker, or Docker Desktop memory can't be raised. Cloud dev environments give you a remote Linux VM with Docker pre-installed, reachable from a browser or your local editor (VS Code, JetBrains Gateway).

### GitHub Codespaces
A managed dev environment running in a container on GitHub's infrastructure. Access via browser or VS Code.

- **Machine sizes:** 2-core / 4GB, 4-core / 8GB, 8-core / 16GB, 16-core / 32GB, 32-core / 64GB
- **Storage:** 32 GB per codespace by default
- **Free tier:** Personal accounts get a monthly free quota of core-hours and storage (re-verify current numbers before starting — the free tier has changed multiple times)
- **Idle timeout:** default 30 min (configurable), then the codespace stops and stops billing compute
- **Prebuilds:** speed up first start by caching the environment
- **Pricing reference:** [GitHub Codespaces billing](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
- **Docs:** [GitHub Codespaces overview](https://docs.github.com/en/codespaces/overview)

**For this course:** The 4-core / 16GB machine is the cheapest size that runs the Phase 3 full profile comfortably. The 2-core / 8GB size runs the light profile.

### Gitpod
Alternative cloud dev environment. Supports GitHub, GitLab, Bitbucket. Workspaces are ephemeral and rebuild from a `.gitpod.yml`.

- **Machine classes:** Standard (4 cores / 8GB) and Large (8 cores / 16GB) on the managed offering
- **Free tier:** Re-verify current allocation on the pricing page before starting
- **Docs:** [Gitpod introduction](https://www.gitpod.io/docs/introduction)
- **Pricing:** [Gitpod pricing](https://www.gitpod.io/pricing)

**For this course:** The Large class (16GB) runs the Phase 3 full profile. Standard (8GB) runs the light profile.

### How to decide
| If... | Use |
|---|---|
| Your account already uses GitHub heavily | Codespaces |
| You want the cheapest managed option with Docker-in-Docker support | Compare both free tiers at the moment you start — they shift |
| You need persistent state across long sessions | Either works; both persist the workspace between starts (Codespaces 30 days by default) |
| You want the lowest-latency shell on a non-GitHub repo | Gitpod |

### What "Docker-in-Docker" means and why it matters here
The Phase 3 stack runs as containers (`docker compose up`). Inside a cloud dev container, that means running Docker *inside* the dev container. Both Codespaces and Gitpod support this via a dev-container feature (Codespaces) or a workspace image (Gitpod). You do **not** install Docker Desktop inside the cloud env.

Ref (Codespaces): [dev container features — docker-in-docker](https://containers.dev/features) · [Codespaces dev container spec](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

### Cost discipline
- Stop the environment when you stop working — don't rely on idle timeout
- Use the smallest size that actually works (light profile on 8GB is fine for most modules)
- Don't leave MinIO writing synthetic data in a loop — Phase 4 performance labs use a generator; turn it off when done
- Monitor your billing page weekly during Phase 3+

## Common failures
| Symptom | Cause | Fix |
|---|---|---|
| Codespace starts but Docker commands fail | Missing docker-in-docker feature in `.devcontainer/devcontainer.json` | Add the `ghcr.io/devcontainers/features/docker-in-docker:2` feature. Ref: [containers.dev features](https://containers.dev/features) |
| Gitpod workspace OOM on Phase 3 full profile | Standard (8GB) class | Upgrade to Large (16GB) or use light profile |
| Unexpected bill | Idle timeout never fired (workspace kept alive by an open terminal) | Stop the environment manually at end of day |

## References
See [references.md](./references.md).

## Checkpoint
- [ ] Chose Codespaces or Gitpod — recorded in `../02_self_assessment/goal.md`
- [ ] Verified current free tier / pricing on the official page
- [ ] Created a test workspace, ran `docker run hello-world`
- [ ] Know how to stop the workspace to avoid idle charges

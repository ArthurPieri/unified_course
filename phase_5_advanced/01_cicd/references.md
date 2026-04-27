# References — 01_cicd

## GitHub Actions (official docs)
- [About workflows](https://docs.github.com/en/actions/using-workflows/about-workflows) — file layout, triggers, jobs, steps.
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) — authoritative reference for every YAML key.
- [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) — `push`, `pull_request`, `schedule`, `workflow_dispatch`.
- [Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) — storing and accessing repo/org/environment secrets.
- [About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) — OIDC federation model.
- [Configuring OpenID Connect in Amazon Web Services](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) — concrete AWS setup.
- [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment) — protection rules, required reviewers, wait timers.
- [actions/checkout](https://github.com/actions/checkout) — canonical checkout action.
- [actions/setup-python](https://github.com/actions/setup-python) — Python runtime + pip cache.

## dbt (official docs)
- [Continuous integration jobs](https://docs.getdbt.com/docs/deploy/continuous-integration) — Slim CI, deferral, state comparisons.
- [Unit tests](https://docs.getdbt.com/docs/build/unit-tests) — mocked-input tests that run without a warehouse.
- [profiles.yml](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml) — connection config for CI environments.

## Additional CI/CD resources
- See the CI/CD examples in this repo's `phase_5_advanced/01_cicd/` for dbt PR workflow and full-stack integration workflow patterns.
- [GitHub Actions — Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) — authoritative workflow reference.
- [Linux Foundation — DevOps and CI/CD overview](https://training.linuxfoundation.org/resources/free-courses-overview/) — CI/CD fundamentals and DevOps lifecycle background.

## Books
- *Fundamentals of Data Engineering*, Reis & Housley, Ch. 2 (data engineering lifecycle) and Ch. 6 (ingestion → serving as a controlled release path).

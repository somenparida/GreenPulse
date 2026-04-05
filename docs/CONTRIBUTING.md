# Contributing to GreenPulse

Thank you for contributing to GreenPulse. This document describes version control, branching, and review expectations aligned with our academic and engineering standards.

## Conventional Commits

All commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

**Examples:**

- `feat(ingestion): add batch telemetry endpoint`
- `fix(dashboard): correct moisture scale on chart`
- `ci: add Trivy scan to main workflow`

## GitFlow Branching Model

We use a strict [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) structure:

| Branch        | Purpose |
|---------------|---------|
| `main`        | Production-ready releases only. Tagged releases are cut from here. |
| `develop`     | Integration branch for the next release. Default target for feature PRs. |
| `feature/*`   | New functionality (e.g. `feature/sensor-calibration`). Branch from `develop`, merge back via PR. |
| `release/*`   | Release preparation (e.g. `release/1.2.0`). Branch from `develop`, merge to `main` and back to `develop`. |
| `hotfix/*`    | Urgent production fixes (e.g. `hotfix/cve-patch`). Branch from `main`, merge to `main` and `develop`. |

### Workflow summary

1. Create `feature/<short-name>` from `develop`.
2. Open a Pull Request into `develop` using the repository template.
3. Ensure CI passes (lint, tests, security scan where applicable).
4. After review and approval, squash or merge per team policy.
5. Releases: maintainers create `release/x.y.z` from `develop`, finalize, merge to `main`, tag, merge back to `develop`.

## Local development

- Copy `.env.example` to `.env` and set variables (no secrets in git).
- Run the stack: `docker compose up --build`.

## Pull requests

- Link related issues or rubric items when applicable.
- Describe **what** changed and **why**, not only the diff.
- For infrastructure changes, note any required manual steps (e.g. Terraform backend bootstrap).

## Security

- Never commit passwords, API keys, or kubeconfig contents.
- Use placeholders such as `${VAR_NAME}` in examples and Kubernetes Secret references supplied at deploy time.

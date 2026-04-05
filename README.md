# GreenPulse

[![CI/CD Pipeline](https://github.com/somenparida/GreenPulse/actions/workflows/main.yml/badge.svg)](https://github.com/somenparida/GreenPulse/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built with Docker](https://img.shields.io/badge/Built%20with-Docker-blue?logo=docker)](https://www.docker.com/)
[![Infrastructure as Code](https://img.shields.io/badge/IaC-Terraform-purple?logo=terraform)](https://www.terraform.io/)
[![Kubernetes Ready](https://img.shields.io/badge/Kubernetes-Ready-blue?logo=kubernetes)](https://kubernetes.io/)

**GreenPulse** is a multi-region IoT edge analytics reference platform for precision agriculture. It ingests soil and crop telemetry (moisture, temperature, pH), persists it in PostgreSQL, and visualizes crop health in a live dashboard. The repository is structured as a monorepo with containerized microservices, Terraform modules for AWS (VPC, EKS, RDS), Kubernetes manifests (including HPA and probes), Ansible for an edge-gateway simulation, and a GitHub Actions pipeline for lint, test, image build, Trivy scanning, and optional cluster deployment.

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Local Development](#local-development-docker-compose)
- [Deployment](#deployment)
  - [Kubernetes](#kubernetes)
  - [Terraform (AWS)](#terraform-aws)
  - [Ansible (Edge)](#ansible-edge-simulation)
- [CI/CD](#cicd-github-actions)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Quick Start

```bash
# Clone repository
git clone https://github.com/somenparida/GreenPulse.git
cd GreenPulse

# Local dev with Docker Compose
cp .env.example .env
# Edit .env with your values
docker compose up --build

# Open dashboard
open http://localhost:8501
```

## Project Layout

```text
GreenPulse/
├── .github/
│   ├── workflows/main.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── apps/
│   ├── sensor-emulator/       # Python telemetry generator
│   ├── ingestion-api/         # Go API + PostgreSQL
│   └── dashboard/             # Streamlit UI
├── docs/
│   └── CONTRIBUTING.md        # GitFlow + Conventional Commits
├── infrastructure/
│   ├── ansible/
│   ├── kubernetes/base/
│   └── terraform/
│       ├── modules/{vpc,eks,rds}
│       ├── backend.hcl.example
│       └── terraform.tfvars.example
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Architecture

```mermaid
flowchart TB
  subgraph Edge["Edge / Field"]
    SE[sensor-emulator]
    AG[Ansible edge-gateway simulation]
  end

  subgraph Cloud["Cloud (AWS example)"]
    ING[ingestion-api on EKS]
    PG[(RDS PostgreSQL)]
    ST[Streamlit dashboard]
    HPA[HPA on ingestion-api]
  end

  subgraph CI["CI/CD"]
    GHA[GitHub Actions]
    TRI[Trivy scan]
    REG[GHCR]
  end

  SE -->|JSON telemetry| ING
  AG -.->|optional forwarder stub| ING
  ING --> PG
  ST -->|readings API| ING
  HPA --> ING
  GHA --> TRI
  GHA --> REG
  REG -->|image pull| ING
  REG -->|image pull| SE
  REG -->|image pull| ST
```

**Multi-region posture:** Terraform in this repo provisions a single primary region (VPC + EKS + RDS). For true multi-region active-active or DR, replicate the same modules in a second workspace with another `aws_region`, front traffic with global load balancing or DNS failover, and replicate or stream telemetry (for example via regional ingestion endpoints). The diagram above shows the logical split between edge simulation and cloud services.

## Local development (Docker Compose)

1. Copy `.env.example` to `.env` and replace every placeholder with real values (for example export `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and a matching `DATABASE_URL`). **Do not commit `.env`.**
2. From the repository root:

```bash
docker compose up --build
```

3. Open the dashboard at `http://localhost:8501`. The ingestion API listens on `http://localhost:8080` (`GET /api/v1/readings`, `POST /api/v1/telemetry`). Health checks: `GET /health/live`, `GET /health/ready`.

## Kubernetes

Manifests live under `infrastructure/kubernetes/base` and are wired with **Kustomize**.

- **Secret:** create `greenpulse-db` in namespace `greenpulse` before rollouts succeed, e.g.  
  `kubectl create secret generic greenpulse-db --namespace=greenpulse --from-literal=DATABASE_URL='${DATABASE_URL}'`  
  or render `secret.example.yaml` with `envsubst` (see file header comments).
- Replace image prefixes `ghcr.io/PLACEHOLDER_ORG/...` with your registry path (GitHub Actions does this automatically via `kubectl set image`).
- Apply: `kubectl apply -k infrastructure/kubernetes/base`

Features demonstrated: **HPA** on `ingestion-api`, **liveness/readiness** probes on all workloads, and **Secret-backed** database credentials (no passwords in Deployment manifests).

## Terraform (AWS)

- Modules: `modules/vpc`, `modules/eks`, `modules/rds`.
- RDS master password is generated with `random_password` (sensitive output) — **not** hardcoded.
- **Remote state:** configure an S3 bucket and DynamoDB table for locking, copy `backend.hcl.example` to `backend.hcl`, replace `REPLACE_ME_*` placeholders, then run `terraform init -backend-config=backend.hcl`.
- **Azure alternative:** for Blob + native locking, use the `azurerm` backend in a fork or second root module; the pattern (remote state + lock) is the same even though this tree targets AWS.

Copy `terraform.tfvars.example` to `terraform.tfvars` (gitignored) or pass `-var` / `TF_VAR_*` for `aws_region`, `environment`, and `rds_master_username`.

## Deployment

### Kubernetes

Manifests live under `infrastructure/kubernetes/base` and are wired with **Kustomize**.

- **Secret:** create `greenpulse-db` in namespace `greenpulse` before rollouts succeed, e.g.  
  `kubectl create secret generic greenpulse-db --namespace=greenpulse --from-literal=DATABASE_URL='${DATABASE_URL}'`  
  or render `secret.example.yaml` with `envsubst` (see file header comments).
- Replace image prefixes `ghcr.io/PLACEHOLDER_ORG/...` with your registry path (GitHub Actions does this automatically via `kubectl set image`).
- Apply: `kubectl apply -k infrastructure/kubernetes/base`

Features demonstrated: **HPA** on `ingestion-api`, **liveness/readiness** probes on all workloads, and **Secret-backed** database credentials (no passwords in Deployment manifests).

### Terraform (AWS)

- Modules: `modules/vpc`, `modules/eks`, `modules/rds`.
- RDS master password is generated with `random_password` (sensitive output) — **not** hardcoded.
- **Remote state:** configure an S3 bucket and DynamoDB table for locking, copy `backend.hcl.example` to `backend.hcl`, replace `REPLACE_ME_*` placeholders, then run `terraform init -backend-config=backend.hcl`.
- **Azure alternative:** for Blob + native locking, use the `azurerm` backend in a fork or second root module; the pattern (remote state + lock) is the same even though this tree targets AWS.

Copy `terraform.tfvars.example` to `terraform.tfvars` (gitignored) or pass `-var` / `TF_VAR_*` for `aws_region`, `environment`, and `rds_master_username`.

### Ansible (Edge Simulation)

See `infrastructure/ansible/playbook.yml` and copy `inventory.example.ini` to `inventory.ini` with your SSH settings (use `${EDGE_SSH_USER}` style placeholders in the example only; real values stay local).

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/main.yml`

- Lints Python with **Ruff**, runs **pytest** for the emulator, and **Go tests** inside a container.
- Builds each Dockerfile, runs **Trivy** against the loaded image, and **pushes** to **GHCR** on pushes to `main` / `develop`.
- **Deploy:** on `main`, if repository secret `KUBE_CONFIG_B64` (base64-encoded kubeconfig) is set, applies Kustomize and runs `kubectl set image` to the commit SHA.

## Contributing

- **GitFlow** and **Conventional Commits** are documented in [CONTRIBUTING.md](docs/CONTRIBUTING.md).
- Pull requests should use `.github/PULL_REQUEST_TEMPLATE.md`.
- Report bugs via [GitHub Issues](https://github.com/somenparida/GreenPulse/issues) using templates.

## Security

For security vulnerabilities, please see [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.

Best practices:
- No passwords or API keys are committed. Use environment variables, Kubernetes Secrets, Terraform sensitive outputs, and GitHub **encrypted secrets** for `KUBE_CONFIG_B64`.
- Container images use **multi-stage** builds with **Alpine/slim** (Python) and **distroless** (Go API).
- All images are scanned with **Trivy** in the CI/CD pipeline.

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

## Support & Feedback

- 💬 **Discussions**: GitHub Discussions for questions and general feedback
- 🐛 **Issues**: [Report bugs or request features](https://github.com/somenparida/GreenPulse/issues)
- 📖 **Docs**: See [docs/](docs/) and inline code comments
- 🔐 **Security**: See [SECURITY.md](SECURITY.md)

---

**Built with ❤️ for precision agriculture IoT platforms.**

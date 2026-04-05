# Security Policy

## Reporting a Vulnerability

GreenPulse takes security seriously. If you discover a vulnerability, please report it responsibly by emailing **security@greenpulse.dev** or opening a **private security advisory** on GitHub rather than creating a public issue.

### What to include:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Affected components (e.g., ingestion-api, dashboard, Terraform modules)
- Suggested fix (if known)

### Response timeline:
- **Initial acknowledgment**: Within 48 hours
- **Patch release**: Within 7 days for critical vulnerabilities
- **Public disclosure**: After patch release (unless otherwise agreed)

## Security best practices for users

1. **Rotate secrets regularly** — Database passwords, API keys, kubeconfig credentials
2. **Keep dependencies updated** — Monitor GitHub Dependabot alerts
3. **Use private subnets** — RDS should never be publicly accessible
4. **Enable audit logging** — EKS audit logs, RDS Enhanced Monitoring
5. **Restrict image pull** — Use private GHCR repos or configure authentication
6. **Enable encryption** — RDS encryption, EKS secrets encryption at rest

## Known security considerations

- **Terraform state**: Remote state must use S3 with versioning + DynamoDB locking
- **Kubernetes RBAC**: Customize RBAC roles per environment (not shown here; extend `infrastructure/kubernetes/base`)
- **Supply chain**: All container images scanned with Trivy in CI/CD; pin base image versions

## Dependencies

Security updates are tracked via:
- GitHub Dependabot (Python, Go, actions)
- Trivy (container image scanning)
- Manual quarterly audits

Report issues via the GitHub Security Advisory feature or email above.

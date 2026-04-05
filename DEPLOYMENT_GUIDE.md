# Deployment Guide

This guide covers deploying GreenPulse to AWS with Terraform and Kubernetes.

## Prerequisites

- AWS Account with appropriate IAM permissions
- `aws-cli` configured with credentials
- `terraform` >= 1.0
- `kubectl` >= 1.27
- `kustomize` >= 5.0
- Docker (for pushing images to GHCR)

## Step 1: Prepare Terraform Backend

```bash
# Create S3 bucket for state (replace ACCOUNT_ID)
aws s3api create-bucket \
  --bucket greenpulse-tf-state-$(date +%s) \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket greenpulse-tf-state-$(date +%s) \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name greenpulse-tf-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

## Step 2: Configure Terraform

```bash
cd infrastructure/terraform

# Copy and configure backend
cp backend.hcl.example backend.hcl
# Edit backend.hcl with your S3 bucket and region

# Initialize Terraform
terraform init -backend-config=backend.hcl

# Copy and configure variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with:
#   - aws_region: desired AWS region
#   - environment: dev/staging/prod
#   - rds_master_username: admin username
```

## Step 3: Plan and Apply Infrastructure

```bash
# Review plan
terraform plan -out=tfplan

# Apply infrastructure (takes 15-20 minutes)
terraform apply tfplan

# Capture outputs
terraform output -json > outputs.json
CLUSTER_NAME=$(jq -r '.eks_cluster_name.value' outputs.json)
```

## Step 4: Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig \
  --region $(jq -r '.aws_region.value' outputs.json) \
  --name $CLUSTER_NAME

# Verify connection
kubectl cluster-info
kubectl get nodes
```

## Step 5: Create Kubernetes Namespace and Secrets

```bash
# Create namespace
kubectl create namespace greenpulse

# Create database secret
DATABASE_URL="postgres://admin:PASSWORD@greenpulse-rds-endpoint:5432/greenpulse?sslmode=require"
kubectl create secret generic greenpulse-db \
  --namespace=greenpulse \
  --from-literal=DATABASE_URL="$DATABASE_URL"

# Verify
kubectl get secrets -n greenpulse
```

## Step 6: Deploy with Kustomize

```bash
# From repository root
kubectl apply -k infrastructure/kubernetes/base

# Monitor rollout
kubectl rollout status deployment/ingestion-api -n greenpulse
kubectl rollout status deployment/dashboard -n greenpulse
kubectl rollout status deployment/sensor-emulator -n greenpulse
```

## Step 7: Configure GitHub Actions for Auto-Deployment

1. Get kubeconfig as base64:
```bash
cat ~/.kube/config | base64 -w 0 > /tmp/kubeconfig.b64
cat /tmp/kubeconfig.b64
```

2. In GitHub repo settings → Secrets → New repository secret:
   - Name: `KUBE_CONFIG_B64`
   - Value: [paste base64 kubeconfig]

3. Push to `main` branch — deployment will trigger automatically.

## Accessing Services

```bash
# Get LoadBalancer IP for dashboard
kubectl get svc -n greenpulse

# Port-forward for local testing
kubectl port-forward -n greenpulse svc/dashboard 8501:8501
kubectl port-forward -n greenpulse svc/ingestion-api 8080:8080

# View logs
kubectl logs -n greenpulse -l app.kubernetes.io/name=ingestion-api -f
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n greenpulse
kubectl logs <pod-name> -n greenpulse --previous
```

### Database connection issues
```bash
# Verify secret
kubectl get secret greenpulse-db -n greenpulse -o yaml

# Test from pod
kubectl exec -it <ingestion-api-pod> -n greenpulse -- \
  psql "$DATABASE_URL" -c "SELECT 1"
```

### Terraform state conflicts
```bash
# Force unlock (use only if lock is stale)
terraform force-unlock <LOCK_ID>
```

## Cleanup

```bash
# Delete all Kubernetes resources
kubectl delete namespace greenpulse

# Destroy AWS infrastructure
cd infrastructure/terraform
terraform destroy
```

## Multi-Region Deployment

To deploy to a second region:

1. Create new Terraform workspace:
```bash
terraform workspace new prod-us-west-2
```

2. Update `terraform.tfvars` with new region
3. Repeat Steps 3-7 with new cluster name and resources

## Monitoring & Logging

- **CloudWatch**: Logs from EKS and RDS
- **Application Metrics**: Exposed on ingestion-api `/metrics` endpoint (Prometheus)
- **Dashboard**: Streamlit app at ingestion-api LoadBalancer IP
- **HPA Status**: `kubectl get hpa -n greenpulse`

For production, integrate with DataDog, New Relic, or similar observability platforms.

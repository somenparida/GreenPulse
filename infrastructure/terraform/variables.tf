variable "aws_region" {
  description = "Primary AWS region for GreenPulse control plane and data plane."
  type        = string
}

variable "environment" {
  description = "Deployment environment name (e.g. prod, staging)."
  type        = string
}

variable "project_name" {
  description = "Name prefix for tagged resources."
  type        = string
  default     = "greenpulse"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR for the VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "eks_version" {
  description = "Kubernetes version for the EKS control plane."
  type        = string
  default     = "1.29"
}

variable "eks_node_instance_types" {
  description = "EC2 instance types for the managed node group."
  type        = list(string)
  default     = ["t3.medium"]
}

variable "eks_node_desired_size" {
  type    = number
  default = 2
}

variable "eks_node_min_size" {
  type    = number
  default = 1
}

variable "eks_node_max_size" {
  type    = number
  default = 4
}

variable "rds_instance_class" {
  description = "RDS instance class for PostgreSQL."
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  type    = number
  default = 20
}

variable "rds_db_name" {
  type    = string
  default = "greenpulse"
}

variable "rds_master_username" {
  description = "Master username (password generated in Terraform via random_password — never hardcode in repo)."
  type        = string
}

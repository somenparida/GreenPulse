variable "project_name" { type = string }
variable "environment" { type = string }
variable "vpc_cidr" { type = string }

variable "eks_cluster_name" {
  description = "EKS cluster name used for subnet discovery tags."
  type        = string
}

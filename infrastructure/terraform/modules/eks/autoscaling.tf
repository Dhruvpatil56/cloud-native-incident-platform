# Cluster autoscaler integration for Terraform-managed EKS node groups.
# Tags below allow Kubernetes Cluster Autoscaler to discover and scale node groups.

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "autoscaling_enabled" {
  description = "Enable autoscaling discovery tags"
  type        = bool
  default     = true
}

locals {
  autoscaler_tags = {
    "k8s.io/cluster-autoscaler/enabled"                = "true"
    "k8s.io/cluster-autoscaler/${var.cluster_name}"    = "owned"
  }
}

# Attach these tags to managed node groups in this module where applicable.
# Example usage in aws_eks_node_group.tags:
# tags = merge(var.common_tags, local.autoscaler_tags)

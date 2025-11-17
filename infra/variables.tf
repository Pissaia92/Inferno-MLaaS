variable "s3_bucket_name" {
  description = "Name of the S3 bucket for model storage"
  type        = string
  default     = "inferno-mlaas-models"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "inferno-mlaas"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "task_cpu" {
  description = "Fargate task CPU units (e.g., 256, 512)"
  type        = string
  default     = "256"  # 0.25 vCPU
}

variable "task_memory" {
  description = "Fargate task memory in MiB (e.g., 512, 1024)"
  type        = string
  default     = "512"  # 0.5 GB
}

variable "service_desired_count" {
  description = "Desired count for the ECS service"
  type        = number
  default     = 1
}
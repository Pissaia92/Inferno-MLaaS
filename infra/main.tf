terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_s3_bucket" "model_storage" {
  bucket = var.s3_bucket_name
}

resource "aws_ecr_repository" "app_repository" {
  name = var.ecr_repository_name

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
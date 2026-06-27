# terraform-project/bootstrap/main.tf
# Run this ONCE manually before anything else:
#   cd terraform-project/bootstrap
#   terraform init && terraform apply

terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "state" {
  bucket        = "automobiletfstate2026"
  force_destroy = false

  tags = { Name = "automobile-tf-state" }
}

resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "lock" {
  name         = "automobiletflock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = { Name = "automobile-tf-lock" }
}

output "s3_bucket_name"     { value = aws_s3_bucket.state.bucket }
output "dynamodb_table_name" { value = aws_dynamodb_table.lock.name }

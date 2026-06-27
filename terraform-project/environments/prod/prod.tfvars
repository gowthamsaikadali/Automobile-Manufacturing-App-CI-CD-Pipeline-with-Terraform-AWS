# terraform-project/environments/prod/prod.tfvars
# DO NOT put db_username / db_password here — injected by CI/CD from GitHub Secrets

aws_region    = "ap-south-1"
project_name  = "automobile-manufacturing"
environment   = "prod"
instance_type = "t3.micro"
key_pair_name = "automobile-key"    # ← Change to your actual key pair name
db_name       = "automobile_db"

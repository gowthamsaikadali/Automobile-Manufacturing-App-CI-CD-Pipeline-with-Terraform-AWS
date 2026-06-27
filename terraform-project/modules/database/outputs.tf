# sensitive = false so the CI/CD pipeline can read it via terraform output -raw
# The endpoint flows through GitHub Actions job outputs, never hardcoded anywhere
output "rds_endpoint" {
  value = aws_db_instance.main.address
}

output "rds_port" {
  value = aws_db_instance.main.port
}

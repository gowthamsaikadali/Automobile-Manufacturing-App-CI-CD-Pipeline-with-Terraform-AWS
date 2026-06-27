output "instance_public_ip" {
  description = "EC2 public IP — used by deploy job for SSH"
  value       = module.compute.instance_public_ip
}

output "alb_dns_name" {
  description = "ALB DNS — your application's public URL"
  value       = module.alb.alb_dns_name
}

# NOT sensitive — pipeline reads this automatically after apply
# and passes it to the deploy job via GitHub Actions job outputs
output "rds_endpoint" {
  description = "RDS endpoint — automatically passed to deploy job"
  value       = module.database.rds_endpoint
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.network.vpc_id
}

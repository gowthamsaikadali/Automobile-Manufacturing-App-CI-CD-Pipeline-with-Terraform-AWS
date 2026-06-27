output "instance_public_ip" {
  description = "EC2 public IP (dev)"
  value       = module.compute.instance_public_ip
}

output "alb_dns_name" {
  description = "ALB DNS (dev)"
  value       = module.alb.alb_dns_name
}

output "rds_endpoint" {
  description = "RDS endpoint (dev)"
  value       = module.database.rds_endpoint
}

output "vpc_id" {
  description = "VPC ID (dev)"
  value       = module.network.vpc_id
}

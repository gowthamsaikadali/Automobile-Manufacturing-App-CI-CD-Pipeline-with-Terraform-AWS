# terraform-project/environments/prod/main.tf

locals {
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

module "network" {
  source       = "../../modules/network"
  project_name = var.project_name
  environment  = var.environment
  tags         = local.tags
}

module "security" {
  source       = "../../modules/security"
  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.network.vpc_id
  tags         = local.tags
}

module "iam" {
  source       = "../../modules/iam"
  project_name = var.project_name
  environment  = var.environment
  tags         = local.tags
}

module "database" {
  source            = "../../modules/database"
  project_name      = var.project_name
  environment       = var.environment
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  subnet_ids        = module.network.private_subnet_ids
  security_group_id = module.security.rds_sg_id
  tags              = local.tags
}

module "alb" {
  source            = "../../modules/alb"
  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.public_subnet_ids
  security_group_id = module.security.alb_sg_id
  tags              = local.tags
}

module "compute" {
  source            = "../../modules/compute"
  project_name      = var.project_name
  environment       = var.environment
  instance_type     = var.instance_type
  key_pair_name     = var.key_pair_name
  subnet_id         = module.network.public_subnet_ids[0]
  security_group_id = module.security.ec2_sg_id
  iam_profile       = module.iam.instance_profile_name
  target_group_arn  = module.alb.target_group_arn
  db_host           = module.database.rds_endpoint
  db_username       = var.db_username
  db_password       = var.db_password
  db_name           = var.db_name
  secret_key        = var.flask_secret_key
  tags              = local.tags
}

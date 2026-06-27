locals {
  prefix = "auto-mfg-${var.environment}"
}

resource "aws_db_subnet_group" "main" {
  name       = "${local.prefix}-db-subnet-grp"
  subnet_ids = var.subnet_ids
  tags       = merge(var.tags, { Name = "${local.prefix}-db-subnet-grp" })
}

resource "aws_db_instance" "main" {
  identifier             = "${local.prefix}-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_type           = "gp2"
  storage_encrypted      = false

  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [var.security_group_id]

  backup_retention_period = 0
  skip_final_snapshot     = true
  deletion_protection     = false
  publicly_accessible     = false
  multi_az                = false

  tags = merge(var.tags, { Name = "${local.prefix}-db" })
}

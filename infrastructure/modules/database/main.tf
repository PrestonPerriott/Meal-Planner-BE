# Database Module
# This module creates a PostgreSQL database instance in AWS

# Create a security group for the database
resource "aws_security_group" "database" {
  name_prefix = "${var.environment}-db-sg"
  description = "Security group for the database"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {
  identifier           = "${var.environment}-db"
  allocated_storage    = 20
  storage_type         = "gp3"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = var.db_instance_class
  db_name             = var.db_name
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.database.name
}

resource "aws_db_subnet_group" "database" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.private_subnet_ids
}

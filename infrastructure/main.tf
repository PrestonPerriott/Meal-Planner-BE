# Configure AWS provider
#provider "aws" {
#  region = var.aws_region
#}

# Networking Module
module "networking" {
  source = "./modules/networking"
  
  environment         = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

# Compute Module for Ollama
module "compute" {
  source = "./modules/compute"
  
  environment         = var.environment
  vpc_id             = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_subnet_ids
  instance_type      = var.ollama_instance_type
  key_name          = var.key_name
  ami_id            = var.ami_id

  tags = {
    Environment = var.environment
    Terraform   = "true"
    Service     = "ollama"
  }
}

# Database Module
module "database" {
  source = "./modules/database"
  
  environment         = var.environment
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  
  db_instance_class  = var.db_instance_class
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
}

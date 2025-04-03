output "ollama_lb_dns" {
  description = "DNS name of the Ollama load balancer"
  value       = module.compute.lb_dns_name
}

output "rds_endpoint" {
  description = "Endpoint of the RDS instance"
  value       = module.database.db_endpoint
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

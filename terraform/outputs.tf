output "backend_public_ip" {
  value       = aws_instance.backend.public_ip
  description = "The public IP of the backend server"
}

output "db_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "The connection endpoint for the RDS instance"
}

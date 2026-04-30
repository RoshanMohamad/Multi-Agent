variable "aws_region" {
  description = "AWS region"
  type        = "string"
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = "string"
  default     = "multi-agent-system"
}

variable "instance_type" {
  description = "EC2 instance type for backend/Ollama"
  type        = "string"
  default     = "t3.large"
}

variable "db_password" {
  description = "RDS root password"
  type        = "string"
  sensitive   = true
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [aws_subnet.public.id] # In production, use private subnets in 2 AZs

  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  db_name              = "multiagentdb"
  engine               = "postgres"
  engine_version      = "15"
  instance_class       = "db.t3.micro"
  username             = "postgres"
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
  publicly_accessible  = true # For demo purposes, keep false in strict production
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  tags = {
    Name = "${var.project_name}-db"
  }
}

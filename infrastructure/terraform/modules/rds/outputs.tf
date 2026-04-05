output "db_endpoint" {
  value     = aws_db_instance.this.address
  sensitive = true
}

output "db_port" {
  value = aws_db_instance.this.port
}

output "db_name" {
  value = aws_db_instance.this.db_name
}

output "master_username" {
  value     = aws_db_instance.this.username
  sensitive = true
}

output "master_password" {
  value     = random_password.master.result
  sensitive = true
}

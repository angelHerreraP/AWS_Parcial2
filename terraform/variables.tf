# variables.tf
variable "key_name" {
  description = "Nombre de la llave SSH para EC2"
  type        = string
}

variable "db_username" {
  description = "Usuario de la base de datos"
  type        = string
}

variable "db_password" {
  description = "Password de la base de datos"
  type        = string
  sensitive   = true
}

variable "ssh_allowed_ip" {
  description = "IP/CIDR desde donde se permite SSH (ejemplo: 189.123.45.67/32)"
  type        = string
  default     = "0.0.0.0/0" 
}# Cambia el default por mi ip si quieres entrear con seguridad

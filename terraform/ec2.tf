# ec2.tf
resource "aws_instance" "web" {
  ami           = "ami-0c101f26f147fa7fd" # Amazon Linux 2 AMI (us-east-1)
  instance_type = "t2.micro"
  subnet_id     = module.vpc.public_subnets[0]
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name = var.key_name

  tags = {
    Name = "WebServer"
  }

  user_data = templatefile("${path.module}/user_data.tpl", {
    db_host = aws_db_instance.default.endpoint,
    db_user = var.db_username,
    db_pass = var.db_password,
    db_name = aws_db_instance.default.db_name
  })
}

# Security group for Ollama instances
resource "aws_security_group" "ollama" {
  name_prefix = "${var.environment}-ollama-sg"
  vpc_id      = var.vpc_id

  # Allow inbound traffic from ALB
  ingress {
    from_port       = var.ollama_port
    to_port         = var.ollama_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-ollama-sg"
  })
}

# Security group for Application Load Balancer
resource "aws_security_group" "alb" {
  name_prefix = "${var.environment}-alb-sg"
  vpc_id      = var.vpc_id

  # Allow inbound HTTPS traffic
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound HTTP traffic
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-alb-sg"
  })
}

resource "aws_launch_template" "ollama" {
  name_prefix   = "ollama-template"
  image_id      = var.ami_id  # Use a GPU-enabled AMI
  instance_type = var.instance_type

  user_data = base64encode(<<-EOF
              #!/bin/bash
              curl -fsSL https://ollama.com/install.sh | sh
              ollama pull deepseek-r1:14b
              EOF
  )

  vpc_security_group_ids = [aws_security_group.ollama.id]
  
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size = 100
      volume_type = "gp3"
    }
  }
}

resource "aws_autoscaling_group" "ollama" {
  desired_capacity    = 1
  max_size           = 1
  min_size           = 1
  target_group_arns  = [aws_lb_target_group.ollama.arn]
  vpc_zone_identifier = var.private_subnet_ids

  launch_template {
    id      = aws_launch_template.ollama.id
    version = "$Latest"
  }
}

resource "aws_lb" "ollama" {
  name               = "ollama-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = var.public_subnet_ids
}

resource "aws_lb_target_group" "ollama" {
  name_prefix = "olm-tg"
  port         = var.ollama_port
  protocol     = "HTTP"
  target_type  = "instance"
  vpc_id       = var.vpc_id
}
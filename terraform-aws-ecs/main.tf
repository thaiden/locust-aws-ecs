
/* Cluster definition, which is used in autoscaling.tf */
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.cluster_name}-ecs"
}

/**
 * Resources.
 */
provider "aws" {
  region = "${var.aws_region}"
}

module "vpc" {
  source = "github.com/terraform-community-modules/tf_aws_vpc"

  name = "${var.security_vpc_name}"

  cidr = "10.0.0.0/16"
  private_subnets = "${var.instance_list_private_subnet_id}"
  public_subnets  = "${var.instance_list_public_subnet_id}"
  enable_dns_hostnames = "true"
  enable_dns_support = "true"
  enable_nat_gateway = "true"

  azs      = "${var.instance_list_available_zone}"

  tags {
    "Terraform" = "true"
    "Environment" = "${var.environment}"
  }
}

resource "aws_security_group" "ecs_cluster_group" {
  name        = "${var.project}-${var.environment}-cluster-security-group"
  description = "${var.project}-${var.environment}-cluster-security-group"
  vpc_id      = "${module.vpc.vpc_id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Project     = "${var.project}"
    Environment = "${var.environment}"
    ClusterName = "${title(var.project)}-${var.environment}-${var.cluster_name}-cluster"
  }
}

data "template_file" "user_data" {
  template = "${file("${path.module}/userdata.sh")}"

  vars {
    project      = "${var.project}"
    environment  = "${var.environment}"
    cluster_name = "${var.cluster_name}"
  }
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
    name = "${var.name_prefix}_ecs_instance_profile"
    role = "${aws_iam_role.ecs_instance_role.name}"
}

resource "aws_iam_role" "ecs_instance_role" {
    name = "${var.name_prefix}_ecs_instance_role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs_instance_role_policy" {
    name = "${var.name_prefix}_ecs_instance_role_policy"
    role = "${aws_iam_role.ecs_instance_role.id}"
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:*",
        "ecr:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ] 
}
EOF
}

/**
 * IAM Role for ECS Service
 */

resource "aws_iam_role" "ecs_service_role" {
    name = "${var.name_prefix}_ecs_service_role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ecs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "ecs_service_role_policy" {
    name = "${var.name_prefix}_ecs_service_role"
    role = "${aws_iam_role.ecs_service_role.id}"
    policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "elasticloadbalancing:*",
        "ec2:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
EOF
}


data "aws_ami" "latest" {
  most_recent = true

  filter {
    name   = "name"
    values = ["${var.aws_ami_latest_filter}"]
  }

  owners = ["${var.aws_ami_latest_owner}"]
}

data "template_file" "autoscaling_user_data" {
    template = "${file("autoscaling/autoscaling_user_data.tpl")}"
    vars {
        ecs_cluster = "${aws_ecs_cluster.ecs_cluster.name}"
    }
}

resource "aws_launch_configuration" "ecs" {
    name = "${aws_ecs_cluster.ecs_cluster.name}-launch_configuration"
    image_id = "${var.instance["ami"] == "latest" ? data.aws_ami.latest.id : var.instance["ami"]}"
    instance_type = "${var.instance["type"]}"
    iam_instance_profile = "${aws_iam_instance_profile.ecs_instance_profile.arn}"
    key_name = "${var.instance["key_name"]}"
    security_groups = ["${aws_security_group.ecs_cluster_group.id}"]
    associate_public_ip_address = true
    user_data = "${data.template_file.autoscaling_user_data.rendered}"

     lifecycle {
        create_before_destroy = true
    }
}

resource "aws_autoscaling_group" "ecs-scalling" {
  availability_zones = "${var.instance_list_available_zone}"
  vpc_zone_identifier = ["${module.vpc.public_subnets}"]
  name = "${aws_ecs_cluster.ecs_cluster.name}-ecs-scalling"
  min_size = "${var.cluster_size}"
  max_size = "${var.cluster_size_max}"
  desired_capacity = "${var.cluster_size_desired_capacity}"
  health_check_type = "EC2"
  force_delete              = true
  
  launch_configuration = "${aws_launch_configuration.ecs.name}"
  health_check_grace_period = "${var.health_check_grace_period}"

  tag {
    key = "Env"
    value = "${var.environment}"
    propagate_at_launch = true
  }

  tag {
    key = "Name"
    value =  "${aws_ecs_cluster.ecs_cluster.name}"
    propagate_at_launch = true
  }
}

resource "aws_elb" "service_elb" {
  name = "${var.project}-${var.environment}"
  subnets = ["${module.vpc.public_subnets}"]
  connection_draining = true
  cross_zone_load_balancing = true
  
  security_groups = [
    "${aws_security_group.ecs_cluster_group.id}"    
  ]

  listener {
    instance_port = "${var.host_port}"
    instance_protocol = "http"
    lb_port = "${var.lb_port}"
    lb_protocol = "http"
  }

  listener {
    instance_port = "${var.slave_port_1}"
    instance_protocol = "tcp"
    lb_port = "${var.slave_port_1}"
    lb_protocol = "tcp"
  }

  listener {
    instance_port = "${var.slave_port_2}"
    instance_protocol = "tcp"
    lb_port = "${var.slave_port_2}"
    lb_protocol = "tcp"
  }

  health_check {
    healthy_threshold = 2
    unhealthy_threshold = 10
    target = "HTTP:${var.host_port}/"
    interval = 5
    timeout = 4
  }
}

/* ECS service definition */
resource "aws_ecs_service" "master_service" {
    name = "${var.name_prefix}_master_service"
    cluster = "${aws_ecs_cluster.ecs_cluster.id}"
    task_definition = "${aws_ecs_task_definition.master_definition.arn}"
    desired_count = "1"
    deployment_minimum_healthy_percent = "${var.minimum_healthy_percent}"
    iam_role = "${aws_iam_role.ecs_service_role.name}"

    load_balancer {
        elb_name = "${aws_elb.service_elb.id}"
        container_name = "locust-master"
        container_port = "${var.host_port}"
    }

    lifecycle {
        create_before_destroy = true
    }
}

resource "aws_ecs_task_definition" "master_definition" {
    family = "${var.name_prefix}_master"
    container_definitions = "${data.template_file.task_master.rendered}"

    lifecycle {
        create_before_destroy = true
    }
}

data "template_file" "task_master" {
    template= "${file("task-definitions/master.json.tmpl")}"

    vars {
        image = "${var.docker_img}"
        docker_port = "${var.docker_port}"
        host_port = "${var.host_port}"       
        target_url = "${var.target_url}"  
        target_port = "${var.target_port}" 
    }
}

// Slave
resource "aws_ecs_service" "slave_service" {
    name = "${var.name_prefix}_slave_service"
    cluster = "${aws_ecs_cluster.ecs_cluster.id}"
    task_definition = "${aws_ecs_task_definition.slave.arn}"
    desired_count = "${var.slave_size_desired_capacity}"
    depends_on = ["aws_ecs_service.master_service"]    
}

data "template_file" "task_slave" {
    template= "${file("task-definitions/slave.json.tmpl")}"

    vars {
        image = "${var.docker_img}"      
        target_url = "${var.target_url}"  
        target_port = "${var.target_port}" 
        master_host = "${aws_elb.service_elb.dns_name}"
    }
}

resource "aws_ecs_task_definition" "slave" {
  family = "${var.name_prefix}_slave"
  container_definitions = "${data.template_file.task_slave.rendered}"
}

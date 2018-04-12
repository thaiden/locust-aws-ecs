/**
 * Required Variables.
 */

 variable "name_prefix" {
    default = "locust"
    description = "Name prefix for this environment."
}

variable "aws_region" {
    default = "us-west-1"
    description = "Determine AWS region endpoint to access."
}

variable "project" {
  description = "Name of project"
  default     = "locust-load-test"
}

variable "environment" {
  description = "Name of environment (i.e. dev, test, prod)"
  default     = "loada1-aws"
}

variable "security_vpc_name" { default = "locust-loada-vpc"}

variable "cluster_name" { default = "locust-aws-loada"}

variable "instance" {
  type = "map"

  default = {
    key_name  = "locust"
    ami       = "ami-7d664a1d"
    type      = "t2.small"
  }
}

variable "instance_list_public_subnet_id" {
  type    = "list"
  default = ["10.0.101.0/24"]
}

variable "instance_list_private_subnet_id" {
  type    = "list"
  default = ["10.0.1.0/24"]
}

variable "instance_list_available_zone" {
  type    = "list"
  default = ["us-west-1a"]
}

variable "cluster_size" {
  description = "Size of cluster"
  default     = 3
}

variable "cluster_size_max" {
  description = "Max size of cluster"
  default     = 8
}

variable "cluster_size_desired_capacity" {
  description = "Desired size of cluster"
  default     = 5
}

variable "slave_size_desired_capacity" {
  description = "Desired size of cluster"
  default     = 4
}

variable "minimum_healthy_percent" {
  default = "50"
}

variable "public_subnet_index" {
  description = "Number of public subnets"
  default     = 0
}

variable "aws_ami_latest_filter" {
  description = "Filter for take the last aws ami"
  default     = "amzn-ami-*-amazon-ecs-optimized"
}

variable "aws_ami_latest_owner" {
  description = "Owner of the last aws ami"
  default     = "amazon"
}

variable "associate_public_ip_address" {
  description = "Associate a public ip address"
  default     = true
}

variable "health_check_grace_period" {
    default = "300"
    description = "Time after instance comes into service before checking health"
}

variable "target_url" {
  default = "<put-url-pointing-service-you-want-to-test>"
}

variable "target_port" {
  default = "9200"
}

variable "docker_port" {
  default = "8089"
}

variable "host_port" {
  default = "8089"
}

variable "docker_img" {
  default = "<ecs image repo>/<name of image>"
}

variable "lb_port" { 
  default = "8089"
}

variable "slave_port_1" { 
  default = "5557"
}

variable "slave_port_2" {
   default = "5558"
}
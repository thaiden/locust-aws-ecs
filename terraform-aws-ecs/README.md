# Prerequisites 
Current script assumes you have ECR repository setup and docker image created&pushed to it. Also it assumes that AWS KeyPair is named **locust**.
 - Info on how to setup KeyPair can be found [Here](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
 - Info on how to setup ECR docker repository is [Here](http://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html)

# Description
Plan is to allow ECS cluster creation with tasks and services using docker images from ECR respository

 - to plan : `make plan`
 - to apply : `make apply`
 - to destroy : `make destroy`

###Note 
Scripts are based on [Link](https://github.com/tierratelematics/terraform-aws-ecs)
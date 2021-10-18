# Configure the AWS Provider

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical

}

resource "aws_instance" "web" {
  ami          		 = data.aws_ami.ubuntu.id
  instance_type 	 = "t3.micro"

  tags = {
    Name = "HelloWorld"
  }
}

# Create a VPC
resource "aws_vpc" "example" {
  cidr_block = "10.0.0.0/16"
}

provider "aws" {
  region  = "eu-central-1"
  allowed_account_ids = ["464791636075"]
  shared_credentials_file = "$HOME/.aes/credentials"
  profile = "lereklerik"
}


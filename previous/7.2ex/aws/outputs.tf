data "aws_caller_identity" "current" {}

output "account_id" {
  value = "${data.aws_caller_identity.current.account_id}"
}

output "caller_arn" {
  value = "${data.aws_caller_identity.current.arn}"
}

output "caller_user" {
  value = "${data.aws_caller_identity.current.user_id}"
}

output "instance_ip_addr" {
  value = "${aws_instance.web.private_ip}"
  description = "The private IP address of the main server instance."
}

output "instance_id" {
description = "ID of the EC2 instance"
value = "${aws_instance.web.id}"
}

output "instance_public_ip" {
description = "Public IP address of the EC2 instance"
value = "${aws_instance.web.public_ip}"
}


variable "resource_group_location" {
  type    = string
  default = "eastus"
}

variable "resource_group_name" {
  type    = string
  default = "ffury"
}

variable "subscription_id" {
  # mettre TF_VAR_subscription_id environment variable
}

variable "environment" {
  type    = string
  default = "dev"
  # mettre TF_VAR_environment environment variable
}

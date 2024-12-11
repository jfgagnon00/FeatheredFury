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

variable "service_principal_password" {
  # mettre TF_VAR_service_principal_password environment variable
}

variable "environment" {
  type    = string
  default = "dev"
  # mettre TF_VAR_environment environment variable
}

variable "application_name" {
  type    = string
  default = "ffury-application"
}

variable "api_name" {
  type    = string
  default = "ffury-api"
}

variable "resource_group_location" {
  type    = string
  default = "canadaeast"
}

variable "resource_group_name" {
  type    = string
  default = "ffury"
}

variable "environment" {
  type    = string
  default = "dev"
  # mettre TF_VAR_environment environment variable

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Valeurs possible: dev, staging ou production."
  }
}

variable "subscription_id" {
  # mettre TF_VAR_subscription_id environment variable
}

variable "tenant_id" {
  # mettre TF_VAR_tenant_id environment variable
}

variable "client_id" {
  # mettre TF_VAR_client_id environment variable
}

variable "secret" {
  # mettre TF_VAR_client environment variable
}

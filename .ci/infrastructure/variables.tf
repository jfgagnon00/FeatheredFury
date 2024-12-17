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

############ Configuration

variable "subscription_id" {
  # mettre TF_VAR_subscription_id environment variable
}

variable "tenant_id" {
  # mettre TF_VAR_tenant_id environment variable
}

variable "container_cpu_count" {
  type    = number
  default = 1
  # mettre TF_VAR_container_cpu_count variable
}

variable "container_memory_gb" {
  type    = number
  default = 2
  # mettre TF_VAR_container_memory_gb variable
}

variable "container_environment_variables" {
  type    = list(string)
  default = []
}

variable "container_tcp_port" {
  type  = number
  default = 80
}

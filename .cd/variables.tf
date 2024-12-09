variable "resource_group_location" {
  type    = string
  default = "eastus"
}

variable "resource_group_name_prefix" {
  type    = string
  default = "ffury"
}

variable "application_name" {
  type    = string
  default = "ffury-application"
}

variable "api_name" {
  type    = string
  default = "ffury-api"
}

variable "service_principal_client_id" {
  type    = string
  default = "<appId>" # Use the appId from the service principal
}

variable "service_principal_client_secret" {
  type    = string
  default = "<password>" # Use the appId from the service principal
}

variable "service_principal_tenant_id" {
  type    = string
  default = "<tenant>" # Use the tenant ID from the service principal
}

variable "service_principal_subscription_id" {
  type    = string
  default = "<subscription-id>" # Optional: Specify subscription if necessary
}

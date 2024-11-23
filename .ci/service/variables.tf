variable "resource_group_name" {
  description = "Nom du groupe de ressources"
  type        = string
  default     = "myResourceGroup"
}

variable "location" {
  description = "Emplacement Azure"
  type        = string
  default     = "East US"
}

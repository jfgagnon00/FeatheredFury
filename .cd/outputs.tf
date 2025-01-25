############ Docker

output "azure_container_registry_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "Azure Container Registry login server"
}

output "azure_container_username" {
  value       = azurerm_container_registry.acr.admin_username
  sensitive   = true
  description = "Azure Container Registry login server"
}

output "azure_container_password" {
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
  description = "Azure Container Registry login server"
}

############ Application + Service

output "web_app_url" {
  value       = azurerm_container_group.acg.fqdn
  sensitive   = true
  description = "URL pour l'application"
}

############ Monitoring

output "storage_connection_string" {
    value     = azurerm_storage_account.asa.primary_connection_string
    sensitive = true
}

############ General

output "subscription" {
    value = data.azurerm_subscription.current.id
}

output "environment" {
    value = "${var.environment}"
}

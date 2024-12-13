############ Docker

output "azure_container_registry_login_server" {
  value       = azurerm_container_registry.container_registry.login_server
  description = "Azure Container Registry login server"
}

############ Service Principal

output "service_principal_app_id" {
  value       = azuread_application.ffury.client_id
  description = "Service Principal AppId"
}

output "service_principal_secret" {
  value       = azuread_service_principal_password.ffury.value
  sensitive   = true
  description = "Service Principal Secret"
}

output "service_principal_tenant_id" {
  value       = data.azuread_client_config.config.tenant_id
  description = "Service Principal TenantId"
}

############ Web Application

output "web_application" {
  value       = azurerm_linux_web_app.ffury.default_hostname
  sensitive   = true
  description = "URL pour l'application"
}
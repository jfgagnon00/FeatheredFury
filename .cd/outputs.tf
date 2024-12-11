############ Docker

output "azure_container_registry_login_server" {
  value = azurerm_container_registry.acr.login_server
   description = "Azure Container Registry login server"
}

############ Service Principal

# output "service_principal_app_id" {
#   value = azuread_application.sp.application_id
#   description = "Service Principal AppId"
# }

output "service_principal_secret" {
  value = azuread_service_principal_password.sp.value
  sensitive = true
  description = "Service Principal Secret"
}

output "service_principal_tenant_id" {
  value = data.azurerm_client_config.config.tenant_id
  description = "TService Principal TenantId"
}

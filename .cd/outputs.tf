output "resource-group" {
  value = azurerm_resource_group.ffury.name
}

output "acr-name" {
  value = azurerm_container_registry.ffury.name
}

output "acr-login_server" {
  value = azurerm_container_registry.ffury.login_server
}

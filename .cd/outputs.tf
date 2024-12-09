output "resource_group_name" {
  value = azurerm_resource_group.ffury.name
}

output "container_registry_name" {
  value = azurerm_container_registry.ffury.name
}

output "container_registry_login_server" {
  value = azurerm_container_registry.ffury.login_server
}
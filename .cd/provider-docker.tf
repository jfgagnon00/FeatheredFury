provider "docker" {
  registry_auth {
    address  = "${azurerm_container_registry.ffury.login_server}"
    username = var.service_principal_client_id
    password = var.service_principal_client_secret
  }
}

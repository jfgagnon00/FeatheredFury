############ Docker

locals {
  container_registry_name = "${var.resource_group_name}${var.environment}acr"
  container_instance_name = "${var.resource_group_name}-${var.environment}-instance"
  
  dns                     = "${var.resource_group_name}-${var.environment}"

  application_name        = "${var.resource_group_name}-${var.environment}-web-app"
  image_name              = "${azurerm_container_registry.acr.login_server}/${var.resource_group_name}-web_app:latest"
}

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "acr" {
  name                = local.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  admin_enabled       = true
  sku                 = "Basic"
}

resource "azurerm_container_group" "acg" {
  name                = local.container_instance_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "Public"
  os_type             = "Linux"
  sku                 = "Standard"

  image_registry_credential {
      username = azurerm_container_registry.acr.admin_username
      password = azurerm_container_registry.acr.admin_password
      server   = azurerm_container_registry.acr.login_server
  }

  container {
    name   = local.application_name
    image  = local.image_name
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }
  }
}
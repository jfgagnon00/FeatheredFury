############ Docker

locals {
  container_registry_name = "${var.resource_group_name}acr${var.environment}"
}

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "container_registry" {
  name                = local.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
}


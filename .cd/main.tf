resource "azurerm_resource_group" "ffury" {
  name     = var.resource_group_name_prefix
  location = var.resource_group_location
}

resource "azurerm_container_registry" "ffury" {
  name                = "${azurerm_resource_group.ffury.name}acr"
  resource_group_name = "${azurerm_resource_group.ffury.name}"
  location            = azurerm_resource_group.ffury.location
  sku                 = "Standard"
}

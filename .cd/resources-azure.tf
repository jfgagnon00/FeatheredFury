resource "azurerm_resource_group" "arg" {
  name     = var.resource_group_name_prefix
  location = var.resource_group_location
}

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "acr" {
  name                = "${azurerm_resource_group.arg.name}acr"
  resource_group_name = azurerm_resource_group.arg.name
  location            = azurerm_resource_group.arg.location
  sku                 = "Basic"
}

# # Azure Container Instances (ACI) pour exécuter les conteneurs
# resource "azurerm_container_group" "aci" {
#   name                = "${azurerm_resource_group.arg.name}aci"
#   location            = azurerm_resource_group.arg.location
#   resource_group_name = azurerm_resource_group.arg.name
#   os_type             = "Linux"
  
#   container {
#     name   = "FeatheredFury-Application"
#     image  = "feathered-fury_application:latest"
#     cpu    = "0.5"
#     memory = "1.5"

#     environment_variables = {
#       #TODO : "EXAMPLE_ENV_VAR" = "value"
#     }
#   }

#   tags = {
#     environment = "staging"
#   }
# }

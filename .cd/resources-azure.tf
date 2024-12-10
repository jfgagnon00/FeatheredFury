# Azure Service Principal et Azure Resource Group
# sont assumes deja cree

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "acr" {
  name                = "${var.resource_group_name}acr"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  sku                 = "Basic"
}

# # Azure Container Group (ACG) pour exécuter les conteneurs
# resource "azurerm_container_group" "acg" {
#   name                = "${var.resource_group_name}acg"
#   location            = var.resource_group_location
#   resource_group_name = var.resource_group_name
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

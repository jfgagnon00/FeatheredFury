############ Config

# Obtenir les configs
data "azurerm_client_config" "config" {
}

############ Resource Group

# Azure Resource Group
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = var.resource_group_name
}

############ Service Principal

# Azure AD Application - necessaire pour la creation du Service Principal
resource "azuread_application" "spa" {
  display_name = "${var.resource_group_name}-service-principal"
}

# Azure AD Service Principal - lie a l'application
resource "azuread_service_principal" "sp" {
  client_id = azuread_application.spa.id
}


resource "random_password" "sp_secret" {
  length  = 32
  special = true
  override_special = "_%@"
}



# Service Principal Password - authentication
resource "azuread_service_principal_password" "sp" {
  service_principal_id = azuread_service_principal.sp.id
}

# Service Principal - Contributor Resource Group Level
resource "azurerm_role_assignment" "spr" {
  principal_id         = azuread_service_principal.sp.id
  role_definition_name = "Contributor"
  scope                = "/subscriptions/${var.subscription_id}/resourceGroups/${azurerm_resource_group.rg.name}"
}

############ Docker

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

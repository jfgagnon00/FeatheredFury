############ Config

data "azuread_client_config" "config" {
}

############ Alias

locals {
  application_name    = "${var.resource_group_name}-application-${var.environment}"
  resource_group_name = "${var.resource_group_name}-${var.environment}"
  acr_name            = "${var.resource_group_name}acr${var.environment}"
  owners              = [data.azuread_client_config.config.object_id]
}

############ Resource Group

# Azure Resource Group
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = local.resource_group_name
}

############ Service Principal

# Azure AD Application - necessaire pour la creation du Service Principal
resource "azuread_application" "ffury" {
  display_name = local.application_name
  owners       = local.owners
}

# Azure AD Service Principal - lie a l'application
resource "azuread_service_principal" "ffury" {
  client_id = azuread_application.ffury.client_id
  owners    = local.owners
}

# Service Principal Password - authentication
resource "azuread_service_principal_password" "ffury" {
  service_principal_id = azuread_service_principal.ffury.id
  end_date             = timeadd(timestamp(), "8760h") # expire dans 1 an
}

# Service Principal - Contributor Resource Group Level
resource "azurerm_role_assignment" "ffury" {
  principal_id         = azuread_service_principal.ffury.object_id
  role_definition_name = "Contributor"
  scope                = "/subscriptions/${var.subscription_id}/resourceGroups/${azurerm_resource_group.rg.name}"
}

# ############ Docker

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "acr" {
  name                = local.acr_name
  resource_group_name = local.resource_group_name
  location            = var.resource_group_location
  sku                 = "Basic"
}

# # # Azure Container Group (ACG) pour exécuter les conteneurs
# # resource "azurerm_container_group" "acg" {
# #   name                = "${var.resource_group_name}acg"
# #   location            = var.resource_group_location
# #   resource_group_name = var.resource_group_name
# #   os_type             = "Linux"
  
# #   container {
# #     name   = "FeatheredFury-Application"
# #     image  = "feathered-fury_application:latest"
# #     cpu    = "0.5"
# #     memory = "1.5"

# #     environment_variables = {
# #       #TODO : "EXAMPLE_ENV_VAR" = "value"
# #     }
# #   }

# #   tags = {
# #     environment = "staging"
# #   }
# # }





############ Config

data "azuread_client_config" "config" {
}

############ Alias

locals {
  application_name     = "${var.resource_group_name}-application-${var.environment}"
  resource_group_name  = "${var.resource_group_name}-${var.environment}"
  owners               = [data.azuread_client_config.config.object_id]
}

############ Resources + Auth

# Resource Group
resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = local.resource_group_name
}

############ Service Principal

# Active Directory Application - necessaire pour la creation du Service Principal
resource "azuread_application" "ffury" {
  display_name = local.application_name
  owners       = local.owners
}

# Active Directory Service Principal - lie a l'application
resource "azuread_service_principal" "ffury" {
  client_id = azuread_application.ffury.client_id
  owners    = local.owners
}

# Service Principal Password - authentication
resource "azuread_service_principal_password" "ffury" {
  service_principal_id = azuread_service_principal.ffury.id
  end_date             = timeadd(timestamp(), "8760h") # expire dans 1 an
}

# Service Principal Roles - Contributor pour Resource Group
resource "azurerm_role_assignment" "ffury" {
  principal_id         = azuread_service_principal.ffury.object_id
  role_definition_name = "Contributor"
  scope                = "/subscriptions/${var.subscription_id}/resourceGroups/${azurerm_resource_group.rg.name}"
}

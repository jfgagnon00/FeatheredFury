############ Alias

locals {
  resource_group_name  = "${var.resource_group_name}-${var.environment}-rg"
}

############ Resource Group

resource "azurerm_resource_group" "rg" {
  location = var.resource_group_location
  name     = local.resource_group_name
}

import {
  to = azurerm_resource_group.rg
  id = "/subscriptions/${data.azurerm_subscription.current.id}/resourceGroups/${local.resource_group_name}"
}

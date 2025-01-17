############ Alias

locals {
    resource_group_name  = "${var.resource_group_name}-${var.environment}-rg"
    storage_account_name = "${var.resource_group_name}${var.environment}asa"
}

############ Resource Group

resource "azurerm_resource_group" "rg" {
    location = var.resource_group_location
    name     = local.resource_group_name
}

############ Blob Storage

resource "azurerm_storage_account" "asa" {
    name                     = local.storage_account_name
    resource_group_name      = azurerm_resource_group.rg.name
    location                 = azurerm_resource_group.rg.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

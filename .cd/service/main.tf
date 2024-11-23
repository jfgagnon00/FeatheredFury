provider "azurerm" {
  features {}
}

# 1. Création du groupe de ressources
resource "azurerm_resource_group" "rg" {
  name     = "myResourceGroup"
  location = "East US"
}

# 2. Création de Azure Container Registry (ACR)
resource "azurerm_container_registry" "acr" {
  name                = "mydockerregistry"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
}

# 3. Création de Blob Storage
resource "azurerm_storage_account" "blob_storage" {
  name                     = "mystorageaccount"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier              = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "blob_container" {
  name                  = "myblobcontainer"
  storage_account_name  = azurerm_storage_account.blob_storage.name
  container_access_type = "private"
}

# 4. Création de Azure SQL Database (Serverless)
resource "azurerm_sql_server" "sql_server" {
  name                         = "mysqlserver"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login         = "sqladmin"
  administrator_login_password = "Password123!" # Utiliser un secret dans Key Vault en production
}

resource "azurerm_sql_database" "sql_db" {
  name                = "mydatabase"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_sql_server.sql_server.location
  server_name         = azurerm_sql_server.sql_server.name
  sku_name            = "BC_Gen5_1" # Serverless SKU
  max_size_gb         = 5
}

# 5. Création de Azure Key Vault pour stocker les secrets
resource "azurerm_key_vault" "keyvault" {
  name                        = "mykeyvault"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
}

# 6. Création du Network Security Group (NSG) et Virtual Network (VNet)
resource "azurerm_virtual_network" "vnet" {
  name                = "myVNet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_network_security_group" "nsg" {
  name                = "myNSG"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# 7. Configuration de Azure Container Instances (ACI) pour exécuter les conteneurs
resource "azurerm_container_group" "aci" {
  name                = "mycontgroup"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  
  container {
    name   = "mycontainer"
    image  = "yourdockerimage"  # Remplacer par l'image Docker à utiliser
    cpu    = "0.5"
    memory = "1.5"

    environment_variables = {
      "EXAMPLE_ENV_VAR" = "value"
    }
  }

  tags = {
    environment = "production"
  }
}

# 8. Déploiement d'Azure Active Directory - pour gestion des identités
resource "azurerm_client_config" "example" {
  # Utilisation de l'authentification via Azure CLI pour simplifier la gestion des identités
}

output "acr_url" {
  value = azurerm_container_registry.acr.login_server
}

output "sql_database_connection_string" {
  value = "Server=${azurerm_sql_server.sql_server.fully_qualified_domain_name};Database=${azurerm_sql_database.sql_db.name};User Id=sqladmin;Password=Password123!" # A sécuriser
}

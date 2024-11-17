Voici un script Terraform de base pour initialiser les services Azure que vous avez mentionnés, en tenant compte de vos besoins : Azure Container Registry, Azure Container Instances, Azure Blob Storage, Azure SQL Database, et des services de sécurité comme Azure Key Vault, Azure Active Directory, etc.

### Prérequis
1. Vous devez avoir un **compte Azure** et avoir configuré l'authentification avec **Terraform** (via `az login`).
2. Vous devez installer **Terraform** sur votre machine.

### Structure de votre projet Terraform
La structure de votre projet Terraform pourrait ressembler à ceci :

```
azure-setup/
│
├── main.tf        # Le script principal Terraform
├── variables.tf   # Définir les variables utilisées
├── outputs.tf     # Définir les sorties
└── terraform.tfvars # Variables avec vos valeurs spécifiques
```

### 1. **`main.tf`** : Script Terraform principal

```hcl
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
```

### 2. **`variables.tf`** : Définir les variables

```hcl
variable "resource_group_name" {
  description = "Nom du groupe de ressources"
  type        = string
  default     = "myResourceGroup"
}

variable "location" {
  description = "Emplacement Azure"
  type        = string
  default     = "East US"
}
```

### 3. **`terraform.tfvars`** : Définir les valeurs spécifiques

```hcl
resource_group_name = "myResourceGroup"
location = "East US"
```

### 4. **Commandes Terraform** :

1. Initialiser votre configuration Terraform :
   ```bash
   terraform init
   ```

2. Vérifier le plan de déploiement :
   ```bash
   terraform plan
   ```

3. Appliquer la configuration pour créer les ressources :
   ```bash
   terraform apply
   ```

### Explication rapide des ressources :
- **Azure Container Registry (ACR)** : Un registre privé pour stocker vos images Docker.
- **Azure Container Instances (ACI)** : Permet de déployer et d'exécuter des conteneurs sur demande sans gestion d'infrastructure.
- **Azure Blob Storage** : Stockage d'objets pour vos fichiers de données (25 Go dans votre cas).
- **Azure SQL Database** : Une base de données SQL avec un plan **serverless** pour s'ajuster aux besoins de charge.
- **Azure Key Vault** : Pour gérer les secrets comme les clés d'API et les mots de passe.
- **Virtual Network (VNet) + NSG** : Sécurisation et gestion de l'accès au réseau.
  
### Notes :
- Remplacez les valeurs par défaut dans le script par des valeurs adaptées à votre environnement, notamment pour les mots de passe et les informations de connexion.
- Le coût de certains services comme **Azure Key Vault**, **Azure SQL Database**, ou **Azure Container Instances** dépendra de leur utilisation réelle (quantité de ressources, fréquence des appels, etc.).

### Estimation des coûts avec Terraform :
Comme indiqué dans la configuration, cela peut vous coûter environ 12-15 $/mois en fonction de l'utilisation des ressources (si vous utilisez ces services avec un faible volume de trafic et de stockage).

Si vous avez besoin de plus de détails ou d'ajuster le script à vos exigences spécifiques, n'hésitez pas à demander !
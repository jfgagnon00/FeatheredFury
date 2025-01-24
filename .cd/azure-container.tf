############ Docker

locals {
  container_registry_name = "${var.resource_group_name}${var.environment}acr"
  container_instance_name = "${var.resource_group_name}-${var.environment}-instance"
  
  dns                     = "${var.resource_group_name}-${var.environment}"

  application_name        = "${var.resource_group_name}-${var.environment}-web-app"
  application_image       = "${azurerm_container_registry.acr.login_server}/${var.resource_group_name}-web_app:latest"

  service_name            = "${var.resource_group_name}-${var.environment}-web-service"
  service_image           = "${azurerm_container_registry.acr.login_server}/${var.resource_group_name}-web_service:latest"
}

# Azure Container Registry - pour builder les images dockers
resource "azurerm_container_registry" "acr" {
  name                = local.container_registry_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  admin_enabled       = true
  sku                 = "Basic"
}

# TODO: n'est pas la facon recommender, revoir
resource  "null_resource" "docker_push" {
  provisioner "local-exec" {
    working_dir = "${path.module}/../.ci"
    command = "./terraform_containers_push.sh"
    environment = {
      FFURY_REGISTRY_SERVER = azurerm_container_registry.acr.login_server
      FFURY_REGISTRY_NAME = azurerm_container_registry.acr.name
      AZURE_STORAGE_CONNECTION_STRING = azurerm_storage_account.asa.primary_connection_string
    }
  }

  depends_on = [
    azurerm_container_registry.acr
  ]
}

resource "azurerm_container_group" "acg" {
  name                = local.container_instance_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "Public"
  dns_name_label      = local.dns
  os_type             = "Linux"
  sku                 = "Standard"

  image_registry_credential {
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
    server   = azurerm_container_registry.acr.login_server
  }

  container {
    name   = local.application_name
    image  = local.application_image
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }
  }

  container {
    name   = local.service_name
    image  = local.service_image
    cpu    = "2.0"
    memory = "4.0"
  }

  depends_on = [
    null_resource.docker_push
  ]
}

############ Alias

locals {
  web_application_name   = "${var.resource_group_name}-${var.environment}"
  application_image_name = "${var.resource_group_name}/application:latest"
  registry_url           = "https://${azurerm_container_registry.container_registry.login_server}"
}

############ Web application

# App Service Plan - hosting de l'application
resource "azurerm_service_plan" "sp" {
  name                = "${azuread_application.ffury.display_name}-service_plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "F1" # plan gratuit

  tags = {
      environment = var.environment
  }
}

# Web Application
resource "azurerm_linux_web_app" "ffury" {
  name                = local.web_application_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.sp.id

  site_config {
    always_on = false
    application_stack {
      docker_image_name        = local.application_image_name
      docker_registry_url      = local.registry_url
      docker_registry_username = azuread_application.ffury.client_id
      docker_registry_password = azuread_service_principal_password.ffury.value
    }
  }

  https_only = true
}

# # Bind the custom domain to the App Service
# resource "azurerm_app_service_custom_hostname_binding" "custom_domain" {
#   hostname            = "www.ffury.org"  # Your custom domain
#   resource_group_name = azurerm_resource_group.rg.name
#   web_app_name        = azurerm_web_app.app.name

#   ssl_state           = "SniEnabled"  # Enable SSL for your custom domain
# }


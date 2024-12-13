############ Web application

# App Service Plan - hosting de l'application
resource "azurerm_service_plan" "sp" {
  name                = "${azuread_application.ffury.display_name}-service_plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "F1"

  tags = {
      environment = var.environment
  }
}

# # Define the Azure DNS Zone for your domain
# resource "azurerm_dns_zone" "zone" {
#   name                = "ffury.org"  # Your domain name
#   resource_group_name = azurerm_resource_group.rg.name
# }


# # Define the Web App (Flask app)
# resource "azurerm_web_app" "app" {
#   name                = "myflaskapp"
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   app_service_plan_id = azurerm_app_service_plan.asp.id

#   site_config {
#     python_version = "3.9"
#   }

#   app_settings = {
#     "FLASK_ENV" = "production"
#   }

#   # Enable SSL (Azure will automatically manage SSL for you)
#   ssl_enforcement {
#     enabled = true
#   }
# }

# # Create a CNAME record to point to your Azure App Service
# resource "azurerm_dns_cname_record" "cname" {
#   name                = "www"  # Subdomain (www.ffury.org)
#   zone_name           = azurerm_dns_zone.zone.name
#   resource_group_name = azurerm_resource_group.rg.name
#   ttl                 = 300
#   records             = [azurerm_web_app.app.default_site_hostname]
# }

# # Bind the custom domain to the App Service
# resource "azurerm_app_service_custom_hostname_binding" "custom_domain" {
#   hostname            = "www.ffury.org"  # Your custom domain
#   resource_group_name = azurerm_resource_group.rg.name
#   web_app_name        = azurerm_web_app.app.name

#   ssl_state           = "SniEnabled"  # Enable SSL for your custom domain
# }


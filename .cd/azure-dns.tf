# locals {
#     certificate_name = "${azurerm_resource_group.rg.name}-certificate"
#     zone_name        = "${azurerm_resource_group.rg.name}.org" 
# }

# # DNS Zone - pour acceder a l'application via une adresse 
# resource "azurerm_dns_zone" "zone" {
#   name                = local.zone_name
#   resource_group_name = azurerm_resource_group.rg.name
# }

# # CNAME record to point to your Azure App Service
# resource "azurerm_dns_cname_record" "cname" {
#   name                = "www"
#   zone_name           = azurerm_dns_zone.zone.name
#   resource_group_name = azurerm_resource_group.rg.name
#   ttl                 = 300
#   record              = local.zone_name
# }

# # Associate the custom domain with the app (after DNS validation)
# resource "azurerm_web_app_custom_domain" "domain" {
#   name                = local.zone_name
#   web_app_id          = azurerm_linux_web_app.ffury.id
#   custom_domain_name  = "www.${local.zone_name}"
#   dns_zone_id         = azurerm_dns_zone.zone.id
#   validation_method   = "CNAME"  # Use CNAME to validate the custom domain
# }

# # Configure SSL for the custom domain (Azure Managed SSL)
# resource "azurerm_app_service_certificate" "ssl" {
#   name                = local.certificate_name
#   resource_group_name = azurerm_resource_group.rg.name
#   web_app_id          = azurerm_linux_web_app.ffury.id
#   custom_domain_name  = azurerm_web_app_custom_domain.domain.custom_domain_name
# }

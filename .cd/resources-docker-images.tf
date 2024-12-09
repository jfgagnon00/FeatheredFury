# Construire image docker pour l'application
resource "docker_image" "application" {
  name = "${azurerm_container_registry.acr.login_server}/${var.application_name}:latest"
  build {
    context = "./app"
  }
}

# Pousser image docker de l'application
resource "docker_registry_image" "dri" {
  name          = docker_image.application.name
  image_digest  = docker_image.application.image_digest
}

# # Construire image docker pour l'api
# resource "docker_image" "api" {
#   name = "${azurerm_container_registry.acr.login_server}/${var.api_name}:latest"
#   build {
#     context = "./api"
#   }
# }

# # Construire image docker pour le reverse proxy
# resource "docker_image" "nginx" {
#   name = "${azurerm_container_registry.acr.login_server}/nginx:latest"
#   build {
#     context = "./nginx"
#   }
# }

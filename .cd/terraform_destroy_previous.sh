#!/bin/bash

terraform apply -auto-approve -refresh-only

# obtenir info pour destruction anciennes resources azure
SUBSCRIPTION=$(terraform output -json subscription | tr -d '"')
ENVIRONMENT=$(terraform output -json environment | tr -d '"')

# mettre a jour le plan terraform
terraform import azurerm_resource_group.rg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg"
terraform import azurerm_container_registry.acr "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerRegistry/registries/ffury${ENVIRONMENT}acr"
terraform import azurerm_container_group.acg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerInstance/containerGroups/ffury-${ENVIRONMENT}-instance"

# destruction - pas important si ca existe ou non, ca va etre detruit si ca existe
terraform destroy -auto-approve

# pas vraiment d'erreur
# s'il y avait rien, on a rien detruit sinon, on a fait ce qui etait demande
exit 0

#!/bin/bash

terraform apply -auto-approve -refresh-only

# obtenir info pour destruction anciennes resources azure
SUBSCRIPTION=$(terraform output -json subscription | tr -d '"')
ENVIRONMENT=$(terraform output -json environment | tr -d '"')

# mettre a jour le plan terraform
terraform import azurerm_resource_group.rg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg"
terraform import azurerm_container_registry.acr "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerRegistry/registries/ffury${ENVIRONMENT}acr"
terraform import azurerm_container_group.acg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerInstance/containerGroups/ffury-${ENVIRONMENT}-instance"
terraform import azurerm_storage_account.asa  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.Storage/storageAccounts/ffury${ENVIRONMENT}asa"

# pas vraiment d'erreur a reporter
exit 0

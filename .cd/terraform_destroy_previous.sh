#!/bin/bash

terraform apply -auto-approve -refresh-only

SUBSCRIPTION=$(terraform output -json subscription | tr -d '"')
ENVIRONMENT=$(terraform output -json environment | tr -d '"')

echo ${SUBSCRIPTION}
echo ${ENVIRONMENT}

terraform import azurerm_resource_group.rg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg"
if [ $? -ne 0 ]; then
    exit 0
fi

terraform import azurerm_container_registry.acr "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerRegistry/registries/ffury${ENVIRONMENT}acr"
terraform import azurerm_container_group.acg  "${SUBSCRIPTION}/resourceGroups/ffury-${ENVIRONMENT}-rg/providers/Microsoft.ContainerInstance/containerGroups/ffury-${ENVIRONMENT}-instance"
terraform destroy -auto-approve

exit 0

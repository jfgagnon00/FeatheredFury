#!/bin/bash

terraform import azurerm_resource_group.rg  "${1}/resourceGroups/ffury-${2}-rg"
if [ $? -ne 0 ]; then
    exit 0
fi

terraform import azurerm_container_registry.acr "${1}/resourceGroups/ffury-${2}-rg/providers/Microsoft.ContainerRegistry/registries/ffury${2}acr"
terraform import azurerm_container_group.acg  "${1}/resourceGroups/ffury-${2}-rg/providers/Microsoft.ContainerInstance/containerGroups/ffury-${2}-instance"
terraform destroy -auto-approve

exit 0

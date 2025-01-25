#!/bin/bash

# destruction - pas important si ca existe ou non, ca va etre detruit si ca existe
terraform destroy -auto-approve

# pas vraiment d'erreur
# s'il y avait rien, on a rien detruit sinon, on a fait ce qui etait demande
exit 0

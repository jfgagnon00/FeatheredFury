# TODO: n'est pas la facon recommender, revoir 
resource  "null_resource" "reference-data" {
  provisioner "local-exec" {
    working_dir = "${path.module}/../"
    command = "./.ci/terraform_build_reference_data.sh"
    environment = {
      AZURE_STORAGE_CONNECTION_STRING = azurerm_storage_account.asa.primary_connection_string
    }
  }

  depends_on = [
    azurerm_storage_account.asa
  ]
}
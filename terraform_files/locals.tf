
locals {
  config = jsondecode(file("${path.module}/../config.json"))

  # Define local variables from config
  aws_access_key_id               = local.config.aws_access_key_id
  aws_secret_access_key           = local.config.aws_secret_access_key
  region_name                     = local.config.region_name
  aws_account_id                  = local.config.aws_account_id
  medicines_inventory_bucket_name = local.config.medicines_inventory_bucket_name
  lambda_package_bucket_name      = local.config.lambda_package_bucket_name
  lambda_function_name            = local.config.lambda_function_name
  lambda_package_path             = local.config.lambda_package_path
}
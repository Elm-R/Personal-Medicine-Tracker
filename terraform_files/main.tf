provider "aws" {
  access_key = local.aws_access_key_id
  secret_key = local.aws_secret_access_key
  region     = local.region_name
}


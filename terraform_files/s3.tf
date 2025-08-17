# create the S3 bucket for the medicines inventory and set the appropriate permissions
resource "aws_s3_bucket" "medicines_inventory" {
  bucket = local.medicines_inventory_bucket_name

  tags = {
    Name        = "My medicines inventory Bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket_ownership_controls" "medicines_inventory_ownership_controls" {
  bucket = aws_s3_bucket.medicines_inventory.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "medicines_inventory_block" {
  bucket = aws_s3_bucket.medicines_inventory.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# create the S3 bucket for the lambda package and set the appropriate permissions
resource "aws_s3_bucket" "lambda_package" {
  bucket = local.lambda_package_bucket_name

  tags = {
    Name        = "My lambda package Bucket"
    Environment = "Prod"
  }
}

resource "aws_s3_bucket_ownership_controls" "lambda_package_ownership_controls" {
  bucket = aws_s3_bucket.lambda_package.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_package_block" {
  bucket = aws_s3_bucket.lambda_package.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
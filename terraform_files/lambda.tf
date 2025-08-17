resource "aws_lambda_function" "my_lambda_for_sending_email" {
  function_name = local.lambda_function_name
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_send_email_role.arn  
  handler       = "lambdaFunctionEmailSES.lambda_handler"

  filename      = local.lambda_package_path

  layers = [
    "arn:aws:lambda:${local.region_name}:336392948345:layer:AWSSDKPandas-Python313:3"
  ]

  timeout = 10
}

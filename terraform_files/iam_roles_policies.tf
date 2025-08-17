# Policy for Lambda logs
resource "aws_iam_policy" "lambda_logs_policy" {
  name = "AWSLambdaBasicExecutionRole-36359b69-66a4-4c43-8d32-f8ce8277cb83"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "logs:CreateLogGroup"
        Resource = "arn:aws:logs:${local.region_name}:${local.aws_account_id}:*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:${local.region_name}:${local.aws_account_id}:log-group:/aws/lambda/send-exp-meds-email:*"
        ]
      }
    ]
  })
}

# Policy for EventBridge invoke Lambda
resource "aws_iam_policy" "eventbridge_invoke_lambda_policy" {
  name = "Amazon-EventBridge-Scheduler-Execution-Policy-3b670786-d1e8-4435-9a08-5b02698320c7"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          "arn:aws:lambda:${local.region_name}:${local.aws_account_id}:function:send-exp-meds-email:*",
          "arn:aws:lambda:${local.region_name}:${local.aws_account_id}:function:send-exp-meds-email"
        ]
      }
    ]
  })
}

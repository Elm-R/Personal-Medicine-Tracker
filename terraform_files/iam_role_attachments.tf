# Attach Lambda logs policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_logs_attach" {
  role       = aws_iam_role.lambda_send_email_role.name
  policy_arn = aws_iam_policy.lambda_logs_policy.arn
}

# Attach EventBridge invoke policy to EventBridge role
resource "aws_iam_role_policy_attachment" "eventbridge_invoke_lambda_attach" {
  role       = aws_iam_role.eventbridge_invoke_lambda_send_email_role.name
  policy_arn = aws_iam_policy.eventbridge_invoke_lambda_policy.arn
}

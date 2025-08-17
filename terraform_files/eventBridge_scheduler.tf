resource "aws_scheduler_schedule" "scheduler_for_lambda_ses_emails" {
  name       = "run-lambda-for-emails-every-10-days-noon"
  group_name = "default"

  schedule_expression_timezone = "Europe/Berlin"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 12 */10 * ? 2025)"

  target {
    arn      = aws_lambda_function.my_lambda_for_sending_email.arn
    role_arn = aws_iam_role.eventbridge_invoke_lambda_send_email_role.arn

    retry_policy {
      maximum_retry_attempts = 50
    }
  }
}

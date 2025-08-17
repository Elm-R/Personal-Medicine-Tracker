# Role for Lambda
resource "aws_iam_role" "lambda_send_email_role" {
  name = "send-exp-meds-email-role-q5vu0ixa"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      }
    ]
  })
}

# Role for EventBridge Scheduler
resource "aws_iam_role" "eventbridge_invoke_lambda_send_email_role" {
  name = "Amazon_EventBridge_Scheduler_LAMBDA_fda03ac39e"
  

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = local.aws_account_id
          }
        }
      }
    ]
  })
}

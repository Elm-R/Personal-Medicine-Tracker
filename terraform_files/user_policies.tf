resource "aws_iam_policy" "lambda_policy" {
  name        = "meds_tracker_lambda_policy"
  description = "Access to Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "s3_policy" {
  name        = "meds_tracker_s3_policy"
  description = "Access to S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "ses_policy" {
  name        = "meds_tracker_ses_policy"
  description = "Access to SES"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ses:*"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name        = "meds_tracker_cloudwatch_policy"
  description = "Access to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["cloudwatch:*"]
        Resource = "*"
      }
    ]
  })
}
    
resource "aws_iam_policy" "eventbridge_policy" {
  name        = "meds_tracker_eventbridge_policy"
  description = "Access to EventBridge"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["events:*"]
        Resource = "*"
      }
    ]
  })
}

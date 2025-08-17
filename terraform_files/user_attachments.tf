resource "aws_iam_user_policy_attachment" "attach_lambda" {
  user       = aws_iam_user.dev_user.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_iam_user_policy_attachment" "attach_s3" {
  user       = aws_iam_user.dev_user.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_iam_user_policy_attachment" "attach_ses" {
  user       = aws_iam_user.dev_user.name
  policy_arn = aws_iam_policy.ses_policy.arn
}

resource "aws_iam_user_policy_attachment" "attach_cloudwatch" {
  user       = aws_iam_user.dev_user.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

resource "aws_iam_user_policy_attachment" "attach_eventbridge" {
  user       = aws_iam_user.dev_user.name
  policy_arn = aws_iam_policy.eventbridge_policy.arn
}


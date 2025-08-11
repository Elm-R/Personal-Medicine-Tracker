from medicineChildCloud import medicineChildCloudClass

class LambdaEmailSender(medicineChildCloudClass):
    def __init__(self):
        super().__init__()

    def handle(self, event, context):
        try:
            
            self.send_email_via_ses_to_exp_meds()

            return {
                'statusCode': 200,
                'message': 'Email sent successfully.',
                'details': {
                    'function': 'send_email_via_ses_to_exp_meds',
                    'triggered_by': event.get('source', 'manual or unknown'),
                }
            }

        except Exception as e:
            return {
                'statusCode': 500,
                'message': 'Error occurred during email sending.',
                'error': str(e),
                'details': {
                    'function': 'send_email_via_ses_to_exp_meds',
                    'triggered_by': event.get('source', 'manual or unknown'),
                }
            }

# AWS Lambda requires a function named lambda_handler
def lambda_handler(event, context):
    handler = LambdaEmailSender()
    return handler.handle(event, context)

#Local testing
if __name__ == "__main__":
    test_event = {"source": "manual"}
    test_context = {}
    result = lambda_handler(test_event, test_context)
    print(result)

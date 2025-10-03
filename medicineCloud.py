from medicineEmailsAndMessages import medicineEmailsAndMessagesClass

import os
from datetime import datetime, timedelta

# from dotenv import load_dotenv
import boto3

class medicineCloudClass(medicineEmailsAndMessagesClass):
    def __init__(self):
        super().__init__()
        #load_dotenv()
        self.creds = self.get_aws_creds()
        self.s3_client = self.init_s3_client()
        self.ses_client = self.init_ses_client()
        self.cloudwatch_client = self.init_cloudwatch_client()

    def init_s3_client(self):
        return  boto3.client('s3', **self.creds)   # ** more dynamic
    
    def init_ses_client(self):
        return boto3.client('ses', **self.creds)    
    
    def init_cloudwatch_client(self):
        return boto3.client('cloudwatch', **self.creds)

    def get_aws_access_key_id(self):
        return os.getenv("AWS_ACCESS_KEY_ID")
    
    
    def get_aws_secret_access_key(self):
        return os.getenv("AWS_SECRET_ACCESS_KEY")

    def get_aws_region_name(self):
        return os.getenv("AWS_DEFAULT_REGION")
    
    def get_aws_creds(self):
        return {
            'aws_access_key_id': self.get_aws_access_key_id(),
            'aws_secret_access_key': self.get_aws_secret_access_key(),
            'region_name': self.get_aws_region_name()
        } 
    

    def send_email_via_ses_to_exp_meds(self):
        try:
            recipient = self.get_recepient_email_to_exp_meds()
            
            response = self.ses_client.send_email(
                Source=self.get_sender_email_to_exp_meds(),
                #ToAddresses needs a list of addresses
                Destination={
                    'ToAddresses': recipient,
                },
                Message=self.build_inventory_message_to_exp_meds()
            )
            print("Email sent. Message ID:", response['MessageId'])
            return response

        except Exception as e:
            print("Error sending email:", str(e))
            return None

    def run_all(self):
        # print(self.get_aws_access_key_id())
        # print(self.get_aws_secret_access_key())
        # print(self.get_aws_region_name())
        # print(self.get_aws_creds())
        # print(self.get_recepient_email_to_exp_meds())

        self.connect()
            
        print(self.send_email_via_ses_to_exp_meds())

        self.close_connection()





if __name__ == "__main__":      

    medCloudObj = medicineCloudClass()
    medCloudObj.run_all()
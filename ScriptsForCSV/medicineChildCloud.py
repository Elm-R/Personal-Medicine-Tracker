from medicineParent import medicineParentClass

import json
import pandas as pd
import numpy as np
import csv
import os
# from io import StringIO
from datetime import datetime, timedelta

import boto3


class medicineChildCloudClass(medicineParentClass):
    def __init__(self):
        super().__init__()  # Call Parent's constructor

        self.csv_data = self.read_csv_file()
        self.shift_csv_data_index()
        
        self.converted_exp_dates = self.convert_expiry_dates_to_datetime()

        
    def set_xdays_for_to_exp_meds(self):
        return 10   

    def get_sender_email_to_exp_meds(self):
        return os.getenv("SENDER_EMAIL", self.config.get("sender_email"))

    
    def get_recepient_email_to_exp_meds(self):
        # env variables for docker
        env_emails = os.getenv("RECIPIENT_EMAIL")
        if env_emails:
            # Split comma-separated emails into a list
            return [email.strip() for email in env_emails.split(",")]
        # Fall back to JSON config
        return self.config.get("recipient_email", [])

    def get_aws_s3_bucket_name_for_meds(self):
        return os.getenv("MEDICINES_INVENTORY_BUCKET", self.config.get("medicines_inventory_bucket_name"))  

    def read_csv_file(self):

        inventory_csv_obj = self.s3_client.get_object(
            Bucket= self.get_aws_s3_bucket_name_for_meds(), 
            Key= "medicines_inventory2025-08-09.csv") 
        
        inventory_csv_data_s3 = pd.read_csv(inventory_csv_obj['Body'])

        return inventory_csv_data_s3
    

    def upload_inventory_to_s3(self, file_path, bucket_name, s3_key, set_owner_control=True):
        
        extra_args = {}
        if set_owner_control:
            extra_args['ACL'] = 'bucket-owner-full-control'

        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs=extra_args if extra_args else None
            )
            print(f"Uploaded '{file_path}' to 's3://{bucket_name}/{s3_key}' successfully.")
        except Exception as e:
            print(f"Upload failed: {e}")

        
    def build_inventory_message_to_exp_meds(self):
        xdays = self.set_xdays_for_to_exp_meds()
        return {
            'Subject': {'Data': 'Medicine Expiry Alert'},
            'Body': {
                'Text': {
                    'Data': f'You have medicines that are expiring in {xdays} days:\n{self.show_to_expire_meds_in_x_days_better_format(xdays)}'
                }
            }
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
      

    def prepare_metric_data(self, row_number, expiry_date):
        # Prepare CloudWatch metric data for each row

        expiry_timestamp = int(expiry_date.timestamp())
    
        metric_data = [
            {
                'MetricName': 'MedicineExpiryTimestamp',
                'Dimensions': [{'Name': 'RowNumber', 'Value': str(row_number)}],
                'Timestamp': self.get_todays_date(),
                'Value': expiry_timestamp,
                'Unit': 'Seconds'
            }
        ]
        
        self.cloudwatch_client.put_metric_data(
            Namespace='MedicineInventory',
            MetricData=metric_data
        )


    def send_metrics_to_cloudwatch(self):
        
        #Send metrics for all medicines expiring soon
        meds_expiring_soon = self.show_to_expire_meds_in_x_days(10)
        
        for idx, row in meds_expiring_soon.iterrows():
            row_number = idx 
            expiry_date = row['expiry_date']
            
            self.prepare_metric_data(row_number, expiry_date)
            print(f"Sent metrics for row {row_number}: expiry={expiry_date.date()}")


    def run_all(self):
         

       #self.set_csv_data_index() 
       #print(self.read_csv_file())
       #self.convert_expiry_dates_to_datetime()

       #print("List expired medicines:", self.show_expired_meds())

       #print("List of to expire medicines:", self.show_to_expire_meds_in_x_days(10))

    #   self.upload_inventory_to_s3(self.set_inventory_csv_file_path(),
    #                                 self.get_aws_s3_bucket_name_for_meds(),
    #                                 f"medicines_inventory{self.get_todays_date()}.csv"
    #                                 )

       print(self.build_inventory_message_to_exp_meds())  

       #self.send_email_via_ses_to_exp_meds() 
       
       #self.send_metrics_to_cloudwatch()
        


if __name__ == "__main__":
    medChildObj = medicineChildCloudClass()
    medChildObj.run_all()  
         
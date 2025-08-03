import json
import pandas as pd
import numpy as np
import csv
import os
from datetime import datetime, timedelta

import boto3


# Class Constructor
class medicineParentClass:
    def __init__(self):
        # Set display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        self.json_file = self.set_json_file()
        self.config = None  # to store configuration data
        self.load_config() # initialize config before using it
        self.inventory_csv_file = self.set_inventory_csv_file_path()

        self.csv_data = self.read_csv_file()

        #shifiting indices: dataframe indices match the ones from the csv file
        self.csv_data.index = self.csv_data.index + 2 
        self.converted_exp_dates = self.convert_expiry_dates_to_datetime()
        
        #self.s3 = boto3.client('s3')
        self.creds = self.get_aws_creds()
        self.s3_client = self.init_s3_client()
        self.ses_client = self.init_ses_client()
        

    def set_json_file(self):
        return "config.json"
    
    def get_todays_date(self):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return todays_date
    
    def get_aws_access_key_id(self):
         return self.config.get("aws_access_key_id") 
    
    def get_aws_secret_access_key(self):
         return self.config.get("aws_secret_access_key") 
    
    def get_aws_region_name(self):
         return self.config.get("region_name") 
    
    #convert expiry dates into datetime format for comparison
    def convert_expiry_dates_to_datetime(self):
        self.csv_data["expiry_date"] = pd.to_datetime(self.csv_data["expiry_date"], format='%Y-%m-%d')
        return self.csv_data["expiry_date"] 

    def load_config(self):
        config_path = "config.json"
        if not os.path.exists(config_path):
            print(f"Config file not found: {config_path}")
            self.config = {}
            return
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def set_inventory_csv_file_path(self):
        return self.config.get("csv_path")
    
    def read_csv_file(self):
        inventory_csv_data = pd.read_csv(self.inventory_csv_file)
    
        if inventory_csv_data.empty:
            print("CSV file is empty or not found.")
            return None
        return inventory_csv_data
    

    def add_medicine_to_inventory(self, name, quantity_in_packages, type, expiry_date, dosage, usage, added_on):
        csv_data = self.read_csv_file()

        new_row = {
        "name": name,
        "quantity_in_packages": quantity_in_packages,
        "type": type,
        "expiry_date": expiry_date,
        "dosage": dosage,
        "usage": usage,
        "added_on": added_on
        }

        df = pd.DataFrame([new_row])

        # append data frame to CSV file
        # Use newline='' to avoid blank lines
        with open(self.inventory_csv_file, mode='a', newline='') as f:
            df.to_csv(f, index=False, header=csv_data.empty)

        # print message
        print("Data appended successfully:", name, ",",quantity_in_packages, ",",type, ",",expiry_date,",",dosage,",",usage,",",added_on)

    def delete_medicine_from_inventory(self, name, quantity_in_packages, type, expiry_date, dosage, usage, added_on):
        csv_data = self.read_csv_file()
        if csv_data is None:
            print("No data to delete from.")
            return
        # Filter out the row to delete
        condition = (
        (csv_data["name"] == name) &
        (csv_data["quantity_in_packages"] == quantity_in_packages) &
        (csv_data["type"] == type) &
        (csv_data["expiry_date"] == expiry_date) &
        (csv_data["dosage"] == dosage) &
        (csv_data["usage"] == usage) &
        (csv_data["added_on"] == added_on)
        )

        # Check if the row exists
        if condition.any():
            csv_data = csv_data[~condition]  # keep all rows except the one to delete
            csv_data.to_csv(self.inventory_csv_file, index=False)
            print("Row deleted successfully:", name, ",", quantity_in_packages, ",", type, ",", expiry_date, ",", dosage, ",", usage, ",", added_on)
        else:
            print("No matching row found to delete.")


    def update_medicine_quantity(self, name, type, expiry_date, 
                                 dosage, new_quantity_in_packages):

        #csv_data = self.read_csv_file() 
        if self.csv_data is None:
           print("No data to update.")
           return None
       
         # Find the row to update
        condition = (
              (self.csv_data["name"] == name) &
              (self.csv_data["type"] == type) &
              (self.csv_data["expiry_date"] == expiry_date) &
              (self.csv_data["dosage"] == dosage)
        )

        print("Searching for:", name, type, expiry_date, dosage)
        
        if condition.any():
            # Update the quantity in packages for the matching row
            self.csv_data.loc[condition, "quantity_in_packages"] = new_quantity_in_packages
            self.csv_data.to_csv(self.inventory_csv_file, index=False)
            
            print(f"Medicine {name} quantity updated successfully.")
        else:
            print("No matching row found to update.")


    def show_expired_meds(self):

        if self.csv_data is None:
           print("No data to update.")
           return None     
        
        expired_meds = self.csv_data [self.converted_exp_dates < self.get_todays_date()]
        
        # print number of rows
        print("number of rows is:", len(expired_meds))
        
        if expired_meds.empty:
            print(f"No expired medicines found.")
        else:
            return expired_meds
            
    
    def show_to_expire_meds_in_x_days(self, xdays):

        if self.csv_data is None:
           print("No data to update.")
           return None 
        
        in_xdays = datetime.now() + timedelta(days=xdays)

        #  filtered DataFrame: cannot chain by & 
        # use () inside the [] for a workaround
     
        to_expire_meds = self.csv_data [(self.converted_exp_dates >= self.get_todays_date())
                                         & (self.converted_exp_dates <= in_xdays)]
        
        if to_expire_meds.empty:
            print(f"No medicines will expire in {xdays} days.")
        else:    
            return to_expire_meds
        
    def show_to_expire_meds_in_x_days_better_format(self, xdays):
        to_expire_meds = self.show_to_expire_meds_in_x_days(xdays)  
        lines = []
        for i, row in to_expire_meds.iterrows():
            lines.append(f"{i}. Name: {row['name']}")
            lines.append(f"   Quantity: {row['quantity_in_packages']}")
            lines.append(f"   Type: {row['type']}")
            lines.append(f"   Expiry Date: {row['expiry_date']}")
            lines.append(f"   Dosage: {row['dosage']}")
            lines.append(f"   Usage: {row['usage']}")
            lines.append(f"   Added on: {row['added_on']}\n")
        return "\n".join(lines)
        
        # todo: group by type

    def get_aws_creds(self):
        return {
            'aws_access_key_id': self.get_aws_access_key_id(),
            'aws_secret_access_key': self.get_aws_secret_access_key(),
            'region_name': self.get_aws_region_name()
        }
          
    def init_s3_client(self):
        self.s3 = boto3.client('s3', **self.creds)      # ** more dynamic 

    def upload_inventory_to_s3(self, file_path, bucket_name, s3_key, set_owner_control=True):
        
        extra_args = {}
        if set_owner_control:
            extra_args['ACL'] = 'bucket-owner-full-control'

        try:
            self.s3.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs=extra_args if extra_args else None
            )
            print(f"Uploaded '{file_path}' to 's3://{bucket_name}/{s3_key}' successfully.")
        except Exception as e:
            print(f"Upload failed: {e}")


    def init_ses_client(self):
        return boto3.client('ses', **self.creds)        


    def set_sender_email_to_exp_meds(self):
        return self.config.get("sender_email")
    
    def set_recepient_email_to_exp_meds(self):
        return self.config.get("recipient_email")
    
    def set_xdays_for_to_exp_meds(self):
        xdays = None
        return xdays

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
            recipient = self.set_recepient_email_to_exp_meds()
            
            response = self.ses_client.send_email(
                Source=self.set_sender_email_to_exp_meds(),
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
        

      

          
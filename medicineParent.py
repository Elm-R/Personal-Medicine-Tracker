import json
import pandas as pd
import numpy as np
import csv
import os
from datetime import datetime


# Class Constructor
class medicineParentClass:
    def __init__(self):
        self.json_file = self.set_json_file()
        self.config = None  # to store configuration data
        self.load_config() # initialize config before using it
        self.inventory_csv_file = self.set_inventory_csv_file_path()
        self.csv_data = self.read_csv_file()

    def set_json_file(self):
        return "config.json"


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

        # pd.set_option("display.max_rows", None)        # Show all rows
        # pd.set_option("display.max_columns", None)     # Show all columns

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


    # show expired and to expire in x days meds

    def show_expired_meds(self):

        if self.csv_data is None:
           print("No data to update.")
           return None     
        
        todays_date = datetime.today().strftime('%Y-%m-%d')
        
        #convert expiry dates into datetime format for comparison
        self.csv_data["expiry_date"] = pd.to_datetime(self.csv_data["expiry_date"], format='%Y-%m-%d')

        expired_meds = self.csv_data [self.csv_data ["expiry_date"] < todays_date]
        # print number of rows
        print("number of rows is:", len(expired_meds))
        # Set display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        #print("List of expired medicines:", expired_meds)
        return expired_meds
        

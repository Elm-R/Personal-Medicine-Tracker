from medicineParent import medicineParentClass

class medicineChildClass(medicineParentClass):
    def __init__(self):
        super().__init__()  # Call Parent's constructor
       

    def set_xdays_for_to_exp_meds(self):
        return 10   

    def run_all(self):
        
        #self.load_config()  # already initialized in Parent's constructor

        #print(self.set_inventory_csv_file_path())
        #print(self.config)
        #print("CSV File Data:", self.read_csv_file())

        # add a medicine to inventory
        #self.add_medicine_to_inventory("Paracetamol", 50, "Tablet", "2025-12-31", "500mg", "Pain relief", "2023-10-01")

        # delete a medicine from inventory
        #self.delete_medicine_from_inventory("Paracetamol", 50, "Tablet", "2025-12-31", "500mg", "Pain relief", "2023-10-01")

        # update a medicine's quantity in inventory
        #self.update_medicine_quantity("Digoxin","tablet", "02/10/2026", "0.25mg", 20)

        #print("List of expired medicines:", self.show_expired_meds())

        #print("List of expired medicines:", self.show_to_expire_meds_in_x_days(10))

        # upload csv file to s3
        # self.upload_inventory_to_s3(self.set_inventory_csv_file_path(),
        #                             "medicines-inventory",
        #                             f"medicines_inventory{self.get_todays_date()}.csv"
        #                             )

        #print(self.build_inventory_message_to_exp_meds())  

        self.send_email_via_ses_to_exp_meds()
       
        


if __name__ == "__main__":
    medChildObj = medicineChildClass()
    medChildObj.run_all()  
         
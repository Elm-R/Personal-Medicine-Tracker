from medicineParent import medicineParentClass

class medicineChildLocalClass(medicineParentClass):
    def __init__(self):
        super().__init__()  # Call Parent's constructor

        self.converted_exp_dates = self.convert_expiry_dates_to_datetime()
        


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

        print("List of expired medicines:", self.show_to_expire_meds_in_x_days(10))
          

if __name__ == "__main__":
    medChildObj = medicineChildLocalClass()
    medChildObj.run_all()  
         
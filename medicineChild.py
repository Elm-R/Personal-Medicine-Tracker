from medicineParent import medicineParentClass

class medicineChildClass(medicineParentClass):
    def __init__(self):
        super().__init__()  # Call Parent's constructor
       

    def run_all(self):
        
        #self.load_config()  # already initialized in Parent's constructor

        #print(self.set_inventory_csv_file_path())
        #print(self.config)
        print("CSV File Data:", self.read_csv_file())

        # add a medicine to inventory
        #self.add_medicine_to_inventory("Paracetamol", 50, "Tablet", "2025-12-31", "500mg", "Pain relief", "2023-10-01")

        # delete a medicine from inventory
        #self.delete_medicine_from_inventory("Paracetamol", 50, "Tablet", "2025-12-31", "500mg", "Pain relief", "2023-10-01")

        


if __name__ == "__main__":
    medChildObj = medicineChildClass()
    medChildObj.run_all()  
         

import mysql.connector
from dotenv import load_dotenv
import os


class medicineChildDBClass(): 
    #def __init__(self, host, user, password, database, port):
    def __init__(self):    
        load_dotenv()
        
        self.host = self.get_db_host()
        self.user = self.get_db_user_name()
        self.password = self.get_db_password()
        self.database = self.get_db_name()
        self.port = self.get_db_port()

        self.connection = None
        self.cursor = None
        self.last_results = None  # store results of last executed query
       
    def get_db_host(self):
        value = os.getenv("MYSQL_HOST")
        if not value:
            raise ValueError("MYSQL_HOST is not set")
        return value

    def get_db_user_name(self):
        value = os.getenv("MYSQL_USER")
        if not value:
            raise ValueError("MYSQL_USER is not set")
        return value

    def get_db_password(self):
        value = os.getenv("MYSQL_PASSWORD")
        if not value:
            raise ValueError("MYSQL_PASSWORD is not set")
        return value

    def get_db_name(self):
        value = os.getenv("MYSQL_DATABASE")
        if not value:
            raise ValueError("MYSQL_DATABASE is not set")
        return value

    def get_db_port(self):
        value = os.getenv("DB_PORT")
        if not value:
            raise ValueError("DB_PORT is not set")
        return int(value) 
    
    def get_db_creds(self):
        return {
            "host": self.get_db_host(),
            "user": self.get_db_user_name(),
            "password": self.get_db_password(),
            "database": self.get_db_name(),
            "port": self.get_db_port(),
        }
    
    def get_medicine_columns_select(self):
        return "id, name, quantity_in_packages, medicine_type, " \
        "expiry_date, dosage, usage_instructions, added_on"
    
    def get_medicine_columns_insert_update(self):
        return "name, quantity_in_packages, medicine_type, " \
        "expiry_date, dosage, usage_instructions, added_on"

    # add meds, delete records, update records, show expired meds
    # show meds to expire in 10 days
    def set_query_show_expired_meds(self):
        
        show_expired_meds_query = f"""
            SELECT {self.get_medicine_columns_select()}
            FROM medicines_inventory
            WHERE expiry_date < CURDATE()
        """ 
        return show_expired_meds_query
    
    def set_query_show_meds_expiring_in_10_days(self):
        show_meds_expiring_in_10_days_query = f"""
            SELECT {self.get_medicine_columns_select()}
            FROM medicines_inventory
        WHERE expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 10 DAY)
        """
        return show_meds_expiring_in_10_days_query
    
    def set_query_add_medicine(self, name, quantity_in_packages, medicine_type,
        expiry_date, dosage, usage_instructions, added_on):
    
        query = f"""
            INSERT INTO medicines_inventory
            ({self.get_medicine_columns_insert_update()})
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, quantity_in_packages, medicine_type, expiry_date, dosage, usage_instructions, added_on)
        return query, values
    
    def set_query_update_medicine(self, id, **fields):
        
        if not fields:
            raise ValueError("No fields to update.")

        # Build SET clause dynamically
        set_clause = ", ".join([f"{col}=%s" for col in fields])

        query = f"UPDATE medicines_inventory SET {set_clause} WHERE id=%s"

        # Values for SET clause + id at the end
        values = tuple(fields.values()) + (id,)

        return query, values

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                **self.get_db_creds()
            )
            self.cursor = self.connection.cursor() 
            print("Successfully connected to the database.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None
            self.cursor = None

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            print("No active connection. Please connect first.")
            return None
        
        try:
            self.cursor.execute(query, params)
            
            if query.strip().upper().startswith("SELECT"):
                self.last_results = self.cursor.fetchall()
            else:
                self.connection.commit()
                self.last_results = None
                print(f"Query executed successfully. Rows affected: {self.cursor.rowcount}")

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            self.last_results = None
            return None
    

    def print_results(self):
        if self.last_results:
            for row in self.last_results:
                print(row)
        else:
            print("No results to display.")


    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")


     

    def run_all(self):
        self.connect()

        select_query = "SELECT * FROM medicines_inventory"
        show_exp_meds_query = self.set_query_show_expired_meds()

        meds_expiring_in_10_days_query =self.set_query_show_meds_expiring_in_10_days()

        add_med_query, values = self.set_query_add_medicine(
            "Methotrexate", 10, "Tablet", "2027-06-30", "25mg", 
             "Take once weekly under medical supervision", "2025-09-20")

        add_med_query, values = self.set_query_update_medicine(
            2457, quantity_in_packages=20, dosage="5mg")     

        results = medChildDBObj.execute_query(add_med_query, values)

        self.print_results()

        self.close_connection()

if __name__ == "__main__":      

    medChildDBObj = medicineChildDBClass()
    medChildDBObj.run_all()

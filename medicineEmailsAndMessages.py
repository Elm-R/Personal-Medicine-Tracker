from medicineDB import medicineChildDBClass

from datetime import datetime, timedelta
import os

class medicineEmailsAndMessagesClass(medicineChildDBClass):
    def __init__(self):
        super().__init__()  # Call Parent's constructor
        

    def get_sender_email_to_exp_meds(self):
        return os.getenv("SENDER_EMAIL")

    def get_recepient_email_to_exp_meds(self):
        # env variables for docker
        env_emails = os.getenv("RECIPIENT_EMAIL")
        if env_emails:
            # Split comma-separated emails into a list
            return [email.strip() for email in env_emails.split(",")]
        # Fall back to JSON config
        return self.config.get("recipient_email", [])
    

    def get_todays_date(self):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return todays_date


    def set_xdays_for_to_exp_meds(self):
        return 10


    def format_meds_expiring_in_10_days(self):
        """
        Return a formatted string of medicines expiring in the next 10 days.
        Uses the existing query builder.
        """
        query = self.set_query_show_meds_expiring_in_10_days()
        self.execute_query(query)
        results = self.last_results or []

        columns = self.get_medicine_columns_select().replace(" ", "").split(",")

        lines = []
        for i, row in enumerate(results, start=1):
            row_dict = dict(zip(columns, row))
            lines.append(f"{i}. Name: {row_dict['name']}")
            lines.append(f"   Quantity: {row_dict['quantity_in_packages']}")
            lines.append(f"   Type: {row_dict['medicine_type']}")
            lines.append(f"   Expiry Date: {row_dict['expiry_date']}")
            lines.append(f"   Dosage: {row_dict['dosage']}")
            lines.append(f"   Usage: {row_dict['usage_instructions']}")
            lines.append(f"   Added on: {row_dict['added_on']}\n")

        return "\n".join(lines) if lines else "No medicines expiring in the next 10 days."


    def build_inventory_message_to_exp_meds(self):

        formatted_list = self.format_meds_expiring_in_10_days()

        return {
            'Subject': {'Data': 'Medicine Expiry Alert - Next 10 Days'},
            'Body': {
                'Text': {
                    'Data': f"You have medicines expiring in the next 10 days:\n\n{formatted_list}"
                }
            }
        }



    def run_all(self):
        self.connect()
        
        print(self.build_inventory_message_to_exp_meds())
        
        self.close_connection()


if __name__ == "__main__":      

    medEmailsMessagesObj = medicineEmailsAndMessagesClass()
    medEmailsMessagesObj.run_all()     
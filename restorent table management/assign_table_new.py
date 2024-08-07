import pygsheets
from collections import deque

class RestaurantTableManagement:
    def __init__(self, data, table_status):
        self.waiting_queue = deque(data)
        self.table_status = table_status

    def assign_customers_to_tables(self):
    # Make a copy of the waiting queue
        queue_copy = self.waiting_queue.copy()
    
    # Iterate over the copied queue
        for customer in queue_copy:
            customer_name, num_seats = customer
            table_to_assign = self.find_table_by_capacity(num_seats)
            if table_to_assign is not None:
                print(f"{customer_name} assigned to Table {table_to_assign}.")
                self.update_table_status(table_to_assign)
                self.waiting_queue.remove(customer)  # Remove assigned customer from the original queue
            else:
                print(f"No available table for {customer_name}.")


    def find_table_by_capacity(self, num_seats):
        for table, status, seater in self.table_status:
            if status == '0' and int(seater) == int(num_seats):  # Check for exact match
                return table
        return None

    def free_table(self, table_number):
        print(f"Table {table_number} is now free.")
        self.update_table_status(table_number, status='0')

    def update_table_status(self, table_number, status='1'):
        for idx, (table, current_status, seater) in enumerate(self.table_status):
            if table == str(table_number):
                self.table_status[idx] = (table, status, seater)

    def visualize_table_status(self):
        return [f"Table {table}: {'Occupied' if status == '1' else 'Empty'}" for table, status, _ in self.table_status]
        
def get_data_from_worksheet():
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json") 
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title", "Sheet1")
    data_range = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=True)
    header = data_range[0]  
    data = data_range[1:]
    return data

def get_table_status_from_worksheet():
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json") 
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title", "Sheet2")
    data_range = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=True)
    header = data_range[0]  
    data = data_range[1:]
    return data

def update_table_status(x):
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json")
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title","Sheet2")
    worksheet.update_value(f'B{x}','0')

def main():
    data = get_data_from_worksheet()
    table_status = get_table_status_from_worksheet()

    # Create a queue containing both the name and the number of seats
    queue = [(row[0], row[1]) for row in data]

    # Create restaurant instance
    restaurant = RestaurantTableManagement(queue, table_status)

    # Assign customers to tables
    restaurant.assign_customers_to_tables()

    # Visualize table status after assignment
    print(restaurant.visualize_table_status())

    while True:
        choice = input("Enter the table number to free (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        try:
            table_number = int(choice)
            if 1 <= table_number <= len(table_status):
                restaurant.free_table(table_number)
                restaurant.assign_customers_to_tables()  # Assign next customer to the freed table
            else:
                print("Invalid table number.")
        except ValueError:
            print("Please enter a valid table number or 'q' to quit.")

    print("Exiting...")

if __name__ == "__main__":
    main()

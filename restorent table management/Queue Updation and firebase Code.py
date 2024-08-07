import pygsheets
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import pytz
cred = credentials.Certificate(r"C:\Users\Hariharan\Desktop\College\SEMESTER 6\19CCE384 DESIGN AND INNOVATION LAB\DIL_NEW\restaurant-5fe8f-firebase-adminsdk-ey24i-40977b5da7.json")
firebase_admin.initialize_app(cred)

def table_status():
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json") 
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title", "Sheet2")
    data_range2 = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=True)
    data2=data_range2[1:]
    return data2

def check_free_table():
    free=[]
    tables=table_status()
    for i in tables:
        if i[1]=="0":
            free.append(i)
    return free

def customer_status():
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json") 
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title", "Sheet1")
    data_range1 = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)
    data1=data_range1[1:]
    x=2
    for i in data1:
        i.append(x)
        x=x+1
    return data1

def assign_customers():
    db = firestore.client()
    customers=customer_status()
    free_tables=check_free_table()
    z=0
    for i in customers:
        for j in free_tables:
            if i[1]==j[2]:
                print("filled",j[0])
                print("filledby",i[0])
                update_table(str(int(j[0])+1))
                timestamp = datetime.now(pytz.utc)  
                data = {
                    "name": i[0],
                    "table_no": j[0],
                    "timestamp": timestamp
                }
                doc_ref = db.collection('UserDisplay').document()
                doc_ref.set(data)
                free_tables.pop(free_tables.index(j))
                print(free_tables)
                delete_row(i[2]-z)
                z=z+1
                break

def update_table(x):
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json")
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title","Sheet2")
    worksheet.update_value(f'B{x}','1')

def delete_row(x):
    client = pygsheets.authorize(service_account_file="C:/Users/Hariharan/Desktop/College/SEMESTER 6/19CCE384 DESIGN AND INNOVATION LAB/DIL_NEW/restaurantkv-1ff2f0101143.json")
    spreadsheet = client.open("kvnewrestaurant")
    worksheet = spreadsheet.worksheet("title","Sheet1")
    worksheet.delete_rows(x)

def main():
    while True:
        assign_customers()

if __name__ == "__main__":
    main()
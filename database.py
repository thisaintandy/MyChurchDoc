import mysql.connector
import random
from datetime import datetime,timedelta
from main import ChurchDocApp

cnx = mysql.connector.connect(
    host='localhost',
    user='andy',
    password='Andres212003*',
    database='churchdoc'
)
cursor = cnx.cursor()

# Get the current date and time
CurrentDate = datetime.now()
# Add 7 days to the current date
AvailableDate = CurrentDate + timedelta(days=7)
    
def check_credentials():
    # Get username and password from user input

    try:
        query = "SELECT Username, Password FROM admin WHERE Username = %s"
        cursor.execute(query, (Username,))
        user = cursor.fetchone()

        if user:
            login, stored_password = user
            if stored_password == Password:
                print("Success")
                showadmin()
                
            else:
                print('Incorrect password')
                check_credentials()
        else:
            print('Username not found')
            check_credentials()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()

# HomePage
def HomePage():
    print("\nHow can we help you today?")
    print("1 - Request Materials")
    print("2 - Schedule an Appointment")
    print("3 - Search Transaction History")
    print("4 - Use Other Log In Credentials")

    prompt = input("Select: ")

    try:
        prompt = int(prompt)  # Convert input to integer

        if prompt == 1:
            request()
        elif prompt == 2:
            schedule()
        elif prompt == 3:
            show()
        elif prompt == 4:
            login()
        else:
            print("Invalid selection!")

        HomePage()  # Repeatedly show the menu after each action

    except ValueError:
        print("Invalid input! Please enter a number.")
        
def request():
    def generate_random_numbers(length):
        random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(length))
        return random_numbers

    # Generate RequestCode
    TransactionCode = generate_random_numbers(9)
    print("Transaction Code:", TransactionCode)

    # Take user input for values
    Name = input("Enter Name: ")
    Birthdate = input("Enter Birthdate: ")
    RequestedMaterials = input("Enter Requested Materials: ")

    try:
        # Insert RequestCode into one table
        query_request_code = "INSERT INTO status (RequestStatus, DateRequested, RequestCode, AvailableDate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_request_code, ("Processing", CurrentDate, TransactionCode, AvailableDate))
        cnx.commit()

        # Get the auto-generated primary key (PK) of the inserted row
        request_code_pk = cursor.lastrowid

        # Insert other values along with the reference to RequestCode PK into another table
        query_data = "INSERT INTO request (RequestCode, Name, Birthdate, RequestedMaterials, Status, DateRequested, AvailableDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values_data = (TransactionCode, Name, Birthdate, RequestedMaterials, "Processing", CurrentDate, AvailableDate)
        cursor.execute(query_data, values_data)
        cnx.commit()

        print("Values inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        cursor.close()
        cnx.close()
        
def schedule():
    def generate_random_numbers(length):
        random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(length))
        return random_numbers

    # Generate RequestCode
    ScheduleCode = generate_random_numbers(9)
    print("Transaction Code:", ScheduleCode)

    # Take user input for values
    # Pa-radio button nito ha
    Name = input("Enter Name: ")
    AppointmentDate = input("Enter Date for Schedule: ")
    Appointment = input("Appointment Type: ")

    try:
        # Insert ScheduleCode into one table
        query_request_code = "INSERT INTO status (RequestStatus, DateRequested, RequestCode, AvailableDate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_request_code, ("For Approval", CurrentDate, ScheduleCode, AvailableDate))
        cnx.commit()
        
        # Get the auto-generated primary key (PK) of the inserted row
        request_code_pk = cursor.lastrowid
        
        # Insert other values along with the reference to RequestCode PK into another table
        query_data = "INSERT INTO scheduledappointment (RequestCode, DateRequested, Name, ScheduleDate, Appointment, Status) VALUES (%s, %s, %s, %s, %s, %s)"
        values_data = (ScheduleCode, CurrentDate, Name, AppointmentDate, Appointment, "For Approval")
        cursor.execute(query_data, values_data)
        cnx.commit()

        print("Values inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and connection
        cursor.close()
        cnx.close()
        

#Log in 
def login():
        print("Log in as Admin - 1")
        #Username: admin1
        #Password: admin2
        print("Log in as User - 2")
        login = input("Select: ")
        print("\n")

        try:
            login = int(login)  # Convert input to integer
            if login == 1:
                check_credentials()
            elif login == 2:
                HomePage()
            else:
                print("Invalid selection!")
        except ValueError:
            print("Invalid input! Please enter a number.")

def show():
    showcode = input("Transaction Code:")
    
    query = f"SELECT * FROM status WHERE RequestCode = %s"
    cursor.execute(query, (showcode,))
    
    # Fetch the row from the result set
    row = cursor.fetchone()

    # Check if the row exists
    if row:
        # Print the column names
        columns = [column[0] for column in cursor.description]
        
        # Print the header with aligned columns
        header = " | ".join(columns)
        print(header)
        print("-" * len(header))  # Add a line to separate header and data
        
        # Print the data with aligned columns
        formatted_row = " | ".join(str(cell).ljust(15) for cell in row)
        print(formatted_row)
        
    else:
        print(f"No transaction found!")
    
def showadmin():
    print("Choose one to show the records")
    print("1 - Materials Requests")
    print("2 - Schedule Request")
    
    prompta = input("Select: ")
    print("\n")
    try:
        prompta = int(prompta)  # Convert input to integer
        if prompta == 1:
            query = f"SELECT * FROM request"
            cursor.execute(query)

        # Fetch all rows from the result set
            rows = cursor.fetchall()

        # Check if any rows exist
            if rows:
                # Print the column names
                columns = [column[0] for column in cursor.description]
                header = " | ".join(columns)
                print(header)
                print("-" * len(header))  # Add a line to separate header and data
                
                # Print the data
                for row in rows:
                    formatted_row = " | ".join(str(cell).ljust(15) for cell in row)
                    print(formatted_row)
            else:
                print(f"No rows found in the 'request' table.")

            # Put back button
            showadmin()
                
        elif prompta == 2:
            query = f"SELECT * FROM scheduledappointment"
            cursor.execute(query)

            # Fetch all rows from the result set
            rows = cursor.fetchall()

            # Check if any rows exist
            if rows:
                # Print the column names
                columns = [column[0] for column in cursor.description]
                header = " | ".join(columns)
                print(header)
                print("-" * len(header))  # Add a line to separate header and data
                
                # Print the data
                for row in rows:
                    formatted_row = " | ".join(str(cell).ljust(15) for cell in row)
                    print(formatted_row)
            else:
                print(f"No rows found in the 'request' table.")

            #Put back button
            showadmin()
               
    finally:
        # Close the cursor and connection
        cursor.close()
        cnx.close()  



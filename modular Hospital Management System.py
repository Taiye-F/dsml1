# db_config.py

import mysql.connector as conn

# Connect to MySQL
myBD = conn.connect(
        host="localhost",
        user= "root",
        password="1234567",
        database="hospital_db1"
    )


# Create a global cursor
myCursor = myBD.cursor()


# CRUD FUNCTIONS
myCursor.execute("""
                CREATE TABLE IF NOT EXISTS Doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                specialty VARCHAR(100))
                """)


myCursor.execute("""
            CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            dob INT)
                """)


myCursor.execute("""
           CREATE TABLE IF NOT EXISTS NonStaff (
            staff_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            role VARCHAR(100) )
                 """)


myCursor.execute("""
            CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            doctor_id INT,
            date DATE,
            status VARCHAR(50),
            FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id))
                 """)


def add_doctor(doctor_id, name, specialty, email, phone_no):
    try:
        query = "INSERT INTO doctors (doctor_id, name, specialty, email, phone_no) VALUES (%s, %s, %s, %s, %s)"
        values = (doctor_id, name, specialty, email, phone_no)
        myCursor.execute(query, values)
        myBD.commit()
        print("Doctor added successfully!")
    except conn.Error as err:
        print(f" Database error: {err}")


def add_patients(patient_id, name, dob):
    try:
        query = "INSERT INTO patients (patient_id, name, dob) VALUES (%s, %s, %s)"
        values = (name, dob)
        myCursor.execute(query, values)
        myBD.commit()
        print("Patients added successfully!")
    except conn.Error as err:
        print(f"Database error: {err}")


from datetime import datetime
dob_input = input("Date of Birth (YYYY-MM-DD): ")
try: 
    dob = datetime.strptime(dob_input, "%Y-%m-%d")
    print("Date of Birth recorded as:", dob.date())
except ValueError:
    print("Invalid date format. Please enter in YYYY-MM-DD format.")


def add_nonstaffs(name, role):
    try:
        query = "INSERT INTO nonstaffs (name, role) VALUES (%s, %s, %s, %s, %s)"
        values = (name, role)
        myCursor.execute(query, values)
        myBD.commit()
        print("nonstaffs added successfully!")
    except conn.Error as err:
        print(f"Database error: {err}")


def book_appointment(appointment_id, patient_id, doctor_id, date):
    try:
        query = "INSERT INTO appointment (apponitment_id, patient_id, doctor_id, date, status) VALUES (%s, %s, %s, %s, %s)"
        values = (appointment_id, patient_id, doctor_id, date,"pending")
        myCursor.execute(query, values)
        myBD.commit()
        print("appointment booked successfully!")
    except conn.Error as err:
        print(f"Database error: {err}")



def  approve_appointment(appointment_id):
    try:
        query = "UPDATE Appointments SET status = 'Approved' WHERE appointment_id = %s"
        myCursor.execute(query, (appointment_id,))
        myBD.commit()
        print("Appointment approved!")
    except conn.Error as err:
        print(f"Database error: {err}")


def cancel_appointment(appointment_id):
    try:
        query = "UPDATE Appointments SET status = 'Cancelled' WHERE appointment_id = %s"
        myCursor.execute(query, (appointment_id,))
        myBD.commit()
        print("Appointment cancelled!")
    except conn.Error as err:
        print(f"Database error: {err}")


def  list_appointment(appointment_id):
    try:
        myCursor.execute("SELECT * FROM Appointments")
        results = myCursor.fetchall()
        print("\n All Appointments:")
        for row in results:
            print(row)
    except conn.Error as err:
        print(f"Database error: {err}")


# authentication system (auth/login.py)
def login_user(user_type, username, password):
    try:
        table = "Doctors" if user_type == "doctor" else "Patients"
        query = f"SELECT * FROM {table} WHERE name=%s AND password=%s"
        myCursor.execute(query, (username, password))
        user = myCursor.fetchone()
        if user:
            print(f"{user_type.capitalize()} login successfully !")
            return True
        else:
            print("Invalid username or password.")
            return False
    except conn.Error as err:
        print(f"Database error: {err}")


def menu():
    while True:
        print("\n--- Hospital Management System---")
        print("1. Add Doctor")
        print("2. Add Patient")
        print("3. Add Non-medical Staff")
        print("4. Book Appoinment")
        print("5. Approve Appointment")
        print("6. List Appointments")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            doctor_id = input("Enter id: ")
            name = input("Doctor name: ")
            specialty = input("Speciality: ")
            email = input("email: ")
            phone_no = input("phone_no: ")
            add_doctor(doctor_id, name, specialty, email, phone_no)

        elif choice == '2':
            name = input("Patient name: ")
            dob = int(input("Date of Birth (YYYY-MM-DD): "))
            add_patients(name, dob)
    
        elif choice == '3':
             name = input("Staff name: ")
             role = input("Role: ")
             add_nonstaffs(name, role)

        elif choice == '4':
            pid = int(input("Patient ID: "))
            did = int(input("Doctor ID: "))
            date = input("Date (YYYY-MM-DD): ")
            book_appointment(pid, did, date)

        elif choice =='5':
            aid = int(input("Appointment ID: "))
            approve_appointment(aid)

        elif choice == '6':
            list_appointment()
        
        elif choice =='7':
            print("Exiting program...")
            break

        else:
            print("Invalid choice, try again.")


# Run the menu
menu()


# Close cursor and connection at the end
myCursor.close()
myBD.close()


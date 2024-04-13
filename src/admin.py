import psycopg2

from datetime import datetime


import database_operations
import profile_management
import personal_training_schedule
import group_schedule_management

def register_admin(connection):
    try:
        cursor = connection.cursor()
        print("\nWelcome new Admin!")
        print("Thanks You for joining our fitness Team!.\n")
        print("Please follow the following prompts to get yourself set up!.\n")

        user = None

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                return None
            elif(profile_management.valid_name(first_name)):
                break

        while True:
            last_name = input("Enter last name: ")
            if(last_name == "0"):
                return None
            elif(profile_management.valid_name(last_name)):
                break


        while True:
            password = input("Enter password: ")
            if(password == "0"):
                return None
            elif(profile_management.valid_password(password)):
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                return None
            elif(profile_management.valid_phone_number(phone_number)):
                break

        cursor.execute("INSERT INTO Administrators (first_name, last_name, password, phone_number) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, password, phone_number))
        connection.commit()

        admin = get_admin_by_name(connection, first_name,last_name)
        print(f"Admin {first_name} has been registered successfully!")
        return admin

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register admin:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()






def login_admin(connection):
    try:
        cursor = connection.cursor()

        print("Welcome back Admin! \nLets get you logged in\n")

        while True:
            user = None

            admin_id = input("Enter your Admin ID: ")
            if(admin_id == "0"):
              break
            password = input("Enter password: ")
            if(password == "0"):
              break

            cursor.execute("SELECT * FROM Administrators WHERE admin_id = %s AND password = %s", (admin_id, password))

            #gets the user we're logging into
            user = cursor.fetchone()

            if user:
                return user  
            else:
                print("Invalid email or password. Please try again.\n")

    except (Exception, psycopg2.Error) as error:
        print("Error during login:", error)

    finally:
        if connection:
            cursor.close()







# DATABASE OPERAITON UNDER HERE:


def get_admin_by_name(connection, first_name,last_name):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Administrators WHERE first_name = %s AND last_name = %s", (first_name,last_name))
        user = cursor.fetchone()

        if user:
            return user
        else:
            print("Admin with first name:", first_name, "not found.")
            return None

    except (Exception, psycopg2.Error) as error:
        print("Failed to find Admin by name:", error)
        return None

    finally:
        if cursor:
            cursor.close()


# maintenence under this line ------------------

def print_maintenence_requests(connection):
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT mr.request_id, mr.request_name, mr.request_details, e.equipment_name, mr.request_date FROM Equipment_Maintentence mr JOIN Equipment e ON mr.equipment_id = e.equipment_id")
        all_maintenance_requests = cursor.fetchall()
        print("")
        if all_maintenance_requests:
            print("Maintenance Requests:\n")
            print("{:<10} {:<25} {:<40} {:<25} {:<65}".format("Request ID", "Request Name", "Request Details", "Equipment Name", "Request Date"))
            print("-" * 115)
            for request in all_maintenance_requests:
                request_id, request_name, request_details, equipment_name, request_date = request
                print("{:<10} {:<25} {:<40} {:<25}  ".format(request_id, request_name, request_details, equipment_name) , request_date)
        else:
            print("No maintenance requests found. Everything is running smoothly")
    except Exception as e:
        print("Error fetching maintenance requests:", e)

    finally:
        if cursor:
            cursor.close()
            print("")




def add_maintenence_requests(connection):
    print_maintenence_requests(connection) #print current maintenence requests first

    try:
        cursor = connection.cursor()
        print("Please follow these promts to make a new manitenence request")
        print("All open maintenence tickets adn equipment are  displayed above this")
        
        
        while True:
            req_name = input("Requests name : ")
            if(req_name == "0"):
                return None
            elif(not (req_name.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break

        while True:
            req_desc = input("Description of the Maintenance request : ")
            if(req_desc == "0"):
                return None
            elif(not (req_desc.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break

        while True:
            equipment_id = input("Equipment ID : ")
            if(equipment_id == "0"):
                return None
            elif (not (equipment_id.strip()=="")):
                break

        while True:
            maintenence_date = input("Date (YYYY-MM-DD) : ")
            if(maintenence_date == "0"):
                return None
            elif(not (maintenence_date.strip()=="")):
                break

        cursor.execute("INSERT INTO Equipment_Maintentence (request_name , request_details , equipment_id , request_date ) VALUES (%s, %s, %s, TO_DATE(%s,'YYYY-MM-DD'))",(req_name, req_desc, equipment_id, maintenence_date)) 
        connection.commit()
    except Exception as e:
        print("Error fetching maintenance requests:", e)
    finally:
        if cursor:
            cursor.close()

        





def delete_maintenence_requests(connection):
    print_maintenence_requests(connection) #print current maintenence requests first
    try:
        cursor = connection.cursor()
        print("Please select the ID of the requerst you awnt to delete")
        print("All open maintenence tickets are displayed above this messaage")
        
        
        while True:
            req_id = input("Requests ID : ")
            if(req_id == "0"):
                return None
            elif(not (req_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break
        cursor.execute("DELETE FROM Equipment_maintentence WHERE request_id = %s",(req_id,)) 
        connection.commit()
        print(f"Reqest number {req_id} has officially been deleted")
    except Exception as e:
        print("Error deleting maintenance requests:", e)
    finally:
        if cursor:
            cursor.close()

# ROOM MANAGEMENT FUCNTIONS UNDER HERE
def print_rooms(connection):

    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * from Rooms")
        all_maintenance_requests = cursor.fetchall()
        print("")
        if all_maintenance_requests:
            print("All Rooms:")
            print("{:<20} {:<20} {:<20} ".format("Room ID", "Room Name","Max Capacity"))
            print("-" * 65)
            for request in all_maintenance_requests:
                room_id, room_name, capacity = request
                print("{:<20} {:<20} {:<20} ".format(room_id, room_name, capacity))
        else:
            print("No Rooms found.")
    except Exception as e:
        print("Error fetching Rooms:", e)

    finally:
        if cursor:
            cursor.close()
            print("")



def add_room(connection):
    print_rooms(connection) #print current maintenence requests first

    try:
        cursor = connection.cursor()
        print("Please follow these promts to make a new room")
        
        
        while True:
            room_name = input("Room name : ")
            if(room_name == "0"):
                return None
            elif(not (room_name.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break

        while True:
            capacity = input("Max Capacity: ")
            if(capacity == "0"):
                return None
            elif(not (capacity.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break


        cursor.execute("INSERT INTO Rooms (room_name , capacity  ) VALUES (%s, %s)",(room_name, capacity)) 
        connection.commit()
        print("Room: {room_name} has been added succesfully")
    except Exception as e:
        print("Error Adding new room:", e)
    finally:
        if cursor:
            cursor.close()



def delete_room(connection):
    print_rooms(connection) #print current maintenence requests first

    try:
        cursor = connection.cursor()
        print("Please Select a Room by ID to delete it.")
        print("all Rooms are shown above")

        
        
        while True:
            room_id = input("Room ID : ")
            if(room_id == "0"):
                return None
            elif(not (room_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break


        cursor.execute("DELETE FROM Rooms WHERE room_id = %s",(room_id,))
        connection.commit()
    except Exception as e:
        print("Error Adding new room:", e)
    finally:
        if cursor:
            cursor.close()



#CLASS SCHEDULE UPDATING FUNCTIONS UNDER HERE
def print_group_schedule_data(connection):
    #first print personal session data
    print_personal_training_classes(connection)
    print('')
    try:
        cursor = connection.cursor()

        # Print group_training_classes table
        cursor.execute("SELECT * FROM group_training_classes")
        group_training_classes = cursor.fetchall()
        if group_training_classes:
            print("Group Training Classes:")
            print("{:<10} {:<15} {:<25} {:<15} {:<25}".format("Class ID", "Trainer ID", "Name", "Booking ID", "Details"))
            print("-" * 95)
            for class_data in group_training_classes:
                print("{:<10} {:<15} {:<25} {:<15} {:<25}".format(*class_data))
        else:
            print("No data found in group_training_classes table")

    except Exception as e:
        print("Error fetching table data:", e)

    finally:
        if cursor:
            cursor.close()

def print_personal_training_classes(connection):
    try:
        cursor = connection.cursor()

        # Fetch personal_training_classes table data
        cursor.execute("""
            SELECT ptc.class_id, t.first_name AS trainer_first_name, m.first_name AS member_first_name, 
                   ptc.booking_id, ptc.details
            FROM personal_training_classes ptc
            LEFT JOIN Trainers t ON ptc.trainer_id = t.trainer_id
            LEFT JOIN Members m ON ptc.member_id = m.member_id
        """)
        classes_data = cursor.fetchall()

        # Print the data
        if classes_data:
            print("Personal Training Classes:")
            print("{:<10} {:<15} {:<15} {:<15} {:<25}".format("Class ID", "Trainer", "Member", "Booking ID", "Details"))
            print("-" * 85)
            for class_data in classes_data:
                class_id, trainer_first_name, member_first_name, booking_id, details = class_data


                print("{:<10} {:<15} {:<15} {:<15} {:<25}".format(class_id, trainer_first_name, member_first_name, booking_id, details))
        else:
            print("No data found in personal_training_classes table")

    except Exception as e:
        print("Error fetching table data:", e)

    finally:
        if cursor:
            cursor.close()


#this function was to long so i brute forced to validation
def create_group_training_class(connection):
    try:
        cursor = connection.cursor()

        # Gather information for the new room booking
        print("Enter the details for the new room booking:")
        room_id = input("Room ID: ")
        day_of_week = input("Day of the week (e.g., Monday, Tuesday, etc.): ")
        start_time = input("Start time (HH:MM:SS): ")
        end_time = input("End time (HH:MM:SS): ")
        recurrence = input("Recurrence: ")

        # Insert the new room booking into the database
        cursor.execute("""
            INSERT INTO Room_Bookings (room_id, day_of_week, start_time, end_time, recurrence)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING booking_id
        """, (room_id, day_of_week, start_time, end_time, recurrence))
        booking_id = cursor.fetchone()[0]

        # Gather information for the new group training class
        print("\nEnter the details for the new group training class:")
        name = input("Class name: ")
        trainer_id = input("Trainer ID: ")
        details = input("Class details: ")

        # Insert the new group training class into the database
        cursor.execute("""
            INSERT INTO Group_training_classes (trainer_id, name, booking_id, details)
            VALUES (%s, %s, %s, %s)
        """, (trainer_id, name, booking_id, details))
        connection.commit()

        print("\nGroup training class created successfully!")

    except Exception as e:
        print("Error creating group training class:", e)

    finally:
        if cursor:
            cursor.close()



def delete_room(connection):
    print_group_schedule_data(connection) #print current maintenence requests first

    try:
        cursor = connection.cursor()
        print("Please Select a Group class by ID to delete it.")
        print("all group classes are shown above")

        
        
        while True:
            class_id = input("Class ID : ")
            if(class_id == "0"):
                return None
            elif(not (class_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break


        cursor.execute("DELETE FROM Group_training_classes WHERE class_id = %s",(class_id,))
        connection.commit()
    except Exception as e:
        print("Error Adding new room:", e)
    finally:
        if cursor:
            cursor.close()



# ALLL BILLING UNDER HERE ---------------------
def print_billing(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT b.billing_id, b.status, b.amount, r.day_of_week, r.start_time, r.end_time, 
            CONCAT(m.first_name, ' ', m.last_name) AS member_name
            FROM Billing b
            JOIN room_bookings r ON b.billing_room_id = r.booking_id
            JOIN Members m ON b.member_id = m.member_id
        """)
        all_billing_records = cursor.fetchall()

        if all_billing_records:
            print("\n \t\t\tBilling Records:")
            print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format("Billing ID", "Status", "Amount", "Day of Week", "Start Time", "End Time", "Member Name"))
            print("-" * 110)
            for record in all_billing_records:
                billing_id, status, amount, day_of_week, start_time, end_time, member_name = record
                #convest times to string before printing
                start_time = start_time.strftime("%H:%M")
                end_time = end_time.strftime("%H:%M")
                #convert status into a word (Completed or Due)
                if status == 0:
                    word_status="Due"
                else:
                    word_status="Competed"

                print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format(billing_id, word_status, amount, day_of_week, start_time, end_time, member_name))
        
        else:
            print("No billing records found.")

    except Exception as e:
        print("Error fetching billing records:", e)

    finally:
        if cursor:
            cursor.close()

def print_due_bills(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT b.billing_id, b.status, b.amount, r.day_of_week, r.start_time, r.end_time, 
            CONCAT(m.first_name, ' ', m.last_name) AS member_name
            FROM Billing b
            JOIN room_bookings r ON b.billing_room_id = r.booking_id
            JOIN Members m ON b.member_id = m.member_id
            WHERE b.status = False
        """)
        all_billing_records = cursor.fetchall()

        if all_billing_records:
            print("\n \t\t\tAll DUE BILLS:")
            print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format("Billing ID", "Status", "Amount", "Day of Week", "Start Time", "End Time", "Member Name"))
            print("-" * 110)
            for record in all_billing_records:
                billing_id, status, amount, day_of_week, start_time, end_time, member_name = record
                #convest times to string before printing
                start_time = start_time.strftime("%H:%M")
                end_time = end_time.strftime("%H:%M")
                #convert status into a word (Completed or Due)
                if status == 0:
                    word_status="Due"
                else:
                    word_status="Competed"

                print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format(billing_id, word_status, amount, day_of_week, start_time, end_time, member_name))
        else:
            print("No billing records found.")

    except Exception as e:
        print("Error fetching billing records:", e)

    finally:
        if cursor:
            cursor.close()

def print_completed_bills(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT b.billing_id, b.status, b.amount, r.day_of_week, r.start_time, r.end_time, 
            CONCAT(m.first_name, ' ', m.last_name) AS member_name
            FROM Billing b
            JOIN room_bookings r ON b.billing_room_id = r.booking_id
            JOIN Members m ON b.member_id = m.member_id
            WHERE b.status = True
        """)
        all_billing_records = cursor.fetchall()

        if all_billing_records:
            print("\n \t\t\tAll DUE BILLS:")
            print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format("Billing ID", "Status", "Amount", "Day of Week", "Start Time", "End Time", "Member Name"))
            print("-" * 110)
            for record in all_billing_records:
                billing_id, status, amount, day_of_week, start_time, end_time, member_name = record
                #convest times to string before printing
                start_time = start_time.strftime("%H:%M")
                end_time = end_time.strftime("%H:%M")
                #convert status into a word (Completed or Due)
                if status == 0:
                    word_status="Due"
                else:
                    word_status="Competed"

                print("{:<15} {:<10} {:<10} {:<15} {:<20} {:<20} {:<25}".format(billing_id, word_status, amount, day_of_week, start_time, end_time, member_name))
        else:
            print("No billing records found.")

    except Exception as e:
        print("Error fetching billing records:", e)

    finally:
        if cursor:
            cursor.close()



def delete_bill(connection):
    try:
        cursor = connection.cursor()
        
        print_billing(connection)#prints all bills

        print("Please select A bill by ID from the list above to delete.")
        
        while True:
            bill_id = input("Billing ID : ")
            if(bill_id == "0"):
                return None
            elif(not (bill_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break
        
        cursor.execute("DELETE FROM Billing WHERE billing_id = %s",(bill_id,))
        print(f"Bill with id : {bill_id} has successfuly been deleted")

    except Exception as e:
        print("Error fetching billing records:", e)

    finally:
        if cursor:
            cursor.close()


def add_bill(connection):
    try:
        cursor = connection.cursor()
        
        print_billing(connection)#prints all bills

        print("Please follow the promts to add a new bill.")
            #STATUS
        while True:
            staus = input("Please enter 'True' for completed and 'False' for Due. : ")
            if(staus == "0"):
                return None
            elif(staus not in ["True","False"]):
               print("Input MUST BE 'True' or 'False'")
               continue #restart loop if not true of false
            elif(not (staus.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break
        
                #amount
        while True:
            amount = input("Dollar Amount (ex 15.99) : ")
            if(amount == "0"):
                return None
            elif(not (amount.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break
                #ROOM
        while True:
            print("Avaliable Rooms:")
            print_rooms(connection)
            room_id = input("Room ID : ")
            if(room_id == "0"):
                return None
            elif (not personal_training_schedule.valid_room(connection,room_id)):
                continue
            elif(not (room_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break

        while True:
            print("Personal Trainin Sessions:")
            personal_training_schedule.print_all_member_personal_sessions(connection)
            room_id = input("Training_session ID : ")
            if(room_id == "0"):
                return None
            elif(not (room_id.strip()=="")): # IF NOT EMPTY STRING, THEN ...
                break
        
        

    
        #cursor.execute("INSERT INTO Billing VALUES (%s,%s,%s,%s,%s,)",(,,,,))
        print(f"A new bill has successfully been added")

    except Exception as e:
        print("Error fetching billing records:", e)

    finally:
        if cursor:
            cursor.close()


def alter_billing(connection):
    try:
        cursor = connection.cursor()

        print_billing(connection)#prints all bills

        print("Please follow the promts to edit an existing bill.")
        print("Press Enter on any item to skip")

        billing_id = input("Enter the Billing ID : ")
        status = input("Enter new status (True/False): ").capitalize()
        amount = input("Enter new amount: ")
        billing_room_id = input("Enter new billing room ID: ")
        billing_session_id = input("Enter new billing session ID: ")
        member_id = input("Enter new member ID: ")

        # make the update statment progressievly  based on the provided parameters
        update_query = "UPDATE Billing SET "
        update_values = []

        if status:
            update_values.append(f"status = {status}")
        if amount:
            update_values.append(f"amount = {amount}")
        if billing_room_id:
            update_values.append(f"billing_room_id = {billing_room_id}")
        if billing_session_id:
            update_values.append(f"billing_session_id = {billing_session_id}")
        if member_id:
            update_values.append(f"member_id = {member_id}")

        if not update_values:
            print("No attributes provided to update.")
            return

        update_query += ", ".join(update_values)
        update_query += f" WHERE billing_id = {billing_id}"

        cursor.execute(update_query)
        connection.commit()

        print("Billing record updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to update billing record:", error)

    finally:
        if cursor:
            cursor.close()



# ADMIN MANAGEMENT PAGE:

def create_new_admin(connection):
    try:
        cursor = connection.cursor()
        print("Please follow the following prompts to add a ned admin!.\n")

        user = None

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                return None
            elif(profile_management.valid_name(first_name)):
                break

        while True:
            last_name = input("Enter last name: ")
            if(last_name == "0"):
                return None
            elif(profile_management.valid_name(last_name)):
                break


        while True:
            password = input("Enter password: ")
            if(password == "0"):
                return None
            elif(profile_management.valid_password(password)):
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                return None
            elif(profile_management.valid_phone_number(phone_number)):
                break

        cursor.execute("INSERT INTO Administrators (first_name, last_name, password, phone_number) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, password, phone_number))
        connection.commit()

        admin = get_admin_by_name(connection, first_name,last_name)
        print(f"Admin {first_name} has been added successfully!")
        return admin

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to add admin:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()


def create_new_trainer(connection):
    try:
        cursor = connection.cursor()
        print("Please follow the following prompts to add a new trainer!.\n")

        user = None

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                return None
            elif(profile_management.valid_name(first_name)):
                break

        while True:
            last_name = input("Enter last name: ")
            if(last_name == "0"):
                return None
            elif(profile_management.valid_name(last_name)):
                break


        while True:
            password = input("Enter password: ")
            if(password == "0"):
                return None
            elif(profile_management.valid_password(password)):
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                return None
            elif(profile_management.valid_phone_number(phone_number)):
                break

        cursor.execute("INSERT INTO Trainers (first_name, last_name, password, phone_number) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, password, phone_number))
        connection.commit()

        cursor.execute("SELECT * FROM Trainers WHERE phone_number=%s AND password=%s",(phone_number,password))
        user = cursor.fetchone()
        print (user)
        print(f"Trainer {first_name} has been added successfully!")
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to add trainer:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()



def create_new_trainer(connection):
    try:
        cursor = connection.cursor()
        print("Please follow the following prompts to add a new trainer!.\n")

        user = None

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                return None
            elif(profile_management.valid_name(first_name)):
                break

        while True:
            last_name = input("Enter last name: ")
            if(last_name == "0"):
                return None
            elif(profile_management.valid_name(last_name)):
                break


        while True:
            password = input("Enter password: ")
            if(password == "0"):
                return None
            elif(profile_management.valid_password(password)):
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                return None
            elif(profile_management.valid_phone_number(phone_number)):
                break

        cursor.execute("INSERT INTO Trainers (first_name, last_name, password, phone_number) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, password, phone_number))
        connection.commit()

        cursor.execute("SELECT * FROM Trainers WHERE phone_number=%s AND password=%s",(phone_number,password))
        user = cursor.fetchone()
        print (user)
        print(f"Trainer {first_name} has been added successfully!")
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to add trainer:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()


# DELETE FUNCTIONS:

def delete_trainer(connection):

    try:
        cursor = connection.cursor()

        personal_training_schedule.print_all_trainers(connection)
        print("Please enter the Trainers ID to DELETE them!\n")

        user = None

        while True:
            trainer_id = input("Trainer ID : ")
            if(trainer_id == "0"):
                return None
            elif(not trainer_id.strip()==""):
                break


        cursor.execute("DELETE FROM Trainers WHERE trainer_id = %s",(trainer_id,))
        connection.commit()

        print (user)
        print(f"Trainer with ID : {trainer_id} has been deleted successfully!")
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to delete trainer:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()


def print_admin_table_data(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT admin_id, first_name, last_name, phone_number, password
            FROM Administrators
        """)
        all_admin_records = cursor.fetchall()

        if all_admin_records:
            print("\n \t\t\tAdministrators Table Data:")
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("Admin ID", "First Name", "Last Name", "Phone Number", "Password"))
            print("-" * 80)
            for record in all_admin_records:
                admin_id, first_name, last_name, phone_number, password = record
                print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(admin_id, first_name, last_name, phone_number, password))
        else:
            print("No administrator records found.")

    except Exception as e:
        print("Error fetching administrator records:", e)

    finally:
        if cursor:
            cursor.close()

def delete_admin(connection):

    try:
        cursor = connection.cursor()

        personal_training_schedule.print_all_trainers(connection)
        print_admin_table_data(connection)
        print("Please enter the Admin ID to DELETE them!\n")

        user = None

        while True:
            admin_id = input("Admin ID : ")
            if(admin_id == "0"):
                return None
            elif(not admin_id.strip()==""):
                break


        cursor.execute("DELETE FROM Administrators WHERE admin_id = %s",(admin_id,))
        connection.commit()

        print (user)
        print(f"Admin with ID : {admin_id} has been deleted successfully!")
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to delete trainer:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()



#         # -- ALL ADMIN MENUS UNDER HERE ------------
# #                       PLEASE READ
# #To integrate this into the main menu just copy paste everything under here into the menu.pu file and 
# # do somthing like this:
# # if choide == "4" .    #Administrator
# # elif choice == "4":  #if admin
# #             clear_terminal()
# #             user = admin_login_menu(connection)
# # #connected to the Admin_login_menu fucntion that returns a user
# # Login menu lead to main Admin menu and has back/cancel operation navigation on every page
# #
# def admin_login_menu(connection):
#      while True:

#         print("\nHello Admin")
#         print("1. Register as Admin")
#         print("2. Login as Admin")
#         print("0. Go back\n")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#                 user = admin.register_admin(connection)
#                 if(user):
#                     print("New Admin registered Successfully ") #redicrect to next menu funciton
#         elif choice == "2":
#                 user = admin.login_admin(connection)
#                 if(user):
#                     print("Admin Successfully Logged in") #redicrect to next menu funciton
#                     admin_menu (user)
#         elif choice == "0":
#             return None

 
 

# # ------------ MAIN ADMIN MENU ------------------
# #connects to a bunch of other menus
# def admin_menu(connection, user):
#      while True:
#         print("\n\tHello Admin", user[1])
#         print("1. Equipment maintenence")
#         print("2. Room managment")
#         print("3. Class scheduling")
#         print("4. Billing and processing")
#         print("5. Trainer management")
#         print("6. Admin Management")
#         print("")

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             clear_terminal()
#             user = admin_maintenence_menu(connection,user)
#         elif choice == "2":
#             clear_terminal()
#             user = admin_room_menu(connection,user)
#         elif choice == "3":
#             clear_terminal()
#             user = admin_class_management_menu(connection,user)
#         elif choice == "4":
#             clear_terminal()
#             user = admin_billing_management_menu(connection,user)
#         elif choice == "5":
#             clear_terminal()
#             user = admin_trainer_management_menu(connection,user)
#         elif choice == "6":
#             clear_terminal()
#             user = admin_admin_management_menu(connection,user)
#         elif choice == "0":# go back to privious menu
#             return user
#         else:
#             print("Invalid choice. Please try again.")


# #Admin sub menu
# def admin_maintenence_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("Hello Admin", user[1])
#         print("1. View Maintenence requests")
#         print("2. Add Maintenence requests")
#         print("3. Remove Maintenence requests")
#         print("0. Go back")

#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.print_maintenence_requests(connection)
#         elif choice == "2":
#             admin.add_maintenence_requests(connection)
#         elif choice == "3":
#             admin.delete_maintenence_requests(connection)
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")

# #Admin sub menu
# def admin_room_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("Hello Admin", user[1])
#         print("1. View all rooms")
#         print("2. Add room")
#         print("3. Delete room")
#         print("0. Go back")

#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.print_rooms(connection)
#         elif choice == "2":
#             admin.add_room(connection)
#         elif choice == "3":
#             admin.delete_room(connection)
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")



# #Admin sub menu
# def admin_class_management_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("\n \t Class Management Page!")
#         print("1. View all scheduled classes (Group & Personal)")
#         print("2. Add new Group class")
#         print("3. Delete Group class")
#         print("4. Add personal session")
#         print("5. Delete personal session")
#         print("0. Go back")

#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.print_group_schedule_data(connection)
#         elif choice == "2":
#             admin.create_group_training_class(connection)
#         elif choice == "3":
#             admin.delete_room(connection)
#         elif choice == "4":
#             personal_training_schedule.schedule_personal_training(connection,user)
#         elif choice == "5":
#             personal_training_schedule.cancel_personal_session(connection,user)
        
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")




# #Admin sub menu
# def admin_billing_management_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("\n \t Class Management Page!")
#         print("1. View all Bills")
#         print("2. View all Due Bills")
#         print("3. View all completed Transactions")
#         print("4. Remove Bill")
#         print("5. Edit Bill")
#         print("0. Go back")


#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.print_billing(connection)
#         elif choice == "2":
#             admin.print_due_bills(connection)
#         elif choice == "3":
#             admin.print_completed_bills(connection)
#         elif choice == "4":
#             admin.delete_bill(connection)
#         elif choice == "5":
#             admin.alter_billing(connection)
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")

# #Admin submenu
# def admin_trainer_management_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("\n \t Class Management Page!")
#         print("1. Add trainer")
#         print("2. Delete Trainer")
#         print("3. View all Trainers")
#         print("0. Go back")

#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.create_new_trainer(connection)
#         elif choice == "2":
#             admin.delete_trainer(connection)
#         elif choice == "3":
#             personal_training_schedule.print_all_trainers(connection)
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")

# #Admin Sub Menu
# def admin_admin_management_menu(connection, user):
     
#     #this admin sub menu runs a loop for maintenence promtps until exited 
#      while True:
#         print("\n \t Class Management Page!")
#         print("1. Add admin")
#         print("2. Delete Admin")
#         print("3. View all Admin")
#         print("0. Go back")


#         choice = input("Enter your choice: ")
#         if choice == "1":
#             admin.create_new_admin(connection)
#         elif choice == "2":
#             admin.delete_admin(connection)
#         elif choice == "3":
#             admin.print_admin_table_data(connection)
       
#         elif choice == "0":
#             return user
#         else:
#             print("Invalid choice. Please try again.")


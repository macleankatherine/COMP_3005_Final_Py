import database
import psycopg2
from datetime import datetime
import profile_management

def trainer_login(connection):
    try:
        cursor = connection.cursor()

        print("Welcome Trainer")
        print("Lets get you logged in!")

        while True:
            trainer = None

            trainerId = input("\nTrainer ID: ")
            if not trainerId.isdigit():
                print("Trainer ID must be a digit.")
                continue
            trainerPassword = input("Password: ")

            cursor.execute("SELECT * FROM Trainers WHERE trainer_id = %s AND password = %s", (trainerId , trainerPassword))
            trainer = cursor.fetchone()

            if trainer:
                return trainer  
            else:
                print("Invalid credentials. Please try again.")

    except (Exception, psycopg2.Error) as error:
        print("Error during login:", error)

    finally:
        if connection:
            cursor.close()

def show_class_schedules(connection, trainer_id, trainer_name):
    try: 
        cursor = connection.cursor()
        cursor.execute('''
            SELECT pt.class_id , pt.trainer_id , pt.member_id , pt.booking_id , pt.details , m.first_name , m.last_name , m.email , m.phone_number
            FROM Personal_training_classes pt
            JOIN Members m ON pt.member_id = m.member_id
            WHERE pt.trainer_id = %s
        ''' , (trainer_id,))

        personalClasses = cursor.fetchall()

        if personalClasses:
            print("\nPersonal Training Sessions For", trainer_name)
            print("-" * 100)

            for classes in personalClasses:
                class_id , trainer_id , member_id , booking_id , details , first_name , last_name , email , phone_number = classes
                
                print(f"Personal Training Session With: {first_name} {last_name}")
                print(f"Client email: {email}")
                print(f"Client Phone Number: {phone_number}")
                print(f"Training Details: {details}")
                print("-" * 100)
            print("\n")
        else:
            print("No personal training classes found")

        cursor.execute('''
            SELECT gc.class_id , gc.trainer_id , gc.name , gc.booking_id , gc.details , rb.start_time , rb.end_time
            FROM Group_training_classes gc
            JOIN Room_Bookings rb ON gc.booking_id = rb.booking_id
            WHERE gc.trainer_id = %s
        ''' , (trainer_id,))

        groupClasses = cursor.fetchall()

        if groupClasses:
            print("Group Training Sessions For", trainer_name)
            print("-" * 100)

            for classes in groupClasses:
                class_id, trainer_id, name, booking_id, details, start_datetime, end_datetime = classes
                
                print(f"Group Training Session: {name}")
                print(f"Class ID: {class_id}")
                print(f"Booking ID: {booking_id}")
                print(f"Session Details: {details}")
                print(f"Start Time: {start_datetime}")
                print(f"End Time: {end_datetime}")
                print("-" * 100)
            print("\n")
        else:
            print("No group training classes found")

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve training classes:", error)

    finally:
        if cursor:
            cursor.close()

def view_member_profiles(connection , searchUser):
    try: 
        cursor = connection.cursor()

        cursor.execute('''
            SELECT first_name , last_name , email , phone_number
            FROM Members
            WHERE first_name ILIKE %s OR last_name ILIKE %s
        ''', ('%' + searchUser + '%', '%' + searchUser + '%'))

        memberProfiles = cursor.fetchall()

        if memberProfiles:
            print("\nMember Profiles Matching Search Term:", searchUser)
            print("{:<15}{:<15}{:<25}{:<15}".format("First Name", "Last Name", "Email", "Phone Number"))
            print("-" * 100)

            for profile in memberProfiles:
                first_name, last_name, email, phone_number = profile
                print("{:<15}{:<15}{:<25}{:<15}".format(first_name , last_name , email , phone_number))

            print("\n")

        else:
            print("No member profiles found for this trainer")

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve member profiles:", error)

    finally:
        if cursor:
            cursor.close()

def update_availability(connection , trainer_id):
    try:
        cursor = connection.cursor()

        #Show the current availability for da trainer
        cursor.execute('''
            SELECT availability_id , day_of_week , start_time , end_time
            FROM Trainer_Availability
            WHERE trainer_id = %s
        ''' , (trainer_id,))

        availabilities = cursor.fetchall()

        if not availabilities:
            print("No availability found for this trainer.")
            return

        #Print current availability
        print("\nCurrent Availability:")
        print("If you want to switch to being unavailable, please enter '00' values for both start and end time on a specific day\n")
        print("{:<20} {:<15} {:<15} {:<15}".format("Availability ID" , "Day of Week" , "Start Time" , "End Time"))
        print("-" * 100)

        for availability in availabilities:
            availability_id , day_of_week , start_time , end_time = availability
            print("{:<20} {:<15} {:<15} {:<15}".format(availability_id, day_of_week, start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S')))

        #Ask for availability to update
        availability_id_to_update = input("\nEnter the availability ID you want to update: ")

        if not availability_id_to_update.isdigit():
            print("Invalid availability ID.")
            return

        availability_id_to_update = int(availability_id_to_update)
        if availability_id_to_update not in [availability[0] for availability in availabilities]:
            print("Invalid availability ID.")
            return

        #axe trainer for new availability details
        new_day_of_week = input("Enter new day of the week: ")
        new_start_time_str = input("Enter new start time (format: HH:MM:SS): ")
        new_end_time_str = input("Enter new end time (format: HH:MM:SS): ")

        #Convert string times to datetime.time objects
        new_start_time = datetime.strptime(new_start_time_str, '%H:%M:%S').time()
        new_end_time = datetime.strptime(new_end_time_str, '%H:%M:%S').time()

        #Update availability 
        cursor.execute('''
            UPDATE Trainer_Availability
            SET day_of_week = %s, start_time = %s, end_time = %s
            WHERE availability_id = %s
        ''' , (new_day_of_week , new_start_time , new_end_time , availability_id_to_update))

        connection.commit()
        print("Availability updated successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Failed to update availability:", error)

    finally:
        if cursor:
            cursor.close()

def create_custom_routine(connection):
    try:
        cursor = connection.cursor()
        print("Create a custome Exercise for a member\n")

        cursor.execute("SELECT * FROM Members")

        members = cursor.fetchall()
        
        if members:
            print("\n{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
                "Member ID", "First Name", "Last Name", "Email", "Password", "Phone Number", "Weight", "Height", "Body Fat"
            ))
            print("-" * 150)

            for member in members:
                member_data = [str(field) if field is not None else "" for field in member]
                print("{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(*member_data))

            print("\n")
        else:
            print("No members found.")

        member_id = input("Enter the member ID for whom you want to create a routine: ")

        if not member_id.isdigit():
            print("Invalid member ID.")
            return

        member_id = int(member_id)
        cursor.execute("SELECT * FROM Members WHERE member_id = %s" , (member_id,))
        member = cursor.fetchone()

        if not member:
            print("Member not found.")
            return

        routine_name = input("Enter routine name: ")
        routine_description = input("Enter routine description: ")

        cursor.execute('''
            INSERT INTO Exersize_routines (member_id , routine_name , routine_desciption)
            VALUES (%s, %s, %s)
        ''' , (member_id , routine_name , routine_description))

        connection.commit()
        print("\nCustom routine created successfully.")

        cursor.execute("SELECT * FROM Exersize_routines WHERE member_id = %s", (member_id,))
        routines = cursor.fetchall()

        if routines:
            print("\nRoutines For This Member")
            print("{:<10}{:<20}{:<20}{:<20}".format("Routine ID" , "Member ID" , "Routine Name" , "Routine Description"))
            print("-" * 100)

            for routine in routines:
                print("{:<10}{:<20}{:<20}{:<20}".format(*routine))

            print("\n")

    except (Exception , psycopg2.Error) as error:
        print("Failed to create custom routine:" , error)

    finally:
        if cursor:
            cursor.close()

def update_trainer_info(connection , trainer):
    try:
        cursor = connection.cursor()
        print("Press enter to skip updating a value \n")
        trainer_id = trainer[0]

        while True:
            print("First Name: " + trainer[1])
            first_name = input("Update: ")
            if first_name == "0":
                return trainer
            elif first_name == '':
                break
            elif profile_management.valid_name(first_name):
                cursor.execute("UPDATE Trainers SET first_name = %s WHERE trainer_id = %s" , (first_name, trainer_id))
                break

        while True:
            print("Last Name: " + trainer[2])
            last_name = input("Update: ")
            if last_name == "0":
                return trainer
            elif last_name == "":
                break
            elif profile_management.valid_name(last_name):
                cursor.execute("UPDATE Trainers SET last_name = %s WHERE trainer_id = %s" , (last_name, trainer_id))
                break

        while True:
            print("Password: " + trainer[3])
            password = input("Update: ")
            if password == "0":
                return trainer
            elif password == "":
                break
            elif profile_management.valid_password(password):
                cursor.execute("UPDATE Trainers SET password = %s WHERE trainer_id = %s" , (password, trainer_id))
                break

        while True:
            print("Phone number: " + trainer[4])
            phone_number = input("Update: ")
            if phone_number == "0":
                return trainer
            elif phone_number == "":
                break
            elif profile_management.valid_phone_number(phone_number):
                cursor.execute("UPDATE Trainers SET phone_number = %s WHERE trainer_id = %s" , (phone_number, trainer_id))
                break

        connection.commit()
        
        return trainer

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to update trainer info:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

        

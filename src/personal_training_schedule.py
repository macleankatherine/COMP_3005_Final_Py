import psycopg2
import database_operations
from datetime import datetime

def schedule_personal_training(connection, user):
    try:
        cursor = connection.cursor()

        print("Select a Trainer:")
        print_all_trainers(connection)

        while True:
            trainer_id = input("Enter the ID of the trainer you want to schedule with: ")
            if not trainer_id.isdigit():
                print("Please enter a number.\n")
            elif(not valid_trainer_id(connection, trainer_id)):
                print("Please enter a valid trainer ID.\n")
            else:
                break

        trainer_id = int(trainer_id)

        while True:
            start_time = input("Enter the start time (HH:MM): ")
            if(validate_time_input(start_time)):
                break
         
        while True:
            end_time = input("Enter the end time (HH:MM): ")
            if(validate_time_input(end_time)):
                break

        while True:
            day_of_week = input("Enter day of the week: ")
            if(validate_day_of_week(day_of_week)):
                break

        if(not is_trainer_available(connection, trainer_id, day_of_week, start_time, end_time)):
            print("Trainer isn't available at this time")
            return
            #NEXT check if the trainer has other group/personal classes at the same time

        while True:
            booking_id = book_room(connection, day_of_week, start_time, end_time)
            if(booking_id):
                break
        
        while True:
            details = input("Enter any additional details for the session: ")
            if(len(details) > 200):
                print("Session detail can only be 200 characters max")
            else:
                break

        cursor.execute(""" 
            INSERT INTO Personal_training_classes (trainer_id, member_id, booking_id, details)
            VALUES (%s, %s, %s, %s)
            RETURNING class_id
        """, (trainer_id, user[0], booking_id, details))

        class_id = cursor.fetchone()[0]
        connection.commit()

        print(f"Personal training session scheduled successfully! Class ID: {class_id}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to schedule personal training session:", error)

    finally:
        if cursor:
            cursor.close()

def print_all_trainers(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT trainer_id, first_name, last_name FROM Trainers")
    trainers = cursor.fetchall()
    for trainer in trainers:
        print(f"{trainer[0]}. {trainer[1]} {trainer[2]}")

    cursor.close()

def valid_trainer_id(connection, trainer_id):
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Trainers WHERE trainer_id = %s", (trainer_id,))
        count = cursor.fetchone()[0]
        
        if count == 1:
            return True
        else:
            return False
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while checking trainer existence:", error)
        return False
    
    finally:
        if cursor:
            cursor.close()


def validate_time_input(time_str):
    try:
        # Parse the time string into a datetime object
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        # If the input doesn't match the expected format, return False
        return False
    
def validate_day_of_week(day_str):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    capitalized_day_str = (day_str.lower()).capitalize()  # Capitalize the first letter

    if capitalized_day_str in days_of_week:
        return capitalized_day_str
    else:
        print("Must enter a day (Monday, etc) ")
        return False


def is_trainer_available(connection, trainer_id, day_of_week, start_time, end_time):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM Trainer_Availability
            WHERE trainer_id = %s
            AND day_of_week = %s
            AND start_time <= %s
            AND end_time >= %s
        """, (trainer_id, day_of_week, start_time, end_time))

        available = cursor.fetchone()[0]

        if available == 0:
            print("Sorry, the selected trainer is not available at that time.")
            return False
        else:
            return True
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Failed to check trainer availability:", error)
        return False

    finally:
        if cursor:
            cursor.close()

def print_rooms(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT room_id, room_name FROM Rooms")
    rooms = cursor.fetchall()
    for room in rooms:
        print(f"{room[0]}. {room[1]}")

    cursor.close()

def valid_room(connection, room_id):

    try:
        cursor = connection.cursor()
        if(not room_id.isdigit()):
            print("PLease enter a number ")
            return False

        cursor.execute("SELECT COUNT(*) FROM Rooms WHERE room_id = %s;", (room_id,))
        room_count = cursor.fetchone()[0]
        cursor.close()

        if room_count == 1:
            return True
        else:
            print("Room with given ID does not exist.")
            return False
        
    except (psycopg2.Error, Exception) as error:
        print("Error while fetching data from PostgreSQL:", error)
        return False
    
    finally:
        cursor.close()

def room_has_conflicts(connection, room_id, day_of_week, start_time, end_time):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Room_bookings 
            WHERE room_id = %s 
            AND (start_time, end_time) OVERLAPS (%s::time, %s::time);
        """, (room_id, start_time, end_time))
        
        conflict_count = cursor.fetchone()[0]
        cursor.close()
        return conflict_count > 0
    
    except (psycopg2.Error, Exception) as error:
        print("Error occurred while checking room conflicts:", error)
        return True



def book_room(connection, day_of_week, start_time, end_time):
    try:
        cursor = connection.cursor()

        print("Select a Room:")
        print_rooms(connection)
        
        while True:
            room_id = input("Enter the ID of the room for the session: ")
            
            if not valid_room(connection, room_id):
                print("Invalid room ID. Please select a valid room.")
            elif room_has_conflicts(connection, room_id, day_of_week, start_time, end_time):
                print("This room has bookings that interfere with the requested time slot. Please choose another room.")
            else:
                break

        room_id = int(room_id)

        recurrence = input("Enter training's recurrence (weekly, etc): ")

        cursor.execute(""" 
            INSERT INTO Room_bookings (room_id, day_of_week, start_time, end_time, recurrence)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING booking_id
        """, (room_id, day_of_week, start_time, end_time, recurrence))

        booking_id = cursor.fetchone()[0]
        connection.commit()
        
        return booking_id

    except (psycopg2.Error, Exception) as error:
        connection.rollback()
        print("Error occurred while booking room:", error)
        return False
    
    finally:
        cursor.close()



def print_all_member_personal_sessions(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]
        
        cursor.execute("""
            SELECT pc.class_id, t.first_name || ' ' || t.last_name AS trainer_name,
                rb.day_of_week, rb.start_time, rb.end_time,
                r.room_name, rb.recurrence, r.capacity, pc.details
            FROM Personal_training_classes pc
            INNER JOIN Trainers t ON pc.trainer_id = t.trainer_id
            INNER JOIN Room_Bookings rb ON pc.booking_id = rb.booking_id
            INNER JOIN Rooms r ON rb.room_id = r.room_id
            WHERE pc.member_id = %s
        """, (member_id,))


        # Fetch all the results
        rows = cursor.fetchall()
        
        print("Personal Training Sessions: ")
        print_personal_training_session(rows)
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching personal training sessions:", error)
    finally:
        cursor.close()

def print_personal_training_session(rows):
    print("{:<5} {:<20} {:<20} {:<20} {:<20} {:<15} {:<15} {:<10}".format(
            "ID", "Trainer", "Day of Week", "Start Time", "End Time", "Room", "Recurrence", "Capacity"))
        
    for row in rows:
        class_id, trainer_name, day_of_week, start_time, end_time, room_name, recurrence, capacity, details = row
        print("{:<5} {:<20} {:<20} {:<20} {:<20} {:<15} {:<15} {:<10}".format(
            class_id, trainer_name, day_of_week, start_time.strftime("%H:%M:%S"), 
            end_time.strftime("%H:%M:%S"), room_name, recurrence, capacity, details))
        
        print("       Details: ", details , "\n")

    print("\n")

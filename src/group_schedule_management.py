import psycopg2
import database_operations

def print_available_group_classes(connection):
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT gc.class_id, gc.name, t.first_name || ' ' || t.last_name AS trainer_name,
                rb.day_of_week, rb.start_time, rb.end_time,
                r.room_name, rb.recurrence, r.capacity
            FROM Group_training_classes gc
            INNER JOIN Trainers t ON gc.trainer_id = t.trainer_id
            INNER JOIN Room_Bookings rb ON gc.booking_id = rb.booking_id
            INNER JOIN Rooms r ON rb.room_id = r.room_id
        """)

        # Fetch all the results
        rows = cursor.fetchall()
        
        print("Available Classes:")
        print_group_classes(rows)
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching available group classes:", error)
    finally:
        cursor.close()

def print_group_classes(rows):
    print("{:<5} {:<20} {:<20} {:<20} {:<20} {:<15} {:<15} {:<10}".format(
            "ID", "Name", "Trainer", "Day of Week", "Start Time", "End Time", "Room", "Recurrence", "Capacity"))
        
    for row in rows:
        class_id, name, trainer_name, day_of_week, start_time, end_time, room_name, recurrence, capacity = row
        print("{:<5} {:<20} {:<20} {:<20} {:<20} {:<15} {:<15} {:<10}".format(
            class_id, name, trainer_name, day_of_week, start_time.strftime("%H:%M"), 
            end_time.strftime("%H:%M"), room_name, recurrence, capacity))
    print("\n")

def schedule_group_class(connection, user):
    try:
        cursor = connection.cursor()

        print_available_group_classes(connection)
        print("What class would you like to register for? ")
        
        while True:
            class_id = input("Enter the class ID (or '0' to quit): ")

            if class_id == '0':
                return user
            elif not class_id.isdigit():
                print("Please enter the id as a number. ")
            elif(valid_group_class(connection, class_id) == None):
                print("The id entered doesn't match any avaiable classes. ")
            else:
                group_class = valid_group_class(connection, class_id)
                break
                
        if group_class:
            member_id = user[0]
            cursor.execute("INSERT INTO Group_training_class_members (class_id, member_id) VALUES (%s, %s)", (class_id, member_id))
            connection.commit()
            print("You have successfully registered for the class!")
            user = database_operations.get_user_by_member_id(connection, member_id)
            return user
        
        else:
            print("Something went wrong. ")
               
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        cursor.close()

def valid_group_class(connection, class_id):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Group_training_classes WHERE class_id = %s", (class_id,))
        group_class = cursor.fetchone()

        if(group_class):
            return group_class
        else: 
            return None
        
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return None
    
    finally:
        cursor.close()

def print_registered_group_classes(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]
        
        cursor.execute("""
            SELECT gc.class_id, gc.name, t.first_name || ' ' || t.last_name AS trainer_name,
                rb.day_of_week, rb.start_time, rb.end_time,
                r.room_name, rb.recurrence, r.capacity
            FROM Group_training_classes gc
            INNER JOIN Trainers t ON gc.trainer_id = t.trainer_id
            INNER JOIN Room_Bookings rb ON gc.booking_id = rb.booking_id
            INNER JOIN Rooms r ON rb.room_id = r.room_id
            INNER JOIN Group_training_class_members gcm ON gc.class_id = gcm.class_id
            WHERE gcm.member_id = %s
        """, (member_id,))

        # Fetch all the results
        rows = cursor.fetchall()
        
        print("\nRegistered Classes:")
        print_group_classes(rows)
    
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching registered group classes:", error)
    finally:
        cursor.close()

def drop_group_class(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]
        
        print_registered_group_classes(connection, user)
        
        print("Which class would you like to drop? Enter class ID (or '0' to go back): ")
        
        while True:
            class_id = input("Enter the class ID: ")
            if class_id == '0':
                return user
            elif not class_id.isdigit():
                print("Please enter the id as a number. ")
            elif(not is_registered_in_class(connection, class_id, member_id)):
                print("The id entered doesn't match any classes you're registered in. ")
            else:
                break
            
        cursor.execute("DELETE FROM Group_training_class_members WHERE class_id = %s AND member_id = %s", (class_id, member_id))
        connection.commit()
        print("You have successfully dropped the class.")
        user = database_operations.get_user_by_member_id(connection, member_id)
        return user
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()

def is_registered_in_class(connection, class_id, member_id):
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT class_id FROM Group_training_class_members WHERE class_id = %s AND member_id = %s", (class_id, member_id))
        if cursor.fetchone():
            return True
        else:
            return False
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        cursor.close()

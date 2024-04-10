import psycopg2
import database_operations
import profile_management

def register_member(connection):
    try:
        cursor = connection.cursor()
        print("Welcome new member!")
        print("Lets you started on your Fitness journey.\n")
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
            email = input("Enter email: ")
            if(email == "0"):
                return None
            elif(profile_management.valid_email(connection, email)):
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

        cursor.execute("INSERT INTO Members (first_name, last_name, email, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (first_name, last_name, email, password, phone_number))
        connection.commit()

        user = database_operations.get_user_by_email(connection, email)
        print("User registered successfully!")
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

def register_health_metrics(connection, user):
    try:
        cursor = connection.cursor()
        print("Lets get to know you better")
        print("Press enter to skip entering a value or > to switch units.\n")
        user_id = user[0]
        orignal_user = user

        user = profile_management.update_weight(connection, user)

        if(user is None):
           return orignal_user
        
        user = profile_management.update_height(connection, user)
        if(user is None):
            return orignal_user

        user = profile_management.update_bodyfat(connection, user)
        if(user is None):
            return orignal_user

        connection.commit()
        user = database_operations.get_user_by_member_id(connection, user_id)
        return user
        

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user health metrics:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()
        
def register_health_goal(connection, user):
    try:
        cursor = connection.cursor()
        print("What are your current fitness goals?")
        print("Include anything will help your trainer create a personalized experience.\n")
        member_id = user[0]

        while True:
            name, details = profile_management.valid_goal(user)

            cursor.execute("INSERT INTO Fitness_Goals (member_id, goal_name, goal_description) VALUES (%s, %s, %s)",
                (member_id, name, details))
            connection.commit()

            print("\n1. Add another health goal. ")
            print("0. Continue. ")
            cont = input()
            if(cont == "0"):
                return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user health goals:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

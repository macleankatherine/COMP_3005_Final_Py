import psycopg2

import database_operations
import profile_management



def register_admin(connection):
    try:
        cursor = connection.cursor()
        print("Welcome new Admin!")
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

        cursor.execute("INSERT INTO Administrators (first_name, last_name, email, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (first_name, last_name, email, password, phone_number))
        connection.commit()

        admin = database_operations.get_admin_by_email(connection, email)
        print(f"Admin {first_name} has been registered successfully!")
        return admin

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user:", error)
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

            email = input("Enter email: ")
            if(email == "0"):
              break
            password = input("Enter password: ")
            if(password == "0"):
              break

            cursor.execute("SELECT * FROM Administrators WHERE email = %s AND password = %s", (email, password))

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


def get_admin_by_email(connection, email):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Administrators WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return user
        else:
            print("Admin with email", email, "not found.")
            return None

    except (Exception, psycopg2.Error) as error:
        print("Failed to find Admin by email:", error)
        return None

    finally:
        if cursor:
            cursor.close()



# if choice == "7":
#                 user = admin.register_admin(connection)
#                 if(user):
#                     print("New Admin registered Successfully ") #redicrect to next menu funciton
#         elif choice == "8":
#                 user = admin.login_admin(connection)
#                 if(user):
#                     print("Admin Successfully Logged in") #redicrect to next menu funciton
            

# def admin_login_menu(connection, user):
#      while True:
#         print("Hello Admin", user[1])
#         print("1. Register as Admin")
#         print("2. Login as admin")
        
#         if choice == "1":
#                 user = admin.register_member(connection)
#                 if(user):
#                     print("New Admin registered Successfully ") #redicrect to next menu funciton
#         elif choice == "2":
#                 user = admin.login_admin(connection)
#                 if(user):
#                     print("Admin Successfully Logged in") #redicrect to next menu funciton
    
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             clear_terminal()
#         # elif choice == "2":
#         #     clear_terminal()
 
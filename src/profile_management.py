import psycopg2
import database_operations
import dashboard

def login_member(connection):
    try:
        cursor = connection.cursor()

        print("Welcome back! \nLets get you logged in\n")

        while True:
            user = None

            email = input("Enter email: ")
            if(email == "0"):
              break
            password = input("Enter password: ")
            if(password == "0"):
              break

            cursor.execute("SELECT * FROM Members WHERE email = %s AND password = %s", (email, password))

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



def update_member_personal_info(connection, user):
    try:
        cursor = connection.cursor()
        print("Press enter to skip updating a value \n")
        user_id = user[0]

        while True:
            print("First Name: " + user[1])
            first_name = input("Update: ")
            if(first_name == "0"):
                return user
            elif (first_name == ''):
                break
            elif(valid_name(first_name)):
                cursor.execute("UPDATE Members SET first_name = %s WHERE member_id = %s",
                    (first_name, user_id))
                break

        while True:
            print("Last Name: " + user[2])
            last_name = input("Update: ")
            if(last_name == "0"):
                return user
            elif(last_name == ""):
                break
            elif(valid_name(last_name)):
                cursor.execute("UPDATE Members SET last_name = %s WHERE member_id = %s",
                    (last_name, user_id))
                break

        while True:
            print("Email: " + user[3])
            email = input("Update: ")
            if(email == "0"):
                return user
            elif(email == ""):
                break
            elif(valid_email(connection, email)):
                cursor.execute("UPDATE Members SET email = %s WHERE member_id = %s",
                    (email, user_id))
                break
 
        while True:
            print("Password: " + user[4])
            password = input("Update: ")
            if(password == "0"):
                return user
            elif(password == ""):
                break
            elif(valid_password(password)):
                cursor.execute("UPDATE Members SET password = %s WHERE member_id = %s",
                    (password, user_id))
                break

        while True:
            print("Phone number: " + user[5])
            phone_number = input("Update: ")
            if(phone_number == "0"):
                return user
            elif(phone_number == ""):
                break
            elif(valid_phone_number(phone_number)):
                cursor.execute("UPDATE Members SET phone_number = %s WHERE member_id = %s",
                    (phone_number, user_id))
                break

        connection.commit()
        user = database_operations.get_user_by_member_id(connection, user_id)
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to update user info:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()
        
        
#Validation Helper functions
def valid_name(name):
    if len(name) < 2 or len(name) > 20:
        print("Names must be at 2-20 characters long.\n")
        return False
    elif not name.isalpha():
        print("Names can only contain characters.\n")
        return False
    else:
        return True

def valid_email(connection, email):
    if "@" not in email:
        print("Email must contain '@'.\n")
        return False
    elif len(email) < 2 or len(email) > 30:
        print("Emails must be 2-30 characters long.\n")
        return False
    elif(database_operations.is_email_in_database(connection, email)):
        print("Email is already in use.\n")
    else:
        return True
    
def valid_password(password):
    if len(password) < 6:
        print("Password must be at least 6 characters long.\n")
        return False
    else:
        return True
    
def valid_phone_number(phone_number):
    if not phone_number.isdigit():
        print("Phone number can contain only digits.\n")
        return False
    elif(len(phone_number) != 10):
        print("Phone number must be 10 characters long.\n")
        return False
    else:
        return True
    
def update_weight(connection, user):
    try:
        cursor = connection.cursor()
        weight_unit = " lbs"
        weight  = ""
        user_id = user[0]

        while True:
            weight = input("Enter weight ("+ weight_unit + "): ")

            if(weight == "0"):
                return None

            elif(weight == ""):
                return user

            elif(weight == '>'): 
                if(weight_unit == " lbs"):
                    weight_unit = "kg"
                elif(weight_unit == "kg"):
                    weight_unit = " lbs"

            elif not weight.isdigit():
                print("Weight can contain only have digits.\n")
            elif len(weight) < 2 or len(weight) > 5:
                print("Weight must be 2-5 characters long.\n")
            else:
                weight += weight_unit
                try:
                    cursor.execute("UPDATE Members SET weight = %s WHERE member_id = %s",
                        (weight, user_id))
                except (Exception, psycopg2.Error) as error:
                    print("ERROR in update \n")
                
                break

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
        
def update_height(connection, user):
    try:
        cursor = connection.cursor()
        user_id = user[0]

        while True:

            height_input = input("Enter height (cm): ")
            if height_input == "0":
                return None
            elif(height_input == ""):
                return user

            elif height_input == ">":
                while True:
                    feet = input("Enter feet: ")
                    if(feet == ">"):
                        break
                    inches = input("Enter inches: ")

                    if not (feet.isdigit() and inches.isdigit()):
                        print("Feet and inches must contain only digits.\n")
                    elif int(feet) < 1:
                        print("Feet must be at least 1.\n")
                    else:
                        height = f"{feet}ft {inches}in"
                        cursor.execute("UPDATE Members SET height = %s WHERE member_id = %s",
                        (height, user_id))
                        break
                if(feet != ">"):
                    break

            elif not height_input.isdigit():
                print("Height must contain only digits.\n")

            elif len(height_input) < 2:
                print("Height in cm must be at least 2 characters long.\n")

            else:
                height = f"{height_input}cm"
                cursor.execute("UPDATE Members SET height = %s WHERE member_id = %s",
                    (height, user_id))
                break
        
        connection.commit()
        user = database_operations.get_user_by_member_id(connection, user_id)
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user height metrics:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

def update_bodyfat(connection, user):
    try:
        user_id = user[0]
        cursor = connection.cursor()

        while True:

            body_fat_perc = input("Enter body fat percentage: ")
            if(body_fat_perc == "0"):
                return None
            elif(body_fat_perc == ""):
                return user
            
            elif len(body_fat_perc) < 1:
                print("Body fat percent must be at least 1 characters long.\n")
            elif not body_fat_perc.isdigit():
                print("Body fat percent must contain only numbers.\n")
            else:
                body_fat_perc += "%"
                cursor.execute("UPDATE Members SET bodyfat_percent = %s WHERE member_id = %s",
                    (body_fat_perc, user_id))
                break

        connection.commit()
        user = database_operations.get_user_by_member_id(connection, user_id)
        return user

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user height metrics:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

def valid_goal():

    while True:
        name = input("Enter the name of your goal: ")
        if(name == "0" or name == ""):
            return None
        elif(len(name) > 20 or len(name) < 2):
            print("Goal name can only be between 2-20 characters")
        else:
            details = input("Enter a detailed description of your goal: \n")

            if(details == "0"):
                return None
            elif(len(details) > 105 or len(details) < 10):
                print("Goal Description can only be between 10-105 characters")
            else:
                return name, details

def update_goal(connection, user):
    try:
        cursor = connection.cursor()
        print("What are fitness goals would you like to update?")
        print("Include anything will help your trainer create a personalized experience.\n")
        member_id = user[0]
        dashboard.print_fitness_goals(connection, member_id)

        while True:
            choice = input("\nWhat goal would you like to update?  ")
            if(choice == "0"):
                return user
            elif(not choice.isdigit()):
                print("Must enter a number \n")
            elif(database_operations.check_fitness_goal_exists(connection, choice, member_id)):
                break
            else:
                print("\nEnter a valid option ")

        while True:
            goals_info = valid_goal()
            if(goals_info is None):
                return user
            
            name, details = goals_info
            cursor.execute("UPDATE Fitness_Goals SET goal_name = %s, goal_description = %s WHERE goal_id = %s",
                (name, details, choice))

            connection.commit()

            print("\n1. Update another health goal ")
            print("0. Back ")
            cont = input("Enter your choice:  ")
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

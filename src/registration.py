import psycopg2
import database_operations

def register_member(connection):
    try:
        cursor = connection.cursor()
        print("Welcome new member!")
        print("Lets you started on your Fitness journey.\n")
        user = None

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                cursor.close()
                return None
            elif len(first_name) < 2:
                print("Names must be at least 2 characters long.\n")
            elif(not first_name.isalpha()):
                print("Names can only contain characters.\n")
            else:
                break

        while True:
            last_name = input("Enter last name: ")
            if(last_name == "0"):
                cursor.close()
                return None
            elif len(last_name) < 2:
                print("Names must be at least 2 characters long.\n")
            elif(not last_name.isalpha()):
                print("Names can only contain characters.\n")
            else:
                break

        while True:
            email = input("Enter email: ")
            if(email == "0"):
                cursor.close()
                return None
            elif "@" not in email:
                print("Email must contain '@'.\n")
            elif(database_operations.is_email_in_database(connection, email)):
                print("Email is already in use.\n")
            else:
                break

        while True:
            password = input("Enter password: ")
            if(password == "0"):
                cursor.close()
                return None
            elif len(password) < 6:
                print("Password must be at least 6 characters long.\n")
            else:
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                cursor.close()
                return None
            elif not phone_number.isdigit():
                print("Phone number can contain only digits.\n")
            elif(len(phone_number) != 10):
                print("Phone number must be 10 characters long.\n")
            else:
                break

        cursor.execute("INSERT INTO Members (first_name, last_name, email, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (first_name, last_name, email, password, phone_number))
        connection.commit()

        user = database_operations.get_user_by_email(connection, email)
        print("User registered successfully!")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()
            return user

def register_health_metrics(connection, user):
    try:
        cursor = connection.cursor()
        print("Lets get to know you better")
        print("Press enter to skip entering a value.\n")
        print("Press > to switch units.\n")
        user_id = user[0]

        weight_unit = "lbs"
        while True:
            weight = input("Enter weight ("+ weight_unit + "): ")
            if(weight == "0"):
                cursor.close()
                return user
            elif(weight == ""):
                break
            elif(weight == '>'): 
                if(weight_unit == "lbs"):
                    weight_unit = "kg"
                elif(weight_unit == "kg"):
                    weight_unit = "lbs"
            elif not weight.isdigit():
                print("Weight can contain only have digits.\n")
            elif len(weight) < 2:
                print("Weight must be at least 2 characters long.\n")
            else:
                weight += weight_unit
                cursor.execute("UPDATE Members SET weight = %s WHERE member_id = %s",
                    (weight, user_id))
                break

        while True:

            height_input = input("Enter height (cm): ")
            if height_input == "0":
                return user
            elif(height_input == ""):
                break

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

        while True:

            body_fat_perc = input("Enter body fat percentage: ")
            if(body_fat_perc == "0"):
                cursor.close()
                return user
            elif(body_fat_perc == ""):
                break

            elif len(body_fat_perc) < 1:
                print("Body fat percent must be at least 1 characters long.\n")
            else:
                body_fat_perc += "%"
                cursor.execute("UPDATE Members SET bodyfat_percent = %s WHERE member_id = %s",
                    (body_fat_perc, user_id))
                break

        connection.commit()
        user = database_operations.get_user_by_member_id(connection, user_id)
        

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user health metrics:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()
            return user


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
                break  
            else:
                print("Invalid email or password. Please try again.\n")

    except (Exception, psycopg2.Error) as error:
        print("Error during login:", error)

    finally:
        if connection:
            cursor.close()
            return user


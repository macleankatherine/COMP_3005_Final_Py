import psycopg2

def register_member(connection):
    try:
        cursor = connection.cursor()
        print("Welcome new member!")
        print("Lets you started on your Fitness journey.\n")

        while True:
            first_name = input("Enter first name: ")
            if(first_name == "0"):
                cursor.close()
                return
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
                return
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
                return
            elif "@" not in email:
                print("Email must contain '@'.\n")
            else:
                break

        while True:
            password = input("Enter password: ")
            if(password == "0"):
                cursor.close()
                return
            elif len(password) < 6:
                print("Password must be at least 6 characters long.\n")
            else:
                break

        while True:
            phone_number = input("Enter phone number: ")
            if(phone_number == "0"):
                cursor.close()
                return
            elif not phone_number.isdigit():
                print("Phone number can contain only digits.\n")
            elif(len(phone_number) != 10):
                print("Phone number must be 10 characters long.]n")
            else:
                break

        cursor.execute("INSERT INTO Members (first_name, last_name, email, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
                       (first_name, last_name, email, password, phone_number))
        connection.commit()
        print("User registered successfully!")

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to register user:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()

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
                break  # Break out of the loop if login is successful
            else:
                print("Invalid email or password. Please try again.\n")

    except (Exception, psycopg2.Error) as error:
        print("Error during login:", error)

    finally:
        if connection:
            cursor.close()
            return user


import psycopg2
from psycopg2 import Error

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Katherine",
            host="localhost",
            port="5432",
            database="final"
        )
        return connection
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

def register_user(connection):
    """Register a new user."""
    try:
        cursor = connection.cursor()

        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        phone_number = input("Enter phone number: ")

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

def login_user(connection):
   while True:
        try:
            cursor = connection.cursor()

            email = input("Enter email: ")
            password = input("Enter password: ")

            cursor.execute("SELECT * FROM Members WHERE email = %s AND password = %s", (email, password))

            #gets the user we're logging into
            user = cursor.fetchone()

            if user:
                print("Login successful!")
                print("Welcome,", user[1])  # user[1] is the first attribute (name)
                break  # Break out of the loop if login is successful
            else:
                print("Invalid email or password. Please try again.")

        except (Exception, psycopg2.Error) as error:
            print("Error during login:", error)

        finally:
            if connection:
                cursor.close()

def print_all_members(connection):
    """Print all members from the Members table."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members")

        members = cursor.fetchall()

        print("\n{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}".format("Member ID", "First Name", "Last Name", "Email", "Password", "Phone Number"))
        print("-" * 100)

        # Print each member
        for member in members:
            print("{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}".format(member[0], member[1], member[2], member[3], member[4], member[5]))
        print("\n")

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving members:", error)

    finally:
        if connection:
            cursor.close()

def delete_all_members(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Members")
        connection.commit()

        print("All members deleted successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error deleting members:", error)

    finally:
        if connection:
            cursor.close()

def main():
    # Connect to the database
    connection = connect_to_db()
    if connection:
       
        #delete_all_members(connection)
        while(True):
            register_user(connection)
            print_all_members(connection)
            login_user(connection)

        # Close the database connection
        connection.close()

if __name__ == "__main__":
    main()

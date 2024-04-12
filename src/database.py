import psycopg2
from psycopg2 import Error

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="simon",
            host="localhost",
            port="5432",
            database="final"
        )
        return connection
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None
        
def print_all_members(connection):
    """Print all members from the Members table."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members")

        members = cursor.fetchall()
        
        if members:
            while True:
                print("\n{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
                    "Member ID", "First Name", "Last Name", "Email", "Password", "Phone Number", "Weight", "Height", "Body Fat"
                ))
                print("-" * 150)

               # Print each member
                for member in members:
                    member_data = [str(field) if field is not None else "" for field in member]
                    print("{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(*member_data))

                print("\n")
                exit = input("Enter 0 to return: ")
                if exit == "0":
                    break
        else:
            print("No members found.")
                
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

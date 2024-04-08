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

# main.py

import registration
import database
# import profile_management
# import dashboard
# import schedule_management

def main():
 
    connection = database.connect_to_db()
    if connection:

        while True:
            print("\nWelcome to Fitness App!")
            print("Who are you?")
            print("1. New User")
            print("2. Returning Member")
            print("3. Trainer ")
            print("4. Adminastrator")
            print("5. print members DEBuG")
            print("0. Exit\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                registration.register_user(connection)
            elif choice == "2":
                registration.login_user(connection)
            # elif choice == "3":

            # elif choice == "4":

            elif choice == "5":
                database.print_all_members(connection)
            elif choice == "0":
                print("Exiting the application...")
                break
            else:
                print("Invalid choice. Please try again.")
    connection.close()

if __name__ == "__main__":
    main()

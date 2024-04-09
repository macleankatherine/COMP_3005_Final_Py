import registration
import profile_management
import database
import os

def clear_terminal():
    os.system('cls')

def main_menu(connection):
    while True:
        #clear_terminal()
        print("\nWelcome to Fitness App!\n")
        print("Who are you?")
        print("1. New User")
        print("2. Returning Member")
        print("3. Trainer ")
        print("4. Adminastrator")
        print("5. print members DEBuG")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = registration.register_member(connection)
            if(user):
                clear_terminal()
                registration.register_health_metrics(connection, user)

        elif choice == "2":
            clear_terminal()
            user = registration.login_member(connection)
            if(user):
                clear_terminal()
                member_menu(connection, user)
        # elif choice == "3":

        # elif choice == "4":

        elif choice == "5":
            database.print_all_members(connection)

        elif choice == "0":
            clear_terminal()
            print("Bye!\n")
            break
        else:
            print("Invalid choice. Please try again.")

def member_menu(connection, user):
     while True:
        print("Hello", user[1])
        print("Welcome Back!\n")
        print("1. Display Dashboard")
        print("2. Schedule Training")
        print("3. Update Member Information")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            print_user(user)            
        # elif choice == "2":
        #     clear_terminal()
        elif choice == "3":
            user = update_member_menu(connection, user)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def update_member_menu(connection, user):
    while True:
        print("What would you like to update", user[1])
        print("1. Personal Information")
        print("2. Health Metrics")
        print("3. Health Goals")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = profile_management.update_member_personal_info(connection, user)
        # elif choice == "2":
        #     clear_terminal()
        elif choice == "3":
            clear_terminal()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
    return user

def print_user(user):
    print("\nUser ID:", user[0])
    print("First Name:", user[1])
    print("Last Name:", user[2])
    print("Email:", user[3])
    print("Password:", user[4])
    print("Phone Number:", user[5],"\n")

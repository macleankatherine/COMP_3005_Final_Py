import registration
import profile_management
import personal_training_schedule
import group_schedule_management
import database
import database_operations
import admin
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
        print("6. print members with goals DEBUG")
        print("7. Adminastrator Resigtiation ")
        print("8. Adminastrator Login")

        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = registration.register_member(connection)
            if(user):
                #clear_terminal()
                user = registration.register_health_metrics(connection, user)
                if(user):
                    #clear_terminal()
                    user = registration.register_health_goal(connection, user)
                    if(user):
                        choice = "2"

        elif choice == "2":
            clear_terminal()
            user = profile_management.login_member(connection)
            if(user):
                clear_terminal()
                member_menu(connection, user)
        # elif choice == "3":

        elif choice == "4":  #if admin
            clear_terminal()
            user = admin.register_admin(connection)
            if(user):
                print("admin registered ")
                 
        elif choice == "5":
            database.print_all_members(connection)
        elif choice == "6":
            database_operations.print_members_goals(connection)

        
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
        print("2. Manage Personal Training")
        print("3. Manage Group Training")
        print("4. Update Member Information")
        print("5. print fitness goals DEBUG")
        print("6. print members DEBUG")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
        elif choice == "2":
        #     clear_terminal()
            user = schedule_perseonal_training_menu(connection, user)
        elif choice == "3":
            user = schedule_group_menu(connection, user)
        elif choice == "4":
            user = update_member_menu(connection, user)
        elif choice == "5":
            database_operations.print_fitness_goals(connection, user[0])
        elif choice == "6":
            database_operations.print_member(connection, user[0])
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

        elif choice == "2":
            clear_terminal()
            user = update_member_metric_menu(connection, user)
            
        elif choice == "3":
            clear_terminal()
            user = profile_management.update_goal(connection, user)

        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
    return user

def update_member_metric_menu(connection, user):
    while True:
        print("Select what metric you would like to update. \n")
        print("1. Weight: " + user[6])
        print("2. Height: "+ user[7])
        print("3. Body Fat %: "+ user[8])

        choice = input("Enter your choice: ")

        if choice == "1":
            #clear_terminal()
            user = profile_management.update_weight(connection, user)

        elif choice == "2":
            clear_terminal()
            user = profile_management.update_height(connection, user)

        elif choice == "3":
            clear_terminal()
            user = profile_management.update_bodyfat(connection, user)

        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

def schedule_group_menu(connection, user):
    while True:
        print("Select what you would like to do. \n")
        print("1. Enroll in Group class ")
        print("2. View enrolled classes ")
        print("3. Drop a class ")
        print("0. Go Back ")

        choice = input("Enter your choice: ")

        if choice == "1":
            #clear_terminal()
            user = group_schedule_management.schedule_group_class(connection, user)

        elif choice == "2":
            #clear_terminal()
            group_schedule_management.print_registered_group_classes(connection, user)

        elif choice == "3":
            #clear_terminal()
            user = group_schedule_management.drop_group_class(connection, user)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

def schedule_perseonal_training_menu(connection, user):
    while True:
        print("Select what you would like to do. \n")
        print("1. Schedule a personal training session ")
        print("2. View personal training sessions ")
        print("3. Cancel a session ")
        print("0. Go Back ")

        choice = input("Enter your choice: ")

        if choice == "1":
            #clear_terminal()
            personal_training_schedule.schedule_personal_training(connection, user)

        elif choice == "2":
            # clear_terminal()
            personal_training_schedule.print_all_member_personal_sessions(connection, user)

        elif choice == "3":
            # clear_terminal()
            personal_training_schedule.cancel_personal_session(connection, user)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")



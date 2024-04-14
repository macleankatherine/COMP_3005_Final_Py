import registration
import profile_management
import personal_training_schedule
import group_schedule_management
import manage_fitness_achievements
import database
import database_operations
import dashboard
import admin
import admin_menu
import os
import trainers_menu
import trainers

def clear_terminal():
    os.system('cls')

def main_menu(connection):
    while True:
        clear_terminal()
        print("\nWelcome to Big Boss Man Fitness!\n")
        print("Who are you?")
        print("1. New User")
        print("2. Returning Member")
        print("3. Trainer ")
        print("4. Administrator")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = registration.register_member(connection)
            if(user):
                clear_terminal()
                user = registration.register_health_metrics(connection, user)
                if(user):
                    clear_terminal()
                    user = registration.register_health_goal(connection, user)
                    if(user):
                        choice = "2"

        if choice == "2":
            clear_terminal()
            user = profile_management.login_member(connection)
            if(user):
                clear_terminal()
                member_menu(connection, user)

        elif choice == "3":
            clear_terminal()
            trainer = trainers.trainer_login(connection)
            if(trainer):
                clear_terminal
                trainers_menu.trainer_menu(connection , trainer)

        elif choice == "4":  
            clear_terminal()
            administrator = admin.login_admin(connection)
            if administrator:
                administrator=admin_menu.admin_menu(connection,administrator)
            else:
                print(" ID or password was invalid")
        elif choice == "5":
            database.print_all_members(connection)
        elif choice == "6":
            database_operations.print_members_goals(connection)

            user = admin_menu.admin_login_menu(connection)
        
        elif choice == "0":
            clear_terminal()
            print("Bye!\n")
            break
        else:
            print("Invalid choice. Please try again.")

def member_menu(connection, user):
     while True:
        clear_terminal()
        print("Hello", user[1])
        print("Welcome Back!\n")
        print("1. Display Dashboard")
        print("2. Manage Personal Training")
        print("3. Manage Group Training")
        print("4. Manage Health Achievements")
        print("5. Update Member Information")
        print("0. Log out\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            dashboard.display_dashboard(connection, user)
        elif choice == "2":
            clear_terminal()
            schedule_personal_training_menu(connection, user)
        elif choice == "3":
            clear_terminal()
            schedule_group_menu(connection, user)
        elif choice == "4":
            clear_terminal()
            manage_fitness_achievements_menu(connection, user)
        elif choice == "5":
            clear_terminal()
            user = update_member_menu(connection, user)

        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def update_member_menu(connection, user):
    while True:
        clear_terminal()
        print("What would you like to update", user[1])
        database_operations.print_member(connection, user[0])
        print("1. Personal Information")
        print("2. Health Metrics")
        print("3. Health Goals")
        print("4. Add Health Goal")
        print("0. Go Back\n")

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

        elif choice == "4":
            clear_terminal()
            user = registration.register_health_goal(connection, user)
            
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
    return user

def update_member_metric_menu(connection, user):
    while True:
        clear_terminal()
        print("Select what metric you would like to update. \n")
        print("1. Weight: " + (user[6] if user[6] is not None else " "))
        print("2. Height: "+ (user[7] if user[7] is not None else " "))
        print("3. Body Fat %: "+ (user[8] if user[8] is not None else " "))
        print("0. Go Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            clear_terminal()
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
        clear_terminal()
        print("Select what you would like to do. \n")
        print("1. Enroll in Group class ")
        print("2. View enrolled classes ")
        print("3. Drop a class ")
        print("0. Go Back ")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = group_schedule_management.schedule_group_class(connection, user)

        elif choice == "2":
            clear_terminal()
            while True:
                group_schedule_management.print_registered_group_classes(connection, user)
                exit = input("\nPress 0 to exit: ")
                if(exit == "0"):
                    break

        elif choice == "3":
            clear_terminal()
            user = group_schedule_management.drop_group_class(connection, user)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

def schedule_personal_training_menu(connection, user):
    while True:
        clear_terminal()
        print("Select what you would like to do. \n")
        print("1. Schedule a personal training session ")
        print("2. View personal training sessions ")
        print("3. Cancel a session ")
        print("0. Go Back ")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            clear_terminal()
            personal_training_schedule.schedule_personal_training(connection, user)

        elif choice == "2":
            clear_terminal()
            while True:
                personal_training_schedule.print_all_member_personal_sessions(connection, user)
                exit = input("\nPress 0 to exit: ")
                if(exit == "0"):
                    break

        elif choice == "3":
            clear_terminal()
            user = personal_training_schedule.cancel_personal_session(connection, user)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

def manage_fitness_achievements_menu(connection, user):
    while True:
        clear_terminal()
        print("Select what you would like to do. \n")
        print("1. Add new fitness Achievement!")
        print("2. Delete Fitness Achievement ")
        print("0. Go Back ")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            manage_fitness_achievements.add_achievement(connection, user)
        elif choice == "2":
            clear_terminal()
            manage_fitness_achievements.delete_achievement(connection, user)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")



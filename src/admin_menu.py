import admin
import registration
import profile_management
import personal_training_schedule
import group_schedule_management
import database
import database_operations
import admin
import os
import menu

def clear_terminal():
    os.system('cls')

        # -- ALL ADMIN MENUS UNDER HERE ------------
#                       PLEASE READ
#To integrate this into the main menu just copy paste everything under here into the menu.pu file and 
# do somthing like this:
# if choide == "4" .    #Administrator
# elif choice == "4":  #if admin
#             clear_terminal()
#             user = admin_login_menu(connection)
# #connected to the Admin_login_menu fucntion that returns a user
# Login menu lead to main Admin menu and has back/cancel operation navigation on every page
#
def admin_login_menu(connection):
     while True:

        print("\nHello Admin")
        print("1. Register as Admin")
        print("2. Login as Admin")
        print("0. Go back\n")

        choice = input("Enter your choice: ")

        if choice == "1":
                user = admin.register_admin(connection)
                if(user):
                    print("New Admin registered Successfully ") #redicrect to next menu funciton
        elif choice == "2":
                user = admin.login_admin(connection)
                if(user):
                    print("Admin Successfully Logged in") #redicrect to next menu funciton
                    admin_menu (connection,user)
        elif choice == "0":
            return None

 
 

# ------------ MAIN ADMIN MENU ------------------
#connects to a bunch of other menus
def admin_menu(connection, user):
     while True:
        print("\n\tHello Admin", user[1])
        print("1. Equipment maintenence")
        print("2. Room managment")
        print("3. Class scheduling")
        print("4. Billing and processing")
        print("5. Trainer management")
        print("6. Admin Management")
        print("")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear_terminal()
            user = admin_maintenence_menu(connection,user)
        elif choice == "2":
            clear_terminal()
            user = admin_room_menu(connection,user)
        elif choice == "3":
            clear_terminal()
            user = admin_class_management_menu(connection,user)
        elif choice == "4":
            clear_terminal()
            user = admin_billing_management_menu(connection,user)
        elif choice == "5":
            clear_terminal()
            user = admin_trainer_management_menu(connection,user)
        elif choice == "6":
            clear_terminal()
            user = admin_admin_management_menu(connection,user)
        elif choice == "0":# go back to privious menu
            return user
        else:
            print("Invalid choice. Please try again.")


#Admin sub menu
def admin_maintenence_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("Hello Admin", user[1])
        print("1. View Maintenence requests")
        print("2. Add Maintenence requests")
        print("3. Remove Maintenence requests")
        print("0. Go back")

        choice = input("Enter your choice: ")
        if choice == "1":
            admin.print_maintenence_requests(connection)
        elif choice == "2":
            admin.add_maintenence_requests(connection)
        elif choice == "3":
            admin.delete_maintenence_requests(connection)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

#Admin sub menu
def admin_room_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("Hello Admin", user[1])
        print("1. View all rooms")
        print("2. Add room")
        print("3. Delete room")
        print("0. Go back")

        choice = input("Enter your choice: ")
        if choice == "1":
            admin.print_rooms(connection)
        elif choice == "2":
            admin.add_room(connection)
        elif choice == "3":
            admin.delete_room(connection)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")



#Admin sub menu
def admin_class_management_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("\n \t Class Management Page!")
        print("1. View all scheduled classes (Group & Personal)")
        print("2. Add new Group class")
        print("3. Delete Group class")
        print("4. Add personal session")
        print("5. Delete personal session")
        print("0. Go back")

        choice = input("Enter your choice: ")
        if choice == "1":
            admin.print_group_schedule_data(connection)
        elif choice == "2":
            admin.create_group_training_class(connection)
        elif choice == "3":
            admin.delete_room(connection)
        elif choice == "4":
            personal_training_schedule.schedule_personal_training(connection,user)
        elif choice == "5":
            personal_training_schedule.cancel_personal_session(connection,user)
        
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")




#Admin sub menu
def admin_billing_management_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("\n \t Class Management Page!")
        print("1. View all Bills")
        print("2. View all Due Bills")
        print("3. View all completed Transactions")
        print("4. Remove Bill")
        print("5. Edit Bill")
        print("0. Go back")


        choice = input("Enter your choice: ")
        if choice == "1":
            admin.print_billing(connection)
        elif choice == "2":
            admin.print_due_bills(connection)
        elif choice == "3":
            admin.print_completed_bills(connection)
        elif choice == "4":
            admin.delete_bill(connection)
        elif choice == "5":
            admin.alter_billing(connection)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

#Admin submenu
def admin_trainer_management_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("\n \t Class Management Page!")
        print("1. Add trainer")
        print("2. Delete Trainer")
        print("3. View all Trainers")
        print("0. Go back")

        choice = input("Enter your choice: ")
        if choice == "1":
            admin.create_new_trainer(connection)
        elif choice == "2":
            admin.delete_trainer(connection)
        elif choice == "3":
            personal_training_schedule.print_all_trainers(connection)
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")

#Admin Sub Menu
def admin_admin_management_menu(connection, user):
     
    #this admin sub menu runs a loop for maintenence promtps until exited 
     while True:
        print("\n \t Class Management Page!")
        print("1. Add admin")
        print("2. Delete Admin")
        print("3. View all Admin")
        print("0. Go back")


        choice = input("Enter your choice: ")
        if choice == "1":
            admin.create_new_admin(connection)
        elif choice == "2":
            admin.delete_admin(connection)
        elif choice == "3":
            admin.print_admin_table_data(connection)
       
        elif choice == "0":
            return user
        else:
            print("Invalid choice. Please try again.")


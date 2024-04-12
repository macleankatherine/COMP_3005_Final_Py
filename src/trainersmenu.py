import database
import trainers

def trainer_menu(connection , trainer):
    while True:
        print("Hello Trainer" , trainer[1])
     
        print("\n1. View Class Schedule")
        print("2. View Member Profile")
        print("3. Update Availability")
        print("4. Create Custom Exercise Routines")
        print("5. Update Profile")
        print("0. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            trainers.show_class_schedules(connection , trainer[0] , trainer[1])
        elif choice == "2":
            searchUser = input("Enter member name to search: ")
            trainers.view_member_profiles(connection , searchUser)
        elif choice == "3":
            trainers.update_availability(connection , trainer[0])
        elif choice == "4":
            trainers.create_custom_routine(connection)
        elif choice == "5":
            trainer = trainers.update_trainer_info(connection , trainer)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

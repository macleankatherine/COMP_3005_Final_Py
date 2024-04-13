import admin

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
        elif choice == 0:
            return user
# main.py

import database
import menu
# import profile_management
# import dashboard
# import schedule_management

def main():
 
    connection = database.connect_to_db()

    if connection:
       menu.main_menu(connection)

    connection.close()

if __name__ == "__main__":
    main()

import psycopg2
import database_operations

def update_member_personal_info(connection, user):
    try:
        cursor = connection.cursor()
        print("Press enter to skip updating a value \n")
        user_id = user[0]

        while True:
            first_name = input("Update first name: ")
            if(first_name == "0"):
                cursor.close()
                return user
            elif (first_name == ''):
                break
            elif len(first_name) < 2:
                print("Names must be at least 2 characters long.\n")
            elif(not first_name.isalpha()):
                print("Names can only contain characters.\n")
            else:
                cursor.execute("UPDATE Members SET first_name = %s WHERE member_id = %s",
                    (first_name, user_id))
                break

        while True:
            last_name = input("Update last name: ")
            if(last_name == "0"):
                cursor.close()
                return user
            elif(last_name == ""):
                break
            elif len(last_name) < 2:
                print("Names must be at least 2 characters long.\n")
            elif(not last_name.isalpha()):
                print("Names can only contain characters.\n")
            else:
                cursor.execute("UPDATE Members SET last_name = %s WHERE member_id = %s",
                    (last_name, user_id))
                break

        while True:
            email = input("Update email: ")
            if(email == "0"):
                cursor.close()
                return user
            elif(email == ""):
                break
            elif "@" not in email:
                print("Email must contain '@'.\n")
            else:
                cursor.execute("UPDATE Members SET email = %s WHERE member_id = %s",
                    (email, user_id))
                break
 
        while True:
            password = input("Update password: ")
            if(password == "0"):
                cursor.close()
                return user
            elif(password == ""):
                break
            elif len(password) < 6:
                print("Password must be at least 6 characters long.\n")
            else:
                cursor.execute("UPDATE Members SET password = %s WHERE member_id = %s",
                    (password, user_id))
                break

        while True:
            phone_number = input("Update phone number: ")
            if(phone_number == "0"):
                cursor.close()
                return user
            elif(phone_number == ""):
                break
            elif not phone_number.isdigit():
                print("Phone number can contain only digits.\n")
            elif(len(phone_number) != 10):
                print("Phone number must be 10 characters long.]n")
            else:
                cursor.execute("UPDATE Members SET phone_number = %s WHERE member_id = %s",
                    (phone_number, user_id))
                break
        connection.commit()

        user = database_operations.get_user_by_member_id(connection, user_id)

    except (Exception, psycopg2.Error) as error:
        if connection:
            print("Failed to update user info:", error)
        else:
            print("Failed to connect to database.")

    finally:
        if connection:
            cursor.close()
            return user
        
        

import psycopg2

def get_user_by_email(connection, email):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Members WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return user
        else:
            print("User with email", email, "not found.")
            return None

    except (Exception, psycopg2.Error) as error:
        print("Failed to find user by email:", error)
        return None

    finally:
        if cursor:
            cursor.close()

def is_email_in_database(connection, email):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Members WHERE email = %s", (email,))
        count = cursor.fetchone()[0]
        return count > 0  # Returns True if email exists, False otherwise
    except (Exception, psycopg2.Error) as error:
        print("Error checking email existence:", error)
        return False  # Return False in case of any error
    finally:
        if cursor:
            cursor.close()

def get_user_by_member_id(connection, member_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
        user = cursor.fetchone()
        return user
    
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch user:", error)
        return None
    
    finally:
        if cursor:
            cursor.close()

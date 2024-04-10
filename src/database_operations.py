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

def print_fitness_goals(connection, member_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Fitness_Goals WHERE member_id = %s", (member_id,))
        goals = cursor.fetchall()

        if goals:
            print("\nFitness Goals:")
            print("-" * 100)

            for goal in goals:
                print(f"Goal ID: {goal[0]}")
                print(f"Goal Name: {goal[2]}")
                print(f"Goal Description: {goal[3]}")
                print("-" * 100)
            print("\n")
        else:
            print("No fitness goals found for this member.")

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve fitness goals:", error)

    finally:
        if cursor:
            cursor.close()

def print_member(connection, member_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
        member = cursor.fetchone()

        if member:
            print("\nMember Details:")
            print("-" * 30)
            print(f"Member ID: {member[0]}")
            print(f"First Name: {member[1]}")
            print(f"Last Name: {member[2]}")
            print(f"Email: {member[3]}")
            print(f"Phone Number: {member[5]}")
            if member[6]:
                print(f"Weight: {member[6]}")
            if member[7]:
                print(f"Height: {member[7]}")
            if member[8]:
                print(f"Body Fat Percentage: {member[8]}")
            print("-" * 30)
            print("\n")
        else:
            print("Member not found.")

    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve member details:", error)

    finally:
        if cursor:
            cursor.close()

def check_fitness_goal_exists(connection, goal_id, member_id):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM Fitness_Goals WHERE goal_id = %s AND member_id = %s)", (goal_id, member_id))
        goal_exists = cursor.fetchone()[0]

        return goal_exists

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if cursor:
            cursor.close()



def print_members_goals(connection):
    """Print all members from the Members table along with their fitness goals."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Members")

        members = cursor.fetchall()

        if members:
            print("\n{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
                "Member ID", "First Name", "Last Name", "Email", "Password", "Phone Number", "Weight", "Height", "Body Fat"
            ))
            print("-" * 150)

            for member in members:
                member_id, first_name, last_name, email, password, phone_number, weight, height, bodyfat_percent = member

                print("{:<10}{:<15}{:<15}{:<25}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
                    member_id, first_name, last_name, email, password, phone_number, weight if weight else "", height if height else "", bodyfat_percent if bodyfat_percent else ""
                ))

                cursor.execute("SELECT * FROM Fitness_Goals WHERE member_id = %s", (member_id,))
                goals = cursor.fetchall()

                if goals:
                    print("\nFitness Goals:")
                    for goal in goals:
                        print("{:<4}{:<15}{:<30}".format(goal[0], goal[2], goal[3]))

                

                print("-" * 150)

        else:
            print("No members found.")

    except (Exception, psycopg2.Error) as error:
        print("Error retrieving members:", error)

    finally:
        if connection:
            cursor.close()

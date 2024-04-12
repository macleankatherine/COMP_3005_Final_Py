import psycopg2

def add_achievement(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]

        while True:
            achievement_name = input("Enter the name of the achievement: ")
            if(achievement_name == "0"):
                return
            elif(len(achievement_name) < 2 or len(achievement_name) > 20):
                print("Name can only be 2-20 characters long. ")
            else:
                break

        while True:
            achievement_description = input("Enter a description for the achievement: ")
            if(len(achievement_description) < 10 or len(achievement_description) > 105):
                print("Details can only be 10-105 characters long. ")
            else:
                break

        cursor.execute("""
            INSERT INTO Fitness_achievements (member_id, achievement_name, achievement_description)
            VALUES (%s, %s, %s)
        """, (member_id, achievement_name, achievement_description))

        connection.commit()
        print("Achievement added successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        print("Error occurred while adding achievement:", error)
    finally:
        if cursor:
            cursor.close()

def delete_achievement(connection, user):
    try:
        cursor = connection.cursor()

        print_member_achievements(connection, user)

        while True:
            print("\nWhat achievement do you want to delete? ")
            achievement_id = input("Enter the id: ")
            if(achievement_id == "0"):
                return
            elif not achievement_id.isdigit():
                print("Please enter a number. \n")
            elif(valid_achievement_id(connection, user, achievement_id)):
                break
            else:
                print("The achievement id entered isn't valid \n")

        cursor.execute("DELETE FROM Fitness_achievements WHERE achievement_id = %s", (achievement_id,))
        connection.commit()
        print("Achievement deleted successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        print("Error occurred while deleting achievement:", error)
    finally:
        if cursor:
            cursor.close()

def valid_achievement_id(connection, user, achievement_id):
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM Fitness_achievements
            WHERE achievement_id = %s AND member_id = %s
        """, (achievement_id, user[0]))

        count = cursor.fetchone()[0]

        if count > 0:
            return True
        else:
            return False

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while checking achievement ID:", error)
        return False
    finally:
        if cursor:
            cursor.close()




def print_member_achievements(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]

        cursor.execute("""
            SELECT achievement_id, achievement_name, achievement_description
            FROM Fitness_achievements
            WHERE member_id = %s
        """, (member_id,))

        rows = cursor.fetchall()
        
        print(f"Fitness Achievements: ")
        print("{:<5} {:<20} {:<105}".format("ID", "Achievement Name", "Achievement Description"))
        print("-" * 130)

        
        for row in rows:
            achievement_id, achievement_name, achievement_description = row
            print("{:<5} {:<20} {:<105}".format(achievement_id, achievement_name, achievement_description))

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching member achievements:", error)
    finally:
        if cursor:
            cursor.close()
import psycopg2
import personal_training_schedule
import group_schedule_management
import manage_fitness_achievements

def display_dashboard(connection, user):
    try:
        cursor = connection.cursor()
        while True:
            member_id = user[0]
            first_name = user[1]
            weight = user[6]
            height = user[7]       
            bodyfat_percent = user[8]

            print("-" * 130)
            print(f"|{first_name}'s Dashboard".ljust(50) + f"Height: {height}".rjust(40) + f"Weight: {weight}".rjust(20) + f"Body fat %: {bodyfat_percent}".rjust(19) + f"|")
            print("-" * 130)

            print_fitness_goals(connection, member_id)
            print("\n")

            manage_fitness_achievements.print_member_achievements(connection, user)
            print("\n")
            
            personal_training_schedule.print_all_member_personal_sessions(connection, user)
            print("\n")

            group_schedule_management.print_registered_group_classes(connection, user)
            print("\n")

            print_members_exercise_routine(connection, user)
            print("\n")

            exit = input("Enter 0 to exit: ")
            if(exit == "0"):
                break


    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching user data:", error)
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
            print("{:<5} {:<20} {:<105}".format("ID", "Name", "Details"))

            print("-" * 130)
    
            for goal in goals:
                print("{:<5} {:<20} {:<50}".format(goal[0], goal[2], goal[3]))
        else:
            print("No fitness goals found for this member.")


    except (Exception, psycopg2.Error) as error:
        print("Failed to retrieve fitness goals:", error)

    finally:
        if cursor:
            cursor.close()
    
def print_members_exercise_routine(connection, user):
    try:
        cursor = connection.cursor()
        member_id = user[0]

        cursor.execute("""
            SELECT routine_id, routine_name, routine_description
            FROM Exercise_routines
            WHERE member_id = %s
        """, (member_id,))

        # Fetch all the results
        rows = cursor.fetchall()

        print("Personalized Exercise Routines: ")
        print("{:<5} {:<20} {:100}".format("ID", "Routine Name", "Routine Description"))
        print("-" * 130)

        for row in rows:
            routine_id, routine_name, routine_description = row
            print("{:<5} {:<20} {:<105}".format(routine_id, routine_name, routine_description))
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error occurred while fetching exercise routines:", error)
    finally:
        if cursor:
            cursor.close()


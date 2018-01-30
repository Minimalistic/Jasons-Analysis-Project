import psycopg2
import time # Used for time delay for on screen text prompts

def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<Error, no database found.>")

# drop_views = ("DROP VIEW top_slugs_view;")

db, cursor = connect()

view_top_slugs = ("CREATE VIEW top_slugs_view AS SELECT path,       \
                    COUNT(*) AS num_views FROM log                  \
                    WHERE status = '200 OK'                         \
                    AND NOT path = '/'                              \
                    GROUP BY path ORDER BY num_views DESC;")

answer_1 = ('SELECT title, num_views                                \
            FROM articles, top_slugs_view                           \
            WHERE top_slugs_view.path = CONCAT(\'/article/\', slug)   \
            ORDER BY num_views DESC LIMIT 3;')

def welcome_banner():
    print("")
    print("-------------------------------------------------")
    print("Welcome to Jason's Python Database Query Machine!")
    print("-------------------------------------------------")
    print_menu()

def print_menu(): # Displays options user can select
    print("")
    print("1) Top 3 Articles")
    print("2) Top Authors")
    print("3) Unfinished")
    print("4) Exit")
    print("")

def prompt_user():
    print("")
    user_input = input("Select an option 1-4: ")
    print_menu()
    if user_input == '1':
        print("Printing top 3 articles based on views...")
        print("")
        time.sleep(.2)

        """Test function to establish proper syntax for interacting with db."""
        db, cursor = connect()

        cursor.execute(view_top_slugs)
        cursor.execute(answer_1)
        # results = cursor.fetchall()
        for results in cursor.fetchall():
            print(results)
        db.close()
        prompt_user()

    elif user_input == '2':
        print("Printing Top 3 authors based on views...")
        prompt_user()
    elif user_input == '3':
        print("This query is not completed yet.")
        prompt_user()
    elif user_input == '4':
        print("Now quitting program...")
        time.sleep(.2)
        print("Program exited.") 
        return   
    else:
        print("Not a recognized option.")
        prompt_user()

welcome_banner()
prompt_user() 




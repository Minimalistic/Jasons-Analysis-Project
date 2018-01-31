import psycopg2
import time 
import sys  

"""SQL Views"""

view_top_slugs = ("CREATE OR REPLACE VIEW top_slugs_view AS SELECT path, \
                    COUNT(*) AS num_views FROM log                       \
                    WHERE status = '200 OK'                              \
                    AND NOT path = '/'                                   \
                    GROUP BY path ORDER BY num_views DESC;")
alt_view = ("CREATE OR REPLACE VIEW alt_view AS SELECT author, num_views \
            FROM articles, top_slugs_view                                \
            WHERE top_slugs_view.path = CONCAT('/article/', slug)        \
            ORDER BY num_views DESC;")
x_view = ("CREATE OR REPLACE VIEW x_view AS SELECT author, sum(num_views)           \
            FROM alt_view                                                \
            GROUP BY author;")
# Queries

answer_1 = ('SELECT title, num_views                                     \
            FROM articles, top_slugs_view                                \
            WHERE top_slugs_view.path = CONCAT(\'/article/\', slug)      \
            ORDER BY num_views DESC LIMIT 3;')

answer_2 = ('SELECT authors.name, x_view.sum                             \
            FROM x_view, authors                                         \
            WHERE x_view.author = authors.id                             \
            ORDER BY sum desc;')

def connect(database_name="news"):
    """Prepare database if it exists and create necessary views."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        cursor.execute(view_top_slugs)
        cursor.execute(alt_view)
        cursor.execute(x_view)
        return db, cursor
    except:
        print("<Error, no database found.>")

def slow_text():
    sys.stdout.write(l)
    sys.stdout.flush()
    print("")
    time.sleep(0.05)

welcome_banner = ('',
                  '-' * 50,
                  'Welcome to Jason\'s Python Database Query Machine!',
                  '-' * 50,)
help_prompt = "Type \"help\" for available commands."

text_menu = ('1) Top 3 Articles', # Displays options user can select
             '2) Top Authors',
             '3) Unfinished',
             '4) Exit')

def queryTop3Articles():
    db, cursor = connect()
    cursor.execute(answer_1)
    results = cursor.fetchall()
    for results in results:
        print(results)
        time.sleep(.05)
    db.close()

def queryTop3Authors():
    db, cursor = connect()
    cursor.execute(answer_2)
    results = cursor.fetchall()
    for results in results:
        print(results)
        time.sleep(.05)
    db.close()

def prompt_user():
    """Displays main command prompt user uses to interact with program"""
    print(help_prompt)
    user_input = input("Select an option 1-4: ")

    if user_input == '1':
        print('')
        print("Preparing top 3 articles based on views...")
        print('')
        time.sleep(.2)
        queryTop3Articles()
    elif user_input == '2':
        print('')
        print("Preparing Top 3 authors based on views...")
        print('')
        time.sleep(.2)
        queryTop3Authors()
    elif user_input == '3':
        print("This query is not completed yet.")
    elif user_input == '4':
        print("Now quitting program...")
        time.sleep(.2)
        print("Program exited.") 
        return   
    else:
        print("Not a recognized command.")

    prompt_user()

for l in welcome_banner:
    slow_text()

for l in text_menu:
    slow_text()

prompt_user()                    # Accept user commands




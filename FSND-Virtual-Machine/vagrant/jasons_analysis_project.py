import sys
import time
import psycopg2

"""Ensure user is running script with python 3 or greater"""

if sys.version_info[0] < 3:
    raise Exception("A minimum of Python version 3 is required to run.")

"""Prepare SQL Views"""

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

errors_view = ("CREATE OR REPLACE VIEW errors_day_view AS SELECT         \
                   DATE(time), COUNT(*) AS num_views                     \
                   FROM log                                              \
                   WHERE status = '404 NOT FOUND'                        \
                   GROUP BY status, DATE                                 \
                   ORDER BY num_views DESC;")

hits_view = ("CREATE OR REPLACE VIEW hits_day_view AS SELECT             \
                 DATE(time), COUNT(*) AS num_views                       \
                 FROM log GROUP BY DATE(time);")

"""Prepare Query answers"""

answer_1 = ("SELECT title, num_views                                     \
            FROM articles, top_slugs_view                                \
            WHERE top_slugs_view.path = CONCAT(\'/article/\', slug)      \
            ORDER BY num_views DESC LIMIT 3;")

answer_2 = ("SELECT authors.name, x_view.sum                             \
            FROM x_view, authors                                         \
            WHERE x_view.author = authors.id                             \
            ORDER BY sum DESC LIMIT 31;")

answer_3 = ("SELECT hits_day_view.date,                                  \
            ROUND(SUM(CAST(errors_day_view.num_views AS decimal)         \
            /                                                            \
            CAST(hits_day_view.num_views AS decimal) * 100), 2)          \
            AS bad_requests                                              \
            FROM hits_day_view, errors_day_view                          \
            WHERE hits_day_view.date = errors_day_view.date              \
            GROUP BY hits_day_view.date                                  \
            ORDER BY bad_requests DESC LIMIT 1;")


def connect(database_name="news"):
    """Connect to database if it exists and create necessary views."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        cursor.execute(view_top_slugs)
        cursor.execute(alt_view)
        cursor.execute(x_view)
        cursor.execute(errors_view)
        cursor.execute(hits_view)
        return db, cursor
    except:
        print("<Error, no database found.>")


def cleanPrint(y):
    for x in y:
        print('-->', x[0], '--', x[1])


def listPrinter(string):
    """Prints string at a delayed speed as a list"""
    for character in string:
        print(character)
        time.sleep(.05)


def printDivider(x):
    print('-' * len(x))
    print(x)
    print('-' * len(x))
    time.sleep(.02)

welcome_banner = ('Welcome to Jason\'s Python Database Query Machine!')

text_menu = ('1) Top 3 Articles',
             '2) Top Authors',
             '3) Days With Greatest Percent Request Errors',
             '4) Exit')


def queryTop3Articles():
    """Returns the 3 most popular articles."""
    db, cursor = connect()
    cursor.execute(answer_1)
    results = cursor.fetchall()
    cleanPrint(results)
    db.close()


def queryTop3Authors():
    """Returns the 3 most popular authors."""
    db, cursor = connect()
    cursor.execute(answer_2)
    results = cursor.fetchall()
    cleanPrint(results)
    db.close()


def queryTopRequestErrors():
    """Returns the days where more than 1% of requests lead to errors."""
    db, cursor = connect()
    cursor.execute(answer_3)
    results = cursor.fetchall()
    cleanPrint(results)
    db.close()


def prompt_user():
    """Display main command prompt used for interacting with program."""
    print()
    user_input = input("Select an option 1-4: ")

    if user_input == '1':
        printDivider("Preparing top 3 articles based on views...")
        queryTop3Articles()
    elif user_input == '2':
        printDivider("Preparing Top 3 authors based on views...")
        queryTop3Authors()
    elif user_input == '3':
        printDivider("Preparing data on days where more than " +
                     "one percent of requests lead to errors...")
        queryTopRequestErrors()
    elif user_input == '4':
        printDivider("Now exiting program...")
        time.sleep(.3)
        print("Program exited.")
        return
    else:
        printDivider("Not a recognized command.")
    prompt_user()

printDivider(welcome_banner)    # Print program start banner to user
listPrinter(text_menu)          # Display available commands in the menu
prompt_user()                   # Accept user commands

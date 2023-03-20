"""
Student name(s): Alexis Wang and Emma Gurcan
Student email(s): alexisw@caltech.edu and egurcan@caltech.edu
High-level program overview: A relational database of volleyball players from
the 2020 FIBV Preliminary Round from the women's league.

******************************************************************************
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client.
DEBUG = False


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='admin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='volleyballdb' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
# Returns all players with a specified jersey.
def findPlayerWithJersey():
    ans = input("What jersey number do you want to search for? ")
    while not ans.isnumeric():
        ans = input("Non-numeric answer - try again: ")
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT player_name, country FROM player WHERE shirt_number = \'%s\';' % (ans, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print("Player: " + row[0] + ", " + row[1])
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred - please check your input is a valid jersey number.')

# Returns the player with the most amount of attacks, blocks, and serves.
# Asks for user's input of a country code.
def findTopPlayer():
    ans = input("What country do you want to search for? ")
    while len(ans) != 3:
        ans = input("Must be a three character country code. Try again: ")
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT player_name, scorers.attacks + scorers.blocks + scorers.serves AS stats FROM scorers ' \
    + 'NATURAL JOIN player WHERE country = \'%s\' ORDER BY stats DESC LIMIT 1;' % (ans, )
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("No country found with that code, or no players found from that country.")
        else:
            print(row[0] + " with " + str(row[1]) + " attacks, blocks, and serves.")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check your country is represented in the dataset.')

# Returns the player with the most dig faults given a league inputted by the client.
# The only league options allowed are men's and women's. If no players from a certain league
# is found, that will be printed out and displayed for the client.
def findPlayerDigs():
    cursor = conn.cursor()
    ans = input("What league do you want to search for? (m/w) ")
    while ans.lower()[0] != 'm' and ans.lower()[0] != 'w':
        ans = input("Invalid league, try again: ")
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT player_name, dig_faults FROM passers ' \
    + 'NATURAL JOIN player WHERE league = \'%s\' ORDER BY dig_faults DESC LIMIT 1;' % (ans.lower()[0], )
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            print("None: no players from specified league found.")
        else:
            print(row[0] + " with " + str(row[1]) + " dig faults.")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check your league is represented in the dataset.')    
# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)
def log_in():
    username = input("What is your username? ")
    password = input("What is your password? ")
    cursor = conn.cursor()
    sql = 'SELECT authenticate(\'%s\', \'%s\');' % (username, password)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row[0]:
            print("Success!")
            if checkAdmin(username): 
                show_admin_options()
        else:
            print("User not found, try again.")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please ensure you have an account.')

def checkAdmin(username):
    sql = 'SELECT is_admin FROM user_info WHERE username = \'%s\'' % (username, )
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row[0] == 'y':
            return True
        return False
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please ensure all inputs are accurate.')
    

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (l) - login')
    print('  (c) - find the highest scoring player of a country')
    print('  (j) - find players with a certain jersey number')
    print('  (d) - find the player with the most dig faults for a league')
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        log_in()
    elif ans == 'c':
        findTopPlayer()
    elif ans == 'j':
        findPlayerWithJersey()
    elif ans == 'd':
        findPlayerDigs()

def addPlayer():
    cursor = conn.cursor()
    name = input("What is the player's name? ")
    shirt = input("How about their jersey number? ")
    country = input("What is the country they are playing for? ")
    league = input("What league are they in? Enter m/w: ")
    gender = input("Finally, what is their gender? ")
    sql = 'INSERT INTO player (player_name, shirt_number, country, league, gender)' \
        + 'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')' % (name, shirt, country, league, gender)
    try:
        cursor.execute(sql)
        print("Added!")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check your inputs are correct and compatible.')  

# Uses the procedure from Part I. Updates the servers table with the 
def updateServes():
    cursor = conn.cursor()
    id = input("What is the player's ID? ")
    aces = input("How many aces did this player newly score? ")
    faults = input("How many serve faults were there (if any)? ")
    # Update command should trigger the procedure
    sql = "UPDATE servers SET num_aces = num_aces + \'%s\', num_faults = num_faults + \'%s\' WHERE player_id = \'%s\';" % (aces, faults, id) 
    try:
        cursor.execute(sql)
        print("Updated!")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check your inputs are correct and compatible.')  

# Adds a user to the user_info table using the sp_add_user procedure.
# Only admins can add other users. Must specify the username, password, 
# and whether the user is an admin or not.
def addUser():
    cursor = conn.cursor()
    username = input("Create a username: ")
    password = input("Create a password: ")
    is_admin = input("Is this user an admin? (y/n) ")
    while is_admin != 'y' and is_admin != 'n':
        is_admin = input("Wrong input. Is this user an admin? (y/n) ")
    sql = 'CALL sp_add_user (\'%s\', \'%s\', \'%s\');' % (username, password, is_admin)
    try:
        cursor.execute(sql)
        print("Added!")
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check your inputs are correct and compatible.')  

# Another example of where we allow you to choose to support admin vs. 
# client features  in the same program, or
# separate the two as different app_client.py and app_admin.py programs 
# using the same database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    print('Welcome admin! What would you like to do? ')
    print('  (a) - add a volleyball player')
    print('  (s) - update the serve statistics for a player')
    print('  (u) - add a new client')
    print('  (n) - nothing: bring me to see the player\'s stats')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        addPlayer()
    elif ans == 's':
        updateServes()
    elif ans == 'u':
        addUser()
    elif ans == 'n':
        show_options()


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()

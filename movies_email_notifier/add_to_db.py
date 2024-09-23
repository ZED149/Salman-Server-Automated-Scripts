
# this file will write existing movies names directory names to the Database
# before writing we need to split the name in a better readable format
# e.g Torbaaz (2024) (2160p) (YTS.MX) should be stored as Torbaaz


# importing some important files
import sqlite3
import os
from dotenv import load_dotenv

# loading enviornmental variables into our scope
load_dotenv()

# GLOBAL Variables
DB_NAME = os.getenv('DB_NAME')
CURR_DIR = os.getcwd()
WORKING_DIR = "Z:\\movies"


# making connection to the Database
print(f"Trying connecting to the database {DB_NAME}")
conn = sqlite3.connect(DB_NAME)

# if connection is successful
if conn:
    print("Connection successful")
    # CURSOR
    cursor = conn.cursor()
    # Create Table Query
    create_table_query = """
    CREATE TABLE "movies" (
	"name"	TEXT NOT NULL UNIQUE,
	"id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id")
    );"""

    # creting table (movies) in the db
    try:
        cursor.execute(create_table_query)
    except sqlite3.OperationalError as e:
        print(e)
        exit(0)
    
    # after table creating, we need to iterate on root
    # then, write all folder names in a given format to the db
    for root, folders, files in os.walk(WORKING_DIR):
        for index, folder in enumerate(folders):
            altered_name = folder.split(' (')[0]
            # adding altered name to the DB
            try:
                cursor.execute('''INSERT INTO movies(name) VALUES(?)
                               ''',[altered_name])
            except sqlite3.IntegrityError as e:
                print(e)
                exit(0)
        
    # commiting changes to the DB
    conn.commit()
else:
    print(f"Connection to the databse {DB_NAME} failed.")
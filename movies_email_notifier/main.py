

# The script will check the files/folders within a ROOT DIRECTORY with a DB
# if there is any folder that is present in the root but not in the DB
# it will add it to the DB
# then, it will send email to the recipients(defined in a separate Excel file) regarding what folders are added to the ROOT


# importing some important libraries
import os
import sqlite3
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from dotenv import load_dotenv
from message_generator import MessageGenerator
from email.mime.image import MIMEImage
from datetime import datetime
from email.utils import formataddr
from email.message import EmailMessage
from email.header import Header


# loading our ENVIRONMENTAL VARIABLES into our scope
load_dotenv()

# GLOBAL
WORKING_DIR: str = "E:\\media\\movies\\not watched"                # root directory to walk on
DB_NAME: str = os.getenv('DB_NAME')                                  # name of the DB to check with
MOVIES: list                                                # placeholder to store fetched movie names
NEW_MOVIES_ADDED: list = []                                 # placeholder to store new movie names that are uploaded
EXCEL_FILE = os.getenv('EXCEL_FILE')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
DISPLAY_NAME = os.getenv("DISPLAY_NAME")


# CONFIGURATIONS

# send_email_core
def send_email_core(username: str, receiver: str,
                    message: str, host: str, port: int, context,
                    password: str) -> None:
    msg = MIMEMultipart('related')
    # msg = EmailMessage()
    # msg['From'] = email.utils.formataddr((DISPLAY_NAME, username))
    msg['From'] = formataddr((str(Header('ZED', 'utf-8')), username))
    msg['To'] = receiver
    msg['Subject'] = 'Test Mail'
    msg.preamble = "This is a multi-part message in MIME format."

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText("This is the alternative plain text message.")
    msgAlternative.attach(msgText)

    msgText = MIMEText(message, 'html')
    msgAlternative.attach(msgText)

    with open('test.png', 'rb') as fb:
        msgImage = MIMEImage(fb.read())

    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    # send email    
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, msg.as_string())

# DB_Fetch_Names
def db_fetch_movie_names() -> list:
    # making a connection to the DB
    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.OperationalError as e:
        # send email to the server admin regarding failure to connect to the movies DB
        host = "smtpout.secureserver.net"
        port = 465

        username = EMAIL_USERNAME
        password = EMAIL_PASSWORD

        receiver = os.getenv('SERVER_ADMIN_EMAIL')
        context = ssl.create_default_context()

        # message string
        message = f"""Unable to connect to the Database file.
Error occurred while trying to connect to the database is:
{e}"""
        send_email_core(username, receiver, message, host, port, context, password)
        exit(0)

    # if the DB connection is successful
    cursor = conn.cursor()
    cursor.execute('''SELECT name from movies''')
    movies = cursor.fetchall()
    conn.close()
    return [m[0] for m in movies]
MOVIES = db_fetch_movie_names()


# add_to_DB
def add_to_db(name: str) -> None:
    # connecting to the DB
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO movies(name) VALUES(?)''',[name])
    conn.commit()
    conn.close()

# send email
def send_email(first_name, last_name, email) -> None:
    """
    Sends an email to the recipient of the form.
    :param first_name:  First name of the receiver
    :param last_name:   Last name of the receiver
    :param email:       Email of the receiver
    :return:            None
    """

    host = "smtpout.secureserver.net"
    port = 465

    username = EMAIL_USERNAME
    password = EMAIL_PASSWORD

    receiver = email
    context = ssl.create_default_context()

    # message string
    message = MessageGenerator.no_reply_movies_added(first_name, NEW_MOVIES_ADDED)

    # core functionality to send email
    send_email_core(username, receiver, message, host, port, context, password)


def iterate_and_send_email():
    # read Excel file
    df = pd.read_excel(EXCEL_FILE)
    # iterating on df
    for index, row in df.iterrows():
        send_email(row['First Name'], row['Last Name'], row['Email'])

    # logging to the log file
    date = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    with open('log', 'a') as file:
        file.write(f"[SERVER] Email sent on {date}.\n")
# MAIN
# iterating on root directory
for root, folders, files in os.walk(WORKING_DIR):
    for folder in folders:
        # check if there are new folders 
        altered_name = folder.split(' (')[0]
        # if name is not in the fetched MOVIES list
        if altered_name not in MOVIES:
            # add the name to the DB
            add_to_db(altered_name)
            NEW_MOVIES_ADDED.append(altered_name)

# we have a list of newly added movies
# need to send email to the recipients regarding the name of the new movies
# if there are new directories found that are not present on the server already
if len(NEW_MOVIES_ADDED) > 0:
    print("Sending Emails to the recipients.")
    iterate_and_send_email()
else:
    # log to the file either an email was sent or not
    # logging to file
    date = datetime.now().strftime("%d-%m-%y, %H:%M:%S")
    with open('log', 'a') as file:
        file.write(f"[SERVER] Email not sent on {date}.\n")
    print("No new movies found.")

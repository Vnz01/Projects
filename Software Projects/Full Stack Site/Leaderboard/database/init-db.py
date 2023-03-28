# Add the necessary imports
import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv
import bcrypt

load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE if not exists Leaderboard")
cursor.execute("USE Leaderboard")
cursor.execute("drop table if exists users;")
cursor.execute("drop table if exists MVP;")
cursor.execute("drop table if exists ScoreComments;")
cursor.execute("drop table if exists sessions;")

try:
   cursor.execute("""
   CREATE TABLE users (
       id           integer  AUTO_INCREMENT PRIMARY KEY,
       username     VARCHAR(100) NOT NULL unique,   
       email        VARCHAR(100) NOT NULL unique,   
       studentId    VARCHAR(100) NOT NULL,   
       password     VARCHAR(100) NOT NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:
   cursor.execute("""
   CREATE TABLE ScoreComments (
       scorecomment_id       integer AUTO_INCREMENT PRIMARY KEY,
       score                 VARCHAR(10) NULL,   
       comment               VARCHAR(1000) NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:
   cursor.execute("""
   CREATE TABLE MVP (
       MVP_id        integer AUTO_INCREMENT PRIMARY KEY,
       MVPidea               VARCHAR(1000) NOT NULL,   
       comment               VARCHAR(1000) NULL,
       scorecomment_id    integer, FOREIGN KEY (scorecomment_id ) REFERENCES ScoreComments(scorecomment_id)
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:
   cursor.execute("""
   create table if not exists sessions (
  session_id varchar(64) primary key,
  session_data json not null,
  created_at timestamp not null default current_timestamp
);
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

pwd_salt = bcrypt.gensalt()
pwd = bcrypt.hashpw('PASSWORD'.encode('utf-8'), pwd_salt)

try:
   
   query = 'INSERT INTO users (username, email, studentID, password) values (%s, %s, %s, %s)'
   values = ("Admin","Admin","Admin",pwd)
   cursor.execute(query, values)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

db.commit()
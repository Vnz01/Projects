# Add the necessary imports
import mysql.connector as mysql
import os
import datetime

from dotenv import load_dotenv

load_dotenv("credentials.env")
# Read Database connection variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']


# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

#creating and using database
cursor.execute("CREATE DATABASE if not exists Weather")
cursor.execute("USE Weather")

cursor.execute("drop table if exists Temperature;")
cursor.execute("drop table if exists LightLevel;")
cursor.execute("drop table if exists Humidity;")

try:    
   cursor.execute("""
   CREATE TABLE Temperature (
       id        integer  AUTO_INCREMENT PRIMARY KEY,
       time         VARCHAR(50),
       temp   int

   );
 """)   
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:    
   cursor.execute("""
   CREATE TABLE LightLevel (
       id          integer  AUTO_INCREMENT PRIMARY KEY,
       time         VARCHAR(50),
       light       int

   );
 """)   
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:    
   cursor.execute("""
   CREATE TABLE Humidity (
       id          integer  AUTO_INCREMENT PRIMARY KEY,
       time         VARCHAR(50),
       hum     int

   );
 """)   
except RuntimeError as err:
   print("runtime error: {0}".format(err))

db.commit()
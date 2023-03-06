# Add the necessary imports
import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE if not exists Restaurant")
cursor.execute("USE Restaurant")
cursor.execute("drop table if exists Orders;")
cursor.execute("drop table if exists Menu_Items;")

try:
   cursor.execute("""
   CREATE TABLE Menu_Items (
       item_id          integer  AUTO_INCREMENT PRIMARY KEY,
       name             VARCHAR(100) NOT NULL,   
       price            integer NOT NULL
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

try:
   cursor.execute("""
   CREATE TABLE Orders (
       order_id        integer AUTO_INCREMENT PRIMARY KEY,
       customer            VARCHAR(100) NULL,    
       quantity       VARCHAR(50) NULL,
       status          VARCHAR(50) NULL,
       item_id        integer, FOREIGN KEY (item_id) REFERENCES Menu_Items(item_id)
   );
 """)
except RuntimeError as err:
   print("runtime error: {0}".format(err))

query = "insert into Menu_Items (name, price) values (%s,%s)"

values = [
 ('Hamburger','5'),
 ('Fries','3'),
 ('Soda','1'),
 ('Hotdog','2'),
 ('Pizza','3')
]

cursor.executemany(query, values)

db.commit()
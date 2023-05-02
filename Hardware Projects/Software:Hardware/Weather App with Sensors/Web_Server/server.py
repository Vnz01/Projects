from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi.responses import RedirectResponse
import os
import bcrypt
import dbutils as db  
from datetime import datetime
from multiprocessing import Process
import requests
from urllib.request import urlopen  
import json
import mysql.connector as mysql
from dotenv import load_dotenv
import time
# import RPi.GPIO as GPIO

app = FastAPI()
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()
cursor.execute("USE Weather")

# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")


def make_request(url):
    while(True):
        try:
            response = requests.get(url)
            return response
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

#root route
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("index.html") as html:
       return HTMLResponse(content=html.read())

def post_temp():
    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    val = (formatted_date, get_temp())
    query = "insert into Temperature (time, temp) values (%s, %s)"
    cursor.execute(query, val)
    db.commit()

def post_light():
    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    val = (formatted_date, get_light())
    query = "insert into LightLevel (time, light) values (%s, %s)"
    cursor.execute(query, val)
    db.commit()

def post_humidity():
    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    val = (formatted_date, get_humidity())
    query = "insert into Humidity (time, hum) values (%s, %s)"
    cursor.execute(query, val)
    db.commit()

#accessing get route from raspberry pi
def get_temp():
    print("calling get temp!")
    url = "http://raspberrypi.local:6543/temp"

    # A GET request to the API
    response = make_request(url)

    # Print the response
    response_json = response.json()
    print(response_json)
    return response_json["temp"]

#accessing get route from raspberry pi
def get_light():
    print("calling get light!")
    url = "http://raspberrypi.local:6543/light"

    # A GET request to the API
    response = make_request(url)

    # Print the response
    response_json = response.json()
    print(response_json)
    return response_json["light"]

#accessing get route from raspberry pi
def get_humidity():
    print("calling get humidity!")
    url = "http://raspberrypi.local:6543/hum"

    # A GET request to the API
    response = make_request(url)

    # Print the response
    response_json = response.json()
    print(response_json)
    return response_json["humidity"]

def collect_data():
    """
    Every several seconds, make requests to the Raspberry Pi API to collect sensor data and store it in the SQL database, then make a request to Raspberry Pi API to display the most recent weather data on the LCD.
    """
    while (True):
        post_temp()
        time.sleep(1)
        post_light()
        time.sleep(1)
        post_humidity()
        time.sleep(13)
        
@app.get("/recent_temp", response_class=JSONResponse)
def get_recent_temps() -> JSONResponse:
   # query the database with the column names. .execute() executes the given query in the database.
   db =mysql.connect(user=db_user, password=db_pass, host=db_host)
   new_cursor = db.cursor()
   new_cursor.execute("USE Weather")
   new_cursor.execute("SELECT * FROM Temperature ORDER BY id DESC LIMIT 8;")
   
   # fetch the remaining rows
   records = new_cursor.fetchall()
   response = {}
   for index, row in enumerate(records):
       response[index] = {
           "id": row[0],
           "time": row[1],
           "temp": row[2]
       }
   new_cursor.close()
   return JSONResponse(response)

@app.get("/recent_hum", response_class=JSONResponse)
def get_recent_hums() -> JSONResponse:
   db =mysql.connect(user=db_user, password=db_pass, host=db_host)
   new_cursor = db.cursor()
   new_cursor.execute("USE Weather")
   new_cursor.execute("SELECT * FROM Humidity ORDER BY id DESC LIMIT 8;")
   
   # fetch the remaining rows
   records = new_cursor.fetchall()
   response = {}
   for index, row in enumerate(records):
       response[index] = {
           "id": row[0],
           "time": row[1],
           "hum": row[2]
       }
   new_cursor.close()
   return JSONResponse(response)

@app.get("/recent_light", response_class=JSONResponse)
def get_recent_light() -> JSONResponse:
   db =mysql.connect(user=db_user, password=db_pass, host=db_host)
   new_cursor = db.cursor()
   new_cursor.execute("USE Weather")
   new_cursor.execute("SELECT * FROM LightLevel ORDER BY id DESC LIMIT 8;")
   
   # fetch the remaining rows
   records = new_cursor.fetchall()
   response = {}
   for index, row in enumerate(records):
       response[index] = {
           "id": row[0],
           "time": row[1],
           "light": row[2]
       }
   new_cursor.close()
   return JSONResponse(response)

if __name__ == "__main__":
    p = Process(target=collect_data)
    p.start()
    uvicorn.run(app, host="0.0.0.0", port=6543)



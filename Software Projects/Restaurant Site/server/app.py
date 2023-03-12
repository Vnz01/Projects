from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   
import uvicorn
from fastapi.responses import RedirectResponse
import os
from urllib.request import urlopen
import json
import mysql.connector as mysql
from dotenv import load_dotenv

''' Environment Variables '''
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
''' Environment Variables '''

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("order.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/admin", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("admin.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/loadMenu", response_class=JSONResponse)
def reloadMenu() -> JSONResponse:
   # connect to the database
   db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
   # preparing a cursor object
   cursor = db.cursor()
   # query the database with the column names. .execute() executes the given query in the database.
   cursor.execute("select item_id, name, price from Menu_Items;")
   # fetch the remaining rows
   records = cursor.fetchall()
   # disconnecting from server
   db.close()

   response = {}
   for index, row in enumerate(records):
       response[index] = {
           "item_id": row[0],
           "name": str(row[1]),
           "price": str(row[2])
       }
   return JSONResponse(response)

@app.post("/editMenu")
def edit_menu(data: dict):
  itemID = data.get("id")
  newName = data.get("name")
  newCost = data.get("price")

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = 'UPDATE Menu_Items SET name = ' + '"'+newName+'",'+' price = '+newCost+ " WHERE item_id = " + itemID +";"
  cursor.execute(query)
  db.commit()
  print(cursor.rowcount, "Row Edited")
  return Response(status_code=200)

@app.post("/deleteMenu")
def delete_menu(data: dict):
  itemid = data.get("id")

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = 'DELETE FROM Menu_Items WHERE item_id = "' + itemid +'"'
  cursor.execute(query)
  db.commit()
  print(cursor.rowcount, "Row Deleted")
  return Response(status_code=200)

  
@app.post("/addMenu")
def add_menu(data: dict):
  name = data.get("name")
  cost = data.get("price")

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()

  query = 'INSERT INTO Menu_Items(name, price) VALUES (%s, %s)'

  values = (name,cost)
 
  # Executes multiple queries immediately. See description below for more info
  cursor.execute(query, values)

  # Make sure data is committed to the database
  db.commit()
  print(cursor.rowcount, " rows inserted.")
  return Response(status_code=200)

@app.get("/loadOrder", response_class=JSONResponse)
def reloadMenu() -> JSONResponse:
   # connect to the database
   db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
   # preparing a cursor object
   cursor = db.cursor()
   # query the database with the column names. .execute() executes the given query in the database.
   
   cursor.execute("select customer, name, quantity, status from Orders LEFT JOIN Menu_Items ON Orders.item_id=Menu_Items.item_id;")
   # fetch the remaining rows
   records = cursor.fetchall()
   db.close()

   response = {}
   for index, row in enumerate(records):
       response[index] = {
           "customer": row[0],
           "name": str(row[1]),
           "quantity": str(row[2]),
           "status": str(row[3])
       }
   return JSONResponse(response)

@app.post("/order")
def orderform(data: dict):
  item_id = data.get("item_id")
  customer = data.get("name")
  amtOrd = data.get("quantity")

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()

  query = 'INSERT INTO Orders(customer, quantity, item_id, status) VALUES (%s, %s, %s, %s)'

  values = (customer, amtOrd, item_id, 'Pending')
 
  # Executes multiple queries immediately. See description below for more info
  cursor.execute(query, values)

  # Make sure data is committed to the database
  db.commit()
  print(cursor.rowcount, " rows inserted.")
  return Response(status_code=200)

@app.get("/clear")
def clearorders():
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("drop table if exists Orders;")
  
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
  
  db.commit()
  print("Rows Deleted")
  return Response(status_code=200)

@app.post("/status")
def changestatus(data: dict):
  orderid = data.get("order_id")
  theStatus = data.get("status")

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()

  query = 'UPDATE Orders SET status = "'+theStatus+ '" WHERE order_id = ' + orderid +';'
 
  # Executes multiple queries immediately. See description below for more info
  cursor.execute(query)

  # Make sure data is committed to the database
  db.commit()
  print(cursor.rowcount, " rows changed.")
  return Response(status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543) 
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
import bcrypt
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel                    
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import dbutils as db  
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sessiondb import Sessions
from sessiondb import SessionStore
sessions = Sessions(db.db_config, secret_key=db.session_config['session_key'], expiry=600)
def authenticate_user(username:str, password:str) -> bool:
  return db.check_user_password(username, password)

''' Environment Variables '''
load_dotenv("credentials.env")

db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
''' Environment Variables '''

app = FastAPI()
views = Jinja2Templates(directory='views') 
static_files = StaticFiles(directory='public') 
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("views/home.html") as html:
        return HTMLResponse(content=html.read())

@app.get("/login", response_class=HTMLResponse)
def get_html(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  if session.get('logged_in'):
    session_id = request.cookies.get("session_id")
    template_data = {'request':request, 'session':session, 'session_id':session_id}
    return views.TemplateResponse('profile.html', template_data)
  else:
    with open("views/login.html") as html:
        return HTMLResponse(content=html.read())

@app.post('/login')
def post_login(data: dict, request:Request, response:Response) -> dict:
  username = data.get('username')
  password = data.get('password')
    # Invalidate previous session if logged in
  session = sessions.get_session(request)
  if len(session) > 0:
    sessions.end_session(request, response)

  # Authenticate the user

  if authenticate_user(username, password):
    session_data = {'username': username, 'logged_in': True}
    session_id = sessions.create_session(response, session_data)
    return {'message': 'Login successful', 'session_id': session_id}
  else:
    return {'message': 'Invalid username or password', 'session_id': 0}


@app.post('/logout')
def post_logout(request:Request, response:Response) -> dict:
  sessions.end_session(request, response)
  return {'message': 'Logout successful', 'session_id': 0}

@app.get('/profile', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  if session.get('logged_in'):
    session_id = request.cookies.get("session_id")
    template_data = {'request':request, 'session':session, 'session_id':session_id}
    return views.TemplateResponse('profile.html', template_data)
  else:
    return RedirectResponse(url="/login", status_code=302)
  
@app.get('/updatemvp', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  if session.get('logged_in'):
    session_id = request.cookies.get("session_id")
    template_data = {'request':request, 'session':session, 'session_id':session_id}
    return views.TemplateResponse('updatemvp.html', template_data)
  else:
    return RedirectResponse(url="/login", status_code=302)
  
@app.get('/leaderboard', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  if session.get('logged_in'):
    session_id = request.cookies.get("session_id")
    template_data = {'request':request, 'session':session, 'session_id':session_id}
    return views.TemplateResponse('leaderboard.html', template_data)
  else:
    return RedirectResponse(url="/login", status_code=302)
  
@app.post('/signup')
def create_user(data: dict) -> int:
  
  username = data.get("Username")
  email = data.get("Email")
  studentID = data.get("StudentID")
  password = data.get("Password")
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "insert into users (username, email, studentID, password) values (%s, %s, %s, %s)"
  values = (username, email, studentID, password)
  print(values)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

@app.post('/reset')
def create_user(data: dict) -> int:
  email = data.get("Email")
  studentID = data.get("StudentID")
  password = data.get("Password")
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  print(email)
  print(studentID)
  print(password)
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = 'UPDATE users SET password=%s WHERE email =%s and studentId =%s;' 
  values = (password, email, studentID)
  cursor.execute(query, values)
  print('UPDATED PASS')
  db.commit()
  db.close()
  return 1

@app.post('/check')
def create_user(data: dict):
  username = data.get("checkuser")
  email = data.get("checkemail")
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT id FROM users WHERE username = '" + username + "' or email = '" + email + "';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "id": str(row[0]),
      }
  if response:
    return(JSONResponse(response[0]['id']))
  return 0

@app.post('/checkReset')
def create_user(data: dict):
  email = data.get("checkE")
  studentID = data.get("checkID")
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT id FROM users WHERE studentId = '" + studentID + "' or email = '" + email + "';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "id": str(row[0]),
      }
  if response:
    return(response[0]['id'])
  
  return 0

@app.post('/getUserData')
def getDATA(data: dict):
  use = data.get('used')
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT username, email, studentId FROM users WHERE username = '"+use+"';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "username": str(row[0]),
          "email": str(row[1]),
          "studentid": str(row[2])
      }
  return JSONResponse(response)

@app.post('/whosLoggedIn')
def whosOn(data: dict):
  key = data.get('ssid')
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT SESSION_DATA FROM SESSIONS where SESSION_ID = '"+key+"';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "session_data": str(row[0])
      }
  print(response)
  return JSONResponse(response)

@app.post('/updateUsername')
def updateUsername(data: dict):
  current = data.get('currentName')
  use = data.get('userChangeTo')
  ssid = data.get('sessionIden')
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE users SET username = '"+use+"'  where username = '"+current+"';")
  db.commit()
  cursor.execute("UPDATE sessions SET session_data = '{" + '"username": "' + use + '", "logged_in": true' + "}'  where session_id = '"+ssid+"';") 
  db.commit()
  

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT username, email, studentId FROM users WHERE username = '"+use+"';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "username": str(row[0]),
          "email": str(row[1]),
          "studentid": str(row[2])

      }
  return JSONResponse(response)
  
@app.post('/updateEmail')
def updateEmail(data: dict):
  current = data.get('currentEmail')
  use = data.get('emailChangeTo')
  ssid = data.get('sessionIden')
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE users SET email = '"+use+"'  where email = '"+current+"';")
  db.commit()

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT username, email, studentId FROM users WHERE email = '"+use+"';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "username": str(row[0]),
          "email": str(row[1]),
          "studentid": str(row[2])

      }
  print(response)
  return JSONResponse(response)

@app.post('/updateSID')
def updateEmail(data: dict):
  current = data.get('sidChangeTo')
  email = data.get('currentE')
  user = data.get('currentU')
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  print(current)
  print(email)
  print(user)
  cursor.execute("UPDATE users SET studentId = '"+current+"'  where email = '"+email+"' and username = '"+user+"';")
  db.commit()

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT username, email, studentId FROM users WHERE email = '"+email+"';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "username": str(row[0]),
          "email": str(row[1]),
          "studentid": str(row[2])

      }
  print(response)
  return JSONResponse(response)
  
@app.post('/updatePass')
def updateEmail(data: dict):
  current = data.get('passChangeTo')
  email = data.get('currentE')
  user = data.get('currentU')
  current = bcrypt.hashpw(current.encode('utf-8'), bcrypt.gensalt())

  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "UPDATE users SET password = %s where email = %s and username = %s;"
  values = (current, email, user)
  cursor.execute(query, values)
  db.commit()
  return 1

@app.post('/checkUsername')
def create_user(data: dict):
  username = data.get("checkuser")
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT id FROM users WHERE username = '" + username + "';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "id": str(row[0]),
      }
  if response:
    return(JSONResponse(response[0]['id']))
  return 0

@app.post('/checkEmail')
def create_user(data: dict):
  email = data.get("checkemail")
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("SELECT id FROM users WHERE email = '" + email + "';")
  records = cursor.fetchall()
  db.close()
  response = {}
  for index, row in enumerate(records):
      response[index] = {
          "id": str(row[0]),
      }
  if response:
    print(response[0]['id'])
    return(response[0]['id'])
  print("0")
  return 0


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
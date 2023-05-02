from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi.responses import RedirectResponse
import os
from datetime import datetime
from multiprocessing import Process

from urllib.request import urlopen  
import json


import time
import LCD as LCD
import Light as light
import HumidTemp as humidTemp
# import RPi.GPIO as GPIO

app = FastAPI()

@app.get("/temp", response_class=JSONResponse)
def get_recent_temp() -> JSONResponse:
   print(humidTemp.getTemp())
   response = {"temp": humidTemp.getTemp()}
   return JSONResponse(response)

@app.get("/hum", response_class=JSONResponse)
def get_recent_light() -> JSONResponse:
   print(humidTemp.getHumid())
   response = {"humidity": humidTemp.getHumid()}
   return JSONResponse(response)

@app.get("/light", response_class=JSONResponse)
def get_recent_light() -> JSONResponse:
   light.setupLight()
   print(LCD.returnLight())
   response = {"light": LCD.returnLight()}
   return JSONResponse(response)

# @app.get("/LCD", response_class=JSONResponse)
# def get_recent_light() -> JSONResponse:
#    print("calling LCD main")
#    print(LCD.LCDmain())
#    response = {"light": LCD.returnLight()}
#    return JSONResponse(response)

if __name__ == "__main__":
   p = Process(target = LCD.startMain)
   p.start()
   uvicorn.run(app, host="0.0.0.0", port=6543)



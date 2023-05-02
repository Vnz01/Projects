#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
from Light import *
from HumidTemp import *
 
def loop():
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    while(True):         
        lcd.clear()
        strhold = str(getLight())
        strhold1 = str(getTemp())
        strhold2 = str(getHumid())
        lcd.setCursor(0,0)  # set cursor position
        lcd.message( 'Light: ' + strhold )   # display the time
        lcd.setCursor(0,1)
        lcd.message( 'Temp:' + strhold1 + ' H:' + strhold2 +'\n' )
        sleep(1)
        
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

def startMain():
    print ('Program is starting ... ')
    setupLight()
    try:
        while(True): 
            loop()
    except KeyboardInterrupt:
        destroy()
        destroyLight()
        GPIO.cleanup()
        exit()  

if __name__ == '__main__':
    print ('Program is starting ... ')
    setupLight()
    try:
        while(True): 
            loop()
    except KeyboardInterrupt:
        destroy()
        destroyLight()
        GPIO.cleanup()
        exit()  

def returnLight():
    setupLight()
    return getLight()
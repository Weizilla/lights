#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()
backlight = True
activate = True

def toggleBacklight():
    global backlight
    backlight = not backlight
    lcd.set_backlight(backlight)

while True:
    if lcd.is_pressed(LCD.SELECT):
        if activate == True:
            toggleBacklight() 
        activate = False
    else:
        activate = True

    time.sleep(0.1)  

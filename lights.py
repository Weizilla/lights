#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as io

backlight = True
powertail = False
activate = True
powerPin = 23

io.setmode(io.BCM)
io.setup(powerPin, io.OUT)
lcd = LCD.Adafruit_CharLCDPlate()
lcd.set_color(1.0, 0.0, 0.0)

def toggleBacklight():
    global backlight
    lcd.set_backlight(backlight)
    backlight = not backlight

def togglePowerTail():
    global powertail
    io.output(powerPin, powertail) 
    powertail = not powertail

while True:
    if lcd.is_pressed(LCD.SELECT):
        if activate == True:
            toggleBacklight() 
            togglePowerTail()
        activate = False
    else:
        activate = True

    time.sleep(0.1)  

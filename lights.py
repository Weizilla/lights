#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as io

buttons = (LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT)

class MessageDisplay(object):
    def __init__(self, lcd):
        self.lcd = lcd

    def message_1(self):
        def msg():
            self.lcd.clear()
            self.lcd.message("exec 1")
        return ("Message 1", msg)

    def message_2(self):
        def msg():
            self.lcd.clear()
            self.lcd.message("exec 2")
        return ("Message 2", msg)

    def message_3(self):
        def msg():
            self.lcd.clear()
            self.lcd.message("exec 3")
        return ("Message 3", msg)

class Menu(object):
    def __init__(self, lcd):
        self.current = 0
        self.menus = []
        self.lcd = lcd

        self.backlight = True
        self.powertail = False
        self.powertail_pin = 23
        io.setmode(io.BCM)
        io.setup(self.powertail_pin, io.OUT)

    def toggle_backlight(self):
        self.lcd.set_backlight(self.backlight)
        self.backlight = not self.backlight

    def togglePowerTail():
        io.output(self.powertail_pin, self.powertail) 
        self.powertail = not self.powertail

    def add_item(self, item):
        self.menus.append(item)

    def button_pressed(self, button):
        if button == LCD.SELECT:
            self.toggle_backlight()
        elif button == LCD.UP:
            self.current += 1
            if self.current == len(self.menus):
                self.current = 0
            self.update_menu()
        elif button == LCD.DOWN:
            self.current -= 1 
            if self.current == -1:
                self.current = len(self.menus) - 1
            self.update_menu()
        elif button == LCD.RIGHT:
            self.exec_menu()
        elif button == LCD.LEFT:
            self.update_menu()

    def update_menu(self):
        item = self.menus[self.current]
        lcd.clear()
        lcd.message(item[0])

    def exec_menu(self):
        item = self.menus[self.current]
        item[1]()

    def is_pressed(self):
        for button in buttons:
            if self.lcd.is_pressed(button):
                return button

    def start(self):
        self.update_menu()
        activate = True
        while True:
            button = self.is_pressed()
            if button is not None:
                if activate:
                    self.button_pressed(button)
                activate = False
            else:
                activate = True

            time.sleep(0.1)  

if __name__ == "__main__":
    lcd = LCD.Adafruit_CharLCDPlate()
    msg = MessageDisplay(lcd)

    menu = Menu(lcd)
    menu.add_item(msg.message_1())
    menu.add_item(msg.message_2())
    menu.add_item(msg.message_3())

    menu.start()

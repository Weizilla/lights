#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as io
import schedule

buttons = (LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT)

class Lights(object):
    def __init__(self):
        self.on_time = "5:45"
        schedule.every().day.at(self.on_time).do(self.light_on)

        self.off_time = "6:30"
        schedule.every().day.at(self.off_time).do(self.light_off)

        self.powertail_pin = 23
        io.setmode(io.BCM)
        io.setup(self.powertail_pin, io.OUT)

    def light_on(self):
        io.output(self.powertail_pin, True) 

    def light_off(self):
        io.output(self.powertail_pin, False)

    def light_on_menu(self):
        return ("On Time {}".format(self.on_time), self.light_on)

    def light_off_menu(self):
        return ("Off Time {}".format(self.off_time), self.light_off)

    def run_pending(self):
        schedule.run_pending()

class Menu(object):
    def __init__(self, lcd):
        self.current = 0
        self.menus = []
        self.updates = []
        self.lcd = lcd

        self.backlight = True

    def toggle_backlight(self):
        self.lcd.set_backlight(self.backlight)
        self.backlight = not self.backlight

    def add_update_listener(self, item):
        self.updates.append(item) 

    def add_menu_item(self, item):
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

    def exec_updates(self):
        for update in self.updates:
            update()

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

            self.exec_updates()

            try:
                time.sleep(0.1)  
            except KeyboardInterrupt:
                print("Goodbye")
                exit(0)

if __name__ == "__main__":
    lcd = LCD.Adafruit_CharLCDPlate()
    lights = Lights()

    menu = Menu(lcd)
    menu.add_menu_item(lights.light_on_menu())
    menu.add_menu_item(lights.light_off_menu())
    menu.add_update_listener(lights.run_pending)

    menu.start()

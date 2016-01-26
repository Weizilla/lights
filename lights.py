#!/usr/bin/python

import time
import RPi.GPIO as io
import schedule

io.setmode(io.BCM)
BIG_BUTTON = 22

class Lights(object):
    def __init__(self):
        self.light = True
        #self.on_time = "5:45"
        #schedule.every().day.at(self.on_time).do(self.light_on)

        #self.off_time = "6:30"
        #schedule.every().day.at(self.off_time).do(self.light_off)
        self.powertail_pin = 23
        io.setup(self.powertail_pin, io.OUT)

    def light_on(self):
        self.light = True
        self.update_powertail()

    def light_off(self):
        self.light = False
        self.update_powertail()

    def toggle_light(self):
        self.light = not self.light
        self.update_powertail()

    def update_powertail(self):
        io.output(self.powertail_pin, self.light) 

    def run_pending(self):
        schedule.run_pending()

class Menu(object):
    def __init__(self):
        self.updates = []
        io.setup(BIG_BUTTON, io.IN, pull_up_down=io.PUD_UP)

    def add_update_listener(self, item):
        self.updates.append(item) 

    def add_big_button(self, item):
        self.big_button = item

    def button_pressed(self, button):
        if button == BIG_BUTTON and self.big_button:
            self.big_button()

    def exec_updates(self):
        for update in self.updates:
            update()

    def is_big_pressed(self):
        if io.input(BIG_BUTTON):
            return BIG_BUTTON

    def start(self):
        big_activate = True
        while True:
            button = self.is_big_pressed()
            if button is not None:
                if big_activate:
                    self.button_pressed(button)
                big_activate = False
            else:
                big_activate = True

            self.exec_updates()

            try:
                time.sleep(0.1)  
            except KeyboardInterrupt:
                print("Goodbye")
                io.cleanup()
                exit(0)

if __name__ == "__main__":
    lights = Lights()

    menu = Menu()
    menu.add_big_button(lights.toggle_light)
    menu.add_update_listener(lights.run_pending)

    menu.start()


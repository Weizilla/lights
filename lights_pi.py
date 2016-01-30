#!/usr/bin/python

import time
import RPi.GPIO as io
import schedule

io.setmode(io.BCM)
BIG_BUTTON = 22
POWERTAIL = 23


class Lights():
    def __init__(self):
        self.light = True
        io.setup(BIG_BUTTON, io.IN, pull_up_down=io.PUD_UP)
        io.setup(POWERTAIL, io.OUT)

    def set_light(self, light):
        self.light = light
        self.update_powertail()

    def toggle_light(self):
        self.light = not self.light
        self.update_powertail()

    def update_powertail(self):
        io.output(POWERTAIL, self.light)

    def run_pending(self):
        schedule.run_pending()

    def is_big_pressed(self):
        if io.input(BIG_BUTTON):
            return BIG_BUTTON

    def start(self):
        big_activate = True
        while True:
            button = self.is_big_pressed()
            if button is not None:
                if big_activate:
                    self.toggle_light()
                big_activate = False
            else:
                big_activate = True

            self.run_pending()

            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("Goodbye")
                io.cleanup()
                exit(0)

if __name__ == "__main__":
    lights = Lights()
    lights.start()

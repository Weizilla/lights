#!/usr/bin/python

import time
import importlib
rpi_spec = importlib.util.find_spec("RPi")
if rpi_spec is not None:
    import RPi.GPIO as io
else:
    io = None
from lights import Lights

BIG_BUTTON = 22
POWERTAIL = 23


class LightsPi(Lights):
    def __init__(self):
        super().__init__()
        if io:
            io.setmode(io.BCM)
            io.setup(BIG_BUTTON, io.IN, pull_up_down=io.PUD_UP)
            io.setup(POWERTAIL, io.OUT)

    def update_state(self):
        io.output(POWERTAIL, self.get_light())

    def run_pending(self):
        # schedule.run_pending()
        pass

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
    lights = LightsPi()
    lights.start()

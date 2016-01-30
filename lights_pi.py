#!/usr/bin/python

import time
import importlib
rpi_spec = importlib.find_loader("RPi")
#rpi_spec = importlib.util.find_spec("RPi")
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
        self.bounce_start = None
        if io:
            io.setmode(io.BCM)
            io.setup(BIG_BUTTON, io.IN, pull_up_down=io.PUD_UP)
            io.setup(POWERTAIL, io.OUT, initial=0)
            io.add_event_detect(BIG_BUTTON, io.BOTH, callback=self.btn_cb, bouncetime=500)

    def update_state(self):
        if self.bounce_start is None or (time.time() - self.bounce_start > 1):
            io.output(POWERTAIL, self.get_light())
            self.bounce_start = time.time()
            return True
        return False

    def btn_cb(self, channel):
        self.toggle_light()

    def start(self):
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop()

    def stop(self):
        print("Goodbye")
        io.cleanup()
        exit(0)

if __name__ == "__main__":
    lights = LightsPi()
    lights.start()
    lights.stop()

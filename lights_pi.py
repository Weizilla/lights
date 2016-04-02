#!/usr/bin/python

import time
import importlib
from lights import Lights
rpi_spec = importlib.find_loader("RPi")
#rpi_spec = importlib.util.find_spec("RPi")
if rpi_spec is not None:
    import RPi.GPIO as io
else:
    io = None

BIG_BUTTON = 22
POWERTAIL = 23


class LightsPi(Lights):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if io:
            io.setmode(io.BCM)
            io.setup(BIG_BUTTON, io.IN, pull_up_down=io.PUD_UP)
            io.setup(POWERTAIL, io.OUT, initial=0)
            io.add_event_detect(BIG_BUTTON, io.BOTH, callback=self.btn_cb, bouncetime=1000)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _set_state(self, value):
        if io:
            io.output(POWERTAIL, value)

    def btn_cb(self, channel):
        self.log("Button toggled")
        self.toggle("button")

    def start(self):
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop()
                exit(1)

    def stop(self):
        if io:
            io.cleanup()


if __name__ == "__main__":
    with LightsPi() as lights:
        lights.start()

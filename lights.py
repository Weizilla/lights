import time


class Lights:
    def __init__(self):
        self.light = True
        self._times = {}

    def toggle_light(self):
        print("toggling light to {}".format(self.light))
        self.light = not self.light
        self.update_state()

    def set_light(self, light):
        print("setting light to {}".format(light))
        self.light = light
        self.update_state()

    def get_light(self):
        return self.light

    def update_state(self):
        print("updating status with light {}".format(self.light))
        pass

    def set_time(self, mode, light):
        print("setting time for mode {}: {}".format(mode, light))
        self._times[mode] = light

    def get_times(self):
        return self._times

    def get_time(self, mode):
        light = self._times.get(mode)
        print("getting time for mode {} : {}".format(mode, light))
        return light

    def start(self):
        print("starting ...")
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("Goodbye")
                exit(0)

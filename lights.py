import time


class Lights:
    def __init__(self):
        self._light = False
        self._times = {}
        self._debounce = None

    def toggle_light(self):
        self.set_light(not self.get_light())
        return self.get_light();

    def set_light(self, light):
        if self._update_state(light):
            self._light = light
        return self.get_light()

    def get_light(self):
        return self._light

    def _update_state(self, new_state):
        if self._debounce is None or (time.time() - self._debounce > 1):
            self.set_state(new_state)
            self._debounce = time.time()
            return True
        return False

    def set_state(self, new_state):
        # to be overwritten by hardware
        print("setting state to {}".format(new_state))
        pass

    def set_time(self, mode, trigger_time):
        print("setting time for mode {}: {}".format(mode, trigger_time))
        self._times[mode] = time.strptime(trigger_time, "%H:%M")

    def get_times(self):
        return {k : time.strftime("%H:%M", v) for (k, v) in self._times.items()}

    def get_time(self, mode):
        light = self._times.get(mode)
        print("getting time for mode {} : {}".format(mode, light))
        return light

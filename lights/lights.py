import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class Lights:
    def __init__(self, state_callback=None):
        self._state = False
        self._debounce = None
        self._state_callback = state_callback
        # self._times = {}
        # self._jobs = {}
        # self._scheduler = BackgroundScheduler()
        # self._scheduler.start()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._debounce is None or (time.time() - self._debounce > 1):
            if self._state_callback:
                self._state_callback(value)
            self._state = value
            self._debounce = time.time()

    def toggle(self):
        self.state = not self.state

    # def set_time(self, mode, trigger_time):
    #     print("setting time for mode {}: {}".format(mode, trigger_time))
    #
    #     light_map = {"on": True, "off": False}
    #     if mode not in light_map:
    #         print("Unexpected mode:", mode)
    #         return
    #
    #     self._times[mode] = trigger_time
    #     next_time = self._calc_next_time(trigger_time)
    #     light = light_map[mode]
    #     job = self._scheduler.add_job(self.set_light, args=[light], next_run_time=next_time)
    #     self._replace_prev_job(mode, job.id)
    #     print("started job {} for mode {} to run at {}".format(job.id, mode, next_time))
    #
    # def _calc_next_time(self, time):
    #     h, m = [int(t) for t in time.split(":")]
    #     now = datetime.now()
    #     next_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
    #     if next_time < now:
    #         next_time += timedelta(days=1)
    #     return next_time
    #
    # def _replace_prev_job(self, mode, new_id):
    #     if mode in self._jobs:
    #         old_id = self._jobs[mode]
    #         self._scheduler.remove_job(old_id)
    #     self._jobs[mode] = new_id
    #
    # def get_times(self):
    #     return self._times

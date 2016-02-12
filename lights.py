import time
from collections import namedtuple
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class Lights:
    def __init__(self, state_callback=None, scheduler=None):
        self._state = False
        self._debounce = None
        self._state_callback = state_callback
        self._scheduler = scheduler or BackgroundScheduler()
        self._scheduler.start()
        self._triggers = {}

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._debounce is None or (time.time() - self._debounce > 1):
            if self._state_callback:
                self._state_callback(value)
            else:
                print("State:", value)
            self._state = value
            self._debounce = time.time()

    def toggle(self):
        self.state = not self.state

    def _set_state(self, state):
        self.state = state

    def add_trigger(self, state, hour, minute, repeat_weekday=False, repeat_weekend=False):
        tomorrow_now = datetime.now() + timedelta(days=1)
        job = self._scheduler.add_job(self._set_state, args=[state], trigger="cron", hour=hour,
                                      minute=minute, end_date=tomorrow_now)
        trigger = Trigger(job_id=job.id, state=state, hour=hour, minute=minute,
                          next_run_time=job.next_run_time,
                          repeat_weekday=repeat_weekday,
                          repeat_weekend=repeat_weekend)
        self._triggers[job.id] = trigger

    @property
    def triggers(self):
        active_triggers = {}
        for job in self._scheduler.get_jobs():
            job_id = job.id
            active_triggers[job_id] = self._triggers[job_id]
        self._triggers = active_triggers
        return list(self._triggers.values())

    def stop(self):
        pass


class Trigger(namedtuple("Trigger", "job_id state hour minute next_run_time repeat_weekday repeat_weekend")):
    pass

import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class Lights:
    weekdays = "mon,tue,wed,thu,fri"
    weekends = "sat,sun"
    all_week = weekdays + "," + weekends

    def __init__(self, state_callback=None, scheduler=None):
        self._state = False
        self._debounce = None
        self._state_callback = state_callback
        self._scheduler = scheduler or BackgroundScheduler()
        self._scheduler.start()
        self._triggers = {}
        self.logger = None

    def log(self, message):
        if self.logger:
            self.logger.info(message)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._debounce is None or (time.time() - self._debounce > 1):
            if self._state_callback:
                self._state_callback(value)
            self.log("Setting state: {}".format(value))
            self._state = value
            self._debounce = time.time()

    def toggle(self):
        self.state = not self.state

    def _set_state(self, state):
        self.log("Trigger setting state: {}".format(state))
        self.state = state

    def add_trigger(self, state, hour, minute, repeat_weekday=False, repeat_weekend=False):
        end_date = self._calc_end_date(repeat_weekday, repeat_weekend)
        day_of_week = self._calc_day_of_week(repeat_weekday, repeat_weekend)

        job = self._scheduler.add_job(func=self._set_state, args=[state], trigger="cron", hour=hour,
                                      minute=minute, end_date=end_date, day_of_week=day_of_week)

        trigger = Trigger(job_id=job.id, state=state, hour=hour, minute=minute,
                          next_run_time=int(job.next_run_time.timestamp()),
                          repeat_weekday=repeat_weekday,
                          repeat_weekend=repeat_weekend)

        self._triggers[job.id] = trigger

    @staticmethod
    def _calc_end_date(repeat_weekday, repeat_weekend):
        tomorrow = datetime.now() + timedelta(days=1)
        return None if repeat_weekday or repeat_weekend else tomorrow

    @staticmethod
    def _calc_day_of_week(repeat_weekday, repeat_weekend):
        if repeat_weekday and repeat_weekend:
            return Lights.all_week
        elif repeat_weekday:
            return Lights.weekdays
        elif repeat_weekend:
            return Lights.weekends
        else:
            return None

    def remove_trigger(self, job_id):
        del self._triggers[job_id]
        self._scheduler.remove_job(job_id)

    @property
    def triggers(self):
        active_triggers = {}
        for job in self._scheduler.get_jobs():
            job_id = job.id
            trigger = self._triggers[job_id]
            trigger.next_run_time = int(job.next_run_time.timestamp())
            active_triggers[job_id] = trigger
        self._triggers = active_triggers
        return list(self._triggers.values())

    def stop(self):
        pass


class Trigger():
    def __init__(self, job_id, state, hour, minute, next_run_time, repeat_weekday, repeat_weekend):
        self.job_id = job_id
        self.state = state
        self.hour = hour
        self.minute = minute
        self.next_run_time = next_run_time
        self.repeat_weekday = repeat_weekday
        self.repeat_weekend= repeat_weekend

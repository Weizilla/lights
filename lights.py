import time
from datetime import datetime, timedelta
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc


class Lights:
    weekdays = "mon,tue,wed,thu,fri"
    weekends = "sat,sun"
    all_week = weekdays + "," + weekends

    def __init__(self, scheduler=None, store=None):
        self._state = False
        self._debounce = None
        self._scheduler = scheduler or BackgroundScheduler()
        self._scheduler.start()
        self._triggers = {}
        self._store = store
        self.logger = None
        if self._store:
            self._load_triggers()

    def _load_triggers(self):
        triggers = self._store.read_triggers()
        [self._add_trigger(**t.__dict__) for t in triggers]
        self.log("Loaded {} triggers".format(len(self._triggers)))

    def log(self, message):
        if self.logger:
            self.logger.info(message)

    def get_state(self):
        return self._state

    def set_state(self, value, source):
        if self._debounce is None or (time.time() - self._debounce > 1):
            self.log("Setting state {} from {}".format(value, source))
            self._state = value
            self._debounce = time.time()
            self._set_state(value)
            if self._store:
                self._store.add_entry(value, source)

    """For sub classes to overwrite on setting state after debounce"""

    def _set_state(self, value):
        pass

    def toggle(self, source):
        self.set_state(not self.get_state(), source)

    def add_trigger(self, state, hour, minute, repeat_weekday=False, repeat_weekend=False,
                    **kwargs):
        trigger = self._add_trigger(state, hour, minute, repeat_weekday, repeat_weekend)

        if self._store:
            self._store.add_trigger(trigger)

    def _add_trigger(self, state, hour, minute, repeat_weekday, repeat_weekend, job_id=None,
                     **kwargs):
        end_date = self._calc_end_date(repeat_weekday, repeat_weekend)
        day_of_week = self._calc_day_of_week(repeat_weekday, repeat_weekend)
        job = self._scheduler.add_job(func=self.set_state, args=[state, "trigger"], trigger="cron",
                                      id=job_id, hour=hour, minute=minute, end_date=end_date,
                                      day_of_week=day_of_week)
        trigger = Trigger(job_id=job.id, state=state, hour=hour, minute=minute,
                          next_run_time=int(job.next_run_time.timestamp()),
                          repeat_weekday=repeat_weekday,
                          repeat_weekend=repeat_weekend)
        self._triggers[job.id] = trigger
        return trigger

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
        if job_id in self._triggers:
            del self._triggers[job_id]
        try:
            self._scheduler.remove_job(job_id)
        except JobLookupError:
            self.log("Job not found {}".format(job_id))
        if self._store:
            self._store.remove_trigger(job_id)

    def get_triggers(self):
        active_triggers = {}
        for job in self._scheduler.get_jobs():
            job_id = job.id
            trigger = self._triggers[job_id]
            trigger.next_run_time = int(job.next_run_time.timestamp())
            active_triggers[job_id] = trigger
        self._triggers = active_triggers
        return sorted(self._triggers.values(), key=lambda t: t.next_run_time)

    def get_history(self):
        return self._store.read_history() if self._store else []

    def stop(self):
        return True


class Trigger:
    def __init__(self, job_id, state, hour, minute, repeat_weekday, repeat_weekend, next_run_time=None):
        self.job_id = job_id
        self.state = state
        self.hour = hour
        self.minute = minute
        self.next_run_time = next_run_time
        self.repeat_weekday = repeat_weekday
        self.repeat_weekend = repeat_weekend


class Entry:
    def __init__(self, timestamp, state, source):
        self.timestamp = timestamp
        self.state = state
        self.source = source
        self.datetime = datetime.fromtimestamp(timestamp, utc)

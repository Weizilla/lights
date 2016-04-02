import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os


class Lights:
    weekdays = "mon,tue,wed,thu,fri"
    weekends = "sat,sun"
    all_week = weekdays + "," + weekends

    def __init__(self, scheduler=None, file_store=None):
        self._state = False
        self._debounce = None
        self._scheduler = scheduler or BackgroundScheduler()
        self._scheduler.start()
        self._triggers = {}
        self._file_store = file_store
        self.logger = None
        self._load_triggers()

    def _load_triggers(self):
        if self._file_store and os.path.exists(self._file_store):
            with open(self._file_store) as file_store:
                contents = file_store.read()
                if contents:
                    triggers = json.loads(contents)
                    for trigger in triggers:
                        self.add_trigger(**trigger)


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

    def toggle(self, source):
        self.set_state(not self.get_state(), source)

    def _set_state(self, state):
        self.log("Trigger setting state: {}".format(state))
        self.state = state

    def add_trigger(self, state, hour, minute, repeat_weekday=False, repeat_weekend=False, **kwargs):
        end_date = self._calc_end_date(repeat_weekday, repeat_weekend)
        day_of_week = self._calc_day_of_week(repeat_weekday, repeat_weekend)

        job = self._scheduler.add_job(func=self._set_state, args=[state], trigger="cron", hour=hour,
                                      minute=minute, end_date=end_date, day_of_week=day_of_week)

        trigger = Trigger(job_id=job.id, state=state, hour=hour, minute=minute,
                          next_run_time=int(job.next_run_time.timestamp()),
                          repeat_weekday=repeat_weekday,
                          repeat_weekend=repeat_weekend)

        self._triggers[job.id] = trigger
        self._save_triggers()

    def _save_triggers(self):
        if self._file_store:
            with open(self._file_store, "w") as data_file:
                triggers_json = json.dumps([t.__dict__ for t in self._triggers.values()])
                data_file.write(triggers_json)

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
        self._save_triggers()

    def get_triggers(self):
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
        self.repeat_weekend = repeat_weekend

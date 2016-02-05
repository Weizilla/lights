from hamcrest import *
from unittest import TestCase
from unittest.mock import Mock
from lights.lights import Lights


class TestLightsScheduler(TestCase):

    def setUp(self):
        self.lights = Lights()

    def test_starts_scheduler(self):
        mock = Mock()

        Lights(scheduler=mock)
        mock.start.assert_called_with()

    def test_add_trigger_and_get_job(self):
        state = True
        hour = 10
        minute = 20
        self.lights.add_trigger(state, hour, minute)

        jobs = self.lights._scheduler.get_jobs()
        assert_that(len(jobs), is_(1))

    def test_add_triggers_and_get_jobs(self):
        num = 5
        for i in range(num):
            self.lights.add_trigger(True, 10, 20)

        jobs = self.lights._scheduler.get_jobs()
        assert_that(len(jobs), is_(num))

        triggers = self.lights.triggers
        assert_that(len(triggers), is_(num))

    def test_add_and_get_trigger(self):
        state = True
        hour = 10
        minute = 20
        self.lights.add_trigger(state, hour, minute)

        job_id = self.lights._scheduler.get_jobs()[0].id
        triggers = self.lights.triggers
        assert_that(len(triggers), is_(1))

        trigger = triggers[0]
        assert_that(trigger.job_id, is_(job_id))
        assert_that(trigger.state, is_(state))
        assert_that(trigger.hour, is_(hour))
        assert_that(trigger.minute, is_(minute))
        assert_that(trigger.next_run_time, is_(not_none()))
        assert_that(trigger.repeat_weekday, is_(False))
        assert_that(trigger.repeat_weekend, is_(False))

    def test_add_no_repeat_has_end_date(self):
        self.lights.add_trigger(True, 10, 20)

        job = self.lights._scheduler.get_jobs()[0]
        assert_that(job.trigger.end_date, is_(not_none()))

    def test_remove_finished_jobs_from_trigger(self):
        self.lights.add_trigger(True, 10, 20)
        self.lights.add_trigger(True, 10, 20)

        jobs = self.lights._scheduler.get_jobs()
        removed_job_id = jobs[0].id
        keep_job_id = jobs[1].id

        self.lights._scheduler.remove_job(removed_job_id)
        jobs = self.lights._scheduler.get_jobs()
        assert_that(len(jobs), is_(1))

        triggers = self.lights.triggers
        assert_that(len(triggers), is_(1))

        trigger = triggers[0]
        assert_that(trigger.job_id, is_(keep_job_id))

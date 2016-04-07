from unittest import TestCase
from hamcrest import assert_that, is_
from unittest.mock import MagicMock
import lights_flask as lights_flask
from lights import Lights, Trigger, Entry
import json
from freezegun import freeze_time
from datetime import datetime
from pytz import utc

NOW = datetime(2016, 4, 7, 12, 23, 57, 0, utc)
TIMESTAMP = 1460031837


class FlaskTest(TestCase):
    def setUp(self):
        self.lights_flask = lights_flask
        self.lights = Lights()
        lights_flask.lights = self.lights

    def test_toggle(self):
        self.lights.toggle = MagicMock()
        self.lights_flask.toggle()
        self.lights.toggle.assert_called_with("web")

    def test_toggle_gets_state(self):
        self.lights.get_state = MagicMock(return_value=True)
        result = json.loads(self.lights_flask.toggle())
        assert_that(result["state"], is_(True))

    def test_stop(self):
        self.lights.stop = MagicMock()
        self.lights_flask.stop()
        self.lights.stop.assert_called_with()

    def test_get_state(self):
        self.lights.get_state = MagicMock(return_value=True)
        self.lights_flask.request = FakeRequest("GET")
        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(True))

    def test_set_state_false(self):
        self.lights_flask.request = FakeRequest("PUT", {"state": False})
        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(False))

    def test_set_state_true(self):
        self.lights_flask.request = FakeRequest("PUT", {"state": True})
        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(True))

    def test_get_trigger(self):
        trigger = Trigger(hour=10, minute=20, job_id=10, state=True, next_run_time=None,
                          repeat_weekend=False, repeat_weekday=False)
        self.lights.get_triggers = MagicMock(return_value=[trigger])

        self.lights_flask.request = FakeRequest("GET")
        results = json.loads(self.lights_flask.triggers())
        assert_that(len(results), is_(1))

        actual = results[0]
        assert_that(actual["job_id"], is_(trigger.job_id))
        assert_that(actual["state"], is_(trigger.state))
        assert_that(actual["hour"], is_(trigger.hour))
        assert_that(actual["minute"], is_(trigger.minute))
        assert_that(actual["next_run_time"], is_(trigger.next_run_time))
        assert_that(actual["repeat_weekday"], is_(trigger.repeat_weekday))
        assert_that(actual["repeat_weekend"], is_(trigger.repeat_weekend))

    def test_set_trigger(self):
        self.lights.add_trigger = MagicMock()

        state = True
        hour = 10
        minute = 20
        repeat_weekends = True
        repeat_weekdays = True
        input_trigger = { "state": state,
                          "hour": hour,
                          "minute": minute,
                          "repeat_weekdays": repeat_weekdays,
                          "repeat_weekends": repeat_weekends}
        self.lights_flask.request = FakeRequest("PUT", input_trigger)

        self.lights_flask.triggers()

        self.lights.add_trigger.assert_called_with(state=state,
                hour=hour, minute=minute, repeat_weekends=repeat_weekends,
                repeat_weekdays=repeat_weekdays)

    def test_remove_trigger(self):
        self.lights.remove_trigger = MagicMock()

        job_id = 10
        self.lights_flask.remove_trigger(job_id)

        self.lights.remove_trigger.assert_called_with(job_id)

    @freeze_time(NOW)
    def test_get_history(self):
        source = "TEST"
        entry = Entry(TIMESTAMP, source)
        self.lights.get_history = MagicMock(return_value=[entry])
        self.lights_flask.request = FakeRequest("GET")

        results = json.loads(self.lights_flask.history())
        assert_that(len(results), is_(1))

        actual = results[0]
        assert_that(actual["timestamp"], is_(TIMESTAMP))
        assert_that(actual["source"], is_(source))


class FakeRequest:
    def __init__(self, method, json=None):
        self.method = method
        self._json = json

    def get_json(self):
        return self._json

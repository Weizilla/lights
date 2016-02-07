from unittest import TestCase
from hamcrest import *
from unittest.mock import Mock
import lights.lights_flask as lights_flask
from lights.lights import Trigger
import json


class FlaskTest(TestCase):
    def setUp(self):
        self.lights_flask = lights_flask
        self.lights = Mock()
        self.lights.state = True
        self.lights.triggers = []
        lights_flask.lights = self.lights

    def test_toggle(self):
        self.lights_flask.toggle()
        self.lights.toggle.assert_called_with()

    def test_toggle_gets_state(self):
        result = json.loads(self.lights_flask.toggle())
        assert_that(result["state"], is_(True))

    def test_stop(self):
        self.lights_flask.stop()
        self.lights.stop.assert_called_with()

    def test_get_state(self):
        self.lights_flask.request = FakeRequest("GET")
        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(True))

    def test_set_state(self):
        input_state = {"state": False}
        self.lights_flask.request = FakeRequest("PUT", input_state)

        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(False))

    def test_get_trigger(self):
        trigger = Trigger(hour=10, minute=20, job_id=10, state=True, next_run_time=None,
                          repeat_weekend=False, repeat_weekday=False)
        self.lights_flask.lights.triggers = [trigger]

        self.lights_flask.request = FakeRequest("GET")
        results = json.loads(self.lights_flask.triggers())
        assert_that(len(results), is_(1))

        trigger = results[0]
        assert_that(trigger, is_(trigger))

    def test_set_trigger(self):
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

        self.lights_flask.lights.add_trigger.assert_called_with(state=state,
                hour=hour, minute=minute, repeat_weekends=repeat_weekends,
                repeat_weekdays=repeat_weekdays)

class FakeRequest:
    def __init__(self, method, json=None):
        self.method = method
        self._json = json

    def get_json(self):
        return self._json

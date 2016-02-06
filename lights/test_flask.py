from unittest import TestCase
from hamcrest import *
from unittest.mock import Mock
import lights.lights_flask as lights_flask
import json


class FlaskTest(TestCase):
    def setUp(self):
        self.lights_flask = lights_flask
        self.mock = Mock()
        self.mock.state = True
        lights_flask.lights = self.mock

    def test_toggle(self):
        self.lights_flask.toggle()
        self.mock.toggle.assert_called_with()

    def test_toggle_gets_state(self):
        result = json.loads(self.lights_flask.toggle())
        assert_that(result["state"], is_(True))

    def test_stop(self):
        self.lights_flask.stop()
        self.mock.stop.assert_called_with()

    def test_get_state(self):
        self.lights_flask.request = FakeRequest("GET")
        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(True))

    def test_set_state(self):
        input_state = {"state": False}
        self.lights_flask.request = FakeRequest("PUT", input_state)

        result = json.loads(self.lights_flask.state())
        assert_that(result["state"], is_(False))


class FakeRequest:
    def __init__(self, method, json=None):
        self.method = method
        self._json = json

    def get_json(self):
        return self._json

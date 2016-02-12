from hamcrest import *
from lights import Lights
from freezegun import freeze_time
from datetime import datetime, timedelta
from unittest.mock import Mock
from unittest import TestCase


class LightsStateTest(TestCase):
    def setUp(self):
        self.lights = Lights()

    def test_state_starts_as_false(self):
        assert_that(self.lights.state, is_(False))

    def test_set_and_return_state(self):
        self.lights.state = True
        assert_that(self.lights.state, is_(True))

    def test_toggle_flips_state(self):
        assert_that(self.lights.state, is_(False))

        self.lights.toggle()
        assert_that(self.lights.state, is_(True))

    def test_set_state_does_not_change_if_less_than_bounce_duration(self):
        self.lights.state = True
        assert_that(self.lights.state, is_(True))

        self.lights.state = False
        assert_that(self.lights.state, is_(True))

    def test_set_state_changes_if_more_than_bounce_duration(self):
        with freeze_time(datetime.now()) as curr_time:
            self.lights.state = True
            assert_that(self.lights.state, is_(True))

            curr_time.tick(delta=timedelta(seconds=90))

            self.lights.state = False
            assert_that(self.lights.state, is_(False))

    def test_toggle_does_not_change_if_less_than_bounce_duration(self):
        self.lights.toggle()
        assert_that(self.lights.state, is_(True))

        self.lights.toggle()
        assert_that(self.lights.state, is_(True))

    def test_toggle_changes_if_more_than_bounce_duration(self):
        with freeze_time(datetime.now()) as curr_time:
            self.lights.toggle()
            assert_that(self.lights.state, is_(True))

            curr_time.tick(delta=timedelta(seconds=90))

            self.lights.toggle()
            assert_that(self.lights.state, is_(False))

    def test_set_state_calls_callback(self):
        mock = Mock()
        lights = Lights(mock.state)

        lights.state = True
        mock.state.assert_called_with(True)

    def test_toggle_calls_callback(self):
        mock = Mock()
        lights = Lights(mock.state)

        lights.toggle()
        mock.state.assert_called_with(True)

from hamcrest import *
from lights import Lights
from freezegun import freeze_time
from datetime import datetime, timedelta
from unittest import TestCase


class LightsStateTest(TestCase):
    def setUp(self):
        self.lights = Lights()

    def test_state_starts_as_false(self):
        assert_that(self.lights.get_state(), is_(False))

    def test_set_and_return_state(self):
        self.lights.set_state(True, "test")
        assert_that(self.lights.get_state(), is_(True))

    def test_toggle_flips_state(self):
        assert_that(self.lights.get_state(), is_(False))

        self.lights.toggle("test")
        assert_that(self.lights.get_state(), is_(True))

    def test_set_state_does_not_change_if_less_than_bounce_duration(self):
        self.lights.set_state(True, "test")
        assert_that(self.lights.get_state(), is_(True))

        self.lights.set_state(False, "test")
        assert_that(self.lights.get_state(), is_(True))

    def test_set_state_changes_if_more_than_bounce_duration(self):
        with freeze_time(datetime.now()) as curr_time:
            self.lights.set_state(True, "test")
            assert_that(self.lights.get_state(), is_(True))

            curr_time.tick(delta=timedelta(seconds=90))

            self.lights.set_state(False, "test")
            assert_that(self.lights.get_state(), is_(False))

    def test_toggle_does_not_change_if_less_than_bounce_duration(self):
        self.lights.toggle("test")
        assert_that(self.lights.get_state(), is_(True))

        self.lights.toggle("test")
        assert_that(self.lights.get_state(), is_(True))

    def test_toggle_changes_if_more_than_bounce_duration(self):
        with freeze_time(datetime.now()) as curr_time:
            self.lights.toggle("test")
            assert_that(self.lights.get_state(), is_(True))

            curr_time.tick(delta=timedelta(seconds=90))

            self.lights.toggle("test")
            assert_that(self.lights.get_state(), is_(False))

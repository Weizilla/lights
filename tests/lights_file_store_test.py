from hamcrest import *
from lights import Lights
from unittest import TestCase
from tempfile import NamedTemporaryFile
import os


class LightsFileStoreTest(TestCase):
    def setUp(self):
        self.temp_file = NamedTemporaryFile(mode="r+", encoding="utf-8", delete=False)

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_should_write_to_file_when_adding_trigger(self):
        lights = Lights(file_store=self.temp_file.name)
        lights.add_trigger(True, 10, 20)

        self.temp_file.seek(0)
        lines = self.temp_file.read()
        assert_that(lines, has_length(greater_than(0)))

    def test_should_read_triggers_from_file_store(self):
        self.temp_file.write("""[ {
            "repeat_weekday": true,
            "state": true,
            "job_id": "6f9a50b3a85d49e281cbed001717bcee",
            "next_run_time": 1456244400,
            "minute": 20,
            "repeat_weekend": false,
            "hour": 10
            } ]""")
        self.temp_file.truncate()
        lights = Lights(file_store=self.temp_file.name)

        triggers = lights.get_triggers()
        assert_that(triggers, has_length(1))

        jobs = lights._scheduler.get_jobs()
        assert_that(jobs, has_length(1))


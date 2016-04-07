from hamcrest import assert_that, is_, is_not, has_length, empty
from unittest import TestCase
from lights_sqlite_store import LightsSqliteStore
from tempfile import NamedTemporaryFile
from lights import Trigger
import sqlite3
import os
import shutil


class LightsStoreTriggerTest(TestCase):

    def setUp(self):
        self.temp_file = NamedTemporaryFile(mode="r+", encoding="utf-8", delete=False)
        self.trigger = Trigger('6f9a50b3a85d49e281cbed001717bcee', True, 10, 20, True, False)
        self.test_db_file = "tests/triggers.db"

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_should_add_trigger_to_db(self):
        store = LightsSqliteStore(self.temp_file.name)
        store.add_trigger(self.trigger)

        conn = sqlite3.connect(self.temp_file.name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        assert_that(rows, has_length(1))

        actual = rows[0]
        assert_that(actual["job_id"], is_(self.trigger.job_id))
        assert_that(actual["state"], is_(self.trigger.state))
        assert_that(actual["hour"], is_(self.trigger.hour))
        assert_that(actual["minute"], is_(self.trigger.minute))
        assert_that(actual["repeat_weekday"], is_(self.trigger.repeat_weekday))
        assert_that(actual["repeat_weekend"], is_(self.trigger.repeat_weekend))
        conn.close()

    def test_should_read_triggers_from_db(self):
        self.file_has_data(self.test_db_file)
        store = LightsSqliteStore(self.test_db_file)

        triggers = store.read_triggers()
        assert_that(triggers, has_length(1))

        trigger = triggers[0]
        assert_that(trigger.job_id, is_(self.trigger.job_id))
        assert_that(trigger.state, is_(self.trigger.state))
        assert_that(trigger.hour, is_(self.trigger.hour))
        assert_that(trigger.minute, is_(self.trigger.minute))
        assert_that(trigger.repeat_weekday, is_(self.trigger.repeat_weekday))
        assert_that(trigger.repeat_weekend, is_(self.trigger.repeat_weekend))
        assert_that(trigger.next_run_time, is_(None))

    def test_should_return_empty_if_blank_db_file(self):
        store = LightsSqliteStore(self.temp_file.name)

        triggers = store.read_triggers()
        assert_that(triggers, is_(empty()))

    def test_should_remove_trigger_from_db(self):
        shutil.copyfile(self.test_db_file, self.temp_file.name)

        store = LightsSqliteStore(self.temp_file.name)
        store.remove_trigger(self.trigger.job_id)

        conn = sqlite3.connect(self.temp_file.name)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        assert_that(rows, is_(empty()))

        triggers = store.read_triggers()
        assert_that(triggers, is_(empty()))

    def test_should_remove_only_single_trigger(self):
        shutil.copyfile("tests/two_triggers.db", self.temp_file.name)

        store = LightsSqliteStore(self.temp_file.name)

        conn = sqlite3.connect(self.temp_file.name)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        assert_that(rows, has_length(2))

        triggers = store.read_triggers()
        assert_that(triggers, has_length(2))

        store.remove_trigger(self.trigger.job_id)

        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        assert_that(rows, has_length(1))

        triggers = store.read_triggers()
        assert_that(triggers, has_length(1))

    @staticmethod
    def file_has_data(test_db_file):
        conn = sqlite3.connect(test_db_file)
        assert_that(conn, is_not(None))

        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        assert_that(rows, has_length(1))
        conn.close()

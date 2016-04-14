from hamcrest import assert_that, is_, is_not, has_length, empty
from unittest import TestCase
from lights_sqlite_store import LightsSqliteStore
from datetime import datetime
from tempfile import NamedTemporaryFile
import sqlite3
import os
from freezegun import freeze_time
from pytz import utc

SOURCE = "test"
NOW = datetime(2016, 4, 7, 12, 23, 57, 0, utc)
TIMESTAMP = 1460031837


class LightsStoreHistoryTest(TestCase):

    def setUp(self):
        self.test_db_file = "tests/history.db"
        self.temp_file = NamedTemporaryFile(mode="r+", encoding="utf-8", delete=False)

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_should_read_history_from_db(self):
        store = LightsSqliteStore(self.test_db_file)

        history = store.read_history()
        assert_that(history, has_length(1))

        entry = history[0]
        self.assert_entry_correct(entry)

    @freeze_time(NOW)
    def test_should_add_entry_to_history_db(self):
        store = LightsSqliteStore(self.temp_file.name)
        store.add_entry(True, SOURCE)

        conn = sqlite3.connect(self.temp_file.name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM history").fetchall()
        assert_that(rows, has_length(1))

        entry = rows[0]
        assert_that(entry["timestamp"], is_(TIMESTAMP))
        assert_that(entry["source"], is_(SOURCE))
        assert_that(entry["state"], is_(True))

        history = store.read_history()
        assert_that(history, has_length(1))

        entry = history[0]
        self.assert_entry_correct(entry)

    @staticmethod
    def assert_entry_correct(entry):
        assert_that(entry.datetime, is_(NOW))
        assert_that(entry.timestamp, is_(TIMESTAMP))
        assert_that(entry.source, is_(SOURCE))
        assert_that(entry.state, is_(True));

import sqlite3
from lights import Trigger, Entry
import time

CREATE_TRIGGER_TABLE = """CREATE TABLE IF NOT EXISTS 'triggers' (
    'job_id' TEXT NOT NULL UNIQUE,
    'state' INTEGER NOT NULL,
    'hour' INTEGER NOT NULL,
    'minute' INTEGER NOT NULL,
    'repeat_weekday' INTEGER NOT NULL,
    'repeat_weekend' INTEGER NOT NULL,
    PRIMARY KEY(job_id)
    );"""

CREATE_HISTORY_TABLE = """CREATE TABLE IF NOT EXISTS "history" (
    'timestamp' INTEGER NOT NULL UNIQUE,
    'state' INTEGER NOT NULL,
    'source' TEXT NOT NULL
    );"""

INSERT_TRIGGER = """INSERT INTO triggers
    (job_id, state, hour, minute, repeat_weekday, repeat_weekend)
    VALUES (?, ?, ?, ?, ?, ?)"""

INSERT_HISTORY = "INSERT INTO history (timestamp, state, source) VALUES (?, ?, ?)"

GET_HISTORY = "SELECT timestamp, state, source FROM history ORDER BY timestamp DESC LIMIT 10"

DELETE_TRIGGER = "DELETE FROM triggers WHERE job_id=?"


class LightsSqliteStore:

    def __init__(self, database):
        self._database = database

    def add_trigger(self, trigger):
        conn = sqlite3.connect(self._database)
        self._create_tables(conn)
        self._insert_trigger(conn, trigger)
        conn.close()

    @staticmethod
    def _create_tables(conn):
        conn.execute(CREATE_TRIGGER_TABLE)
        conn.execute(CREATE_HISTORY_TABLE)
        conn.commit()

    @staticmethod
    def _insert_trigger(conn, trigger):
        conn.execute(INSERT_TRIGGER, (trigger.job_id,
                                      trigger.state,
                                      trigger.hour,
                                      trigger.minute,
                                      trigger.repeat_weekday,
                                      trigger.repeat_weekend))
        conn.commit()

    def remove_trigger(self, job_id):
        conn = sqlite3.connect(self._database)
        conn.execute(DELETE_TRIGGER, (job_id,))
        conn.commit()
        conn.close()

    def read_triggers(self):
        conn = sqlite3.connect(self._database)
        self._create_tables(conn)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        triggers = [Trigger(**row) for row in rows]
        conn.close()
        return triggers

    def read_history(self):
        conn = sqlite3.connect(self._database)
        self._create_tables(conn)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        rows = cursor.execute(GET_HISTORY).fetchall()
        entries = [Entry(**row) for row in rows]
        conn.close()
        return entries

    def add_entry(self, state, source):
        conn = sqlite3.connect(self._database)
        self._create_tables(conn)

        timestamp = int(time.time())
        conn.execute(INSERT_HISTORY, (timestamp, state, source))
        conn.commit()
        conn.close()

import sqlite3
from lights import Trigger

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS 'triggers' (
    'job_id' TEXT NOT NULL UNIQUE,
    'state'    INTEGER NOT NULL,
    'hour'    INTEGER NOT NULL,
    'minute'    INTEGER NOT NULL,
    'repeat_weekday'    INTEGER NOT NULL,
    'repeat_weekend'    INTEGER NOT NULL,
    PRIMARY KEY(job_id)
    );"""

INSERT_TRIGGER = """INSERT INTO triggers
    (job_id, state, hour, minute, repeat_weekday, repeat_weekend)
    VALUES (?, ?, ?, ?, ?, ?)"""

DELETE_TRIGGER = """DELETE from triggers WHERE job_id=?"""

class LightsSqliteStore:

    def __init__(self, database):
        self._database = database

    def add_trigger(self, trigger):
        conn = sqlite3.connect(self._database)
        self._create_table(conn)
        self._insert_trigger(conn, trigger)
        conn.close()

    @staticmethod
    def _create_table(conn):
        conn.execute(CREATE_TABLE)
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
        self._create_table(conn)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM triggers").fetchall()
        triggers = [Trigger(**row) for row in rows]
        conn.close()
        return triggers

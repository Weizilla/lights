from lights import Lights, Trigger
from unittest import TestCase
from tempfile import NamedTemporaryFile
from lights_sqlite_store import LightsSqliteStore
from unittest.mock import Mock, MagicMock, ANY
import os

TRIGGER = Trigger('6f9a50b3a85d49e281cbed001717bcee', True, 10, 20, True, False)


class LightsStoreTest(TestCase):

    def setUp(self):
        self.store = LightsStoreStub()
        self.lights = Lights(store=self.store)

    def test_should_add_trigger_to_store(self):
        self.store.add_trigger = MagicMock()
        self.lights.add_trigger(True, 10, 20)
        self.store.add_trigger.assert_called_with(ANY)

    def test_should_read_triggers_from_store(self):
        self.store.read_triggers = MagicMock()
        self.lights = Lights(store=self.store)
        self.store.read_triggers.assert_called_with()

    def test_should_remove_trigger_from_store(self):
        self.store.remove_trigger = MagicMock()
        self.lights.remove_trigger(job_id=TRIGGER.job_id)
        self.store.remove_trigger.assert_called_with(TRIGGER.job_id)

    def test_should_add_history_entry_to_store(self):
        self.store.add_entry = MagicMock()
        self.lights.set_state(True, "test")
        self.store.add_entry.assert_called_with(True, "test")

    def test_should_read_history_from_store(self):
        self.store.read_history = MagicMock()
        self.lights.get_history()
        self.store.read_history.assert_called_with()


class LightsStoreStub:
    @staticmethod
    def read_triggers():
        return [TRIGGER]

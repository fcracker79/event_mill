import unittest
from unittest import mock

from event_mill.event_source.declarations import EventSource
from event_mill.projection.declarations import Projection
from event_mill.reactor.definitions import SyncProjectionReactor


class TestSyncProjectionReactor(unittest.TestCase):
    def setUp(self):
        self.mock_projection = mock.create_autospec(Projection)
        self.mock_event_source = mock.create_autospec(EventSource)
        self.mock_limit = mock.create_autospec(int)
        self.sut = SyncProjectionReactor(self.mock_projection, self.mock_event_source, limit=self.mock_limit)

    def test_loop(self):
        pass

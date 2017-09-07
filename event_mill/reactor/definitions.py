from event_mill.event_source.declarations import EventSource
from event_mill.projection.declarations import Projection
from event_mill.reactor.declarations import Reactor


class SyncProjectionReactor(Reactor):
    def __init__(self, projection: Projection, event_source: EventSource, limit: int):
        self._projection = projection
        self._event_source = event_source
        self._limit = limit

    def loop(self):
        while True:
            with self._event_source.get_events(self._limit) as events:
                for e in events:
                    self._projection.project(e)

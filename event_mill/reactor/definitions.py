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
            self._event_source.before()
            try:
                events = self._event_source.get_events(self._limit)
                for e in events:
                    self._projection.project(e)
            except Exception as e:
                # TODO log
                self._event_source.after_error(e)
            else:
                self._event_source.after()

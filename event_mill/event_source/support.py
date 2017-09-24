import abc
import typing

from event_mill.event.declarations import Event
from event_mill.event_source.declarations import EventIterable, EventSource, Rewindable


class EmptyEventIterable(EventIterable):
    def __enter__(self):
        pass

    def __iter__(self) -> typing.Iterable[Event]:
        return ()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class DelegateEventIterable(EventIterable):
    def __init__(self, delegate: EventIterable, on_exit_callback: typing.Callable[[], None]):
        self._events = None
        self._delegate = delegate
        self._on_exit_callback = on_exit_callback

    def __enter__(self) -> EventIterable:
        self._events = self._delegate.__enter__()
        return self

    def __iter__(self) -> typing.Iterable[Event]:
        return self._events

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            self._on_exit_callback()
        return self._delegate.__exit__(exc_type, exc_val, exc_tb)


class DelegateRewindableEventSource(EventSource, Rewindable, metaclass=abc.ABCMeta):
    def __init__(self, delegate: EventSource):
        self._delegate = delegate

    @abc.abstractmethod
    def _set_height(self, height: int) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_height(self) -> int:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_events(self, limit: int) -> EventIterable:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_received_events_height(self) -> int:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _save_received_events(self, events: typing.Iterable[Event]):
        pass  # pragma: no cover

    def _get_events_and_update_height(self, limit: int) -> typing.Optional[DelegateEventIterable]:
        received_events_height = self._get_received_events_height()
        if self._get_height() == received_events_height:
            return None
        return DelegateEventIterable(self._get_events(limit), lambda: self._set_height(received_events_height))

    def get_events(self, limit: int) -> EventIterable:
        events = self._get_events_and_update_height(limit)
        if events is None:
            with self._delegate.get_events(limit) as events:
                self._save_received_events(events)
            events = EmptyEventIterable()
        return events

    def rewind(self):
        self._set_height(0)

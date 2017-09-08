import abc
import typing

from event_mill.event.declarations import Event


class Rewindable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rewind(self):
        pass  # pragma: no cover


class EventSource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_events(self, limit: int) -> typing.Iterable[Event]:
        pass  # pragma: no cover

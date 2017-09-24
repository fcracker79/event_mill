import abc
import collections
import typing

from event_mill.event.declarations import Event


class EventIterable(collections.Iterable, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __enter__(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # pragma: no cover

    @abc.abstractmethod
    def __iter__(self) -> typing.Iterable[Event]:
        pass  # pragma: no cover


class EventSource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_events(self, limit: int) -> EventIterable:
        pass  # pragma: no cover


class Rewindable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rewind(self):
        pass  # pragma: no cover

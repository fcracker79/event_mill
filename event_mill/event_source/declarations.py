import abc
import typing

from event_mill.event.declarations import Event


class Rewindable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rewind(self):
        pass  # pragma: no cover


class EventSource(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def before(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def get_events(self, limit: int) -> typing.Iterable[Event]:
        pass  # pragma: no cover

    @abc.abstractmethod
    def after(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def after_error(self, error: Exception) -> None:
        pass  # pragma: no cover

import abc
from event_mill.event.declarations import Event


class Projection(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def project(self, event: Event) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def clear(self) -> None:
        pass  # pragma: no cover

import abc
import typing
import uuid


class Event(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def uid(self) -> uuid.UUID:
        pass  # pragma: no cover

    @property
    @abc.abstractmethod
    def payload(self) -> typing.Any:
        pass  # pragma: no cover

    def __eq__(self, other):
        return type(self) == type(other) and self.uid == other.uid

    def __hash__(self):
        return hash(self.uid)

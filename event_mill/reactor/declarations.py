import abc


class Reactor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def loop(self) -> None:
        pass  # pragma: no cover

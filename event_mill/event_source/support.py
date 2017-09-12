import abc
import typing

from event_mill.event.declarations import Event
from event_mill.event_source.declarations import EventSource, Rewindable


class DelegateRewindableEventSource(EventSource, Rewindable, metaclass=abc.ABCMeta):
    def __init__(self, delegate: EventSource):
        self._delegate = delegate
        self._before_called = False

    def before(self):
        assert not self._before_called
        self._before_called = True

    @abc.abstractmethod
    def _before_storage(self) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _set_height(self, height: int) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_events_and_update_height(self, limit: int) -> typing.Iterable[Event]:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _add_events_and_update_height(self, events: typing.Iterable[Event]):
        pass  # pragma: no cover

    def get_events(self, limit: int) -> typing.Iterable[Event]:
        assert not self._before_called
        events = None
        while not events:
            self._before_storage()
            try:
                events = self._get_events_and_update_height(limit)
            except Exception as e:
                # TODO log
                self.after_error(e)

            if not events:
                self.after()
                self._delegate.before()
                try:
                    events = self._delegate.get_events(limit)
                except Exception as e:
                    # TODO log
                    self._delegate.after_error(e)
                else:
                    self._before_storage()
                    try:
                        self._add_events_and_update_height(events)
                    except Exception as e:
                        # TODO log
                        self.after_error(e)
                    else:
                        self.after()
                    self._delegate.after()
        self._before_called = False
        return events

    def rewind(self):
        self._set_height(0)


class DelegateContextEventSource(EventSource, metaclass=abc.ABCMeta):
    def __init__(self, delegate: EventSource):
        self._delegate = delegate

    @abc.abstractmethod
    def _before_get_events(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def _after_get_events(self):
        pass  # pragma: no cover

    @abc.abstractmethod
    def _after_failed_get_events(self, exception: Exception):
        pass  # pragma: no cover

    class _ScopedIterable:
        def __init__(self, context: 'DelegateContextEventSource', generate_events_function: callable):
            self._context = context
            self._generate_events_function = generate_events_function

        def __enter__(self):
            return self._context._before_get_events()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return self._context._after_failed_get_events(exc_val) if exc_val \
                else self._context._after_get_events()

        def __iter__(self):
            return self._generate_events_function()

    def get_events(self, limit: int) -> typing.Iterable[Event]:
        return self._ScopedIterable(self, lambda: self._delegate.get_events(limit))

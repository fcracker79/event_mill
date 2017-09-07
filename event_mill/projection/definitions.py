import abc
import typing

from event_mill.event.declarations import Event
from event_mill.exceptions import EventMillException
from event_mill.projection.declarations import Projection


Record = typing.TypeVar('Record')


class UnprocessableEventException(typing.Generic[Record], EventMillException):
    def __init__(self, record: Record, *a, **kw):
        super(UnprocessableEventException, self).__init__(*a, **kw)
        self._record = record

    @property
    def record(self) -> Record:
        return self._record


class BaseProjection(typing.Generic[Record], Projection, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _get_record_by(self, event: Event) -> Record:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _store_locked_event(self, event: Event, record: Record) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _process_event(self, event: Event, record: Record) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def _get_unlocked_events(self, event: Event, record: Record) -> typing.Set[Event]:
        pass  # pragma: no cover

    def project(self, event: Event) -> None:
        events_to_be_processed = {event, }
        unlocked_events = set()
        processed_events = set()
        while events_to_be_processed:
            unlocked_events.clear()
            processed_events.clear()
            for e in events_to_be_processed:
                try:
                    record = self._get_record_by(e)
                except UnprocessableEventException as ex:
                    self._store_locked_event(e, ex.record)
                else:
                    self._process_event(e, record)
                    processed_events.add(e)
                    unlocked_events |= self._get_unlocked_events(e, record)
            events_to_be_processed = unlocked_events - processed_events

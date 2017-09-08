import abc
import typing

from event_mill.event.declarations import Event
from event_mill.event_source.declarations import EventSource
from event_mill.event_source.support import DelegateContextEventSource, DelegateRewindableEventSource

try:
    from sqlalchemy.orm.session import Session
    from sqlalchemy.exc import SQLAlchemyError

    class SQLAlchemyTransactionDelegateEventSource(DelegateContextEventSource):
        def __init__(self, delegate: EventSource, session_factory: typing.Callable[[], Session]):
            super().__init__(delegate)
            self._session_factory = session_factory

        def _before_get_events(self):
            # This should trigger the creation of a new session
            self._session_factory()

        def _after_failed_get_events(self, exception: Exception):
            try:
                self._session_factory().rollback()
            except SQLAlchemyError:
                pass
                # TODO log

        def _after_get_events(self):
            self._session_factory().commit()

    class SQLAlchemyDelegateRewindableEventSource(DelegateRewindableEventSource, metaclass=abc.ABCMeta):
        def __init__(
                self, delegate: EventSource,
                session_factory: typing.Callable[[], Session]):
            super(SQLAlchemyDelegateRewindableEventSource, self).__init__(delegate)
            self._session_factory = session_factory

        @abc.abstractmethod
        def _query_get_height(self) -> str:
            pass  # pragma: no cover

        @abc.abstractmethod
        def _query_insert_height(self) -> str:
            pass  # pragma: no cover

        @abc.abstractmethod
        def _query_set_height(self) -> str:
            pass  # pragma: no cover

        @abc.abstractmethod
        def _get_events_by_limits(self) -> str:
            pass  # pragma: no cover

        @abc.abstractmethod
        def _hydrate_event(self, dbms_data: typing.Any) -> Event:
            pass  # pragma: no cover

        def _get_height(self):
            session = self._session_factory()
            result = session.connection().execute(self._query_get_height())
            return result and result[0] or None

        def _set_height(self, height: int) -> None:
            session = self._session_factory()
            result = session.connection().execute(self._query_get_height())
            if result and result[0]:
                session.execute(self._query_set_height(), (height, ))
            else:
                session.execute(self._query_insert_height(), (height,))

        def _get_events_and_update_height(self, limit: int) -> typing.Iterable[Event]:
            result = [
                self._hydrate_event(row)
                for row in self._session_factory().connection().execute(self._get_events_by_limits(), (limit, ))
            ]
            self._set_height(self._get_height() + len(result))
            return result

        @abc.abstractmethod
        def _add_event(self, event: Event, session: Session):
            pass  # pragma: no cover

        def _add_events_and_update_height(self, events: typing.Iterable[Event]):
            session = self._session_factory()
            count = 0
            for event in events:
                self._add_event(event, session)
            self._set_height(self._get_height() + count)

except ImportError:
    Session = SQLAlchemyError = None
    # TODO logs

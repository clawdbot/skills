import asyncio
import inspect
import typing as t
from dataclasses import dataclass
from enum import Enum

import typing_extensions as te
from atproto_core.did_doc import DidDocument, is_valid_did_doc
from atproto_server.auth.jwt import get_jwt_payload

if t.TYPE_CHECKING:
    from atproto_server.auth.jwt import JwtPayload

    from atproto_client import models


_SESSION_STRING_SEPARATOR: t.Final[te.Literal[':::']] = ':::'


class SessionEvent(Enum):
    IMPORT = 'import'
    CREATE = 'create'
    REFRESH = 'refresh'


SessionResponse: te.TypeAlias = t.Union[
    'models.ComAtprotoServerCreateSession.Response',
    'models.ComAtprotoServerRefreshSession.Response',
    'Session',
]

SessionChangeCallback = t.Callable[[SessionEvent, 'Session'], None]
AsyncSessionChangeCallback = t.Callable[[SessionEvent, 'Session'], t.Coroutine[t.Any, t.Any, None]]


def _session_exists(session: t.Optional['Session']) -> te.TypeGuard['Session']:
    if not session:
        raise ValueError('Session does not exists. It is not possible to dispatch session change event.')

    return isinstance(session, Session)


class SessionDispatcher:
    def __init__(self, session: t.Optional['Session'] = None) -> None:
        self._session: t.Optional['Session'] = session

        self._on_session_change_callbacks: t.List[SessionChangeCallback] = []
        self._on_session_change_async_callbacks: t.List[AsyncSessionChangeCallback] = []

    def set_session(self, session: 'Session') -> None:
        self._session = session

    def on_session_change(self, callback: t.Union['AsyncSessionChangeCallback', 'SessionChangeCallback']) -> None:
        if inspect.iscoroutinefunction(callback):
            self._on_session_change_async_callbacks.append(callback)
        elif inspect.isfunction(callback):
            self._on_session_change_callbacks.append(callback)

    def dispatch_session_change(self, event: SessionEvent) -> None:
        self._call_on_session_change_callbacks(event)

    async def dispatch_session_change_async(self, event: SessionEvent) -> None:
        self._call_on_session_change_callbacks(event)  # Allow synchronous callbacks in the async client
        await self._call_on_session_change_callbacks_async(event)

    def _call_on_session_change_callbacks(self, event: SessionEvent) -> None:
        assert _session_exists(self._session)
        session_copy = self._session.copy()  # Avoid modifying the original session

        for on_session_change_callback in self._on_session_change_callbacks:
            on_session_change_callback(event, session_copy)

    async def _call_on_session_change_callbacks_async(self, event: SessionEvent) -> None:
        assert _session_exists(self._session)
        session_copy = self._session.copy()  # Avoid modifying the original session

        coroutines: t.List[t.Coroutine[t.Any, t.Any, None]] = []
        for on_session_change_async_callback in self._on_session_change_async_callbacks:
            coroutines.append(on_session_change_async_callback(event, session_copy))

        await asyncio.gather(*coroutines)


@dataclass
class Session:
    handle: str
    did: str
    access_jwt: str
    refresh_jwt: str
    pds_endpoint: t.Optional[str] = 'https://bsky.social'  # Backward compatibility for old sessions

    @property
    def access_jwt_payload(self) -> 'JwtPayload':
        return get_jwt_payload(self.access_jwt)

    @property
    def refresh_jwt_payload(self) -> 'JwtPayload':
        return get_jwt_payload(self.refresh_jwt)

    def __repr__(self) -> str:
        return f'<Session handle={self.handle} did={self.did}>'

    def __str__(self) -> str:
        return self.encode()

    def encode(self) -> str:
        payload = [
            self.handle,
            self.did,
            self.access_jwt,
            self.refresh_jwt,
            self.pds_endpoint,
        ]
        return _SESSION_STRING_SEPARATOR.join(payload)

    @classmethod
    def decode(cls, session_string: str) -> 'Session':
        fields = session_string.split(_SESSION_STRING_SEPARATOR)

        if len(fields) == 4:
            # Old session format
            handle, did, access_jwt, refresh_jwt = fields
            return cls(handle, did, access_jwt, refresh_jwt)

        handle, did, access_jwt, refresh_jwt, pds_endpoint = session_string.split(_SESSION_STRING_SEPARATOR)
        return cls(handle, did, access_jwt, refresh_jwt, pds_endpoint)

    def copy(self) -> 'Session':
        return Session(self.handle, self.did, self.access_jwt, self.refresh_jwt, self.pds_endpoint)

    #: Alias for :attr:`encode`
    export = encode


def get_session_pds_endpoint(session: 'SessionResponse') -> t.Optional[str]:
    """Return the PDS endpoint of the given session.

    Note:
        Return :obj:`None` for self-hosted PDSs.
    """
    if isinstance(session, Session):
        return session.pds_endpoint

    if session.did_doc and is_valid_did_doc(session.did_doc):
        doc = DidDocument.from_dict(session.did_doc)
        return doc.get_pds_endpoint()

    return None

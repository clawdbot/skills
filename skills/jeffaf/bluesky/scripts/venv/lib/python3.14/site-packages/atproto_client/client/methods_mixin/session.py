import typing as t
from datetime import timedelta

from atproto_client.client.methods_mixin.time import TimeMethodsMixin
from atproto_client.client.session import (
    AsyncSessionChangeCallback,
    Session,
    SessionChangeCallback,
    SessionDispatcher,
    SessionEvent,
    SessionResponse,
    get_session_pds_endpoint,
)
from atproto_client.exceptions import LoginRequiredError


class SessionDispatchMixin:
    def on_session_change(self, callback: SessionChangeCallback) -> None:
        """Register a callback for session change event.

        Args:
            callback: A callback to be called when the session changes.
                The callback must accept two arguments: event and session.

        Note:
            Possible events: `SessionEvent.IMPORT`, `SessionEvent.CREATE`, `SessionEvent.REFRESH`.

        Tip:
            You should save the session string to persistent storage
            on `SessionEvent.CREATE` and `SessionEvent.REFRESH` event.

        Example:
            >>> from atproto import Client, SessionEvent, Session
            >>>
            >>> client = Client()
            >>>
            >>> @client.on_session_change
            >>> def on_session_change(event: SessionEvent, session: Session):
            >>>     print(event, session)
            >>>
            >>> # or you can use this syntax:
            >>> # client.on_session_change(on_session_change)

        Returns:
            :obj:`None`
        """
        self._session_dispatcher.on_session_change(callback)

    def _call_on_session_change_callbacks(self, event: SessionEvent) -> None:
        self._session_dispatcher.dispatch_session_change(event)


class AsyncSessionDispatchMixin:
    def on_session_change(self, callback: t.Union['AsyncSessionChangeCallback', 'SessionChangeCallback']) -> None:
        """Register a callback for session change event.

        Args:
            callback: A callback to be called when the session changes.
                The callback must accept two arguments: event and session.

        Note:
            Possible events: `SessionEvent.IMPORT`, `SessionEvent.CREATE`, `SessionEvent.REFRESH`.

        Note:
            You can register both synchronous and asynchronous callbacks.

        Tip:
            You should save the session string to persistent storage
            on `SessionEvent.CREATE` and `SessionEvent.REFRESH` event.

        Example:
            >>> from atproto import AsyncClient, SessionEvent, Session
            >>>
            >>> client = AsyncClient()
            >>>
            >>> @client.on_session_change
            >>> async def on_session_change(event: SessionEvent, session: Session):
            >>>     print(event, session)
            >>>
            >>> # or you can use this syntax:
            >>> # client.on_session_change(on_session_change)

        Returns:
            :obj:`None`
        """
        self._session_dispatcher.on_session_change(callback)

    async def _call_on_session_change_callbacks(self, event: SessionEvent) -> None:
        await self._session_dispatcher.dispatch_session_change_async(event)


class SessionMethodsMixin(TimeMethodsMixin):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self._session: t.Optional[Session] = None
        self._session_dispatcher = SessionDispatcher()

    def _register_auth_headers_source(self) -> None:
        self.request.add_additional_headers_source(self._get_access_auth_headers)

    def _should_refresh_session(self) -> bool:
        if not self._session or not self._session.access_jwt_payload or not self._session.access_jwt_payload.exp:
            raise LoginRequiredError

        expired_at = self.get_time_from_timestamp(self._session.access_jwt_payload.exp)
        expired_at = expired_at - timedelta(minutes=15)  # let's update the token a bit earlier than required

        return self.get_current_time() > expired_at

    def _set_or_update_session(self, session: SessionResponse, pds_endpoint: str) -> 'Session':
        if not self._session:
            self._session = Session(
                access_jwt=session.access_jwt,
                refresh_jwt=session.refresh_jwt,
                did=session.did,
                handle=session.handle,
                pds_endpoint=pds_endpoint,
            )
            self._session_dispatcher.set_session(self._session)
            self._register_auth_headers_source()
        else:
            self._session.access_jwt = session.access_jwt
            self._session.refresh_jwt = session.refresh_jwt
            self._session.did = session.did
            self._session.handle = session.handle
            self._session.pds_endpoint = pds_endpoint

        return self._session

    def _set_session_common(self, session: SessionResponse, current_pds: str) -> Session:
        pds_endpoint = get_session_pds_endpoint(session)
        if not pds_endpoint:
            # current_pds ends with xrpc endpoint, but this is not a problem
            # overhead is only 4-5 symbols in the exported session string
            pds_endpoint = current_pds

        self._update_pds_endpoint(pds_endpoint)
        return self._set_or_update_session(session, pds_endpoint)

    def _get_access_auth_headers(self) -> t.Dict[str, str]:
        if not self._session:
            return {}

        return {'Authorization': f'Bearer {self._session.access_jwt}'}

    def _get_refresh_auth_headers(self) -> t.Dict[str, str]:
        if not self._session:
            return {}

        return {'Authorization': f'Bearer {self._session.refresh_jwt}'}

    def _update_pds_endpoint(self, pds_endpoint: str) -> None:
        self.update_base_url(pds_endpoint)

    def export_session_string(self) -> str:
        """Export session string.

        Note:
            This method is useful for storing the session and reusing it later.

        Warning:
            You should use it if you create the client instance often.
            Because of server rate limits for `createSession`.
            Rate limited by handle.
            30/5 min, 300/day.

        Attention:
            You must export session at the end of the Client`s life cycle!
            Alternatively, you can subscribe to the session change event.
            Use :py:attr:`~on_session_change` to register handler.

        Example:
            >>> from atproto import Client
            >>> # the first time login with login and password
            >>> client = Client()
            >>> client.login('login', 'password')
            >>> session_string = client.export_session_string()
            >>> # store session_string somewhere.
            >>> # for example, in env and next time use it for login
            >>> client2 = Client()
            >>> client2.login(session_string=session_string)

        Returns:
            :obj:`str`: Session string.
        """
        if not self._session:
            raise LoginRequiredError

        return self._session.export()

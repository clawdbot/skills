import asyncio
import random
import socket
import time
import traceback
import typing as t
from copy import deepcopy
from urllib.parse import urlencode

from atproto_client.models import get_model_as_dict
from atproto_client.models.base import ParamsModelBase
from atproto_client.models.common import XrpcError
from atproto_core.exceptions import DAGCBORDecodingError
from websockets.asyncio.client import connect as aconnect
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    InvalidHandshake,
    PayloadTooBig,
    ProtocolError,
)
from websockets.sync.client import connect

from atproto_firehose.exceptions import FirehoseDecodingError, FirehoseError
from atproto_firehose.models import ErrorFrame, Frame, MessageFrame

_MAX_MESSAGE_SIZE_BYTES = 1024 * 1024 * 5  # 5MB

OnMessageCallback = t.Callable[['MessageFrame'], None]
AsyncOnMessageCallback = t.Callable[['MessageFrame'], t.Coroutine[t.Any, t.Any, None]]

OnCallbackErrorCallback = t.Callable[[BaseException], None]
AsyncOnCallbackErrorCallback = t.Callable[[BaseException], t.Coroutine[t.Any, t.Any, None]]

_OK_ERRORS = (ConnectionClosedOK,)
_ERR_ERRORS = (
    TimeoutError,
    asyncio.TimeoutError,
    ConnectionError,
    ConnectionClosedError,
    InvalidHandshake,
    PayloadTooBig,
    ProtocolError,
    socket.gaierror,
)


if t.TYPE_CHECKING:
    from websockets.asyncio.client import connect as AsyncConnect
    from websockets.sync.client import ClientConnection as SyncWebSocketClient


def _build_websocket_uri(method: str, base_uri: str, params: t.Optional[t.Dict[str, t.Any]] = None) -> str:
    query_string = ''
    if params:
        query_string = f'?{urlencode(params)}'

    return f'{base_uri}/{method}{query_string}'


def _handle_frame_decoding_error(exception: Exception) -> None:
    if isinstance(exception, (DAGCBORDecodingError, FirehoseDecodingError)):
        # Ignore an invalid atproto_firehose frame that could not be properly decoded.
        # It's better to ignore one frame rather than stop the whole connection
        # or trap into an infinite loop of reconnections.
        return

    raise exception


def _handle_websocket_error_or_stop(exception: Exception) -> bool:
    """Return if the connection should be properly being closed or reraise exception."""
    if isinstance(exception, _OK_ERRORS):
        return True
    if isinstance(exception, _ERR_ERRORS):
        return False

    if isinstance(exception, FirehoseError):
        raise exception

    raise FirehoseError from exception


def _get_message_frame_from_bytes_or_raise(data: bytes) -> MessageFrame:
    frame = Frame.from_bytes(data)
    if isinstance(frame, ErrorFrame):
        raise FirehoseError(XrpcError(frame.body.error, frame.body.message))
    if isinstance(frame, MessageFrame):
        return frame
    raise FirehoseDecodingError('Unknown frame type')


class _WebsocketClientBase:
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        recv_timeout: t.Optional[float] = None,
    ) -> None:
        self._method = method
        self._base_uri = base_uri
        self._params = params
        self._recv_timeout = recv_timeout

        self._reconnect_no = 0
        self._max_reconnect_delay_sec = 64

    def update_params(self, params: t.Union[ParamsModelBase, t.Dict[str, t.Any]]) -> None:
        """Update params.

        Warning:
            If you are using `params` arg at the client start, you must care about keeping params up to date.
            Otherwise, your client will be rolled back to the previous state (cursor) on reconnecting.
        """
        if isinstance(params, ParamsModelBase):
            self._params = get_model_as_dict(params)
        else:
            self._params = deepcopy(params)

    @property
    def _websocket_uri(self) -> str:
        # the user should care about updated params by himself
        return _build_websocket_uri(self._method, self._base_uri, self._params)

    def _get_client(self) -> 'SyncWebSocketClient':
        # Disable automatic pings for sync client (added in websockets v15+)
        # to maintain behavior consistent with <v14 for now.
        return connect(
            self._websocket_uri,
            max_size=_MAX_MESSAGE_SIZE_BYTES,
            close_timeout=0.1,
            # see https://websockets.readthedocs.io/en/stable/topics/keepalive.html
            ping_interval=None,  # Disable automatic pings
        )

    def _get_async_client(self) -> 'AsyncConnect':
        # Async client connect function accepts ping_interval directly (default is 20s)
        return aconnect(self._websocket_uri, max_size=_MAX_MESSAGE_SIZE_BYTES, close_timeout=0.1)

    def _get_reconnection_delay(self) -> int:
        base_sec = 2**self._reconnect_no
        rand_sec = random.uniform(-0.5, 0.5)  # noqa: S311

        return min(base_sec, self._max_reconnect_delay_sec) + rand_sec


class _WebsocketClient(_WebsocketClientBase):
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        recv_timeout: t.Optional[float] = None,
    ) -> None:
        super().__init__(method, base_uri, params, recv_timeout)

        self._stopped = False

        self._on_message_callback: t.Optional[OnMessageCallback] = None
        self._on_callback_error_callback: t.Optional[OnCallbackErrorCallback] = None

    def _process_message_frame(self, frame: 'MessageFrame') -> None:
        try:
            if self._on_message_callback is not None:
                self._on_message_callback(frame)
        except Exception as e:  # noqa: BLE001
            if self._on_callback_error_callback:
                try:
                    self._on_callback_error_callback(e)
                except:  # noqa
                    traceback.print_exc()
            else:
                traceback.print_exc()

    def start(
        self,
        on_message_callback: OnMessageCallback,
        on_callback_error_callback: t.Optional[OnCallbackErrorCallback] = None,
    ) -> None:
        """Subscribe to Firehose and start client.

        Args:
            on_message_callback: Callback that will be called on the new Firehose message.
            on_callback_error_callback: Callback that will be called if the `on_message_callback` raised an exception.

        Returns:
            :obj:`None`
        """
        self._on_message_callback = on_message_callback
        self._on_callback_error_callback = on_callback_error_callback

        while not self._stopped:
            try:
                if self._reconnect_no != 0:
                    time.sleep(self._get_reconnection_delay())

                with self._get_client() as client:
                    self._reconnect_no = 0

                    while not self._stopped:
                        raw_frame = client.recv(self._recv_timeout)
                        if isinstance(raw_frame, str):
                            # skip text frames (should not be occurred)
                            continue

                        try:
                            frame = _get_message_frame_from_bytes_or_raise(raw_frame)
                            self._process_message_frame(frame)
                        except Exception as e:  # noqa: BLE001
                            _handle_frame_decoding_error(e)
            except Exception as e:  # noqa: BLE001
                self._reconnect_no += 1

                should_stop = _handle_websocket_error_or_stop(e)
                if should_stop:
                    break

    def stop(self) -> None:
        """Unsubscribe and stop the Firehose client.

        Returns:
            :obj:`None`
        """
        self._stopped = True


class _AsyncWebsocketClient(_WebsocketClientBase):
    def __init__(
        self,
        method: str,
        base_uri: str,
        params: t.Optional[t.Dict[str, t.Any]] = None,
        recv_timeout: t.Optional[float] = None,
    ) -> None:
        super().__init__(method, base_uri, params, recv_timeout)

        self._stop_event = asyncio.Event()

        self._on_message_callback: t.Optional[AsyncOnMessageCallback] = None
        self._on_callback_error_callback: t.Optional[AsyncOnCallbackErrorCallback] = None

    async def _process_message_frame(self, frame: 'MessageFrame') -> None:
        try:
            if self._on_message_callback is not None:
                await self._on_message_callback(frame)
        except Exception as e:  # noqa: BLE001
            if self._on_callback_error_callback:
                try:
                    await self._on_callback_error_callback(e)
                except:  # noqa
                    traceback.print_exc()
            else:
                traceback.print_exc()

    async def start(
        self,
        on_message_callback: AsyncOnMessageCallback,
        on_callback_error_callback: t.Optional[AsyncOnCallbackErrorCallback] = None,
    ) -> None:
        """Subscribe to Firehose and start client.

        Args:
            on_message_callback: Callback that will be called on the new Firehose message.
            on_callback_error_callback: Callback that will be called if the `on_message_callback` raised an exception.

        Returns:
            :obj:`None`
        """
        self._on_message_callback = on_message_callback
        self._on_callback_error_callback = on_callback_error_callback

        while not self._stop_event.is_set():
            try:
                if self._reconnect_no != 0:
                    await asyncio.sleep(self._get_reconnection_delay())

                async with self._get_async_client() as client:
                    self._reconnect_no = 0

                    while not self._stop_event.is_set():
                        # TODO(MarshalX): if the perf will be critical consider to use async-timeout lib
                        raw_frame = await asyncio.wait_for(client.recv(), timeout=self._recv_timeout)
                        if isinstance(raw_frame, str):
                            # skip text frames (should not be occurred)
                            continue

                        try:
                            frame = _get_message_frame_from_bytes_or_raise(raw_frame)
                            await self._process_message_frame(frame)
                        except Exception as e:  # noqa: BLE001
                            _handle_frame_decoding_error(e)

            except Exception as e:  # noqa: BLE001
                self._reconnect_no += 1

                should_stop = _handle_websocket_error_or_stop(e)
                if should_stop:
                    break

    async def stop(self) -> None:
        """Unsubscribe and stop the Firehose client.

        Returns:
            :obj:`None`
        """
        self._stop_event.set()


FirehoseClient = _WebsocketClient
AsyncFirehoseClient = _AsyncWebsocketClient

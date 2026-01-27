import typing as t
from enum import Enum

import typing_extensions as te
from httpx import Headers

from atproto_client.models.utils import get_model_as_dict, get_model_as_json
from atproto_client.request import AsyncRequest, Request, Response

if t.TYPE_CHECKING:
    from atproto_client.models.base import DataModelBase, ParamsModelBase

# TODO(MarshalX): Generate async version automatically!


class InvokeType(Enum):
    QUERY = 'query'
    PROCEDURE = 'procedure'


_BASE_API_URL = 'https://bsky.social/xrpc'

_CONTENT_TYPE_JSON = 'application/json'
_DEFAULT_CONTENT_TYPE = _CONTENT_TYPE_JSON


def _handle_kwargs(kwargs: dict) -> None:
    """Mutates input data."""
    headers = Headers(kwargs.get('headers'))  # case-insensitive dict

    content_type = headers.get('Content-Type', _DEFAULT_CONTENT_TYPE)
    # set content type from lexicon only if it's not set by user
    if 'Content-Type' not in headers and 'input_encoding' in kwargs:
        content_type = kwargs['input_encoding']
        headers['Content-Type'] = content_type

    if content_type == _CONTENT_TYPE_JSON and 'data' in kwargs and kwargs['data']:
        kwargs['content'] = get_model_as_json(kwargs.pop('data'))

    if kwargs.get('params'):
        kwargs['params'] = get_model_as_dict(kwargs['params'])

    # set headers back
    kwargs['headers'] = dict(headers.items())

    # pop non-request kwargs
    kwargs.pop('input_encoding', None)
    kwargs.pop('output_encoding', None)


def _handle_base_url(base_url: t.Optional[str] = None) -> str:
    if base_url is None:
        return _BASE_API_URL

    if not base_url.endswith('/xrpc'):
        return f'{base_url.rstrip("/")}/xrpc'

    return base_url


class _ClientCommonMethodsMixin:
    def clone(self) -> te.Self:
        """Clone the client instance.

        Used to customize atproto proxy and set of labeler services.

        Returns:
            Cloned client instance.
        """
        return type(self)(base_url=self._base_url, request=self.request.clone())

    def update_base_url(self, base_url: t.Optional[str] = None) -> None:
        """Update XRPC base URL.

        Typically used for switching between PDSs.

        Args:
            base_url: New base URL.
                Defaults to bsky.social.
        """
        self._base_url = _handle_base_url(base_url)

    def _build_url(self, nsid: str) -> str:
        return f'{self._base_url}/{nsid}'


class ClientBase(_ClientCommonMethodsMixin):
    """Low-level methods are here."""

    def __init__(self, base_url: t.Optional[str] = None, request: t.Optional[Request] = None) -> None:
        if request is None:
            request = Request()

        self._request = request
        self._base_url = _handle_base_url(base_url)

    @property
    def request(self) -> Request:
        return self._request

    def invoke_query(
        self,
        nsid: str,
        params: t.Optional['ParamsModelBase'] = None,
        data: t.Optional[t.Union['DataModelBase', bytes]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._invoke(InvokeType.QUERY, url=self._build_url(nsid), params=params, data=data, **kwargs)

    def invoke_procedure(
        self,
        nsid: str,
        params: t.Optional['ParamsModelBase'] = None,
        data: t.Optional[t.Union['DataModelBase', bytes]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._invoke(InvokeType.PROCEDURE, url=self._build_url(nsid), params=params, data=data, **kwargs)

    def _invoke(self, invoke_type: InvokeType, **kwargs: t.Any) -> Response:
        _handle_kwargs(kwargs)

        if invoke_type is InvokeType.QUERY:
            return self.request.get(**kwargs)
        return self.request.post(**kwargs)


class AsyncClientBase(_ClientCommonMethodsMixin):
    """Low-level methods are here."""

    def __init__(self, base_url: t.Optional[str] = None, request: t.Optional[AsyncRequest] = None) -> None:
        if request is None:
            request = AsyncRequest()

        self._request = request
        self._base_url = _handle_base_url(base_url)

    @property
    def request(self) -> AsyncRequest:
        return self._request

    async def invoke_query(
        self,
        nsid: str,
        params: t.Optional['ParamsModelBase'] = None,
        data: t.Optional[t.Union['DataModelBase', bytes]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return await self._invoke(InvokeType.QUERY, url=self._build_url(nsid), params=params, data=data, **kwargs)

    async def invoke_procedure(
        self,
        nsid: str,
        params: t.Optional['ParamsModelBase'] = None,
        data: t.Optional[t.Union['DataModelBase', bytes]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return await self._invoke(InvokeType.PROCEDURE, url=self._build_url(nsid), params=params, data=data, **kwargs)

    async def _invoke(self, invoke_type: InvokeType, **kwargs: t.Any) -> Response:
        _handle_kwargs(kwargs)

        if invoke_type is InvokeType.QUERY:
            return await self.request.get(**kwargs)
        return await self.request.post(**kwargs)

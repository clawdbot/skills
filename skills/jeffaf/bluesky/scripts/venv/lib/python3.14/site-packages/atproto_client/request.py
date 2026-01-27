import typing as t
from dataclasses import dataclass
from importlib import metadata as importlib_metadata

import httpx
import typing_extensions as te
from pydantic_core import from_json

from atproto_client import exceptions
from atproto_client.models.common import XrpcError
from atproto_client.models.utils import get_or_create, load_json

try:
    _ATPROTO_SDK_VERSION = importlib_metadata.version('atproto')
except importlib_metadata.PackageNotFoundError:
    _ATPROTO_SDK_VERSION = 'unknown'

_ATPROTO_SDK_USER_AGENT = f'atproto/{_ATPROTO_SDK_VERSION} Python SDK (atproto.blue)'


@dataclass
class Response:
    success: bool
    status_code: int
    content: t.Optional[t.Union[t.Dict[str, t.Any], bytes, 'XrpcError']]
    headers: t.Dict[str, t.Any]


_NormalizedHeaders = t.Dict[str, t.Tuple[str, str]]


def _normalize_headers(headers: t.Dict[str, str]) -> _NormalizedHeaders:
    """Normalize headers by converting keys to lowercase.

    Args:
        headers: Headers dictionary with the original case.

    Returns:
        Dictionary with lowercase keys mapped to tuples of (original_key, value).
    """
    return {key.lower(): (key, value) for key, value in headers.items()}


def _denormalize_headers(headers: _NormalizedHeaders) -> t.Dict[str, str]:
    """Denormalize headers by converting keys back to their original case.

    Args:
        headers: Headers dictionary with lowercase keys mapped to tuples of (original_key, value).

    Returns:
        Dictionary with original keys and values.
    """
    return {original_key: value for _, (original_key, value) in headers.items()}


def _convert_headers_to_dict(headers: httpx.Headers) -> t.Dict[str, str]:
    """Convert custom case-insensitive multi-dict of HTTPX to pure dict with lowercase keys.

    Note:
        Concatenate headers into a single comma separated value when a key occurs multiple times.
    """
    return {key.lower(): value for key, value in headers.items()}


def _parse_response(response: httpx.Response) -> Response:
    content = response.content
    content_type = response.headers.get('content-type')
    if content_type and 'application/json' in content_type.lower():
        content = from_json(response.content)

    return Response(
        success=True,
        status_code=response.status_code,
        content=content,
        headers=_convert_headers_to_dict(response.headers),
    )


def _handle_request_errors(exception: Exception) -> None:
    try:
        raise exception
    except httpx.TimeoutException as e:
        raise exceptions.InvokeTimeoutError from e
    except httpx.NetworkError as e:
        raise exceptions.NetworkError from e
    # TODO(MarshalX): add more exceptions


def _handle_response(response: httpx.Response) -> httpx.Response:
    if 200 <= response.status_code <= 299:
        return response

    error_response = Response(
        success=False,
        status_code=response.status_code,
        content=response.content,
        headers=_convert_headers_to_dict(response.headers),
    )
    error_content = load_json(response.content, strict=False)
    if error_content:
        error_response.content = t.cast('XrpcError', get_or_create(error_content, XrpcError, strict=False))

    if response.status_code in {401, 403}:
        raise exceptions.UnauthorizedError(error_response)
    if response.status_code == 400:
        raise exceptions.BadRequestError(error_response)
    if response.status_code in {409, 413, 502}:
        raise exceptions.NetworkError(error_response)

    raise exceptions.RequestException(error_response)


class RequestBase:
    _MANDATORY_HEADERS: t.ClassVar[t.Dict[str, str]] = {'User-Agent': _ATPROTO_SDK_USER_AGENT}

    def __init__(self) -> None:
        self._additional_headers: t.Dict[str, str] = {}
        self._additional_header_sources: t.List[t.Callable[[], t.Dict[str, str]]] = []

    def get_headers(self, additional_headers: t.Optional[t.Dict[str, str]] = None) -> t.Dict[str, str]:
        """Get headers for the request.

        Args:
            additional_headers: Additional headers.
                Overrides existing headers with the same name.

        Returns:
            Headers for the request.
        """
        # The order of calling `.update()` matters. It defines the priority of overriding.
        headers_lower = {
            **_normalize_headers(RequestBase._MANDATORY_HEADERS),
            **_normalize_headers(self._additional_headers),
        }

        for header_source in self._additional_header_sources:
            headers_lower.update(_normalize_headers(header_source()))

        if additional_headers:
            headers_lower.update(_normalize_headers(additional_headers))

        return _denormalize_headers(headers_lower)

    def set_additional_headers(self, headers: t.Dict[str, str]) -> None:
        """Set additional headers for the request.

        Args:
            headers: Additional headers.
        """
        self._additional_headers = headers.copy()

    def add_additional_headers_source(self, callback: t.Callable[[], t.Dict[str, str]]) -> None:
        """Add additional headers for the request.

        Args:
            callback: Function to get additional headers.
        """
        self._additional_header_sources.append(callback)

    def add_additional_header(self, header_name: str, header_value: str) -> None:
        """Add additional headers for the request.

        Note:
            This method overrides the existing header with the same name.

        Args:
            header_name: Header name.
            header_value: Header value.
        """
        self._additional_headers[header_name] = header_value

    def clone(self) -> te.Self:
        """Clone the client instance.

        Used to customize atproto proxy and set of labeler services.

        Returns:
            Cloned client instance.
        """
        cloned_request = type(self)()

        cloned_request._additional_headers = self._additional_headers.copy()
        cloned_request._additional_header_sources = self._additional_header_sources.copy()

        return cloned_request


class Request(RequestBase):
    """Class for handling requests errors and working with httpx.

    Args:
        **kwargs: Additional parameters for httpx.Client.
    """

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__()
        self._client = httpx.Client(follow_redirects=True, **kwargs)

    def _send_request(self, method: str, url: str, **kwargs: t.Any) -> httpx.Response:
        headers = self.get_headers(kwargs.pop('headers', None))

        try:
            response = self._client.request(method=method, url=url, headers=headers, **kwargs)
            return _handle_response(response)
        except Exception as e:
            _handle_request_errors(e)
            raise e

    def close(self) -> None:
        self._client.close()

    def get(self, *args: t.Any, **kwargs: t.Any) -> Response:
        return _parse_response(self._send_request('GET', *args, **kwargs))

    def post(self, *args: t.Any, **kwargs: t.Any) -> Response:
        return _parse_response(self._send_request('POST', *args, **kwargs))


class AsyncRequest(RequestBase):
    """Class for handling requests errors and working with httpx.

    Args:
        **kwargs: Additional parameters for httpx.AsyncClient.
    """

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__()
        self._client = httpx.AsyncClient(follow_redirects=True, **kwargs)

    async def _send_request(self, method: str, url: str, **kwargs: t.Any) -> httpx.Response:
        headers = self.get_headers(kwargs.pop('headers', None))

        try:
            response = await self._client.request(method=method, url=url, headers=headers, **kwargs)
            return _handle_response(response)
        except Exception as e:
            _handle_request_errors(e)
            raise e

    async def close(self) -> None:
        await self._client.aclose()

    async def get(self, *args: t.Any, **kwargs: t.Any) -> Response:
        return _parse_response(await self._send_request('GET', *args, **kwargs))

    async def post(self, *args: t.Any, **kwargs: t.Any) -> Response:
        return _parse_response(await self._send_request('POST', *args, **kwargs))

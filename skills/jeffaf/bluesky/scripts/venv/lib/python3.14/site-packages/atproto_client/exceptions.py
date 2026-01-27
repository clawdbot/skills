import typing as t

from atproto_core.exceptions import AtProtocolError

if t.TYPE_CHECKING:
    from atproto_client.request import Response


_DEFAULT_LOGING_REQUIRED_ERROR_MESSAGE = 'To perform this action, you must be logged in. Use the `login` method first.'


class ModelError(AtProtocolError): ...


class ModelFieldNotFoundError(ModelError): ...


class RequestErrorBase(AtProtocolError):
    def __init__(self, response: t.Optional['Response'] = None) -> None:
        self.response: t.Optional['Response'] = response


class NetworkError(RequestErrorBase): ...


class InvokeTimeoutError(NetworkError): ...


class UnauthorizedError(RequestErrorBase): ...


class RequestException(RequestErrorBase): ...


class BadRequestError(RequestErrorBase): ...


class LoginRequiredError(AtProtocolError):
    def __init__(self, message: t.Optional[str] = _DEFAULT_LOGING_REQUIRED_ERROR_MESSAGE) -> None:
        super().__init__(message)

import base64
import typing as t


def force_bytes(value: t.Union[bytes, str]) -> bytes:
    if isinstance(value, str):
        return value.encode('UTF-8')

    return value


def base64url_decode(input_data: t.Union[bytes, str]) -> bytes:
    input_bytes = force_bytes(input_data)

    rem = len(input_bytes) % 4

    if rem > 0:
        input_bytes += b'=' * (4 - rem)

    return base64.urlsafe_b64decode(input_bytes)


def base64url_encode(input_data: bytes) -> bytes:
    return base64.urlsafe_b64encode(input_data).replace(b'=', b'')

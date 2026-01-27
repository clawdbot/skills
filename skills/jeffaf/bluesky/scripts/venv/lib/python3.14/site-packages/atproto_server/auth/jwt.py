import binascii
import typing as t
from datetime import datetime, timezone

from atproto_crypto.verify import verify_signature
from pydantic import BaseModel, ConfigDict
from pydantic_core import from_json

from atproto_server.auth.utils import base64url_decode
from atproto_server.exceptions import (
    TokenDecodeError,
    TokenExpiredSignatureError,
    TokenImmatureSignatureError,
    TokenInvalidAudienceError,
    TokenInvalidIssuedAtError,
    TokenInvalidSignatureError,
)

GetSigningKeyCallback = t.Callable[[str, bool], str]
GetSigningKeyCallbackAsync = t.Callable[[str, bool], t.Coroutine[t.Any, t.Any, str]]


class JwtPayload(BaseModel):
    """The payload of the JWT.

    Based on https://www.rfc-editor.org/rfc/rfc7519#section-4.1
    """

    model_config = ConfigDict(extra='allow', strict=True)

    iss: t.Optional[str] = None  #: Issuer (DID).
    sub: t.Optional[str] = None  #: Subject (DID).
    aud: t.Optional[t.Union[str, t.List[str]]] = None  #: Audience (DID).
    jti: t.Optional[str] = None  #: JWT ID. Presented in Refresh Token.
    nbf: t.Optional[int] = None  #: Not Before. Not used by ATProto.
    exp: t.Optional[int] = None  #: Expiration Time.
    iat: t.Optional[int] = None  #: Issued At.
    scope: t.Optional[str] = None  #: Scope. ATProto specific.
    # ... any other JWT Claim Set member.


def parse_jwt(jwt: t.Union[str, bytes]) -> t.Tuple[bytes, bytes, t.Dict[str, t.Any], bytes]:
    """Parse the given JWT.

    Args:
        jwt: The JWT to parse.

    Returns:
        :obj:`tuple` of :obj:`bytes`, :obj:`bytes`, :obj:`dict`, :obj:`bytes`:
        The parsed JWT: payload, signing input, header, signature.
    """
    if isinstance(jwt, str):
        jwt = jwt.encode('UTF-8')

    try:
        signing_input, crypto_segment = jwt.rsplit(b'.', 1)
        header_segment, payload_segment = signing_input.split(b'.', 1)
    except ValueError as e:
        raise TokenDecodeError('Not enough segments') from e

    try:
        header_data = base64url_decode(header_segment)
    except (TypeError, binascii.Error) as e:
        raise TokenDecodeError('Invalid header padding') from e

    try:
        header = from_json(header_data)
    except ValueError as e:
        raise TokenDecodeError(f'Invalid header string: {e}') from e

    if not isinstance(header, dict):
        raise TokenDecodeError('Invalid header string: must be a json object')

    header = t.cast('t.Dict[str, t.Any]', from_json(header_data))  # we expect an object in header

    try:
        payload = base64url_decode(payload_segment)
    except (TypeError, binascii.Error) as e:
        raise TokenDecodeError('Invalid payload padding') from e

    try:
        signature = base64url_decode(crypto_segment)
    except (TypeError, binascii.Error) as e:
        raise TokenDecodeError('Invalid crypto padding') from e

    return payload, signing_input, header, signature


def decode_jwt_payload(payload: t.Union[str, bytes]) -> JwtPayload:
    """Decode the given JWT payload.

    Args:
        payload: The JWT payload to decode.

    Returns:
        :obj:`JwtPayload`: The decoded payload of the given JWT.
    """
    try:
        plain_payload = from_json(payload)
    except ValueError as e:
        raise TokenDecodeError(f'Invalid payload string: {e}') from e
    if not isinstance(plain_payload, dict):
        raise TokenDecodeError('Invalid payload string: must be a json object')

    try:
        return JwtPayload(**plain_payload)  # type: ignore  # noqa: PGH003
    except Exception as e:
        raise TokenDecodeError(f'Invalid payload string: {e}') from e


def get_jwt_payload(jwt: str) -> JwtPayload:
    """Return the payload of the given JWT.

    Args:
        jwt: The JWT to get the payload from.

    Returns:
        :obj:`JwtPayload`: The payload of the given JWT.
    """
    payload, *_ = parse_jwt(jwt)
    return decode_jwt_payload(payload)


def _validate_exp(
    exp: int,
    now: float,
    leeway: float,
) -> None:
    try:
        exp = int(exp)
    except ValueError as e:
        raise TokenDecodeError('Expiration Time claim (exp) must be an integer.') from e

    if exp <= (now - leeway):
        raise TokenExpiredSignatureError('Signature has expired')


def _validate_iat(
    iat: int,
    now: float,
    leeway: float,
) -> None:
    try:
        iat = int(iat)
    except ValueError as e:
        raise TokenInvalidIssuedAtError('Issued At claim (iat) must be an integer.') from e
    if iat > (now + leeway):
        raise TokenImmatureSignatureError('The token is not yet valid (iat)')


def validate_jwt_payload(payload: JwtPayload, leeway: int = 0) -> None:
    """Validate the given JWT payload.

    Args:
        payload: The JWT payload to validate.
        leeway: The leeway in seconds to accept when verifying time claims (exp, iat).

    Returns:
        :obj:`None`: The payload is valid.

    Raises:
        TokenDecodeError: If the given JWT is invalid.
        TokenExpiredSignatureError: If the given JWT is expired.
        TokenImmatureSignatureError: If the given JWT is immature.
        TokenInvalidIssuedAtError: If the given JWT has invalid issued at.
    """
    now = datetime.now(tz=timezone.utc).timestamp()

    if payload.exp is not None:
        _validate_exp(payload.exp, now, leeway)
    if payload.iat is not None:
        _validate_iat(payload.iat, now, leeway)


def _verify_signature(signing_key: str, signing_input: bytes, signature: bytes) -> bool:
    try:
        return verify_signature(signing_key, signing_input, signature)
    except Exception as e:
        raise TokenInvalidSignatureError('Could not verify JWT signature') from e


def verify_jwt(
    jwt: str, get_signing_key_callback: GetSigningKeyCallback, own_did: t.Optional[str] = None, leeway: int = 0
) -> JwtPayload:
    """Verify the given JWT.

    Args:
        jwt: The JWT to verify.
        get_signing_key_callback: The callback to get the signing key.
        own_did: The DID of the service (aud).
        leeway: The leeway in seconds to accept when verifying time claims (exp, iat).

    Returns:
        :obj:`JwtPayload`: The payload of the given JWT.

    Raises:
        TokenDecodeError: If the given JWT is invalid.
        TokenExpiredSignatureError: If the given JWT is expired.
        TokenImmatureSignatureError: If the given JWT is immature.
        TokenInvalidAudienceError: If the given JWT has invalid audience.
        TokenInvalidIssuedAtError: If the given JWT has invalid issued at.
        TokenInvalidSignatureError: If the given JWT has invalid signature.
    """
    plain_payload, signing_input, _, signature = parse_jwt(jwt)

    payload = decode_jwt_payload(plain_payload)
    validate_jwt_payload(payload, leeway)

    if own_did and payload.aud != own_did:
        raise TokenInvalidAudienceError('Invalid subject')

    if payload.iss is None:
        raise TokenDecodeError('Invalid payload. Expected not None iss')

    signing_key = get_signing_key_callback(payload.iss, False)
    if _verify_signature(signing_key, signing_input, signature):
        return payload

    fresh_signing_key = get_signing_key_callback(payload.iss, True)  # get signing key without a cache
    if fresh_signing_key == signing_key:
        raise TokenInvalidSignatureError('Invalid signature even with fresh signing key it is equal to the old one)')

    if _verify_signature(fresh_signing_key, signing_input, signature):
        return payload

    # this code should be unreachable
    # verifying methods must raise exception before
    raise TokenInvalidSignatureError('Invalid signature')


async def verify_jwt_async(
    jwt: str, get_signing_key_callback: GetSigningKeyCallbackAsync, own_did: t.Optional[str] = None, leeway: int = 0
) -> JwtPayload:
    """Asynchronously verifies the given JWT.

    Args:
        jwt: The JWT to verify.
        get_signing_key_callback: The callback to get the signing key.
        own_did: The DID of the service (aud).
        leeway: The leeway in seconds to accept when verifying time claims (exp, iat).

    Returns:
        :obj:`JwtPayload`: The payload of the given JWT.

    Raises:
        TokenDecodeError: If the given JWT is invalid.
        TokenExpiredSignatureError: If the given JWT is expired.
        TokenImmatureSignatureError: If the given JWT is immature.
        TokenInvalidAudienceError: If the given JWT has invalid audience.
        TokenInvalidIssuedAtError: If the given JWT has invalid issued at.
        TokenInvalidSignatureError: If the given JWT has invalid signature.
    """
    plain_payload, signing_input, _, signature = parse_jwt(jwt)

    payload = decode_jwt_payload(plain_payload)
    validate_jwt_payload(payload, leeway)

    if own_did and payload.aud != own_did:
        raise TokenInvalidAudienceError('Invalid subject')

    if payload.iss is None:
        raise TokenDecodeError('Invalid payload. Expected not None iss')

    signing_key = await get_signing_key_callback(payload.iss, False)
    if _verify_signature(signing_key, signing_input, signature):
        return payload

    fresh_signing_key = await get_signing_key_callback(payload.iss, True)  # get signing key without a cache
    if fresh_signing_key == signing_key:
        raise TokenInvalidSignatureError('Invalid signature even with fresh signing key it is equal to the old one)')

    if _verify_signature(fresh_signing_key, signing_input, signature):
        return payload

    # this code should be unreachable
    # verifying methods must raise exception before
    raise TokenInvalidSignatureError('Invalid signature')

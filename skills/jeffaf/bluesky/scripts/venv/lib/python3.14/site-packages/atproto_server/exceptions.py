from atproto_core.exceptions import AtProtocolError


class InvalidTokenError(AtProtocolError):
    pass


class TokenDecodeError(InvalidTokenError):
    pass


class TokenInvalidSignatureError(TokenDecodeError):
    pass


class TokenInvalidAudienceError(InvalidTokenError):
    pass


class TokenExpiredSignatureError(InvalidTokenError):
    pass


class TokenInvalidIssuedAtError(InvalidTokenError):
    pass


class TokenImmatureSignatureError(InvalidTokenError):
    pass

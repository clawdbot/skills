from atproto_core.exceptions import AtProtocolError


class FirehoseError(AtProtocolError): ...


class FirehoseDecodingError(FirehoseError): ...

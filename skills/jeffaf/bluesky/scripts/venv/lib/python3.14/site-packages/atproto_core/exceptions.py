class AtProtocolError(Exception):
    """Base exception."""


class InvalidNsidError(AtProtocolError): ...


class InvalidAtUriError(AtProtocolError): ...


class InvalidCARFile(AtProtocolError): ...


class DAGCBORDecodingError(AtProtocolError): ...

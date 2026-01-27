from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from atproto_client.models.utils import get_or_create
from atproto_core.cbor import decode_dag_multi
from atproto_core.exceptions import AtProtocolError

from atproto_firehose.exceptions import FirehoseDecodingError


class FrameType(Enum):
    """Type of frame."""

    MESSAGE = 1
    ERROR = -1

    @classmethod
    def has_value(cls, value: int) -> bool:
        return value in cls._value2member_map_


@dataclass
class MessageFrameHeader:
    """Header of the message frame."""

    op: FrameType = FrameType.MESSAGE  #: Operation. For Message header is :obj:`FrameType.MESSAGE` always.
    t: Optional[str] = None  #: Type of body content.


@dataclass
class ErrorFrameHeader:
    """Header of the error frame."""

    op: FrameType = FrameType.ERROR  #: Operation. For Error header is :obj:`FrameType.ERROR` always.


#: Base frame header.
FrameHeader = Union[MessageFrameHeader, ErrorFrameHeader]


@dataclass
class ErrorFrameBody:
    """Body of error frame."""

    error: str  #: Code of the error.
    message: Optional[str] = None  #: Description of the error.


def parse_frame_header(raw_header: dict) -> FrameHeader:
    try:
        header_op = int(raw_header.get('op', 0))
        if not FrameType.has_value(header_op):
            raise FirehoseDecodingError('Invalid frame type')

        frame_type = FrameType(header_op)
        if frame_type is FrameType.MESSAGE:
            return get_or_create(raw_header, MessageFrameHeader)
        return get_or_create(raw_header, ErrorFrameHeader)
    except (ValueError, AtProtocolError) as e:
        raise FirehoseDecodingError('Invalid frame header') from e


def parse_frame(header: FrameHeader, raw_body: dict) -> Union['ErrorFrame', 'MessageFrame']:
    try:
        if isinstance(header, ErrorFrameHeader):
            body = get_or_create(raw_body, ErrorFrameBody)
            return ErrorFrame(header, body)
        if isinstance(header, MessageFrameHeader):
            return MessageFrame(header, raw_body)
        raise FirehoseDecodingError('Invalid frame type')
    except AtProtocolError as e:
        raise FirehoseDecodingError('Invalid frame body') from e


@dataclass
class Frame:
    """Firehose base frame."""

    header: Union[MessageFrameHeader, ErrorFrameHeader]  #: Header.
    body: Union[ErrorFrameBody, dict]  #: Body

    @property
    def operation(self) -> FrameType:
        """:obj:`FrameType`: Frame operation (frame type)."""
        return self.header.op

    @property
    def is_message(self) -> bool:
        """:obj:`bool`: Is frame the MessageFrame."""
        return self.operation is FrameType.MESSAGE

    @property
    def is_error(self) -> bool:
        """:obj:`bool`: Is frame the ErrorFrame."""
        return self.operation is FrameType.ERROR

    @staticmethod
    def from_bytes(data: Union[bytes, bytearray]) -> Union['MessageFrame', 'ErrorFrame']:
        """Decode frame from bytes of stream of bytes.

        Args:
            data: Bytes or stream of bytes of frame.

        Returns:
            :obj:`atproto.firehose_models.MessageFrame` or :obj:`atproto.firehose_models.ErrorFrame`

        Raises:
            :class:`atproto.exceptions.FirehoseError`: Invalid data frame.
        """
        decoded_parts = decode_dag_multi(data)
        if len(decoded_parts) > 2:
            raise FirehoseDecodingError('Too many CBOR data parts in the frame')
        if not len(decoded_parts):
            raise FirehoseDecodingError('Invalid frame without CBOR data')

        raw_header = decoded_parts[0]

        raw_body = None
        if len(decoded_parts) > 1:
            raw_body = decoded_parts[1]

        if raw_body is None:
            raise FirehoseDecodingError('Frame body not found')

        header = parse_frame_header(raw_header)
        return parse_frame(header, raw_body)


@dataclass
class MessageFrame(Frame):
    """Firehose message frame."""

    header: MessageFrameHeader  #: Header.
    body: dict  #: Body.

    @property
    def type(self) -> str:
        """:obj:`str`: Type of body."""
        return self.header.t


@dataclass
class ErrorFrame(Frame):
    """Firehose error frame."""

    header: ErrorFrameHeader  #: Header.
    body: ErrorFrameBody  #: Body.

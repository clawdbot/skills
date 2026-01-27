import re
import typing as t
from dataclasses import dataclass, field

from atproto_core.exceptions import InvalidNsidError

_NSID_DELIM = '.'
_NSID_NAMESPACE = '*'

_MAX_NSID_LEN = 253 + 1 + 63
_MAX_NSID_PART_LEN = 63
_MIN_NSID_PART_LEN = 1
_MIN_NSID_SEGMENTS_COUNT = 3

_NSID_VALID_CHARS_REGEX = r'^[a-zA-Z0-9.-]*$'
_NSID_FIRST_SEGMENT_NO_LEADING_DIGIT_REGEX = r'^[0-9]'
_NSID_LAST_SEGMENT_REGEX = r'^[a-zA-Z][a-zA-Z0-9]*$'

_NSID_PART_FORBIDDEN_START = '-'
_NSID_PART_FORBIDDEN_END = '-'

Segments = t.List[str]


@dataclass
class NSID:
    """NameSpaced IDs (NSIDs).

    Examples:
        com.example.status

        io.social.getFeed

        net.users.bob.ping
    """

    segments: Segments = field(default_factory=list)

    @classmethod
    def from_str(cls, nsid: str) -> 'NSID':
        """Create `NSID` instance from string."""
        validate_nsid(nsid)
        return cls(segments=get_nsid_segments(nsid))

    @property
    def authority(self) -> str:
        """Get authority of NSID.

        com.example.thing
        ^^^^^^^^^^^--------> example.com

        delim joined self.segments[:-1][::-1]
        """
        segments_without_name = self.segments[:-1]
        segments_without_name.reverse()

        return _NSID_DELIM.join(segments_without_name)

    @property
    def name(self) -> str:
        """Get name."""
        return self.segments[-1]

    def __str__(self) -> str:
        return _NSID_DELIM.join(self.segments)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, NSID):
            return hash(self) == hash(other)

        return False


def get_nsid_segments(nsid: str) -> Segments:
    return nsid.split('.')


def _exclude_nsid_namespace_if_exists(segments: Segments) -> str:
    last_segment = segments[-1]

    if last_segment == _NSID_NAMESPACE:
        segments = segments[:-1]

    return _NSID_DELIM.join(segments)


def _validate_nsid_segment(segment: str, is_first_segment: bool, is_last_segment: bool) -> bool:
    """Validate NSID segment.

    Args:
        segment: Segment to validate.
        is_first_segment: The first segment indicator.
        is_last_segment: The last segment indicator.

    Returns:
        :obj:`bool`: The validation result is always True.

    Raises:
        :class:`atproto.exceptions.InvalidNsidError`: Invalid NSID exception.
    """
    segment_len = len(segment)
    if segment_len < _MIN_NSID_PART_LEN:
        raise InvalidNsidError(f'NSID segment is too short. Min len: {_MIN_NSID_PART_LEN}')
    if segment_len > _MAX_NSID_PART_LEN:
        raise InvalidNsidError(f'NSID segment is too long. Max len: {_MAX_NSID_PART_LEN}')

    if segment.startswith(_NSID_PART_FORBIDDEN_START):
        raise InvalidNsidError(f'NSID segment cannot start with {_NSID_PART_FORBIDDEN_START}')
    if segment.endswith(_NSID_PART_FORBIDDEN_END):
        raise InvalidNsidError(f'NSID segment cannot end with {_NSID_PART_FORBIDDEN_END}')

    if is_first_segment and re.search(_NSID_FIRST_SEGMENT_NO_LEADING_DIGIT_REGEX, segment):
        raise InvalidNsidError('NSID first segment cannot start with a digit')

    if is_last_segment and not re.search(_NSID_LAST_SEGMENT_REGEX, segment):
        raise InvalidNsidError('NSID final segments must start with a letter and contain only letters and digits')

    return True


def _validate_nsid(nsid: str) -> bool:
    """Validate NSID.

    Args:
        nsid: NSID to validate.

    Returns:
        :obj:`bool`: Validation result is always True.

    Raises:
        :class:`atproto.exceptions.InvalidNsidError`: Invalid NSID exception.
    """
    if len(nsid) > _MAX_NSID_LEN:
        raise InvalidNsidError(f'NSID is too long. Max len: {_MAX_NSID_LEN}')
    if not re.search(_NSID_VALID_CHARS_REGEX, nsid):
        raise InvalidNsidError('NSID contains invalid chars. Only letters, digits, dots, and hyphens are allowed')

    segments = get_nsid_segments(nsid)
    if len(segments) < _MIN_NSID_SEGMENTS_COUNT:
        raise InvalidNsidError(f'NSID must contains at least {_MIN_NSID_SEGMENTS_COUNT} segments')

    segments_count = len(segments)
    for segment_index, segment in enumerate(segments):
        is_first_segment = segment_index == 0
        is_last_segment = segment_index + 1 == segments_count
        _validate_nsid_segment(segment, is_first_segment, is_last_segment)

    return True


def validate_nsid(nsid: str, *, soft_fail: bool = False) -> bool:
    """Validate NSID.

    Args:
        nsid: NSID to validate.
        soft_fail: enable to return False on fall instead of exception

    Returns:
        :obj:`bool`: Validation result.

    Raises:
        :class:`atproto.exceptions.InvalidNsidError`: Invalid NSID exception.
    """
    try:
        return _validate_nsid(nsid)
    except InvalidNsidError as e:
        if soft_fail:
            return False

        raise e

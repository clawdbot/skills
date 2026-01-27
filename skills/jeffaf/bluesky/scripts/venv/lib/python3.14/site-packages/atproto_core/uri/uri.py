import re
import typing as t
import urllib.parse as urlparse
from urllib.parse import urlencode

from atproto_core.exceptions import InvalidAtUriError

# ref: https://github.com/bluesky-social/atproto/blob/a4af3494bd8263187bb3450193bcd2467ae6b788/packages/syntax/src/aturi.ts#L5C5-L5C98
_ATP_URI_REGEX = r'^(at:\/\/)?((?:did:[a-z0-9:%-]+)|(?:[a-z0-9][a-z0-9.:-]*))(\/[^?#\s]*)?(\?[^#\s]+)?(#[^\s]+)?$'
_ATP_RELATIVE_URI_REGEX = r'^(\/[^?#\s]*)?\?([^#\s]+)?(#[^\s]+)?$'  # modified to not include "?" in a group


class AtUri:
    """ATP URI Scheme.

    Examples:
        Repository: at://alice.host.com

        Repository: at://did:plc:bv6ggog3tya2z3vxsub7hnal

        Collection: at://alice.host.com/io.example.song

        Record: at://alice.host.com/io.example.song/3yI5-c1z-cc2p-1a

        Record Field: at://alice.host.com/io.example.song/3yI5-c1z-cc2p-1a#/title
    """

    def __init__(
        self,
        host: str,
        pathname: str = '',
        hash_: str = '',
        search_params: t.Optional[t.List[t.Tuple[str, t.Any]]] = None,
    ) -> None:
        if search_params is None:
            search_params = []

        if hash_ and not pathname:
            raise InvalidAtUriError('`hash_` cannot be set without `pathname`')
        if search_params and not pathname:
            raise InvalidAtUriError('`search_params` cannot be set without `pathname`')

        self.host = host
        self.pathname = pathname
        self.hash = hash_
        self.search_params = search_params

    @property
    def protocol(self) -> str:
        """Get protocol."""
        return 'at://'

    @property
    def origin(self) -> str:
        """Get origin."""
        return f'at://{self.host}'

    @property
    def hostname(self) -> str:
        """Get hostname."""
        return self.host

    @property
    def collection(self) -> str:
        """Get collection name."""
        for part in self.pathname.split('/'):
            if part:
                return part

        return ''

    @property
    def rkey(self) -> str:
        """Get record key (rkey)."""
        parts = [p for p in self.pathname.split('/') if p]
        if len(parts) > 1:
            return parts[1]

        return ''

    @property
    def http(self) -> str:
        """Convert instance to HTTP URI."""
        return str(self)

    @property
    def search(self) -> str:
        """Get search params."""
        return urlencode(self.search_params)

    @classmethod
    def make(cls, handle_or_did: str, collection: t.Optional[str] = None, rkey: t.Optional[str] = None) -> 'AtUri':
        """Create `AtUri` instance from handle or DID."""
        uri = handle_or_did

        if collection:
            uri = f'{handle_or_did}/{collection}'
        if rkey:
            uri = f'{uri}/{rkey}'

        return cls.from_str(uri)

    @classmethod
    def from_str(cls, uri: str) -> 'AtUri':
        """Create `AtUri` instance from URI."""
        groups = re.findall(_ATP_URI_REGEX, uri, re.IGNORECASE)
        if not groups:
            raise InvalidAtUriError

        group = groups[0]
        search_params = urlparse.parse_qsl(group[3] or '')
        return cls(host=group[1] or '', pathname=group[2] or '', hash_=group[4] or '', search_params=search_params)

    @classmethod
    def from_relative_str(cls, base: str, uri: str) -> 'AtUri':
        """Create `AtUri` instance from relative URI."""
        groups = re.findall(_ATP_RELATIVE_URI_REGEX, uri, re.IGNORECASE)
        if not groups:
            raise InvalidAtUriError

        group = groups[0]
        search_params = urlparse.parse_qsl(group[1] or '')
        return cls(host=base, pathname=group[0] or '', hash_=group[2] or '', search_params=search_params)

    def __str__(self) -> str:
        path = self.pathname or '/'
        if not path.startswith('/'):
            path = f'/{path}'

        query = urlencode(self.search_params)
        if query:
            query = f'?{query}'

        hash_ = self.hash
        if hash_ and not hash_.startswith('#'):
            hash_ = f'#{hash_}'

        return f'at://{self.host}{path}{query}{hash_}'

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, AtUri):
            return hash(self) == hash(other)

        return False

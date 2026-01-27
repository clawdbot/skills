import typing as t
from io import BytesIO

from atproto_client import models

_FEATURES_TYPE = t.List[
    t.Union[
        'models.AppBskyRichtextFacet.Mention',
        'models.AppBskyRichtextFacet.Link',
        'models.AppBskyRichtextFacet.Tag',
    ]
]


class TextBuilder:
    """Helper that helps construct rich text.

    There are three facets: link, mention, tag.

    Each facet could be linked to text segment.

    This helper provides chained API.

    Example:
        Without chaining:

        >>> from atproto import client_utils
        >>> text_builder = client_utils.TextBuilder()
        >>> text_builder.tag('This is a rich message. ', 'atproto')
        >>> text_builder.text('I can mention ')
        >>> text_builder.mention('account', 'did:plc:kvwvcn5iqfooopmyzvb4qzba')
        >>> text_builder.text(' and add clickable ')
        >>> text_builder.link('link', 'https://atproto.blue/')

        With chaining:

        >>> from atproto import client_utils
        >>> text_builder = client_utils.TextBuilder().text('Test msg using ').link('Python SDK', 'https://atproto.blue/')

        Later you can use this builder in the Client:

        >>> from atproto import Client, client_utils
        >>> client = Client()
        >>> # You can pass instance of TextBuilder instead of str to the "text" argument.
        >>> client.send_post(client_utils.TextBuilder().link('Python SDK', 'https://atproto.blue/'))
        >>> # Same with send_image method

    Note:
        This helper doesn't support overlapped features (features at the same byte range).
    """

    def __init__(self) -> None:
        self._buffer = BytesIO()
        self._facets: t.List[models.AppBskyRichtextFacet.Main] = []

    @property
    def __tell(self) -> int:
        return self._buffer.tell()

    _start_index = __tell
    _end_index = __tell

    def _write_text(self, text: str) -> t.Tuple[int, int]:
        start_index = self._start_index
        self._write_bytes(text.encode('UTF-8'))
        end_index = self._end_index
        return start_index, end_index

    def _write_bytes(self, data: bytes) -> int:
        return self._buffer.write(data)

    def _add_facet(self, facet: models.AppBskyRichtextFacet.Main) -> None:
        self._facets.append(facet)

    def _create_byte_slice(self, text: str) -> models.AppBskyRichtextFacet.ByteSlice:
        start, end = self._write_text(text)
        return models.AppBskyRichtextFacet.ByteSlice(byte_start=start, byte_end=end)

    def _create_facet(self, text: str, features: _FEATURES_TYPE) -> models.AppBskyRichtextFacet.Main:
        return models.AppBskyRichtextFacet.Main(
            features=features,
            index=self._create_byte_slice(text),
        )

    def build_facets(self) -> t.List[models.AppBskyRichtextFacet.Main]:
        """Build facets from the current state of the builder."""
        return self._facets.copy()

    def build_text(self) -> str:
        """Build text from the current state of the builder."""
        return self._buffer.getvalue().decode()

    def text(self, text: str) -> 'TextBuilder':
        """Add text to the builder.

        Args:
            text: Text.
        """
        self._write_text(text)
        return self

    def link(self, text: str, url: str) -> 'TextBuilder':
        """Add link to the builder.

        Args:
            text: Text of the link.
            url: Valid URL. For example, https://atproto.blue/
        """
        self._add_facet(self._create_facet(text, [models.AppBskyRichtextFacet.Link(uri=url)]))
        return self

    def mention(self, text: str, did: str) -> 'TextBuilder':
        """Add mention to the builder.

        Args:
            text: Text of the mention.
            did: Valid DID. For example, did:plc:kvwvcn5iqfooopmyzvb4qzba
        """
        self._add_facet(self._create_facet(text, [models.AppBskyRichtextFacet.Mention(did=did)]))
        return self

    def tag(self, text: str, tag: str) -> 'TextBuilder':
        """Add tag to the builder.

        Args:
            text: Text of the tag.
            tag: Hashtag.
        """
        self._add_facet(self._create_facet(text, [models.AppBskyRichtextFacet.Tag(tag=tag)]))
        return self

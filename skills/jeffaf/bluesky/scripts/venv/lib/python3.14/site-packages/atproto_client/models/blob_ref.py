import typing as t

import typing_extensions as te
from atproto_core.cid import CID
from pydantic import BaseModel, ConfigDict, Field


class IpldLink(BaseModel):
    """CID representation in JSON."""

    model_config = ConfigDict(extra='allow', populate_by_name=True, strict=True)

    link: str = Field(alias='$link')  #: CID.


class BlobRef(BaseModel):
    """Blob reference."""

    model_config = ConfigDict(extra='allow', populate_by_name=True, strict=True)

    mime_type: str = Field(alias='mimeType')  #: Mime type.
    size: int  #: Size in bytes.
    ref: t.Union[str, bytes, IpldLink]  #: CID.

    py_type: te.Literal['blob'] = Field(default='blob', alias='$type')

    @property
    def cid(self) -> 'CID':
        """Get CID."""
        if self.is_bytes_representation:
            return CID.decode(self.ref)

        return CID.decode(self.ref.link)

    @property
    def is_json_representation(self) -> bool:
        """Check if it is JSON representation.

        Returns:
            True if it is JSON representation.
        """
        return isinstance(self.ref, IpldLink)

    @property
    def is_bytes_representation(self) -> bool:
        """Check if it is bytes representation.

        Returns:
            True if it is bytes representation.
        """
        return isinstance(self.ref, (str, bytes))

    def to_json_representation(self) -> 'BlobRef':
        """Get JSON representation.

        Note:
            Used in XRPC, etc. where JSON is used.

        Warning:
            It returns new instance.

        Returns:
            BlobRef in JSON representation.
        """
        if self.is_json_representation:
            return BlobRef(mime_type=self.mime_type, size=self.size, ref=IpldLink(link=self.ref.link))

        return BlobRef(mime_type=self.mime_type, size=self.size, ref=IpldLink(link=self.ref))

    def to_bytes_representation(self) -> 'BlobRef':
        """Get bytes representation.

        Note:
            Used in Firehose, CAR, etc. where bytes are possible.

        Warning:
            It returns new instance.

        Returns:
            BlobRef in bytes representation.
        """
        if self.is_bytes_representation:
            return BlobRef(mime_type=self.mime_type, size=self.size, ref=self.ref)

        return BlobRef(mime_type=self.mime_type, size=self.size, ref=self.ref.link)

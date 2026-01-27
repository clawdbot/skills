##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
    from atproto_client.models.blob_ref import BlobRef
from atproto_client.models import base


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.feed.generator`."""

    created_at: string_formats.DateTime  #: Created at.
    did: string_formats.Did  #: Did.
    display_name: str = Field(max_length=240)  #: Display name.
    accepts_interactions: t.Optional[bool] = (
        None  #: Declaration that a feed accepts feedback interactions from a client through app.bsky.feed.sendInteractions.
    )
    avatar: t.Optional['BlobRef'] = None  #: Avatar.
    content_mode: t.Optional[
        t.Union['models.AppBskyFeedDefs.ContentModeUnspecified', 'models.AppBskyFeedDefs.ContentModeVideo', str]
    ] = None  #: Content mode.
    description: te.Annotated[t.Optional[str], Field(max_length=3000)] = None  #: Description.
    description_facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None  #: Description facets.
    labels: t.Optional[
        te.Annotated[t.Union['models.ComAtprotoLabelDefs.SelfLabels'], Field(discriminator='py_type')]
    ] = None  #: Self-label values.

    py_type: t.Literal['app.bsky.feed.generator'] = Field(default='app.bsky.feed.generator', alias='$type', frozen=True)


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyFeedGenerator.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyFeedGenerator.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyFeedGenerator.Record`."""

    records: t.Dict[str, 'models.AppBskyFeedGenerator.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyFeedGenerator.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

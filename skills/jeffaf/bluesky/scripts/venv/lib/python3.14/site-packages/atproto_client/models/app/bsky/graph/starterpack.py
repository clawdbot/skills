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
from atproto_client.models import base


class FeedItem(base.ModelBase):
    """Definition model for :obj:`app.bsky.graph.starterpack`."""

    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.graph.starterpack#feedItem'] = Field(
        default='app.bsky.graph.starterpack#feedItem', alias='$type', frozen=True
    )


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.graph.starterpack`."""

    created_at: string_formats.DateTime  #: Created at.
    list: string_formats.AtUri  #: Reference (AT-URI) to the list record.
    name: str = Field(min_length=1, max_length=500)  #: Display name for starter pack; can not be empty.
    description: te.Annotated[t.Optional[str], Field(max_length=3000)] = None  #: Description.
    description_facets: t.Optional[t.List['models.AppBskyRichtextFacet.Main']] = None  #: Description facets.
    feeds: te.Annotated[t.Optional[t.List['models.AppBskyGraphStarterpack.FeedItem']], Field(max_length=3)] = (
        None  #: Feeds.
    )

    py_type: t.Literal['app.bsky.graph.starterpack'] = Field(
        default='app.bsky.graph.starterpack', alias='$type', frozen=True
    )


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyGraphStarterpack.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyGraphStarterpack.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyGraphStarterpack.Record`."""

    records: t.Dict[str, 'models.AppBskyGraphStarterpack.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyGraphStarterpack.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

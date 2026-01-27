##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.graph.block`."""

    created_at: string_formats.DateTime  #: Created at.
    subject: string_formats.Did  #: DID of the account to be blocked.

    py_type: t.Literal['app.bsky.graph.block'] = Field(default='app.bsky.graph.block', alias='$type', frozen=True)


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyGraphBlock.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyGraphBlock.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyGraphBlock.Record`."""

    records: t.Dict[str, 'models.AppBskyGraphBlock.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyGraphBlock.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

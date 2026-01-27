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

Live = t.Literal['app.bsky.actor.status#live']  #: Advertises an account as currently offering live content.


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.actor.status`."""

    created_at: string_formats.DateTime  #: Created at.
    status: t.Union['models.AppBskyActorStatus.Live', str]  #: The status for the account.
    duration_minutes: te.Annotated[t.Optional[int], Field(ge=1)] = (
        None  #: The duration of the status in minutes. Applications can choose to impose minimum and maximum limits.
    )
    embed: t.Optional[te.Annotated[t.Union['models.AppBskyEmbedExternal.Main'], Field(discriminator='py_type')]] = (
        None  #: An optional embed associated with the status.
    )

    py_type: t.Literal['app.bsky.actor.status'] = Field(default='app.bsky.actor.status', alias='$type', frozen=True)


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyActorStatus.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyActorStatus.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyActorStatus.Record`."""

    records: t.Dict[str, 'models.AppBskyActorStatus.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyActorStatus.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

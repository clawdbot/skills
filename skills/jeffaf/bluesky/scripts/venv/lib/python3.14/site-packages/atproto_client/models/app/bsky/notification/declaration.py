##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.notification.declaration`."""

    allow_subscriptions: t.Union[
        t.Literal['followers'], t.Literal['mutuals'], t.Literal['none'], str
    ]  #: A declaration of the user's preference for allowing activity subscriptions from other users. Absence of a record implies 'followers'.

    py_type: t.Literal['app.bsky.notification.declaration'] = Field(
        default='app.bsky.notification.declaration', alias='$type', frozen=True
    )


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyNotificationDeclaration.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyNotificationDeclaration.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyNotificationDeclaration.Record`."""

    records: t.Dict[str, 'models.AppBskyNotificationDeclaration.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyNotificationDeclaration.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

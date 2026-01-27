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
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.notification.listNotifications`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    priority: t.Optional[bool] = None  #: Priority.
    reasons: t.Optional[t.List[str]] = (
        None  #: Notification reasons to include in response. A reason that matches the reason property of #notification.
    )
    seen_at: t.Optional[string_formats.DateTime] = None  #: Seen at.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    priority: te.NotRequired[t.Optional[bool]]  #: Priority.
    reasons: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: Notification reasons to include in response. A reason that matches the reason property of #notification.
    seen_at: te.NotRequired[t.Optional[string_formats.DateTime]]  #: Seen at.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.notification.listNotifications`."""

    notifications: t.List['models.AppBskyNotificationListNotifications.Notification']  #: Notifications.
    cursor: t.Optional[str] = None  #: Cursor.
    priority: t.Optional[bool] = None  #: Priority.
    seen_at: t.Optional[string_formats.DateTime] = None  #: Seen at.


class Notification(base.ModelBase):
    """Definition model for :obj:`app.bsky.notification.listNotifications`."""

    author: 'models.AppBskyActorDefs.ProfileView'  #: Author.
    cid: string_formats.Cid  #: Cid.
    indexed_at: string_formats.DateTime  #: Indexed at.
    is_read: bool  #: Is read.
    reason: t.Union[
        t.Literal['like'],
        t.Literal['repost'],
        t.Literal['follow'],
        t.Literal['mention'],
        t.Literal['reply'],
        t.Literal['quote'],
        t.Literal['starterpack-joined'],
        t.Literal['verified'],
        t.Literal['unverified'],
        t.Literal['like-via-repost'],
        t.Literal['repost-via-repost'],
        t.Literal['subscribed-post'],
        str,
    ]  #: The reason why this notification was delivered - e.g. your post was liked, or you received a new follower.
    record: 'UnknownType'  #: Record.
    uri: string_formats.AtUri  #: Uri.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    reason_subject: t.Optional[string_formats.AtUri] = None  #: Reason subject.

    py_type: t.Literal['app.bsky.notification.listNotifications#notification'] = Field(
        default='app.bsky.notification.listNotifications#notification', alias='$type', frozen=True
    )

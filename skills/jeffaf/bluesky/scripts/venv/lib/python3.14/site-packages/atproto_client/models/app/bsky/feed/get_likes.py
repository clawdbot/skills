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


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.feed.getLikes`."""

    uri: string_formats.AtUri  #: AT-URI of the subject (eg, a post record).
    cid: t.Optional[string_formats.Cid] = (
        None  #: CID of the subject record (aka, specific version of record), to filter likes.
    )
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    uri: string_formats.AtUri  #: AT-URI of the subject (eg, a post record).
    cid: te.NotRequired[
        t.Optional[string_formats.Cid]
    ]  #: CID of the subject record (aka, specific version of record), to filter likes.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.feed.getLikes`."""

    likes: t.List['models.AppBskyFeedGetLikes.Like']  #: Likes.
    uri: string_formats.AtUri  #: Uri.
    cid: t.Optional[string_formats.Cid] = None  #: Cid.
    cursor: t.Optional[str] = None  #: Cursor.


class Like(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.getLikes`."""

    actor: 'models.AppBskyActorDefs.ProfileView'  #: Actor.
    created_at: string_formats.DateTime  #: Created at.
    indexed_at: string_formats.DateTime  #: Indexed at.

    py_type: t.Literal['app.bsky.feed.getLikes#like'] = Field(
        default='app.bsky.feed.getLikes#like', alias='$type', frozen=True
    )

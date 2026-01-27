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
    """Parameters model for :obj:`app.bsky.feed.getFeedSkeleton`."""

    feed: string_formats.AtUri  #: Reference to feed generator record describing the specific feed being requested.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    feed: string_formats.AtUri  #: Reference to feed generator record describing the specific feed being requested.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.feed.getFeedSkeleton`."""

    feed: t.List['models.AppBskyFeedDefs.SkeletonFeedPost']  #: Feed.
    cursor: t.Optional[str] = None  #: Cursor.
    req_id: te.Annotated[t.Optional[str], Field(max_length=100)] = (
        None  #: Unique identifier per request that may be passed back alongside interactions.
    )

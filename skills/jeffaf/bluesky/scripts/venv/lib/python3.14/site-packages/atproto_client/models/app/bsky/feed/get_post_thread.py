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
    """Parameters model for :obj:`app.bsky.feed.getPostThread`."""

    uri: string_formats.AtUri  #: Reference (AT-URI) to post record.
    depth: te.Annotated[t.Optional[int], Field(ge=0, le=1000)] = (
        None  #: How many levels of reply depth should be included in response.
    )
    parent_height: te.Annotated[t.Optional[int], Field(ge=0, le=1000)] = (
        None  #: How many levels of parent (and grandparent, etc) post to include.
    )


class ParamsDict(t.TypedDict):
    uri: string_formats.AtUri  #: Reference (AT-URI) to post record.
    depth: te.NotRequired[t.Optional[int]]  #: How many levels of reply depth should be included in response.
    parent_height: te.NotRequired[t.Optional[int]]  #: How many levels of parent (and grandparent, etc) post to include.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.feed.getPostThread`."""

    thread: te.Annotated[
        t.Union[
            'models.AppBskyFeedDefs.ThreadViewPost',
            'models.AppBskyFeedDefs.NotFoundPost',
            'models.AppBskyFeedDefs.BlockedPost',
        ],
        Field(discriminator='py_type'),
    ]  #: Thread.
    threadgate: t.Optional['models.AppBskyFeedDefs.ThreadgateView'] = None  #: Threadgate.

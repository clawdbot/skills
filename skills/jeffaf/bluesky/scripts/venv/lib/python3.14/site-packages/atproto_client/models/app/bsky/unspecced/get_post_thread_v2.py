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
    """Parameters model for :obj:`app.bsky.unspecced.getPostThreadV2`."""

    anchor: string_formats.AtUri  #: Reference (AT-URI) to post record. This is the anchor post, and the thread will be built around it. It can be any post in the tree, not necessarily a root post.
    above: t.Optional[bool] = True  #: Whether to include parents above the anchor.
    below: te.Annotated[t.Optional[int], Field(ge=0, le=20)] = (
        None  #: How many levels of replies to include below the anchor.
    )
    branching_factor: te.Annotated[t.Optional[int], Field(ge=0, le=100)] = (
        None  #: Maximum of replies to include at each level of the thread, except for the direct replies to the anchor, which are (NOTE: currently, during unspecced phase) all returned (NOTE: later they might be paginated).
    )
    sort: t.Optional[t.Union[t.Literal['newest'], t.Literal['oldest'], t.Literal['top'], str]] = (
        'oldest'  #: Sorting for the thread replies.
    )


class ParamsDict(t.TypedDict):
    anchor: string_formats.AtUri  #: Reference (AT-URI) to post record. This is the anchor post, and the thread will be built around it. It can be any post in the tree, not necessarily a root post.
    above: te.NotRequired[t.Optional[bool]]  #: Whether to include parents above the anchor.
    below: te.NotRequired[t.Optional[int]]  #: How many levels of replies to include below the anchor.
    branching_factor: te.NotRequired[
        t.Optional[int]
    ]  #: Maximum of replies to include at each level of the thread, except for the direct replies to the anchor, which are (NOTE: currently, during unspecced phase) all returned (NOTE: later they might be paginated).
    sort: te.NotRequired[
        t.Optional[t.Union[t.Literal['newest'], t.Literal['oldest'], t.Literal['top'], str]]
    ]  #: Sorting for the thread replies.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getPostThreadV2`."""

    has_other_replies: bool  #: Whether this thread has additional replies. If true, a call can be made to the `getPostThreadOtherV2` endpoint to retrieve them.
    thread: t.List[
        'models.AppBskyUnspeccedGetPostThreadV2.ThreadItem'
    ]  #: A flat list of thread items. The depth of each item is indicated by the depth property inside the item.
    threadgate: t.Optional['models.AppBskyFeedDefs.ThreadgateView'] = None  #: Threadgate.


class ThreadItem(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.getPostThreadV2`."""

    depth: int  #: The nesting level of this item in the thread. Depth 0 means the anchor item. Items above have negative depths, items below have positive depths.
    uri: string_formats.AtUri  #: Uri.
    value: te.Annotated[
        t.Union[
            'models.AppBskyUnspeccedDefs.ThreadItemPost',
            'models.AppBskyUnspeccedDefs.ThreadItemNoUnauthenticated',
            'models.AppBskyUnspeccedDefs.ThreadItemNotFound',
            'models.AppBskyUnspeccedDefs.ThreadItemBlocked',
        ],
        Field(discriminator='py_type'),
    ]  #: Value.

    py_type: t.Literal['app.bsky.unspecced.getPostThreadV2#threadItem'] = Field(
        default='app.bsky.unspecced.getPostThreadV2#threadItem', alias='$type', frozen=True
    )

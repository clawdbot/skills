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
    """Parameters model for :obj:`app.bsky.unspecced.getPostThreadOtherV2`."""

    anchor: string_formats.AtUri  #: Reference (AT-URI) to post record. This is the anchor post.


class ParamsDict(t.TypedDict):
    anchor: string_formats.AtUri  #: Reference (AT-URI) to post record. This is the anchor post.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getPostThreadOtherV2`."""

    thread: t.List[
        'models.AppBskyUnspeccedGetPostThreadOtherV2.ThreadItem'
    ]  #: A flat list of other thread items. The depth of each item is indicated by the depth property inside the item.


class ThreadItem(base.ModelBase):
    """Definition model for :obj:`app.bsky.unspecced.getPostThreadOtherV2`."""

    depth: int  #: The nesting level of this item in the thread. Depth 0 means the anchor item. Items above have negative depths, items below have positive depths.
    uri: string_formats.AtUri  #: Uri.
    value: te.Annotated[
        t.Union['models.AppBskyUnspeccedDefs.ThreadItemPost'], Field(discriminator='py_type')
    ]  #: Value.

    py_type: t.Literal['app.bsky.unspecced.getPostThreadOtherV2#threadItem'] = Field(
        default='app.bsky.unspecced.getPostThreadOtherV2#threadItem', alias='$type', frozen=True
    )

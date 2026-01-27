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


class DisableRule(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.postgate`. Disables embedding of this post."""

    py_type: t.Literal['app.bsky.feed.postgate#disableRule'] = Field(
        default='app.bsky.feed.postgate#disableRule', alias='$type', frozen=True
    )


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.feed.postgate`."""

    created_at: string_formats.DateTime  #: Created at.
    post: string_formats.AtUri  #: Reference (AT-URI) to the post record.
    detached_embedding_uris: te.Annotated[t.Optional[t.List[string_formats.AtUri]], Field(max_length=50)] = (
        None  #: List of AT-URIs embedding this post that the author has detached from.
    )
    embedding_rules: t.Optional[
        t.List[te.Annotated[t.Union['models.AppBskyFeedPostgate.DisableRule'], Field(discriminator='py_type')]]
    ] = Field(
        max_length=5
    )  #: List of rules defining who can embed this post. If value is an empty array or is undefined, no particular rules apply and anyone can embed.

    py_type: t.Literal['app.bsky.feed.postgate'] = Field(default='app.bsky.feed.postgate', alias='$type', frozen=True)


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyFeedPostgate.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyFeedPostgate.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyFeedPostgate.Record`."""

    records: t.Dict[str, 'models.AppBskyFeedPostgate.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyFeedPostgate.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

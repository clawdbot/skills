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


class MentionRule(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.threadgate`. Allow replies from actors mentioned in your post."""

    py_type: t.Literal['app.bsky.feed.threadgate#mentionRule'] = Field(
        default='app.bsky.feed.threadgate#mentionRule', alias='$type', frozen=True
    )


class FollowerRule(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.threadgate`. Allow replies from actors who follow you."""

    py_type: t.Literal['app.bsky.feed.threadgate#followerRule'] = Field(
        default='app.bsky.feed.threadgate#followerRule', alias='$type', frozen=True
    )


class FollowingRule(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.threadgate`. Allow replies from actors you follow."""

    py_type: t.Literal['app.bsky.feed.threadgate#followingRule'] = Field(
        default='app.bsky.feed.threadgate#followingRule', alias='$type', frozen=True
    )


class ListRule(base.ModelBase):
    """Definition model for :obj:`app.bsky.feed.threadgate`. Allow replies from actors on a list."""

    list: string_formats.AtUri  #: List.

    py_type: t.Literal['app.bsky.feed.threadgate#listRule'] = Field(
        default='app.bsky.feed.threadgate#listRule', alias='$type', frozen=True
    )


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.feed.threadgate`."""

    created_at: string_formats.DateTime  #: Created at.
    post: string_formats.AtUri  #: Reference (AT-URI) to the post record.
    allow: t.Optional[
        t.List[
            te.Annotated[
                t.Union[
                    'models.AppBskyFeedThreadgate.MentionRule',
                    'models.AppBskyFeedThreadgate.FollowerRule',
                    'models.AppBskyFeedThreadgate.FollowingRule',
                    'models.AppBskyFeedThreadgate.ListRule',
                ],
                Field(discriminator='py_type'),
            ]
        ]
    ] = Field(
        max_length=5
    )  #: List of rules defining who can reply to this post. If value is an empty array, no one can reply. If value is undefined, anyone can reply.
    hidden_replies: te.Annotated[t.Optional[t.List[string_formats.AtUri]], Field(max_length=300)] = (
        None  #: List of hidden reply URIs.
    )

    py_type: t.Literal['app.bsky.feed.threadgate'] = Field(
        default='app.bsky.feed.threadgate', alias='$type', frozen=True
    )


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyFeedThreadgate.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyFeedThreadgate.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyFeedThreadgate.Record`."""

    records: t.Dict[str, 'models.AppBskyFeedThreadgate.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyFeedThreadgate.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

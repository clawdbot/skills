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


class Main(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    record: 'models.ComAtprotoRepoStrongRef.Main'  #: Record.

    py_type: t.Literal['app.bsky.embed.record'] = Field(default='app.bsky.embed.record', alias='$type', frozen=True)


class View(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    record: te.Annotated[
        t.Union[
            'models.AppBskyEmbedRecord.ViewRecord',
            'models.AppBskyEmbedRecord.ViewNotFound',
            'models.AppBskyEmbedRecord.ViewBlocked',
            'models.AppBskyEmbedRecord.ViewDetached',
            'models.AppBskyFeedDefs.GeneratorView',
            'models.AppBskyGraphDefs.ListView',
            'models.AppBskyLabelerDefs.LabelerView',
            'models.AppBskyGraphDefs.StarterPackViewBasic',
        ],
        Field(discriminator='py_type'),
    ]  #: Record.

    py_type: t.Literal['app.bsky.embed.record#view'] = Field(
        default='app.bsky.embed.record#view', alias='$type', frozen=True
    )


class ViewRecord(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    author: 'models.AppBskyActorDefs.ProfileViewBasic'  #: Author.
    cid: string_formats.Cid  #: Cid.
    indexed_at: string_formats.DateTime  #: Indexed at.
    uri: string_formats.AtUri  #: Uri.
    value: 'UnknownType'  #: The record data itself.
    embeds: t.Optional[
        t.List[
            te.Annotated[
                t.Union[
                    'models.AppBskyEmbedImages.View',
                    'models.AppBskyEmbedVideo.View',
                    'models.AppBskyEmbedExternal.View',
                    'models.AppBskyEmbedRecord.View',
                    'models.AppBskyEmbedRecordWithMedia.View',
                ],
                Field(discriminator='py_type'),
            ]
        ]
    ] = None  #: Embeds.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    like_count: t.Optional[int] = None  #: Like count.
    quote_count: t.Optional[int] = None  #: Quote count.
    reply_count: t.Optional[int] = None  #: Reply count.
    repost_count: t.Optional[int] = None  #: Repost count.

    py_type: t.Literal['app.bsky.embed.record#viewRecord'] = Field(
        default='app.bsky.embed.record#viewRecord', alias='$type', frozen=True
    )


class ViewNotFound(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    not_found: bool = Field(frozen=True)  #: Not found.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.embed.record#viewNotFound'] = Field(
        default='app.bsky.embed.record#viewNotFound', alias='$type', frozen=True
    )


class ViewBlocked(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    author: 'models.AppBskyFeedDefs.BlockedAuthor'  #: Author.
    blocked: bool = Field(frozen=True)  #: Blocked.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.embed.record#viewBlocked'] = Field(
        default='app.bsky.embed.record#viewBlocked', alias='$type', frozen=True
    )


class ViewDetached(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.record`."""

    detached: bool = Field(frozen=True)  #: Detached.
    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['app.bsky.embed.record#viewDetached'] = Field(
        default='app.bsky.embed.record#viewDetached', alias='$type', frozen=True
    )

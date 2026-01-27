##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Main(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.recordWithMedia`."""

    media: te.Annotated[
        t.Union['models.AppBskyEmbedImages.Main', 'models.AppBskyEmbedVideo.Main', 'models.AppBskyEmbedExternal.Main'],
        Field(discriminator='py_type'),
    ]  #: Media.
    record: 'models.AppBskyEmbedRecord.Main'  #: Record.

    py_type: t.Literal['app.bsky.embed.recordWithMedia'] = Field(
        default='app.bsky.embed.recordWithMedia', alias='$type', frozen=True
    )


class View(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.recordWithMedia`."""

    media: te.Annotated[
        t.Union['models.AppBskyEmbedImages.View', 'models.AppBskyEmbedVideo.View', 'models.AppBskyEmbedExternal.View'],
        Field(discriminator='py_type'),
    ]  #: Media.
    record: 'models.AppBskyEmbedRecord.View'  #: Record.

    py_type: t.Literal['app.bsky.embed.recordWithMedia#view'] = Field(
        default='app.bsky.embed.recordWithMedia#view', alias='$type', frozen=True
    )

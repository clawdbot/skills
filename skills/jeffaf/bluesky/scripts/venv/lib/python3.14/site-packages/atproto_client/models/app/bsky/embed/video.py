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
    from atproto_client.models.blob_ref import BlobRef
from atproto_client.models import base


class Main(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.video`."""

    video: 'BlobRef'  #: The mp4 video file. May be up to 100mb, formerly limited to 50mb.
    alt: te.Annotated[t.Optional[str], Field(max_length=10000)] = (
        None  #: Alt text description of the video, for accessibility.
    )
    aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None  #: Aspect ratio.
    captions: te.Annotated[t.Optional[t.List['models.AppBskyEmbedVideo.Caption']], Field(max_length=20)] = (
        None  #: Captions.
    )

    py_type: t.Literal['app.bsky.embed.video'] = Field(default='app.bsky.embed.video', alias='$type', frozen=True)


class Caption(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.video`."""

    file: 'BlobRef'  #: File.
    lang: string_formats.Language  #: Lang.

    py_type: t.Literal['app.bsky.embed.video#caption'] = Field(
        default='app.bsky.embed.video#caption', alias='$type', frozen=True
    )


class View(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.video`."""

    cid: string_formats.Cid  #: Cid.
    playlist: string_formats.Uri  #: Playlist.
    alt: te.Annotated[t.Optional[str], Field(max_length=10000)] = None  #: Alt.
    aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None  #: Aspect ratio.
    thumbnail: t.Optional[string_formats.Uri] = None  #: Thumbnail.

    py_type: t.Literal['app.bsky.embed.video#view'] = Field(
        default='app.bsky.embed.video#view', alias='$type', frozen=True
    )

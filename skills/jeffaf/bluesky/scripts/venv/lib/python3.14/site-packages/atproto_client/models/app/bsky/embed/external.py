##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
    from atproto_client.models.blob_ref import BlobRef
from atproto_client.models import base


class Main(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.external`. A representation of some externally linked content (eg, a URL and 'card'), embedded in a Bluesky record (eg, a post)."""

    external: 'models.AppBskyEmbedExternal.External'  #: External.

    py_type: t.Literal['app.bsky.embed.external'] = Field(default='app.bsky.embed.external', alias='$type', frozen=True)


class External(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.external`."""

    description: str  #: Description.
    title: str  #: Title.
    uri: string_formats.Uri  #: Uri.
    thumb: t.Optional['BlobRef'] = None  #: Thumb.

    py_type: t.Literal['app.bsky.embed.external#external'] = Field(
        default='app.bsky.embed.external#external', alias='$type', frozen=True
    )


class View(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.external`."""

    external: 'models.AppBskyEmbedExternal.ViewExternal'  #: External.

    py_type: t.Literal['app.bsky.embed.external#view'] = Field(
        default='app.bsky.embed.external#view', alias='$type', frozen=True
    )


class ViewExternal(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.external`."""

    description: str  #: Description.
    title: str  #: Title.
    uri: string_formats.Uri  #: Uri.
    thumb: t.Optional[string_formats.Uri] = None  #: Thumb.

    py_type: t.Literal['app.bsky.embed.external#viewExternal'] = Field(
        default='app.bsky.embed.external#viewExternal', alias='$type', frozen=True
    )

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
    """Definition model for :obj:`app.bsky.embed.images`."""

    images: t.List['models.AppBskyEmbedImages.Image'] = Field(max_length=4)  #: Images.

    py_type: t.Literal['app.bsky.embed.images'] = Field(default='app.bsky.embed.images', alias='$type', frozen=True)


class Image(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.images`."""

    alt: str  #: Alt text description of the image, for accessibility.
    image: 'BlobRef'  #: Image.
    aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None  #: Aspect ratio.

    py_type: t.Literal['app.bsky.embed.images#image'] = Field(
        default='app.bsky.embed.images#image', alias='$type', frozen=True
    )


class View(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.images`."""

    images: t.List['models.AppBskyEmbedImages.ViewImage'] = Field(max_length=4)  #: Images.

    py_type: t.Literal['app.bsky.embed.images#view'] = Field(
        default='app.bsky.embed.images#view', alias='$type', frozen=True
    )


class ViewImage(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.images`."""

    alt: str  #: Alt text description of the image, for accessibility.
    fullsize: string_formats.Uri  #: Fully-qualified URL where a large version of the image can be fetched. May or may not be the exact original blob. For example, CDN location provided by the App View.
    thumb: string_formats.Uri  #: Fully-qualified URL where a thumbnail of the image can be fetched. For example, CDN location provided by the App View.
    aspect_ratio: t.Optional['models.AppBskyEmbedDefs.AspectRatio'] = None  #: Aspect ratio.

    py_type: t.Literal['app.bsky.embed.images#viewImage'] = Field(
        default='app.bsky.embed.images#viewImage', alias='$type', frozen=True
    )

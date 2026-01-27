##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import base


class AspectRatio(base.ModelBase):
    """Definition model for :obj:`app.bsky.embed.defs`. width:height represents an aspect ratio. It may be approximate, and may not correspond to absolute dimensions in any given unit."""

    height: int = Field(ge=1)  #: Height.
    width: int = Field(ge=1)  #: Width.

    py_type: t.Literal['app.bsky.embed.defs#aspectRatio'] = Field(
        default='app.bsky.embed.defs#aspectRatio', alias='$type', frozen=True
    )

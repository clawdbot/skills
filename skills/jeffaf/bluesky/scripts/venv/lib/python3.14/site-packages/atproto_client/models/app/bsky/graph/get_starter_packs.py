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
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.graph.getStarterPacks`."""

    uris: t.List[string_formats.AtUri] = Field(max_length=25)  #: Uris.


class ParamsDict(t.TypedDict):
    uris: t.List[string_formats.AtUri]  #: Uris.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.graph.getStarterPacks`."""

    starter_packs: t.List['models.AppBskyGraphDefs.StarterPackViewBasic']  #: Starter packs.

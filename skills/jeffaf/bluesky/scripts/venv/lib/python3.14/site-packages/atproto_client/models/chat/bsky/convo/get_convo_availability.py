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
    """Parameters model for :obj:`chat.bsky.convo.getConvoAvailability`."""

    members: t.List[string_formats.Did] = Field(min_length=1, max_length=10)  #: Members.


class ParamsDict(t.TypedDict):
    members: t.List[string_formats.Did]  #: Members.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.getConvoAvailability`."""

    can_chat: bool  #: Can chat.
    convo: t.Optional['models.ChatBskyConvoDefs.ConvoView'] = None  #: Convo.

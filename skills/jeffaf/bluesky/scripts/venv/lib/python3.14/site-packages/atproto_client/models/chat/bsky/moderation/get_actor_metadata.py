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
    """Parameters model for :obj:`chat.bsky.moderation.getActorMetadata`."""

    actor: string_formats.Did  #: Actor.


class ParamsDict(t.TypedDict):
    actor: string_formats.Did  #: Actor.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.moderation.getActorMetadata`."""

    all: 'models.ChatBskyModerationGetActorMetadata.Metadata'  #: All.
    day: 'models.ChatBskyModerationGetActorMetadata.Metadata'  #: Day.
    month: 'models.ChatBskyModerationGetActorMetadata.Metadata'  #: Month.


class Metadata(base.ModelBase):
    """Definition model for :obj:`chat.bsky.moderation.getActorMetadata`."""

    convos: int  #: Convos.
    convos_started: int  #: Convos started.
    messages_received: int  #: Messages received.
    messages_sent: int  #: Messages sent.

    py_type: t.Literal['chat.bsky.moderation.getActorMetadata#metadata'] = Field(
        default='chat.bsky.moderation.getActorMetadata#metadata', alias='$type', frozen=True
    )

##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`chat.bsky.convo.sendMessage`."""

    convo_id: str  #: Convo id.
    message: 'models.ChatBskyConvoDefs.MessageInput'  #: Message.


class DataDict(t.TypedDict):
    convo_id: str  #: Convo id.
    message: 'models.ChatBskyConvoDefs.MessageInput'  #: Message.

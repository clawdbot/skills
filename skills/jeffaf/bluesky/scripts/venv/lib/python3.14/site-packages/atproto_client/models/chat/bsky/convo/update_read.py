##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`chat.bsky.convo.updateRead`."""

    convo_id: str  #: Convo id.
    message_id: t.Optional[str] = None  #: Message id.


class DataDict(t.TypedDict):
    convo_id: str  #: Convo id.
    message_id: te.NotRequired[t.Optional[str]]  #: Message id.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.updateRead`."""

    convo: 'models.ChatBskyConvoDefs.ConvoView'  #: Convo.

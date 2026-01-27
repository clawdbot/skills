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


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`chat.bsky.moderation.getMessageContext`."""

    message_id: str  #: Message id.
    after: t.Optional[int] = 5  #: After.
    before: t.Optional[int] = 5  #: Before.
    convo_id: t.Optional[str] = (
        None  #: Conversation that the message is from. NOTE: this field will eventually be required.
    )


class ParamsDict(t.TypedDict):
    message_id: str  #: Message id.
    after: te.NotRequired[t.Optional[int]]  #: After.
    before: te.NotRequired[t.Optional[int]]  #: Before.
    convo_id: te.NotRequired[
        t.Optional[str]
    ]  #: Conversation that the message is from. NOTE: this field will eventually be required.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.moderation.getMessageContext`."""

    messages: t.List[
        te.Annotated[
            t.Union['models.ChatBskyConvoDefs.MessageView', 'models.ChatBskyConvoDefs.DeletedMessageView'],
            Field(discriminator='py_type'),
        ]
    ]  #: Messages.

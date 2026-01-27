##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`chat.bsky.convo.sendMessageBatch`."""

    items: t.List['models.ChatBskyConvoSendMessageBatch.BatchItem'] = Field(max_length=100)  #: Items.


class DataDict(t.TypedDict):
    items: t.List['models.ChatBskyConvoSendMessageBatch.BatchItem']  #: Items.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.sendMessageBatch`."""

    items: t.List['models.ChatBskyConvoDefs.MessageView']  #: Items.


class BatchItem(base.ModelBase):
    """Definition model for :obj:`chat.bsky.convo.sendMessageBatch`."""

    convo_id: str  #: Convo id.
    message: 'models.ChatBskyConvoDefs.MessageInput'  #: Message.

    py_type: t.Literal['chat.bsky.convo.sendMessageBatch#batchItem'] = Field(
        default='chat.bsky.convo.sendMessageBatch#batchItem', alias='$type', frozen=True
    )

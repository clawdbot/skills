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
    """Parameters model for :obj:`chat.bsky.convo.getLog`."""

    cursor: t.Optional[str] = None  #: Cursor.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.getLog`."""

    logs: t.List[
        te.Annotated[
            t.Union[
                'models.ChatBskyConvoDefs.LogBeginConvo',
                'models.ChatBskyConvoDefs.LogAcceptConvo',
                'models.ChatBskyConvoDefs.LogLeaveConvo',
                'models.ChatBskyConvoDefs.LogMuteConvo',
                'models.ChatBskyConvoDefs.LogUnmuteConvo',
                'models.ChatBskyConvoDefs.LogCreateMessage',
                'models.ChatBskyConvoDefs.LogDeleteMessage',
                'models.ChatBskyConvoDefs.LogReadMessage',
                'models.ChatBskyConvoDefs.LogAddReaction',
                'models.ChatBskyConvoDefs.LogRemoveReaction',
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: Logs.
    cursor: t.Optional[str] = None  #: Cursor.

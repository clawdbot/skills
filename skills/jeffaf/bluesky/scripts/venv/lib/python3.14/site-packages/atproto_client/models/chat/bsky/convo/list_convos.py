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
    """Parameters model for :obj:`chat.bsky.convo.listConvos`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    read_state: t.Optional[t.Union[t.Literal['unread'], str]] = None  #: Read state.
    status: t.Optional[t.Union[t.Literal['request'], t.Literal['accepted'], str]] = None  #: Status.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    read_state: te.NotRequired[t.Optional[t.Union[t.Literal['unread'], str]]]  #: Read state.
    status: te.NotRequired[t.Optional[t.Union[t.Literal['request'], t.Literal['accepted'], str]]]  #: Status.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.listConvos`."""

    convos: t.List['models.ChatBskyConvoDefs.ConvoView']  #: Convos.
    cursor: t.Optional[str] = None  #: Cursor.

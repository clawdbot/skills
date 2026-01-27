##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`chat.bsky.convo.updateAllRead`."""

    status: t.Optional[t.Union[t.Literal['request'], t.Literal['accepted'], str]] = None  #: Status.


class DataDict(t.TypedDict):
    status: te.NotRequired[t.Optional[t.Union[t.Literal['request'], t.Literal['accepted'], str]]]  #: Status.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`chat.bsky.convo.updateAllRead`."""

    updated_count: int  #: The count of updated convos.

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
    """Parameters model for :obj:`com.atproto.label.subscribeLabels`."""

    cursor: t.Optional[int] = None  #: The last known event seq number to backfill from.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[int]]  #: The last known event seq number to backfill from.


class Labels(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.subscribeLabels`."""

    labels: t.List['models.ComAtprotoLabelDefs.Label']  #: Labels.
    seq: int  #: Seq.

    py_type: t.Literal['com.atproto.label.subscribeLabels#labels'] = Field(
        default='com.atproto.label.subscribeLabels#labels', alias='$type', frozen=True
    )


class Info(base.ModelBase):
    """Definition model for :obj:`com.atproto.label.subscribeLabels`."""

    name: t.Union[t.Literal['OutdatedCursor'], str]  #: Name.
    message: t.Optional[str] = None  #: Message.

    py_type: t.Literal['com.atproto.label.subscribeLabels#info'] = Field(
        default='com.atproto.label.subscribeLabels#info', alias='$type', frozen=True
    )

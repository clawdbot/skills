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
    """Parameters model for :obj:`com.atproto.temp.fetchLabels`."""

    limit: te.Annotated[t.Optional[int], Field(ge=1, le=250)] = None  #: Limit.
    since: t.Optional[int] = None  #: Since.


class ParamsDict(t.TypedDict):
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    since: te.NotRequired[t.Optional[int]]  #: Since.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.temp.fetchLabels`."""

    labels: t.List['models.ComAtprotoLabelDefs.Label']  #: Labels.

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
    """Parameters model for :obj:`com.atproto.admin.getInviteCodes`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=500)] = None  #: Limit.
    sort: t.Optional[t.Union[t.Literal['recent'], t.Literal['usage'], str]] = 'recent'  #: Sort.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    sort: te.NotRequired[t.Optional[t.Union[t.Literal['recent'], t.Literal['usage'], str]]]  #: Sort.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.admin.getInviteCodes`."""

    codes: t.List['models.ComAtprotoServerDefs.InviteCode']  #: Codes.
    cursor: t.Optional[str] = None  #: Cursor.

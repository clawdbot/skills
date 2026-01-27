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
    """Parameters model for :obj:`com.atproto.sync.listHosts`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=1000)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.listHosts`."""

    hosts: t.List[
        'models.ComAtprotoSyncListHosts.Host'
    ]  #: Sort order is not formally specified. Recommended order is by time host was first seen by the server, with oldest first.
    cursor: t.Optional[str] = None  #: Cursor.


class Host(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.listHosts`."""

    hostname: str  #: Hostname of server; not a URL (no scheme).
    account_count: t.Optional[int] = None  #: Account count.
    seq: t.Optional[int] = (
        None  #: Recent repo stream event sequence number. May be delayed from actual stream processing (eg, persisted cursor not in-memory cursor).
    )
    status: t.Optional['models.ComAtprotoSyncDefs.HostStatus'] = None  #: Status.

    py_type: t.Literal['com.atproto.sync.listHosts#host'] = Field(
        default='com.atproto.sync.listHosts#host', alias='$type', frozen=True
    )

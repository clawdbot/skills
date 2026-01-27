##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.getHostStatus`."""

    hostname: str  #: Hostname of the host (eg, PDS or relay) being queried.


class ParamsDict(t.TypedDict):
    hostname: str  #: Hostname of the host (eg, PDS or relay) being queried.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.getHostStatus`."""

    hostname: str  #: Hostname.
    account_count: t.Optional[int] = (
        None  #: Number of accounts on the server which are associated with the upstream host. Note that the upstream may actually have more accounts.
    )
    seq: t.Optional[int] = (
        None  #: Recent repo stream event sequence number. May be delayed from actual stream processing (eg, persisted cursor not in-memory cursor).
    )
    status: t.Optional['models.ComAtprotoSyncDefs.HostStatus'] = None  #: Status.

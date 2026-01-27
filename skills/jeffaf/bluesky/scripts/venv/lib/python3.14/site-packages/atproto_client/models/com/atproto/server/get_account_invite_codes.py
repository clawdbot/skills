##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.server.getAccountInviteCodes`."""

    create_available: t.Optional[bool] = (
        True  #: Controls whether any new 'earned' but not 'created' invites should be created.
    )
    include_used: t.Optional[bool] = True  #: Include used.


class ParamsDict(t.TypedDict):
    create_available: te.NotRequired[
        t.Optional[bool]
    ]  #: Controls whether any new 'earned' but not 'created' invites should be created.
    include_used: te.NotRequired[t.Optional[bool]]  #: Include used.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.getAccountInviteCodes`."""

    codes: t.List['models.ComAtprotoServerDefs.InviteCode']  #: Codes.

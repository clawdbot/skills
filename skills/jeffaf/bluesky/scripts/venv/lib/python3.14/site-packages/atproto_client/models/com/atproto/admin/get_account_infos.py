##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.admin.getAccountInfos`."""

    dids: t.List[string_formats.Did]  #: Dids.


class ParamsDict(t.TypedDict):
    dids: t.List[string_formats.Did]  #: Dids.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.admin.getAccountInfos`."""

    infos: t.List['models.ComAtprotoAdminDefs.AccountView']  #: Infos.

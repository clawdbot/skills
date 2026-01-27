##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.admin.disableInviteCodes`."""

    accounts: t.Optional[t.List[str]] = None  #: Accounts.
    codes: t.Optional[t.List[str]] = None  #: Codes.


class DataDict(t.TypedDict):
    accounts: te.NotRequired[t.Optional[t.List[str]]]  #: Accounts.
    codes: te.NotRequired[t.Optional[t.List[str]]]  #: Codes.

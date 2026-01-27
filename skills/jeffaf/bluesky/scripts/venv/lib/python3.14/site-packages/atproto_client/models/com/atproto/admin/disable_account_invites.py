##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.admin.disableAccountInvites`."""

    account: string_formats.Did  #: Account.
    note: t.Optional[str] = None  #: Optional reason for disabled invites.


class DataDict(t.TypedDict):
    account: string_formats.Did  #: Account.
    note: te.NotRequired[t.Optional[str]]  #: Optional reason for disabled invites.

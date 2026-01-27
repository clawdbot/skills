##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.admin.updateAccountEmail`."""

    account: string_formats.AtIdentifier  #: The handle or DID of the repo.
    email: str  #: Email.


class DataDict(t.TypedDict):
    account: string_formats.AtIdentifier  #: The handle or DID of the repo.
    email: str  #: Email.

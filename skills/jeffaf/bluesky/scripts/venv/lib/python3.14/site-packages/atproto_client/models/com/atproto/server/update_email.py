##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.updateEmail`."""

    email: str  #: Email.
    email_auth_factor: t.Optional[bool] = None  #: Email auth factor.
    token: t.Optional[str] = (
        None  #: Requires a token from com.atproto.sever.requestEmailUpdate if the account's email has been confirmed.
    )


class DataDict(t.TypedDict):
    email: str  #: Email.
    email_auth_factor: te.NotRequired[t.Optional[bool]]  #: Email auth factor.
    token: te.NotRequired[
        t.Optional[str]
    ]  #: Requires a token from com.atproto.sever.requestEmailUpdate if the account's email has been confirmed.

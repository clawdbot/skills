##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.createSession`."""

    identifier: str  #: Handle or other identifier supported by the server for the authenticating user.
    password: str  #: Password.
    allow_takendown: t.Optional[bool] = (
        None  #: When true, instead of throwing error for takendown accounts, a valid response with a narrow scoped token will be returned.
    )
    auth_factor_token: t.Optional[str] = None  #: Auth factor token.


class DataDict(t.TypedDict):
    identifier: str  #: Handle or other identifier supported by the server for the authenticating user.
    password: str  #: Password.
    allow_takendown: te.NotRequired[
        t.Optional[bool]
    ]  #: When true, instead of throwing error for takendown accounts, a valid response with a narrow scoped token will be returned.
    auth_factor_token: te.NotRequired[t.Optional[str]]  #: Auth factor token.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.createSession`."""

    access_jwt: str  #: Access jwt.
    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    refresh_jwt: str  #: Refresh jwt.
    active: t.Optional[bool] = None  #: Active.
    did_doc: t.Optional['UnknownType'] = None  #: Did doc.
    email: t.Optional[str] = None  #: Email.
    email_auth_factor: t.Optional[bool] = None  #: Email auth factor.
    email_confirmed: t.Optional[bool] = None  #: Email confirmed.
    status: t.Optional[t.Union[t.Literal['takendown'], t.Literal['suspended'], t.Literal['deactivated'], str]] = (
        None  #: If active=false, this optional field indicates a possible reason for why the account is not active. If active=false and no status is supplied, then the host makes no claim for why the repository is no longer being hosted.
    )

##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownInputType, UnknownType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.createAccount`."""

    handle: string_formats.Handle  #: Requested handle for the account.
    did: t.Optional[string_formats.Did] = None  #: Pre-existing atproto DID, being imported to a new account.
    email: t.Optional[str] = None  #: Email.
    invite_code: t.Optional[str] = None  #: Invite code.
    password: t.Optional[str] = (
        None  #: Initial account password. May need to meet instance-specific password strength requirements.
    )
    plc_op: t.Optional['UnknownInputType'] = (
        None  #: A signed DID PLC operation to be submitted as part of importing an existing account to this instance. NOTE: this optional field may be updated when full account migration is implemented.
    )
    recovery_key: t.Optional[str] = (
        None  #: DID PLC rotation key (aka, recovery key) to be included in PLC creation operation.
    )
    verification_code: t.Optional[str] = None  #: Verification code.
    verification_phone: t.Optional[str] = None  #: Verification phone.


class DataDict(t.TypedDict):
    handle: string_formats.Handle  #: Requested handle for the account.
    did: te.NotRequired[t.Optional[string_formats.Did]]  #: Pre-existing atproto DID, being imported to a new account.
    email: te.NotRequired[t.Optional[str]]  #: Email.
    invite_code: te.NotRequired[t.Optional[str]]  #: Invite code.
    password: te.NotRequired[
        t.Optional[str]
    ]  #: Initial account password. May need to meet instance-specific password strength requirements.
    plc_op: te.NotRequired[
        t.Optional['UnknownInputType']
    ]  #: A signed DID PLC operation to be submitted as part of importing an existing account to this instance. NOTE: this optional field may be updated when full account migration is implemented.
    recovery_key: te.NotRequired[
        t.Optional[str]
    ]  #: DID PLC rotation key (aka, recovery key) to be included in PLC creation operation.
    verification_code: te.NotRequired[t.Optional[str]]  #: Verification code.
    verification_phone: te.NotRequired[t.Optional[str]]  #: Verification phone.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.createAccount`. Account login session returned on successful account creation."""

    access_jwt: str  #: Access jwt.
    did: string_formats.Did  #: The DID of the new account.
    handle: string_formats.Handle  #: Handle.
    refresh_jwt: str  #: Refresh jwt.
    did_doc: t.Optional['UnknownType'] = None  #: Complete DID document.

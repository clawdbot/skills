##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.contact.verifyPhone`."""

    code: str  #: The code received via SMS as a result of the call to `app.bsky.contact.startPhoneVerification`.
    phone: str  #: The phone number to verify. Should be the same as the one passed to `app.bsky.contact.startPhoneVerification`.


class DataDict(t.TypedDict):
    code: str  #: The code received via SMS as a result of the call to `app.bsky.contact.startPhoneVerification`.
    phone: str  #: The phone number to verify. Should be the same as the one passed to `app.bsky.contact.startPhoneVerification`.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.contact.verifyPhone`."""

    token: str  #: JWT to be used in a call to `app.bsky.contact.importContacts`. It is only valid for a single call.

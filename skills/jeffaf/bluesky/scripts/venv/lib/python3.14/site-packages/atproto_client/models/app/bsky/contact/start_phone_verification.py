##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.contact.startPhoneVerification`."""

    phone: str  #: The phone number to receive the code via SMS.


class DataDict(t.TypedDict):
    phone: str  #: The phone number to receive the code via SMS.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.contact.startPhoneVerification`."""

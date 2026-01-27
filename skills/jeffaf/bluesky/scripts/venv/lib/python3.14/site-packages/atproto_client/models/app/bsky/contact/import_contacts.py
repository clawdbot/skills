##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.contact.importContacts`."""

    contacts: t.List[str] = Field(
        min_length=1, max_length=1000
    )  #: List of phone numbers in global E.164 format (e.g., '+12125550123'). Phone numbers that cannot be normalized into a valid phone number will be discarded. Should not repeat the 'phone' input used in `app.bsky.contact.verifyPhone`.
    token: str  #: JWT to authenticate the call. Use the JWT received as a response to the call to `app.bsky.contact.verifyPhone`.


class DataDict(t.TypedDict):
    contacts: t.List[
        str
    ]  #: List of phone numbers in global E.164 format (e.g., '+12125550123'). Phone numbers that cannot be normalized into a valid phone number will be discarded. Should not repeat the 'phone' input used in `app.bsky.contact.verifyPhone`.
    token: str  #: JWT to authenticate the call. Use the JWT received as a response to the call to `app.bsky.contact.verifyPhone`.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.contact.importContacts`."""

    matches_and_contact_indexes: t.List[
        'models.AppBskyContactDefs.MatchAndContactIndex'
    ]  #: The users that matched during import and their indexes on the input contacts, so the client can correlate with its local list.

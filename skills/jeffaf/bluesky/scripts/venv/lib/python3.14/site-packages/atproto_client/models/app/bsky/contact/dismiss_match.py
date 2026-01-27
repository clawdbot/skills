##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`app.bsky.contact.dismissMatch`."""

    subject: string_formats.Did  #: The subject's DID to dismiss the match with.


class DataDict(t.TypedDict):
    subject: string_formats.Did  #: The subject's DID to dismiss the match with.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.contact.dismissMatch`."""

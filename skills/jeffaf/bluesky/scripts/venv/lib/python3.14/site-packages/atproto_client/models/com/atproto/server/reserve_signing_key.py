##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.reserveSigningKey`."""

    did: t.Optional[string_formats.Did] = None  #: The DID to reserve a key for.


class DataDict(t.TypedDict):
    did: te.NotRequired[t.Optional[string_formats.Did]]  #: The DID to reserve a key for.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.reserveSigningKey`."""

    signing_key: str  #: The public key for the reserved signing key, in did:key serialization.

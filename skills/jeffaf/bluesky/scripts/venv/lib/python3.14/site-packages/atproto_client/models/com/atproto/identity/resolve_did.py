##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.identity.resolveDid`."""

    did: string_formats.Did  #: DID to resolve.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: DID to resolve.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.identity.resolveDid`."""

    did_doc: 'UnknownType'  #: The complete DID document for the identity.

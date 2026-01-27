##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownInputType, UnknownType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.identity.signPlcOperation`."""

    also_known_as: t.Optional[t.List[str]] = None  #: Also known as.
    rotation_keys: t.Optional[t.List[str]] = None  #: Rotation keys.
    services: t.Optional['UnknownInputType'] = None  #: Services.
    token: t.Optional[str] = None  #: A token received through com.atproto.identity.requestPlcOperationSignature.
    verification_methods: t.Optional['UnknownInputType'] = None  #: Verification methods.


class DataDict(t.TypedDict):
    also_known_as: te.NotRequired[t.Optional[t.List[str]]]  #: Also known as.
    rotation_keys: te.NotRequired[t.Optional[t.List[str]]]  #: Rotation keys.
    services: te.NotRequired[t.Optional['UnknownInputType']]  #: Services.
    token: te.NotRequired[
        t.Optional[str]
    ]  #: A token received through com.atproto.identity.requestPlcOperationSignature.
    verification_methods: te.NotRequired[t.Optional['UnknownInputType']]  #: Verification methods.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.identity.signPlcOperation`."""

    operation: 'UnknownType'  #: A signed DID PLC operation.

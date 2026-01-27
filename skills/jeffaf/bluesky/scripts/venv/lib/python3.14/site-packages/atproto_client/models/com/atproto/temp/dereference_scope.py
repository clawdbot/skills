##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.temp.dereferenceScope`."""

    scope: str  #: The scope reference (starts with 'ref:').


class ParamsDict(t.TypedDict):
    scope: str  #: The scope reference (starts with 'ref:').


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.temp.dereferenceScope`."""

    scope: str  #: The full oauth permission scope.

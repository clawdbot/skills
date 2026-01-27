##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.identity.resolveHandle`."""

    handle: string_formats.Handle  #: The handle to resolve.


class ParamsDict(t.TypedDict):
    handle: string_formats.Handle  #: The handle to resolve.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.identity.resolveHandle`."""

    did: string_formats.Did  #: Did.

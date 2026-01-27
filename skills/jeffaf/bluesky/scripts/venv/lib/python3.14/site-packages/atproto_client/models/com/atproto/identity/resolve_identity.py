##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.identity.resolveIdentity`."""

    identifier: string_formats.AtIdentifier  #: Handle or DID to resolve.


class ParamsDict(t.TypedDict):
    identifier: string_formats.AtIdentifier  #: Handle or DID to resolve.

##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.getHead`."""

    did: string_formats.Did  #: The DID of the repo.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: The DID of the repo.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.getHead`."""

    root: string_formats.Cid  #: Root.

##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.server.getServiceAuth`."""

    aud: string_formats.Did  #: The DID of the service that the token will be used to authenticate with.
    exp: t.Optional[int] = (
        None  #: The time in Unix Epoch seconds that the JWT expires. Defaults to 60 seconds in the future. The service may enforce certain time bounds on tokens depending on the requested scope.
    )
    lxm: t.Optional[string_formats.Nsid] = None  #: Lexicon (XRPC) method to bind the requested token to.


class ParamsDict(t.TypedDict):
    aud: string_formats.Did  #: The DID of the service that the token will be used to authenticate with.
    exp: te.NotRequired[
        t.Optional[int]
    ]  #: The time in Unix Epoch seconds that the JWT expires. Defaults to 60 seconds in the future. The service may enforce certain time bounds on tokens depending on the requested scope.
    lxm: te.NotRequired[t.Optional[string_formats.Nsid]]  #: Lexicon (XRPC) method to bind the requested token to.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.getServiceAuth`."""

    token: str  #: Token.

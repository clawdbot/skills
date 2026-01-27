##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.getRepo`."""

    did: string_formats.Did  #: The DID of the repo.
    since: t.Optional[string_formats.Tid] = None  #: The revision ('rev') of the repo to create a diff from.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: The DID of the repo.
    since: te.NotRequired[t.Optional[string_formats.Tid]]  #: The revision ('rev') of the repo to create a diff from.


#: Response raw data type.
Response: te.TypeAlias = bytes

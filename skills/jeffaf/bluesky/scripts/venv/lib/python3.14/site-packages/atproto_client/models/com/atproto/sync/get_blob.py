##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.getBlob`."""

    cid: string_formats.Cid  #: The CID of the blob to fetch.
    did: string_formats.Did  #: The DID of the account.


class ParamsDict(t.TypedDict):
    cid: string_formats.Cid  #: The CID of the blob to fetch.
    did: string_formats.Did  #: The DID of the account.


#: Response raw data type.
Response: te.TypeAlias = bytes

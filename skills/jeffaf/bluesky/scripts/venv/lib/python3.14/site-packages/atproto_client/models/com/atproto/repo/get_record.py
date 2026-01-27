##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.repo.getRecord`."""

    collection: string_formats.Nsid  #: The NSID of the record collection.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo.
    rkey: string_formats.RecordKey  #: The Record Key.
    cid: t.Optional[string_formats.Cid] = (
        None  #: The CID of the version of the record. If not specified, then return the most recent version.
    )


class ParamsDict(t.TypedDict):
    collection: string_formats.Nsid  #: The NSID of the record collection.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo.
    rkey: string_formats.RecordKey  #: The Record Key.
    cid: te.NotRequired[
        t.Optional[string_formats.Cid]
    ]  #: The CID of the version of the record. If not specified, then return the most recent version.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.repo.getRecord`."""

    uri: string_formats.AtUri  #: Uri.
    value: 'UnknownType'  #: Value.
    cid: t.Optional[string_formats.Cid] = None  #: Cid.

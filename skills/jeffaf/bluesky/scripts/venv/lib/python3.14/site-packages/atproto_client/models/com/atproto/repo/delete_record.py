##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.repo.deleteRecord`."""

    collection: string_formats.Nsid  #: The NSID of the record collection.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    rkey: string_formats.RecordKey  #: The Record Key.
    swap_commit: t.Optional[string_formats.Cid] = None  #: Compare and swap with the previous commit by CID.
    swap_record: t.Optional[string_formats.Cid] = None  #: Compare and swap with the previous record by CID.


class DataDict(t.TypedDict):
    collection: string_formats.Nsid  #: The NSID of the record collection.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    rkey: string_formats.RecordKey  #: The Record Key.
    swap_commit: te.NotRequired[t.Optional[string_formats.Cid]]  #: Compare and swap with the previous commit by CID.
    swap_record: te.NotRequired[t.Optional[string_formats.Cid]]  #: Compare and swap with the previous record by CID.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.repo.deleteRecord`."""

    commit: t.Optional['models.ComAtprotoRepoDefs.CommitMeta'] = None  #: Commit.

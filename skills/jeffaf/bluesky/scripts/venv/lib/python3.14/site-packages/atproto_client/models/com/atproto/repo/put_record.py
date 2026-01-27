##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
    from atproto_client.models.unknown_type import UnknownInputType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.repo.putRecord`."""

    collection: string_formats.Nsid  #: The NSID of the record collection.
    record: 'UnknownInputType'  #: The record to write.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    rkey: string_formats.RecordKey = Field(max_length=512)  #: The Record Key.
    swap_commit: t.Optional[string_formats.Cid] = None  #: Compare and swap with the previous commit by CID.
    swap_record: t.Optional[string_formats.Cid] = (
        None  #: Compare and swap with the previous record by CID. WARNING: nullable and optional field; may cause problems with golang implementation.
    )
    validate_: t.Optional[bool] = (
        None  #: Can be set to 'false' to skip Lexicon schema validation of record data, 'true' to require it, or leave unset to validate only for known Lexicons.
    )


class DataDict(t.TypedDict):
    collection: string_formats.Nsid  #: The NSID of the record collection.
    record: 'UnknownInputType'  #: The record to write.
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    rkey: string_formats.RecordKey  #: The Record Key.
    swap_commit: te.NotRequired[t.Optional[string_formats.Cid]]  #: Compare and swap with the previous commit by CID.
    swap_record: te.NotRequired[
        t.Optional[string_formats.Cid]
    ]  #: Compare and swap with the previous record by CID. WARNING: nullable and optional field; may cause problems with golang implementation.
    validate: te.NotRequired[
        t.Optional[bool]
    ]  #: Can be set to 'false' to skip Lexicon schema validation of record data, 'true' to require it, or leave unset to validate only for known Lexicons.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.repo.putRecord`."""

    cid: string_formats.Cid  #: Cid.
    uri: string_formats.AtUri  #: Uri.
    commit: t.Optional['models.ComAtprotoRepoDefs.CommitMeta'] = None  #: Commit.
    validation_status: t.Optional[t.Union[t.Literal['valid'], t.Literal['unknown'], str]] = None  #: Validation status.

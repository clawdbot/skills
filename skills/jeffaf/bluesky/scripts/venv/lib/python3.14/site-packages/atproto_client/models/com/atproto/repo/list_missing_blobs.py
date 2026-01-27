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
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.repo.listMissingBlobs`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=1000)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.repo.listMissingBlobs`."""

    blobs: t.List['models.ComAtprotoRepoListMissingBlobs.RecordBlob']  #: Blobs.
    cursor: t.Optional[str] = None  #: Cursor.


class RecordBlob(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.listMissingBlobs`."""

    cid: string_formats.Cid  #: Cid.
    record_uri: string_formats.AtUri  #: Record uri.

    py_type: t.Literal['com.atproto.repo.listMissingBlobs#recordBlob'] = Field(
        default='com.atproto.repo.listMissingBlobs#recordBlob', alias='$type', frozen=True
    )

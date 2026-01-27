##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import base, string_formats


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.listBlobs`."""

    did: string_formats.Did  #: The DID of the repo.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=1000)] = None  #: Limit.
    since: t.Optional[string_formats.Tid] = None  #: Optional revision of the repo to list blobs since.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: The DID of the repo.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    since: te.NotRequired[t.Optional[string_formats.Tid]]  #: Optional revision of the repo to list blobs since.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.listBlobs`."""

    cids: t.List[string_formats.Cid]  #: Cids.
    cursor: t.Optional[str] = None  #: Cursor.

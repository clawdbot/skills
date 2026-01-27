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
    """Parameters model for :obj:`com.atproto.sync.listReposByCollection`."""

    collection: string_formats.Nsid  #: Collection.
    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=2000)] = (
        None  #: Maximum size of response set. Recommend setting a large maximum (1000+) when enumerating large DID lists.
    )


class ParamsDict(t.TypedDict):
    collection: string_formats.Nsid  #: Collection.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[
        t.Optional[int]
    ]  #: Maximum size of response set. Recommend setting a large maximum (1000+) when enumerating large DID lists.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.listReposByCollection`."""

    repos: t.List['models.ComAtprotoSyncListReposByCollection.Repo']  #: Repos.
    cursor: t.Optional[str] = None  #: Cursor.


class Repo(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.listReposByCollection`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['com.atproto.sync.listReposByCollection#repo'] = Field(
        default='com.atproto.sync.listReposByCollection#repo', alias='$type', frozen=True
    )

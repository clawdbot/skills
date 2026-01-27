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
    """Parameters model for :obj:`com.atproto.sync.listRepos`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=1000)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.sync.listRepos`."""

    repos: t.List['models.ComAtprotoSyncListRepos.Repo']  #: Repos.
    cursor: t.Optional[str] = None  #: Cursor.


class Repo(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.listRepos`."""

    did: string_formats.Did  #: Did.
    head: string_formats.Cid  #: Current repo commit CID.
    rev: string_formats.Tid  #: Rev.
    active: t.Optional[bool] = None  #: Active.
    status: t.Optional[
        t.Union[
            t.Literal['takendown'],
            t.Literal['suspended'],
            t.Literal['deleted'],
            t.Literal['deactivated'],
            t.Literal['desynchronized'],
            t.Literal['throttled'],
            str,
        ]
    ] = None  #: If active=false, this optional field indicates a possible reason for why the account is not active. If active=false and no status is supplied, then the host makes no claim for why the repository is no longer being hosted.

    py_type: t.Literal['com.atproto.sync.listRepos#repo'] = Field(
        default='com.atproto.sync.listRepos#repo', alias='$type', frozen=True
    )

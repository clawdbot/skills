##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.moderation.searchRepos`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    q: t.Optional[str] = None  #: Q.
    term: t.Optional[str] = None  #: DEPRECATED: use 'q' instead.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    q: te.NotRequired[t.Optional[str]]  #: Q.
    term: te.NotRequired[t.Optional[str]]  #: DEPRECATED: use 'q' instead.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.searchRepos`."""

    repos: t.List['models.ToolsOzoneModerationDefs.RepoView']  #: Repos.
    cursor: t.Optional[str] = None  #: Cursor.

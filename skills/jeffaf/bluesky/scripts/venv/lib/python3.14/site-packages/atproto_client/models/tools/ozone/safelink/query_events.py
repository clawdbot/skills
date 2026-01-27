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


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.safelink.queryEvents`."""

    cursor: t.Optional[str] = None  #: Cursor for pagination.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Maximum number of results to return.
    pattern_type: t.Optional[str] = None  #: Filter by pattern type.
    sort_direction: t.Optional[t.Union[t.Literal['asc'], t.Literal['desc'], str]] = 'desc'  #: Sort direction.
    urls: t.Optional[t.List[str]] = None  #: Filter by specific URLs or domains.


class DataDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor for pagination.
    limit: te.NotRequired[t.Optional[int]]  #: Maximum number of results to return.
    pattern_type: te.NotRequired[t.Optional[str]]  #: Filter by pattern type.
    sort_direction: te.NotRequired[t.Optional[t.Union[t.Literal['asc'], t.Literal['desc'], str]]]  #: Sort direction.
    urls: te.NotRequired[t.Optional[t.List[str]]]  #: Filter by specific URLs or domains.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.safelink.queryEvents`."""

    events: t.List['models.ToolsOzoneSafelinkDefs.Event']  #: Events.
    cursor: t.Optional[str] = None  #: Next cursor for pagination. Only present if there are more results.

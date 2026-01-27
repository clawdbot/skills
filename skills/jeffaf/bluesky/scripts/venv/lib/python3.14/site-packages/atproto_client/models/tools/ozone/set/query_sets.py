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
    """Parameters model for :obj:`tools.ozone.set.querySets`."""

    cursor: t.Optional[str] = None  #: Cursor.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    name_prefix: t.Optional[str] = None  #: Name prefix.
    sort_by: t.Optional[t.Union[t.Literal['name'], t.Literal['createdAt'], t.Literal['updatedAt']]] = (
        'name'  #: Sort by.
    )
    sort_direction: t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]] = (
        'asc'  #: Defaults to ascending order of name field.
    )


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    name_prefix: te.NotRequired[t.Optional[str]]  #: Name prefix.
    sort_by: te.NotRequired[
        t.Optional[t.Union[t.Literal['name'], t.Literal['createdAt'], t.Literal['updatedAt']]]
    ]  #: Sort by.
    sort_direction: te.NotRequired[
        t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]]
    ]  #: Defaults to ascending order of name field.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.set.querySets`."""

    sets: t.List['models.ToolsOzoneSetDefs.SetView']  #: Sets.
    cursor: t.Optional[str] = None  #: Cursor.

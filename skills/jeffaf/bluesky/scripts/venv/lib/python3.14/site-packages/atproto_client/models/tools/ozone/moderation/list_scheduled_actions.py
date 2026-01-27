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


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.moderation.listScheduledActions`."""

    statuses: t.List[
        t.Union[t.Literal['pending'], t.Literal['executed'], t.Literal['cancelled'], t.Literal['failed'], str]
    ] = Field(min_length=1)  #: Filter actions by status.
    cursor: t.Optional[str] = None  #: Cursor for pagination.
    ends_before: t.Optional[string_formats.DateTime] = None  #: Filter actions scheduled to execute before this time.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Maximum number of results to return.
    starts_after: t.Optional[string_formats.DateTime] = None  #: Filter actions scheduled to execute after this time.
    subjects: te.Annotated[t.Optional[t.List[string_formats.Did]], Field(max_length=100)] = (
        None  #: Filter actions for specific DID subjects.
    )


class DataDict(t.TypedDict):
    statuses: t.List[
        t.Union[t.Literal['pending'], t.Literal['executed'], t.Literal['cancelled'], t.Literal['failed'], str]
    ]  #: Filter actions by status.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor for pagination.
    ends_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Filter actions scheduled to execute before this time.
    limit: te.NotRequired[t.Optional[int]]  #: Maximum number of results to return.
    starts_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Filter actions scheduled to execute after this time.
    subjects: te.NotRequired[t.Optional[t.List[string_formats.Did]]]  #: Filter actions for specific DID subjects.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.listScheduledActions`."""

    actions: t.List['models.ToolsOzoneModerationDefs.ScheduledActionView']  #: Actions.
    cursor: t.Optional[str] = None  #: Cursor for next page of results.

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
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.moderation.createReport`."""

    reason_type: (
        'models.ComAtprotoModerationDefs.ReasonType'  #: Indicates the broad category of violation the report is for.
    )
    subject: te.Annotated[
        t.Union['models.ComAtprotoAdminDefs.RepoRef', 'models.ComAtprotoRepoStrongRef.Main'],
        Field(discriminator='py_type'),
    ]  #: Subject.
    mod_tool: t.Optional['models.ComAtprotoModerationCreateReport.ModTool'] = None  #: Mod tool.
    reason: te.Annotated[t.Optional[str], Field(max_length=20000)] = (
        None  #: Additional context about the content and violation.
    )


class DataDict(t.TypedDict):
    reason_type: (
        'models.ComAtprotoModerationDefs.ReasonType'  #: Indicates the broad category of violation the report is for.
    )
    subject: te.Annotated[
        t.Union['models.ComAtprotoAdminDefs.RepoRef', 'models.ComAtprotoRepoStrongRef.Main'],
        Field(discriminator='py_type'),
    ]  #: Subject.
    mod_tool: te.NotRequired[t.Optional['models.ComAtprotoModerationCreateReport.ModTool']]  #: Mod tool.
    reason: te.NotRequired[t.Optional[str]]  #: Additional context about the content and violation.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.moderation.createReport`."""

    created_at: string_formats.DateTime  #: Created at.
    id: int  #: Id.
    reason_type: 'models.ComAtprotoModerationDefs.ReasonType'  #: Reason type.
    reported_by: string_formats.Did  #: Reported by.
    subject: te.Annotated[
        t.Union['models.ComAtprotoAdminDefs.RepoRef', 'models.ComAtprotoRepoStrongRef.Main'],
        Field(discriminator='py_type'),
    ]  #: Subject.
    reason: te.Annotated[t.Optional[str], Field(max_length=20000)] = None  #: Reason.


class ModTool(base.ModelBase):
    """Definition model for :obj:`com.atproto.moderation.createReport`. Moderation tool information for tracing the source of the action."""

    name: str  #: Name/identifier of the source (e.g., 'bsky-app/android', 'bsky-web/chrome').
    meta: t.Optional['UnknownType'] = None  #: Additional arbitrary metadata about the source.

    py_type: t.Literal['com.atproto.moderation.createReport#modTool'] = Field(
        default='com.atproto.moderation.createReport#modTool', alias='$type', frozen=True
    )

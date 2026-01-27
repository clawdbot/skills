##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

from pydantic import Field

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.moderation.getAccountTimeline`."""

    did: string_formats.Did  #: Did.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: Did.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.getAccountTimeline`."""

    timeline: t.List['models.ToolsOzoneModerationGetAccountTimeline.TimelineItem']  #: Timeline.


class TimelineItem(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.getAccountTimeline`."""

    day: str  #: Day.
    summary: t.List['models.ToolsOzoneModerationGetAccountTimeline.TimelineItemSummary']  #: Summary.

    py_type: t.Literal['tools.ozone.moderation.getAccountTimeline#timelineItem'] = Field(
        default='tools.ozone.moderation.getAccountTimeline#timelineItem', alias='$type', frozen=True
    )


class TimelineItemSummary(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.getAccountTimeline`."""

    count: int  #: Count.
    event_subject_type: t.Union[
        t.Literal['account'], t.Literal['record'], t.Literal['chat'], str
    ]  #: Event subject type.
    event_type: t.Union[
        'models.ToolsOzoneModerationDefs.ModEventTakedown',
        'models.ToolsOzoneModerationDefs.ModEventReverseTakedown',
        'models.ToolsOzoneModerationDefs.ModEventComment',
        'models.ToolsOzoneModerationDefs.ModEventReport',
        'models.ToolsOzoneModerationDefs.ModEventLabel',
        'models.ToolsOzoneModerationDefs.ModEventAcknowledge',
        'models.ToolsOzoneModerationDefs.ModEventEscalate',
        'models.ToolsOzoneModerationDefs.ModEventMute',
        'models.ToolsOzoneModerationDefs.ModEventUnmute',
        'models.ToolsOzoneModerationDefs.ModEventMuteReporter',
        'models.ToolsOzoneModerationDefs.ModEventUnmuteReporter',
        'models.ToolsOzoneModerationDefs.ModEventEmail',
        'models.ToolsOzoneModerationDefs.ModEventResolveAppeal',
        'models.ToolsOzoneModerationDefs.ModEventDivert',
        'models.ToolsOzoneModerationDefs.ModEventTag',
        'models.ToolsOzoneModerationDefs.AccountEvent',
        'models.ToolsOzoneModerationDefs.IdentityEvent',
        'models.ToolsOzoneModerationDefs.RecordEvent',
        'models.ToolsOzoneModerationDefs.ModEventPriorityScore',
        'models.ToolsOzoneModerationDefs.RevokeAccountCredentialsEvent',
        'models.ToolsOzoneModerationDefs.AgeAssuranceEvent',
        'models.ToolsOzoneModerationDefs.AgeAssuranceOverrideEvent',
        'models.ToolsOzoneModerationDefs.TimelineEventPlcCreate',
        'models.ToolsOzoneModerationDefs.TimelineEventPlcOperation',
        'models.ToolsOzoneModerationDefs.TimelineEventPlcTombstone',
        'models.ToolsOzoneHostingGetAccountHistory.AccountCreated',
        'models.ToolsOzoneHostingGetAccountHistory.EmailConfirmed',
        'models.ToolsOzoneHostingGetAccountHistory.PasswordUpdated',
        'models.ToolsOzoneHostingGetAccountHistory.HandleUpdated',
        'models.ToolsOzoneModerationDefs.ScheduleTakedownEvent',
        'models.ToolsOzoneModerationDefs.CancelScheduledTakedownEvent',
        str,
    ]  #: Event type.

    py_type: t.Literal['tools.ozone.moderation.getAccountTimeline#timelineItemSummary'] = Field(
        default='tools.ozone.moderation.getAccountTimeline#timelineItemSummary', alias='$type', frozen=True
    )

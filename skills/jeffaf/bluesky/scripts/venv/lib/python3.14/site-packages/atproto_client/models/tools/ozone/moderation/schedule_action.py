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
    """Input data model for :obj:`tools.ozone.moderation.scheduleAction`."""

    action: te.Annotated[
        t.Union['models.ToolsOzoneModerationScheduleAction.Takedown'], Field(discriminator='py_type')
    ]  #: Action.
    created_by: string_formats.Did  #: Created by.
    scheduling: 'models.ToolsOzoneModerationScheduleAction.SchedulingConfig'  #: Scheduling.
    subjects: t.List[string_formats.Did] = Field(max_length=100)  #: Array of DID subjects to schedule the action for.
    mod_tool: t.Optional['models.ToolsOzoneModerationDefs.ModTool'] = (
        None  #: This will be propagated to the moderation event when it is applied.
    )


class DataDict(t.TypedDict):
    action: te.Annotated[
        t.Union['models.ToolsOzoneModerationScheduleAction.Takedown'], Field(discriminator='py_type')
    ]  #: Action.
    created_by: string_formats.Did  #: Created by.
    scheduling: 'models.ToolsOzoneModerationScheduleAction.SchedulingConfig'  #: Scheduling.
    subjects: t.List[string_formats.Did]  #: Array of DID subjects to schedule the action for.
    mod_tool: te.NotRequired[
        t.Optional['models.ToolsOzoneModerationDefs.ModTool']
    ]  #: This will be propagated to the moderation event when it is applied.


class Takedown(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.scheduleAction`. Schedule a takedown action."""

    acknowledge_account_subjects: t.Optional[bool] = (
        None  #: If true, all other reports on content authored by this account will be resolved (acknowledged).
    )
    comment: t.Optional[str] = None  #: Comment.
    duration_in_hours: t.Optional[int] = (
        None  #: Indicates how long the takedown should be in effect before automatically expiring.
    )
    email_content: t.Optional[str] = None  #: Email content to be sent to the user upon takedown.
    email_subject: t.Optional[str] = None  #: Subject of the email to be sent to the user upon takedown.
    policies: te.Annotated[t.Optional[t.List[str]], Field(max_length=5)] = (
        None  #: Names/Keywords of the policies that drove the decision.
    )
    severity_level: t.Optional[str] = None  #: Severity level of the violation (e.g., 'sev-0', 'sev-1', 'sev-2', etc.).
    strike_count: t.Optional[int] = None  #: Number of strikes to assign to the user when takedown is applied.
    strike_expires_at: t.Optional[string_formats.DateTime] = (
        None  #: When the strike should expire. If not provided, the strike never expires.
    )

    py_type: t.Literal['tools.ozone.moderation.scheduleAction#takedown'] = Field(
        default='tools.ozone.moderation.scheduleAction#takedown', alias='$type', frozen=True
    )


class SchedulingConfig(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.scheduleAction`. Configuration for when the action should be executed."""

    execute_after: t.Optional[string_formats.DateTime] = (
        None  #: Earliest time to execute the action (for randomized scheduling).
    )
    execute_at: t.Optional[string_formats.DateTime] = None  #: Exact time to execute the action.
    execute_until: t.Optional[string_formats.DateTime] = (
        None  #: Latest time to execute the action (for randomized scheduling).
    )

    py_type: t.Literal['tools.ozone.moderation.scheduleAction#schedulingConfig'] = Field(
        default='tools.ozone.moderation.scheduleAction#schedulingConfig', alias='$type', frozen=True
    )


class ScheduledActionResults(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.scheduleAction`."""

    failed: t.List['models.ToolsOzoneModerationScheduleAction.FailedScheduling']  #: Failed.
    succeeded: t.List[string_formats.Did]  #: Succeeded.

    py_type: t.Literal['tools.ozone.moderation.scheduleAction#scheduledActionResults'] = Field(
        default='tools.ozone.moderation.scheduleAction#scheduledActionResults', alias='$type', frozen=True
    )


class FailedScheduling(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.scheduleAction`."""

    error: str  #: Error.
    subject: string_formats.Did  #: Subject.
    error_code: t.Optional[str] = None  #: Error code.

    py_type: t.Literal['tools.ozone.moderation.scheduleAction#failedScheduling'] = Field(
        default='tools.ozone.moderation.scheduleAction#failedScheduling', alias='$type', frozen=True
    )

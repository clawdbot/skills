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


class ModEventView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    created_at: string_formats.DateTime  #: Created at.
    created_by: string_formats.Did  #: Created by.
    event: te.Annotated[
        t.Union[
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
            'models.ToolsOzoneModerationDefs.AgeAssuranceEvent',
            'models.ToolsOzoneModerationDefs.AgeAssuranceOverrideEvent',
            'models.ToolsOzoneModerationDefs.RevokeAccountCredentialsEvent',
            'models.ToolsOzoneModerationDefs.ScheduleTakedownEvent',
            'models.ToolsOzoneModerationDefs.CancelScheduledTakedownEvent',
        ],
        Field(discriminator='py_type'),
    ]  #: Event.
    id: int  #: Id.
    subject: te.Annotated[
        t.Union[
            'models.ComAtprotoAdminDefs.RepoRef',
            'models.ComAtprotoRepoStrongRef.Main',
            'models.ChatBskyConvoDefs.MessageRef',
        ],
        Field(discriminator='py_type'),
    ]  #: Subject.
    subject_blob_cids: t.List[str]  #: Subject blob cids.
    creator_handle: t.Optional[str] = None  #: Creator handle.
    mod_tool: t.Optional['models.ToolsOzoneModerationDefs.ModTool'] = None  #: Mod tool.
    subject_handle: t.Optional[str] = None  #: Subject handle.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventView'] = Field(
        default='tools.ozone.moderation.defs#modEventView', alias='$type', frozen=True
    )


class ModEventViewDetail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    created_at: string_formats.DateTime  #: Created at.
    created_by: string_formats.Did  #: Created by.
    event: te.Annotated[
        t.Union[
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
            'models.ToolsOzoneModerationDefs.AgeAssuranceEvent',
            'models.ToolsOzoneModerationDefs.AgeAssuranceOverrideEvent',
            'models.ToolsOzoneModerationDefs.RevokeAccountCredentialsEvent',
            'models.ToolsOzoneModerationDefs.ScheduleTakedownEvent',
            'models.ToolsOzoneModerationDefs.CancelScheduledTakedownEvent',
        ],
        Field(discriminator='py_type'),
    ]  #: Event.
    id: int  #: Id.
    subject: te.Annotated[
        t.Union[
            'models.ToolsOzoneModerationDefs.RepoView',
            'models.ToolsOzoneModerationDefs.RepoViewNotFound',
            'models.ToolsOzoneModerationDefs.RecordView',
            'models.ToolsOzoneModerationDefs.RecordViewNotFound',
        ],
        Field(discriminator='py_type'),
    ]  #: Subject.
    subject_blobs: t.List['models.ToolsOzoneModerationDefs.BlobView']  #: Subject blobs.
    mod_tool: t.Optional['models.ToolsOzoneModerationDefs.ModTool'] = None  #: Mod tool.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventViewDetail'] = Field(
        default='tools.ozone.moderation.defs#modEventViewDetail', alias='$type', frozen=True
    )


class SubjectStatusView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    created_at: (
        string_formats.DateTime
    )  #: Timestamp referencing the first moderation status impacting event was emitted on the subject.
    id: int  #: Id.
    review_state: 'models.ToolsOzoneModerationDefs.SubjectReviewState'  #: Review state.
    subject: te.Annotated[
        t.Union[
            'models.ComAtprotoAdminDefs.RepoRef',
            'models.ComAtprotoRepoStrongRef.Main',
            'models.ChatBskyConvoDefs.MessageRef',
        ],
        Field(discriminator='py_type'),
    ]  #: Subject.
    updated_at: (
        string_formats.DateTime
    )  #: Timestamp referencing when the last update was made to the moderation status of the subject.
    account_stats: t.Optional['models.ToolsOzoneModerationDefs.AccountStats'] = (
        None  #: Statistics related to the account subject.
    )
    account_strike: t.Optional['models.ToolsOzoneModerationDefs.AccountStrike'] = (
        None  #: Strike information for the account (account-level only).
    )
    age_assurance_state: t.Optional[
        t.Union[
            t.Literal['pending'],
            t.Literal['assured'],
            t.Literal['unknown'],
            t.Literal['reset'],
            t.Literal['blocked'],
            str,
        ]
    ] = None  #: Current age assurance state of the subject.
    age_assurance_updated_by: t.Optional[t.Union[t.Literal['admin'], t.Literal['user'], str]] = (
        None  #: Whether or not the last successful update to age assurance was made by the user or admin.
    )
    appealed: t.Optional[bool] = (
        None  #: True indicates that the a previously taken moderator action was appealed against, by the author of the content. False indicates last appeal was resolved by moderators.
    )
    comment: t.Optional[str] = None  #: Sticky comment on the subject.
    hosting: t.Optional[
        te.Annotated[
            t.Union['models.ToolsOzoneModerationDefs.AccountHosting', 'models.ToolsOzoneModerationDefs.RecordHosting'],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Hosting.
    last_appealed_at: t.Optional[string_formats.DateTime] = (
        None  #: Timestamp referencing when the author of the subject appealed a moderation action.
    )
    last_reported_at: t.Optional[string_formats.DateTime] = None  #: Last reported at.
    last_reviewed_at: t.Optional[string_formats.DateTime] = None  #: Last reviewed at.
    last_reviewed_by: t.Optional[string_formats.Did] = None  #: Last reviewed by.
    mute_reporting_until: t.Optional[string_formats.DateTime] = None  #: Mute reporting until.
    mute_until: t.Optional[string_formats.DateTime] = None  #: Mute until.
    priority_score: te.Annotated[t.Optional[int], Field(ge=0, le=100)] = (
        None  #: Numeric value representing the level of priority. Higher score means higher priority.
    )
    records_stats: t.Optional['models.ToolsOzoneModerationDefs.RecordsStats'] = (
        None  #: Statistics related to the record subjects authored by the subject's account.
    )
    subject_blob_cids: t.Optional[t.List[string_formats.Cid]] = None  #: Subject blob cids.
    subject_repo_handle: t.Optional[str] = None  #: Subject repo handle.
    suspend_until: t.Optional[string_formats.DateTime] = None  #: Suspend until.
    tags: t.Optional[t.List[str]] = None  #: Tags.
    takendown: t.Optional[bool] = None  #: Takendown.

    py_type: t.Literal['tools.ozone.moderation.defs#subjectStatusView'] = Field(
        default='tools.ozone.moderation.defs#subjectStatusView', alias='$type', frozen=True
    )


class SubjectView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Detailed view of a subject. For record subjects, the author's repo and profile will be returned."""

    subject: str  #: Subject.
    type: 'models.ComAtprotoModerationDefs.SubjectType'  #: Type.
    profile: t.Optional[te.Annotated[t.Union['base.UnknownUnionModel'], Field()]] = None  #: Profile.
    record: t.Optional['models.ToolsOzoneModerationDefs.RecordViewDetail'] = None  #: Record.
    repo: t.Optional['models.ToolsOzoneModerationDefs.RepoViewDetail'] = None  #: Repo.
    status: t.Optional['models.ToolsOzoneModerationDefs.SubjectStatusView'] = None  #: Status.

    py_type: t.Literal['tools.ozone.moderation.defs#subjectView'] = Field(
        default='tools.ozone.moderation.defs#subjectView', alias='$type', frozen=True
    )


class AccountStats(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Statistics about a particular account subject."""

    appeal_count: t.Optional[int] = None  #: Total number of appeals against a moderation action on the account.
    escalate_count: t.Optional[int] = None  #: Number of times the account was escalated.
    report_count: t.Optional[int] = None  #: Total number of reports on the account.
    suspend_count: t.Optional[int] = None  #: Number of times the account was suspended.
    takedown_count: t.Optional[int] = None  #: Number of times the account was taken down.

    py_type: t.Literal['tools.ozone.moderation.defs#accountStats'] = Field(
        default='tools.ozone.moderation.defs#accountStats', alias='$type', frozen=True
    )


class RecordsStats(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Statistics about a set of record subject items."""

    appealed_count: t.Optional[int] = None  #: Number of items that were appealed at least once.
    escalated_count: t.Optional[int] = None  #: Number of items that were escalated at least once.
    pending_count: t.Optional[int] = None  #: Number of item currently in "reviewOpen" or "reviewEscalated" state.
    processed_count: t.Optional[int] = None  #: Number of item currently in "reviewNone" or "reviewClosed" state.
    reported_count: t.Optional[int] = None  #: Number of items that were reported at least once.
    subject_count: t.Optional[int] = None  #: Total number of item in the set.
    takendown_count: t.Optional[int] = None  #: Number of item currently taken down.
    total_reports: t.Optional[int] = None  #: Cumulative sum of the number of reports on the items in the set.

    py_type: t.Literal['tools.ozone.moderation.defs#recordsStats'] = Field(
        default='tools.ozone.moderation.defs#recordsStats', alias='$type', frozen=True
    )


class AccountStrike(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Strike information for an account."""

    active_strike_count: t.Optional[int] = None  #: Current number of active strikes (excluding expired strikes).
    first_strike_at: t.Optional[string_formats.DateTime] = None  #: Timestamp of the first strike received.
    last_strike_at: t.Optional[string_formats.DateTime] = None  #: Timestamp of the most recent strike received.
    total_strike_count: t.Optional[int] = None  #: Total number of strikes ever received (including expired strikes).

    py_type: t.Literal['tools.ozone.moderation.defs#accountStrike'] = Field(
        default='tools.ozone.moderation.defs#accountStrike', alias='$type', frozen=True
    )


SubjectReviewState = t.Union[
    'models.ToolsOzoneModerationDefs.ReviewOpen',
    'models.ToolsOzoneModerationDefs.ReviewEscalated',
    'models.ToolsOzoneModerationDefs.ReviewClosed',
    'models.ToolsOzoneModerationDefs.ReviewNone',
    str,
]  #: Subject review state

ReviewOpen = t.Literal[
    'tools.ozone.moderation.defs#reviewOpen'
]  #: Moderator review status of a subject: Open. Indicates that the subject needs to be reviewed by a moderator

ReviewEscalated = t.Literal[
    'tools.ozone.moderation.defs#reviewEscalated'
]  #: Moderator review status of a subject: Escalated. Indicates that the subject was escalated for review by a moderator

ReviewClosed = t.Literal[
    'tools.ozone.moderation.defs#reviewClosed'
]  #: Moderator review status of a subject: Closed. Indicates that the subject was already reviewed and resolved by a moderator

ReviewNone = t.Literal[
    'tools.ozone.moderation.defs#reviewNone'
]  #: Moderator review status of a subject: Unnecessary. Indicates that the subject does not need a review at the moment but there is probably some moderation related metadata available for it


class ModEventTakedown(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Take down a subject permanently or temporarily."""

    acknowledge_account_subjects: t.Optional[bool] = (
        None  #: If true, all other reports on content authored by this account will be resolved (acknowledged).
    )
    comment: t.Optional[str] = None  #: Comment.
    duration_in_hours: t.Optional[int] = (
        None  #: Indicates how long the takedown should be in effect before automatically expiring.
    )
    policies: te.Annotated[t.Optional[t.List[str]], Field(max_length=5)] = (
        None  #: Names/Keywords of the policies that drove the decision.
    )
    severity_level: t.Optional[str] = None  #: Severity level of the violation (e.g., 'sev-0', 'sev-1', 'sev-2', etc.).
    strike_count: t.Optional[int] = None  #: Number of strikes to assign to the user for this violation.
    strike_expires_at: t.Optional[string_formats.DateTime] = (
        None  #: When the strike should expire. If not provided, the strike never expires.
    )
    target_services: t.Optional[t.List[t.Union[t.Literal['appview'], t.Literal['pds'], str]]] = (
        None  #: List of services where the takedown should be applied. If empty or not provided, takedown is applied on all configured services.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventTakedown'] = Field(
        default='tools.ozone.moderation.defs#modEventTakedown', alias='$type', frozen=True
    )


class ModEventReverseTakedown(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Revert take down action on a subject."""

    comment: t.Optional[str] = None  #: Describe reasoning behind the reversal.
    policies: te.Annotated[t.Optional[t.List[str]], Field(max_length=5)] = (
        None  #: Names/Keywords of the policy infraction for which takedown is being reversed.
    )
    severity_level: t.Optional[str] = (
        None  #: Severity level of the violation. Usually set from the last policy infraction's severity.
    )
    strike_count: t.Optional[int] = (
        None  #: Number of strikes to subtract from the user's strike count. Usually set from the last policy infraction's severity.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventReverseTakedown'] = Field(
        default='tools.ozone.moderation.defs#modEventReverseTakedown', alias='$type', frozen=True
    )


class ModEventResolveAppeal(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Resolve appeal on a subject."""

    comment: t.Optional[str] = None  #: Describe resolution.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventResolveAppeal'] = Field(
        default='tools.ozone.moderation.defs#modEventResolveAppeal', alias='$type', frozen=True
    )


class ModEventComment(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Add a comment to a subject. An empty comment will clear any previously set sticky comment."""

    comment: t.Optional[str] = None  #: Comment.
    sticky: t.Optional[bool] = None  #: Make the comment persistent on the subject.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventComment'] = Field(
        default='tools.ozone.moderation.defs#modEventComment', alias='$type', frozen=True
    )


class ModEventReport(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Report a subject."""

    report_type: 'models.ComAtprotoModerationDefs.ReasonType'  #: Report type.
    comment: t.Optional[str] = None  #: Comment.
    is_reporter_muted: t.Optional[bool] = (
        None  #: Set to true if the reporter was muted from reporting at the time of the event. These reports won't impact the reviewState of the subject.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventReport'] = Field(
        default='tools.ozone.moderation.defs#modEventReport', alias='$type', frozen=True
    )


class ModEventLabel(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Apply/Negate labels on a subject."""

    create_label_vals: t.List[str]  #: Create label vals.
    negate_label_vals: t.List[str]  #: Negate label vals.
    comment: t.Optional[str] = None  #: Comment.
    duration_in_hours: t.Optional[int] = (
        None  #: Indicates how long the label will remain on the subject. Only applies on labels that are being added.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventLabel'] = Field(
        default='tools.ozone.moderation.defs#modEventLabel', alias='$type', frozen=True
    )


class ModEventPriorityScore(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Set priority score of the subject. Higher score means higher priority."""

    score: int = Field(ge=0, le=100)  #: Score.
    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventPriorityScore'] = Field(
        default='tools.ozone.moderation.defs#modEventPriorityScore', alias='$type', frozen=True
    )


class AgeAssuranceEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Age assurance info coming directly from users. Only works on DID subjects."""

    attempt_id: str  #: The unique identifier for this instance of the age assurance flow, in UUID format.
    created_at: string_formats.DateTime  #: The date and time of this write operation.
    status: t.Union[
        t.Literal['unknown'], t.Literal['pending'], t.Literal['assured'], str
    ]  #: The status of the Age Assurance process.
    access: t.Optional['models.AppBskyAgeassuranceDefs.Access'] = None  #: Access.
    complete_ip: t.Optional[str] = None  #: The IP address used when completing the AA flow.
    complete_ua: t.Optional[str] = None  #: The user agent used when completing the AA flow.
    country_code: t.Optional[str] = (
        None  #: The ISO 3166-1 alpha-2 country code provided when beginning the Age Assurance flow.
    )
    init_ip: t.Optional[str] = None  #: The IP address used when initiating the AA flow.
    init_ua: t.Optional[str] = None  #: The user agent used when initiating the AA flow.
    region_code: t.Optional[str] = None  #: The ISO 3166-2 region code provided when beginning the Age Assurance flow.

    py_type: t.Literal['tools.ozone.moderation.defs#ageAssuranceEvent'] = Field(
        default='tools.ozone.moderation.defs#ageAssuranceEvent', alias='$type', frozen=True
    )


class AgeAssuranceOverrideEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Age assurance status override by moderators. Only works on DID subjects."""

    comment: str = Field(min_length=1)  #: Comment describing the reason for the override.
    status: t.Union[
        t.Literal['assured'], t.Literal['reset'], t.Literal['blocked'], str
    ]  #: The status to be set for the user decided by a moderator, overriding whatever value the user had previously. Use reset to default to original state.
    access: t.Optional['models.AppBskyAgeassuranceDefs.Access'] = None  #: Access.

    py_type: t.Literal['tools.ozone.moderation.defs#ageAssuranceOverrideEvent'] = Field(
        default='tools.ozone.moderation.defs#ageAssuranceOverrideEvent', alias='$type', frozen=True
    )


class RevokeAccountCredentialsEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Account credentials revocation by moderators. Only works on DID subjects."""

    comment: str = Field(min_length=1)  #: Comment describing the reason for the revocation.

    py_type: t.Literal['tools.ozone.moderation.defs#revokeAccountCredentialsEvent'] = Field(
        default='tools.ozone.moderation.defs#revokeAccountCredentialsEvent', alias='$type', frozen=True
    )


class ModEventAcknowledge(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    acknowledge_account_subjects: t.Optional[bool] = (
        None  #: If true, all other reports on content authored by this account will be resolved (acknowledged).
    )
    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventAcknowledge'] = Field(
        default='tools.ozone.moderation.defs#modEventAcknowledge', alias='$type', frozen=True
    )


class ModEventEscalate(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventEscalate'] = Field(
        default='tools.ozone.moderation.defs#modEventEscalate', alias='$type', frozen=True
    )


class ModEventMute(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Mute incoming reports on a subject."""

    duration_in_hours: int  #: Indicates how long the subject should remain muted.
    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventMute'] = Field(
        default='tools.ozone.moderation.defs#modEventMute', alias='$type', frozen=True
    )


class ModEventUnmute(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Unmute action on a subject."""

    comment: t.Optional[str] = None  #: Describe reasoning behind the reversal.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventUnmute'] = Field(
        default='tools.ozone.moderation.defs#modEventUnmute', alias='$type', frozen=True
    )


class ModEventMuteReporter(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Mute incoming reports from an account."""

    comment: t.Optional[str] = None  #: Comment.
    duration_in_hours: t.Optional[int] = (
        None  #: Indicates how long the account should remain muted. Falsy value here means a permanent mute.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventMuteReporter'] = Field(
        default='tools.ozone.moderation.defs#modEventMuteReporter', alias='$type', frozen=True
    )


class ModEventUnmuteReporter(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Unmute incoming reports from an account."""

    comment: t.Optional[str] = None  #: Describe reasoning behind the reversal.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventUnmuteReporter'] = Field(
        default='tools.ozone.moderation.defs#modEventUnmuteReporter', alias='$type', frozen=True
    )


class ModEventEmail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Keep a log of outgoing email to a user."""

    subject_line: str  #: The subject line of the email sent to the user.
    comment: t.Optional[str] = None  #: Additional comment about the outgoing comm.
    content: t.Optional[str] = None  #: The content of the email sent to the user.
    is_delivered: t.Optional[bool] = (
        None  #: Indicates whether the email was successfully delivered to the user's inbox.
    )
    policies: te.Annotated[t.Optional[t.List[str]], Field(max_length=5)] = (
        None  #: Names/Keywords of the policies that necessitated the email.
    )
    severity_level: t.Optional[str] = (
        None  #: Severity level of the violation. Normally 'sev-1' that adds strike on repeat offense.
    )
    strike_count: t.Optional[int] = (
        None  #: Number of strikes to assign to the user for this violation. Normally 0 as an indicator of a warning and only added as a strike on a repeat offense.
    )
    strike_expires_at: t.Optional[string_formats.DateTime] = (
        None  #: When the strike should expire. If not provided, the strike never expires.
    )

    py_type: t.Literal['tools.ozone.moderation.defs#modEventEmail'] = Field(
        default='tools.ozone.moderation.defs#modEventEmail', alias='$type', frozen=True
    )


class ModEventDivert(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Divert a record's blobs to a 3rd party service for further scanning/tagging."""

    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventDivert'] = Field(
        default='tools.ozone.moderation.defs#modEventDivert', alias='$type', frozen=True
    )


class ModEventTag(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Add/Remove a tag on a subject."""

    add: t.List[str]  #: Tags to be added to the subject. If already exists, won't be duplicated.
    remove: t.List[str]  #: Tags to be removed to the subject. Ignores a tag If it doesn't exist, won't be duplicated.
    comment: t.Optional[str] = None  #: Additional comment about added/removed tags.

    py_type: t.Literal['tools.ozone.moderation.defs#modEventTag'] = Field(
        default='tools.ozone.moderation.defs#modEventTag', alias='$type', frozen=True
    )


class AccountEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Logs account status related events on a repo subject. Normally captured by automod from the firehose and emitted to ozone for historical tracking."""

    active: (
        bool  #: Indicates that the account has a repository which can be fetched from the host that emitted this event.
    )
    timestamp: string_formats.DateTime  #: Timestamp.
    comment: t.Optional[str] = None  #: Comment.
    status: t.Optional[
        t.Union[
            t.Literal['unknown'],
            t.Literal['deactivated'],
            t.Literal['deleted'],
            t.Literal['takendown'],
            t.Literal['suspended'],
            t.Literal['tombstoned'],
            str,
        ]
    ] = None  #: Status.

    py_type: t.Literal['tools.ozone.moderation.defs#accountEvent'] = Field(
        default='tools.ozone.moderation.defs#accountEvent', alias='$type', frozen=True
    )


class IdentityEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Logs identity related events on a repo subject. Normally captured by automod from the firehose and emitted to ozone for historical tracking."""

    timestamp: string_formats.DateTime  #: Timestamp.
    comment: t.Optional[str] = None  #: Comment.
    handle: t.Optional[string_formats.Handle] = None  #: Handle.
    pds_host: t.Optional[string_formats.Uri] = None  #: Pds host.
    tombstone: t.Optional[bool] = None  #: Tombstone.

    py_type: t.Literal['tools.ozone.moderation.defs#identityEvent'] = Field(
        default='tools.ozone.moderation.defs#identityEvent', alias='$type', frozen=True
    )


class RecordEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Logs lifecycle event on a record subject. Normally captured by automod from the firehose and emitted to ozone for historical tracking."""

    op: t.Union[t.Literal['create'], t.Literal['update'], t.Literal['delete'], str]  #: Op.
    timestamp: string_formats.DateTime  #: Timestamp.
    cid: t.Optional[string_formats.Cid] = None  #: Cid.
    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#recordEvent'] = Field(
        default='tools.ozone.moderation.defs#recordEvent', alias='$type', frozen=True
    )


class ScheduleTakedownEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Logs a scheduled takedown action for an account."""

    comment: t.Optional[str] = None  #: Comment.
    execute_after: t.Optional[string_formats.DateTime] = None  #: Execute after.
    execute_at: t.Optional[string_formats.DateTime] = None  #: Execute at.
    execute_until: t.Optional[string_formats.DateTime] = None  #: Execute until.

    py_type: t.Literal['tools.ozone.moderation.defs#scheduleTakedownEvent'] = Field(
        default='tools.ozone.moderation.defs#scheduleTakedownEvent', alias='$type', frozen=True
    )


class CancelScheduledTakedownEvent(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Logs cancellation of a scheduled takedown action for an account."""

    comment: t.Optional[str] = None  #: Comment.

    py_type: t.Literal['tools.ozone.moderation.defs#cancelScheduledTakedownEvent'] = Field(
        default='tools.ozone.moderation.defs#cancelScheduledTakedownEvent', alias='$type', frozen=True
    )


class RepoView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    indexed_at: string_formats.DateTime  #: Indexed at.
    moderation: 'models.ToolsOzoneModerationDefs.Moderation'  #: Moderation.
    related_records: t.List['UnknownType']  #: Related records.
    deactivated_at: t.Optional[string_formats.DateTime] = None  #: Deactivated at.
    email: t.Optional[str] = None  #: Email.
    invite_note: t.Optional[str] = None  #: Invite note.
    invited_by: t.Optional['models.ComAtprotoServerDefs.InviteCode'] = None  #: Invited by.
    invites_disabled: t.Optional[bool] = None  #: Invites disabled.
    threat_signatures: t.Optional[t.List['models.ComAtprotoAdminDefs.ThreatSignature']] = None  #: Threat signatures.

    py_type: t.Literal['tools.ozone.moderation.defs#repoView'] = Field(
        default='tools.ozone.moderation.defs#repoView', alias='$type', frozen=True
    )


class RepoViewDetail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    indexed_at: string_formats.DateTime  #: Indexed at.
    moderation: 'models.ToolsOzoneModerationDefs.ModerationDetail'  #: Moderation.
    related_records: t.List['UnknownType']  #: Related records.
    deactivated_at: t.Optional[string_formats.DateTime] = None  #: Deactivated at.
    email: t.Optional[str] = None  #: Email.
    email_confirmed_at: t.Optional[string_formats.DateTime] = None  #: Email confirmed at.
    invite_note: t.Optional[str] = None  #: Invite note.
    invited_by: t.Optional['models.ComAtprotoServerDefs.InviteCode'] = None  #: Invited by.
    invites: t.Optional[t.List['models.ComAtprotoServerDefs.InviteCode']] = None  #: Invites.
    invites_disabled: t.Optional[bool] = None  #: Invites disabled.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    threat_signatures: t.Optional[t.List['models.ComAtprotoAdminDefs.ThreatSignature']] = None  #: Threat signatures.

    py_type: t.Literal['tools.ozone.moderation.defs#repoViewDetail'] = Field(
        default='tools.ozone.moderation.defs#repoViewDetail', alias='$type', frozen=True
    )


class RepoViewNotFound(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['tools.ozone.moderation.defs#repoViewNotFound'] = Field(
        default='tools.ozone.moderation.defs#repoViewNotFound', alias='$type', frozen=True
    )


class RecordView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    blob_cids: t.List[string_formats.Cid]  #: Blob cids.
    cid: string_formats.Cid  #: Cid.
    indexed_at: string_formats.DateTime  #: Indexed at.
    moderation: 'models.ToolsOzoneModerationDefs.Moderation'  #: Moderation.
    repo: 'models.ToolsOzoneModerationDefs.RepoView'  #: Repo.
    uri: string_formats.AtUri  #: Uri.
    value: 'UnknownType'  #: Value.

    py_type: t.Literal['tools.ozone.moderation.defs#recordView'] = Field(
        default='tools.ozone.moderation.defs#recordView', alias='$type', frozen=True
    )


class RecordViewDetail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    blobs: t.List['models.ToolsOzoneModerationDefs.BlobView']  #: Blobs.
    cid: string_formats.Cid  #: Cid.
    indexed_at: string_formats.DateTime  #: Indexed at.
    moderation: 'models.ToolsOzoneModerationDefs.ModerationDetail'  #: Moderation.
    repo: 'models.ToolsOzoneModerationDefs.RepoView'  #: Repo.
    uri: string_formats.AtUri  #: Uri.
    value: 'UnknownType'  #: Value.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.

    py_type: t.Literal['tools.ozone.moderation.defs#recordViewDetail'] = Field(
        default='tools.ozone.moderation.defs#recordViewDetail', alias='$type', frozen=True
    )


class RecordViewNotFound(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    uri: string_formats.AtUri  #: Uri.

    py_type: t.Literal['tools.ozone.moderation.defs#recordViewNotFound'] = Field(
        default='tools.ozone.moderation.defs#recordViewNotFound', alias='$type', frozen=True
    )


class Moderation(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    subject_status: t.Optional['models.ToolsOzoneModerationDefs.SubjectStatusView'] = None  #: Subject status.

    py_type: t.Literal['tools.ozone.moderation.defs#moderation'] = Field(
        default='tools.ozone.moderation.defs#moderation', alias='$type', frozen=True
    )


class ModerationDetail(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    subject_status: t.Optional['models.ToolsOzoneModerationDefs.SubjectStatusView'] = None  #: Subject status.

    py_type: t.Literal['tools.ozone.moderation.defs#moderationDetail'] = Field(
        default='tools.ozone.moderation.defs#moderationDetail', alias='$type', frozen=True
    )


class BlobView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    cid: string_formats.Cid  #: Cid.
    created_at: string_formats.DateTime  #: Created at.
    mime_type: str  #: Mime type.
    size: int  #: Size.
    details: t.Optional[
        te.Annotated[
            t.Union['models.ToolsOzoneModerationDefs.ImageDetails', 'models.ToolsOzoneModerationDefs.VideoDetails'],
            Field(discriminator='py_type'),
        ]
    ] = None  #: Details.
    moderation: t.Optional['models.ToolsOzoneModerationDefs.Moderation'] = None  #: Moderation.

    py_type: t.Literal['tools.ozone.moderation.defs#blobView'] = Field(
        default='tools.ozone.moderation.defs#blobView', alias='$type', frozen=True
    )


class ImageDetails(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    height: int  #: Height.
    width: int  #: Width.

    py_type: t.Literal['tools.ozone.moderation.defs#imageDetails'] = Field(
        default='tools.ozone.moderation.defs#imageDetails', alias='$type', frozen=True
    )


class VideoDetails(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    height: int  #: Height.
    length: int  #: Length.
    width: int  #: Width.

    py_type: t.Literal['tools.ozone.moderation.defs#videoDetails'] = Field(
        default='tools.ozone.moderation.defs#videoDetails', alias='$type', frozen=True
    )


class AccountHosting(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    status: t.Union[
        t.Literal['takendown'],
        t.Literal['suspended'],
        t.Literal['deleted'],
        t.Literal['deactivated'],
        t.Literal['unknown'],
        str,
    ]  #: Status.
    created_at: t.Optional[string_formats.DateTime] = None  #: Created at.
    deactivated_at: t.Optional[string_formats.DateTime] = None  #: Deactivated at.
    deleted_at: t.Optional[string_formats.DateTime] = None  #: Deleted at.
    reactivated_at: t.Optional[string_formats.DateTime] = None  #: Reactivated at.
    updated_at: t.Optional[string_formats.DateTime] = None  #: Updated at.

    py_type: t.Literal['tools.ozone.moderation.defs#accountHosting'] = Field(
        default='tools.ozone.moderation.defs#accountHosting', alias='$type', frozen=True
    )


class RecordHosting(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    status: t.Union[t.Literal['deleted'], t.Literal['unknown'], str]  #: Status.
    created_at: t.Optional[string_formats.DateTime] = None  #: Created at.
    deleted_at: t.Optional[string_formats.DateTime] = None  #: Deleted at.
    updated_at: t.Optional[string_formats.DateTime] = None  #: Updated at.

    py_type: t.Literal['tools.ozone.moderation.defs#recordHosting'] = Field(
        default='tools.ozone.moderation.defs#recordHosting', alias='$type', frozen=True
    )


class ReporterStats(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`."""

    account_report_count: int  #: The total number of reports made by the user on accounts.
    did: string_formats.Did  #: Did.
    labeled_account_count: int  #: The total number of accounts labeled as a result of the user's reports.
    labeled_record_count: int  #: The total number of records labeled as a result of the user's reports.
    record_report_count: int  #: The total number of reports made by the user on records.
    reported_account_count: int  #: The total number of accounts reported by the user.
    reported_record_count: int  #: The total number of records reported by the user.
    takendown_account_count: int  #: The total number of accounts taken down as a result of the user's reports.
    takendown_record_count: int  #: The total number of records taken down as a result of the user's reports.

    py_type: t.Literal['tools.ozone.moderation.defs#reporterStats'] = Field(
        default='tools.ozone.moderation.defs#reporterStats', alias='$type', frozen=True
    )


class ModTool(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. Moderation tool information for tracing the source of the action."""

    name: str  #: Name/identifier of the source (e.g., 'automod', 'ozone/workspace').
    meta: t.Optional['UnknownType'] = None  #: Additional arbitrary metadata about the source.

    py_type: t.Literal['tools.ozone.moderation.defs#modTool'] = Field(
        default='tools.ozone.moderation.defs#modTool', alias='$type', frozen=True
    )


TimelineEventPlcCreate = t.Literal[
    'tools.ozone.moderation.defs#timelineEventPlcCreate'
]  #: Moderation event timeline event for a PLC create operation

TimelineEventPlcOperation = t.Literal[
    'tools.ozone.moderation.defs#timelineEventPlcOperation'
]  #: Moderation event timeline event for generic PLC operation

TimelineEventPlcTombstone = t.Literal[
    'tools.ozone.moderation.defs#timelineEventPlcTombstone'
]  #: Moderation event timeline event for a PLC tombstone operation


class ScheduledActionView(base.ModelBase):
    """Definition model for :obj:`tools.ozone.moderation.defs`. View of a scheduled moderation action."""

    action: t.Union[t.Literal['takedown'], str]  #: Type of action to be executed.
    created_at: string_formats.DateTime  #: When the scheduled action was created.
    created_by: string_formats.Did  #: DID of the user who created this scheduled action.
    did: string_formats.Did  #: Subject DID for the action.
    id: int  #: Auto-incrementing row ID.
    status: t.Union[
        t.Literal['pending'], t.Literal['executed'], t.Literal['cancelled'], t.Literal['failed'], str
    ]  #: Current status of the scheduled action.
    event_data: t.Optional['UnknownType'] = (
        None  #: Serialized event object that will be propagated to the event when performed.
    )
    execute_after: t.Optional[string_formats.DateTime] = (
        None  #: Earliest time to execute the action (for randomized scheduling).
    )
    execute_at: t.Optional[string_formats.DateTime] = None  #: Exact time to execute the action.
    execute_until: t.Optional[string_formats.DateTime] = (
        None  #: Latest time to execute the action (for randomized scheduling).
    )
    execution_event_id: t.Optional[int] = (
        None  #: ID of the moderation event created when action was successfully executed.
    )
    last_executed_at: t.Optional[string_formats.DateTime] = None  #: When the action was last attempted to be executed.
    last_failure_reason: t.Optional[str] = None  #: Reason for the last execution failure.
    randomize_execution: t.Optional[bool] = (
        None  #: Whether execution time should be randomized within the specified range.
    )
    updated_at: t.Optional[string_formats.DateTime] = None  #: When the scheduled action was last updated.

    py_type: t.Literal['tools.ozone.moderation.defs#scheduledActionView'] = Field(
        default='tools.ozone.moderation.defs#scheduledActionView', alias='$type', frozen=True
    )

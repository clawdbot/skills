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
    """Parameters model for :obj:`tools.ozone.moderation.queryStatuses`."""

    age_assurance_state: t.Optional[
        t.Union[
            t.Literal['pending'],
            t.Literal['assured'],
            t.Literal['unknown'],
            t.Literal['reset'],
            t.Literal['blocked'],
            str,
        ]
    ] = None  #: If specified, only subjects with the given age assurance state will be returned.
    appealed: t.Optional[bool] = None  #: Get subjects in unresolved appealed status.
    collections: te.Annotated[t.Optional[t.List[string_formats.Nsid]], Field(max_length=20)] = (
        None  #: If specified, subjects belonging to the given collections will be returned. When subjectType is set to 'account', this will be ignored.
    )
    comment: t.Optional[str] = None  #: Search subjects by keyword from comments.
    cursor: t.Optional[str] = None  #: Cursor.
    exclude_tags: t.Optional[t.List[str]] = None  #: Exclude tags.
    hosting_deleted_after: t.Optional[string_formats.DateTime] = (
        None  #: Search subjects where the associated record/account was deleted after a given timestamp.
    )
    hosting_deleted_before: t.Optional[string_formats.DateTime] = (
        None  #: Search subjects where the associated record/account was deleted before a given timestamp.
    )
    hosting_statuses: t.Optional[t.List[str]] = None  #: Search subjects by the status of the associated record/account.
    hosting_updated_after: t.Optional[string_formats.DateTime] = (
        None  #: Search subjects where the associated record/account was updated after a given timestamp.
    )
    hosting_updated_before: t.Optional[string_formats.DateTime] = (
        None  #: Search subjects where the associated record/account was updated before a given timestamp.
    )
    ignore_subjects: t.Optional[t.List[string_formats.Uri]] = None  #: Ignore subjects.
    include_all_user_records: t.Optional[bool] = (
        None  #: All subjects, or subjects from given 'collections' param, belonging to the account specified in the 'subject' param will be returned.
    )
    include_muted: t.Optional[bool] = (
        None  #: By default, we don't include muted subjects in the results. Set this to true to include them.
    )
    last_reviewed_by: t.Optional[string_formats.Did] = (
        None  #: Get all subject statuses that were reviewed by a specific moderator.
    )
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    min_account_suspend_count: t.Optional[int] = (
        None  #: If specified, only subjects that belong to an account that has at least this many suspensions will be returned.
    )
    min_priority_score: te.Annotated[t.Optional[int], Field(ge=0, le=100)] = (
        None  #: If specified, only subjects that have priority score value above the given value will be returned.
    )
    min_reported_records_count: t.Optional[int] = (
        None  #: If specified, only subjects that belong to an account that has at least this many reported records will be returned.
    )
    min_strike_count: te.Annotated[t.Optional[int], Field(ge=1)] = (
        None  #: If specified, only subjects that belong to an account that has at least this many active strikes will be returned.
    )
    min_takendown_records_count: t.Optional[int] = (
        None  #: If specified, only subjects that belong to an account that has at least this many taken down records will be returned.
    )
    only_muted: t.Optional[bool] = None  #: When set to true, only muted subjects and reporters will be returned.
    queue_count: t.Optional[int] = (
        None  #: Number of queues being used by moderators. Subjects will be split among all queues.
    )
    queue_index: t.Optional[int] = (
        None  #: Index of the queue to fetch subjects from. Works only when queueCount value is specified.
    )
    queue_seed: t.Optional[str] = None  #: A seeder to shuffle/balance the queue items.
    reported_after: t.Optional[string_formats.DateTime] = None  #: Search subjects reported after a given timestamp.
    reported_before: t.Optional[string_formats.DateTime] = None  #: Search subjects reported before a given timestamp.
    review_state: t.Optional[
        t.Union[
            'models.ToolsOzoneModerationDefs.ReviewOpen',
            'models.ToolsOzoneModerationDefs.ReviewClosed',
            'models.ToolsOzoneModerationDefs.ReviewEscalated',
            'models.ToolsOzoneModerationDefs.ReviewNone',
            str,
        ]
    ] = None  #: Specify when fetching subjects in a certain state.
    reviewed_after: t.Optional[string_formats.DateTime] = None  #: Search subjects reviewed after a given timestamp.
    reviewed_before: t.Optional[string_formats.DateTime] = None  #: Search subjects reviewed before a given timestamp.
    sort_direction: t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]] = 'desc'  #: Sort direction.
    sort_field: t.Optional[
        t.Union[
            t.Literal['lastReviewedAt'],
            t.Literal['lastReportedAt'],
            t.Literal['reportedRecordsCount'],
            t.Literal['takendownRecordsCount'],
            t.Literal['priorityScore'],
        ]
    ] = 'lastReportedAt'  #: Sort field.
    subject: t.Optional[string_formats.Uri] = None  #: The subject to get the status for.
    subject_type: t.Optional[t.Union[t.Literal['account'], t.Literal['record'], str]] = (
        None  #: If specified, subjects of the given type (account or record) will be returned. When this is set to 'account' the 'collections' parameter will be ignored. When includeAllUserRecords or subject is set, this will be ignored.
    )
    tags: te.Annotated[t.Optional[t.List[str]], Field(max_length=25)] = (
        None  #: Tags. Items in this array are applied with OR filters. To apply AND filter, put all tags in the same string and separate using && characters.
    )
    takendown: t.Optional[bool] = None  #: Get subjects that were taken down.


class ParamsDict(t.TypedDict):
    age_assurance_state: te.NotRequired[
        t.Optional[
            t.Union[
                t.Literal['pending'],
                t.Literal['assured'],
                t.Literal['unknown'],
                t.Literal['reset'],
                t.Literal['blocked'],
                str,
            ]
        ]
    ]  #: If specified, only subjects with the given age assurance state will be returned.
    appealed: te.NotRequired[t.Optional[bool]]  #: Get subjects in unresolved appealed status.
    collections: te.NotRequired[
        t.Optional[t.List[string_formats.Nsid]]
    ]  #: If specified, subjects belonging to the given collections will be returned. When subjectType is set to 'account', this will be ignored.
    comment: te.NotRequired[t.Optional[str]]  #: Search subjects by keyword from comments.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    exclude_tags: te.NotRequired[t.Optional[t.List[str]]]  #: Exclude tags.
    hosting_deleted_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects where the associated record/account was deleted after a given timestamp.
    hosting_deleted_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects where the associated record/account was deleted before a given timestamp.
    hosting_statuses: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: Search subjects by the status of the associated record/account.
    hosting_updated_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects where the associated record/account was updated after a given timestamp.
    hosting_updated_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects where the associated record/account was updated before a given timestamp.
    ignore_subjects: te.NotRequired[t.Optional[t.List[string_formats.Uri]]]  #: Ignore subjects.
    include_all_user_records: te.NotRequired[
        t.Optional[bool]
    ]  #: All subjects, or subjects from given 'collections' param, belonging to the account specified in the 'subject' param will be returned.
    include_muted: te.NotRequired[
        t.Optional[bool]
    ]  #: By default, we don't include muted subjects in the results. Set this to true to include them.
    last_reviewed_by: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: Get all subject statuses that were reviewed by a specific moderator.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    min_account_suspend_count: te.NotRequired[
        t.Optional[int]
    ]  #: If specified, only subjects that belong to an account that has at least this many suspensions will be returned.
    min_priority_score: te.NotRequired[
        t.Optional[int]
    ]  #: If specified, only subjects that have priority score value above the given value will be returned.
    min_reported_records_count: te.NotRequired[
        t.Optional[int]
    ]  #: If specified, only subjects that belong to an account that has at least this many reported records will be returned.
    min_strike_count: te.NotRequired[
        t.Optional[int]
    ]  #: If specified, only subjects that belong to an account that has at least this many active strikes will be returned.
    min_takendown_records_count: te.NotRequired[
        t.Optional[int]
    ]  #: If specified, only subjects that belong to an account that has at least this many taken down records will be returned.
    only_muted: te.NotRequired[
        t.Optional[bool]
    ]  #: When set to true, only muted subjects and reporters will be returned.
    queue_count: te.NotRequired[
        t.Optional[int]
    ]  #: Number of queues being used by moderators. Subjects will be split among all queues.
    queue_index: te.NotRequired[
        t.Optional[int]
    ]  #: Index of the queue to fetch subjects from. Works only when queueCount value is specified.
    queue_seed: te.NotRequired[t.Optional[str]]  #: A seeder to shuffle/balance the queue items.
    reported_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects reported after a given timestamp.
    reported_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects reported before a given timestamp.
    review_state: te.NotRequired[
        t.Optional[
            t.Union[
                'models.ToolsOzoneModerationDefs.ReviewOpen',
                'models.ToolsOzoneModerationDefs.ReviewClosed',
                'models.ToolsOzoneModerationDefs.ReviewEscalated',
                'models.ToolsOzoneModerationDefs.ReviewNone',
                str,
            ]
        ]
    ]  #: Specify when fetching subjects in a certain state.
    reviewed_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects reviewed after a given timestamp.
    reviewed_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Search subjects reviewed before a given timestamp.
    sort_direction: te.NotRequired[t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]]]  #: Sort direction.
    sort_field: te.NotRequired[
        t.Optional[
            t.Union[
                t.Literal['lastReviewedAt'],
                t.Literal['lastReportedAt'],
                t.Literal['reportedRecordsCount'],
                t.Literal['takendownRecordsCount'],
                t.Literal['priorityScore'],
            ]
        ]
    ]  #: Sort field.
    subject: te.NotRequired[t.Optional[string_formats.Uri]]  #: The subject to get the status for.
    subject_type: te.NotRequired[
        t.Optional[t.Union[t.Literal['account'], t.Literal['record'], str]]
    ]  #: If specified, subjects of the given type (account or record) will be returned. When this is set to 'account' the 'collections' parameter will be ignored. When includeAllUserRecords or subject is set, this will be ignored.
    tags: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: Tags. Items in this array are applied with OR filters. To apply AND filter, put all tags in the same string and separate using && characters.
    takendown: te.NotRequired[t.Optional[bool]]  #: Get subjects that were taken down.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.queryStatuses`."""

    subject_statuses: t.List['models.ToolsOzoneModerationDefs.SubjectStatusView']  #: Subject statuses.
    cursor: t.Optional[str] = None  #: Cursor.

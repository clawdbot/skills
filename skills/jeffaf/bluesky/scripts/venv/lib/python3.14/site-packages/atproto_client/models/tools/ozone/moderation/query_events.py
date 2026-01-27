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
    """Parameters model for :obj:`tools.ozone.moderation.queryEvents`."""

    added_labels: t.Optional[t.List[str]] = (
        None  #: If specified, only events where all of these labels were added are returned.
    )
    added_tags: t.Optional[t.List[str]] = (
        None  #: If specified, only events where all of these tags were added are returned.
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
    ] = None  #: If specified, only events where the age assurance state matches the given value are returned.
    batch_id: t.Optional[str] = (
        None  #: If specified, only events where the batchId matches the given value are returned.
    )
    collections: te.Annotated[t.Optional[t.List[string_formats.Nsid]], Field(max_length=20)] = (
        None  #: If specified, only events where the subject belongs to the given collections will be returned. When subjectType is set to 'account', this will be ignored.
    )
    comment: t.Optional[str] = (
        None  #: If specified, only events with comments containing the keyword are returned. Apply || separator to use multiple keywords and match using OR condition.
    )
    created_after: t.Optional[string_formats.DateTime] = None  #: Retrieve events created after a given timestamp.
    created_before: t.Optional[string_formats.DateTime] = None  #: Retrieve events created before a given timestamp.
    created_by: t.Optional[string_formats.Did] = None  #: Created by.
    cursor: t.Optional[str] = None  #: Cursor.
    has_comment: t.Optional[bool] = None  #: If true, only events with comments are returned.
    include_all_user_records: t.Optional[bool] = (
        False  #: If true, events on all record types (posts, lists, profile etc.) or records from given 'collections' param, owned by the did are returned.
    )
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    mod_tool: t.Optional[t.List[str]] = (
        None  #: If specified, only events where the modTool name matches any of the given values are returned.
    )
    policies: t.Optional[t.List[str]] = (
        None  #: Policies. If specified, only events where the action policies match any of the given policies are returned.
    )
    removed_labels: t.Optional[t.List[str]] = (
        None  #: If specified, only events where all of these labels were removed are returned.
    )
    removed_tags: t.Optional[t.List[str]] = (
        None  #: If specified, only events where all of these tags were removed are returned.
    )
    report_types: t.Optional[t.List[str]] = None  #: Report types.
    sort_direction: t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]] = (
        'desc'  #: Sort direction for the events. Defaults to descending order of created at timestamp.
    )
    subject: t.Optional[string_formats.Uri] = None  #: Subject.
    subject_type: t.Optional[t.Union[t.Literal['account'], t.Literal['record'], str]] = (
        None  #: If specified, only events where the subject is of the given type (account or record) will be returned. When this is set to 'account' the 'collections' parameter will be ignored. When includeAllUserRecords or subject is set, this will be ignored.
    )
    types: t.Optional[t.List[str]] = (
        None  #: The types of events (fully qualified string in the format of tools.ozone.moderation.defs#modEvent<name>) to filter by. If not specified, all events are returned.
    )
    with_strike: t.Optional[bool] = None  #: If specified, only events where strikeCount value is set are returned.


class ParamsDict(t.TypedDict):
    added_labels: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: If specified, only events where all of these labels were added are returned.
    added_tags: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: If specified, only events where all of these tags were added are returned.
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
    ]  #: If specified, only events where the age assurance state matches the given value are returned.
    batch_id: te.NotRequired[
        t.Optional[str]
    ]  #: If specified, only events where the batchId matches the given value are returned.
    collections: te.NotRequired[
        t.Optional[t.List[string_formats.Nsid]]
    ]  #: If specified, only events where the subject belongs to the given collections will be returned. When subjectType is set to 'account', this will be ignored.
    comment: te.NotRequired[
        t.Optional[str]
    ]  #: If specified, only events with comments containing the keyword are returned. Apply || separator to use multiple keywords and match using OR condition.
    created_after: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Retrieve events created after a given timestamp.
    created_before: te.NotRequired[
        t.Optional[string_formats.DateTime]
    ]  #: Retrieve events created before a given timestamp.
    created_by: te.NotRequired[t.Optional[string_formats.Did]]  #: Created by.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    has_comment: te.NotRequired[t.Optional[bool]]  #: If true, only events with comments are returned.
    include_all_user_records: te.NotRequired[
        t.Optional[bool]
    ]  #: If true, events on all record types (posts, lists, profile etc.) or records from given 'collections' param, owned by the did are returned.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    mod_tool: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: If specified, only events where the modTool name matches any of the given values are returned.
    policies: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: Policies. If specified, only events where the action policies match any of the given policies are returned.
    removed_labels: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: If specified, only events where all of these labels were removed are returned.
    removed_tags: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: If specified, only events where all of these tags were removed are returned.
    report_types: te.NotRequired[t.Optional[t.List[str]]]  #: Report types.
    sort_direction: te.NotRequired[
        t.Optional[t.Union[t.Literal['asc'], t.Literal['desc']]]
    ]  #: Sort direction for the events. Defaults to descending order of created at timestamp.
    subject: te.NotRequired[t.Optional[string_formats.Uri]]  #: Subject.
    subject_type: te.NotRequired[
        t.Optional[t.Union[t.Literal['account'], t.Literal['record'], str]]
    ]  #: If specified, only events where the subject is of the given type (account or record) will be returned. When this is set to 'account' the 'collections' parameter will be ignored. When includeAllUserRecords or subject is set, this will be ignored.
    types: te.NotRequired[
        t.Optional[t.List[str]]
    ]  #: The types of events (fully qualified string in the format of tools.ozone.moderation.defs#modEvent<name>) to filter by. If not specified, all events are returned.
    with_strike: te.NotRequired[
        t.Optional[bool]
    ]  #: If specified, only events where strikeCount value is set are returned.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.queryEvents`."""

    events: t.List['models.ToolsOzoneModerationDefs.ModEventView']  #: Events.
    cursor: t.Optional[str] = None  #: Cursor.

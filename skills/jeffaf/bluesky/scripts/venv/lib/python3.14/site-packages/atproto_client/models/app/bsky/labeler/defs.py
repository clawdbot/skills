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


class LabelerView(base.ModelBase):
    """Definition model for :obj:`app.bsky.labeler.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileView'  #: Creator.
    indexed_at: string_formats.DateTime  #: Indexed at.
    uri: string_formats.AtUri  #: Uri.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    like_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Like count.
    viewer: t.Optional['models.AppBskyLabelerDefs.LabelerViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.labeler.defs#labelerView'] = Field(
        default='app.bsky.labeler.defs#labelerView', alias='$type', frozen=True
    )


class LabelerViewDetailed(base.ModelBase):
    """Definition model for :obj:`app.bsky.labeler.defs`."""

    cid: string_formats.Cid  #: Cid.
    creator: 'models.AppBskyActorDefs.ProfileView'  #: Creator.
    indexed_at: string_formats.DateTime  #: Indexed at.
    policies: 'models.AppBskyLabelerDefs.LabelerPolicies'  #: Policies.
    uri: string_formats.AtUri  #: Uri.
    labels: t.Optional[t.List['models.ComAtprotoLabelDefs.Label']] = None  #: Labels.
    like_count: te.Annotated[t.Optional[int], Field(ge=0)] = None  #: Like count.
    reason_types: t.Optional[t.List['models.ComAtprotoModerationDefs.ReasonType']] = (
        None  #: The set of report reason 'codes' which are in-scope for this service to review and action. These usually align to policy categories. If not defined (distinct from empty array), all reason types are allowed.
    )
    subject_collections: t.Optional[t.List[string_formats.Nsid]] = (
        None  #: Set of record types (collection NSIDs) which can be reported to this service. If not defined (distinct from empty array), default is any record type.
    )
    subject_types: t.Optional[t.List['models.ComAtprotoModerationDefs.SubjectType']] = (
        None  #: The set of subject types (account, record, etc) this service accepts reports on.
    )
    viewer: t.Optional['models.AppBskyLabelerDefs.LabelerViewerState'] = None  #: Viewer.

    py_type: t.Literal['app.bsky.labeler.defs#labelerViewDetailed'] = Field(
        default='app.bsky.labeler.defs#labelerViewDetailed', alias='$type', frozen=True
    )


class LabelerViewerState(base.ModelBase):
    """Definition model for :obj:`app.bsky.labeler.defs`."""

    like: t.Optional[string_formats.AtUri] = None  #: Like.

    py_type: t.Literal['app.bsky.labeler.defs#labelerViewerState'] = Field(
        default='app.bsky.labeler.defs#labelerViewerState', alias='$type', frozen=True
    )


class LabelerPolicies(base.ModelBase):
    """Definition model for :obj:`app.bsky.labeler.defs`."""

    label_values: t.List[
        'models.ComAtprotoLabelDefs.LabelValue'
    ]  #: The label values which this labeler publishes. May include global or custom labels.
    label_value_definitions: t.Optional[t.List['models.ComAtprotoLabelDefs.LabelValueDefinition']] = (
        None  #: Label values created by this labeler and scoped exclusively to it. Labels defined here will override global label definitions for this labeler.
    )

    py_type: t.Literal['app.bsky.labeler.defs#labelerPolicies'] = Field(
        default='app.bsky.labeler.defs#labelerPolicies', alias='$type', frozen=True
    )

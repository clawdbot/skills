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


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.labeler.service`."""

    created_at: string_formats.DateTime  #: Created at.
    policies: 'models.AppBskyLabelerDefs.LabelerPolicies'  #: Policies.
    labels: t.Optional[
        te.Annotated[t.Union['models.ComAtprotoLabelDefs.SelfLabels'], Field(discriminator='py_type')]
    ] = None  #: Labels.
    reason_types: t.Optional[t.List['models.ComAtprotoModerationDefs.ReasonType']] = (
        None  #: The set of report reason 'codes' which are in-scope for this service to review and action. These usually align to policy categories. If not defined (distinct from empty array), all reason types are allowed.
    )
    subject_collections: t.Optional[t.List[string_formats.Nsid]] = (
        None  #: Set of record types (collection NSIDs) which can be reported to this service. If not defined (distinct from empty array), default is any record type.
    )
    subject_types: t.Optional[t.List['models.ComAtprotoModerationDefs.SubjectType']] = (
        None  #: The set of subject types (account, record, etc) this service accepts reports on.
    )

    py_type: t.Literal['app.bsky.labeler.service'] = Field(
        default='app.bsky.labeler.service', alias='$type', frozen=True
    )


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyLabelerService.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyLabelerService.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyLabelerService.Record`."""

    records: t.Dict[str, 'models.AppBskyLabelerService.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyLabelerService.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

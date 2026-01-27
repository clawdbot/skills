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


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.graph.verification`."""

    created_at: string_formats.DateTime  #: Date of when the verification was created.
    display_name: str  #: Display name of the subject the verification applies to at the moment of verifying, which might not be the same at the time of viewing. The verification is only valid if the current displayName matches the one at the time of verifying.
    handle: string_formats.Handle  #: Handle of the subject the verification applies to at the moment of verifying, which might not be the same at the time of viewing. The verification is only valid if the current handle matches the one at the time of verifying.
    subject: string_formats.Did  #: DID of the subject the verification applies to.

    py_type: t.Literal['app.bsky.graph.verification'] = Field(
        default='app.bsky.graph.verification', alias='$type', frozen=True
    )


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyGraphVerification.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyGraphVerification.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyGraphVerification.Record`."""

    records: t.Dict[str, 'models.AppBskyGraphVerification.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyGraphVerification.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

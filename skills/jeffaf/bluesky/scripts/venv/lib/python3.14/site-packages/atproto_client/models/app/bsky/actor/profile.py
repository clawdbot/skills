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
    from atproto_client.models.blob_ref import BlobRef
from atproto_client.models import base


class Record(base.RecordModelBase):
    """Record model for :obj:`app.bsky.actor.profile`."""

    avatar: t.Optional['BlobRef'] = (
        None  #: Small image to be displayed next to posts from account. AKA, 'profile picture'.
    )
    banner: t.Optional['BlobRef'] = None  #: Larger horizontal image to display behind profile view.
    created_at: t.Optional[string_formats.DateTime] = None  #: Created at.
    description: te.Annotated[t.Optional[str], Field(max_length=2560)] = None  #: Free-form profile description text.
    display_name: te.Annotated[t.Optional[str], Field(max_length=640)] = None  #: Display name.
    joined_via_starter_pack: t.Optional['models.ComAtprotoRepoStrongRef.Main'] = None  #: Joined via starter pack.
    labels: t.Optional[
        te.Annotated[t.Union['models.ComAtprotoLabelDefs.SelfLabels'], Field(discriminator='py_type')]
    ] = None  #: Self-label values, specific to the Bluesky application, on the overall account.
    pinned_post: t.Optional['models.ComAtprotoRepoStrongRef.Main'] = None  #: Pinned post.
    pronouns: te.Annotated[t.Optional[str], Field(max_length=200)] = None  #: Free-form pronouns text.
    website: t.Optional[string_formats.Uri] = None  #: Website.

    py_type: t.Literal['app.bsky.actor.profile'] = Field(default='app.bsky.actor.profile', alias='$type', frozen=True)


class GetRecordResponse(base.SugarResponseModelBase):
    """Get record response for :obj:`models.AppBskyActorProfile.Record`."""

    uri: str  #: The URI of the record.
    value: 'models.AppBskyActorProfile.Record'  #: The record.
    cid: t.Optional[str] = None  #: The CID of the record.


class ListRecordsResponse(base.SugarResponseModelBase):
    """List records response for :obj:`models.AppBskyActorProfile.Record`."""

    records: t.Dict[str, 'models.AppBskyActorProfile.Record']  #: Map of URIs to records.
    cursor: t.Optional[str] = None  #: Next page cursor.


class CreateRecordResponse(base.SugarResponseModelBase):
    """Create record response for :obj:`models.AppBskyActorProfile.Record`."""

    uri: str  #: The URI of the record.
    cid: str  #: The CID of the record.

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
    from atproto_core.cid import CIDType

    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`com.atproto.sync.subscribeRepos`."""

    cursor: t.Optional[int] = None  #: The last known event seq number to backfill from.


class ParamsDict(t.TypedDict):
    cursor: te.NotRequired[t.Optional[int]]  #: The last known event seq number to backfill from.


class Commit(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`. Represents an update of repository state. Note that empty commits are allowed, which include no repo data changes, but an update to rev and signature."""

    blobs: t.List[
        'CIDType'
    ]  #: Blobs. DEPRECATED -- will soon always be empty. List of new blobs (by CID) referenced by records in this commit.
    blocks: t.Union[
        str, bytes
    ]  #: CAR file containing relevant blocks, as a diff since the previous repo state. The commit must be included as a block, and the commit block CID must be the first entry in the CAR header 'roots' list.
    commit: 'CIDType'  #: Repo commit object CID.
    ops: t.List['models.ComAtprotoSyncSubscribeRepos.RepoOp'] = Field(
        max_length=200
    )  #: Ops. List of repo mutation operations in this commit (eg, records created, updated, or deleted).
    rebase: bool  #: DEPRECATED -- unused.
    repo: (
        string_formats.Did
    )  #: The repo this event comes from. Note that all other message types name this field 'did'.
    rev: string_formats.Tid  #: The rev of the emitted commit. Note that this information is also in the commit object included in blocks, unless this is a tooBig event.
    seq: int  #: The stream sequence number of this message.
    time: string_formats.DateTime  #: Timestamp of when this message was originally broadcast.
    too_big: bool  #: DEPRECATED -- replaced by #sync event and data limits. Indicates that this commit contained too many ops, or data size was too large. Consumers will need to make a separate request to get missing data.
    prev_data: t.Optional['CIDType'] = (
        None  #: The root CID of the MST tree for the previous commit from this repo (indicated by the 'since' revision field in this message). Corresponds to the 'data' field in the repo commit object. NOTE: this field is effectively required for the 'inductive' version of firehose.
    )
    since: t.Optional[string_formats.Tid] = None  #: The rev of the last emitted commit from this repo (if any).

    py_type: t.Literal['com.atproto.sync.subscribeRepos#commit'] = Field(
        default='com.atproto.sync.subscribeRepos#commit', alias='$type', frozen=True
    )


class Sync(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`. Updates the repo to a new state, without necessarily including that state on the firehose. Used to recover from broken commit streams, data loss incidents, or in situations where upstream host does not know recent state of the repository."""

    blocks: t.Union[
        str, bytes
    ]  #: CAR file containing the commit, as a block. The CAR header must include the commit block CID as the first 'root'.
    did: string_formats.Did  #: The account this repo event corresponds to. Must match that in the commit object.
    rev: str  #: The rev of the commit. This value must match that in the commit object.
    seq: int  #: The stream sequence number of this message.
    time: string_formats.DateTime  #: Timestamp of when this message was originally broadcast.

    py_type: t.Literal['com.atproto.sync.subscribeRepos#sync'] = Field(
        default='com.atproto.sync.subscribeRepos#sync', alias='$type', frozen=True
    )


class Identity(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`. Represents a change to an account's identity. Could be an updated handle, signing key, or pds hosting endpoint. Serves as a prod to all downstream services to refresh their identity cache."""

    did: string_formats.Did  #: Did.
    seq: int  #: Seq.
    time: string_formats.DateTime  #: Time.
    handle: t.Optional[string_formats.Handle] = (
        None  #: The current handle for the account, or 'handle.invalid' if validation fails. This field is optional, might have been validated or passed-through from an upstream source. Semantics and behaviors for PDS vs Relay may evolve in the future; see atproto specs for more details.
    )

    py_type: t.Literal['com.atproto.sync.subscribeRepos#identity'] = Field(
        default='com.atproto.sync.subscribeRepos#identity', alias='$type', frozen=True
    )


class Account(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`. Represents a change to an account's status on a host (eg, PDS or Relay). The semantics of this event are that the status is at the host which emitted the event, not necessarily that at the currently active PDS. Eg, a Relay takedown would emit a takedown with active=false, even if the PDS is still active."""

    active: (
        bool  #: Indicates that the account has a repository which can be fetched from the host that emitted this event.
    )
    did: string_formats.Did  #: Did.
    seq: int  #: Seq.
    time: string_formats.DateTime  #: Time.
    status: t.Optional[
        t.Union[
            t.Literal['takendown'],
            t.Literal['suspended'],
            t.Literal['deleted'],
            t.Literal['deactivated'],
            t.Literal['desynchronized'],
            t.Literal['throttled'],
            str,
        ]
    ] = None  #: If active=false, this optional field indicates a reason for why the account is not active.

    py_type: t.Literal['com.atproto.sync.subscribeRepos#account'] = Field(
        default='com.atproto.sync.subscribeRepos#account', alias='$type', frozen=True
    )


class Info(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`."""

    name: t.Union[t.Literal['OutdatedCursor'], str]  #: Name.
    message: t.Optional[str] = None  #: Message.

    py_type: t.Literal['com.atproto.sync.subscribeRepos#info'] = Field(
        default='com.atproto.sync.subscribeRepos#info', alias='$type', frozen=True
    )


class RepoOp(base.ModelBase):
    """Definition model for :obj:`com.atproto.sync.subscribeRepos`. A repo operation, ie a mutation of a single record."""

    action: t.Union[t.Literal['create'], t.Literal['update'], t.Literal['delete'], str]  #: Action.
    path: str  #: Path.
    cid: t.Optional['CIDType'] = None  #: For creates and updates, the new record CID. For deletions, null.
    prev: t.Optional['CIDType'] = (
        None  #: For updates and deletes, the previous record CID (required for inductive firehose). For creations, field should not be defined.
    )

    py_type: t.Literal['com.atproto.sync.subscribeRepos#repoOp'] = Field(
        default='com.atproto.sync.subscribeRepos#repoOp', alias='$type', frozen=True
    )

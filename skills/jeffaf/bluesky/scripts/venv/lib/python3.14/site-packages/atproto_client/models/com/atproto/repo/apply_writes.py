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


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.repo.applyWrites`."""

    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    writes: t.List[
        te.Annotated[
            t.Union[
                'models.ComAtprotoRepoApplyWrites.Create',
                'models.ComAtprotoRepoApplyWrites.Update',
                'models.ComAtprotoRepoApplyWrites.Delete',
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: Writes.
    swap_commit: t.Optional[string_formats.Cid] = (
        None  #: If provided, the entire operation will fail if the current repo commit CID does not match this value. Used to prevent conflicting repo mutations.
    )
    validate_: t.Optional[bool] = (
        None  #: Can be set to 'false' to skip Lexicon schema validation of record data across all operations, 'true' to require it, or leave unset to validate only for known Lexicons.
    )


class DataDict(t.TypedDict):
    repo: string_formats.AtIdentifier  #: The handle or DID of the repo (aka, current account).
    writes: t.List[
        te.Annotated[
            t.Union[
                'models.ComAtprotoRepoApplyWrites.Create',
                'models.ComAtprotoRepoApplyWrites.Update',
                'models.ComAtprotoRepoApplyWrites.Delete',
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: Writes.
    swap_commit: te.NotRequired[
        t.Optional[string_formats.Cid]
    ]  #: If provided, the entire operation will fail if the current repo commit CID does not match this value. Used to prevent conflicting repo mutations.
    validate: te.NotRequired[
        t.Optional[bool]
    ]  #: Can be set to 'false' to skip Lexicon schema validation of record data across all operations, 'true' to require it, or leave unset to validate only for known Lexicons.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.repo.applyWrites`."""

    commit: t.Optional['models.ComAtprotoRepoDefs.CommitMeta'] = None  #: Commit.
    results: t.Optional[
        t.List[
            te.Annotated[
                t.Union[
                    'models.ComAtprotoRepoApplyWrites.CreateResult',
                    'models.ComAtprotoRepoApplyWrites.UpdateResult',
                    'models.ComAtprotoRepoApplyWrites.DeleteResult',
                ],
                Field(discriminator='py_type'),
            ]
        ]
    ] = None  #: Results.


class Create(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`. Operation which creates a new record."""

    collection: string_formats.Nsid  #: Collection.
    value: 'UnknownType'  #: Value.
    rkey: te.Annotated[t.Optional[string_formats.RecordKey], Field(max_length=512)] = (
        None  #: NOTE: maxLength is redundant with record-key format. Keeping it temporarily to ensure backwards compatibility.
    )

    py_type: t.Literal['com.atproto.repo.applyWrites#create'] = Field(
        default='com.atproto.repo.applyWrites#create', alias='$type', frozen=True
    )


class Update(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`. Operation which updates an existing record."""

    collection: string_formats.Nsid  #: Collection.
    rkey: string_formats.RecordKey  #: Rkey.
    value: 'UnknownType'  #: Value.

    py_type: t.Literal['com.atproto.repo.applyWrites#update'] = Field(
        default='com.atproto.repo.applyWrites#update', alias='$type', frozen=True
    )


class Delete(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`. Operation which deletes an existing record."""

    collection: string_formats.Nsid  #: Collection.
    rkey: string_formats.RecordKey  #: Rkey.

    py_type: t.Literal['com.atproto.repo.applyWrites#delete'] = Field(
        default='com.atproto.repo.applyWrites#delete', alias='$type', frozen=True
    )


class CreateResult(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`."""

    cid: string_formats.Cid  #: Cid.
    uri: string_formats.AtUri  #: Uri.
    validation_status: t.Optional[t.Union[t.Literal['valid'], t.Literal['unknown'], str]] = None  #: Validation status.

    py_type: t.Literal['com.atproto.repo.applyWrites#createResult'] = Field(
        default='com.atproto.repo.applyWrites#createResult', alias='$type', frozen=True
    )


class UpdateResult(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`."""

    cid: string_formats.Cid  #: Cid.
    uri: string_formats.AtUri  #: Uri.
    validation_status: t.Optional[t.Union[t.Literal['valid'], t.Literal['unknown'], str]] = None  #: Validation status.

    py_type: t.Literal['com.atproto.repo.applyWrites#updateResult'] = Field(
        default='com.atproto.repo.applyWrites#updateResult', alias='$type', frozen=True
    )


class DeleteResult(base.ModelBase):
    """Definition model for :obj:`com.atproto.repo.applyWrites`."""

    py_type: t.Literal['com.atproto.repo.applyWrites#deleteResult'] = Field(
        default='com.atproto.repo.applyWrites#deleteResult', alias='$type', frozen=True
    )

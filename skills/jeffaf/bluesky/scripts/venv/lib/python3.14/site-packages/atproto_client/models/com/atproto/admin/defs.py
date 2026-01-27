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
    from atproto_client.models.unknown_type import UnknownType
from atproto_client.models import base


class StatusAttr(base.ModelBase):
    """Definition model for :obj:`com.atproto.admin.defs`."""

    applied: bool  #: Applied.
    ref: t.Optional[str] = None  #: Ref.

    py_type: t.Literal['com.atproto.admin.defs#statusAttr'] = Field(
        default='com.atproto.admin.defs#statusAttr', alias='$type', frozen=True
    )


class AccountView(base.ModelBase):
    """Definition model for :obj:`com.atproto.admin.defs`."""

    did: string_formats.Did  #: Did.
    handle: string_formats.Handle  #: Handle.
    indexed_at: string_formats.DateTime  #: Indexed at.
    deactivated_at: t.Optional[string_formats.DateTime] = None  #: Deactivated at.
    email: t.Optional[str] = None  #: Email.
    email_confirmed_at: t.Optional[string_formats.DateTime] = None  #: Email confirmed at.
    invite_note: t.Optional[str] = None  #: Invite note.
    invited_by: t.Optional['models.ComAtprotoServerDefs.InviteCode'] = None  #: Invited by.
    invites: t.Optional[t.List['models.ComAtprotoServerDefs.InviteCode']] = None  #: Invites.
    invites_disabled: t.Optional[bool] = None  #: Invites disabled.
    related_records: t.Optional[t.List['UnknownType']] = None  #: Related records.
    threat_signatures: t.Optional[t.List['models.ComAtprotoAdminDefs.ThreatSignature']] = None  #: Threat signatures.

    py_type: t.Literal['com.atproto.admin.defs#accountView'] = Field(
        default='com.atproto.admin.defs#accountView', alias='$type', frozen=True
    )


class RepoRef(base.ModelBase):
    """Definition model for :obj:`com.atproto.admin.defs`."""

    did: string_formats.Did  #: Did.

    py_type: t.Literal['com.atproto.admin.defs#repoRef'] = Field(
        default='com.atproto.admin.defs#repoRef', alias='$type', frozen=True
    )


class RepoBlobRef(base.ModelBase):
    """Definition model for :obj:`com.atproto.admin.defs`."""

    cid: string_formats.Cid  #: Cid.
    did: string_formats.Did  #: Did.
    record_uri: t.Optional[string_formats.AtUri] = None  #: Record uri.

    py_type: t.Literal['com.atproto.admin.defs#repoBlobRef'] = Field(
        default='com.atproto.admin.defs#repoBlobRef', alias='$type', frozen=True
    )


class ThreatSignature(base.ModelBase):
    """Definition model for :obj:`com.atproto.admin.defs`."""

    property: str  #: Property.
    value: str  #: Value.

    py_type: t.Literal['com.atproto.admin.defs#threatSignature'] = Field(
        default='com.atproto.admin.defs#threatSignature', alias='$type', frozen=True
    )

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


class InviteCode(base.ModelBase):
    """Definition model for :obj:`com.atproto.server.defs`."""

    available: int  #: Available.
    code: str  #: Code.
    created_at: string_formats.DateTime  #: Created at.
    created_by: str  #: Created by.
    disabled: bool  #: Disabled.
    for_account: str  #: For account.
    uses: t.List['models.ComAtprotoServerDefs.InviteCodeUse']  #: Uses.

    py_type: t.Literal['com.atproto.server.defs#inviteCode'] = Field(
        default='com.atproto.server.defs#inviteCode', alias='$type', frozen=True
    )


class InviteCodeUse(base.ModelBase):
    """Definition model for :obj:`com.atproto.server.defs`."""

    used_at: string_formats.DateTime  #: Used at.
    used_by: string_formats.Did  #: Used by.

    py_type: t.Literal['com.atproto.server.defs#inviteCodeUse'] = Field(
        default='com.atproto.server.defs#inviteCodeUse', alias='$type', frozen=True
    )

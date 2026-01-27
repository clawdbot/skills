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


class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.listAppPasswords`."""

    passwords: t.List['models.ComAtprotoServerListAppPasswords.AppPassword']  #: Passwords.


class AppPassword(base.ModelBase):
    """Definition model for :obj:`com.atproto.server.listAppPasswords`."""

    created_at: string_formats.DateTime  #: Created at.
    name: str  #: Name.
    privileged: t.Optional[bool] = None  #: Privileged.

    py_type: t.Literal['com.atproto.server.listAppPasswords#appPassword'] = Field(
        default='com.atproto.server.listAppPasswords#appPassword', alias='$type', frozen=True
    )

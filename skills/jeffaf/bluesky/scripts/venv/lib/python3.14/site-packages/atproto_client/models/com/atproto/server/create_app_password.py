##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

from atproto_client.models import base, string_formats


class Data(base.DataModelBase):
    """Input data model for :obj:`com.atproto.server.createAppPassword`."""

    name: str  #: A short name for the App Password, to help distinguish them.
    privileged: t.Optional[bool] = (
        None  #: If an app password has 'privileged' access to possibly sensitive account state. Meant for use with trusted clients.
    )


class DataDict(t.TypedDict):
    name: str  #: A short name for the App Password, to help distinguish them.
    privileged: te.NotRequired[
        t.Optional[bool]
    ]  #: If an app password has 'privileged' access to possibly sensitive account state. Meant for use with trusted clients.


class AppPassword(base.ModelBase):
    """Definition model for :obj:`com.atproto.server.createAppPassword`."""

    created_at: string_formats.DateTime  #: Created at.
    name: str  #: Name.
    password: str  #: Password.
    privileged: t.Optional[bool] = None  #: Privileged.

    py_type: t.Literal['com.atproto.server.createAppPassword#appPassword'] = Field(
        default='com.atproto.server.createAppPassword#appPassword', alias='$type', frozen=True
    )

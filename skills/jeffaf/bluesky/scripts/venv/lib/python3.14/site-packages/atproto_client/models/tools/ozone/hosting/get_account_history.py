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


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    did: string_formats.Did  #: Did.
    cursor: t.Optional[str] = None  #: Cursor.
    events: t.Optional[
        t.List[
            t.Union[
                t.Literal['accountCreated'],
                t.Literal['emailUpdated'],
                t.Literal['emailConfirmed'],
                t.Literal['passwordUpdated'],
                t.Literal['handleUpdated'],
                str,
            ]
        ]
    ] = None  #: Events.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    did: string_formats.Did  #: Did.
    cursor: te.NotRequired[t.Optional[str]]  #: Cursor.
    events: te.NotRequired[
        t.Optional[
            t.List[
                t.Union[
                    t.Literal['accountCreated'],
                    t.Literal['emailUpdated'],
                    t.Literal['emailConfirmed'],
                    t.Literal['passwordUpdated'],
                    t.Literal['handleUpdated'],
                    str,
                ]
            ]
        ]
    ]  #: Events.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    events: t.List['models.ToolsOzoneHostingGetAccountHistory.Event']  #: Events.
    cursor: t.Optional[str] = None  #: Cursor.


class Event(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    created_at: string_formats.DateTime  #: Created at.
    created_by: str  #: Created by.
    details: te.Annotated[
        t.Union[
            'models.ToolsOzoneHostingGetAccountHistory.AccountCreated',
            'models.ToolsOzoneHostingGetAccountHistory.EmailUpdated',
            'models.ToolsOzoneHostingGetAccountHistory.EmailConfirmed',
            'models.ToolsOzoneHostingGetAccountHistory.PasswordUpdated',
            'models.ToolsOzoneHostingGetAccountHistory.HandleUpdated',
        ],
        Field(discriminator='py_type'),
    ]  #: Details.

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#event'] = Field(
        default='tools.ozone.hosting.getAccountHistory#event', alias='$type', frozen=True
    )


class AccountCreated(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    email: t.Optional[str] = None  #: Email.
    handle: t.Optional[string_formats.Handle] = None  #: Handle.

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#accountCreated'] = Field(
        default='tools.ozone.hosting.getAccountHistory#accountCreated', alias='$type', frozen=True
    )


class EmailUpdated(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    email: str  #: Email.

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#emailUpdated'] = Field(
        default='tools.ozone.hosting.getAccountHistory#emailUpdated', alias='$type', frozen=True
    )


class EmailConfirmed(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    email: str  #: Email.

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#emailConfirmed'] = Field(
        default='tools.ozone.hosting.getAccountHistory#emailConfirmed', alias='$type', frozen=True
    )


class PasswordUpdated(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#passwordUpdated'] = Field(
        default='tools.ozone.hosting.getAccountHistory#passwordUpdated', alias='$type', frozen=True
    )


class HandleUpdated(base.ModelBase):
    """Definition model for :obj:`tools.ozone.hosting.getAccountHistory`."""

    handle: string_formats.Handle  #: Handle.

    py_type: t.Literal['tools.ozone.hosting.getAccountHistory#handleUpdated'] = Field(
        default='tools.ozone.hosting.getAccountHistory#handleUpdated', alias='$type', frozen=True
    )

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


class Option(base.ModelBase):
    """Definition model for :obj:`tools.ozone.setting.defs`."""

    created_by: string_formats.Did  #: Created by.
    did: string_formats.Did  #: Did.
    key: string_formats.Nsid  #: Key.
    last_updated_by: string_formats.Did  #: Last updated by.
    scope: t.Union[t.Literal['instance'], t.Literal['personal'], str]  #: Scope.
    value: 'UnknownType'  #: Value.
    created_at: t.Optional[string_formats.DateTime] = None  #: Created at.
    description: te.Annotated[t.Optional[str], Field(max_length=10240)] = None  #: Description.
    manager_role: t.Optional[
        t.Union[
            'models.ToolsOzoneTeamDefs.RoleModerator',
            'models.ToolsOzoneTeamDefs.RoleTriage',
            'models.ToolsOzoneTeamDefs.RoleAdmin',
            'models.ToolsOzoneTeamDefs.RoleVerifier',
            str,
        ]
    ] = None  #: Manager role.
    updated_at: t.Optional[string_formats.DateTime] = None  #: Updated at.

    py_type: t.Literal['tools.ozone.setting.defs#option'] = Field(
        default='tools.ozone.setting.defs#option', alias='$type', frozen=True
    )

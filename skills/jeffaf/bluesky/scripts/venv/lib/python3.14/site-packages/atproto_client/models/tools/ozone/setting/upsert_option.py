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
    from atproto_client.models.unknown_type import UnknownInputType
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.setting.upsertOption`."""

    key: string_formats.Nsid  #: Key.
    scope: t.Union[t.Literal['instance'], t.Literal['personal'], str]  #: Scope.
    value: 'UnknownInputType'  #: Value.
    description: te.Annotated[t.Optional[str], Field(max_length=2000)] = None  #: Description.
    manager_role: t.Optional[
        t.Union[
            'models.ToolsOzoneTeamDefs.RoleModerator',
            'models.ToolsOzoneTeamDefs.RoleTriage',
            'models.ToolsOzoneTeamDefs.RoleVerifier',
            'models.ToolsOzoneTeamDefs.RoleAdmin',
            str,
        ]
    ] = None  #: Manager role.


class DataDict(t.TypedDict):
    key: string_formats.Nsid  #: Key.
    scope: t.Union[t.Literal['instance'], t.Literal['personal'], str]  #: Scope.
    value: 'UnknownInputType'  #: Value.
    description: te.NotRequired[t.Optional[str]]  #: Description.
    manager_role: te.NotRequired[
        t.Optional[
            t.Union[
                'models.ToolsOzoneTeamDefs.RoleModerator',
                'models.ToolsOzoneTeamDefs.RoleTriage',
                'models.ToolsOzoneTeamDefs.RoleVerifier',
                'models.ToolsOzoneTeamDefs.RoleAdmin',
                str,
            ]
        ]
    ]  #: Manager role.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.setting.upsertOption`."""

    option: 'models.ToolsOzoneSettingDefs.Option'  #: Option.

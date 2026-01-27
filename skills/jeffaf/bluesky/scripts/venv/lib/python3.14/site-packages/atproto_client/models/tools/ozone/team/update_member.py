##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

from atproto_client.models import string_formats

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Data(base.DataModelBase):
    """Input data model for :obj:`tools.ozone.team.updateMember`."""

    did: string_formats.Did  #: Did.
    disabled: t.Optional[bool] = None  #: Disabled.
    role: t.Optional[
        t.Union[
            'models.ToolsOzoneTeamDefs.RoleAdmin',
            'models.ToolsOzoneTeamDefs.RoleModerator',
            'models.ToolsOzoneTeamDefs.RoleVerifier',
            'models.ToolsOzoneTeamDefs.RoleTriage',
            str,
        ]
    ] = None  #: Role.


class DataDict(t.TypedDict):
    did: string_formats.Did  #: Did.
    disabled: te.NotRequired[t.Optional[bool]]  #: Disabled.
    role: te.NotRequired[
        t.Optional[
            t.Union[
                'models.ToolsOzoneTeamDefs.RoleAdmin',
                'models.ToolsOzoneTeamDefs.RoleModerator',
                'models.ToolsOzoneTeamDefs.RoleVerifier',
                'models.ToolsOzoneTeamDefs.RoleTriage',
                str,
            ]
        ]
    ]  #: Role.

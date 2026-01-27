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
    """Output data model for :obj:`tools.ozone.server.getConfig`."""

    appview: t.Optional['models.ToolsOzoneServerGetConfig.ServiceConfig'] = None  #: Appview.
    blob_divert: t.Optional['models.ToolsOzoneServerGetConfig.ServiceConfig'] = None  #: Blob divert.
    chat: t.Optional['models.ToolsOzoneServerGetConfig.ServiceConfig'] = None  #: Chat.
    pds: t.Optional['models.ToolsOzoneServerGetConfig.ServiceConfig'] = None  #: Pds.
    verifier_did: t.Optional[string_formats.Did] = None  #: The did of the verifier used for verification.
    viewer: t.Optional['models.ToolsOzoneServerGetConfig.ViewerConfig'] = None  #: Viewer.


class ServiceConfig(base.ModelBase):
    """Definition model for :obj:`tools.ozone.server.getConfig`."""

    url: t.Optional[string_formats.Uri] = None  #: Url.

    py_type: t.Literal['tools.ozone.server.getConfig#serviceConfig'] = Field(
        default='tools.ozone.server.getConfig#serviceConfig', alias='$type', frozen=True
    )


class ViewerConfig(base.ModelBase):
    """Definition model for :obj:`tools.ozone.server.getConfig`."""

    role: t.Optional[
        t.Union[
            'models.ToolsOzoneTeamDefs.RoleAdmin',
            'models.ToolsOzoneTeamDefs.RoleModerator',
            'models.ToolsOzoneTeamDefs.RoleTriage',
            'models.ToolsOzoneTeamDefs.RoleVerifier',
            str,
        ]
    ] = None  #: Role.

    py_type: t.Literal['tools.ozone.server.getConfig#viewerConfig'] = Field(
        default='tools.ozone.server.getConfig#viewerConfig', alias='$type', frozen=True
    )

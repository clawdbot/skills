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
    """Parameters model for :obj:`tools.ozone.moderation.getRepos`."""

    dids: t.List[string_formats.Did] = Field(max_length=100)  #: Dids.


class ParamsDict(t.TypedDict):
    dids: t.List[string_formats.Did]  #: Dids.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`tools.ozone.moderation.getRepos`."""

    repos: t.List[
        te.Annotated[
            t.Union[
                'models.ToolsOzoneModerationDefs.RepoViewDetail', 'models.ToolsOzoneModerationDefs.RepoViewNotFound'
            ],
            Field(discriminator='py_type'),
        ]
    ]  #: Repos.

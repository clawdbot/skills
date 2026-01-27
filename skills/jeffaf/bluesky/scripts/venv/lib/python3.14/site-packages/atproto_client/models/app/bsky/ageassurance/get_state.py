##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.ageassurance.getState`."""

    country_code: str  #: Country code.
    region_code: t.Optional[str] = None  #: Region code.


class ParamsDict(t.TypedDict):
    country_code: str  #: Country code.
    region_code: te.NotRequired[t.Optional[str]]  #: Region code.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.ageassurance.getState`."""

    metadata: 'models.AppBskyAgeassuranceDefs.StateMetadata'  #: Metadata.
    state: 'models.AppBskyAgeassuranceDefs.State'  #: State.

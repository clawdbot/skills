##################################################################
# THIS IS THE AUTO-GENERATED CODE. DON'T EDIT IT BY HANDS!
# Copyright (C) 2024 Ilya (Marshal) <https://github.com/MarshalX>.
# This file is part of Python atproto SDK. Licenced under MIT.
##################################################################


import typing as t

import typing_extensions as te
from pydantic import Field

if t.TYPE_CHECKING:
    from atproto_client import models
from atproto_client.models import base


class Params(base.ParamsModelBase):
    """Parameters model for :obj:`app.bsky.unspecced.getSuggestedUsers`."""

    category: t.Optional[str] = None  #: Category of users to get suggestions for.
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=50)] = None  #: Limit.


class ParamsDict(t.TypedDict):
    category: te.NotRequired[t.Optional[str]]  #: Category of users to get suggestions for.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getSuggestedUsers`."""

    actors: t.List['models.AppBskyActorDefs.ProfileView']  #: Actors.

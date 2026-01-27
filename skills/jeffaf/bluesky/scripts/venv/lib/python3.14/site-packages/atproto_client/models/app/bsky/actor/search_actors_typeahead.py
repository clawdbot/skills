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
    """Parameters model for :obj:`app.bsky.actor.searchActorsTypeahead`."""

    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    q: t.Optional[str] = None  #: Search query prefix; not a full query string.
    term: t.Optional[str] = None  #: DEPRECATED: use 'q' instead.


class ParamsDict(t.TypedDict):
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    q: te.NotRequired[t.Optional[str]]  #: Search query prefix; not a full query string.
    term: te.NotRequired[t.Optional[str]]  #: DEPRECATED: use 'q' instead.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.actor.searchActorsTypeahead`."""

    actors: t.List['models.AppBskyActorDefs.ProfileViewBasic']  #: Actors.

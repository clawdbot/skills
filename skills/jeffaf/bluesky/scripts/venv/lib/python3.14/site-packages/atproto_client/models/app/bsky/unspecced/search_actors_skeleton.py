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
    """Parameters model for :obj:`app.bsky.unspecced.searchActorsSkeleton`."""

    q: str  #: Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended. For typeahead search, only simple term match is supported, not full syntax.
    cursor: t.Optional[str] = (
        None  #: Optional pagination mechanism; may not necessarily allow scrolling through entire result set.
    )
    limit: te.Annotated[t.Optional[int], Field(ge=1, le=100)] = None  #: Limit.
    typeahead: t.Optional[bool] = None  #: If true, acts as fast/simple 'typeahead' query.
    viewer: t.Optional[string_formats.Did] = (
        None  #: DID of the account making the request (not included for public/unauthenticated queries). Used to boost followed accounts in ranking.
    )


class ParamsDict(t.TypedDict):
    q: str  #: Search query string; syntax, phrase, boolean, and faceting is unspecified, but Lucene query syntax is recommended. For typeahead search, only simple term match is supported, not full syntax.
    cursor: te.NotRequired[
        t.Optional[str]
    ]  #: Optional pagination mechanism; may not necessarily allow scrolling through entire result set.
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    typeahead: te.NotRequired[t.Optional[bool]]  #: If true, acts as fast/simple 'typeahead' query.
    viewer: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: DID of the account making the request (not included for public/unauthenticated queries). Used to boost followed accounts in ranking.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.searchActorsSkeleton`."""

    actors: t.List['models.AppBskyUnspeccedDefs.SkeletonSearchActor']  #: Actors.
    cursor: t.Optional[str] = None  #: Cursor.
    hits_total: t.Optional[int] = (
        None  #: Count of search hits. Optional, may be rounded/truncated, and may not be possible to paginate through all hits.
    )

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
    """Parameters model for :obj:`app.bsky.unspecced.getTrendingTopics`."""

    limit: te.Annotated[t.Optional[int], Field(ge=1, le=25)] = None  #: Limit.
    viewer: t.Optional[string_formats.Did] = (
        None  #: DID of the account making the request (not included for public/unauthenticated queries). Used to boost followed accounts in ranking.
    )


class ParamsDict(t.TypedDict):
    limit: te.NotRequired[t.Optional[int]]  #: Limit.
    viewer: te.NotRequired[
        t.Optional[string_formats.Did]
    ]  #: DID of the account making the request (not included for public/unauthenticated queries). Used to boost followed accounts in ranking.


class Response(base.ResponseModelBase):
    """Output data model for :obj:`app.bsky.unspecced.getTrendingTopics`."""

    suggested: t.List['models.AppBskyUnspeccedDefs.TrendingTopic']  #: Suggested.
    topics: t.List['models.AppBskyUnspeccedDefs.TrendingTopic']  #: Topics.
